from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from genai.schemas import GenerateParams
from genai.credentials import Credentials
from genai.model import Model
from genai.extensions.langchain import LangChainInterface
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chroma.setup_chroma import get_chunks_example
from .sql_llm import SqlLLmHandler
from .chat_llm import ChatAgentLlmHandler
from .llm import LLM
from db import DBHandler
import logging
from utils import convert_records_to_json, print_prompt, print_prompt_result

from dotenv import load_dotenv
import os

load_dotenv()

db = SQLDatabase.from_uri(f"postgresql://{os.getenv('HOST')}:{os.getenv('PORT')}/thingsboard?user={os.getenv('DB_USER')}&password={os.getenv('PASSWORD')}", include_tables=["device", "ts_kv", "ts_kv_latest", "ts_kv_dictionary"], sample_rows_in_table_info=3)
sql_llm = SqlLLmHandler()

logger = logging.getLogger()

db_handler = DBHandler(logger)
chat_llm = ChatAgentLlmHandler()

parameters = GenerateParams(decoding_method="greedy", max_new_tokens=1024, stop_sequences=[";"])
api_key = os.getenv("GENAI_KEY", None)
api_url = os.getenv("GENAI_API", None)
creds = Credentials(api_key, api_endpoint=api_url)
model = LangChainInterface(model='google/flan-ul2', credentials=creds, params=parameters)

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

Table Usage:
- 'device' table gives me information about a device
- 'ts_kv_dictionary' is a table that stores a mapping of specific keys and their id. These keys tell us what value is recorded in the 'ts_kv_latest' table
   For eg, if we need to filter on metrics we need to find the respective key ids of CO_Idling, HC, etc which can be found in the 'ts_kv_dictionary' table.
- 'ts_kv_latest' holds the records of what the device has measured along with the key id which maps to a specific region or metric in the 'ts_kv_dictionary' table.

Information:
- The tables are created such that you have to perform a join on all 3 tables when you are asked questions which require specific conditions.
- A device or vehicle is non compliant or in a failed state if it satisfies either one the below conditions
  CO_Idling > 0.3 OR HC > 200 OR CO_RPM > 0.2
- A device is said to belong to a specific region/state or city if City=city/state/region
- For time series or historical data use the ts_kv table for other queries use the ts_kv_latest

Examples:
{examples}

From the above examples choose the best query to answer the question. DO NOT ATTEMPT to skip where clauses.

Question: {input}"""


PROMPT = PromptTemplate(
    input_variables=["input",  "examples", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

async def get_sql_query_v2(input):
    examples = get_chunks_example(input)
    await db_handler.connect()
    chain = LLMChain(llm= model, prompt=PROMPT)
    result = chain.run(dict(input=input, examples=examples, table_info=db.get_table_info(), dialect=db.dialect))
    sql_query = sql_llm.parse_result(result)
    print(sql_query)
    try:
        llm_chat = LLM(chat_llm)
        dbResult = await db_handler.execute_query(sql_query)
        print(dbResult)
        result_json = convert_records_to_json(dbResult)
        print_prompt(chat_llm.get_prompt(input, result_json))
        chat_result = llm_chat.generate(input, result_json)
        print(chat_result)
        print_prompt_result(chat_result)
        return chat_llm.parse_result(chat_result)
    except Exception as e:
        print(e)
        return "I am unable to answer the question"