# 🔄 Ollama Model Wechsel-Anleitung

**Wie ändert man das Ollama-Modell auf dem Raspberry Pi?**

Diese Anleitung geht davon aus, dass **llama3.2:latest bereits läuft**.

---

## ⚡ Quick Guide (5 Minuten)

```bash
# 1. SSH zum Pi
ssh pi

# 2. Neues Modell herunterladen
ollama pull <model-name>

# 3. .env bearbeiten
cd ~/kitchenhelper-ai
nano .env

# Ändere Zeile:
# OLLAMA_MODEL=llama3.2
# zu:
# OLLAMA_MODEL=<neues-modell>

# 4. Docker neu starten
docker compose restart

# 5. Logs prüfen
docker compose logs -f
```

**Fertig!** Das neue Modell wird jetzt verwendet.

---

## 📋 Verfügbare Modelle

### Empfohlen für Pi 5 (8GB RAM)

| Modell | Größe | Speed | Qualität | Empfehlung |
|--------|-------|-------|----------|------------|
| **llama3.2:latest** (3B) | 2.0 GB | 4-5 tok/s | ⭐⭐⭐⭐ | ✅ **Standard** |
| llama3.2:1b | 1.3 GB | 7-8 tok/s | ⭐⭐ | ❌ Halluzinationen |
| gemma2:2b | 1.6 GB | 5-6 tok/s | ⭐⭐⭐ | ⚠️ Untested |
| phi3:mini | 2.3 GB | 3-4 tok/s | ⭐⭐⭐ | ⚠️ Untested |

### Für leistungsstärkere Hardware

| Modell | Größe | Speed | Qualität | Hardware |
|--------|-------|-------|----------|----------|
| llama3.1:8b | 4.7 GB | 2-3 tok/s | ⭐⭐⭐⭐⭐ | Desktop/Server |
| mistral:7b | 4.1 GB | 2-3 tok/s | ⭐⭐⭐⭐ | Desktop/Server |

---

## 🔍 Modell-Liste anzeigen

```bash
# Installierte Modelle
ollama list

# Verfügbare Modelle (online)
ollama search llama
ollama search gemma
ollama search phi3
```

---

## 🧪 Modell testen (bevor du wechselst)

```bash
# Modell herunterladen
ollama pull gemma2:2b

# Interaktiv testen
ollama run gemma2:2b

# Rezept-Prompt testen
ollama run gemma2:2b "Generate a simple recipe with tomatoes, pasta, and garlic. Return JSON format."
```

**Wenn das Ergebnis gut aussieht:** Wechsel in der `.env` durchführen.

---

## 📝 Schritt-für-Schritt Anleitung

### 1️⃣ Neues Modell herunterladen

```bash
ssh pi
ollama pull <model-name>

# Beispiel: Gemma 2B
ollama pull gemma2:2b
```

**Download-Zeit:** 1-5 Minuten (je nach Modellgröße)

---

### 2️⃣ .env Datei bearbeiten

```bash
cd ~/kitchenhelper-ai
nano .env
```

**Finde Zeile:**
```
OLLAMA_MODEL=llama3.2
```

**Ändere zu:**
```
OLLAMA_MODEL=gemma2:2b
```

**Speichern:** `Ctrl+O` → `Enter` → `Ctrl+X`

---

### 3️⃣ Docker neu starten

```bash
docker compose restart
```

**Oder vollständiger Neustart:**
```bash
docker compose down
docker compose up -d
```

---

### 4️⃣ Überprüfen

```bash
# Logs ansehen (Ctrl+C zum Beenden)
docker compose logs -f

# Erwarte:
# "Ollama available: True"
# "Ollama model: gemma2:2b"
```

**API testen:**
```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

---

## 🗑️ Altes Modell löschen (Platz sparen)

```bash
# Liste installierte Modelle
ollama list

# Lösche ungenutztes Modell
ollama rm llama3.2:1b

# Bestätigung:
# "deleted 'llama3.2:1b'"
```

**Disk-Space frei:** ~1-2 GB pro gelöschtes Modell

---

## ⚠️ Troubleshooting

### Problem: "Model not found"

```bash
# Prüfe ob Modell existiert
ollama list

# Falls nicht: Herunterladen
ollama pull <model-name>
```

---

### Problem: Container startet nicht

```bash
# Logs prüfen
docker compose logs

# Häufige Fehler:
# - "Out of memory" → Kleineres Modell wählen
# - "Connection refused" → Ollama-Service prüfen

# Ollama Service Status
sudo systemctl status ollama
```

---

### Problem: Schlechte Rezept-Qualität

**Mögliche Ursachen:**
- Modell zu klein (< 3B Parameter)
- Temperatur zu hoch
- Prompt nicht optimal

**Lösung:**
- Zurück zu `llama3.2:latest` (bewährt)
- Größeres Modell testen (Desktop-Hardware)

---

## 🎯 Empfohlene Modelle nach Use-Case

### Free-Tier (Pi 5)
- **llama3.2:latest** ← Beste Balance Quality/Speed

### Pro-Tier (Cloud)
- **Gemini 2.0 Flash** (API) ← 10x schneller

### Testing/Development
- **llama3.2:1b** ← Nur für Speed-Tests, NICHT Production!

---

## 📊 Performance-Vergleich

| Modell | Rezept-Zeit | Qualität | RAM |
|--------|-------------|----------|-----|
| llama3.2:1b | ~18s | ❌ Schlecht | 1.5 GB |
| llama3.2:latest | ~35s | ✅ Gut | 2.5 GB |
| llama3.1:8b | ~60s | ⭐ Sehr gut | 5.5 GB |
| Gemini Flash | ~3s | ⭐⭐ Exzellent | Cloud |

---

## 🔄 Zurück zu Standard-Modell

```bash
cd ~/kitchenhelper-ai
nano .env

# Ändere zu:
OLLAMA_MODEL=llama3.2

docker compose restart
```

---

## 📚 Weitere Ressourcen

- **Ollama Library:** https://ollama.com/library
- **Model Cards:** Details zu jedem Modell (Parameter, Training, etc.)
- **Pi Deployment Guide:** `docs/PI-DEPLOYMENT.md`

---

**Letzte Aktualisierung:** 2025-12-01
**Getestet mit:** Raspberry Pi 5 (8GB), Ollama 0.x, llama3.2:latest
