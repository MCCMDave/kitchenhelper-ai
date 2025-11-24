# Docker Deployment Setup - KitchenHelper-AI

## 📋 KONTEXT

KitchenHelper-AI läuft aktuell lokal mit FastAPI + SQLite. Ziel: Komplettes Docker-Setup erstellen für Entwicklung auf Windows-Laptop und späteres Deployment auf Raspberry Pi 5. Setup muss plattformübergreifend funktionieren (x86_64 Windows → ARM64 Pi).

**Projekt-Pfade:**
- Stand-PC: `C:\Users\Startklar\Desktop\GitHub\kitchenhelper-ai`
- Laptop: `C:\Users\david\Desktop\GitHub\kitchenhelper-ai`

**Aktueller Stack:**
- Backend: FastAPI, SQLAlchemy, SQLite, JWT, bcrypt
- Frontend: Vanilla JS, HTML, CSS
- Python: 3.13
- Dependencies: siehe `/mnt/project/requirements.txt`

## 🎯 AUFGABEN

### Docker Files
- [ ] `Dockerfile` - Multi-stage build, Python 3.13-slim, optimiert für beide Architekturen
- [ ] `docker-compose.yml` - Service orchestration mit volume mounts
- [ ] `.dockerignore` - Exclude venv, __pycache__, .git, etc.
- [ ] `.env.example` - Template für alle Secrets

### Deployment Scripts
- [ ] `deploy.sh` (für Pi, später) - Git pull + Docker commands
- [ ] `dev-start.ps1` (für Windows) - Development startup script
- [ ] `logs-view.ps1` - Quick log viewing

### Documentation
- [ ] `docs/DOCKER-SETUP.md` - Vollständige Dokumentation:
  - Installation Docker Desktop (Windows)
  - Installation Docker (Raspberry Pi)
  - Build & Run Commands
  - Troubleshooting
  - Migration Windows → Pi
- [ ] `docs/DEPLOYMENT.md` - Pi-spezifische Deployment-Anleitung

### Configuration Updates
- [ ] `config.py` - Environment variables statt hardcoded paths
- [ ] Relative Pfade checken in allen Python files

## 📝 KRITISCHE REQUIREMENTS

### Dockerfile Specs:
```dockerfile
# Multi-stage build
FROM python:3.13-slim as base
# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"
# Non-root user
RUN useradd -m -u 1000 appuser
# Exposed port: 8000
```

### docker-compose.yml Specs:
```yaml
services:
  kitchenhelper:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./database:/app/database
      - ./logs:/app/logs
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=sqlite:///./database/kitchenhelper.db
    restart: unless-stopped
    mem_limit: 512m
    cpus: 0.5
```

### Environment Variables (.env.example):
```bash
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///./database/kitchenhelper.db
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Wichtige Punkte:
1. **Relative Pfade** - Keine absoluten Windows/Linux Pfade
2. **Line Endings** - LF statt CRLF (Git autocrlf)
3. **Multi-arch** - Funktioniert auf x86_64 UND ARM64
4. **Volume Mounts** - Database & Logs persistent
5. **Health Checks** - Container monitoring
6. **Security** - Non-root user, secrets via .env

## 🧪 TESTING

### Windows Laptop (Entwicklung):
```powershell
# Build image
docker compose build

# Start services
docker compose up -d

# View logs
docker compose logs -f

# Health check
curl http://localhost:8000/health

# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# Stop services
docker compose down

# Mit Volume cleanup
docker compose down -v
```

### Verification Checklist:
- [ ] Container startet ohne Errors
- [ ] Health check returns 200
- [ ] Swagger docs erreichbar: http://localhost:8000/docs
- [ ] Frontend erreichbar: http://localhost:8000
- [ ] Login funktioniert
- [ ] Database persistence nach restart
- [ ] Logs werden geschrieben

## 📦 DATEIEN

**Erstellen:**
- `/Dockerfile`
- `/docker-compose.yml`
- `/.dockerignore`
- `/.env.example`
- `/deploy.sh`
- `/dev-start.ps1`
- `/logs-view.ps1`
- `/docs/DOCKER-SETUP.md`
- `/docs/DEPLOYMENT.md`

**Bearbeiten:**
- `/mnt/project/config.py` (falls hardcoded paths existieren)
- `/.gitignore` (add: `.env`, `logs/`, `database/*.db`)
- `/README.md` (add: Docker-Setup Sektion)

**Nicht ändern:**
- Alle existierenden Python/JS files (außer config.py)
- Projekt-Struktur bleibt gleich

## 🎯 ZUSÄTZLICHE ANFORDERUNGEN

### PowerShell Scripts (Windows-freundlich):
```powershell
# dev-start.ps1
# Startet Backend lokal ODER in Docker (Parameter)
param([switch]$Docker)

if ($Docker) {
    Write-Host "Starting in Docker..." -ForegroundColor Green
    docker compose up -d
} else {
    Write-Host "Starting local dev server..." -ForegroundColor Green
    cd backend
    .\venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload
}
```

### Git Configuration:
```gitattributes
# .gitattributes - Force LF line endings
* text=auto
*.py text eol=lf
*.sh text eol=lf
*.yml text eol=lf
```

### README.md Update:
```markdown
## 🐳 Docker Setup

### Development (Windows):
1. Install Docker Desktop
2. Copy `.env.example` to `.env`
3. Run: `docker compose up -d`
4. Visit: http://localhost:8000

### Production (Raspberry Pi):
See: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
```

## 📊 SUCCESS METRICS

✅ Docker image buildet ohne Errors  
✅ Container startet und läuft stabil  
✅ Health check funktioniert  
✅ Alle API Endpoints erreichbar  
✅ Database persistence funktioniert  
✅ Logs werden korrekt geschrieben  
✅ Gleicher Code funktioniert auf Windows UND (später) Pi  
✅ Dokumentation vollständig und verständlich

## 🚫 NICHT TUN

- ❌ Keine Cloud-spezifischen Configs (AWS/Azure/GCP)
- ❌ Keine komplexen Orchestration-Tools (Kubernetes, Swarm)
- ❌ Keine Änderungen an bestehender Business-Logik
- ❌ Keine Datenbank-Migration von SQLite weg
- ❌ Keine Änderung der Port-Konfiguration (8000 bleibt)

## 📝 NOTIZEN

- Docker Desktop muss manuell vom User installiert werden (nicht Teil des Scripts)
- Cloudflare Tunnel Setup kommt später (separate Task)
- Pi-hole Konflikt ist KEIN Problem (unterschiedliche Ports)
- Database-File kann einfach kopiert werden für Migration

---

**START:** Erstelle Dockerfile mit multi-stage build, dann docker-compose.yml, dann alle Scripts, dann Dokumentation. Teste jeden Schritt lokal.

**WICHTIG:** Verwende relative Pfade überall! Checke config.py für hardcoded paths!