# 🌍 KitchenHelper-AI: Automatisches Übersetzungssystem

## Was macht das Script?

Das `i18n-auto-translate.py` Script **vervollständigt automatisch** alle fehlenden Übersetzungen in der `frontend/js/i18n.js` mit Hilfe von **Ollama (llama3.2)**.

### Features

✅ **Vollautomatisch** - Übersetzt alle 8 Sprachen ohne manuelle Arbeit
✅ **Kostenlos** - Nutzt lokales Ollama (kein API-Key nötig)
✅ **Smart** - Übersetzt nur fehlende Keys, vorhandene bleiben unverändert
✅ **Zukunftssicher** - Einfach nochmal ausführen wenn neue Keys hinzukommen
✅ **Context-Aware** - Berücksichtigt den Kontext (Auth, Recipes, Errors, etc.)

---

## 🚀 Verwendung

### 1. Voraussetzungen

**Ollama muss laufen:**
```bash
ollama serve
```

**llama3.2 muss installiert sein:**
```bash
ollama pull llama3.2
```

**Python-Paket installieren:**
```bash
pip install ollama
```

### 2. Script ausführen

```bash
cd kitchenhelper-ai
python scripts/i18n-auto-translate.py
```

### 3. Das passiert dann

```
======================================================================
KitchenHelper-AI: Automatic i18n Translation System
======================================================================

i18n.js: C:\...\kitchenhelper-ai\frontend\js\i18n.js

Pruefe Ollama...
   OK: Ollama laeuft!
   OK: llama3.2 verfuegbar!

Starte Uebersetzung fuer 8 Sprachen...

======================================================================
FRENCH (FR)
======================================================================

Status:
   EN Keys: 255
   FR Keys: 49
   FEHLEN: 206 Keys

Starte Ollama-Uebersetzung (206 Keys)...

   [  1/206] auth.username_hint                      OK
   [  2/206] auth.password_repeat                    OK
   [  3/206] auth.demo_hint                          OK
   ...
   [206/206] settings.delete_account                 OK

OK: FR vollstaendig: 255/255 Keys

GESPEICHERT: FR in i18n.js aktualisiert!

[... das gleiche für ES, IT, PT, SV, NO, DA, NL ...]

======================================================================
FERTIG! Alle Sprachen vervollstaendigt!
======================================================================
```

---

## 📊 Aktueller Status

### Vor dem Script:
```
DE: 255 Keys ✅
EN: 255 Keys ✅
FR:  49 Keys ❌ (206 fehlen)
ES:  49 Keys ❌ (206 fehlen)
IT:  49 Keys ❌ (206 fehlen)
PT:  49 Keys ❌ (206 fehlen)
SV:  49 Keys ❌ (206 fehlen)
NO:  49 Keys ❌ (206 fehlen)
DA:  49 Keys ❌ (206 fehlen)
NL:  49 Keys ❌ (206 fehlen)
```

### Nach dem Script:
```
Alle 10 Sprachen: 255/255 Keys ✅
```

---

## 🔄 Neue Keys hinzufügen

Wenn du in Zukunft **neue Keys** zur `i18n.js` hinzufügst:

1. Füge sie in **DE** und **EN** manuell hinzu
2. Führe das Script nochmal aus:
   ```bash
   python scripts/i18n-auto-translate.py
   ```
3. **Fertig!** Alle anderen Sprachen werden automatisch ergänzt

---

## ⚙️ Wie funktioniert es?

### 1. Parsing
- Liest die `i18n.js` und extrahiert alle Übersetzungen
- Vergleicht jede Sprache mit EN (Referenz)
- Identifiziert fehlende Keys

### 2. Übersetzung (Ollama)
- Für jeden fehlenden Key:
  - Sendet EN-Text + Kontext an llama3.2
  - Bekommt professionelle Übersetzung zurück
  - Berücksichtigt UI-Kontext (Auth, Recipes, Errors, etc.)

### 3. Update
- Erstellt neue Sprach-Sektion mit allen Keys
- Ersetzt alte Sektion in `i18n.js`
- Erhält Code-Formatierung (Kommentare, Kategorien)

---

## 🎯 Qualität der Übersetzungen

**llama3.2** ist ein hochwertiges LLM mit guten Übersetzungsfähigkeiten:
- ✅ Grammatik & Syntax korrekt
- ✅ Kontext-bewusst (Koch-App Terminologie)
- ✅ Behält Platzhalter ({count}, {name})
- ⚠️ Kulturelle Nuancen eventuell nicht 100% perfekt

**Empfehlung:**
- Automatische Übersetzung als **Basis** (95% Qualität)
- Native Speaker können später **einzelne Begriffe verfeinern**

---

## 🛠️ Troubleshooting

### "Ollama nicht erreichbar"
```bash
# Starte Ollama
ollama serve
```

### "llama3.2 nicht gefunden"
```bash
# Installiere Model
ollama pull llama3.2
```

### "ModuleNotFoundError: No module named 'ollama'"
```bash
# Installiere Python-Paket
pip install ollama
```

### Script läuft zu langsam?
- Normal! 206 Keys × 8 Sprachen = 1648 Übersetzungen
- Dauert ca. **15-30 Minuten** (abhängig von CPU)
- Läuft vollautomatisch, einfach laufen lassen

---

## 📝 Technische Details

**Datei:** `scripts/i18n-auto-translate.py`
**Abhängigkeiten:** `ollama` (Python Package)
**Model:** `llama3.2` (lokal via Ollama)
**Eingabe:** `frontend/js/i18n.js`
**Ausgabe:** Updated `frontend/js/i18n.js`

**Zeilen Code:** ~320
**Sprachen:** FR, ES, IT, PT, SV, NO, DA, NL
**Übersetzungen pro Lauf:** ~1648

---

## 💡 Entwickler-Tipps

### Dry-Run Mode (Test ohne Änderungen)
Ändere in Zeile 304:
```python
completed = complete_translations(i18n_path, lang_code, dry_run=True)
```

### Nur eine Sprache übersetzen
Ändere in Zeile 302:
```python
for lang_code in ['fr']:  # Nur Französisch
```

### Andere Ollama-Models testen
Ändere in Zeile 85:
```python
model='llama3.3:70b'  # Größeres Model für bessere Qualität
```

---

## 🤝 Contributions

Wenn du **Native Speaker** bist und Übersetzungen verbessern möchtest:
1. Öffne `frontend/js/i18n.js`
2. Suche nach deiner Sprache (z.B. `fr:`)
3. Verbessere einzelne Übersetzungen
4. Pull Request erstellen

**Tipp:** Fokussiere auf häufig genutzte Keys (auth.*, nav.*, common.*)
