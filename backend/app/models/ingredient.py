from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Ingredient(Base):
    """Ingredient Model - Zutaten des Users"""
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Zutat-Details
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)  # Gemüse, Fleisch, Gewürze, etc.
    quantity = Column(Float, nullable=True)  # Menge: 500, 1.5, etc.
    unit = Column(String, nullable=True)  # Einheit: g, kg, ml, l, Stück, TL, EL
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    is_permanent = Column(Boolean, default=False)  # z.B. Salz, Gewürze
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="ingredients")
    
    def __repr__(self):
        return f"<Ingredient(name='{self.name}', category='{self.category}')>"