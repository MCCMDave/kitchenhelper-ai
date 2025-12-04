# Kitchen Root-Domain Setup

## Ziel: kitchenhelper-ai.de statt kitchen.kitchenhelper-ai.de

**Aktuell:**
- Frontend: `kitchen.kitchenhelper-ai.de`
- Backend API: `api.kitchenhelper-ai.de`
- Root-Domain (`kitchenhelper-ai.de`): Error 522 (nicht konfiguriert)

**Gewünscht:**
- Frontend: `kitchenhelper-ai.de` (Root-Domain)
- Backend API: `api.kitchenhelper-ai.de` (bleibt)
- Redirect: `kitchen.kitchenhelper-ai.de` → `kitchenhelper-ai.de` (optional)

---

## Was du tun musst (Cloudflare)

### 1. Cloudflare Tunnel - Root-Domain hinzufügen

**A. Im Cloudflare Dashboard:**
1. Gehe zu: **Zero Trust** → **Access** → **Tunnels**
2. Wähle deinen Tunnel (z.B. "kitchen-tunnel")
3. Klicke auf **Configure**
4. Unter **Public Hostnames** → **Add a public hostname**

**B. Root-Domain konfigurieren:**
```
Subdomain: (leer lassen für Root)
Domain: kitchenhelper-ai.de
Type: HTTP
URL: localhost:8081  (oder deine Pi Frontend-Port)
```

**C. Speichern** → Root-Domain sollte jetzt funktionieren

---

### 2. (Optional) Redirect kitchen.* → Root

**Im Cloudflare Dashboard (DNS):**
1. **Rules** → **Page Rules** oder **Redirect Rules**
2. Neue Rule erstellen:
   ```
   Wenn: kitchen.kitchenhelper-ai.de/*
   Dann: Redirect zu https://kitchenhelper-ai.de/$1 (301 Permanent)
   ```

---

## Was ich gemacht habe (Code)

### Frontend Config aktualisiert

**Datei:** `frontend/config.js`

```javascript
// Erkennt automatisch:
// - Root-Domain (kitchenhelper-ai.de)
// - Subdomain (kitchen.kitchenhelper-ai.de)
// - Localhost (192.168.2.54:8081, 127.0.0.1:8081)

const API_URL = window.location.hostname === 'kitchenhelper-ai.de' ||
                window.location.hostname === 'kitchen.kitchenhelper-ai.de'
    ? 'https://api.kitchenhelper-ai.de'
    : 'http://192.168.2.54:8000';
```

**Funktioniert jetzt für:**
- ✅ `kitchenhelper-ai.de` → `https://api.kitchenhelper-ai.de`
- ✅ `kitchen.kitchenhelper-ai.de` → `https://api.kitchenhelper-ai.de`
- ✅ `192.168.2.54:8081` → `http://192.168.2.54:8000` (lokal)

---

## Testing nach Setup

**1. DNS Propagation prüfen:**
```bash
nslookup kitchenhelper-ai.de
# Sollte auf Cloudflare IP zeigen
```

**2. Browser testen:**
- `https://kitchenhelper-ai.de` → Sollte Login-Seite zeigen
- `https://kitchenhelper-ai.de/dashboard.html` → Sollte Dashboard zeigen
- API-Calls sollten funktionieren

**3. Falls Probleme:**
- Cloudflare Cache leeren: **Caching** → **Purge Everything**
- Browser Cache leeren (Strg+Shift+R)
- DNS Cache leeren: `ipconfig /flushdns` (Windows)

---

## Vorteile Root-Domain

✅ **Kürzer & Professioneller:** `kitchenhelper-ai.de` statt `kitchen.kitchenhelper-ai.de`
✅ **SEO:** Besser für Suchmaschinen
✅ **Branding:** Leichter zu merken
✅ **Flexibilität:** Subdomains für andere Services frei

---

## Technische Details

**Cloudflare Tunnel Flow:**
```
User → kitchenhelper-ai.de
  ↓
Cloudflare Edge (SSL/TLS)
  ↓
Cloudflare Tunnel (verschlüsselt)
  ↓
Pi Raspberry (localhost:8081)
  ↓
Frontend Files (index.html, dashboard.html, etc.)
```

**API Routing (bleibt gleich):**
```
Frontend → api.kitchenhelper-ai.de
  ↓
Cloudflare Edge
  ↓
Cloudflare Tunnel
  ↓
Pi Raspberry (localhost:8000)
  ↓
FastAPI Backend
```

---

## Rollback (falls Probleme)

**Falls Root-Domain nicht funktioniert:**
1. Cloudflare Tunnel: Public Hostname für Root löschen
2. Frontend funktioniert weiter auf `kitchen.kitchenhelper-ai.de`
3. Kein Code-Rollback nötig (Auto-Detection!)

---

## Status

- ✅ Code vorbereitet (funktioniert für beide Domains)
- ⏳ Cloudflare Setup: **Wartet auf dich!**
- ⏳ Testing: Nach Cloudflare Setup

**Next Steps:**
1. Cloudflare Tunnel konfigurieren (siehe oben)
2. Mir Bescheid geben wenn fertig
3. Ich teste dann Root-Domain

**Fragen? Schreib mir!**
