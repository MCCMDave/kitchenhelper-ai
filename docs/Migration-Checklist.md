# KitchenHelper-AI Migration Checklist

**Start:** November 2025  
**Ziel:** Full-Stack Python Migration + Monetarisierung  
**Geschätzte Dauer:** 4-6 Wochen

---

## Phase 1: Backend Setup (Woche 1)

### 1.1 Projekt-Initialisierung
- [ ] FastAPI-Projekt erstellen (`fastapi-cli` oder manuell)
- [ ] Virtual Environment einrichten
- [ ] `requirements.txt` erstellen
- [ ] Git Repository initialisieren
- [ ] `.gitignore` konfigurieren (`.env`, `venv/`, `__pycache__/`)
- [ ] Projektstruktur aufbauen:
  ```
  backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── config.py
  │   ├── models/
  │   ├── schemas/
  │   ├── routes/
  │   ├── services/
  │   └── utils/
  ├── tests/
  ├── alembic/
  ├── requirements.txt
  └── .env.example
  ```

### 1.2 Datenbank Setup
- [ ] SQLAlchemy konfigurieren
- [ ] Alembic für Migrations initialisieren
- [ ] Models definieren:
  - [ ] `User` Model
  - [ ] `Ingredient` Model
  - [ ] `Recipe` Model
  - [ ] `RecipeIngredient` Model (Junction)
  - [ ] `Favorite` Model
  - [ ] `DietProfile` Model
- [ ] Erste Migration erstellen & ausführen
- [ ] Test-Daten erstellen (Seed Script)

### 1.3 Authentication
- [ ] JWT-Utils implementieren (`create_token`, `verify_token`)
- [ ] Password Hashing (bcrypt/passlib)
- [ ] User Registration Endpoint
- [ ] Login Endpoint
- [ ] Token Refresh Endpoint
- [ ] Auth Middleware/Dependency
- [ ] Tests für Auth

### 1.4 Core API Endpoints
- [ ] `/users/me` (GET, PATCH, DELETE)
- [ ] `/ingredients` CRUD (GET, POST, PATCH, DELETE)
- [ ] Health Check Endpoint (`/health`)
- [ ] CORS konfigurieren
- [ ] Environment Variables (.env)
- [ ] Error Handling Middleware

**Milestone 1:** Backend läuft lokal, Auth funktioniert, CRUD-Operationen testen ✅

---

## Phase 2: AI Integration (Woche 2)

### 2.1 AI Service Layer
- [ ] `AIService` Klasse erstellen
- [ ] Claude API Integration
  - [ ] Request-Builder für Rezepte
  - [ ] Response-Parser (JSON)
  - [ ] Error Handling
- [ ] OpenAI API Integration
- [ ] Gemini API Integration
- [ ] Provider-Switcher implementieren
- [ ] Rate Limiting (pro Provider)
- [ ] API-Keys serverseitig speichern

### 2.2 Recipe Generation
- [ ] `/recipes/generate` Endpoint
  - [ ] Zutaten validieren
  - [ ] Diet Profiles berücksichtigen
  - [ ] AI Provider auswählen
  - [ ] Daily Limits prüfen (Tier-basiert)
  - [ ] Rezepte in DB speichern
- [ ] `/recipes/history` Endpoint
- [ ] `/recipes/{id}` Endpoint
- [ ] Nutrition Calculation Service
  - [ ] BE/KE-Rechner
  - [ ] Portionsrechner
- [ ] Tests für Recipe-Generation

### 2.3 Demo Mode
- [ ] Demo-Rezepte Generator (ohne API)
- [ ] Daily Limit Tracking (localStorage → DB)
- [ ] Limit-Reset Logic (täglich)
- [ ] Upgrade-Modal Trigger

**Milestone 2:** Rezeptgenerierung funktioniert mit echten AI-APIs ✅

---

## Phase 3: Frontend Migration (Woche 2-3)

### 3.1 Static Files Setup
- [ ] FastAPI static file serving konfigurieren
- [ ] HTML/CSS/JS aus Single-File extrahieren:
  - [ ] `index.html`
  - [ ] `styles.css`
  - [ ] `app.js`
- [ ] Asset-Struktur:
  ```
  frontend/
  ├── index.html
  ├── css/
  │   └── styles.css
  ├── js/
  │   ├── app.js
  │   ├── api.js
  │   ├── auth.js
  │   └── components/
  └── assets/
  ```

### 3.2 API-Client Refactoring
- [ ] `api.js` Modul erstellen
- [ ] Auth Token Management (localStorage)
- [ ] API-Base-URL konfigurierbar
- [ ] Request Interceptor (Auto-Token)
- [ ] Response Interceptor (Error Handling)
- [ ] Alle API-Calls migrieren:
  - [ ] Auth (Login/Register/Refresh)
  - [ ] Ingredients CRUD
  - [ ] Recipe Generation
  - [ ] Favorites
  - [ ] Profiles

### 3.3 localStorage → API Migration
- [ ] Ingredients: API statt localStorage
- [ ] Favorites: API statt localStorage
- [ ] Diet Profiles: API statt localStorage
- [ ] API Keys: Aus Frontend entfernen
- [ ] User Settings: API statt localStorage
- [ ] Migration-Script für bestehende User (optional)

### 3.4 UI Components
- [ ] Login/Register Modal
- [ ] Loading States verbessern
- [ ] Error Messages (API-Errors)
- [ ] Offline-Handling (Service Worker?)
- [ ] PWA Manifest

**Milestone 3:** Frontend kommuniziert komplett mit Backend API ✅

---

## Phase 4: Payment Integration (Woche 3)

### 4.1 Stripe Setup
- [ ] Stripe Account erstellen
- [ ] API Keys (Test + Live)
- [ ] Webhook Endpoint einrichten
- [ ] Stripe CLI für Testing

### 4.2 Subscription Logic
- [ ] Tier-System implementieren (Demo/Basic/Premium)
- [ ] `/payments/create-checkout` Endpoint
- [ ] Success/Cancel URLs
- [ ] Customer Portal Link
- [ ] Stripe Webhook Handler:
  - [ ] `subscription.created`
  - [ ] `subscription.updated`
  - [ ] `subscription.deleted`
  - [ ] `invoice.payment_succeeded`
  - [ ] `invoice.payment_failed`

### 4.3 Frontend Payment Flow
- [ ] Pricing Page erstellen
- [ ] Checkout-Button Integration
- [ ] Subscription Status Display
- [ ] Upgrade/Downgrade UI
- [ ] Cancel Subscription Flow

### 4.4 Access Control
- [ ] Tier-basierte Feature-Locks:
  - [ ] Recipe Limits (Demo: 3, Basic: 50, Premium: ∞)
  - [ ] AI Provider (Demo: -, Basic: Claude, Premium: Alle)
  - [ ] Favorites Limit
  - [ ] Diet Profiles Limit
- [ ] Middleware für Tier-Checks
- [ ] Upgrade-Prompts bei Limit-Erreichen

**Milestone 4:** Zahlungsabwicklung funktioniert, Abo-Management läuft ✅

---

## Phase 5: Features & Polish (Woche 4)

### 5.1 Diet Profiles
- [ ] `/profiles` CRUD komplett
- [ ] Profile-Switcher UI
- [ ] Diabetes-Einheiten (BE/KE) Settings
- [ ] Custom Profile Creation (Premium)
- [ ] Profile-Validierung

### 5.2 Favorites System
- [ ] `/favorites` CRUD komplett
- [ ] Favorite-Button in Rezept-Cards
- [ ] Favorites-Seite
- [ ] Export-Funktion (PDF?)

### 5.3 User Experience
- [ ] Onboarding-Flow für neue User
- [ ] Demo-Mode Erklärung
- [ ] Tooltips & Help-Texte
- [ ] Mobile Responsiveness testen
- [ ] PWA Installation-Prompt

### 5.4 Admin Features (optional)
- [ ] Admin Dashboard (User-Übersicht)
- [ ] Usage Analytics
- [ ] Subscription Insights
- [ ] Error Monitoring (Sentry?)

**Milestone 5:** Alle Core-Features implementiert, UX optimiert ✅

---

## Phase 6: Deployment (Woche 4-5)

### 6.1 Pi Homelab Setup
- [ ] Docker Compose File erstellen:
  - [ ] FastAPI Container
  - [ ] PostgreSQL Container (oder SQLite)
  - [ ] Nginx/Caddy Reverse Proxy
- [ ] Environment Variables setzen
- [ ] SSL via Cloudflare Tunnel
- [ ] Backup-Strategie (DB)
- [ ] Health Checks
- [ ] Logging konfigurieren

### 6.2 Testing & QA
- [ ] Unit Tests (Backend)
- [ ] Integration Tests (API)
- [ ] E2E Tests (Frontend)
- [ ] Load Testing (Apache Bench/Locust)
- [ ] Security Audit
- [ ] GDPR Compliance Check

### 6.3 Monitoring
- [ ] Uptime Monitoring (UptimeRobot)
- [ ] Error Tracking (Sentry)
- [ ] Analytics (Plausible/Matomo)
- [ ] Performance Monitoring
- [ ] Database Backups automatisieren

### 6.4 Documentation
- [ ] API Docs finalisieren (Swagger)
- [ ] User Guide erstellen
- [ ] Developer Docs (Setup, Contributing)
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] FAQ

**Milestone 6:** App läuft produktiv auf Pi Homelab ✅

---

## Phase 7: Launch Prep (Woche 5-6)

### 7.1 Marketing
- [ ] Landing Page erstellen
- [ ] SEO optimieren
- [ ] Social Media Assets
- [ ] Launch-Ankündigung vorbereiten
- [ ] Beta-Tester einladen

### 7.2 Production Deployment (optional)
- [ ] Railway.app/Fly.io Account
- [ ] Production Deployment testen
- [ ] DNS konfigurieren
- [ ] SSL Certificates
- [ ] Performance Tuning
- [ ] CDN konfigurieren (Cloudflare)

### 7.3 Go-Live
- [ ] Soft Launch (Beta)
- [ ] Monitoring aktivieren
- [ ] Support-Email einrichten
- [ ] Bug-Tracking System
- [ ] Feedback-Loop etablieren

**Milestone 7:** Public Beta Launch 🚀

---

## Bonus: Future Features

### Geplante Features (Post-Launch)
- [ ] Einkaufslisten-Generator
- [ ] Meal Planning (Wochenplanung)
- [ ] Social Features (Rezepte teilen)
- [ ] User-generierte Rezepte
- [ ] Barcode-Scanner (Mobile)
- [ ] Alexa/Google Home Integration
- [ ] Multi-Language Support
- [ ] Dark Mode
- [ ] Rezept-Bewertungen & Kommentare
- [ ] Ernährungstagebuch
- [ ] Mobile App (React Native)

---

## Risiken & Mitigation

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| API-Kosten explodieren | Mittel | Hoch | Rate Limiting, Caching, Tier-Limits |
| Pi-Homelab instabil | Niedrig | Mittel | Cloud-Backup (Railway), Monitoring |
| Stripe-Abrechnung Fehler | Niedrig | Hoch | Webhook-Testing, Sandbox-Tests |
| GDPR-Verstöße | Niedrig | Sehr Hoch | Legal Review, Privacy by Design |
| Schlechte Performance | Mittel | Mittel | Load Testing, CDN, DB-Optimierung |

---

## Definition of Done

Eine Phase gilt als **abgeschlossen**, wenn:
1. ✅ Alle Tasks erledigt
2. ✅ Tests geschrieben & bestanden
3. ✅ Code reviewed
4. ✅ Dokumentation aktualisiert
5. ✅ Deployment funktioniert
6. ✅ Milestone erreicht

---

## Notizen

- **Python Version:** 3.11+
- **Deployment Target:** Raspberry Pi 5 (8GB RAM)
- **Database:** SQLite (MVP) → PostgreSQL (Production)
- **Testing Framework:** pytest
- **CI/CD:** GitHub Actions (optional)

---

**Letzte Aktualisierung:** November 2025  
**Status:** Phase 0 - Projektinitialisierung
