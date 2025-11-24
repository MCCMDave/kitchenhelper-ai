from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

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

    # CORS - Allowed Origins (comma-separated in .env)
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000"

    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """Settings Singleton - wird nur einmal geladen"""
    return Settings()

# Exportiere für einfachen Import
settings = get_settings()