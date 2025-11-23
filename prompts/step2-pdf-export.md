# PDF Export für Rezepte

## 📋 KONTEXT
Favorites läuft. Ziel: Rezepte als formatierte PDFs exportieren mit reportlab.

## 🎯 AUFGABEN

### Backend
- [ ] Dependency: `reportlab==4.0.7` zu requirements.txt
- [ ] Service: `/mnt/project/backend/app/services/pdf_generator.py`
  - Class RecipePDFGenerator mit generate(recipe_data: Dict) → BytesIO
  - A4 Format, Margins 2cm
  - Content: Title, Meta-Table, Ingredients-List, Nutrition-Table, Footer
- [ ] Route: `/mnt/project/backend/app/routes/recipes.py`
  - GET /{recipe_id}/export/pdf
  - Load recipe, prepare dict, call generator
  - StreamingResponse mit application/pdf
  - Safe filename: recipe.name → replace spaces/slashes

### Frontend
- [ ] Update: `/mnt/project/frontend/js/favorites.js`
  - exportRecipe(recipeId) implementieren
  - Fetch mit Authorization header
  - Blob download trigger
  - UI feedback (info → success/error)

## 📝 CODE

**TableStyle (kritisch für Layout):**
```python
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

meta_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
]))
```

**Blob Download:**
```javascript
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `rezept_${recipeId}.pdf`;
document.body.appendChild(a);
a.click();
window.URL.revokeObjectURL(url);
document.body.removeChild(a);
```

**StreamingResponse:**
```python
from fastapi.responses import StreamingResponse

safe_name = recipe.name.replace(' ', '_').replace('/', '_')[:50]
filename = f"rezept_{safe_name}.pdf"

return StreamingResponse(
    pdf_buffer,
    media_type="application/pdf",
    headers={"Content-Disposition": f'attachment; filename="{filename}"'}
)
```

## 🧪 TESTING
```bash
# Backend
pip install reportlab==4.0.7
uvicorn app.main:app --reload  # restart needed

# Swagger
GET /api/recipes/1/export/pdf → Download starts

# PDF Check
- Title correct
- Meta table (difficulty, time, method, servings)
- Ingredients list complete
- Nutrition (nur KE oder BE, nicht beide!)
- Footer "Erstellt mit KitchenHelper-AI 🍳"

# Frontend
1. Open favorite
2. Click "Als PDF"
3. PDF downloads
4. Open → Verify content
```

## 📦 DATEIEN

**Erstellen:**
- `/mnt/project/backend/app/services/pdf_generator.py`

**Bearbeiten:**
- `/mnt/project/requirements.txt` (reportlab)
- `/mnt/project/backend/app/routes/recipes.py` (export endpoint)
- `/mnt/project/frontend/js/favorites.js` (exportRecipe method)

---

**START:** PDF Generator Service mit reportlab SimpleDocTemplate