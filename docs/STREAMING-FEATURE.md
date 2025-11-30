# 🌊 Streaming-Feature Dokumentation

## Überblick

Das Streaming-Feature ermöglicht es Benutzern, die Rezept-Generierung in Echtzeit zu sehen - ähnlich wie bei ChatGPT. Statt 35-40 Sekunden auf ein plötzlich erscheinendes Rezept zu warten, sehen sie den Text Wort für Wort erscheinen.

### Vorteile
- ✅ **3-5x bessere wahrgenommene Geschwindigkeit** (psychologischer Effekt)
- ✅ User weiß sofort: "AI arbeitet, nicht abgestürzt"
- ✅ Professioneller Eindruck wie moderne AI-Tools
- ✅ User bleibt engagiert statt frustriert zu warten

---

## 🏗️ Architektur

### Backend: Server-Sent Events (SSE)

**Neue Route:** `POST /api/recipes/generate/stream`

**Wie es funktioniert:**
1. Ollama API wird mit `stream=True` aufgerufen
2. Tokens werden live empfangen (via `requests.iter_lines()`)
3. Jedes Token wird als SSE-Event gesendet: `data: {"token": "..."}\n\n`
4. Nach Abschluss: `data: {"done": true}\n\n`

**Code-Location:**
- `backend/app/routes/recipes.py:47-126` - Streaming-Route
- `backend/app/services/ai_recipe_generator.py:193-239` - Generator mit stream=True

### Frontend: EventSource API

**Wie es funktioniert:**
1. `EventSource` verbindet sich mit `/recipes/generate/stream`
2. `onmessage` empfängt Tokens in Echtzeit
3. Text wird live in `<div id="streaming-output">` angezeigt
4. Auto-Scroll zum Bottom (wie Chat-Apps)
5. Bei `done=true`: JSON parsen und Rezept-Karten rendern

**Code-Location:**
- `frontend/js/recipes.js:50-243` - Streaming-Logik
  - `generate()` - Router (classic vs streaming)
  - `generateClassic()` - Aktuelle Methode (mit Loading-Message + Pro-Promo)
  - `generateWithStreaming()` - Neue Streaming-Methode

---

## 🎯 Aktivierung

### Aktueller Status: **Deaktiviert** (Ready to Test)

**Warum?**
- Feature ist implementiert, aber noch nicht getestet
- EventSource API hat Limitierungen (kein Custom Headers Support in allen Browsern)
- Authentication muss ggf. via URL-Parameter erfolgen statt Header

### Aktivieren (wenn bereit):

**Frontend:**
```javascript
// In frontend/js/recipes.js:64
const useStreaming = true; // Aktuell: false
```

**Backend:**
- Bereits aktiviert (Route existiert)
- Ollama muss laufen: `http://localhost:11434` (oder Pi IP)

---

## 🧪 Testing-Checkliste

### 1. Backend-Test (ohne Frontend)
```bash
# Terminal 1: Start Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Test SSE Endpoint
curl -N -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"ingredient_ids": [1,2], "ai_provider": "ai", "servings": 2}' \
  http://localhost:8000/api/recipes/generate/stream
```

**Erwartete Ausgabe:**
```
data: {"token": "["}

data: {"token": "\n"}

data: {"token": "  {"}

...
data: {"done": true}
```

### 2. Frontend-Test
1. `useStreaming = true` setzen (recipes.js:64)
2. Browser öffnen, DevTools Console offen
3. Rezept generieren
4. Beobachten:
   - Streaming-UI erscheint (Monospace-Box)
   - Text "tippt sich selbst"
   - Nach 35-40s: Rezept-Karten erscheinen

### 3. Error-Handling-Test
- Ollama offline → Fehlermeldung
- Ungültige Tokens → JSON Parse Error
- Network Timeout → EventSource reconnect

---

## ⚠️ Bekannte Limitierungen

### 1. EventSource Authentication
**Problem:** `EventSource` unterstützt keine Custom Headers (Authorization)

**Lösungen:**
- **Option A:** Token via URL-Parameter: `/generate/stream?token=<JWT>`
- **Option B:** Cookie-basierte Auth (statt Bearer Token)
- **Option C:** Temporäre Session-ID generieren

**Aktueller Code:**
```javascript
// Diese Zeile funktioniert NICHT in allen Browsern:
const eventSource = new EventSource(url, {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

**Fix benötigt:**
```javascript
const url = `${api.API_BASE_URL}/recipes/generate/stream?token=${token}`;
const eventSource = new EventSource(url); // Kein headers-Parameter
```

### 2. Nur Ollama (Free-Tier)
- Gemini API hat kein echtes Streaming (oder andere Implementierung)
- Pro-User bekommen Gemini (2-3s) → Streaming nicht nötig
- Free-User bekommen Ollama (35-40s) → Streaming sinnvoll

### 3. CORS & Nginx
Bei Produktion mit Nginx:
```nginx
# nginx.conf für SSE
location /api/recipes/generate/stream {
    proxy_pass http://backend:8000;
    proxy_buffering off;              # WICHTIG!
    proxy_set_header X-Accel-Buffering no;
    proxy_read_timeout 120s;
    chunked_transfer_encoding on;
}
```

---

## 📊 Performance-Vergleich

| Methode | Zeit | User-Wahrnehmung | Engagement |
|---------|------|------------------|------------|
| **Classic** (aktuell) | 35-40s | ❌ "Ist es abgestürzt?" | 😟 Niedrig |
| **Streaming** (neu) | 35-40s | ✅ "AI arbeitet live!" | 😊 Hoch |
| **Gemini Pro** | 2-3s | ✅ "Blitzschnell!" | 😍 Sehr hoch |

**Fazit:** Streaming macht Free-Tier **gefühlt 3-5x schneller**, obwohl Zeit gleich bleibt!

---

## 🔧 Next Steps

### Phase 1: Testing & Debugging
1. ✅ Backend implementiert
2. ✅ Frontend implementiert
3. ⏳ EventSource Auth-Fix (Token via URL)
4. ⏳ Lokales Testing (Laptop + Ollama)
5. ⏳ Error-Handling verbessern

### Phase 2: Pi Deployment
1. Ollama auf Pi installieren (bereits erledigt)
2. Backend auf Pi deployen (Docker)
3. Streaming auf Pi testen (4,3 tokens/s)
4. Nginx Config anpassen

### Phase 3: Production
1. Feature-Flag in Settings ("Beta: Streaming aktivieren")
2. A/B Testing (50% Streaming, 50% Classic)
3. User-Feedback sammeln
4. Standardmäßig aktivieren

---

## 💡 UX-Verbesserungen (Future)

### Idee 1: Syntax-Highlighting während Streaming
```javascript
// Statt monospace plain text:
outputDiv.textContent = fullText;

// Mit Markdown-Rendering (live):
outputDiv.innerHTML = marked(fullText); // marked.js library
```

### Idee 2: JSON-Preview während Streaming
```javascript
// Sobald erste { erscheint:
if (fullText.includes('{')) {
    try {
        const partial = JSON.parse(fullText + ']}'); // Close brackets
        renderPartialRecipe(partial[0]); // Live-Preview!
    } catch (e) { /* Noch nicht valide */ }
}
```

### Idee 3: Typing-Sound (optional)
```javascript
// Wie alte Schreibmaschine:
if (data.token && data.token.trim()) {
    new Audio('/sounds/typewriter.mp3').play();
}
```

---

## 📚 Weitere Resourcen

- [Server-Sent Events (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [Ollama API Docs - Streaming](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion)
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)

---

**Status:** ✅ Implementiert, 🧪 Testing ausstehend
**Erstellt:** 30.11.2025
**Autor:** Claude + David
