# Cloudflare Auto Cache Clear Setup

## Problem gelöst! 🎯

**Vorher:**
- Git pull auf Pi → Änderungen sofort auf `192.168.2.54:8081` ✅
- ABER: `kitchen.kitchenhelper-ai.de` zeigt alte Version ❌ (5-30 Min Delay)

**Nachher:**
- Git pull auf Pi → Script löscht automatisch Cloudflare Cache
- Änderungen auf BEIDEN sofort sichtbar! ✅

---

## Einrichtung (Einmalig, 5 Minuten)

### 1. Cloudflare API Token erstellen

1. Gehe zu: https://dash.cloudflare.com/profile/api-tokens
2. Klicke: **Create Token**
3. Wähle Template: **"Edit zone DNS"** oder **"Custom token"**
4. Konfiguration:
   ```
   Permissions:
   ├─ Zone → Cache Purge → Purge
   ├─ Zone → Zone → Read

   Zone Resources:
   └─ Include → Specific zone → kitchenhelper-ai.de
   ```
5. Klicke: **Continue to summary** → **Create Token**
6. **WICHTIG:** Kopiere den Token (wird nur einmal angezeigt!)

---

### 2. Zone ID finden

1. Gehe zu: https://dash.cloudflare.com
2. Klicke auf: **kitchenhelper-ai.de**
3. Scrolle runter im **Overview** Tab
4. Rechte Sidebar → **API** Section → **Zone ID**
5. Kopiere die Zone ID (z.B. `abc123def456...`)

---

### 3. Auf dem Pi einrichten

**SSH in den Pi:**
```bash
ssh pi
```

**Environment Variables setzen:**
```bash
# Option A: Permanent in ~/.bashrc (empfohlen)
echo 'export CLOUDFLARE_ZONE_ID="deine_zone_id_hier"' >> ~/.bashrc
echo 'export CLOUDFLARE_API_TOKEN="dein_token_hier"' >> ~/.bashrc
source ~/.bashrc

# Option B: Nur für aktuelle Session (zum Testen)
export CLOUDFLARE_ZONE_ID="deine_zone_id_hier"
export CLOUDFLARE_API_TOKEN="dein_token_hier"
```

**Script ausführbar machen:**
```bash
cd /home/pi/kitchenhelper-ai
chmod +x scripts/git-pull-and-clear-cache.sh
chmod +x scripts/cloudflare-cache-clear.sh
```

---

## Nutzung

### Automatisch: Git Pull + Cache Clear
```bash
cd /home/pi/kitchenhelper-ai
./scripts/git-pull-and-clear-cache.sh
```

**Was passiert:**
1. ✅ Git Pull (holt neueste Änderungen)
2. ✅ Python Cache löschen (`__pycache__`)
3. ✅ Cloudflare Cache löschen (API Call)
4. ✅ Bestätigung anzeigen

### Nur Cache löschen (ohne Git Pull)
```bash
./scripts/cloudflare-cache-clear.sh
```

---

## Alias erstellen (optional)

Für noch schnelleren Zugriff:

```bash
echo 'alias deploy="cd /home/pi/kitchenhelper-ai && ./scripts/git-pull-and-clear-cache.sh"' >> ~/.bashrc
source ~/.bashrc
```

Dann einfach nur:
```bash
deploy
```

---

## Workflow

**Von deinem PC (VS Code):**
```bash
git add .
git commit -m "Feature: XYZ"
git push origin main
```

**Auf dem Pi (SSH):**
```bash
deploy  # Oder: ./scripts/git-pull-and-clear-cache.sh
```

**Ergebnis (10-30 Sekunden später):**
- ✅ http://192.168.2.54:8081 (sofort)
- ✅ https://kitchen.kitchenhelper-ai.de (10-30s)
- ✅ https://kitchenhelper-ai.de (10-30s)

---

## Kosten

**Cloudflare Cache Purge API:**
- ✅ **100% KOSTENLOS** im Free Plan
- ✅ Unlimitierte Requests
- ✅ Keine versteckten Kosten

---

## Troubleshooting

### "CLOUDFLARE_ZONE_ID or CLOUDFLARE_API_TOKEN not set"
```bash
# Prüfe ob gesetzt:
echo $CLOUDFLARE_ZONE_ID
echo $CLOUDFLARE_API_TOKEN

# Wenn leer, erneut setzen (siehe Schritt 3)
```

### "Failed to clear cache"
1. Prüfe Token noch gültig: https://dash.cloudflare.com/profile/api-tokens
2. Prüfe Zone ID korrekt
3. Prüfe Internet-Verbindung auf Pi

### Cache trotzdem nicht gelöscht?
```bash
# Hard Refresh im Browser:
# Windows/Linux: Ctrl + Shift + R
# Mac: Cmd + Shift + R
```

---

## Was wird gecacht?

**Von Cloudflare automatisch gecacht:**
- `.html` (30 Minuten)
- `.css` (1 Stunde)
- `.js` (1 Stunde)
- Bilder (`.jpg`, `.png`, `.svg`) (2 Stunden)

**Unser Script löscht:** ALLES (purge_everything)

---

## Manuelle Alternative (ohne Script)

**Cloudflare Dashboard:**
1. https://dash.cloudflare.com
2. Klicke: **kitchenhelper-ai.de**
3. **Caching** → **Configuration**
4. **Purge Everything**
5. Bestätigen

**Aber:** Mit Script ist's schneller! 🚀
