# Encoding-Regeln für KitchenHelper-AI

## Alle Dateien: UTF-8 mit Umlauten

Für dieses Projekt verwenden wir **durchgehend UTF-8 Encoding**.

### JavaScript (.js), HTML, CSS, Markdown (.md)

✅ **Deutsche Umlaute IMMER verwenden!**

Korrekte deutsche Rechtschreibung mit ä, ö, ü, ß ist **Pflicht**.

**Beispiel:**
```javascript
// ✅ Richtig
const text = "Gewürze verwalten";
const hint = "Klicke auf ein Gewürz um es hinzuzufügen";

// ❌ Falsch
const text = "Gewuerze verwalten";
const hint = "Klicke auf ein Gewuerz um es hinzuzufuegen";
```

### Python (.py)

✅ **Deutsche Umlaute in Strings OK!**

Python 3 unterstützt UTF-8 standardmäßig.

**Beispiel:**
```python
# ✅ Richtig
message = "Rezept erfolgreich erstellt"
description = "Gewürze und Kräuter"

# In Docstrings auch OK
def generate_recipe():
    """
    Generiere ein Rezept basierend auf verfügbaren Zutaten.
    Berücksichtigt Ernährungsprofile und Präferenzen.
    """
```

### JSON (.json)

✅ **Umlaute erlaubt**

JSON ist UTF-8 kompatibel.

**Beispiel:**
```json
{
  "name": "Käsespätzle",
  "category": "Hauptgericht",
  "ingredients": ["Mehl", "Eier", "Käse"]
}
```

## PDF-Export Hinweis

⚠️ **Emojis im PDF werden entfernt**

Die reportlab-Bibliothek unterstützt keine Emojis (Unicode > U+FFFF).
Diese werden automatisch im PDF-Generator entfernt.

**Lösung:**
- UI: Emojis verwenden (🌿 🥩 🧀)
- PDF: Nur Text ohne Emojis

## Zusammenfassung

```
Alle Dateitypen → UTF-8 Encoding
Umlaute        → IMMER verwenden (ä ö ü ß)
Emojis         → OK in UI, werden in PDF entfernt
```
