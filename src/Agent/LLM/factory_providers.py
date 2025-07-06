from src.Agent.LLM.base_factory_provider import BaseLLMFactory
from src.Agent.LLM.LLMProviders.openai_provider import OpenaiProvider

class LLMFactory(BaseLLMFactory):

    def __init__(self):
        super().__init__()

    def create_llm_provider(self,llm_name : str):    
        if(llm_name == "OPENAI"):
            return OpenaiProvider()
        
        return None