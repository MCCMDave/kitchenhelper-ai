from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.recipe import RecipeListResponse
from app.models.user import User
from app.utils.database import get_db
from app.utils.auth import get_current_user
from app.data.faq_recipes import get_all_faq_categories, get_faq_category
from app.services.ai_recipe_generator import ai_generator
from app.routes.recipes import check_daily_limit, increment_recipe_count
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeResponse, RecipeIngredient, NutritionInfo
import json
from datetime import datetime

router = APIRouter(prefix="/faq", tags=["FAQ"])


@router.get("/categories")
def get_faq_categories(
    language: str = Query("en", regex="^(en|de)$"),
    current_user: User = Depends(get_current_user)
):
    """
    Get all FAQ recipe categories

    Returns list of predefined recipe categories for quick access
    """
    categories = get_all_faq_categories(language)
    return {
        "categories": categories,
        "count": len(categories)
    }


@router.post("/generate/{category_id}", response_model=RecipeListResponse)
def generate_faq_recipe(
    category_id: str,
    language: str = Query("en", regex="^(en|de)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate recipe from FAQ category

    - **category_id**: FAQ category ID (e.g., "quick-dinner-veg")
    - **language**: "en" or "de"

    This uses predefined ingredients and settings from the FAQ category.
    Counts against daily limit like regular recipe generation.
    """
    # 1. Check daily limit
    if not check_daily_limit(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "daily_limit_reached",
                "message": f"Tageslimit erreicht ({current_user.daily_limit} Rezepte). Upgrade für mehr!",
                "daily_limit": current_user.daily_limit,
                "subscription_tier": current_user.subscription_tier.value
            }
        )

    # 2. Load FAQ category
    category = get_faq_category(category_id, language)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FAQ category '{category_id}' not found"
        )

    # 3. Generate recipes using AI
    try:
        generated_recipes = ai_generator.generate_recipes(
            ingredients=category["ingredients"],
            count=3,
            servings=category["servings"],
            diet_profiles=category["diet_profiles"],
            diabetes_unit="KE",  # Default
            language=language,
            user_tier=current_user.subscription_tier.value
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "ai_generation_failed",
                "message": f"AI-Generierung fehlgeschlagen: {str(e)}",
                "fallback": "Bitte versuche es später erneut"
            }
        )

    # 4. Save recipes to database
    saved_recipes = []
    for recipe_data in generated_recipes:
        new_recipe = Recipe(
            user_id=current_user.id,
            name=recipe_data["name"],
            description=recipe_data["description"],
            difficulty=recipe_data["difficulty"],
            cooking_time=recipe_data["cooking_time"],
            method=recipe_data["method"],
            servings=recipe_data["servings"],
            used_ingredients=json.dumps(recipe_data["used_ingredients"]),
            leftover_tips=recipe_data["leftover_tips"],
            ingredients_json=json.dumps(recipe_data["ingredients"]),
            nutrition_json=json.dumps(recipe_data["nutrition_per_serving"]),
            ai_provider=recipe_data["ai_provider"]
        )

        db.add(new_recipe)
        db.flush()

        # Response format
        recipe_response = RecipeResponse(
            id=new_recipe.id,
            user_id=new_recipe.user_id,
            name=new_recipe.name,
            description=new_recipe.description,
            difficulty=new_recipe.difficulty,
            cooking_time=new_recipe.cooking_time,
            method=new_recipe.method,
            servings=new_recipe.servings,
            used_ingredients=recipe_data["used_ingredients"],
            leftover_tips=recipe_data["leftover_tips"],
            ingredients=[RecipeIngredient(**ing) for ing in recipe_data["ingredients"]],
            nutrition_per_serving=NutritionInfo(**recipe_data["nutrition_per_serving"]),
            ai_provider=new_recipe.ai_provider,
            generated_at=new_recipe.generated_at
        )

        saved_recipes.append(recipe_response)

    db.commit()

    # 5. Increment counter
    increment_recipe_count(current_user, db)

    # 6. Response
    remaining = current_user.daily_limit - current_user.daily_recipe_count

    return RecipeListResponse(
        recipes=saved_recipes,
        count=len(saved_recipes),
        daily_count_remaining=remaining,
        message=f"✅ {len(saved_recipes)} Rezepte aus FAQ '{category['title']}' generiert! Noch {remaining} heute verfügbar."
    )
