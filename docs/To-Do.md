# KitchenHelper-AI - To-Do Liste

**Projekt-Status:** Feature-Complete MVP
**Aktueller Stand:** Testing & Deployment-Ready
**Nächster Meilenstein:** Echte KI-Integration & Docker Deployment

---

## ✅ Completed

### Backend (erledigt)
- [x] FastAPI-Projekt mit Ordnerstruktur
- [x] Virtual Environment + requirements.txt
- [x] SQLAlchemy Models (User, Ingredient, Recipe, Favorite, DietProfile)
- [x] JWT Authentication
- [x] Auth Endpoints (register, login, token-refresh)
- [x] User Endpoints (me, update, delete)
- [x] Ingredients CRUD
- [x] Recipes Generate (Mock AI)
- [x] Favorites CRUD
- [x] Diet Profiles CRUD
- [x] PDF Export für Rezepte (reportlab)
- [x] Language Parameter für Rezeptgenerierung

### Frontend (erledigt)
- [x] HTML/CSS/JS modular aufgebaut
- [x] API-Client Modul (api.js)
- [x] Login/Register mit Validierung
- [x] Passwort-Reset Flow (UI)
- [x] Dashboard mit Tab-Navigation
- [x] Ingredients Management mit Autocomplete
- [x] Recipe Generation UI
- [x] Favorites als Modal mit PDF Export
- [x] Diet Profiles als Checkbox-Grid
- [x] Settings (Avatar, Password, Account Info)
- [x] Multi-Language Support (EN/DE)
- [x] Dark Mode Toggle
- [x] Responsive Design

### Dokumentation (erledigt)
- [x] CLAUDE.md Projekt-Kontext
- [x] README.md für Tester
- [x] API-Documentation.md
- [x] CODING-GUIDELINES.md

---

## 🔥 Priorität 1 - Nächste Schritte

### AI Integration
- [ ] Claude API Service implementieren
- [ ] OpenAI API Service implementieren
- [ ] Gemini API Service implementieren
- [ ] AI Provider Selection im Frontend
- [ ] Real Nutrition Calculation

### Testing
- [ ] pytest Setup
- [ ] Unit Tests für Auth
- [ ] Unit Tests für API Endpoints
- [ ] Frontend E2E Tests (optional)

---

## 📅 Priorität 2 - Nach AI Integration

### Deployment
- [ ] Dockerfile erstellen
- [ ] docker-compose.yml für Backend + DB
- [ ] Nginx Reverse Proxy Config
- [ ] SSL/HTTPS Setup
- [ ] Deployment auf Raspberry Pi

### Payment Integration
- [ ] Stripe Account Setup
- [ ] Checkout Session Endpoint
- [ ] Webhook für Payment Success
- [ ] Subscription Management
- [ ] Tier-basierte Feature Limits

---

## 📋 Backlog (Nice-to-Have)

### Features
- [ ] Einkaufslisten-Generator
- [ ] Meal Planning (Wochenplanung)
- [ ] Rezepte teilen (Social)
- [ ] Barcode-Scanner Integration
- [x] Multi-Language Support ✅
- [x] Dark Mode ✅
- [ ] PWA Offline-Modus
- [x] Export zu PDF ✅

### Optimierungen
- [ ] Caching Layer (Redis)
- [ ] Rate Limiting verbessern
- [ ] Logging & Monitoring
- [ ] Error Tracking (Sentry)
- [ ] Analytics Dashboard

### Security
- [ ] Email Verification (echte Emails)
- [ ] Password Reset via Email
- [ ] Two-Factor Authentication
- [ ] Security Headers
- [ ] Input Sanitization Review

---

## 📝 Notizen

### Bekannte Issues
- Password Reset aktuell nur mit Console-Code (kein echter Email-Versand)
- Mock AI generiert statische Rezepte
- Subscription Tiers noch nicht enforced

### Entscheidungen
- SQLite für Development, PostgreSQL für Production
- Vanilla JS statt Framework (Lernprojekt)
- reportlab für PDF (Python-native)

---

**Letzte Aktualisierung:** 24. November 2025
**Nächstes Review:** 01. Dezember 2025
