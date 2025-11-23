# Shopping List Generator

## 📋 KONTEXT
Favorites + PDF läuft. Ziel: Aus mehreren Rezepten automatisch Einkaufsliste, gruppiert nach Kategorie.

## 🎯 AUFGABEN

### Backend
- [ ] Models: `/mnt/project/backend/app/models/shopping_list.py`
  - ShoppingList (id, user_id, name, created_at, items relationship)
  - ShoppingListItem (id, list_id, ingredient_name, amount, category, is_checked)
- [ ] Routes: `/mnt/project/backend/app/routes/shopping_lists.py`
  - POST /from-recipes → consolidate ingredients from recipe_ids
  - GET / → All lists mit summary (items_count, checked_count)
  - GET /{id} → Full list grouped by category (items_by_category)
  - PATCH /items/{id}/check → Toggle is_checked
  - DELETE /{id}
- [ ] Main: Import + register router
- [ ] Database: Import models

### Frontend
- [ ] Modul: `/mnt/project/frontend/js/shopping.js`
  - addRecipe(recipeId) → selectedRecipes Set + confirm dialog
  - generateList() → Create via API
  - viewList(listId) → Load + render modal
  - renderList() → Categories als sections, checkboxes
  - toggleItem(itemId, checked) → Update backend
  - closeList() → Remove modal
- [ ] API: `/mnt/project/frontend/js/api.js`
  - createShoppingList(recipeIds, listName)
  - getShoppingLists(), getShoppingList(id)
  - toggleShoppingItem(itemId, isChecked)
  - deleteShoppingList(id)
- [ ] Favorites: Button "Zur Einkaufsliste" hinzufügen
- [ ] Dashboard: Script-Tag

## 📝 CODE

**Consolidation Logic (Backend):**
```python
from collections import defaultdict

ingredients_map = defaultdict(lambda: {"amounts": [], "category": None})

for recipe in recipes:
    ingredients = json.loads(recipe.ingredients_json)
    for ing in ingredients:
        name = ing['name'].lower()
        ingredients_map[name]['amounts'].append(ing.get('amount', ''))

# Create items
for name, data in ingredients_map.items():
    combined_amount = ", ".join(data['amounts']) if data['amounts'] else ''
    item = ShoppingListItem(
        shopping_list_id=list_id,
        ingredient_name=name.title(),
        amount=combined_amount,
        category=data['category'] or 'Sonstiges',
        is_checked=False
    )
```

**Category Grouping (Backend):**
```python
items_by_category = defaultdict(list)
for item in shopping_list.items:
    items_by_category[item.category or 'Sonstiges'].append({
        "id": item.id,
        "name": item.ingredient_name,
        "amount": item.amount,
        "is_checked": item.is_checked
    })

return {"items_by_category": dict(items_by_category)}
```

**Modal Rendering (Frontend):**
```javascript
renderList() {
    const html = `
        <div class="shopping-list-modal">
            <div class="modal-content">
                <h2>${this.currentList.name}</h2>
                ${Object.entries(this.currentList.items_by_category).map(([cat, items]) => `
                    <div class="shopping-category">
                        <h3>${cat}</h3>
                        <ul>
                            ${items.map(item => `
                                <li>
                                    <input type="checkbox" ${item.is_checked ? 'checked' : ''}
                                           onchange="ShoppingList.toggleItem(${item.id}, this.checked)">
                                    <span style="${item.is_checked ? 'text-decoration: line-through;' : ''}">
                                        ${item.amount} ${item.name}
                                    </span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                `).join('')}
                <button onclick="ShoppingList.closeList()">Schließen</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
}
```

## 🧪 TESTING
```bash
# Swagger
POST /shopping-lists/from-recipes {"recipe_ids": [1,2,3], "list_name": "Test"}
→ Consolidated items, grouped

GET /shopping-lists/ → Summary
GET /shopping-lists/1 → Full with items_by_category
PATCH /shopping-lists/items/1/check {"is_checked": true}

# Frontend
1. Click "Zur Einkaufsliste" on 3 recipes
2. Confirm dialog → "Liste erstellen"
3. Enter name
4. Modal shows all ingredients
5. Check items → Line-through
6. Categories grouped correctly
```

## 📦 DATEIEN

**Erstellen:**
- `/mnt/project/backend/app/models/shopping_list.py`
- `/mnt/project/backend/app/routes/shopping_lists.py`
- `/mnt/project/frontend/js/shopping.js`

**Bearbeiten:**
- `/mnt/project/backend/app/main.py` (router)
- `/mnt/project/backend/app/utils/database.py` (imports)
- `/mnt/project/frontend/js/api.js` (5 functions)
- `/mnt/project/frontend/js/favorites.js` (button)
- `/mnt/project/dashboard.html` (script)

---

**START:** ShoppingList Models (2 Models mit relationships)