import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NeoFactory Industrial IoT Operations Platform"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    
    # Defaults to SQLite for local dev if Postgres isn't configured
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    
    # Feature Flags
    ENABLE_AI: bool = False
    ENABLE_ATTACK_ENGINE: bool = False
    ENABLE_REPLAY: bool = False
    ENABLE_ANALYTICS: bool = False
    ENABLE_CYBER_RANGE: bool = False
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    class Config:
        case_sensitive = True

settings = Settings()

if settings.POSTGRES_SERVER:
    settings.SQLALCHEMY_DATABASE_URI = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:5432/{settings.POSTGRES_DB}"
elif not settings.SQLALCHEMY_DATABASE_URI:
    settings.SQLALCHEMY_DATABASE_URI = "sqlite:///./neofactory.db"
