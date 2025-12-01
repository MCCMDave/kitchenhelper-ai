from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base
import enum

class SubscriptionTier(str, enum.Enum):
    """Subscription Levels"""
    DEMO = "demo"
    BASIC = "basic"
    PREMIUM = "premium"

class User(Base):
    """User Model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    emoji = Column(String, default="👤", nullable=True)
    
    # Subscription
    subscription_tier = Column(
        Enum(SubscriptionTier), 
        default=SubscriptionTier.DEMO,
        nullable=False
    )
    stripe_customer_id = Column(String, nullable=True)
    
    # Limits
    daily_recipe_count = Column(Integer, default=0)
    last_recipe_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ingredients = relationship("Ingredient", back_populates="user", cascade="all, delete-orphan")
    recipes = relationship("Recipe", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    diet_profiles = relationship("DietProfile", back_populates="user", cascade="all, delete-orphan")
    meal_logs = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', tier='{self.subscription_tier}')>"
    
    @property
    def daily_limit(self) -> int:
        """Tageslimit basierend auf Tier"""
        limits = {
            SubscriptionTier.DEMO: 3,
            SubscriptionTier.BASIC: 50,
            SubscriptionTier.PREMIUM: 999999  # "Unbegrenzt"
        }
        return limits.get(self.subscription_tier, 3)