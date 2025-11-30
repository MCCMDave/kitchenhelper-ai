# Cloudflare Tunnel Setup für KitchenHelper-AI

## Übersicht
Mit Cloudflare Tunnel (früher Argo Tunnel) kannst du KitchenHelper-AI **öffentlich erreichbar** machen - **ohne Port-Forwarding** im Router und mit **automatischem HTTPS**.

**Vorteile:**
- ✅ Kostenlos
- ✅ HTTPS automatisch (SSL-Zertifikat von Cloudflare)
- ✅ Kein Port-Forwarding nötig
- ✅ Öffentlich erreichbar für Beta-Tester
- ✅ DDoS-Schutz durch Cloudflare

**Voraussetzungen:**
- Cloudflare-Account (kostenlos)
- Domain bei Cloudflare registriert/verwaltet (z.B. meluciolabs.de)
- Raspberry Pi mit laufendem KitchenHelper-AI Backend

---

## Schritt 1: Domain zu Cloudflare hinzufügen

Falls du noch keine Domain bei Cloudflare hast:

1. Gehe zu https://dash.cloudflare.com
2. "Add a Site" → Domain eingeben (z.B. `meluciolabs.de`)
3. Free Plan wählen
4. Nameserver bei deinem Domain-Anbieter (Porkbun/Namecheap) auf Cloudflare umstellen:
   - Cloudflare zeigt dir zwei Nameserver (z.B. `fiona.ns.cloudflare.com`)
   - Bei Porkbun/Namecheap: Domain → DNS Settings → Nameserver ändern
5. Warten bis DNS propagiert (5 Min - 24h, meist <1h)

---

## Schritt 2: Cloudflared auf Pi installieren

```bash
# SSH zum Pi
ssh pi

# Cloudflared für ARM64 herunterladen
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -o cloudflared

# Ausführbar machen
chmod +x cloudflared

# Nach /usr/local/bin verschieben
sudo mv cloudflared /usr/local/bin/

# Version prüfen
cloudflared --version
# Output: cloudflared version 2024.x.x
```

---

## Schritt 3: Tunnel erstellen

```bash
# Login in Cloudflare (öffnet Browser-Tab)
cloudflared tunnel login
# → Browser öffnet sich, Cloudflare autorisieren
# → Credentials werden gespeichert in ~/.cloudflared/cert.pem
```

**Wichtig:** Falls SSH ohne GUI:
```bash
# Alternative: Login-URL manuell öffnen
cloudflared tunnel login
# Kopiere die angezeigte URL und öffne sie auf deinem Laptop
# Nach Login: cert.pem wird auf dem Pi gespeichert
```

```bash
# Tunnel erstellen (Name: kitchen)
cloudflared tunnel create kitchen

# Output:
# Created tunnel kitchen with id: abc123-xyz-...
# Credentials written to: /home/dave/.cloudflared/abc123-xyz-....json
```

**Merke dir die Tunnel-ID!** (z.B. `abc123-xyz-456`)

---

## Schritt 4: DNS-Route konfigurieren

```bash
# Subdomain mit Tunnel verknüpfen
cloudflared tunnel route dns kitchen kitchen.meluciolabs.de

# Output:
# Successfully created route for kitchen.meluciolabs.de
```

**Erklärung:**
- `kitchen` = Tunnel-Name (aus Schritt 3)
- `kitchen.meluciolabs.de` = Subdomain, unter der die App erreichbar sein soll

Du kannst auch eine andere Subdomain wählen:
```bash
cloudflared tunnel route dns kitchen app.meluciolabs.de
# Oder:
cloudflared tunnel route dns kitchen demo.studiodelmelucio.de
```

---

## Schritt 5: Tunnel-Config erstellen

```bash
# Config-Ordner erstellen (falls nicht vorhanden)
mkdir -p ~/.cloudflared

# Config-Datei erstellen
nano ~/.cloudflared/config.yml
```

**Inhalt von config.yml:**
```yaml
tunnel: abc123-xyz-456  # DEINE Tunnel-ID (aus Schritt 3)
credentials-file: /home/dave/.cloudflared/abc123-xyz-456.json  # DEIN Pfad

ingress:
  # KitchenHelper-AI Backend (Port 8000)
  - hostname: kitchen.meluciolabs.de  # Deine Subdomain
    service: http://localhost:8000
    originRequest:
      noTLSVerify: true  # Für lokales HTTP

  # Catch-all Rule (erforderlich!)
  - service: http_status:404
```

**Speichern:** `Ctrl+O` → `Enter` → `Ctrl+X`

---

## Schritt 6: Tunnel starten

### Manuell (zum Testen)
```bash
cloudflared tunnel run kitchen

# Output:
# 2024-XX-XX... INF Connection registered connIndex=0
# 2024-XX-XX... INF Route propagating to kitchen.meluciolabs.de
```

**Test im Browser:**
- Öffne `https://kitchen.meluciolabs.de`
- → Du solltest das KitchenHelper-AI Frontend sehen!

**WICHTIG:** Frontend muss auf **Cloudflare-Domain** hosten (siehe Schritt 7)

### Dauerhaft (als Systemd Service)

```bash
# Tunnel als Service installieren
sudo cloudflared service install

# Service starten
sudo systemctl start cloudflared

# Auto-Start beim Booten aktivieren
sudo systemctl enable cloudflared

# Status prüfen
sudo systemctl status cloudflared
```

**Service-Befehle:**
```bash
sudo systemctl stop cloudflared      # Stoppen
sudo systemctl restart cloudflared   # Neustarten
sudo systemctl status cloudflared    # Status prüfen
journalctl -u cloudflared -f         # Logs live anzeigen
```

---

## Schritt 7: Frontend für Cloudflare-Domain konfigurieren

Die `config.js` erkennt bereits Cloudflare-Domains automatisch:

```javascript
// frontend/js/config.js (bereits implementiert!)
API_BASE_URL: (() => {
    const hostname = window.location.hostname;

    if (hostname.includes('cloudflare') || hostname.includes('.de')) {
        // Cloudflare Tunnel oder custom domain
        return `${window.location.protocol}//${window.location.host}/api`;
    }
    // ... andere Fälle
})(),
```

**Frontend hosten:**

**Option A: GitHub Pages (Empfohlen)**
```bash
# Auf Laptop
cd kitchenhelper-ai
git checkout -b gh-pages
git push origin gh-pages

# In GitHub:
# Settings → Pages → Source: gh-pages branch → /frontend folder
# Custom Domain: kitchen.meluciolabs.de
```

**Option B: Frontend auch über Tunnel**
```yaml
# ~/.cloudflared/config.yml erweitern:
ingress:
  # Frontend (statische Files via Python HTTP Server)
  - hostname: kitchen.meluciolabs.de
    path: /*
    service: http://localhost:8080  # Frontend Server

  # Backend API
  - hostname: kitchen.meluciolabs.de
    path: /api/*
    service: http://localhost:8000

  - service: http_status:404
```

Frontend-Server starten:
```bash
cd ~/kitchenhelper-ai/frontend
python3 -m http.server 8080
```

---

## Troubleshooting

### Problem: "Unable to reach the origin service"
**Lösung:** Backend läuft nicht auf Port 8000
```bash
# Prüfen:
curl http://localhost:8000/api/health
docker compose ps  # Läuft der Container?
```

### Problem: "DNS route not found"
**Lösung:** DNS-Route fehlt oder falsch
```bash
# Routen auflisten:
cloudflared tunnel route dns kitchen

# Neue Route erstellen:
cloudflared tunnel route dns kitchen kitchen.meluciolabs.de
```

### Problem: Tunnel startet nicht nach Reboot
**Lösung:** Service nicht aktiviert
```bash
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

### Problem: CORS-Fehler im Browser
**Lösung:** Backend ALLOWED_ORIGINS erweitern
```bash
# backend/.env
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,https://kitchen.meluciolabs.de
```

---

## Sicherheit

### Rate Limiting (empfohlen)
```yaml
# ~/.cloudflared/config.yml
ingress:
  - hostname: kitchen.meluciolabs.de
    service: http://localhost:8000
    originRequest:
      connectTimeout: 30s
      noTLSVerify: true
```

### Cloudflare Firewall Rules (optional)
1. Cloudflare Dashboard → Firewall → Firewall Rules
2. "Create a Firewall Rule"
3. Beispiel: Rate Limit 100 Requests/Minute pro IP

### Basic Auth (optional)
```yaml
# ~/.cloudflared/config.yml - für geschlossene Beta
ingress:
  - hostname: kitchen.meluciolabs.de
    service: http://localhost:8000
    originRequest:
      httpHostHeader: kitchen.meluciolabs.de
      access:
        required: true
        teamName: dein-team  # Cloudflare Access einrichten
```

---

## Kosten

| Feature | Preis |
|---------|-------|
| Cloudflare Tunnel | Kostenlos ✅ |
| Domain (Porkbun) | ~6€/Jahr |
| HTTPS/SSL | Kostenlos (automatisch) |
| DDoS-Schutz | Kostenlos (im Free Plan) |
| Bandwidth | Unbegrenzt ✅ |

---

## Zusammenfassung

Nach Setup ist deine App erreichbar unter:
- **Öffentlich:** `https://kitchen.meluciolabs.de` (via Cloudflare Tunnel)
- **Lokal:** `http://192.168.2.54:8000` (im Heimnetzwerk)
- **VPN:** `http://100.103.86.47:8000` (via Tailscale)

**Empfehlung:**
- **Entwicklung:** Lokal/Tailscale
- **Beta-Tester:** Cloudflare Tunnel
- **Produktion:** Cloudflare Tunnel + Rate Limiting + Monitoring

---

## Nächste Schritte

1. [ ] Cloudflare-Account erstellen
2. [ ] Domain zu Cloudflare hinzufügen
3. [ ] Cloudflared auf Pi installieren
4. [ ] Tunnel erstellen und starten
5. [ ] Frontend auf GitHub Pages deployen (optional)
6. [ ] Backend ALLOWED_ORIGINS erweitern
7. [ ] Beta-Testern Link geben: `https://kitchen.meluciolabs.de`
