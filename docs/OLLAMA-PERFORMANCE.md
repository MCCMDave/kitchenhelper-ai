# Ollama Performance Testing auf Raspberry Pi 5

## Übersicht
Dieses Dokument beschreibt wie du die Performance-Limits von Ollama auf dem Pi testen kannst.

## Test-Script ausführen

### Auf dem Pi (via SSH)
```bash
ssh pi
cd ~/kitchenhelper-ai/backend

# Aktiviere venv (falls nicht Docker)
source ../venv/bin/activate  # Oder: poetry shell

# Test 1: Einzelner Request (Baseline)
python test_ollama_load.py --concurrent 1

# Test 2: 3 parallele Requests
python test_ollama_load.py --concurrent 3

# Test 3: 5 parallele Requests
python test_ollama_load.py --concurrent 5

# Test 4: 10 parallele Requests (Stresstest)
python test_ollama_load.py --concurrent 10
```

### Vom Laptop (Remote)
```powershell
# Via Tailscale
$env:OLLAMA_URL = "http://100.103.86.47:11434"
python test_ollama_load.py --concurrent 3
```

## Was wird getestet?

Das Script sendet **gleichzeitige Requests** an Ollama und misst:
- ✅ **Success Rate**: Wie viele Requests erfolgreich waren
- ⏱️ **Response Times**: Min/Max/Average/Median Antwortzeiten
- 📊 **Performance-Degradation**: Werden Antworten langsamer bei mehr Last?
- ❌ **Failure Point**: Ab wie vielen Requests scheitern Anfragen?

## Erwartete Ergebnisse

### Raspberry Pi 5 (8GB RAM)
- **1-2 Requests**: Sollte problemlos funktionieren (~30-40s pro Request)
- **3-5 Requests**: Wahrscheinlich noch ok, aber Antworten werden länger (60-90s)
- **5-10 Requests**: Pi könnte an Limits kommen, einzelne Requests könnten timeout
- **>10 Requests**: Sehr wahrscheinlich Failures/Timeouts

### Was passiert bei Überlastung?
- **Keine Crashes**: Ollama/Pi crashen nicht, sondern...
- **Längere Antwortzeiten**: Requests dauern einfach 2-3x länger
- **Timeouts**: Nach 120s bricht das Script ab (kann erhöht werden)
- **Context Switch Overhead**: CPU wechselt zwischen Requests → alle werden langsamer

## Performance-Tuning

### Ollama Memory Limit
```bash
# Standard: Ollama nutzt soviel RAM wie verfügbar
# Limit setzen (z.B. 4GB für Ollama):
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=2  # Max 2 parallele Requests

# Ollama neu starten
sudo systemctl restart ollama
```

### Model-Optimierung
```bash
# Kleineres Modell = schneller, mehr Durchsatz
ollama pull llama3.2:1b  # 1 Billion Parameter (statt 3B)

# Im Code MODEL = "llama3.2:1b" setzen und erneut testen
```

## Produktions-Empfehlung

Basierend auf Test-Ergebnissen:

| Concurrent Users | Strategie |
|------------------|-----------|
| 1-2 Users        | ✅ Direkt auf Pi, kein Problem |
| 3-5 Users        | ⚠️ Rate Limiting einbauen (max 2-3 gleichzeitige Requests) |
| 5-10 Users       | ❌ Pi wird zu langsam → Cloud API nutzen (OpenAI/Anthropic) |
| >10 Users        | ❌ Dedicated GPU-Server oder Cloud-only |

## Rate Limiting im Backend

Falls Tests zeigen dass >3 Requests problematisch sind:

```python
# backend/app/routes/recipes.py
from fastapi import HTTPException
import asyncio

# Global semaphore (max 2 gleichzeitige AI-Requests)
ai_semaphore = asyncio.Semaphore(2)

@router.post("/generate")
async def generate_recipes(...):
    if not await ai_semaphore.acquire(blocking=False):
        raise HTTPException(
            status_code=429,
            detail="Server busy. Please try again in 30s."
        )
    try:
        # ... existing generation code ...
    finally:
        ai_semaphore.release()
```

## Next Steps

1. **Run Tests**: Führe Script mit 1, 3, 5, 10 concurrent requests aus
2. **Document Results**: Schreibe Ergebnisse hier rein (siehe Template unten)
3. **Decide Strategy**: Rate Limiting? Kleineres Modell? Cloud Fallback?

---

## Test Results (Template)

**Date:** [YYYY-MM-DD]
**Pi Model:** Raspberry Pi 5 8GB
**Ollama Model:** llama3.2
**Ollama Version:** [ollama version]

| Concurrent Requests | Success Rate | Avg Time | Max Time | Notes |
|---------------------|--------------|----------|----------|-------|
| 1                   | 100%         | 35s      | 35s      | Baseline |
| 3                   | ?%           | ?s       | ?s       | - |
| 5                   | ?%           | ?s       | ?s       | - |
| 10                  | ?%           | ?s       | ?s       | - |

**Conclusion:**
[Schreibe hier Fazit nach Tests]
