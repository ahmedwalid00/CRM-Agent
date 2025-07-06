from abc import ABC, abstractmethod
from src.Helpers.config import  get_settings

class BaseProvider(ABC):
    def __init__(self):
        self._settings = get_settings()

    @abstractmethod
    def initialize_llm(self):
        pass

    @property
    @abstractmethod
    def llm(self):
        pass

    @abstractmethod
    async def initialize_llm_mcptools(self, mcp_config: dict):
        """Initialize the provider with LLM and tools"""
        pass

    @property
    @abstractmethod
    def llm_with_tools(self):
        """Return the LLM instance with tools bound"""
        pass

    @property
    @abstractmethod
    def tools(self):
        """expose tools if needed separately"""
        pass
