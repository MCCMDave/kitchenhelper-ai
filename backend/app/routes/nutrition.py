# Nutrition Routes - OpenFoodFacts API Integration
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from app.services.nutrition_service import nutrition_service
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


class NutritionResponse(BaseModel):
    """Nutrition data for an ingredient"""
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None
    per: str = "100g"
    source: str
    ke: Optional[float] = None  # Kohlenhydrateinheit (10g carbs)
    be: Optional[float] = None  # Broteinheit (12g carbs)


class BulkNutritionRequest(BaseModel):
    """Request for multiple ingredients"""
    ingredients: List[str]


class BulkNutritionResponse(BaseModel):
    """Response with nutrition for multiple ingredients"""
    items: List[NutritionResponse]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    total_ke: float
    total_be: float


@router.get("/lookup", response_model=NutritionResponse)
def lookup_nutrition(
    ingredient: str = Query(..., min_length=2, description="Ingredient name"),
    current_user: User = Depends(get_current_user)
):
    """
    Look up nutrition information for a single ingredient.

    Uses OpenFoodFacts database with fallback values for common ingredients.

    - **ingredient**: Name of the ingredient (e.g., "tomato", "chicken breast")

    Returns nutrition per 100g.
    """
    data = nutrition_service.get_nutrition_sync(ingredient)

    carbs = data.get('carbs', 0)

    return NutritionResponse(
        name=data.get('name', ingredient),
        calories=data.get('calories', 0),
        protein=data.get('protein', 0),
        carbs=carbs,
        fat=data.get('fat', 0),
        fiber=data.get('fiber'),
        per=data.get('per', '100g'),
        source=data.get('source', 'unknown'),
        ke=round(carbs / 10, 1) if carbs else None,
        be=round(carbs / 12, 1) if carbs else None
    )


@router.post("/bulk", response_model=BulkNutritionResponse)
def bulk_lookup_nutrition(
    request: BulkNutritionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Look up nutrition information for multiple ingredients.

    - **ingredients**: List of ingredient names

    Returns individual nutrition per 100g and totals.
    """
    if len(request.ingredients) > 50:
        raise HTTPException(
            status_code=400,
            detail="Maximum 50 ingredients per request"
        )

    items = []
    totals = {
        'calories': 0,
        'protein': 0.0,
        'carbs': 0.0,
        'fat': 0.0
    }

    for ingredient in request.ingredients:
        data = nutrition_service.get_nutrition_sync(ingredient)
        carbs = data.get('carbs', 0)

        item = NutritionResponse(
            name=data.get('name', ingredient),
            calories=data.get('calories', 0),
            protein=data.get('protein', 0),
            carbs=carbs,
            fat=data.get('fat', 0),
            fiber=data.get('fiber'),
            per=data.get('per', '100g'),
            source=data.get('source', 'unknown'),
            ke=round(carbs / 10, 1) if carbs else None,
            be=round(carbs / 12, 1) if carbs else None
        )
        items.append(item)

        totals['calories'] += data.get('calories', 0)
        totals['protein'] += data.get('protein', 0)
        totals['carbs'] += carbs
        totals['fat'] += data.get('fat', 0)

    return BulkNutritionResponse(
        items=items,
        total_calories=int(totals['calories']),
        total_protein=round(totals['protein'], 1),
        total_carbs=round(totals['carbs'], 1),
        total_fat=round(totals['fat'], 1),
        total_ke=round(totals['carbs'] / 10, 1),
        total_be=round(totals['carbs'] / 12, 1)
    )


@router.get("/calculate-meal")
def calculate_meal_nutrition(
    ingredients: str = Query(..., description="Comma-separated: 'ingredient:amount' (e.g., 'chicken:150g,rice:200g')"),
    servings: int = Query(default=1, ge=1, le=10),
    current_user: User = Depends(get_current_user)
):
    """
    Calculate nutrition for a meal with specific amounts.

    - **ingredients**: Comma-separated ingredient:amount pairs
    - **servings**: Number of servings to divide by

    Example: `chicken:150g,rice:200g,broccoli:100g`
    """
    # Parse ingredients
    ingredient_list = []
    for item in ingredients.split(','):
        parts = item.strip().split(':')
        if len(parts) == 2:
            ingredient_list.append({
                'name': parts[0].strip(),
                'amount': parts[1].strip()
            })
        else:
            ingredient_list.append({
                'name': parts[0].strip(),
                'amount': '100g'
            })

    if not ingredient_list:
        raise HTTPException(
            status_code=400,
            detail="No valid ingredients provided"
        )

    # Calculate nutrition
    nutrition = nutrition_service.calculate_recipe_nutrition(
        ingredient_list,
        servings
    )

    return {
        "servings": servings,
        "per_serving": nutrition,
        "ingredients_parsed": ingredient_list
    }
