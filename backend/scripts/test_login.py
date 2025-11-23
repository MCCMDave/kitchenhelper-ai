"""
Test Login für KitchenHelper User
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests

API_URL = "http://127.0.0.1:8000/api"

def test_login(email_or_username, password):
    """Teste Login"""
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email_or_username": email_or_username,
                "password": password
            },
            timeout=5
        )

        if response.status_code == 200:
            print(f"[OK] Login erfolgreich: {email_or_username}")
            data = response.json()
            print(f"     Token: {data['access_token'][:30]}...")
            return True
        else:
            print(f"[FAIL] Login fehlgeschlagen: {email_or_username}")
            print(f"       Status: {response.status_code}")
            try:
                print(f"       Error: {response.json()}")
            except:
                print(f"       Response: {response.text[:100]}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Backend nicht erreichbar! Bitte starten mit:")
        print(f"        cd backend && uvicorn app.main:app --reload")
        return None
    except Exception as e:
        print(f"[ERROR] Fehler beim Login-Test: {e}")
        return False

def check_backend():
    """Prüfe ob Backend läuft"""
    try:
        response = requests.get(f"http://127.0.0.1:8000/", timeout=2)
        return True
    except:
        return False

def main():
    print("\n" + "="*60)
    print("KITCHENHELPER LOGIN TESTS")
    print("="*60)

    # Check backend
    if not check_backend():
        print("\n[WARNING] Backend nicht erreichbar!")
        print("Bitte starten mit:")
        print("  cd backend")
        print("  .\\venv\\Scripts\\activate")
        print("  uvicorn app.main:app --reload")
        print("\nDann dieses Script erneut ausführen.")
        return

    print("\n[OK] Backend erreichbar\n")

    test_users = [
        ("a@a.a", "aaaaaa", "Email"),
        ("aaa", "aaaaaa", "Username"),
        ("b@b.b", "bbbbbb", "Email"),
        ("bbb", "bbbbbb", "Username"),
        ("test@test.de", "test123", "Email"),
        ("testuser", "test123", "Username"),
    ]

    print("Testing User Logins...")
    print("-"*60)

    results = {"success": 0, "failed": 0, "error": 0}

    for login_id, password, login_type in test_users:
        print(f"\nTest: {login_id} ({login_type})")
        result = test_login(login_id, password)

        if result is True:
            results["success"] += 1
        elif result is False:
            results["failed"] += 1
        else:
            results["error"] += 1
            break  # Backend nicht erreichbar

    print("\n" + "="*60)
    print("ERGEBNIS")
    print("="*60)
    print(f"Erfolgreich: {results['success']}")
    print(f"Fehlgeschlagen: {results['failed']}")
    print(f"Fehler: {results['error']}")

    if results['failed'] == 0 and results['error'] == 0:
        print("\n[SUCCESS] Alle Login-Tests bestanden!")
    else:
        print("\n[WARNING] Einige Tests fehlgeschlagen!")

    print("="*60)

if __name__ == "__main__":
    main()
