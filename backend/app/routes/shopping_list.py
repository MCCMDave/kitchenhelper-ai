# Shopping List Routes
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
import json
import re
from io import BytesIO

from app.schemas.shopping_list import (
    ShoppingListRequest,
    ShoppingListResponse,
    ShoppingListItem
)
from app.models.recipe import Recipe
from app.models.favorite import Favorite
from app.models.user import User
from app.utils.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/shopping-list", tags=["Shopping List"])

# Category mapping for sorting
INGREDIENT_CATEGORIES = {
    # Vegetables
    'tomato': 'Vegetables', 'tomate': 'Vegetables', 'tomaten': 'Vegetables',
    'potato': 'Vegetables', 'kartoffel': 'Vegetables', 'kartoffeln': 'Vegetables',
    'carrot': 'Vegetables', 'karotte': 'Vegetables', 'karotten': 'Vegetables',
    'onion': 'Vegetables', 'zwiebel': 'Vegetables', 'zwiebeln': 'Vegetables',
    'garlic': 'Vegetables', 'knoblauch': 'Vegetables',
    'pepper': 'Vegetables', 'paprika': 'Vegetables',
    'cucumber': 'Vegetables', 'gurke': 'Vegetables',
    'broccoli': 'Vegetables', 'brokkoli': 'Vegetables',
    'spinach': 'Vegetables', 'spinat': 'Vegetables',
    'salad': 'Vegetables', 'salat': 'Vegetables',
    'zucchini': 'Vegetables',

    # Meat & Fish
    'chicken': 'Meat & Fish', 'haehnchen': 'Meat & Fish', 'hahnchen': 'Meat & Fish',
    'beef': 'Meat & Fish', 'rind': 'Meat & Fish', 'rindfleisch': 'Meat & Fish',
    'pork': 'Meat & Fish', 'schwein': 'Meat & Fish', 'schweinefleisch': 'Meat & Fish',
    'salmon': 'Meat & Fish', 'lachs': 'Meat & Fish',
    'fish': 'Meat & Fish', 'fisch': 'Meat & Fish',
    'bacon': 'Meat & Fish', 'speck': 'Meat & Fish',

    # Dairy
    'milk': 'Dairy', 'milch': 'Dairy',
    'cheese': 'Dairy', 'kaese': 'Dairy', 'käse': 'Dairy',
    'butter': 'Dairy',
    'cream': 'Dairy', 'sahne': 'Dairy',
    'yogurt': 'Dairy', 'joghurt': 'Dairy',
    'egg': 'Dairy', 'ei': 'Dairy', 'eier': 'Dairy',

    # Pantry
    'rice': 'Pantry', 'reis': 'Pantry',
    'pasta': 'Pantry', 'nudeln': 'Pantry', 'spaghetti': 'Pantry',
    'flour': 'Pantry', 'mehl': 'Pantry',
    'oil': 'Pantry', 'oel': 'Pantry', 'öl': 'Pantry',
    'sugar': 'Pantry', 'zucker': 'Pantry',
    'salt': 'Pantry', 'salz': 'Pantry',

    # Spices
    'pepper': 'Spices', 'pfeffer': 'Spices',
    'basil': 'Spices', 'basilikum': 'Spices',
    'oregano': 'Spices',
    'thyme': 'Spices', 'thymian': 'Spices',
    'curry': 'Spices',
    'paprika': 'Spices',
}


def categorize_ingredient(name: str) -> str:
    """Determine category for an ingredient"""
    normalized = name.lower().strip()
    for key, category in INGREDIENT_CATEGORIES.items():
        if key in normalized:
            return category
    return 'Other'


def parse_amount(amount_str: str) -> tuple:
    """Parse amount string to (number, unit)"""
    match = re.match(r'(\d+(?:\.\d+)?)\s*(\w+)?', amount_str.strip())
    if match:
        return float(match.group(1)), match.group(2) or ''
    return 1.0, amount_str


def combine_ingredients(ingredients_list: List[Dict]) -> List[ShoppingListItem]:
    """Combine duplicate ingredients and sum amounts"""
    combined = {}

    for ing in ingredients_list:
        name = ing.get('name', '').strip()
        amount_str = ing.get('amount', '1')

        if not name:
            continue

        # Normalize name for comparison
        key = name.lower()

        if key in combined:
            # Try to add amounts
            existing_num, existing_unit = parse_amount(combined[key]['amount'])
            new_num, new_unit = parse_amount(amount_str)

            if existing_unit == new_unit or not new_unit:
                combined[key]['amount'] = f"{existing_num + new_num} {existing_unit}".strip()
            else:
                # Different units, just append
                combined[key]['amount'] = f"{combined[key]['amount']} + {amount_str}"
        else:
            combined[key] = {
                'name': name,
                'amount': amount_str,
                'category': categorize_ingredient(name)
            }

    # Convert to ShoppingListItem and sort by category
    items = [
        ShoppingListItem(
            name=data['name'],
            amount=data['amount'],
            category=data['category'],
            checked=False
        )
        for data in combined.values()
    ]

    # Sort by category, then by name
    category_order = ['Vegetables', 'Meat & Fish', 'Dairy', 'Pantry', 'Spices', 'Other']
    items.sort(key=lambda x: (
        category_order.index(x.category) if x.category in category_order else 99,
        x.name.lower()
    ))

    return items


@router.post("/generate", response_model=ShoppingListResponse)
def generate_shopping_list(
    request: ShoppingListRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate shopping list from recipes and/or favorites.

    - **recipe_ids**: List of recipe IDs to include
    - **favorite_ids**: List of favorite IDs to include
    - **scale_factor**: Scale ingredients (e.g., 2.0 for double portions)
    """
    if not request.recipe_ids and not request.favorite_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide at least one recipe_id or favorite_id"
        )

    all_ingredients = []
    recipe_names = []

    # Load recipes
    if request.recipe_ids:
        recipes = db.query(Recipe).filter(
            Recipe.id.in_(request.recipe_ids),
            Recipe.user_id == current_user.id
        ).all()

        for recipe in recipes:
            recipe_names.append(recipe.name)
            if recipe.ingredients_json:
                ingredients = json.loads(recipe.ingredients_json)
                for ing in ingredients:
                    # Scale amounts
                    if request.scale_factor != 1.0:
                        num, unit = parse_amount(ing.get('amount', '1'))
                        ing['amount'] = f"{num * request.scale_factor:.1f} {unit}".strip()
                    all_ingredients.append(ing)

    # Load favorites (favorites reference recipes via recipe_id)
    if request.favorite_ids:
        favorites = db.query(Favorite).filter(
            Favorite.id.in_(request.favorite_ids),
            Favorite.user_id == current_user.id
        ).all()

        for fav in favorites:
            # Access recipe data through the relationship
            if fav.recipe:
                recipe_names.append(fav.recipe.name)
                if fav.recipe.ingredients_json:
                    ingredients = json.loads(fav.recipe.ingredients_json)
                    for ing in ingredients:
                        # Scale amounts
                        if request.scale_factor != 1.0:
                            num, unit = parse_amount(ing.get('amount', '1'))
                            ing['amount'] = f"{num * request.scale_factor:.1f} {unit}".strip()
                        all_ingredients.append(ing)

    # Combine and categorize
    items = combine_ingredients(all_ingredients)

    return ShoppingListResponse(
        items=items,
        total_items=len(items),
        recipes_included=recipe_names,
        created_at=datetime.utcnow()
    )


@router.post("/export/text")
def export_shopping_list_text(
    request: ShoppingListRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export shopping list as plain text file.
    """
    # Generate shopping list first
    shopping_list = generate_shopping_list(request, current_user, db)

    # Create text content
    lines = [
        "=" * 40,
        "SHOPPING LIST",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 40,
        "",
        f"Recipes: {', '.join(shopping_list.recipes_included)}",
        "",
        "-" * 40,
    ]

    current_category = None
    for item in shopping_list.items:
        if item.category != current_category:
            current_category = item.category
            lines.append("")
            lines.append(f"[ {current_category.upper()} ]")
            lines.append("")

        lines.append(f"  [ ] {item.amount} {item.name}")

    lines.append("")
    lines.append("-" * 40)
    lines.append(f"Total items: {shopping_list.total_items}")
    lines.append("")
    lines.append("Generated by KitchenHelper-AI")

    content = "\n".join(lines)

    return StreamingResponse(
        BytesIO(content.encode('utf-8')),
        media_type="text/plain",
        headers={
            "Content-Disposition": 'attachment; filename="shopping_list.txt"'
        }
    )


@router.post("/export/json")
def export_shopping_list_json(
    request: ShoppingListRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export shopping list as JSON file (for import into other apps).
    """
    shopping_list = generate_shopping_list(request, current_user, db)

    export_data = {
        "app": "KitchenHelper-AI",
        "version": "1.0",
        "created_at": datetime.utcnow().isoformat(),
        "recipes": shopping_list.recipes_included,
        "items": [
            {
                "name": item.name,
                "amount": item.amount,
                "category": item.category,
                "checked": item.checked
            }
            for item in shopping_list.items
        ]
    }

    content = json.dumps(export_data, indent=2, ensure_ascii=False)

    return StreamingResponse(
        BytesIO(content.encode('utf-8')),
        media_type="application/json",
        headers={
            "Content-Disposition": 'attachment; filename="shopping_list.json"'
        }
    )
