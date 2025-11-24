# KitchenHelper-AI

KI-gestützte Rezeptgenerierung basierend auf deinen verfügbaren Zutaten. Spezielle Unterstützung für Diabetiker mit Kohlenhydrat-Einheiten (KE/BE) Berechnungen.

[English Version](README.md) | **Deutsche Version**

## Features

- **KI Rezeptgenerierung** - Erstelle Rezepte aus deinen Zutaten (Mock AI für Demo)
- **Zutatenverwaltung** - Verwalte deine Zutaten mit Kategorien und Ablaufdatum
- **Favoriten-System** - Speichere deine Lieblingsrezepte mit PDF-Export
- **Ernährungsprofile** - Unterstützung für mehrere Diät-Profile:
  - Diabetiker (mit KE/BE-Berechnungen)
  - Vegan / Vegetarisch
  - Glutenfrei / Laktosefrei
  - Keto / Low-Carb / High-Protein
- **Mehrsprachig** - Deutsch und Englisch (umschaltbar im Header)
- **Dark Mode** - Hell/Dunkel Theme umschaltbar
- **Responsive Design** - Funktioniert auf Desktop und Mobilgeräten

## Schnellstart (Für Tester)

### Voraussetzungen

- **Python 3.10+** installiert
- **Git** installiert
- Ein Webbrowser (Chrome, Firefox, Edge)

### Installationsschritte

1. **Repository klonen**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kitchenhelper-ai.git
   cd kitchenhelper-ai
   ```

2. **Backend einrichten**
   ```bash
   cd backend

   # Virtual Environment erstellen
   python -m venv venv

   # Virtual Environment aktivieren
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1

   # Windows Git Bash:
   source venv/Scripts/activate

   # macOS/Linux:
   source venv/bin/activate

   # Abhängigkeiten installieren
   pip install -r requirements.txt
   ```

3. **Datenbank mit Testnutzern initialisieren**
   ```bash
   # Noch im backend Ordner mit aktiviertem venv
   python scripts/db_manager.py reset
   ```

4. **Backend-Server starten**
   ```bash
   uvicorn app.main:app --reload
   ```

   Die API ist verfügbar unter: http://127.0.0.1:8000

   Swagger Docs: http://127.0.0.1:8000/docs

5. **Frontend öffnen**

   Einfach `frontend/index.html` im Browser öffnen.

   Oder VS Code mit der "Live Server" Extension nutzen.

### Testnutzer

Nach Ausführung von `db_manager.py reset` sind diese Testnutzer verfügbar:

| Email | Benutzername | Passwort |
|-------|--------------|----------|
| a@a.a | aaa | aaaaaa |
| b@b.b | bbb | bbbbbb |
| test@test.de | testuser | test123 |

Login mit Email ODER Benutzername möglich.

## Projektstruktur

```
kitchenhelper-ai/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy Models
│   │   ├── routes/        # API Endpoints
│   │   ├── schemas/       # Pydantic Schemas
│   │   ├── services/      # Business Logic (PDF, Rezeptgen)
│   │   └── utils/         # Helpers (auth, database, jwt)
│   ├── database/          # SQLite Datenbank
│   ├── scripts/           # Utility Skripte
│   │   ├── db_manager.py  # Datenbankverwaltung
│   │   └── test_login.py  # Login Test Skript
│   └── requirements.txt
├── frontend/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript Module
│   ├── index.html         # Login/Registrieren Seite
│   └── dashboard.html     # Hauptanwendung
├── docs/                  # Dokumentation
└── README.md
```

## API Endpoints

### Authentifizierung
- `POST /api/auth/register` - Neues Konto erstellen
- `POST /api/auth/login` - Login (Email oder Username)
- `POST /api/auth/request-password-reset` - Reset-Token anfordern
- `POST /api/auth/reset-password` - Passwort mit Token zurücksetzen

### Benutzer
- `GET /api/users/me` - Aktuelle Benutzerinfo abrufen
- `PUT /api/users/me` - Profil aktualisieren (Username, Email, Emoji, Passwort)
- `DELETE /api/users/me` - Account löschen

### Zutaten
- `GET /api/ingredients` - Alle Zutaten auflisten
- `POST /api/ingredients` - Zutat hinzufügen
- `PUT /api/ingredients/{id}` - Zutat aktualisieren
- `DELETE /api/ingredients/{id}` - Zutat löschen

### Rezepte
- `POST /api/recipes/generate` - Rezepte aus Zutaten generieren
- `GET /api/recipes/history` - Rezeptverlauf abrufen
- `GET /api/recipes/{id}` - Einzelnes Rezept abrufen
- `GET /api/recipes/{id}/export/pdf` - Rezept als PDF exportieren

### Favoriten
- `GET /api/favorites` - Favoriten auflisten
- `POST /api/favorites` - Favorit hinzufügen
- `DELETE /api/favorites/{id}` - Favorit entfernen

### Ernährungsprofile
- `GET /api/profiles` - Profile auflisten
- `POST /api/profiles` - Profil erstellen
- `PUT /api/profiles/{id}` - Profil aktualisieren
- `DELETE /api/profiles/{id}` - Profil löschen

## App testen

### Grundlegender Ablauf

1. **Registrieren** eines neuen Accounts oder mit Testnutzer einloggen
2. **Zutaten hinzufügen** im Zutaten-Tab
3. **Rezepte generieren** im Rezepte-Tab
   - Zutaten auswählen
   - "Rezepte generieren" klicken
4. **Favorisieren** von Rezepten (Stern-Button)
5. **Favoriten ansehen** - Klicken um Details-Modal zu öffnen
6. **PDF exportieren** - Rezept als PDF herunterladen

### Features zum Testen

- [ ] Benutzerregistrierung mit Benutzername + Emoji
- [ ] Login mit Email ODER Benutzername
- [ ] Passwort-Reset Ablauf
- [ ] Zutaten hinzufügen/bearbeiten/löschen
- [ ] Zutaten nach Kategorie filtern
- [ ] Rezepte generieren (Mock AI)
- [ ] Favoriten hinzufügen/entfernen
- [ ] Favoriten-Details im Modal ansehen
- [ ] Rezept als PDF exportieren
- [ ] Ernährungsprofile erstellen (Diabetiker, Vegan, etc.)
- [ ] Mehrere aktive Profile
- [ ] Sprachwechsel (EN/DE)
- [ ] Dark/Light Mode Wechsel
- [ ] Responsive Design (Browser-Größe ändern)
- [ ] Benutzermenü-Dropdown (Einstellungen, Profile, Logout)

## Fehlerbehebung

### Backend startet nicht
```bash
# Sicherstellen dass venv aktiviert ist
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux

# Prüfen ob alle Abhängigkeiten installiert sind
pip install -r requirements.txt

# Prüfen ob Port 8000 frei ist
```

### Datenbankfehler
```bash
# Datenbank komplett zurücksetzen
python scripts/db_manager.py reset
```

### Frontend kann nicht verbinden
- Sicherstellen dass Backend auf http://127.0.0.1:8000 läuft
- Browser-Konsole auf Fehler prüfen
- CORS-Einstellungen im Backend prüfen

### PDF Export funktioniert nicht
```bash
# Sicherstellen dass reportlab installiert ist
pip install reportlab==4.0.7
# Backend nach Installation neu starten
```

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Auth**: JWT Bearer Tokens
- **PDF**: ReportLab
- **Deployment**: Docker (x86_64 & ARM64)

---

## Docker Setup

### Entwicklung (Windows)

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) installieren
2. Environment-Datei kopieren:
   ```powershell
   Copy-Item .env.example .env
   ```
3. `.env` bearbeiten und `JWT_SECRET_KEY` ändern
4. Container starten:
   ```powershell
   docker compose up -d
   ```
5. Besuchen: http://localhost:8000

**Oder Helper-Skript verwenden:**
```powershell
.\dev-start.ps1 -Docker    # In Docker starten
.\dev-start.ps1            # Lokalen Dev-Server starten
.\dev-start.ps1 -Help      # Alle Optionen anzeigen
```

### Produktion (Raspberry Pi)

Siehe: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Docker Befehle

```bash
docker compose build       # Image bauen
docker compose up -d       # Container starten
docker compose down        # Container stoppen
docker compose logs -f     # Logs anzeigen
```

Vollständige Dokumentation: [docs/DOCKER-SETUP.md](docs/DOCKER-SETUP.md)

## Abo-Stufen (Demo)

| Stufe | Rezepte/Tag | Favoriten |
|-------|-------------|-----------|
| Demo | 3 | 5 |
| Basic | 50 | 50 |
| Premium | Unbegrenzt | Unbegrenzt |

## Beitragen

1. Repository forken
2. Feature-Branch erstellen
3. Änderungen vornehmen
4. Gründlich testen
5. Pull Request einreichen

## Lizenz

Dieses Projekt dient Bildungs- und Demonstrationszwecken.

---

**Fragen?** Öffne ein Issue auf GitHub!
