import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw"
    DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    DB_PATH: Path = BASE_DIR / "db" / "storage"
    INDEX_JSON: Path = BASE_DIR / "data" / "index.json"

    # Vector DB Settings
    QDRANT_COLLECTION: str = "memora_knowledge"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # LLM Settings
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # RAG Settings
    CHUNK_SIZE: int = 300  # words
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
settings.DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
settings.DB_PATH.mkdir(parents=True, exist_ok=True)
