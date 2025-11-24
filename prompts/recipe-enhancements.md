# Recipe Enhancements - KitchenHelper-AI

## 📋 KONTEXT

Recipe System funktioniert, aber fehlt Polish-Features. Ziel: Rating, Notes, Portion Calculator und Search/Filter hinzufügen für bessere UX.

**Projekt-Pfade:**
- Stand-PC: `C:\Users\Startklar\Desktop\GitHub\kitchenhelper-ai`
- Laptop: `C:\Users\david\Desktop\GitHub\kitchenhelper-ai`

**Existing:**
- Recipe Model: `/mnt/project/recipe-_models.py`
- Recipe Routes: `/mnt/project/recipes-_routes.py`
- Recipe Frontend: `/mnt/project/recipes.js`

## 🎯 AUFGABEN

### Feature #1: Recipe Rating System
**Was:** 1-5 Sterne Rating für Rezepte

**Backend:**
- [ ] Model: `/mnt/project/recipe-_models.py`
  - Add: `rating = Column(Integer, nullable=True)` (1-5)
- [ ] Schema: `/mnt/project/recipe-_models.py`
  - RecipeResponse: Include rating field
- [ ] Route: PATCH /api/recipes/{id}/rating
  - Body: `{"rating": 4}`
  - Validation: 1-5 only

**Frontend:**
- [ ] `/mnt/project/recipes.js`
  - Star display (★★★★☆)
  - Click to rate
  - Visual feedback
- [ ] `/mnt/project/favorites.js`
  - Same rating display

### Feature #2: Recipe Notes
**Was:** User kann persönliche Notizen zu Rezepten hinzufügen

**Backend:**
- [ ] Model: Add `notes = Column(Text, nullable=True)`
- [ ] Route: PATCH /api/recipes/{id}/notes
  - Body: `{"notes": "Weniger Salz nächstes Mal"}`

**Frontend:**
- [ ] Notes section in recipe card (collapsed by default)
- [ ] "Notizen hinzufügen" button → Text area
- [ ] Save/Cancel buttons
- [ ] Display saved notes

### Feature #3: Portion Calculator
**Was:** Rezept-Mengen automatisch für 1/2/4/6 Personen anpassen

**Backend:**
- [ ] Route: GET /api/recipes/{id}/portions?servings=4
  - Multipliziert alle Mengen
  - Returns: Adjusted recipe
- [ ] Calculation: `new_amount = original_amount * (servings / original_servings)`

**Frontend:**
- [ ] Portion selector: [1] [2] [4] [6] Personen
- [ ] Live update von Mengen
- [ ] Highlight geänderte Werte

### Feature #4: Search & Filter
**Was:** Rezepte durchsuchen und filtern

**Backend:**
- [ ] Route: GET /api/recipes/search?q={query}&rating_min=3&has_notes=true
  - Fulltext search in title + ingredients
  - Filter by rating
  - Filter by notes existence
  - Filter by favorites

**Frontend:**
- [ ] Search bar mit live search
- [ ] Filter chips: "Nur Favoriten", "Mit Notizen", "4+ Sterne"
- [ ] Results update on change

## 🧪 TESTING
```javascript
// Rating Test
// 1. Click 4 stars on recipe
// → Saved, displays ★★★★☆

// Notes Test  
// 1. Click "Notizen hinzufügen"
// 2. Enter: "Super lecker!"
// → Saved, displays below recipe

// Portions Test
// 1. Recipe for 2 persons: 200g rice
// 2. Select 4 persons
// → Shows 400g rice

// Search Test
// 1. Type "Pasta" in search
// → Filters recipes with "Pasta" in title/ingredients
```

## 📦 DATEIEN

**Bearbeiten:**
- `/mnt/project/recipe-_models.py`
- `/mnt/project/recipes-_routes.py`
- `/mnt/project/recipes.js`
- `/mnt/project/favorites.js`
- `/mnt/project/components.css`

---

**START:** Feature #1 (Rating), dann #2 (Notes), dann #3 (Portions), dann #4 (Search). Einzeln testen!