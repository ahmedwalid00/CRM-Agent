from abc import ABC , abstractmethod
from src.Helpers.config import get_settings


class BaseLLMBuilder(ABC):
    def __init__(self):
        self._settings = get_settings()

    @abstractmethod
    def build_llm(self):
        pass
