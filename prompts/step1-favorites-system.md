# Favorites System - Backend + Frontend

## 📋 KONTEXT
Backend MVP läuft (User/Ingredients/Recipes). Frontend in Vanilla JS. Ziel: Vollständiges Favorites mit embedded recipes.

## 🎯 AUFGABEN

### Backend
- [ ] Model: `/mnt/project/backend/app/models/favorite.py`
  - Pattern: `ingredient.py` als Referenz
  - Relationships: User + Recipe (joinedload wichtig!)
  - UniqueConstraint('user_id', 'recipe_id')
- [ ] Schema: `/mnt/project/backend/app/schemas/favorite.py`
  - FavoriteCreate, FavoriteResponse, FavoriteWithRecipe
  - FavoriteWithRecipe hat embedded RecipeResponse
- [ ] Routes: `/mnt/project/backend/app/routes/favorites.py`
  - GET / → joinedload(Favorite.recipe), parse JSON fields
  - POST / → Duplikat-Check before create
  - DELETE /{id} → 204
  - GET /check/{recipe_id} → {is_favorite, favorite_id}
- [ ] Main: Import + register favorites router
- [ ] Database: Import favorite in init_db()

### Frontend
- [ ] Modul: `/mnt/project/frontend/js/favorites.js`
  - load(), render(), renderCard(favorite)
  - toggle(recipeId) → add/remove
  - Cache: favoriteIds Set für Lookups
  - renderNutrition() → KE oder BE (nicht beide!)
- [ ] API Client: `/mnt/project/frontend/js/api.js`
  - getFavorites(), addFavorite(recipeId), removeFavorite(id), checkFavorite(recipeId)
- [ ] Dashboard: Script-Tag einbinden

## 📝 CODE

**UniqueConstraint (Model):**
```python
__table_args__ = (
    UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe'),
)
```

**Joinedload Pattern (Route):**
```python
favorites = db.query(Favorite).filter(
    Favorite.user_id == current_user.id
).options(
    joinedload(Favorite.recipe)
).order_by(Favorite.added_at.desc()).all()

# JSON parsing
recipe_response = RecipeResponse(
    ingredients=[RecipeIngredient(**ing) for ing in json.loads(recipe.ingredients_json)],
    nutrition_per_serving=NutritionInfo(**json.loads(recipe.nutrition_json))
)
```

**Frontend Toggle:**
```javascript
async toggle(recipeId) {
    const isFavorite = this.favoriteIds.has(recipeId);
    if (isFavorite) {
        const fav = this.items.find(f => f.recipe.id === recipeId);
        await api.removeFavorite(fav.id);
        this.favoriteIds.delete(recipeId);
    } else {
        await api.addFavorite(recipeId);
        this.favoriteIds.add(recipeId);
    }
}
```

## 🧪 TESTING
```bash
# Swagger
GET /api/favorites/ → Embedded recipes check
POST /api/favorites/ {"recipe_id": 1} → 201
POST /api/favorites/ {"recipe_id": 1} → 400 (duplicate)
DELETE /api/favorites/1 → 204

# Manual
1. Generate 3 recipes
2. Click ⭐ on 2 recipes
3. Go to Favorites tab → Full cards
4. Click ⭐ again → Remove
```

## 📦 DATEIEN

**Erstellen:**
- `/mnt/project/backend/app/models/favorite.py`
- `/mnt/project/backend/app/schemas/favorite.py`
- `/mnt/project/backend/app/routes/favorites.py`
- `/mnt/project/frontend/js/favorites.js`

**Bearbeiten:**
- `/mnt/project/backend/app/main.py` (router)
- `/mnt/project/backend/app/utils/database.py` (import)
- `/mnt/project/frontend/js/api.js` (4 functions)
- `/mnt/project/dashboard.html` (script tag)

---

**START:** Favorite Model nach ingredient.py Pattern