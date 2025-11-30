# ✅ Raspberry Pi Deployment - Checkliste

## 🎯 Überblick

Diese Checkliste führt dich Schritt für Schritt durch das komplette Deployment auf deinem Raspberry Pi 5.

**Geschätzte Dauer:** 15-20 Minuten (einmalig)

---

## 📋 Vorbereitungen (Laptop)

### 1. Code zu GitHub pushen

```powershell
cd C:\Users\david\Desktop\GitHub\kitchenhelper-ai

# Status prüfen
git status

# Alle Änderungen stagen
git add .

# Commit (inkl. Streaming-Feature)
git commit -m "🚀 feat: Add streaming feature + deployment docs

- Loading message with Pro promotion
- SSE streaming for Ollama recipes
- Complete Pi deployment guide
- Ready for Pi deployment"

# Push zu GitHub
git push
```

**✅ Erwartung:** Alle Dateien auf GitHub, bereit zum Clonen

---

## 🥧 Pi Deployment

### 2. SSH zum Pi verbinden

```bash
ssh pi
# Alias funktioniert (aus Memory: ssh pi ohne IP)
```

**✅ Erwartung:** Erfolgreich verbunden zu `pi@raspberrypi`

---

### 3. Repository klonen

```bash
cd ~
git clone https://github.com/MCCMDave/kitchenhelper-ai.git
cd kitchenhelper-ai
ls -la
```

**Credentials beim Clone:**
- Username: `MCCMDave`
- Password: Dein GitHub **Personal Access Token**
  - Falls nicht vorhanden: https://github.com/settings/tokens
  - Scopes: ✅ repo

**✅ Erwartung:** Repository erfolgreich geklont in `~/kitchenhelper-ai`

---

### 4. Ollama prüfen (sollte bereits laufen)

```bash
# Status prüfen
systemctl status ollama

# Modell prüfen
ollama list
# Sollte llama3.2:latest anzeigen

# API-Test
curl http://localhost:11434/api/tags
```

**✅ Erwartung:**
- Ollama läuft (active)
- llama3.2:latest vorhanden (~2GB)
- API antwortet mit JSON

**Falls Ollama fehlt:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

---

### 5. .env-Datei erstellen

```bash
cd ~/kitchenhelper-ai

# Template kopieren
cp .env.example .env

# Bearbeiten
nano .env
```

**Wichtige Werte anpassen:**

```env
# JWT Secret generieren:
JWT_SECRET_KEY=HIER-GENERIERTES-SECRET

# Generieren mit:
python3 -c "import secrets; print(secrets.token_hex(32))"
# Kopiere die Ausgabe und ersetze HIER-GENERIERTES-SECRET

DATABASE_URL=sqlite:///./database/kitchenhelper.db
DEBUG=False

# Pi's IP oder Tailscale IP
ALLOWED_ORIGINS=http://192.168.1.X:8000,http://localhost:8000

# AI Provider
GOOGLE_AI_API_KEY=              # Leer lassen (nur Ollama)
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
```

**Speichern:** `CTRL+O` → `Enter` → `CTRL+X`

**✅ Erwartung:** `.env` existiert mit korrektem JWT_SECRET_KEY

---

### 6. Docker Container bauen & starten

```bash
cd ~/kitchenhelper-ai

# Build
docker compose build

# Start im Hintergrund
docker compose up -d

# Logs beobachten
docker compose logs -f
```

**✅ Erwartung (in Logs):**
```
kitchenhelper-api | INFO: AI Generator initialized - Gemini: False, Ollama: True
kitchenhelper-api | INFO: Uvicorn running on http://0.0.0.0:8000
```

**CTRL+C** zum Beenden der Log-Anzeige (Container läuft weiter)

---

### 7. Health Check

```bash
# Vom Pi aus:
curl http://localhost:8000/health
# {"status":"healthy"}

# API Docs:
curl http://localhost:8000/docs
# Sollte HTML zurückgeben

# Ollama Integration testen (vom Container):
docker compose exec kitchenhelper curl http://host.docker.internal:11434/api/tags
# {"models":[{"name":"llama3.2:latest",...}]}
```

**✅ Erwartung:** Alle 3 Endpoints antworten korrekt

---

### 8. Vom Laptop aus testen

**Browser öffnen (auf Laptop):**

```
http://<PI-IP>:8000/docs
```

**Ersetze `<PI-IP>` mit:**
- Lokale IP: `192.168.1.X` (via `ip addr` auf Pi)
- Tailscale IP: `100.X.X.X` (via `tailscale ip` auf Pi)

**✅ Erwartung:** Swagger UI erscheint, alle Endpoints sichtbar

---

## 🧪 Funktionstest

### 9. User registrieren & Rezept generieren

**Über Swagger UI:**

1. **POST /auth/register**
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "Test1234!"
   }
   ```
   ✅ Erwartung: 201 Created

2. **POST /auth/login**
   ```json
   {
     "username": "testuser",
     "password": "Test1234!"
   }
   ```
   ✅ Erwartung: Token erhalten, kopieren

3. **Authorize-Button** → Token einfügen → "Authorize"

4. **POST /ingredients**
   ```json
   {
     "name": "Tomaten",
     "category": "vegetables",
     "carbs": 3.5
   }
   ```
   ✅ Erwartung: Zutat erstellt mit ID

5. **POST /recipes/generate**
   ```json
   {
     "ingredient_ids": [1],
     "ai_provider": "ai",
     "servings": 2,
     "language": "de"
   }
   ```
   ✅ Erwartung: Nach 35-40s → Rezept generiert (Ollama llama3.2)

---

## 🎉 Deployment erfolgreich!

### Container-Management

```bash
# Logs anzeigen
docker compose logs -f

# Container neu starten
docker compose restart

# Stoppen
docker compose down

# Starten
docker compose up -d

# Status prüfen
docker compose ps
```

### Täglicher Update-Workflow

**Laptop:**
```powershell
git add .
git commit -m "✨ feat: ..."
git push
```

**Pi:**
```bash
ssh pi
cd ~/kitchenhelper-ai
git pull
docker compose up -d --build
docker compose logs -f
```

---

## 🐛 Troubleshooting

### "Port 8000 already in use"

```bash
# Prüfen was läuft
docker ps

# Falls Nextcloud auf 8080 läuft: OK
# Falls anderer Container auf 8000: Anpassen in docker-compose.yml
nano docker-compose.yml
# Ändere 8000:8000 → 8001:8000
```

### "Out of memory" beim Build

```bash
# Nextcloud temporär stoppen
docker compose -f ~/nextcloud/docker-compose.yml stop

# Kitchen bauen
cd ~/kitchenhelper-ai
docker compose build

# Nextcloud wieder starten
docker compose -f ~/nextcloud/docker-compose.yml start
```

### Ollama nicht erreichbar

```bash
# Prüfen
systemctl status ollama

# Restart
sudo systemctl restart ollama

# Test vom Container
docker compose exec kitchenhelper curl http://host.docker.internal:11434/api/tags
```

### Git Pull klappt nicht

```bash
# Credential Helper aktivieren
git config --global credential.helper store

# Beim nächsten Pull: Token eingeben, wird gespeichert
```

---

## 📚 Weitere Docs

- **Deployment Details:** `docs/PI-DEPLOYMENT.md`
- **Streaming-Feature:** `docs/STREAMING-FEATURE.md`
- **AI Integration:** `docs/AI-INTEGRATION.md`
- **Projekt-Kontext:** `docs/CLAUDE.md`

---

## 🔄 Nächste Schritte (optional)

### Streaming aktivieren (Beta)

```javascript
// In frontend/js/recipes.js:64
const useStreaming = true; // Aktuell: false
```

Dann git add, commit, push, git pull auf Pi, rebuild.

### Externen Zugriff

- Cloudflare Tunnel: Kostenlos, HTTPS automatisch
- Tailscale: Bereits aktiv, sicher über VPN
- ngrok: Temporär für Tests

### Monitoring

```bash
# Resource Usage
docker stats --no-stream

# Disk Space
df -h
du -sh ~/kitchenhelper-ai/backend/database
```

---

**Viel Erfolg beim Deployment! 🚀**
