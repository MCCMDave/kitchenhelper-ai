from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# ORDNER AUTOMATISCH ERSTELLEN
def ensure_database_directory():
    """Stelle sicher, dass der database-Ordner existiert"""
    # Extrahiere den Ordnerpfad aus der DATABASE_URL
    if settings.DATABASE_URL.startswith("sqlite"):
        # sqlite:///./database/kitchenhelper.db → database/kitchenhelper.db
        db_path = settings.DATABASE_URL.replace("sqlite:///./", "")
        db_dir = os.path.dirname(db_path)
        
        # Erstelle Ordner, falls nicht vorhanden
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"[OK] Created directory: {db_dir}")

# Ordner erstellen VOR Engine-Erstellung
ensure_database_directory()

# SQLAlchemy Engine erstellen
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Rest bleibt gleich...
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Datenbank-Tabellen erstellen"""
    from app.models import user, ingredient, recipe, favorite, diet_profile
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created!")