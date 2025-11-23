from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """App-Konfiguration"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./database/kitchenhelper.db"
    
    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-key-CHANGE-THIS-IN-PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    APP_NAME: str = "KitchenHelper-AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """Settings Singleton - wird nur einmal geladen"""
    return Settings()

# Exportiere für einfachen Import
settings = get_settings()