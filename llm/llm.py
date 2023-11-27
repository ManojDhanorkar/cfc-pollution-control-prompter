import os
from genai.credentials import Credentials
from genai.model import Model

class LLM:
    def __init__(self, llmHandler=None):
        if llmHandler is None:
            raise ValueError("Please provide instances of LLMHandler")
        api_key = os.getenv("GENAI_KEY", None)
        api_url = os.getenv("GENAI_API", None)
        creds = Credentials(api_key, api_endpoint=api_url)
        self.llmHandler = llmHandler
        self.model = Model(llmHandler.model_type, params=llmHandler.parameters, credentials=creds)

    def set_prompt(self, prompt):
        self.prompt = prompt

    def generate(self, input, result):
        prompt = self.llmHandler.get_prompt(input, result)
        prompt_result = self.model.generate([prompt])
        return prompt_result[0].generated_text
