from genai.schemas import GenerateParams
from .llm_handler import LLMHandler

class ChatAgentLlmHandler(LLMHandler):
    def __init__(self):
        parmaeters = GenerateParams(decoding_method="greedy", max_new_tokens=1024, repetition_penalty=1.5)
        super().__init__(model_type='tiiuae/falcon-40b', parameters=parmaeters)

    def get_prompt(self, input, result):
        return (f"""
Context: ```json
{result}
```
You are a pollution control assistant. Do not answer in code or json. You can use csv to represent arrays. 
Once you reply do not generate anything else. Give the answer in back ticks without any language type.
The answer should at least be one sentence long and not just numbers.
From the above context and no prior knowledge answer the question in plain english.
Question: {input}
Reply:""")
    
    def parse_result(self, query):
        new_str = query.strip().strip('`')
        print(new_str)
        return new_str