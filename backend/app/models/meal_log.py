from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.utils.database import Base


class MealLog(Base):
    """
    Meal Log for tracking daily carb/KE intake
    Allows users to log consumed meals and track against daily limits
    """
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)  # Optional: Can log custom meals

    # Meal info
    meal_name = Column(String, nullable=False)
    meal_type = Column(String, nullable=True)  # "breakfast", "lunch", "dinner", "snack"
    servings = Column(Float, default=1.0)

    # Nutrition tracking
    carbs_grams = Column(Float, nullable=False)
    ke = Column(Float, nullable=False)
    be = Column(Float, nullable=False)
    calories = Column(Integer, nullable=True)
    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)

    # Timestamps
    consumed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    logged_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="meal_logs")
    recipe = relationship("Recipe", backref="meal_logs")

    def __repr__(self):
        return f"<MealLog(id={self.id}, user_id={self.user_id}, meal='{self.meal_name}', ke={self.ke})>"
