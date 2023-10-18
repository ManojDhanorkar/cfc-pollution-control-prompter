import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from datetime import datetime
from llm.sql_chain import answer_query_with_sql
from llm.sql_chain_v2 import get_sql_query_v2
import logging 
import requests as req
import os

load_dotenv()

#now we will Create and configure logger 
logging.basicConfig(filename="prompter2.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

#Let us Create an object 
logger=logging.getLogger() 
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

key = os.environ['IBMAPI_KEY']

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/get")
# def get_bot_response(request: Request):
#     userText = request.query_params.get("msg")
#     print("user", userText)
#     result = get_response(userText)
#     return result
    #return str(get_english_response(userText))

def get_response(userText):
    question_in_english=get_english_response(userText)
    '''get_sql()
    execute_sql()
    use_value_inresponse()'''
    response = send_hindi_response(question_in_english)
    #response = "Your question is - " + userText
    return response

def get_english_input(userText):
    # Define new data to create
    new_data = {  
        "model_id": "tiiuae/falcon-40b",
        "inputs": [userText],
        "parameters": {"decoding_method": "greedy",
                        "stop_sequences": [      ".",      "?"    ],
                        "min_new_tokens": 1,
                        "max_new_tokens": 500,
                        "moderations": {"hap": {"input": "true",
                                                "threshold": 0.75, 
                                                "output": "true" }
                        }}, 
                "template": {    "id": "prompt_builder", 
                "data": {      "instruction": "please translate from hindi to english", 
                    "input_prefix": "Hindi:",  
                    "output_prefix": "English:", 
                    "examples": [ { "input": "आप अपने वाहन को पीयूसी के लिए कैसे प्रमाणित करते हैं?",
                                    "output": "how do you certify your vehicle for PUC?"},
                                    { "input": "आज तक ऐसे कितने वाहन हैं जो नियमों का पालन नहीं कर रहे हैं?",
                                    "output": "How many vehicles are there as of today that are non compliant?"
                                    }]} 
    }}
    # The API endpoint to communicate with
    url_post = "https://bam-api.res.ibm.com/v1/generate"
    # Set up the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }
    # A POST request to tthe API
    post_response = req.post(url_post, headers=headers, json=new_data)
    # Print the response
    post_response_json = post_response.json()
    logger.info("hindi to english")
    logger.info(post_response)
    logger.info(post_response_json)
    logger.info(post_response_json['results'])
    response = post_response_json['results'][0]['generated_text'].partition("Hindi")
    logger.info(response[0])
    return response[0]

def get_hindi_output(userText):
    # Define new data to create
    new_data = {  
        "model_id": "tiiuae/falcon-40b",
        "inputs": [userText],
        "parameters": {"decoding_method": "greedy",
                        "stop_sequences": [      ".",      "?"    ],
                        "min_new_tokens": 1,
                        "max_new_tokens": 500,
                        "moderations": {"hap": {"input": "true",
                                                "threshold": 0.75, 
                                                "output": "true" }
                        }}, 
                "template": {    "id": "prompt_builder", 
                "data": {      "instruction": "please translate from english to hindi", 
                    "input_prefix": "English:",  
                    "output_prefix": "Hindi:", 
                    "examples": [ { "input": "My vehicle is not PUC certified.",
                              "output": "मेरा वाहन पीयूसी प्रमाणित नहीं है।" },                              
                              { "input": "There are 36 vehicles that are non compliant as of today.",
                              "output": "आज तक 36 वाहन ऐसे हैं जो नियमों का अनुपालन नहीं कर रहे हैं।" }]} 
    }}
    # The API endpoint to communicate with
    url_post = "https://bam-api.res.ibm.com/v1/generate"
    # Set up the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key 
    }
    # A POST request to tthe API
    post_response = req.post(url_post, headers=headers, json=new_data)
    # Print the response
    post_response_json = post_response.json()
    logger.info("english to hindi")    
    logger.info(post_response_json['results'])
    response = post_response_json['results'][0]['generated_text']
    return response

################################## DB & LLM ###########################

@app.get("/get")
async def query(request: Request):
    try:
        # BUILD ANSWERING CHAIN HERE           
        #logger.info(f"Starting.........: {msg}")    
        #input= get_english_input("msg") 
        #logger.info(f"Starting.........: {input}") 
        q = request.query_params.get("msg")
        logger.info(f"Starting chain for query: {q}")
        input= get_english_input(q) 
        logger.info(f"Starting.........: {input}")
        result = await get_sql_query_v2(input)
        logger.info(f"Starting.........: {result}")   
        response=get_hindi_output(result)
        return response
        #return result
    except Exception as e:
        return str(e)
    
@app.get("/testsql")
async def testsql():
    try:
        query="Give me a count of non compliant PUCs"
        res = await get_sql_query_v2(query)
        return res
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    #Now we are going to Set the threshold of logger to DEBUG 
    logger.setLevel(logging.INFO)     
    logger.info("PUC Prompter: This is just an information for you")
    print("Server started on port ", 5002)
    uvicorn.run(app, host='0.0.0.0', port=5002, log_config=None)

