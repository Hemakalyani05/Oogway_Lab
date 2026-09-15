"""
Application configuration settings via Pydantic Settings.
"""
from typing import List, Optional
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # App Info
    PROJECT_NAME: str = "The Lenny Growth Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    # Database: Default standard SQLite or PostgreSQL
    DATABASE_URL: str = Field(
        default="sqlite:///./lenny_assistant.db",
        description="Database connection URL"
    )

    # LLM Providers Configuration
    DEFAULT_PROVIDER: str = "mock"  # Options: 'ollama', 'anthropic', 'openai', 'mock'
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # Cloud LLM Settings
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-7-sonnet-20250219"
    
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"

    # Retrieval & RAG
    TRANSCRIPTS_DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "transcripts"
    )
    TOP_K_RETRIEVAL: int = 5
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 80
    EMBEDDING_DIM: int = 384


settings = Settings()
