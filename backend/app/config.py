from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import secrets
import sys

class Settings(BaseSettings):
    """App-Konfiguration"""

    # Database
    DATABASE_URL: str = "sqlite:///./database/kitchenhelper.db"

    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-key-CHANGE-THIS-IN-PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 Stunde (Balance: UX vs Security)

    # App
    APP_NAME: str = "KitchenHelper-AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # Sicherer Default - In .env auf True setzen für Development

    # CORS - Allowed Origins (comma-separated in .env)
    ALLOWED_ORIGINS: str = "https://kitchenhelper-ai.de,https://kitchen.kitchenhelper-ai.de,http://192.168.2.54:8081,http://100.103.86.47:8081,http://localhost:8081,http://127.0.0.1:8081"

    # AI Providers
    GOOGLE_AI_API_KEY: str = ""  # Gemini API Key (Pro users)
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    OLLAMA_BASE_URL: str = "http://localhost:11434"  # Local Ollama
    OLLAMA_MODEL: str = "llama3.2"

    # Email (Resend.com)
    RESEND_API_KEY: str = ""  # Resend API Key (get from resend.com)
    RESEND_FROM_EMAIL: str = "KitchenHelper <noreply@yourdomain.com>"  # Change after domain verification
    RESEND_REPLY_TO: str = "studio.del.melucio@gmail.com"  # Studio email for gaming/entertainment
    FRONTEND_BASE_URL: str = "http://192.168.2.54:8081"  # Frontend URL for email links
    FRONTEND_URL: str = "http://192.168.2.54:8081"  # Alias for compatibility

    # Stripe (Payment)
    STRIPE_SECRET_KEY: str = ""  # Stripe Secret Key (get from stripe.com)
    STRIPE_PUBLISHABLE_KEY: str = ""  # Stripe Publishable Key
    STRIPE_WEBHOOK_SECRET: str = ""  # Stripe Webhook Secret (for webhook signature verification)

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
    settings_instance = Settings()

    # Security Warning: Check for default JWT_SECRET_KEY
    if settings_instance.JWT_SECRET_KEY == "your-super-secret-key-CHANGE-THIS-IN-PRODUCTION":
        print("\n" + "="*70)
        print("⚠️  SECURITY WARNING: Using default JWT_SECRET_KEY!")
        print("="*70)
        print("CRITICAL: Change JWT_SECRET_KEY in .env file before deployment!")
        print("Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'")
        print("="*70 + "\n")

        # Exit in production mode (wenn DEBUG=False)
        if not settings_instance.DEBUG:
            print("❌ FATAL: Cannot start in production with default JWT_SECRET_KEY!")
            sys.exit(1)

    return settings_instance

# Exportiere für einfachen Import
settings = get_settings()