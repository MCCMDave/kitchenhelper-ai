# Raspberry Pi Deployment - KitchenHelper-AI

Anleitung für das Deployment auf einem Raspberry Pi 5 (oder älter mit ARM64).

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Docker Installation](#docker-installation)
3. [Projekt Setup](#projekt-setup)
4. [Deployment](#deployment)
5. [Automatisierung](#automatisierung)
6. [Netzwerk & Zugriff](#netzwerk--zugriff)
7. [Wartung](#wartung)
8. [Troubleshooting](#troubleshooting)

---

## Voraussetzungen

### Hardware

- Raspberry Pi 4/5 mit 4GB+ RAM (empfohlen: 8GB)
- SD-Karte 32GB+ (empfohlen: SSD via USB)
- Aktive Kühlung (bei dauerhafter Nutzung)

### Software

- Raspberry Pi OS (64-bit) - Bookworm oder neuer
- SSH-Zugang aktiviert
- Internetverbindung

### Empfohlene Pi-Konfiguration

```bash
# System aktualisieren
sudo apt update && sudo apt upgrade -y

# Swap erweitern (für Build-Prozess)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

---

## Docker Installation

### 1. Docker Engine installieren

```bash
# Docker installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# User zur Docker-Gruppe hinzufügen
sudo usermod -aG docker $USER

# Ausloggen und wieder einloggen (wichtig!)
exit
# Neu verbinden via SSH
```

### 2. Docker Compose installieren

Docker Compose ist bei neueren Docker-Versionen bereits enthalten:

```bash
# Version prüfen
docker compose version

# Falls nicht vorhanden:
sudo apt install docker-compose-plugin
```

### 3. Docker automatisch starten

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### 4. Installation testen

```bash
docker run hello-world
```

---

## Projekt Setup

### 1. Repository klonen

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/kitchenhelper-ai.git
cd kitchenhelper-ai
```

### 2. Environment konfigurieren

```bash
# .env Datei erstellen
cp .env.example .env

# .env bearbeiten
nano .env
```

**Wichtig:** `JWT_SECRET_KEY` ändern!

```bash
# Sicheren Key generieren
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Verzeichnisse erstellen

```bash
mkdir -p backend/database logs
```

---

## Deployment

### Erstes Deployment

```bash
cd ~/kitchenhelper-ai

# Deploy-Script ausführbar machen
chmod +x deploy.sh

# Deployment starten
./deploy.sh
```

Das Script führt automatisch aus:
1. Git pull (neueste Änderungen)
2. Docker image build
3. Container starten
4. Health check

### Manuelles Deployment

```bash
# Image bauen
docker compose build

# Container starten
docker compose up -d

# Status prüfen
docker compose ps

# Logs anzeigen
docker compose logs -f
```

---

## Automatisierung

### Auto-Start nach Reboot

Docker ist bereits so konfiguriert, dass Container mit `restart: unless-stopped` automatisch starten.

### Automatische Updates (optional)

Erstelle einen Cron-Job für automatische Updates:

```bash
crontab -e
```

Füge hinzu (täglich um 3:00 Uhr):

```cron
0 3 * * * cd ~/kitchenhelper-ai && git pull && docker compose build && docker compose up -d >> ~/kitchenhelper-update.log 2>&1
```

---

## Netzwerk & Zugriff

### Lokales Netzwerk

Die API ist erreichbar unter:
- `http://<pi-ip>:8000` - API
- `http://<pi-ip>:8000/docs` - Swagger UI

Pi-IP finden:
```bash
hostname -I
```

### Feste IP-Adresse (empfohlen)

```bash
sudo nano /etc/dhcpcd.conf
```

Füge hinzu:
```
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

### Externer Zugriff (optional)

Für Zugriff von außerhalb des Netzwerks:

1. **Port Forwarding** im Router (Port 8000 → Pi-IP:8000)
2. **Oder besser:** Cloudflare Tunnel (sicherer, kein Port-Forwarding nötig)

Cloudflare Tunnel Setup kommt als separates Dokument.

---

## Wartung

### Logs prüfen

```bash
# Docker Logs
docker compose logs -f

# Letzte 100 Zeilen
docker compose logs --tail=100

# System-Logs
journalctl -u docker -f
```

### Datenbank-Backup

```bash
# Backup erstellen
cp ~/kitchenhelper-ai/backend/database/kitchenhelper.db ~/backup/kitchenhelper_$(date +%Y%m%d).db

# Automatisches Backup (Cron)
0 2 * * * cp ~/kitchenhelper-ai/backend/database/kitchenhelper.db ~/backup/kitchenhelper_$(date +\%Y\%m\%d).db
```

### Updates einspielen

```bash
cd ~/kitchenhelper-ai
./deploy.sh
```

### Container neu starten

```bash
docker compose restart
```

### Speicherplatz freigeben

```bash
# Docker aufräumen
docker system prune -a

# Alte Logs löschen
sudo journalctl --vacuum-time=7d
```

---

## Troubleshooting

### Container startet nicht

```bash
# Detaillierte Logs
docker compose logs

# Container manuell starten
docker compose up
```

### Build-Fehler auf ARM64

```bash
# Mehr Swap zuweisen (temporär)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Nach dem Build wieder entfernen
sudo swapoff /swapfile
sudo rm /swapfile
```

### Speicherprobleme

```bash
# Speicherverbrauch prüfen
docker stats

# Nicht genutzte Images entfernen
docker image prune -a
```

### Netzwerk-Probleme

```bash
# Pi-Netzwerk testen
ping google.com

# Docker-Netzwerk prüfen
docker network ls
docker network inspect bridge
```

### Permission-Fehler

```bash
# Docker-Gruppe prüfen
groups $USER

# Falls docker nicht dabei:
sudo usermod -aG docker $USER
# Dann ausloggen/einloggen
```

### Health Check schlägt fehl

```bash
# Manuell testen
curl http://localhost:8000/health

# Container-Status
docker compose ps

# In den Container schauen
docker compose exec kitchenhelper sh
```

---

## Ressourcen-Limits

Die `docker-compose.yml` enthält bereits Limits für den Pi:

```yaml
mem_limit: 512m   # Max 512MB RAM
cpus: "0.5"       # Max 50% CPU
```

Diese können bei Bedarf angepasst werden:

```yaml
# Für Pi 5 mit 8GB RAM
mem_limit: 1g
cpus: "1.0"
```

---

## Monitoring (optional)

### Einfaches Monitoring mit htop

```bash
sudo apt install htop
htop
```

### Docker Stats

```bash
# Live-Ansicht
docker stats

# Einmalig
docker stats --no-stream
```

---

## Checkliste Deployment

- [ ] Docker installiert und läuft
- [ ] Repository geklont
- [ ] `.env` Datei konfiguriert (JWT_SECRET_KEY geändert!)
- [ ] `./deploy.sh` erfolgreich ausgeführt
- [ ] Health Check funktioniert (`curl localhost:8000/health`)
- [ ] Swagger UI erreichbar (`http://<pi-ip>:8000/docs`)
- [ ] Backup-Strategie eingerichtet

---

Bei Fragen: Issue auf GitHub erstellen!
