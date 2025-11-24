# Docker Setup - KitchenHelper-AI

Diese Anleitung beschreibt das komplette Docker-Setup für Entwicklung und Deployment.

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Windows Entwicklung](#windows-entwicklung)
3. [Build & Run](#build--run)
4. [Environment Konfiguration](#environment-konfiguration)
5. [Troubleshooting](#troubleshooting)
6. [Migration zum Pi](#migration-zum-pi)

---

## Voraussetzungen

### Windows (Entwicklung)

1. **Docker Desktop installieren**
   - Download: https://www.docker.com/products/docker-desktop/
   - Während der Installation "WSL 2" als Backend auswählen
   - Nach der Installation: Neustart erforderlich

2. **Docker Desktop starten**
   - Nach dem Start erscheint das Docker-Icon im System Tray
   - Warten bis "Docker Desktop is running" angezeigt wird

3. **Überprüfen**
   ```powershell
   docker --version
   docker compose version
   ```

### Raspberry Pi (Production)

Siehe: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Windows Entwicklung

### Option 1: Lokaler Dev-Server (empfohlen für Entwicklung)

```powershell
# Im Projektordner
.\dev-start.ps1
```

Dies startet uvicorn mit Hot-Reload für schnelle Entwicklung.

### Option 2: Docker Container

```powershell
# Container starten
.\dev-start.ps1 -Docker

# Container stoppen
.\dev-start.ps1 -Stop

# Image neu bauen
.\dev-start.ps1 -Build

# Logs anzeigen
.\dev-start.ps1 -Logs
```

---

## Build & Run

### Erster Start

```powershell
# 1. .env Datei erstellen
Copy-Item .env.example .env

# 2. .env bearbeiten (wichtig: JWT_SECRET_KEY ändern!)
notepad .env

# 3. Image bauen
docker compose build

# 4. Container starten
docker compose up -d

# 5. Status prüfen
docker compose ps

# 6. Logs anzeigen
docker compose logs -f
```

### Tägliche Nutzung

```powershell
# Starten
docker compose up -d

# Stoppen
docker compose down

# Stoppen und Volumes löschen (Datenbank wird gelöscht!)
docker compose down -v

# Neu bauen nach Code-Änderungen
docker compose build && docker compose up -d
```

### Health Check

```powershell
# Manuell
curl http://localhost:8000/health

# Oder im Browser
# http://localhost:8000/health
# http://localhost:8000/docs (Swagger UI)
```

---

## Environment Konfiguration

### .env Datei

```bash
# Wichtig: In Production ändern!
JWT_SECRET_KEY=your-super-secret-key-CHANGE-THIS-IN-PRODUCTION

# Datenbank (SQLite default)
DATABASE_URL=sqlite:///./database/kitchenhelper.db

# Debug-Modus (False in Production)
DEBUG=False

# CORS Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Sicheren Secret Key generieren

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### Volumes

Die Docker-Konfiguration verwendet zwei persistente Volumes:

| Volume | Pfad im Container | Beschreibung |
|--------|-------------------|--------------|
| `./backend/database` | `/app/database` | SQLite Datenbank |
| `./logs` | `/app/logs` | Anwendungs-Logs |

Diese Ordner bleiben erhalten, auch wenn der Container neu gebaut wird.

---

## Troubleshooting

### Container startet nicht

```powershell
# Logs prüfen
docker compose logs

# Container manuell starten (für mehr Output)
docker compose up
```

### Port 8000 bereits belegt

```powershell
# Prozess finden (Windows)
netstat -ano | findstr :8000

# In docker-compose.yml anderen Port wählen:
# ports:
#   - "8001:8000"
```

### Datenbank-Fehler

```powershell
# Container stoppen
docker compose down

# Datenbank löschen (Achtung: Alle Daten weg!)
Remove-Item -Recurse backend/database/*.db

# Neu starten (erstellt neue DB)
docker compose up -d
```

### Image neu bauen (nach Änderungen)

```powershell
# Ohne Cache
docker compose build --no-cache

# Dann neu starten
docker compose up -d
```

### Alle Container/Images aufräumen

```powershell
# Ungenutzte Container entfernen
docker container prune

# Ungenutzte Images entfernen
docker image prune

# Alles aufräumen (Vorsicht!)
docker system prune -a
```

### WSL 2 Probleme (Windows)

Falls Docker Desktop nicht startet:
1. Windows Features prüfen: "Windows-Subsystem für Linux" aktivieren
2. WSL 2 Update installieren: https://aka.ms/wsl2kernel
3. Docker Desktop neu installieren

---

## Migration zum Pi

### Datenbank migrieren

1. Datenbank-Datei kopieren:
   ```powershell
   # Von Windows
   scp backend/database/kitchenhelper.db pi@192.168.x.x:~/kitchenhelper-ai/backend/database/
   ```

2. Oder per USB-Stick / Cloud-Sync

### Code deployen

```bash
# Auf dem Pi
cd ~/kitchenhelper-ai
git pull origin main
./deploy.sh
```

Siehe [DEPLOYMENT.md](DEPLOYMENT.md) für die vollständige Pi-Anleitung.

---

## Architektur

```
┌─────────────────────────────────────────┐
│           Docker Container              │
│  ┌───────────────────────────────────┐  │
│  │         Python 3.13-slim          │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │    FastAPI Application      │  │  │
│  │  │    (uvicorn :8000)          │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│                    │                    │
│        ┌───────────┴───────────┐        │
│        ▼                       ▼        │
│  /app/database           /app/logs      │
└────────┬───────────────────────┬────────┘
         │                       │
    Volume Mount            Volume Mount
         │                       │
         ▼                       ▼
  ./backend/database         ./logs
   (Host System)          (Host System)
```

---

## Nächste Schritte

- [ ] Docker Desktop installieren
- [ ] `.env` Datei konfigurieren
- [ ] `docker compose build` ausführen
- [ ] `docker compose up -d` ausführen
- [ ] http://localhost:8000/docs testen

Bei Fragen: Issue auf GitHub erstellen!
