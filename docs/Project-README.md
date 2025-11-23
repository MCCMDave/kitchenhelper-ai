# KitchenHelper-AI Development

## Projektübersicht
KitchenHelper-AI ist eine intelligente Web-App zur Rezeptgenerierung aus verfügbaren Zutaten mit KI-Integration (Claude, OpenAI, Gemini). Die App bietet spezialisierte Ernährungsprofile (Diabetes mit BE/KE, Keto, Vegan, etc.) und ein Freemium-Geschäftsmodell.

**Status:** Migration von Single-Page HTML zu Full-Stack Python-App

## Tech-Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Datenbank:** SQLite → PostgreSQL (bei Skalierung)
- **Authentication:** JWT (JSON Web Tokens)
- **Payment:** Stripe API
- **API-Clients:** Anthropic, OpenAI, Google Gemini
- **ORM:** SQLAlchemy
- **Validation:** Pydantic

### Frontend
- **Core:** HTML5, CSS3, Vanilla JavaScript
- **Design:** Mobile-First, Progressive Web App
- **Storage:** API-basiert (vorher localStorage)
- **später optional:** React/Vue (nach MVP)

### Deployment
- **Phase 1 (MVP):** Raspberry Pi 5 Homelab + Cloudflare Tunnel
- **Phase 2 (Production):** Railway.app / Fly.io
- **Database Hosting:** Railway PostgreSQL / Supabase
- **CDN:** Cloudflare

## Architektur

```
┌─────────────────────────────────────────────┐
│           Frontend (HTML/CSS/JS)            │
│  ┌─────────┬─────────┬──────────┬────────┐ │
│  │ Recipe  │ Profile │ Favorites│ Payment│ │
│  │ Manager │ Manager │ Manager  │ Portal │ │
│  └────┬────┴────┬────┴─────┬────┴───┬────┘ │
└───────┼─────────┼──────────┼────────┼──────┘
        │         │          │        │
        ▼         ▼          ▼        ▼
┌───────────────────────────────────────────┐
│         FastAPI Backend (REST API)        │
│  ┌──────────────────────────────────────┐ │
│  │         API Endpoints                │ │
│  │  /auth/  /recipes/  /users/  /pay/  │ │
│  └──────────┬────────────────┬──────────┘ │
│             ▼                ▼             │
│  ┌──────────────┐  ┌──────────────────┐  │
│  │ Auth Service │  │  Recipe Service  │  │
│  │   (JWT)      │  │  (AI Integration)│  │
│  └──────┬───────┘  └────────┬─────────┘  │
│         ▼                    ▼             │
│  ┌──────────────────────────────────────┐ │
│  │        SQLAlchemy ORM                │ │
│  └──────────────┬───────────────────────┘ │
└─────────────────┼───────────────────────────┘
                  ▼
         ┌─────────────────┐
         │ SQLite Database │
         │   (später PG)   │
         └─────────────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
  ┌───────────┐    ┌──────────────┐
  │  Stripe   │    │  AI APIs     │
  │  Payment  │    │ Claude/GPT/  │
  │  Gateway  │    │   Gemini     │
  └───────────┘    └──────────────┘
```

## Datenbankschema (Core)

```sql
-- Users
users (
    id, email, password_hash, created_at,
    subscription_tier, stripe_customer_id
)

-- Ingredients
ingredients (
    id, user_id, name, category, 
    expiry_date, is_permanent
)

-- Recipes (Generated)
recipes (
    id, user_id, name, description,
    difficulty, cooking_time, method,
    servings, created_at
)

-- Recipe Ingredients (Junction)
recipe_ingredients (
    recipe_id, ingredient_name, 
    amount, carbs
)

-- Favorites
favorites (
    id, user_id, recipe_id, created_at
)

-- Diet Profiles
user_diet_profiles (
    id, user_id, profile_type,
    settings_json, is_active
)
```

## API-Struktur

```
/api/v1/
├── auth/
│   ├── POST /register
│   ├── POST /login
│   └── POST /refresh
├── users/
│   ├── GET /me
│   ├── PATCH /me
│   └── DELETE /me
├── ingredients/
│   ├── GET /
│   ├── POST /
│   ├── PATCH /{id}
│   └── DELETE /{id}
├── recipes/
│   ├── POST /generate
│   ├── GET /history
│   └── GET /{id}
├── favorites/
│   ├── GET /
│   ├── POST /
│   └── DELETE /{id}
├── profiles/
│   ├── GET /
│   ├── POST /
│   └── PATCH /{id}
└── payments/
    ├── POST /create-checkout
    ├── POST /webhook
    └── GET /subscription-status
```

## Subscription Tiers

| Feature | Demo | Basic | Premium |
|---------|------|-------|---------|
| Rezepte/Tag | 3 | 50 | ∞ |
| AI-Provider | - | Claude | Alle |
| Ernährungsprofile | 1 | 3 | ∞ |
| Favoriten | 5 | 50 | ∞ |
| Preis | €0 | €4.99/m | €9.99/m |

## Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (Development)
cd frontend
python -m http.server 8000

# Database
alembic upgrade head  # Migrations
```

## Deployment (Pi Homelab)

```bash
# Docker Compose Setup
docker-compose up -d

# Services:
# - FastAPI: localhost:8000
# - PostgreSQL: localhost:5432
# - Cloudflare Tunnel: kitchenhelper-ai.yourdomain.com
```

## Environment Variables

```env
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Database
DATABASE_URL=sqlite:///./kitchenhelper.db

# Auth
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# App
DEBUG=False
ALLOWED_ORIGINS=https://kitchenhelper-ai.com
```

## Security Considerations

- ✅ API-Keys nur serverseitig
- ✅ JWT mit Refresh-Tokens
- ✅ HTTPS via Cloudflare
- ✅ Rate Limiting (SlowAPI)
- ✅ CORS richtig konfiguriert
- ✅ Input Validation (Pydantic)
- ✅ SQL Injection Prevention (SQLAlchemy ORM)

## Testing

```bash
# Unit Tests
pytest tests/

# API Tests
pytest tests/api/

# Coverage
pytest --cov=app tests/
```

## Roadmap

**Phase 1: MVP (4 Wochen)**
- ✅ Backend Setup
- ✅ User Auth
- ✅ Rezept-Generation
- ✅ Frontend-Migration

**Phase 2: Monetarisierung (2 Wochen)**
- Stripe Integration
- Subscription Management
- Payment Webhooks

**Phase 3: Features (laufend)**
- Erweiterte Profile
- Social Features (Rezepte teilen)
- Mobile App (React Native)

## Team & Kontakt

**Entwickler:** David Vaupel  
**Email:** david_vaupel@hotmail.com  
**Status:** Solo-Projekt, IHK Cloud IT Administrator Zertifizierung  
**Inspired by:** Katja

---

**Version:** 1.0.0  
**Letztes Update:** November 2025

**Status:** ✅ Phase 1 Complete - Backend MVP läuft  
**Aktueller Stand:** Authentication fertig, bereit für Ingredients API  
**NÃ¤chster Meilenstein:** Recipe Generation mit AI Integration

## Quick Start (für nächste Session)
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Browse: http://127.0.0.1:8000/docs