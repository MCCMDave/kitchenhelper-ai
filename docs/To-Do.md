# KitchenHelper-AI - To-Do Liste

**Projekt-Status:** Feature-Complete MVP
**Aktueller Stand:** Testing & Deployment-Ready
**Nächster Meilenstein:** Echte KI-Integration & Docker Deployment

---

## 🔥 Sofort (Diese Woche)

### Backend Setup
- [ ] FastAPI-Projekt initialisieren mit Ordnerstruktur
- [ ] Virtual Environment + requirements.txt
- [ ] SQLAlchemy Models definieren (User, Ingredient, Recipe)
- [ ] Alembic Migrations Setup
- [ ] JWT Authentication implementieren
- [ ] `/auth/register` + `/auth/login` Endpoints
- [ ] Environment Variables (.env) konfigurieren

### Git & Dokumentation
- [ ] Git Repository initialisieren
- [ ] `.gitignore` konfigurieren
- [ ] README.md im Repo erstellen
- [ ] Erste Version committen

**Ziel:** Lauffähiges Backend mit Auth bis Ende Woche

---

## ⏰ Diese Woche (Nach Backend Setup)

### API Endpoints
- [ ] `/users/me` (GET, PATCH, DELETE)
- [ ] `/ingredients` CRUD
- [ ] `/recipes/generate` (erstmal Mock)
- [ ] Error Handling Middleware
- [ ] CORS richtig konfigurieren

### Testing
- [ ] pytest Setup
- [ ] Auth Tests schreiben
- [ ] API Endpoint Tests

---

## 📅 Nächste Woche

### AI Integration
- [ ] Claude API Service implementieren
- [ ] OpenAI API Service implementieren
- [ ] Gemini API Service implementieren
- [ ] Recipe Generation mit echten APIs
- [ ] Nutrition Calculation Logic
- [ ] BE/KE-Rechner für Diabetes-Profil

### Frontend Start
- [ ] HTML/CSS/JS aus Single-File extrahieren
- [ ] Ordnerstruktur für Frontend anlegen
- [ ] API-Client Modul (`api.js`) erstellen
- [ ] Login/Register Modal implementieren

---

## 🎯 Sprint 1 (Woche 3-4)

### Frontend Migration
- [ ] Alle localStorage-Calls durch API-Calls ersetzen
- [ ] Ingredients Management → API
- [ ] Recipe Generation → API
- [ ] Favorites → API
- [ ] Diet Profiles → API
- [ ] Token Management implementieren

### Features
- [ ] Demo-Mode mit Daily Limits
- [ ] Recipe History anzeigen
- [ ] Favorites System UI
- [ ] Loading States & Error Handling

---

## 💰 Sprint 2 (Woche 5-6)

### Stripe Integration
- [ ] Stripe Account + Test Keys
- [ ] `/payments/create-checkout` implementieren
- [ ] Webhook Endpoint für Subscription Events
- [ ] Tier-System (Demo/Basic/Premium) umsetzen
- [ ] Pricing Page erstellen
- [ ] Subscription Status UI
- [ ] Feature Locks nach Tier

---

## 🚀 Deployment (Woche 7)

### Pi Homelab
- [ ] Docker Compose Setup
- [ ] PostgreSQL Container (oder SQLite behalten)
- [ ] Nginx/Caddy Reverse Proxy
- [ ] Cloudflare Tunnel konfigurieren
- [ ] Environment Variables setzen
- [ ] Backup-Strategie für DB

### Testing & QA
- [ ] Load Testing
- [ ] Security Audit
- [ ] GDPR Compliance Check
- [ ] Mobile Responsiveness testen

---

## 📋 Backlog (Nice-to-Have)

### Features
- [ ] Einkaufslisten-Generator
- [ ] Meal Planning (Wochenplanung)
- [ ] Rezepte teilen (Social)
- [ ] Barcode-Scanner Integration
- [x] Multi-Language Support (EN) ✅
- [x] Dark Mode ✅
- [ ] PWA Offline-Modus
- [x] Export zu PDF/Email ✅

### Optimierungen
- [ ] Caching-Layer (Redis?)
- [ ] CDN für Static Files
- [ ] Image Optimization
- [ ] Database Query Optimization
- [ ] API Response Compression

### Admin
- [ ] Admin Dashboard
- [ ] User Analytics
- [ ] Subscription Insights
- [ ] Error Monitoring (Sentry)
- [ ] Email-Benachrichtigungen

---

## 🐛 Bekannte Issues (aus aktuellem HTML)

### Bugs zu fixen
- [ ] Demo-Rezepte: Zutaten nicht immer korrekt zugeordnet
- [ ] Nährwert-Anzeige: Portionsrechner manchmal ungenau
- [ ] Favoriten: Keine Deduplizierung
- [ ] Mobile: Zutaten-Input zu klein
- [ ] Export-Funktion fehlt komplett

### Verbesserungen
- [ ] UX: Onboarding-Tutorial für neue User
- [ ] Performance: Lange Zutatenlisten laden langsam
- [ ] Accessibility: Keyboard-Navigation fehlt
- [ ] SEO: Meta-Tags optimieren

---

## 🔧 Tech Debt

### Code-Qualität
- [ ] Single-File HTML auflösen (✅ durch Migration)
- [ ] Inline CSS extrahieren (✅ durch Migration)
- [ ] JavaScript modularisieren (✅ durch Migration)
- [ ] Tests hinzufügen (✅ durch Migration)
- [ ] Type Hints in Python (Pydantic)

### Dokumentation
- [ ] API Docs (Swagger/OpenAPI) ✅
- [ ] User Guide schreiben
- [ ] Developer Setup Guide
- [ ] Deployment Guide

---

## 📊 Metriken & Ziele

### Launch Ziele
- [ ] < 3s Ladezeit
- [ ] 99% Uptime
- [ ] < 500ms API Response Time
- [ ] 100% Mobile-Kompatibilität
- [ ] GDPR-Compliant

### Business Ziele
- [ ] 10 Beta-User in Woche 1
- [ ] 50 User in Monat 1
- [ ] 5 Paying Customers in Monat 2
- [ ] €50 MRR in Monat 3

---

## 🎓 Lern-Ziele (für Dave)

### Python & Backend
- [ ] FastAPI Best Practices lernen
- [ ] SQLAlchemy ORM verstehen
- [ ] Alembic Migrations meistern
- [ ] JWT Auth implementieren können
- [ ] Async Python verstehen

### DevOps
- [ ] Docker Compose nutzen
- [ ] Nginx/Caddy konfigurieren
- [ ] Cloudflare Tunnel Setup
- [ ] CI/CD Pipeline (optional)
- [ ] Monitoring & Logging

### Business
- [ ] Stripe Integration hands-on
- [ ] SaaS Pricing-Strategien
- [ ] User Analytics auswerten
- [ ] GDPR/Privacy verstehen

---

## ✅ Completed

- [x] HTML Prototyp fertiggestellt (2400+ Zeilen)
- [x] AI-Integration getestet (Claude/OpenAI/Gemini)
- [x] Diabetes-Profil mit BE/KE-Rechnung
- [x] Demo-Mode implementiert
- [x] Favoriten-System
- [x] Projektplanung abgeschlossen
- [x] API-Dokumentation erstellt
- [x] Migration-Checklist erstellt
- [x] **Backend komplett implementiert** (23.11.2025)
  - Auth, Users, Ingredients, Recipes, Favorites, Profiles
- [x] **Frontend Migration abgeschlossen** (23.11.2025)
  - Vanilla JS SPA mit Modulen
- [x] **Multi-Language Support (EN/DE)** (23.11.2025)
- [x] **PDF Export fuer Rezepte** (23.11.2025)
- [x] **Dark Mode Toggle** (23.11.2025)
- [x] **Favoriten als Modal** (23.11.2025)

---

## 📝 Notizen

### Wichtige Entscheidungen
- **Tech-Stack:** FastAPI + SQLAlchemy + JWT + Stripe
- **Deployment:** Start auf Pi Homelab, später Railway/Fly.io
- **Database:** SQLite → PostgreSQL bei Bedarf
- **Frontend:** HTML/CSS/JS behalten (kein React vorerst)

### Ressourcen
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Stripe Docs:** https://stripe.com/docs/api
- **SQLAlchemy:** https://docs.sqlalchemy.org
- **JWT.io:** https://jwt.io

### Zeitplan
- **Woche 1-2:** Backend MVP
- **Woche 3-4:** Frontend Migration
- **Woche 5-6:** Payment Integration
- **Woche 7:** Deployment & Testing
- **Woche 8:** Launch 🚀

---

**Letzte Aktualisierung:** 23. November 2025
**Nächstes Review:** 30. November 2025
