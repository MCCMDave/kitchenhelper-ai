# 🚀 Deployment Workflow - Kitchen

## Kompletter Automatisierter Workflow

**Ein Befehl macht alles:**
```bash
./scripts/deploy-to-pi.sh "Deine commit message"
```

**Was passiert automatisch:**
1. ✅ Git commit + push zu GitHub
2. ✅ SSH zu Pi → git pull
3. ✅ Frontend restart (HTTP Server port 8081)
4. ✅ Backend restart (Docker)
5. ✅ Cloudflare Cache löschen (wenn konfiguriert)

---

## 🎯 Quick Start

### Einmalig: Script ausführbar machen
```bash
chmod +x scripts/deploy-to-pi.sh
```

### Danach immer nur:
```bash
./scripts/deploy-to-pi.sh "Feature: Landing page added"
```

**Fertig!** In 30-60 Sekunden live auf:
- http://192.168.2.54:8081
- https://kitchen.kitchenhelper-ai.de

---

## ⚡ Cloudflare Auto Cache-Clear (Optional)

**Ohne Cloudflare:**
- IP:Port → Sofort ✅
- Domain → 5-30 Minuten ⏳

**Mit Cloudflare:**
- IP:Port → Sofort ✅
- Domain → 10-30 Sekunden ✅

### Setup (einmalig, 5 Minuten):

1. **Cloudflare API Token erstellen:**
   - https://dash.cloudflare.com/profile/api-tokens
   - **Create Token** → Template: "Edit zone DNS"
   - Permissions: `Zone → Cache Purge → Purge` + `Zone → Zone → Read`
   - Zone: `kitchenhelper-ai.de`
   - Token kopieren (wird nur einmal angezeigt!)

2. **Zone ID finden:**
   - https://dash.cloudflare.com
   - Domain klicken → Overview → Rechts: Zone ID kopieren

3. **In ~/.bashrc setzen** (auf deinem PC):
   ```bash
   echo 'export CLOUDFLARE_ZONE_ID="deine_zone_id"' >> ~/.bashrc
   echo 'export CLOUDFLARE_API_TOKEN="dein_api_token"' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Testen:**
   ```bash
   echo $CLOUDFLARE_ZONE_ID   # Sollte Zone ID zeigen
   echo $CLOUDFLARE_API_TOKEN # Sollte Token zeigen
   ```

**Fertig!** Ab jetzt wird Cache automatisch gelöscht.

---

## 📖 Manuelle Befehle (falls nötig)

### Nur Git Pull auf Pi (ohne Docker restart):
```bash
ssh pi "cd /home/dave/kitchenhelper-ai && git pull origin main"
```

### Nur Frontend restart:
```bash
ssh pi "pkill -f 'python3.*8081' && cd /home/dave/kitchenhelper-ai/frontend && nohup python3 -m http.server 8081 --bind 0.0.0.0 > /dev/null 2>&1 &"
```

### Nur Backend restart:
```bash
ssh pi "cd /home/dave/kitchenhelper-ai && docker-compose restart"
```

### Nur Cloudflare Cache löschen:
```bash
./scripts/cloudflare-cache-clear.sh
```

---

## 🔧 Workflow Varianten

### A) Normaler Workflow (empfohlen):
```bash
# 1. Code ändern in VS Code
# 2. Deploy script ausführen:
./scripts/deploy-to-pi.sh "Feature XYZ"
```

### B) Manueller Workflow:
```bash
# 1. Commit & Push
git add -A
git commit -m "Feature XYZ"
git push origin main

# 2. SSH zu Pi
ssh pi

# 3. Auf Pi:
cd /home/dave/kitchenhelper-ai
git pull origin main

# 4. Services restart
pkill -f 'python3.*8081'
cd frontend && nohup python3 -m http.server 8081 --bind 0.0.0.0 > /dev/null 2>&1 &
cd ..
docker-compose restart

# 5. (Optional) Cache löschen
./scripts/cloudflare-cache-clear.sh
```

### C) Nur auf Pi deployen (kein GitHub):
```bash
ssh pi "cd /home/dave/kitchenhelper-ai && git pull origin main && docker-compose restart && pkill -f 'python3.*8081' && cd frontend && nohup python3 -m http.server 8081 --bind 0.0.0.0 > /dev/null 2>&1 &"
```

---

## 🐛 Troubleshooting

### "ssh: connect to host pi port 22: Connection refused"
```bash
# Tailscale läuft wahrscheinlich nicht
# → Tailscale auf Laptop starten
```

### "git pull" zeigt keine Änderungen
```bash
# Prüfe ob gepusht wurde:
git log origin/main -1

# Force pull:
ssh pi "cd /home/dave/kitchenhelper-ai && git fetch origin && git reset --hard origin/main"
```

### Frontend zeigt noch alte Version (lokal)
```bash
# Browser Cache leeren:
# Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)

# Oder Python Server neu starten:
ssh pi "pkill -f 'python3.*8081' && cd /home/dave/kitchenhelper-ai/frontend && nohup python3 -m http.server 8081 --bind 0.0.0.0 > /dev/null 2>&1 &"
```

### Domain zeigt noch alte Version
```bash
# Option 1: Cloudflare Cache manuell löschen
# → https://dash.cloudflare.com → kitchenhelper-ai.de → Caching → Purge Everything

# Option 2: Warte 5-30 Minuten

# Option 3: Cloudflare Auto-Clear einrichten (siehe oben)
```

### Docker Backend funktioniert nicht
```bash
# Logs prüfen:
ssh pi "docker logs kitchenhelper-api"

# Container neu starten:
ssh pi "cd /home/dave/kitchenhelper-ai && docker-compose down && docker-compose up -d"

# Container rebuild (bei Backend-Code-Änderungen):
ssh pi "cd /home/dave/kitchenhelper-ai && docker-compose down && docker-compose up -d --build"
```

---

## 📊 Deployment Cheatsheet

| Was geändert? | Benötigt |
|---------------|----------|
| Frontend (HTML/CSS/JS) | Frontend restart ✅ |
| Backend Python Code | Docker restart ✅ |
| Backend Requirements | Docker rebuild 🔨 |
| .env Datei | Docker restart ✅ |
| docker-compose.yml | Docker down/up 🔨 |
| Alles | Deploy script 🚀 |

**Frontend restart:**
```bash
pkill -f 'python3.*8081' && cd frontend && nohup python3 -m http.server 8081 > /dev/null 2>&1 &
```

**Docker restart:**
```bash
docker-compose restart
```

**Docker rebuild:**
```bash
docker-compose down && docker-compose up -d --build
```

---

## 🎯 Empfohlener Workflow für Claude

**Wenn ich (Claude) Code commite, mache ich automatisch:**

1. ✅ Code schreiben & committen
2. ✅ `./scripts/deploy-to-pi.sh "message"` ausführen
3. ✅ Bestätigung zeigen mit URLs

**Fertig!** Keine manuellen Steps mehr nötig.

---

## 💾 Backup vor großen Changes

```bash
# Backup erstellen:
ssh pi "cd /home/dave && tar -czf kitchenhelper-backup-$(date +%Y%m%d).tar.gz kitchenhelper-ai/"

# Backup runterladen:
scp pi:/home/dave/kitchenhelper-backup-*.tar.gz ~/Desktop/
```

---

## 🚨 Rollback (falls was schiefgeht)

```bash
# Letzten Commit rückgängig (lokal):
git reset --hard HEAD~1

# Auf Pi zurücksetzen:
ssh pi "cd /home/dave/kitchenhelper-ai && git reset --hard HEAD~1"

# Services restart:
./scripts/deploy-to-pi.sh "Rollback"
```
