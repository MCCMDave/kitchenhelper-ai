from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict

# Request Schemas (Input)
class RecipeGenerateRequest(BaseModel):
    """Recipe generation request"""
    ingredient_ids: List[int] = Field(..., min_length=1, description="IDs of available ingredients")
    ai_provider: str = Field(default="mock", description="mock, anthropic, openai, gemini")
    diet_profiles: List[str] = Field(default=[], description="e.g. ['diabetic', 'vegan']")
    diabetes_unit: Optional[str] = Field(default="KE", description="BE or KE")
    servings: int = Field(default=2, ge=1, le=10, description="Number of servings")
    language: str = Field(default="en", description="Recipe language: en or de")

# Nested Schemas für Recipe Response
class RecipeIngredient(BaseModel):
    """Einzelne Zutat im Rezept"""
    name: str
    amount: str
    carbs: Optional[float] = None

class NutritionInfo(BaseModel):
    """Nährwerte pro Portion"""
    calories: int
    protein: float
    carbs: float
    fat: float
    ke: Optional[float] = None
    be: Optional[float] = None

# Response Schema (Output)
class RecipeResponse(BaseModel):
    """Vollständiges Rezept"""
    id: int
    user_id: int
    name: str
    description: Optional[str]
    difficulty: int
    cooking_time: Optional[str]
    method: Optional[str]
    servings: int
    
    # Parsed JSON fields
    used_ingredients: List[str]
    leftover_tips: Optional[str]
    ingredients: List[RecipeIngredient]
    nutrition_per_serving: NutritionInfo
    
    # Metadata
    ai_provider: str
    generated_at: datetime
    
    class Config:
        from_attributes = True

class RecipeListResponse(BaseModel):
    """Response für /generate mit mehreren Rezepten"""
    recipes: List[RecipeResponse]
    count: int
    daily_count_remaining: int
    message: Optional[str] = None