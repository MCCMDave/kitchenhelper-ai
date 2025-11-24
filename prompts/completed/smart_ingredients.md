# Smart Ingredients System - KitchenHelper-AI

## 📋 KONTEXT

KitchenHelper-AI hat basic Ingredients CRUD. Ziel: Intelligence Layer hinzufügen mit Auto-Category Detection, Auto-Suggestions und Quick-Select für häufige Gewürze. Macht Ingredient-Management 10x besser.

**Projekt-Pfade:**
- Stand-PC: `C:\Users\Startklar\Desktop\GitHub\kitchenhelper-ai`
- Laptop: `C:\Users\david\Desktop\GitHub\kitchenhelper-ai`

**Tech Stack:**
- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: Vanilla JS, HTML, CSS
- Existing: `/mnt/project/ingredients.js`, `/mnt/project/ingredients-_routes.py`

## 🎯 AUFGABEN

### Feature #1: Auto-Category Detection
**Was:** System erkennt automatisch die Kategorie beim Eingeben einer Zutat

**Backend:**
- [ ] Service: `/mnt/project/utils/category_detector.py`
```python
  class CategoryDetector:
      CATEGORIES = {
          "Gemüse": ["tomate", "paprika", "zwiebel", "knoblauch", ...],
          "Obst": ["apfel", "banane", "orange", ...],
          "Fleisch": ["hähnchen", "rind", "schwein", ...],
          "Gewürze": ["salz", "pfeffer", "paprika", ...],
          # ... mehr Kategorien
      }
      
      def detect(self, ingredient_name: str) -> str:
          # Fuzzy matching mit lowercase
          # Return best match oder "Sonstiges"
```
- [ ] Route: `/mnt/project/ingredients-_routes.py`
  - POST /api/ingredients/detect-category
  - Body: `{"name": "Tomate"}`
  - Response: `{"category": "Gemüse", "confidence": 0.95}`
- [ ] Integration: Auto-suggest category in POST /api/ingredients/

**Frontend:**
- [ ] `/mnt/project/ingredients.js`
  - On ingredient name input (debounced)
  - Call detect-category API
  - Auto-fill category field (user kann überschreiben)
  - Visual feedback: "Kategorie erkannt: Gemüse ✓"

### Feature #2: Auto-Suggestion Dropdown
**Was:** Beim Tippen werden passende Zutaten vorgeschlagen (aus DB + Predefined List)

**Backend:**
- [ ] Route: GET /api/ingredients/suggestions?q={query}
  - Sucht in User's ingredients
  - Sucht in predefined common ingredients list
  - Returns: `[{"name": "Tomate", "category": "Gemüse", "source": "common"}]`
- [ ] Predefined List: `/mnt/project/data/common_ingredients.json`
```json
  [
    {"name": "Tomate", "category": "Gemüse"},
    {"name": "Zwiebel", "category": "Gemüse"},
    {"name": "Knoblauch", "category": "Gemüse"},
    // ... 100-200 häufigste Zutaten
  ]
```

**Frontend:**
- [ ] `/mnt/project/ingredients.js`
  - Autocomplete component
  - Debounced search (300ms)
  - Dropdown mit max 10 suggestions
  - Keyboard navigation (Arrow Up/Down, Enter)
  - Click to select
- [ ] `/mnt/project/components.css`
  - Autocomplete dropdown styling
  - Highlight selected item

### Feature #3: Spice Quick-Select
**Was:** Schnellauswahl-Interface für häufige Gewürze mit einem Click

**UI Design:**
```
[+ Zutat hinzufügen]  [⚡ Gewürze]  <- Toggle

Wenn "Gewürze" aktiv:
┌─────────────────────────────────┐
│ Häufige Gewürze:                │
│ [Salz] [Pfeffer] [Paprika]      │
│ [Oregano] [Basilikum] [Thymian] │
│ [Knoblauch] [Zwiebel] [Chili]   │
│                                  │
│ Alle schon hinzugefügt? ✓       │
└─────────────────────────────────┘
```

**Backend:**
- [ ] Model: Existing ingredients table (no changes)
- [ ] Route: POST /api/ingredients/batch
  - Body: `{"ingredients": [{"name": "Salz", "category": "Gewürze"}, ...]}`
  - Creates multiple at once
  - Returns: Created ingredients

**Frontend:**
- [ ] `/mnt/project/ingredients.js`
  - spiceQuickSelect() function
  - Modal/Panel mit Grid von Spice-Buttons
  - Checkboxes für Selection
  - "Alle hinzufügen" Button
  - Existing spices = disabled/checked
- [ ] Predefined Spices List:
```javascript
  const COMMON_SPICES = [
    {name: "Salz", category: "Gewürze", icon: "🧂"},
    {name: "Pfeffer", category: "Gewürze", icon: "🌶️"},
    {name: "Paprika", category: "Gewürze", icon: "🌶️"},
    // ... ~20 häufigste Gewürze
  ];
```

### Feature #4: Duplicate Prevention
**Was:** Warnung wenn User versucht existierende Zutat nochmal hinzuzufügen

**Backend:**
- [ ] Route: POST /api/ingredients/ 
  - Check if ingredient with same name (case-insensitive) exists
  - If yes: Return 409 Conflict mit suggestion
  - Response: `{"error": "Ingredient exists", "existing_id": 123, "suggestion": "update_quantity"}`

**Frontend:**
- [ ] `/mnt/project/ingredients.js`
  - Catch 409 error
  - Show modal: "Tomate existiert bereits. Menge erhöhen?"
  - Options: "Abbrechen" | "Menge erhöhen"
  - If "Menge erhöhen" → PATCH /api/ingredients/{id}

## 🧪 TESTING

### Auto-Category Test:
```bash
# Test detection
POST /api/ingredients/detect-category
{"name": "Tomate"}
# → {"category": "Gemüse", "confidence": 0.95}

# Frontend: Tippe "Paprika"
# → Kategorie-Field füllt sich automatisch mit "Gemüse"
```

### Auto-Suggestion Test:
```bash
# Test suggestions
GET /api/ingredients/suggestions?q=tom
# → [{"name": "Tomate", "category": "Gemüse", "source": "common"}]

# Frontend: Tippe "Tom"
# → Dropdown zeigt: Tomate, Tomatensauce, etc.
```

### Spice Quick-Select Test:
```javascript
// 1. Click "⚡ Gewürze" button
// 2. Modal opens with 20 common spices
// 3. Select: Salz, Pfeffer, Oregano
// 4. Click "Hinzufügen"
// → All 3 added to ingredients list
// 5. Open modal again
// → Selected spices are disabled/checked
```

### Duplicate Prevention Test:
```bash
# 1. Add "Tomate"
# 2. Try to add "Tomate" again
# → Modal: "Tomate existiert bereits. Menge erhöhen?"
# 3. Click "Menge erhöhen"
# → Opens edit modal with existing ingredient
```

## 📦 DATEIEN

**Erstellen:**
- `/mnt/project/utils/category_detector.py`
- `/mnt/project/data/common_ingredients.json`

**Bearbeiten:**
- `/mnt/project/ingredients-_routes.py` (neue routes)
- `/mnt/project/ingredients.js` (alle 4 features)
- `/mnt/project/components.css` (autocomplete, spice grid)
- `/mnt/project/api.js` (neue API calls)

**Nicht ändern:**
- Models (keine DB-Changes nötig)
- Andere Frontend-Module

## 📝 CODE PATTERNS

**Category Detection (Fuzzy Match):**
```python
from difflib import SequenceMatcher

def fuzzy_match(term: str, choices: list) -> str:
    term = term.lower()
    best = max(choices, key=lambda x: SequenceMatcher(None, term, x.lower()).ratio())
    return best
```

**Debounced Input (Frontend):**
```javascript
let debounceTimer;
function debouncedSearch(query) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        fetchSuggestions(query);
    }, 300);
}
```

**Autocomplete Keyboard Nav:**
```javascript
input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') selectedIndex++;
    if (e.key === 'ArrowUp') selectedIndex--;
    if (e.key === 'Enter') selectItem(selectedIndex);
});
```

## 🚫 NICHT TUN

- ❌ Keine AI/ML Models (zu komplex, bleib bei simple fuzzy matching)
- ❌ Keine externe API calls (offline-fähig bleiben)
- ❌ Keine Breaking Changes an existierenden APIs
- ❌ Keine Änderung der Datenbank-Struktur

---

**START:** Feature #1 (Auto-Category) implementieren und testen, dann #2 (Auto-Suggestions), dann #3 (Spice Quick-Select), dann #4 (Duplicate Prevention). Jedes Feature einzeln testen!