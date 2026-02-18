from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Retail DSS API"
    PROJECT_VERSION: str = "2.0.0"
    
    # Veritabanı
    # Varsayılan: SQLite (Sync) - Async için database.py içinde dönüşüm yapılacak.
    DATABASE_URL: str = "sqlite:///./retail.db"
    
    # Güvenlik & CORS
    SECRET_KEY: str = "supersecretkey"
    FRONTEND_URL: str = "http://localhost:5173"
    
    # AI & Dış Servisler
    GEMINI_API_KEY: str = ""
    WEATHER_API_KEY: str = ""
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://retail-dss-project.vercel.app"
    
    # Test Modu
    TESTING: bool = False
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
