"""
KitchenHelper-AI Database Manager
Utility script for database management tasks
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Import models
from app.models.user import User
from app.utils.database import Base

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'kitchenhelper.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    """Create database connection"""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal()

def show_users():
    """Display all users in database"""
    engine, db = get_db()

    print("\n" + "="*60)
    print("USERS IN DATABASE")
    print("="*60)

    users = db.query(User).all()

    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"\nID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Username: {getattr(user, 'username', 'N/A')}")
            print(f"  Emoji: {getattr(user, 'emoji', 'N/A')}")
            print(f"  Tier: {user.subscription_tier}")
            print(f"  Created: {user.created_at}")

    print("\n" + "="*60)
    print(f"Total: {len(users)} users")
    print("="*60)

    db.close()

def check_schema():
    """Check current database schema"""
    engine, db = get_db()
    inspector = inspect(engine)

    print("\n" + "="*60)
    print("DATABASE SCHEMA")
    print("="*60)

    tables = inspector.get_table_names()
    print(f"\nTables: {tables}")

    if 'users' in tables:
        columns = inspector.get_columns('users')
        print("\nUsers table columns:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")

    print("="*60)
    db.close()

def clear_all_data():
    """Clear all data from database (keep schema)"""
    engine, db = get_db()

    print("\nClearing all data...")

    try:
        db.query(User).delete()
        db.commit()
        print("All users deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    db.close()

def reset_database():
    """Delete and recreate database with new schema"""
    print("\nResetting database...")

    # Delete old database file
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"Deleted: {DB_PATH}")
        except PermissionError:
            print(f"ERROR: Database is locked by another process.")
            print(f"       Please stop the backend server first (uvicorn).")
            print(f"       Then run this script again.")
            return False

    # Create new database with current schema
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    print("Created new database with current schema.")

    # Show new schema
    check_schema()

def create_test_users():
    """Create test users"""
    engine, db = get_db()

    test_users = [
        {"email": "a@a.a", "username": "aaa", "password": "aaa"},
        {"email": "b@b.b", "username": "bbb", "password": "bbb"},
        {"email": "test@test.de", "username": "testuser", "password": "testuser"},
    ]

    print("\nCreating test users...")

    for user_data in test_users:
        try:
            # Check if user exists
            existing = db.query(User).filter(
                (User.email == user_data["email"]) |
                (User.username == user_data["username"])
            ).first()

            if existing:
                print(f"  Skipped (exists): {user_data['email']}")
                continue

            # Create user
            hashed_password = pwd_context.hash(user_data["password"])
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=hashed_password,
                emoji="👤",
                subscription_tier="demo"
            )
            db.add(user)
            db.commit()
            print(f"  Created: {user_data['email']} / {user_data['username']} / {user_data['password']}")
        except Exception as e:
            db.rollback()
            print(f"  Error creating {user_data['email']}: {e}")

    db.close()

def full_reset_with_test_users():
    """Complete reset: delete DB, recreate, add test users"""
    print("\n" + "="*60)
    print("FULL DATABASE RESET")
    print("="*60)

    reset_database()
    create_test_users()
    show_users()

    print("\nDone! Test users created:")
    print("  - a@a.a / aaa / aaa")
    print("  - b@b.b / bbb / bbb")
    print("  - test@test.de / testuser / testuser")

def main():
    """Interactive menu"""
    while True:
        print("\n" + "="*60)
        print("KITCHENHELPER DATABASE MANAGER")
        print("="*60)
        print("\n1. Show all users")
        print("2. Check schema")
        print("3. Clear all data")
        print("4. Reset database (delete + recreate)")
        print("5. Create test users")
        print("6. FULL RESET + Test Users")
        print("0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            show_users()
        elif choice == "2":
            check_schema()
        elif choice == "3":
            confirm = input("Delete all data? (yes/no): ")
            if confirm.lower() == "yes":
                clear_all_data()
        elif choice == "4":
            confirm = input("Delete and recreate database? (yes/no): ")
            if confirm.lower() == "yes":
                reset_database()
        elif choice == "5":
            create_test_users()
        elif choice == "6":
            confirm = input("FULL RESET - Delete DB, recreate, add test users? (yes/no): ")
            if confirm.lower() == "yes":
                full_reset_with_test_users()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    # If run with argument, execute directly
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "reset":
            full_reset_with_test_users()
        elif cmd == "users":
            show_users()
        elif cmd == "schema":
            check_schema()
        else:
            print(f"Unknown command: {cmd}")
            print("Available: reset, users, schema")
    else:
        main()
