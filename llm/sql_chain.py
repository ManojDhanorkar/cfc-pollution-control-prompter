from db import DBHandler
from .sql_llm import SqlLLmHandler
from .chat_llm import ChatAgentLlmHandler
from .llm import LLM
from utils import convert_records_to_json, print_prompt, print_prompt_result
import logging

logger = logging.getLogger()

db_handler = DBHandler(logger)
sql_llm = SqlLLmHandler()
chat_llm = ChatAgentLlmHandler()

async def answer_query_with_sql(query):
    await db_handler.connect()
    llm  = LLM(sql_llm)
    print_prompt(sql_llm.get_prompt(query))
    llm_result = llm.generate(query)
    print_prompt_result(llm_result)
    sqlQuery = sql_llm.parse_result(llm_result)
    try:
        llm_chat = LLM(chat_llm)
        dbResult = await db_handler.execute_query(sqlQuery)
        result_json = convert_records_to_json(dbResult)
        print_prompt(chat_llm.get_prompt(result_json))
        chat_result = llm_chat.generate(result_json)
        print_prompt_result(chat_result)
        return chat_result
    except Exception as e:
        print(e)
        return "I am unable to answer the question"