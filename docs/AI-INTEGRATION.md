# 🤖 AI Integration - Gemini & Ollama

## Übersicht

KitchenHelper-AI verwendet ein **tier-basiertes AI-System** für die Rezeptgenerierung:

- **Free Tier:** Ollama (lokal, kostenlos, datenschutzfreundlich)
- **Pro Tier:** Gemini Flash (schnell, Cloud) mit automatischem Ollama-Fallback

## Architektur

```
User Request
    ↓
Recipe Generator Route (/recipes/generate)
    ↓
AI Provider Selection (based on user tier)
    ↓
┌─────────────────────────────────────┐
│ Free Tier: → Ollama (lokal)         │
│ Pro Tier:  → Gemini + Ollama backup │
└─────────────────────────────────────┘
    ↓
Recipe JSON Response
```

## Performance

| Tier | Provider | Generierungszeit | Kosten | Datenschutz |
|------|----------|------------------|--------|-------------|
| Free | Ollama (llama3.2:3B) | ~35-40s | 0€ | ✅ Lokal |
| Pro  | Gemini Flash | ~2-3s | ~0.001€/Rezept | ⚠️ Cloud |
| Pro  | Ollama (Fallback) | ~35-40s | 0€ | ✅ Lokal |

**User-Wahrnehmung:** 10-15x Geschwindigkeitsunterschied macht Premium sehr attraktiv!

**Gemessene Performance (Pi 5, 8GB RAM, CPU-only):**
- **llama3.2:latest (3B):** 4,3 tokens/s, Q4_K_M Quantisierung
  - Rezeptgenerierung: ~35-40s für mittleres Rezept
  - Qualität: Gut, wenige Fehler
- **llama3.2:1b:** 7,8 tokens/s (1,8x schneller)
  - Rezeptgenerierung: ~18-20s
  - Qualität: ❌ **Unbrauchbar** (Halluzinationen, falsche Zutaten)

**Empfehlung:** llama3.2:latest (3B) nutzen - Qualität >> Geschwindigkeit

## Setup

### 1. Ollama (für Free & Pro Fallback)

**Installation auf Raspberry Pi:**
```bash
# Ollama installieren
curl -fsSL https://ollama.ai/install.sh | sh

# Modell herunterladen
ollama pull llama3.2

# Server starten (läuft automatisch als Service)
sudo systemctl start ollama
```

**Testen:**
```bash
curl http://localhost:11434/api/tags
```

### 2. Gemini API (optional, nur für Pro-Features)

**API Key besorgen:**
1. Gehe zu [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Erstelle einen neuen API Key
3. Füge ihn zur `.env` hinzu:

```env
GOOGLE_AI_API_KEY=dein-api-key-hier
```

**Kosten (Stand: 2025):**
- Gemini 2.0 Flash: **KOSTENLOS** bis 15 requests/minute
- Bei mehr: $0.00075 per 1K characters (~0.001€ pro Rezept)

## Konfiguration

**Backend `.env`:**
```env
# Gemini (Pro users)
GOOGLE_AI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

# Ollama (Free users + Pro fallback)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**Modell-Optionen:**

| Provider | Modell | Empfehlung |
|----------|--------|------------|
| Gemini | `gemini-2.0-flash-exp` | ✅ Schnell, kostenlos |
| Gemini | `gemini-1.5-flash` | Stabil, leicht teurer |
| Ollama | `llama3.2` | ✅ Gut, schnell (3B params) |
| Ollama | `gemma2` | Alternative, kleiner |

## API Usage

**Frontend Request:**
```javascript
const response = await fetch('/api/recipes/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    ingredient_ids: [1, 2, 3],
    ai_provider: "ai",  // "mock" oder "ai"
    servings: 2,
    language: "de"
  })
});
```

**Backend Logic:**
```python
# Free User → Ollama
if user_tier == "free":
    recipes = ollama.generate(...)

# Pro User → Gemini mit Fallback
if user_tier == "pro":
    try:
        recipes = gemini.generate(...)
    except:
        recipes = ollama.generate(...)  # Fallback
```

## Monitoring & Logging

**Backend Logs zeigen AI Provider:**
```
INFO: AI Generator initialized - Gemini: True, Ollama: True
INFO: Pro user - Using Gemini API
INFO: Free user - Using Ollama
ERROR: Gemini failed: API timeout - Falling back to Ollama
```

**Recipe Response enthält Provider-Info:**
```json
{
  "recipes": [
    {
      "name": "Pasta Carbonara",
      "ai_provider": "gemini",  // oder "ollama" oder "mock"
      ...
    }
  ]
}
```

## Fehlerbehandlung

**Szenarien:**

| Fall | Pro User | Free User |
|------|----------|-----------|
| Ollama down | ❌ Error (Gemini + Fallback fail) | ❌ Error |
| Gemini down | ✅ Fallback zu Ollama | N/A |
| Beide down | ❌ Error | ❌ Error |
| Mock | ✅ Immer verfügbar | ✅ Immer verfügbar |

**User Feedback:**
```javascript
// Bei Fehler: Fallback zu Mock vorschlagen
if (error.status === 503) {
  alert("AI-Generierung nicht verfügbar. Template-basierte Rezepte werden verwendet.");
  // Retry mit ai_provider="mock"
}
```

## Upgrade-Path

**Free → Pro Marketing:**
- "🚀 3x schnellere Rezept-Generierung mit Pro!"
- "⚡ Upgrade für sofortige Ergebnisse (2-3s statt 10s)"
- "Premium AI-Modelle mit besserer Kreativität"

## Sicherheit

**Wichtig:**
- ✅ API Keys **niemals** im Frontend!
- ✅ API Keys nur in `.env` (nicht in Git!)
- ✅ Rate Limiting auf Backend-Seite
- ✅ User Tier aus JWT Token (nicht aus Request-Body)

**Rate Limiting:**
```python
# Gemini Free Tier Limit: 15 req/min
# → Max 15 Pro-User gleichzeitig
# → Bei mehr: 429 Error → Ollama Fallback
```

## Zukunft

**Mögliche Erweiterungen:**
- [ ] Streaming Responses (Server-Sent Events)
- [ ] Custom Prompt Templates (User-definiert)
- [ ] Recipe Variations ("Mach es veganer")
- [ ] Multi-Language AI (Prompt-Optimization per Sprache)
- [ ] Image Generation (Rezeptfotos via DALL-E/Stable Diffusion)

---

**Implementiert:** 30.11.2025
**Status:** ✅ Production-Ready (Ollama required, Gemini optional)
