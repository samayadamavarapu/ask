import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Ask Me Anything About Yoga"
    VERSION: str = "1.0.0"
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "yoga_rag_db"
    
    # Vector Store
    CHROMA_PERSIST_DIRECTORY: str = "data/chroma_db"
    
    # Embeddings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # LLM
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-3.5-turbo" # or gpt-4
    
    # RAG Settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 3
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
