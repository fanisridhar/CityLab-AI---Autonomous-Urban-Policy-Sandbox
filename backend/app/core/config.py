"""
Application configuration using Pydantic settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Database
    DATABASE_URL: str = "postgresql://citylab:citylab_password@localhost:5432/citylab_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM APIs
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Vector DB
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    USE_PINECONE: bool = False  # Set to True to use Pinecone instead of Chroma
    
    # Simulation Settings
    SIMULATION_TICK_INTERVAL: int = 60  # seconds per simulation tick
    MAX_SIMULATION_DAYS: int = 30
    DEFAULT_AGENT_COUNT: int = 100
    
    # Data paths
    DATA_DIR: Path = Path("./data")
    RAW_DATA_DIR: Path = Path("./data/raw")
    PROCESSED_DATA_DIR: Path = Path("./data/processed")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create singleton instance
settings = Settings()

# Create data directories if they don't exist
settings.DATA_DIR.mkdir(exist_ok=True)
settings.RAW_DATA_DIR.mkdir(exist_ok=True)
settings.PROCESSED_DATA_DIR.mkdir(exist_ok=True)
