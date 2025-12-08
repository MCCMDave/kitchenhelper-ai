"""
Recipe Database API Routes - BASIC Tier+
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.recipe_db import RecipeDB
from app.models.user import User
from app.routes.auth import get_current_user

router = APIRouter(prefix="/recipe-db", tags=["Recipe Database"])


@router.get("/search")
async def search_recipes(
    query: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Category filter (low_carb, low_gi, etc.)"),
    max_carbs: Optional[int] = Query(None, description="Max carbs per serving"),
    max_gi: Optional[int] = Query(None, description="Max glycemic index"),
    quick_only: bool = Query(False, description="Only recipes <30min"),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search recipes in database (BASIC Tier+)

    **Requires:** BASIC, PREMIUM, PRO, or BUSINESS tier
    """
    # Feature-Check: recipe_db
    if not current_user.has_feature("recipe_db"):
        raise HTTPException(
            status_code=403,
            detail="Recipe database requires BASIC tier or higher. Upgrade at /settings"
        )

    # Base query
    recipes_query = db.query(RecipeDB)

    # Text search
    if query:
        recipes_query = recipes_query.filter(
            (RecipeDB.name.ilike(f"%{query}%")) |
            (RecipeDB.description.ilike(f"%{query}%"))
        )

    # Category filter
    if category:
        category_map = {
            "low_carb": RecipeDB.is_low_carb,
            "low_gi": RecipeDB.is_low_gi,
            "diabetic_friendly": RecipeDB.is_diabetic_friendly,
            "vegetarian": RecipeDB.is_vegetarian,
            "vegan": RecipeDB.is_vegan,
            "gluten_free": RecipeDB.is_gluten_free,
            "quick": RecipeDB.is_quick,
        }
        if category in category_map:
            recipes_query = recipes_query.filter(category_map[category] == True)

    # Nutritional filters
    if max_carbs is not None:
        recipes_query = recipes_query.filter(RecipeDB.carbs <= max_carbs)

    if max_gi is not None:
        recipes_query = recipes_query.filter(RecipeDB.gi <= max_gi)

    if quick_only:
        recipes_query = recipes_query.filter(RecipeDB.is_quick == True)

    # Sort by quality score (curated recipes first)
    recipes_query = recipes_query.order_by(RecipeDB.quality_score.desc())

    # Pagination
    total = recipes_query.count()
    recipes = recipes_query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "recipes": [recipe.to_dict() for recipe in recipes],
        "source": "recipe_db",
        "tier_required": "BASIC"
    }


@router.get("/{recipe_id}")
async def get_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get single recipe by ID (BASIC Tier+)
    """
    if not current_user.has_feature("recipe_db"):
        raise HTTPException(
            status_code=403,
            detail="Recipe database requires BASIC tier or higher"
        )

    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Increment usage count
    recipe.usage_count += 1
    db.commit()

    return recipe.to_dict()


@router.get("/categories/list")
async def list_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get available categories with counts
    """
    if not current_user.has_feature("recipe_db"):
        raise HTTPException(
            status_code=403,
            detail="Recipe database requires BASIC tier or higher"
        )

    categories = {
        "low_carb": db.query(RecipeDB).filter(RecipeDB.is_low_carb == True).count(),
        "low_gi": db.query(RecipeDB).filter(RecipeDB.is_low_gi == True).count(),
        "diabetic_friendly": db.query(RecipeDB).filter(RecipeDB.is_diabetic_friendly == True).count(),
        "vegetarian": db.query(RecipeDB).filter(RecipeDB.is_vegetarian == True).count(),
        "vegan": db.query(RecipeDB).filter(RecipeDB.is_vegan == True).count(),
        "gluten_free": db.query(RecipeDB).filter(RecipeDB.is_gluten_free == True).count(),
        "quick": db.query(RecipeDB).filter(RecipeDB.is_quick == True).count(),
    }

    total = db.query(RecipeDB).count()

    return {
        "total_recipes": total,
        "categories": categories
    }


@router.get("/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get database statistics (FREE tier - info only)
    """
    total = db.query(RecipeDB).count()

    return {
        "total_recipes": total,
        "user_tier": current_user.subscription_tier.value,
        "has_access": current_user.has_feature("recipe_db"),
        "upgrade_url": "/settings" if not current_user.has_feature("recipe_db") else None
    }
