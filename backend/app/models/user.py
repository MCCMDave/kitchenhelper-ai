from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base
import enum

class SubscriptionTier(str, enum.Enum):
    """Subscription Levels"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    PRO = "pro"
    BUSINESS_SOLO = "business_solo"
    BUSINESS_TEAM = "business_team"
    BUSINESS_PRAXIS = "business_praxis"

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
        default=SubscriptionTier.FREE,
        nullable=False
    )
    stripe_customer_id = Column(String, nullable=True)

    # Admin Override (alle Features kostenlos)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Email Verification
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)

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
        if self.is_admin:
            return 999999  # Admin = unbegrenzt

        limits = {
            SubscriptionTier.FREE: 999999,  # Unbegrenzt (aber langsam)
            SubscriptionTier.BASIC: 999999,
            SubscriptionTier.PREMIUM: 999999,
            SubscriptionTier.PRO: 999999,
            SubscriptionTier.BUSINESS_SOLO: 999999,
            SubscriptionTier.BUSINESS_TEAM: 999999,
            SubscriptionTier.BUSINESS_PRAXIS: 999999
        }
        return limits.get(self.subscription_tier, 999999)

    @property
    def max_favorites(self) -> int:
        """Favoriten-Limit basierend auf Tier"""
        if self.is_admin:
            return 999999

        limits = {
            SubscriptionTier.FREE: 10,
            SubscriptionTier.BASIC: 999999,
            SubscriptionTier.PREMIUM: 999999,
            SubscriptionTier.PRO: 999999,
            SubscriptionTier.BUSINESS_SOLO: 999999,
            SubscriptionTier.BUSINESS_TEAM: 999999,
            SubscriptionTier.BUSINESS_PRAXIS: 999999
        }
        return limits.get(self.subscription_tier, 10)

    def has_feature(self, feature: str) -> bool:
        """Prüft ob User Zugriff auf Feature hat"""
        if self.is_admin:
            return True  # Admin hat alle Features

        feature_access = {
            # FREE Tier
            "recipe_generation": [SubscriptionTier.FREE, SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "basic_nutrition": [SubscriptionTier.FREE, SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "be_calculation": [SubscriptionTier.FREE, SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "pdf_export_favorites": [SubscriptionTier.FREE, SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],

            # BASIC Tier+
            "recipe_db": [SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "gi_gl": [SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "pdf_export_all": [SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "shopping_lists": [SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],

            # PREMIUM Tier+
            "meal_planning": [SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "carb_budget": [SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "advanced_filters": [SubscriptionTier.PREMIUM, SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],

            # PRO Tier+
            "api_access": [SubscriptionTier.PRO, SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "team_sharing": [SubscriptionTier.PRO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "white_label": [SubscriptionTier.PRO, SubscriptionTier.BUSINESS_PRAXIS],

            # BUSINESS Tiers
            "sla_guarantee": [SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "priority_support": [SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
            "invoice_billing": [SubscriptionTier.BUSINESS_SOLO, SubscriptionTier.BUSINESS_TEAM, SubscriptionTier.BUSINESS_PRAXIS],
        }

        allowed_tiers = feature_access.get(feature, [])
        return self.subscription_tier in allowed_tiers