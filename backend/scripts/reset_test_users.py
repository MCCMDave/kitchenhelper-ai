#!/usr/bin/env python3
"""
Reset Database and Create Test Users

Deletes all existing users and creates 3 test users:
- a@a.a / aaa / aaa123
- b@b.b / bbb / bbb123
- c@c.c / ccc / ccc123
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User, Base
from app.utils.password import hash_password

# Import all models to ensure relationships are loaded
try:
    from app.models.ingredient import Ingredient
    from app.models.profile import Profile
    from app.models.meal_log import MealLog
except ImportError:
    pass  # Models may not exist yet

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'kitchenhelper.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def reset_users():
    """Delete all users and create test users"""
    # Use raw connection to avoid ORM relationship issues
    conn = engine.raw_connection()
    cursor = conn.cursor()

    try:
        # Delete all existing users
        cursor.execute("DELETE FROM users")
        deleted_count = cursor.rowcount
        print(f"OK: Deleted {deleted_count} existing users")

        # Create 3 test users
        test_users = [
            {
                "email": "a@a.a",
                "username": "aaa",
                "password": "aaa123",
                "emoji": "👤"
            },
            {
                "email": "b@b.b",
                "username": "bbb",
                "password": "bbb123",
                "emoji": "👤"
            },
            {
                "email": "c@c.c",
                "username": "ccc",
                "password": "ccc123",
                "emoji": "👤"
            }
        ]

        for user_data in test_users:
            hashed_pw = hash_password(user_data["password"])
            cursor.execute(
                "INSERT INTO users (email, username, hashed_password, emoji, subscription_tier, daily_recipe_count) VALUES (?, ?, ?, ?, ?, ?)",
                (user_data["email"], user_data["username"], hashed_pw, user_data["emoji"], "demo", 0)
            )
            print(f"OK: Created test user: {user_data['username']} ({user_data['email']}) | PW: {user_data['password']}")

        conn.commit()
        print("\nDatabase reset complete!")
        print("\nTest Users:")
        print("  1. a@a.a / aaa / aaa123")
        print("  2. b@b.b / bbb / bbb123")
        print("  3. c@c.c / ccc / ccc123")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("KitchenHelper-AI Database Reset")
    print("=" * 60)
    print("\nWARNING: This will DELETE all existing users!")

    confirm = input("\nContinue? (yes/no): ").lower().strip()

    if confirm == "yes":
        reset_users()
    else:
        print("Cancelled")
