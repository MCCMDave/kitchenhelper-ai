from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import json
from app.schemas.favorite import (
    FavoriteCreate, FavoriteResponse, FavoriteListResponse,
    RecipeInfo, RecipeIngredientInfo, NutritionInfoEmbed
)
from app.models.favorite import Favorite
from app.models.recipe import Recipe
from app.models.user import User, SubscriptionTier
from app.utils.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])


def parse_recipe_for_response(recipe: Recipe) -> RecipeInfo:
    """Parse Recipe Model zu RecipeInfo Schema mit JSON-Feldern"""
    # Parse JSON fields
    ingredients = []
    if recipe.ingredients_json:
        try:
            raw_ingredients = json.loads(recipe.ingredients_json)
            ingredients = [
                RecipeIngredientInfo(
                    name=ing.get("name", ""),
                    amount=ing.get("amount", ""),
                    carbs=ing.get("carbs")
                )
                for ing in raw_ingredients
            ]
        except (json.JSONDecodeError, TypeError):
            ingredients = []

    nutrition = None
    if recipe.nutrition_json:
        try:
            raw_nutrition = json.loads(recipe.nutrition_json)
            nutrition = NutritionInfoEmbed(
                calories=raw_nutrition.get("calories"),
                protein=raw_nutrition.get("protein"),
                carbs=raw_nutrition.get("carbs"),
                fat=raw_nutrition.get("fat"),
                ke=raw_nutrition.get("ke"),
                be=raw_nutrition.get("be")
            )
        except (json.JSONDecodeError, TypeError):
            nutrition = None

    used_ingredients = []
    if recipe.used_ingredients:
        try:
            used_ingredients = json.loads(recipe.used_ingredients)
        except (json.JSONDecodeError, TypeError):
            used_ingredients = []

    return RecipeInfo(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        difficulty=recipe.difficulty or 2,
        cooking_time=recipe.cooking_time,
        method=recipe.method,
        servings=recipe.servings or 2,
        used_ingredients=used_ingredients,
        leftover_tips=recipe.leftover_tips,
        ingredients=ingredients,
        nutrition_per_serving=nutrition,
        ai_provider=recipe.ai_provider,
        generated_at=recipe.generated_at
    )


def check_favorite_limit(user: User, db: Session) -> bool:
    """
    Pruefe ob User noch Favoriten hinzufuegen darf

    Returns:
        True wenn unter dem Limit, False wenn Limit erreicht
    """
    current_count = db.query(Favorite).filter(Favorite.user_id == user.id).count()

    limits = {
        SubscriptionTier.DEMO: 5,
        SubscriptionTier.BASIC: 50,
        SubscriptionTier.PREMIUM: 999999  # "Unbegrenzt"
    }

    limit = limits.get(user.subscription_tier, 5)
    return current_count < limit


def get_favorite_limit(user: User) -> int:
    """Hole das Favoriten-Limit fuer den User"""
    limits = {
        SubscriptionTier.DEMO: 5,
        SubscriptionTier.BASIC: 50,
        SubscriptionTier.PREMIUM: 999999
    }
    return limits.get(user.subscription_tier, 5)


@router.get("/", response_model=FavoriteListResponse)
def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Alle Favoriten des Users abrufen

    Gibt eine Liste aller favorisierten Rezepte mit VOLLSTAENDIGEN Recipe-Details zurueck.
    Inkludiert: ingredients, nutrition, used_ingredients, leftover_tips, etc.
    """
    # JOIN mit Recipe fuer bessere Performance
    favorites = (
        db.query(Favorite)
        .options(joinedload(Favorite.recipe))
        .filter(Favorite.user_id == current_user.id)
        .order_by(Favorite.added_at.desc())
        .all()
    )

    # Manuell Response bauen mit vollstaendigen Recipe-Daten
    result = []
    for fav in favorites:
        recipe_info = None
        if fav.recipe:
            recipe_info = parse_recipe_for_response(fav.recipe)

        result.append(FavoriteResponse(
            id=fav.id,
            user_id=fav.user_id,
            recipe_id=fav.recipe_id,
            added_at=fav.added_at,
            recipe=recipe_info
        ))

    return FavoriteListResponse(
        favorites=result,
        count=len(result)
    )


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def create_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rezept als Favorit markieren

    **Validierungen:**
    - Recipe muss existieren und dem User gehoeren
    - Recipe darf nicht bereits favorisiert sein (409 Conflict)
    - User muss unter seinem Tier-Limit sein (403 Forbidden)

    **Tier-Limits:**
    - Demo: max 5 Favoriten
    - Basic: max 50 Favoriten
    - Premium: unbegrenzt
    """
    # 1. Pruefe ob Recipe existiert und dem User gehoert
    recipe = db.query(Recipe).filter(
        Recipe.id == favorite_data.recipe_id,
        Recipe.user_id == current_user.id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found or does not belong to you"
        )

    # 2. Pruefe ob bereits favorisiert
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.recipe_id == favorite_data.recipe_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recipe is already in favorites"
        )

    # 3. Pruefe Tier-Limit
    if not check_favorite_limit(current_user, db):
        limit = get_favorite_limit(current_user)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Favorite limit reached ({limit}). Upgrade your subscription for more favorites."
        )

    # 4. Favorit erstellen
    new_favorite = Favorite(
        user_id=current_user.id,
        recipe_id=favorite_data.recipe_id
    )

    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    # Recipe-Daten laden fuer Response
    db.refresh(new_favorite, ["recipe"])

    # Vollstaendige Recipe-Daten zurueckgeben
    recipe_info = None
    if new_favorite.recipe:
        recipe_info = parse_recipe_for_response(new_favorite.recipe)

    return FavoriteResponse(
        id=new_favorite.id,
        user_id=new_favorite.user_id,
        recipe_id=new_favorite.recipe_id,
        added_at=new_favorite.added_at,
        recipe=recipe_info
    )


@router.get("/check/{recipe_id}")
def check_favorite(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Pruefe ob ein Rezept bereits favorisiert ist

    Returns:
        is_favorite: bool - True wenn favorisiert
        favorite_id: int | None - ID des Favoriten falls vorhanden
    """
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.recipe_id == recipe_id
    ).first()

    return {
        "is_favorite": favorite is not None,
        "favorite_id": favorite.id if favorite else None
    }


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Favorit entfernen

    Loescht einen Favoriten. Nur der Besitzer kann seine Favoriten loeschen.
    """
    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == current_user.id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )

    db.delete(favorite)
    db.commit()

    return None
