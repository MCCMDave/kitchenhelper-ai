from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Embedded Recipe Ingredient
class RecipeIngredientInfo(BaseModel):
    """Einzelne Zutat im Rezept"""
    name: str
    amount: str
    carbs: Optional[float] = None

# Embedded Nutrition Info
class NutritionInfoEmbed(BaseModel):
    """Naehrwerte pro Portion"""
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    ke: Optional[float] = None
    be: Optional[float] = None

# Embedded Recipe Info - VOLLSTAENDIG fuer Favorite Response
class RecipeInfo(BaseModel):
    """Vollstaendige Recipe-Infos fuer Favorite Response"""
    id: int
    name: str
    description: Optional[str] = None
    difficulty: int = 2
    cooking_time: Optional[str] = None
    method: Optional[str] = None
    servings: int = 2

    # Vollstaendige Rezeptdaten
    used_ingredients: Optional[List[str]] = []
    leftover_tips: Optional[str] = None
    ingredients: Optional[List[RecipeIngredientInfo]] = []
    nutrition_per_serving: Optional[NutritionInfoEmbed] = None

    # Metadata
    ai_provider: Optional[str] = "mock"
    generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Request Schema (Input)
class FavoriteCreate(BaseModel):
    """Rezept favorisieren Request"""
    recipe_id: int = Field(..., description="ID des Rezepts zum Favorisieren")

# Response Schemas (Output)
class FavoriteResponse(BaseModel):
    """Einzelner Favorit mit Recipe-Info"""
    id: int
    user_id: int
    recipe_id: int
    added_at: datetime
    recipe: Optional[RecipeInfo] = None

    class Config:
        from_attributes = True

class FavoriteListResponse(BaseModel):
    """Liste aller Favoriten"""
    favorites: List[FavoriteResponse]
    count: int
