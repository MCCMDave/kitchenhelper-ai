# Admin & Developer Tools - KitchenHelper-AI

## 📋 KONTEXT

Entwicklung erleichtern mit Tools für Test-User Management, Demo-Daten und Debugging. Nur für Dev-Environment, nicht Production.

**Projekt-Pfade:**
- Stand-PC: `C:\Users\Startklar\Desktop\GitHub\kitchenhelper-ai`
- Laptop: `C:\Users\david\Desktop\GitHub\kitchenhelper-ai`

## 🎯 AUFGABEN

### Tool #1: Test User Manager
**Was:** Quick Create/Delete Test-Accounts

**Backend:**
- [ ] Route: POST /api/admin/test-users
  - Creates user: test1, test2, test3
  - Password: "test"
  - Auto-generates sample data
- [ ] Route: DELETE /api/admin/test-users
  - Deletes all test users
- [ ] Middleware: Only available if DEBUG=True

**Frontend:**
- [ ] Admin panel (hidden button)
- [ ] "Create 3 Test Users"
- [ ] "Delete All Test Users"

### Tool #2: Database Seed Script
**Was:** Populate DB mit Demo-Daten

**Implementation:**
- [ ] Script: `/mnt/project/seed.py`
  - Creates users
  - Creates ingredients
  - Creates recipes
  - Creates favorites
- [ ] Run: `python seed.py`

### Tool #3: API Request Logger
**Was:** Log alle API requests für Debugging

**Backend:**
- [ ] Middleware: Log requests to file
- [ ] Format: Timestamp, Method, Path, Status, Duration
- [ ] File: `logs/api-requests.log`

### Tool #4: Health Dashboard
**Was:** System metrics overview

**Backend:**
- [ ] Route: GET /api/admin/health
  - DB connection status
  - User count
  - Recipe count
  - Disk space
  - Uptime

**Frontend:**
- [ ] Admin dashboard page
- [ ] Live metrics display

## 🧪 TESTING
```bash
# Create test users
POST /api/admin/test-users
# → Creates test1, test2, test3

# Seed DB
python seed.py
# → Populates with demo data

# Check health
GET /api/admin/health
# → {"status": "healthy", "users": 5, ...}
```

## 📦 DATEIEN

**Erstellen:**
- `/mnt/project/admin-_routes.py`
- `/mnt/project/seed.py`
- `/mnt/project/middleware/logger.py`

---

**START:** Tool #1 (Test Users), dann #2 (Seed), dann #3 (Logger), dann #4 (Health).
