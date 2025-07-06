from abc import ABC , abstractmethod
from src.Helpers.config import get_settings



class BaseLLMFactory(ABC):
    def __init__(self):
        self.settings = get_settings()

    @abstractmethod
    def create_llm_provider(self ,llm_name : str):
        pass
        
