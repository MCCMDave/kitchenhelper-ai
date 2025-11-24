# Bug-Fix Bundle - KitchenHelper-AI

## 📋 KONTEXT

KitchenHelper-AI MVP läuft stabil, hat aber 4 bekannte UX-Bugs die vor weiteren Features behoben werden sollten. Ziel: Alle Bugs fixen für stabile Production-Basis.

**Projekt-Pfade:**
- Stand-PC: `C:\Users\Startklar\Desktop\GitHub\kitchenhelper-ai`
- Laptop: `C:\Users\david\Desktop\GitHub\kitchenhelper-ai`

**Tech Stack:**
- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: Vanilla JS, HTML, CSS
- Referenz: `/mnt/project/` Files

## 🎯 AUFGABEN

### Bug #1: German Umlauts Display
**Problem:** ä, ö, ü werden als falsche Zeichen angezeigt

**Fix:**
- [ ] Backend: UTF-8 Response Headers prüfen (`app/main.py`)
- [ ] Frontend: Meta charset prüfen (sollte `<meta charset="UTF-8">` sein)
- [ ] API Responses: Ensure proper encoding in all routes
- [ ] Database: Check SQLite encoding (sollte UTF-8 sein)
- [ ] Test mit: "Hähnchenbrust", "Käse", "Öl", "Gemüse"

**Files:**
- `/mnt/project/main.py` - Add charset to response headers
- `/mnt/project/index.html` - Verify meta tag
- `/mnt/project/dashboard.html` - Verify meta tag
- Alle `/mnt/project/*-_routes.py` - Check response encoding

### Bug #2: Favorites Expansion
**Problem:** Favorites zeigen nicht die vollen Rezept-Details beim Expandieren

**Fix:**
- [ ] Frontend: `/mnt/project/favorites.js` 
  - renderCard() Funktion analysieren
  - Expansion-Logic für Details implementieren
  - Ähnlich wie in recipes.js (Referenz nutzen!)
- [ ] Toggle-Mechanismus: Click expands/collapses
- [ ] Show: Ingredients List, Nutrition, Instructions, Cooking Time
- [ ] CSS: Smooth transition für expansion

**Referenz:**
- `/mnt/project/recipes.js` - Expansion pattern kopieren
- `/mnt/project/components.css` - Existing card styles

### Bug #3: Dark Mode Contrast
**Problem:** Schlechte Lesbarkeit in Dark Mode (Kontrast zu niedrig)

**Fix:**
- [ ] CSS: `/mnt/project/variables.css`
  - Dark mode colors überprüfen
  - Kontrast erhöhen (WCAG AA Standard: min 4.5:1)
  - Text auf dunklem Hintergrund: Heller machen
  - Buttons/Cards: Besserer Kontrast
- [ ] Test: Mit Browser DevTools Contrast Checker
- [ ] Alle Texte lesbar bei aktivem Dark Mode

**Variables zu prüfen:**
```css
[data-theme="dark"] {
  --text-primary: /* Heller machen */
  --text-secondary: /* Heller machen */
  --bg-primary: /* Evtl. etwas heller */
  --bg-secondary: /* Kontrast zu bg-primary */
}
```

### Bug #4: Multi-Profile Selection
**Problem:** User kann nicht mehrere Diät-Profile gleichzeitig aktivieren (z.B. "Diabetiker" + "Vegan")

**Fix Backend:**
- [ ] Schema: `/mnt/project/diet_profile-_models.py`
  - Aktuell: Single profile per user (vermutlich `is_active` boolean?)
  - Neu: Multiple active profiles möglich
  - Option A: Remove `is_active` constraint, allow multiple
  - Option B: Change to JSON array in User model
- [ ] Routes: `/mnt/project/diet_profiles-_routes.py`
  - GET active profiles (plural!)
  - POST toggle profile (add/remove from active list)
  - Ensure recipe generation considers ALL active profiles

**Fix Frontend:**
- [ ] UI: `/mnt/project/profiles.js`
  - Multi-select statt radio buttons
  - Checkboxes für Profile-Auswahl
  - Visual feedback für multiple selections
  - Recipe generation berücksichtigt alle aktiven Profile

**Wichtig:** Backward compatibility! Existing single-profile users dürfen nicht brechen.

## 🧪 TESTING

### Umlauts Test:
```bash
# Create ingredient with umlauts
POST /api/ingredients/
{
  "name": "Hähnchenbrust",
  "category": "Geflügel",
  "quantity": "500g"
}

# Verify in Frontend
# → Should display: Hähnchenbrust (not H�hnchenbrust)
```

### Favorites Expansion Test:
```javascript
// 1. Add recipe to favorites
// 2. Go to Favorites tab
// 3. Click on favorite card
// → Should expand and show full details
// 4. Click again → Should collapse
```

### Dark Mode Test:
```javascript
// 1. Toggle dark mode in UI
// 2. Check all pages: Dashboard, Ingredients, Recipes, Favorites
// 3. Verify all text is readable
// 4. Use DevTools: Check contrast ratio (min 4.5:1)
```

### Multi-Profile Test:
```bash
# 1. Create profiles: "Diabetiker", "Vegan"
# 2. Activate both profiles
# 3. Generate recipe
# → Should consider BOTH restrictions
# 4. Recipe should have KE/BE AND no animal products
```

## 📦 DATEIEN

**Bearbeiten:**
- `/mnt/project/main.py` (UTF-8 headers)
- `/mnt/project/index.html` (charset check)
- `/mnt/project/dashboard.html` (charset check)
- `/mnt/project/favorites.js` (expansion logic)
- `/mnt/project/variables.css` (dark mode contrast)
- `/mnt/project/diet_profile-_models.py` (multi-profile logic)
- `/mnt/project/diet_profiles-_routes.py` (multi-profile API)
- `/mnt/project/profiles.js` (multi-select UI)
- `/mnt/project/components.css` (expansion transitions)

**Nicht erstellen:**
- Keine neuen Files nötig

## 🚫 NICHT TUN

- ❌ Keine neuen Features hinzufügen
- ❌ Keine Datenbank-Migration (außer für multi-profile wenn nötig)
- ❌ Keine Design-Überarbeitung (nur Contrast-Fix)
- ❌ Keine Breaking Changes an existierenden APIs

## 📝 NOTIZEN

- Umlauts: Standard-Problem, sollte einfach zu fixen sein
- Favorites: Code von recipes.js wiederverwenden
- Dark Mode: WCAG AA = min 4.5:1, AAA = min 7:1 (shoot for AA)
- Multi-Profile: Vorsicht mit backward compatibility!

---

**START:** Bug #1 (Umlauts) fixen, dann #2 (Favorites), dann #3 (Dark Mode), dann #4 (Multi-Profile). Nach jedem Bug testen!