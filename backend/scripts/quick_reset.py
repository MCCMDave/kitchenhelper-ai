"""
Quick Database Reset Script
Run this AFTER stopping the backend server!

Usage:
  1. Stop uvicorn server (Ctrl+C in terminal)
  2. Run: python scripts/quick_reset.py
  3. Start server again: uvicorn app.main:app --reload
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'kitchenhelper.db')

def main():
    print("="*60)
    print("QUICK DATABASE RESET")
    print("="*60)

    # Step 1: Delete old database
    print(f"\n1. Deleting database: {DB_PATH}")
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("   OK - Database deleted")
        except PermissionError:
            print("   ERROR: Database is locked!")
            print("   Please stop the backend server first.")
            print("   Press Ctrl+C in the uvicorn terminal.")
            return
    else:
        print("   OK - No existing database found")

    # Step 2: Import and create new database
    print("\n2. Creating new database with updated schema...")

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from passlib.context import CryptContext

    from app.utils.database import Base
    from app.models.user import User
    from app.models import ingredient, recipe, favorite, diet_profile

    DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    print("   OK - Tables created")

    # Step 3: Create test users
    print("\n3. Creating test users...")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    test_users = [
        {"email": "a@a.a", "username": "aaa", "password": "aaa"},
        {"email": "b@b.b", "username": "bbb", "password": "bbb"},
        {"email": "test@test.de", "username": "testuser", "password": "testuser"},
    ]

    for user_data in test_users:
        hashed_password = pwd_context.hash(user_data["password"])
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=hashed_password,
            emoji="👤",
            subscription_tier="demo"
        )
        db.add(user)
        print(f"   Created: {user_data['email']} / {user_data['username']} / {user_data['password']}")

    db.commit()
    db.close()

    print("\n" + "="*60)
    print("DONE! Database reset complete.")
    print("="*60)
    print("\nTest accounts:")
    print("  - a@a.a / aaa / aaa")
    print("  - b@b.b / bbb / bbb")
    print("  - test@test.de / testuser / testuser")
    print("\nYou can now start the server:")
    print("  uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
