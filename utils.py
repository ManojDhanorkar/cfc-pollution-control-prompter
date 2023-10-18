import logging

logger = logging.getLogger()

def convert_records_to_json(records):
    result = []
    for record in records:
        json_record = {}
        for key, value in record.items():
            json_record[key] = value
        result.append(json_record)
    return result

def print_prompt(prompt):
    logger.info(f"========PROMPT============\n{prompt}\n========================")

def print_prompt_result(result):
    logger.info(f"==========LLM RESULT=======\n{result}\n===================")