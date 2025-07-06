import threading
from pydantic_settings import BaseSettings
from typing import List, Optional

_lock = threading.Lock()
_instance = None

class Settings(BaseSettings):
    """
    A singleton Pydantic settings class that loads from .env.
    """
    def __new__(cls, *args, **kwargs):
        global _instance
        if _instance is None:
            with _lock:
                if _instance is None:
                    _instance = super().__new__(cls)
        return _instance

    # --- General App Settings ---
    APP_NAME: str
    OPENAI_API_KEY: str
    OPENAI_API_URL: Optional[str] = None
    GENERATION_MODEL_ID_LITERAL: List[str]
    GENERATION_MODEL_ID: str
    INPUT_DAFAULT_MAX_CHARACTERS: int
    GENERATION_DAFAULT_MAX_TOKENS: int
    GENERATION_DAFAULT_TEMPERATURE: float
    GENERATION_BACKEND : str

    # --- MCP Required Settings ---
    SUPABASE_URI: Optional[str] = None
    SUPABASE_PASSWORD: Optional[str] = None 
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_TEAM_ID: Optional[str] = None
        
    class Config:
        env_file = ".env"
        env_nested_delimiter = '__'

def get_settings() -> Settings:
    """Returns the singleton instance of the Settings class."""
    return Settings()