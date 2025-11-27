# Setup: Prompts Ordnerstruktur + Templates

## 📋 KONTEXT
KitchenHelper-AI Projekt. Erstelle komplette Ordnerstruktur für token-optimierte Claude Code Prompts mit Templates und Workflow-Doku.

## 🎯 AUFGABEN

### Ordnerstruktur
- [ ] `prompts/` (Root)
- [ ] `prompts/completed/` (Archiv für fertige Prompts)
- [ ] `prompts/templates/` (Vorlagen)
- [ ] `prompts/archive/` (Alte Versionen)

### Dateien erstellen
- [ ] `prompts/README.md` (Workflow-Dokumentation)
- [ ] `prompts/templates/TEMPLATE.md` (Standard-Template)
- [ ] `prompts/current.md` (Arbeits-Datei, leer mit Kommentar)
- [ ] `prompts/.gitkeep` in completed/, archive/ (für Git)

### README Inhalt
````markdown
# Claude Code Workflow

## QUICK START
1. Backend: `cd backend && .\venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload`
2. Prompt: `code prompts/current.md` (schreiben/pasten)
3. Claude: `claude --file prompts/current.md`
4. Test: `pytest tests/`
5. Archive: `mv prompts/current.md prompts/completed/DATUM-feature.md`

## MULTI-STEP
Große Features splitten:
- `prompts/step1-backend.md`
- `prompts/step2-frontend.md`
- `prompts/step3-integration.md`

Dann nacheinander: `claude --file prompts/stepX.md`

## CHECKLIST
- [ ] Git backup
- [ ] Backend läuft
- [ ] Prompt token-optimiert
- [ ] Nach jedem Step testen

## TROUBLESHOOTING
- Claude findet Datei nicht: `pwd` prüfen (sollte KitchenHelper/ sein)
- Backend läuft nicht: `cd backend && pip install -r requirements.txt`

## STATISTICS
Track deine Token-Ersparnis in commits!
````

### TEMPLATE Inhalt
````markdown
# [Feature Name] - KitchenHelper-AI

## 📋 KONTEXT
[Status in 1-2 Zeilen. Abhängigkeiten. Ziel.]

## 🎯 AUFGABEN

### Backend
- [ ] Task 1 (Referenz: /mnt/project/existing.py)
- [ ] Task 2

### Frontend
- [ ] Task 1
- [ ] Task 2

## 📝 CODE
[Nur kritische Beispiele. Rest per Referenz.]

## 🧪 TESTING
```bash
# Test commands
```

## 📦 DATEIEN
**Erstellen:** [Liste]
**Bearbeiten:** [Liste]

---
**START:** [Erste konkrete Aufgabe]
````

### current.md Inhalt
````markdown
# Current Working Prompt

<!-- 
Nutze dieses File für deinen aktuellen Arbeits-Prompt.
Nach Completion archivieren:
mv prompts/current.md prompts/completed/YYYY-MM-DD-feature.md
-->

## Hier deinen Prompt einfügen...
````

## 📝 CODE

**Ordner erstellen (PowerShell-kompatibel):**
````python
import os
from pathlib import Path

# Base path
base = Path("/mnt/project/prompts")

# Create directories
dirs = [
    base,
    base / "completed",
    base / "templates",
    base / "archive"
]

for d in dirs:
    d.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {d}")
````

**PowerShell Alternative (falls Python nicht geht):**
````powershell
$folders = @("prompts", "prompts\completed", "prompts\templates", "prompts\archive")
foreach ($folder in $folders) {
    New-Item -Path $folder -ItemType Directory -Force
}
````

## 🧪 TESTING
````bash
# Prüfe Struktur
ls prompts/
# → Sollte zeigen: completed/, templates/, archive/, README.md, current.md

ls prompts/templates/
# → Sollte zeigen: TEMPLATE.md

# Inhalt prüfen
cat prompts/README.md
cat prompts/templates/TEMPLATE.md
cat prompts/current.md
````

## 📦 DATEIEN

**Erstellen:**
- `/mnt/project/prompts/` (Ordner)
- `/mnt/project/prompts/completed/` (Ordner)
- `/mnt/project/prompts/templates/` (Ordner)
- `/mnt/project/prompts/archive/` (Ordner)
- `/mnt/project/prompts/README.md` (vollständiger Inhalt)
- `/mnt/project/prompts/templates/TEMPLATE.md` (vollständiger Inhalt)
- `/mnt/project/prompts/current.md` (mit Platzhalter-Kommentar)
- `/mnt/project/prompts/completed/.gitkeep` (leere Datei für Git)
- `/mnt/project/prompts/archive/.gitkeep` (leere Datei für Git)

**Bearbeiten:**
- Keine

---

**START:** Erstelle Ordnerstruktur mit mkdir, dann Dateien mit vollständigem Inhalt