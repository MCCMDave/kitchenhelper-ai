from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.utils.units import convert_to_base_unit, get_unit_category

async def reduce_ingredient_quantity(
    user_id: int,
    ingredient_name: str,
    used_quantity: float,
    used_unit: str,
    db: Session
):
    """Reduziert Zutatenmenge nach Rezeptnutzung"""

    # Finde Zutat (case-insensitive)
    ingredient = db.query(Ingredient).filter(
        Ingredient.user_id == user_id,
        Ingredient.name.ilike(f"%{ingredient_name}%")
    ).first()

    if not ingredient:
        return {"error": f"Zutat '{ingredient_name}' nicht gefunden", "status": "not_found"}

    if not ingredient.quantity or not ingredient.unit:
        return {"error": f"'{ingredient_name}' hat keine Mengenangabe", "status": "no_quantity"}

    # Konvertiere in Basis-Einheit
    current_qty, current_unit = convert_to_base_unit(ingredient.quantity, ingredient.unit)
    used_qty, used_unit_base = convert_to_base_unit(used_quantity, used_unit)

    # Prüfe Kategorie (g != ml)
    if current_unit != used_unit_base:
        return {"error": f"Einheiten nicht kompatibel: {current_unit} vs {used_unit_base}", "status": "unit_mismatch"}

    # Reduziere
    new_quantity = current_qty - used_qty

    if new_quantity <= 0:
        # Aufgebraucht → Löschen
        db.delete(ingredient)
        db.commit()
        return {
            "status": "deleted",
            "ingredient": ingredient_name,
            "message": f"{ingredient_name} aufgebraucht und entfernt"
        }
    else:
        # Menge reduzieren
        ingredient.quantity = new_quantity
        ingredient.unit = current_unit
        db.commit()
        return {
            "status": "reduced",
            "ingredient": ingredient_name,
            "old_quantity": f"{current_qty} {current_unit}",
            "new_quantity": f"{new_quantity} {current_unit}",
            "message": f"{ingredient_name}: {new_quantity} {current_unit} übrig"
        }
