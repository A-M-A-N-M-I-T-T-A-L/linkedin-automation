from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # LinkedIn settings
    LINKEDIN_EMAIL: str
    LINKEDIN_PASSWORD: str
    
    # Application settings
    MAX_CONNECTIONS_PER_DAY: int = 20
    MAX_JOBS_TO_PARSE: int = 100
    LOG_LEVEL: str = "INFO"
    
    # Database settings
    DB_PATH: str = "data/vectors"
    DATA_DIR: str = "data"
    
    # LLM settings
    LLM_PROVIDER: str = "ollama"
    OLLAMA_MODEL: str = "llama2"
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
