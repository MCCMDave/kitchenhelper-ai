from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Recipe(Base):
    """Recipe Model - Generierte Rezepte"""
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Rezept-Basis
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(Integer, default=2)  # 1-5
    cooking_time = Column(String, nullable=True)  # z.B. "30 Min"
    method = Column(String, nullable=True)  # Pfanne, Ofen, etc.
    servings = Column(Integer, default=2)
    
    # JSON-Felder (als Text gespeichert)
    used_ingredients = Column(Text, nullable=True)  # JSON Array
    leftover_tips = Column(Text, nullable=True)
    ingredients_json = Column(Text, nullable=True)  # Vollständige Zutatenliste mit Mengen
    nutrition_json = Column(Text, nullable=True)  # Nährwerte pro Portion
    
    # Metadata
    ai_provider = Column(String, default="mock")  # mock, anthropic, openai, gemini
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recipes")
    favorites = relationship("Favorite", back_populates="recipe", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Recipe(name='{self.name}', user_id={self.user_id})>"