# 🚀 Deployment Update - 01.12.2025

**Updates für Raspberry Pi Deployment**

---

## ✨ Neue Features

### 1. **Timeout erhöht (60s → 180s)**
- Ollama bekommt mehr Zeit für Rezept-Generierung
- Verhindert Timeouts bei langsamen Modellen
- **Datei:** `backend/app/services/ai_recipe_generator.py:173,225`

### 2. **Rate Limiting implementiert**
- Max 2-3 gleichzeitige AI-Requests
- Schützt Pi vor Überlastung
- Warteschlange für weitere Requests
- **Dateien:**
  - `backend/app/middleware/rate_limit.py` (neu)
  - `backend/app/main.py:42`

### 3. **FAQ-Feature**
- 10 vorgefertigte Rezept-Kategorien
- Schneller Zugriff auf häufige Anfragen
- Bilingual (DE/EN)
- **Dateien:**
  - `backend/app/data/faq_recipes.py` (neu)
  - `backend/app/routes/faq.py` (neu)
  - `backend/app/main.py:57`

### 4. **Dokumentation**
- Modell-Wechsel-Anleitung
- .env Kommentare für Pi
- **Dateien:**
  - `docs/OLLAMA-MODEL-CHANGE.md` (neu)
  - `.env.example:32-37`

---

## 📋 Deployment auf Pi - Schritt für Schritt

### **WICHTIG: Zuerst Updates auf Pi deployen, dann .env anpassen!**

---

### 1️⃣ SSH zum Pi

```bash
ssh pi
```

---

### 2️⃣ Git Pull (Updates holen)

```bash
cd ~/kitchenhelper-ai
git pull
```

**Erwarte:**
```
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
...
Updating abc1234..def5678
Fast-forward
 backend/app/services/ai_recipe_generator.py | 4 ++--
 backend/app/middleware/rate_limit.py       | 95 ++++++++++++++++++++++++++++
 backend/app/routes/faq.py                  | 135 +++++++++++++++++++++++++++++++++++++++
 ...
```

---

### 3️⃣ .env anpassen (OLLAMA_BASE_URL Fix)

```bash
nano .env
```

**Finde Zeile:**
```
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

**Ändere zu:**
```
OLLAMA_BASE_URL=http://localhost:11434
```

**Speichern:** `Ctrl+O` → `Enter` → `Ctrl+X`

**Warum?**
- `host.docker.internal` funktioniert nicht mit `network_mode: host`
- `localhost` greift direkt auf Pi-Host Ollama zu

---

### 4️⃣ Docker neu starten

```bash
docker compose down
docker compose up -d
```

**Erwarte:**
```
[+] Running 1/1
 ⠿ Container kitchenhelper-api  Started
```

---

### 5️⃣ Logs prüfen (wichtig!)

```bash
docker compose logs -f
```

**Erwarte:**
```
kitchenhelper-api | [OK] KitchenHelper-AI v1.0.0 started!
kitchenhelper-api | INFO:app.services.ai_recipe_generator:AI Generator initialized - Gemini: False, Ollama: True
kitchenhelper-api | INFO:app.middleware.rate_limit:OllamaRateLimiter initialized (max_concurrent: 2)
```

**❌ KEIN "Ollama not available" Fehler mehr!**

`Ctrl+C` zum Beenden

---

### 6️⃣ Health Check

```bash
curl http://localhost:8000/health
```

**Erwarte:**
```json
{"status":"ok"}
```

---

### 7️⃣ FAQ-Feature testen (optional)

```bash
curl http://localhost:8000/api/faq/categories \
  -H "Authorization: Bearer <dein-token>"
```

**Erwarte:**
```json
{
  "categories": [
    {"id": "quick-dinner-veg", "title": "Quick Vegetarian Dinner", ...},
    {"id": "diabetic-breakfast", "title": "Diabetic-Friendly Breakfast", ...},
    ...
  ],
  "count": 10
}
```

---

## ✅ Deployment erfolgreich!

**Neue Features aktiv:**
- ✅ Timeout 180s (3 Min)
- ✅ Rate Limiting (max 2 concurrent)
- ✅ FAQ-Feature (10 Kategorien)
- ✅ Ollama Connection Fix

---

## 🔧 Troubleshooting

### Problem: "Ollama not available"

```bash
# 1. Prüfe Ollama Service
sudo systemctl status ollama

# 2. Falls gestoppt:
sudo systemctl start ollama

# 3. Teste manuell
curl http://localhost:11434/api/tags

# 4. Docker neu starten
docker compose restart
```

---

### Problem: Rate Limit zu restriktiv

**.env bearbeiten:**
```bash
nano backend/app/middleware/rate_limit.py

# Zeile 22 ändern:
# max_concurrent: int = 2  →  max_concurrent: int = 3
```

**Docker neu starten:**
```bash
docker compose restart
```

---

### Problem: FAQ lädt nicht

**Prüfe Route:**
```bash
docker compose logs | grep faq

# Erwarte:
# "GET /api/faq/categories"
```

**Prüfe Code:**
```bash
cat backend/app/main.py | grep faq

# Erwarte:
# from app.routes import (..., faq)
# app.include_router(faq.router, prefix="/api")
```

---

## 📊 Neue API-Endpoints

### GET `/api/faq/categories`
**Liste aller FAQ-Kategorien**

**Query Params:**
- `language`: "en" oder "de"

**Response:**
```json
{
  "categories": [...],
  "count": 10
}
```

---

### POST `/api/faq/generate/{category_id}`
**Rezept aus FAQ-Kategorie generieren**

**Path Params:**
- `category_id`: "quick-dinner-veg", "diabetic-breakfast", etc.

**Query Params:**
- `language`: "en" oder "de"

**Response:**
```json
{
  "recipes": [...],
  "count": 3,
  "daily_count_remaining": 47,
  "message": "✅ 3 Rezepte aus FAQ 'Quick Vegetarian Dinner' generiert!"
}
```

---

## 📚 Weiterführende Docs

- **Modell wechseln:** `docs/OLLAMA-MODEL-CHANGE.md`
- **Pi Deployment:** `docs/PI-DEPLOYMENT.md`
- **AI Integration:** `docs/AI-INTEGRATION.md`

---

**Deployment-Datum:** 2025-12-01
**Getestet:** ❌ Noch nicht auf Pi getestet
**Nächster Schritt:** Git Push → Pi Deployment → Testing

---

## 🎯 Next Steps (nach Deployment)

1. **Commit & Push zu GitHub** (Laptop)
2. **Pi Deployment** (wie oben beschrieben)
3. **Testing:**
   - Rezept-Generierung (Free + Pro)
   - FAQ-Feature testen
   - Rate Limiting testen (2+ concurrent requests)
   - Timeout testen (sollte nicht mehr bei 60s abbrechen)

4. **Optional:**
   - Pro Lite Tier evaluieren (Groq/Deepseek)
   - Trainingsdaten-Disclaimer platzieren
   - Frontend FAQ-UI implementieren

---

**Status:** ✅ Code bereit für Deployment
