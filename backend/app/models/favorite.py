from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Favorite(Base):
    """Favorite Model - Favorisierte Rezepte des Users"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)

    # Timestamp
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorites")

    # Unique Constraint: Ein User kann ein Rezept nur einmal favorisieren
    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_favorite'),
    )

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, recipe_id={self.recipe_id})>"
