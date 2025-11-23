from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Request Schemas (Input)
class IngredientCreate(BaseModel):
    """Neue Zutat hinzufügen"""
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    expiry_date: Optional[datetime] = None
    is_permanent: bool = False

class IngredientUpdate(BaseModel):
    """Zutat aktualisieren (alle Felder optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    expiry_date: Optional[datetime] = None
    is_permanent: Optional[bool] = None

# Response Schema (Output)
class IngredientResponse(BaseModel):
    """Zutat-Info"""
    id: int
    user_id: int
    name: str
    category: Optional[str]
    expiry_date: Optional[datetime]
    is_permanent: bool
    added_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True