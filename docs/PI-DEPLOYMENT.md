# 🥧 Pi Deployment - Git Workflow

## Voraussetzungen

- Raspberry Pi 5 (8GB) mit Raspbian OS Headless
- Docker bereits installiert
- Git bereits lokal konfiguriert (du pushst schon zu GitHub)

---

## 1. Einmalige Installation auf dem Pi

### **Schritt 1: SSH zum Pi verbinden**

```bash
# SSH Config angepasst (einfacher Zugriff)
ssh pi

# Falls SSH Config noch nicht angepasst:
# ssh pi@<PI-IP>
```

### **Schritt 2: Git installieren (falls nicht vorhanden)**

```bash
# Git Version prüfen
git --version

# Falls "command not found":
sudo apt update
sudo apt install git -y

# Git konfigurieren (wichtig für commits auf Pi!)
git config --global user.name "MCCMDave"
git config --global user.email "deine@email.de"

# Credential Helper (speichert GitHub Token)
git config --global credential.helper store
```

### **Schritt 3: Repository klonen**

```bash
# In Home-Verzeichnis (empfohlen!)
cd ~

# Repository klonen
git clone https://github.com/MCCMDave/kitchenhelper-ai.git

# Username: MCCMDave
# Password: <DEIN-GITHUB-PERSONAL-ACCESS-TOKEN>

# In Projekt wechseln
cd kitchenhelper-ai

# Verzeichnisstruktur prüfen
ls -la
```

**Speicherort:** `~/kitchenhelper-ai` = `/home/pi/kitchenhelper-ai`

**Verzeichnisstruktur auf dem Pi:**
```
/home/pi/
├── kitchenhelper-ai/          ← Dein Projekt hier!
│   ├── backend/
│   │   ├── app/
│   │   ├── database/           ← SQLite DB wird hier erstellt
│   │   └── requirements.txt
│   ├── frontend/
│   ├── docs/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── .env                    ← Du erstellst diese Datei
│   └── .gitignore
├── nextcloud/                  ← Deine bestehende Nextcloud
└── backup-kitchen.sh           ← Backup Script (optional)
```

**Warum Home-Verzeichnis?**
- ✅ Einfacher Zugriff: `cd ~/kitchenhelper-ai`
- ✅ Kein Root nötig
- ✅ User-Rechte automatisch korrekt
- ✅ Backups einfacher (nur /home/pi sichern)
- ✅ Neben Nextcloud gut organisiert

**Personal Access Token erstellen** (falls noch nicht vorhanden):
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Scopes: ✅ **repo**
4. Token als Passwort beim Clone nutzen

### **Schritt 3: Ollama installieren**

```bash
# Ollama auf Host installieren (NICHT im Container!)
curl -fsSL https://ollama.ai/install.sh | sh

# Modell laden (~2GB, dauert 2-5 Min)
ollama pull llama3.2

# Test
curl http://localhost:11434/api/tags
# Sollte zeigen: {"models":[{"name":"llama3.2:latest",...}]}
```

### **Schritt 4: .env erstellen**

```bash
cd ~/kitchenhelper-ai

# .env aus Template erstellen
cp .env.example .env
nano .env
```

**Wichtige Einträge:**

```env
# JWT Secret generieren:
# python3 -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET_KEY=<HIER-GENERIERTES-SECRET>

DATABASE_URL=sqlite:///./database/kitchenhelper.db
DEBUG=False

# Pi's IP oder Domain
ALLOWED_ORIGINS=http://192.168.1.100:8000,http://localhost:8000

# AI Provider
GOOGLE_AI_API_KEY=              # Leer lassen (nur Ollama)
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
```

**Speichern:** `CTRL+O` → `Enter` → `CTRL+X`

### **Schritt 5: Docker starten**

```bash
cd ~/kitchenhelper-ai

# Build & Start
docker compose build
docker compose up -d

# Logs prüfen
docker compose logs -f
```

**Erwartete Logs:**
```
kitchenhelper-api | INFO: AI Generator initialized - Gemini: False, Ollama: True
kitchenhelper-api | INFO: Uvicorn running on http://0.0.0.0:8000
```

**CTRL+C zum Beenden**

### **Schritt 6: Test**

```bash
# Health Check
curl http://localhost:8000/health
# {"status":"healthy"}

# Von Laptop aus (Browser):
# http://<PI-IP>:8000/docs
```

**✅ Installation fertig!**

---

## 2. Tägliche Updates (2 Minuten)

### **Auf Laptop: Code ändern & pushen**

```powershell
cd C:\Users\david\Desktop\GitHub\kitchenhelper-ai

# Status prüfen
git status

# Alle Änderungen stagen
git add .

# Commit (mit aussagekräftiger Message!)
git commit -m "✨ Add new feature"

# Zu GitHub pushen
git push
```

**Commit Message Emojis:**
- ✨ feat - Neues Feature
- 🐛 fix - Bugfix
- 📝 docs - Dokumentation
- ♻️ refactor - Refactoring
- 🎨 style - CSS/UI
- 🔧 chore - Config

### **Auf Pi: Updates holen & deployen**

```bash
# SSH zum Pi
ssh pi@<PI-IP>
cd ~/kitchenhelper-ai

# Updates holen
git pull

# Container neu starten
docker compose down
docker compose up -d --build

# Logs prüfen
docker compose logs -f
```

**Fertig!** 🎉

---

## 3. Spezielle Update-Szenarien

### **Nur Backend-Code geändert**

```bash
# Pi
git pull
docker compose restart kitchenhelper  # Kein Rebuild!
```

### **Dependencies geändert (requirements.txt)**

```bash
# Pi
git pull
docker compose down
docker compose build --no-cache  # Wichtig!
docker compose up -d
```

### **Datenbank-Migration (Alembic)**

```bash
# Pi
git pull
docker compose exec kitchenhelper alembic upgrade head
docker compose restart kitchenhelper
```

---

## 4. Rollback bei Problemen

### **Zum letzten funktionierenden Stand**

```bash
# Commits anzeigen
git log --oneline -5

# Zu bestimmtem Commit zurück
git reset --hard <commit-hash>

# Container neu starten
docker compose down
docker compose up -d --build
```

### **Nur eine Datei zurücksetzen**

```bash
git checkout HEAD~1 backend/app/routes/recipes.py
docker compose restart kitchenhelper
```

---

## 5. Troubleshooting

### **"Port already in use"**

```bash
# Port-Konflikt mit Nextcloud prüfen
docker ps

# Lösung: Ports in docker-compose.yml anpassen
nano docker-compose.yml
# Ändere 8000:8000 zu einem freien Port
```

### **"Out of memory" beim Build**

```bash
# Nextcloud temporär stoppen
cd ~/nextcloud
docker compose stop

# Kitchen bauen
cd ~/kitchenhelper-ai
docker compose build

# Nextcloud wieder starten
cd ~/nextcloud
docker compose start
```

### **Ollama nicht erreichbar vom Container**

```bash
# Prüfen ob Ollama läuft
systemctl status ollama

# Test vom Container
docker compose exec kitchenhelper curl http://host.docker.internal:11434/api/tags
```

### **Git Authentication Failed**

```bash
# Credential Helper aktivieren
git config --global credential.helper store

# Beim nächsten git pull: Token eingeben, wird gespeichert
```

---

## 6. Backup

**Database Backup (täglich per Cron):**

```bash
# Backup Script erstellen
nano ~/backup-kitchen.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/mnt/ssd/backups/kitchenhelper"

mkdir -p $BACKUP_DIR

# Database
cp ~/kitchenhelper-ai/backend/database/kitchenhelper.db \
   $BACKUP_DIR/db_$DATE.db

# .env
cp ~/kitchenhelper-ai/.env $BACKUP_DIR/.env_$DATE

# Alte Backups löschen (>30 Tage)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
```

```bash
chmod +x ~/backup-kitchen.sh

# Cronjob (täglich 2 Uhr)
crontab -e
# Add: 0 2 * * * /home/pi/backup-kitchen.sh
```

---

## 7. Monitoring

### **Resource Usage**

```bash
# Container Stats
docker stats --no-stream

# Disk Usage
df -h
du -sh ~/kitchenhelper-ai/backend/database

# Logs Größe
du -sh ~/kitchenhelper-ai/logs
```

### **Health Check**

```bash
# API Status
curl http://localhost:8000/health

# Ollama Status
systemctl status ollama

# Container Status
docker compose ps
```

---

## Quick Reference

```bash
# Update Workflow
git pull && docker compose up -d --build

# Logs anzeigen
docker compose logs -f

# Container neu starten
docker compose restart

# Stoppen/Starten
docker compose down
docker compose up -d

# Rebuild (nach Dependencies)
docker compose build --no-cache

# Rollback
git reset --hard <commit-hash>
docker compose up -d --build
```

---

## Nächste Schritte

- [ ] Externen Zugriff (Cloudflare Tunnel oder Tailscale)
- [ ] HTTPS/SSL (Let's Encrypt)
- [ ] Monitoring (Grafana optional)
- [ ] CI/CD (GitHub Actions auto-deploy)

**Siehe auch:**
- `AI-INTEGRATION.md` - Ollama/Gemini Setup
- `DATA-ENCRYPTION.md` - E2EE Konzept
- `GIT-DEPLOYMENT.md` - Git Details & Troubleshooting
