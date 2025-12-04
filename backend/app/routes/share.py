# Recipe Sharing Routes
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import json
import secrets
import hashlib

from app.schemas.shopping_list import ShareLinkResponse
from app.models.recipe import Recipe
from app.models.favorite import Favorite
from app.models.user import User
from app.utils.database import get_db
from app.utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/share", tags=["Sharing"])

# TODO (Security): Migrate to persistent storage for production
# Current implementation: In-memory store (share links lost on restart)
# Production options:
#   1. Redis (recommended for TTL and performance)
#   2. Database table with expires_at column + background cleanup job
#   3. SQLite with periodic cleanup (simpler but less scalable)
# Security: Share links already have TTL (max 30 days) and cleanup on access
share_store = {}


class SharedRecipeResponse(BaseModel):
    """Public recipe data (no user info)"""
    name: str
    description: Optional[str]
    difficulty: int
    cooking_time: Optional[str]
    method: Optional[str]
    servings: int
    ingredients: list
    nutrition_per_serving: dict
    shared_by: str  # Just username, no email
    shared_at: datetime


class ShareRequest(BaseModel):
    """Request to create share link"""
    recipe_id: Optional[int] = None
    favorite_id: Optional[int] = None
    expires_hours: int = 168  # 7 days default


def generate_share_id() -> str:
    """Generate unique share ID"""
    return secrets.token_urlsafe(12)


def cleanup_expired_shares():
    """Remove expired share links"""
    now = datetime.utcnow()
    expired = [sid for sid, data in share_store.items() if data['expires_at'] < now]
    for sid in expired:
        del share_store[sid]


@router.post("/create", response_model=ShareLinkResponse)
def create_share_link(
    request: ShareRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a shareable link for a recipe or favorite.

    - **recipe_id**: ID of recipe to share
    - **favorite_id**: ID of favorite to share
    - **expires_hours**: Link expiry (default 168 = 7 days, max 720 = 30 days)

    Returns share URL that anyone can access without login.
    """
    cleanup_expired_shares()

    if not request.recipe_id and not request.favorite_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide either recipe_id or favorite_id"
        )

    # Limit expiry to 30 days
    expires_hours = min(request.expires_hours, 720)

    recipe_data = None
    recipe_name = ""

    # Load recipe
    if request.recipe_id:
        recipe = db.query(Recipe).filter(
            Recipe.id == request.recipe_id,
            Recipe.user_id == current_user.id
        ).first()

        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )

        recipe_name = recipe.name
        recipe_data = {
            "name": recipe.name,
            "description": recipe.description,
            "difficulty": recipe.difficulty,
            "cooking_time": recipe.cooking_time,
            "method": recipe.method,
            "servings": recipe.servings,
            "ingredients": json.loads(recipe.ingredients_json) if recipe.ingredients_json else [],
            "nutrition_per_serving": json.loads(recipe.nutrition_json) if recipe.nutrition_json else {},
        }

    # Load favorite (favorites reference recipes via recipe_id)
    elif request.favorite_id:
        favorite = db.query(Favorite).filter(
            Favorite.id == request.favorite_id,
            Favorite.user_id == current_user.id
        ).first()

        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )

        # Access recipe data through the relationship
        if not favorite.recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Associated recipe not found"
            )

        recipe_name = favorite.recipe.name
        recipe_data = {
            "name": favorite.recipe.name,
            "description": favorite.recipe.description,
            "difficulty": favorite.recipe.difficulty,
            "cooking_time": favorite.recipe.cooking_time,
            "method": favorite.recipe.method,
            "servings": favorite.recipe.servings,
            "ingredients": json.loads(favorite.recipe.ingredients_json) if favorite.recipe.ingredients_json else [],
            "nutrition_per_serving": json.loads(favorite.recipe.nutrition_json) if favorite.recipe.nutrition_json else {},
        }

    # Generate share ID
    share_id = generate_share_id()
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)

    # Store share data
    share_store[share_id] = {
        "data": recipe_data,
        "expires_at": expires_at,
        "creator_id": current_user.id,
        "creator_name": current_user.username or "Anonymous",
        "created_at": datetime.utcnow()
    }

    # Build share URL (frontend will handle this)
    share_url = f"/shared/{share_id}"

    return ShareLinkResponse(
        share_id=share_id,
        share_url=share_url,
        expires_at=expires_at,
        recipe_name=recipe_name
    )


@router.get("/{share_id}", response_model=SharedRecipeResponse)
def get_shared_recipe(share_id: str):
    """
    Get a shared recipe by its share ID.

    **No authentication required** - anyone with the link can view.
    """
    cleanup_expired_shares()

    if share_id not in share_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found or expired"
        )

    share_data = share_store[share_id]

    if share_data['expires_at'] < datetime.utcnow():
        del share_store[share_id]
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Share link has expired"
        )

    recipe = share_data['data']

    return SharedRecipeResponse(
        name=recipe['name'],
        description=recipe.get('description'),
        difficulty=recipe['difficulty'],
        cooking_time=recipe.get('cooking_time'),
        method=recipe.get('method'),
        servings=recipe['servings'],
        ingredients=recipe['ingredients'],
        nutrition_per_serving=recipe['nutrition_per_serving'],
        shared_by=share_data['creator_name'],
        shared_at=share_data['created_at']
    )


@router.delete("/{share_id}")
def revoke_share_link(
    share_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Revoke a share link (only the creator can do this).
    """
    if share_id not in share_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found"
        )

    if share_store[share_id]['creator_id'] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only revoke your own share links"
        )

    del share_store[share_id]

    return {"message": "Share link revoked successfully"}


@router.get("/my/links")
def get_my_share_links(
    current_user: User = Depends(get_current_user)
):
    """
    Get all active share links created by the current user.
    """
    cleanup_expired_shares()

    my_links = []
    for share_id, data in share_store.items():
        if data['creator_id'] == current_user.id:
            my_links.append({
                "share_id": share_id,
                "recipe_name": data['data']['name'],
                "created_at": data['created_at'],
                "expires_at": data['expires_at'],
                "share_url": f"/shared/{share_id}"
            })

    return {"links": my_links, "count": len(my_links)}
