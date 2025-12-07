#!/usr/bin/env python3
"""
Migration: Tier-System Update
- Fügt is_admin Spalte hinzu
- Aktualisiert subscription_tier Enum (FREE, BASIC, PREMIUM, PRO, BUSINESS_*)
"""
import sqlite3
import sys

DB_PATH = "database/kitchenhelper.db"

def migrate():
    """Führt Migration aus"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🔧 Starting migration: Tier System Update")

        # 1. is_admin Spalte hinzufügen
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            print("✅ Added column: is_admin")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("⚠️  Column is_admin already exists")
            else:
                raise

        # 2. Subscription Tier aktualisieren (DEMO → FREE für bestehende User)
        cursor.execute("""
            UPDATE users
            SET subscription_tier = 'free'
            WHERE subscription_tier = 'demo' OR subscription_tier IS NULL
        """)
        updated = cursor.rowcount
        print(f"✅ Updated {updated} users: DEMO → FREE")

        # 3. Ersten User als Admin setzen (falls vorhanden)
        cursor.execute("SELECT id, email FROM users ORDER BY id LIMIT 1")
        first_user = cursor.fetchone()
        if first_user:
            cursor.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (first_user[0],))
            print(f"✅ Set admin flag for: {first_user[1]} (ID: {first_user[0]})")

        conn.commit()
        conn.close()

        print("✅ Migration completed successfully!")
        return 0

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(migrate())
