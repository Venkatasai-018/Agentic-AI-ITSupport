"""
Configuration management for the IT Support System
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Agentic IT Support System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./it_support.db"
    
    # OpenAI (Optional)
    OPENAI_API_KEY: Optional[str] = None
    
    # Agent Configuration
    AUTO_RESOLVE_CONFIDENCE_THRESHOLD: float = 0.7
    MAX_RESOLUTION_ATTEMPTS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
