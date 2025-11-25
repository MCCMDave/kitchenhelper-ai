# Admin & Developer Tools Routes
# WARNING: Only enable in development! Set DEBUG=True in environment

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
import os

from app.models.user import User, SubscriptionTier
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.favorite import Favorite
from app.utils.database import get_db
from app.utils.password import hash_password

router = APIRouter(prefix="/admin", tags=["Admin"])

# Security check: Only allow in DEBUG mode
def require_debug_mode():
    """Middleware to check if DEBUG mode is enabled"""
    debug = os.getenv("DEBUG", "False").lower() == "true"
    if not debug:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin endpoints are only available in DEBUG mode"
        )

@router.post("/test-users", dependencies=[Depends(require_debug_mode)])
def create_test_users(db: Session = Depends(get_db)):
    """
    Create 3 test users with sample data

    WARNING: Only available when DEBUG=True

    Creates:
    - test1 / test (Demo tier)
    - test2 / test (Basic tier)
    - test3 / test (Premium tier)
    """
    created_users = []

    for i in range(1, 4):
        username = f"test{i}"
        email = f"test{i}@test.com"

        # Check if user already exists
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing:
            continue

        # Determine tier
        tier = SubscriptionTier.DEMO if i == 1 else (
            SubscriptionTier.BASIC if i == 2 else SubscriptionTier.PREMIUM
        )

        # Create user
        new_user = User(
            email=email,
            username=username,
            hashed_password=hash_password("test"),
            subscription_tier=tier,
            daily_limit=3 if tier == SubscriptionTier.DEMO else (
                50 if tier == SubscriptionTier.BASIC else 999999
            ),
            emoji="🧪"
        )

        db.add(new_user)
        db.flush()

        # Add sample ingredients
        sample_ingredients = [
            {"name": "Tomaten", "category": "Vegetables"},
            {"name": "Nudeln", "category": "Pantry"},
            {"name": "Käse", "category": "Dairy"},
            {"name": "Hähnchen", "category": "Meat & Fish"},
            {"name": "Salz", "category": "Spices", "is_permanent": True},
        ]

        for ing_data in sample_ingredients:
            ingredient = Ingredient(
                user_id=new_user.id,
                name=ing_data["name"],
                category=ing_data["category"],
                is_permanent=ing_data.get("is_permanent", False)
            )
            db.add(ingredient)

        created_users.append({
            "username": username,
            "email": email,
            "password": "test",
            "tier": tier.value,
            "id": new_user.id
        })

    db.commit()

    return {
        "message": f"{len(created_users)} test users created",
        "users": created_users
    }


@router.delete("/test-users", dependencies=[Depends(require_debug_mode)])
def delete_test_users(db: Session = Depends(get_db)):
    """
    Delete all test users (test1, test2, test3)

    WARNING: Only available when DEBUG=True
    """
    deleted_count = 0

    for i in range(1, 4):
        username = f"test{i}"
        user = db.query(User).filter(User.username == username).first()

        if user:
            # CASCADE will delete related ingredients, recipes, favorites
            db.delete(user)
            deleted_count += 1

    db.commit()

    return {
        "message": f"{deleted_count} test users deleted",
        "deleted_usernames": [f"test{i}" for i in range(1, 4)]
    }


@router.get("/health", dependencies=[Depends(require_debug_mode)])
def get_health_metrics(db: Session = Depends(get_db)):
    """
    Get system health metrics

    WARNING: Only available when DEBUG=True

    Returns:
    - Database connection status
    - User count
    - Recipe count
    - Favorite count
    - Ingredient count
    """
    try:
        # Test DB connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Get counts
    user_count = db.query(User).count()
    recipe_count = db.query(Recipe).count()
    favorite_count = db.query(Favorite).count()
    ingredient_count = db.query(Ingredient).count()

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "metrics": {
            "users": user_count,
            "recipes": recipe_count,
            "favorites": favorite_count,
            "ingredients": ingredient_count
        },
        "environment": {
            "debug_mode": os.getenv("DEBUG", "False"),
            "database_url": os.getenv("DATABASE_URL", "sqlite:///./database/kitchenhelper.db")
        }
    }
