from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base


class DietProfile(Base):
    """DietProfile Model - Ernaehrungsprofile des Users (Diabetes, Keto, Vegan, etc.)"""
    __tablename__ = "diet_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Profile Type
    profile_type = Column(String, nullable=False)
    # Moegliche Werte: "diabetic", "keto", "vegan", "vegetarian",
    #                  "low_carb", "high_protein", "gluten_free", "lactose_free"

    name = Column(String, nullable=False)  # Custom Name vom User
    is_active = Column(Boolean, default=True)

    # Settings als JSON (flexibel fuer verschiedene Profile)
    settings_json = Column(Text, nullable=True)
    # Beispiel Diabetes: {"unit": "KE", "daily_carb_limit": 180}
    # Beispiel Keto: {"daily_carb_limit": 50, "daily_fat_min": 150}

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="diet_profiles")

    # Unique Constraint: User kann nicht zweimal gleichen profile_type + name haben
    __table_args__ = (
        UniqueConstraint('user_id', 'profile_type', 'name', name='unique_user_profile_type_name'),
    )

    def __repr__(self):
        return f"<DietProfile(user_id={self.user_id}, type='{self.profile_type}', name='{self.name}')>"
