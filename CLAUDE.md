# KitchenHelper-AI - Projekt-Kontext

## Projektbeschreibung

KitchenHelper-AI ist eine Webanwendung zur KI-gesteuerten Rezeptgenerierung. Nutzer geben ihre verfuegbaren Zutaten ein und erhalten personalisierte Rezeptvorschlaege von verschiedenen KI-Anbietern (Claude, OpenAI, Gemini).

**Besonderheit:** Diabetes-Unterstuetzung mit BE/KE-Rechner fuer kohlenhydratbewusste Ernaehrung.

## Tech-Stack

- **Backend:** Python mit FastAPI
- **Datenbank:** SQLAlchemy ORM (SQLite, spaeter PostgreSQL)
- **Authentication:** JWT Bearer Tokens
- **Frontend:** Vanilla HTML/CSS/JavaScript (kein Framework)
- **Payments:** Stripe Integration (geplant)
- **Deployment:** Docker auf Raspberry Pi Homelab

## Projektstruktur

```
Kitchenhelper/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy Models
│   │   ├── schemas/       # Pydantic Schemas
│   │   ├── routes/        # API Endpoints
│   │   ├── services/      # Business Logic
│   │   └── utils/         # Helper Functions
│   ├── database/          # SQLite DB
│   └── venv/              # Virtual Environment
├── frontend/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript Modules
│   ├── index.html         # Login Page
│   └── dashboard.html     # Main App
├── docs/                  # Dokumentation
├── prototypes/            # Original HTML-Prototyp
└── CLAUDE.md
```

## Aktueller Status

- **Phase:** Feature-Complete MVP
- **Backend:** FastAPI mit allen Endpoints (Auth, Users, Ingredients, Recipes, Favorites, Profiles, PDF Export)
- **Frontend:** Vanilla JS SPA mit API-Integration, Multi-Language (EN/DE)
- **Neue Features (23.11.2025):**
  - PDF Export fuer Rezepte (reportlab)
  - Multi-Language Support (Englisch/Deutsch)
  - Favoriten als Modal statt Expand/Collapse
  - Bilinguale Rezeptgenerierung
- **Naechster Schritt:** Testing, Deployment, echte KI-Integration

## Wichtige Befehle

```bash
# Backend starten (Windows PowerShell)
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload

# Backend starten (Git Bash)
cd backend
source venv/Scripts/activate
uvicorn app.main:app --reload

# Frontend oeffnen
# Einfach frontend/index.html im Browser oeffnen
# Oder mit Live Server Extension in VS Code
```

## URLs

- **Backend API:** http://127.0.0.1:8000
- **Swagger Docs:** http://127.0.0.1:8000/docs
- **Frontend:** frontend/index.html (lokal oeffnen)

## Coding-Richtlinien

Siehe `docs/CODING-GUIDELINES.md` fuer detaillierte Regeln. Die wichtigsten:

### Python/Backend
- Type Hints verwenden (Pydantic Models)
- Async-Funktionen fuer I/O-Operationen
- Try-Except fuer Fehlerbehandlung
- Keine hartcodierten Pfade oder Secrets

### Allgemein
- KISS-Prinzip: Keep It Simple, Stupid
- Klare Variablennamen
- Kommentare wo noetig
- UTF-8 Encoding

## API-Struktur

Die geplante API ist dokumentiert in `docs/API-Documentation.md`. Hauptendpoints:

- `/auth/*` - Registrierung, Login, Token-Refresh
- `/users/me` - Profilverwaltung
- `/ingredients` - CRUD fuer Zutaten
- `/recipes/generate` - KI-Rezeptgenerierung (mit language parameter)
- `/recipes/{id}/export/pdf` - PDF Export
- `/favorites` - Favoritenverwaltung
- `/profiles` - Ernaehrungsprofile (Diabetes, Vegan, etc.)
- `/payments/*` - Stripe Integration

## Subscription-Tiers

| Tier | Rezepte/Tag | API Calls/Min | Favoriten |
|------|-------------|---------------|-----------|
| Demo | 3 | 10 | 5 |
| Basic | 50 | 60 | 50 |
| Premium | Unbegrenzt | 120 | Unbegrenzt |

## Umgebungsvariablen (geplant)

```env
DATABASE_URL=sqlite:///./kitchenhelper.db
SECRET_KEY=<jwt-secret>
ANTHROPIC_API_KEY=<api-key>
OPENAI_API_KEY=<api-key>
GOOGLE_AI_API_KEY=<api-key>
STRIPE_SECRET_KEY=<stripe-key>
STRIPE_WEBHOOK_SECRET=<webhook-secret>
```

## Hinweise fuer Claude

- Dokumentation ist auf Deutsch
- Der Entwickler (Dave) lernt Python/FastAPI - erklaere gerne Konzepte
- Deployment-Ziel ist ein Raspberry Pi mit Docker
- GDPR-Compliance beachten (EU-Nutzer)
- Bei Unsicherheiten: Lieber nachfragen als raten

## Ressourcen

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Stripe API](https://stripe.com/docs/api)
- [JWT.io](https://jwt.io)

---

**Letzte Aktualisierung:** 23. November 2025