#!/usr/bin/env python3
"""
Database Seed Script for KitchenHelper-AI
Populates database with demo data for development/testing

Usage:
    python scripts/seed.py
"""

import sys
import os
from datetime import datetime, timedelta
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.utils.database import SessionLocal, init_db
from app.models.user import User, SubscriptionTier
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.favorite import Favorite
from app.models.diet_profile import DietProfile
from app.utils.password import hash_password


def seed_users(db: Session):
    """Create demo users"""
    print("📊 Seeding users...")

    users_data = [
        {"username": "demo", "email": "demo@kitchenhelper.ai", "tier": SubscriptionTier.DEMO, "emoji": "👨‍🍳"},
        {"username": "alice", "email": "alice@test.com", "tier": SubscriptionTier.BASIC, "emoji": "👩"},
        {"username": "bob", "email": "bob@test.com", "tier": SubscriptionTier.PREMIUM, "emoji": "👨"},
    ]

    created = []
    for user_data in users_data:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            print(f"  ⏭️  User '{user_data['username']}' already exists")
            created.append(existing)
            continue

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hash_password("demo123"),
            subscription_tier=user_data["tier"],
            daily_limit=3 if user_data["tier"] == SubscriptionTier.DEMO else (50 if user_data["tier"] == SubscriptionTier.BASIC else 999999),
            emoji=user_data["emoji"]
        )
        db.add(user)
        db.flush()
        created.append(user)
        print(f"  ✅ Created user '{user.username}' ({user.subscription_tier.value})")

    db.commit()
    return created


def seed_ingredients(db: Session, users):
    """Create demo ingredients for each user"""
    print("\n🥗 Seeding ingredients...")

    ingredients_data = {
        "demo": [
            {"name": "Tomaten", "category": "Vegetables", "expiry": datetime.now() + timedelta(days=5)},
            {"name": "Nudeln", "category": "Pantry", "is_permanent": True},
            {"name": "Parmesan", "category": "Dairy", "expiry": datetime.now() + timedelta(days=14)},
            {"name": "Basilikum", "category": "Spices", "is_permanent": True},
            {"name": "Knoblauch", "category": "Vegetables", "is_permanent": True},
        ],
        "alice": [
            {"name": "Chicken Breast", "category": "Meat & Fish", "expiry": datetime.now() + timedelta(days=2)},
            {"name": "Rice", "category": "Pantry", "is_permanent": True},
            {"name": "Soy Sauce", "category": "Pantry", "is_permanent": True},
            {"name": "Broccoli", "category": "Vegetables", "expiry": datetime.now() + timedelta(days=4)},
            {"name": "Ginger", "category": "Spices", "is_permanent": True},
        ],
        "bob": [
            {"name": "Salmon", "category": "Meat & Fish", "expiry": datetime.now() + timedelta(days=1)},
            {"name": "Lemon", "category": "Fruits", "expiry": datetime.now() + timedelta(days=7)},
            {"name": "Dill", "category": "Spices", "is_permanent": True},
            {"name": "Butter", "category": "Dairy", "expiry": datetime.now() + timedelta(days=21)},
            {"name": "Potatoes", "category": "Vegetables", "expiry": datetime.now() + timedelta(days=30)},
        ]
    }

    created_count = 0
    for user in users:
        if user.username not in ingredients_data:
            continue

        for ing_data in ingredients_data[user.username]:
            ingredient = Ingredient(
                user_id=user.id,
                name=ing_data["name"],
                category=ing_data["category"],
                expiry_date=ing_data.get("expiry"),
                is_permanent=ing_data.get("is_permanent", False)
            )
            db.add(ingredient)
            created_count += 1

        print(f"  ✅ Created {len(ingredients_data[user.username])} ingredients for '{user.username}'")

    db.commit()
    print(f"  📦 Total: {created_count} ingredients created")


def seed_recipes(db: Session, users):
    """Create demo recipes"""
    print("\n🍽️  Seeding recipes...")

    recipes_data = {
        "demo": [
            {
                "name": "Spaghetti Carbonara",
                "description": "Classic Italian pasta dish with bacon and eggs",
                "difficulty": 2,
                "cooking_time": "25 Min",
                "method": "Stove",
                "servings": 2,
                "ingredients": [
                    {"name": "Spaghetti", "amount": "200g"},
                    {"name": "Bacon", "amount": "100g"},
                    {"name": "Eggs", "amount": "2"},
                    {"name": "Parmesan", "amount": "50g"},
                ],
                "nutrition": {"calories": 650, "protein": 28, "carbs": 72, "fat": 26}
            }
        ],
        "alice": [
            {
                "name": "Chicken Stir Fry",
                "description": "Quick Asian-style chicken with vegetables",
                "difficulty": 1,
                "cooking_time": "20 Min",
                "method": "Pan",
                "servings": 2,
                "ingredients": [
                    {"name": "Chicken Breast", "amount": "300g"},
                    {"name": "Broccoli", "amount": "200g"},
                    {"name": "Soy Sauce", "amount": "3 tbsp"},
                    {"name": "Rice", "amount": "150g"},
                ],
                "nutrition": {"calories": 480, "protein": 42, "carbs": 55, "fat": 8}
            }
        ]
    }

    created_count = 0
    for user in users:
        if user.username not in recipes_data:
            continue

        for recipe_data in recipes_data[user.username]:
            recipe = Recipe(
                user_id=user.id,
                name=recipe_data["name"],
                description=recipe_data["description"],
                difficulty=recipe_data["difficulty"],
                cooking_time=recipe_data["cooking_time"],
                method=recipe_data["method"],
                servings=recipe_data["servings"],
                used_ingredients=json.dumps([ing["name"] for ing in recipe_data["ingredients"]]),
                ingredients_json=json.dumps(recipe_data["ingredients"]),
                nutrition_json=json.dumps(recipe_data["nutrition"]),
                ai_provider="seed"
            )
            db.add(recipe)
            created_count += 1

        print(f"  ✅ Created {len(recipes_data[user.username])} recipes for '{user.username}'")

    db.commit()
    print(f"  📦 Total: {created_count} recipes created")


def main():
    """Main seeding function"""
    print("\n" + "="*50)
    print("  🌱 KitchenHelper-AI Database Seeder")
    print("="*50 + "\n")

    # Initialize database
    init_db()
    db = SessionLocal()

    try:
        # Seed data
        users = seed_users(db)
        seed_ingredients(db, users)
        seed_recipes(db, users)

        print("\n" + "="*50)
        print("  ✅ Database seeding completed!")
        print("="*50 + "\n")

        print("📝 Test Credentials:")
        print("  - Username: demo / Password: demo123")
        print("  - Username: alice / Password: demo123")
        print("  - Username: bob / Password: demo123")
        print()

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
