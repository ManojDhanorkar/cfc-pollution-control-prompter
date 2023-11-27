class LLMHandler:
    def __init__(self, model_type, parameters):
        self.model_type = model_type
        self.parameters = parameters
        
    def get_prompt(self, query):
        # Some code to handle the loose string
        raise NotImplementedError
    
    def parse_result(self, query):
        return query