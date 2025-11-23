from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


# Request Schemas (Input)
class DietProfileCreate(BaseModel):
    """Neues Diet Profile erstellen"""
    profile_type: str = Field(..., description="diabetic, keto, vegan, vegetarian, low_carb, high_protein, gluten_free, lactose_free")
    name: str = Field(..., min_length=1, max_length=100, description="Custom Name fuer das Profil")
    settings: Optional[Dict[str, Any]] = Field(default={}, description="Profil-spezifische Einstellungen")
    is_active: bool = Field(default=True, description="Profil aktiv?")


class DietProfileUpdate(BaseModel):
    """Diet Profile bearbeiten"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


# Response Schemas (Output)
class DietProfileResponse(BaseModel):
    """Einzelnes Diet Profile"""
    id: int
    user_id: int
    profile_type: str
    name: str
    settings: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class DietProfileListResponse(BaseModel):
    """Liste aller Diet Profiles"""
    profiles: List[DietProfileResponse]
    count: int
    active_count: int
