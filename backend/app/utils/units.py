# Unit-System für Mengenverwaltung

UNITS = {
    # Gewicht
    "g": {"name_de": "Gramm", "name_en": "grams", "category": "weight", "base_unit": "g"},
    "kg": {"name_de": "Kilogramm", "name_en": "kilograms", "category": "weight", "base_unit": "g", "factor": 1000},

    # Volumen
    "ml": {"name_de": "Milliliter", "name_en": "milliliters", "category": "volume", "base_unit": "ml"},
    "l": {"name_de": "Liter", "name_en": "liters", "category": "volume", "base_unit": "ml", "factor": 1000},

    # Kochmaße
    "tl": {"name_de": "Teelöffel", "name_en": "teaspoon", "category": "volume", "base_unit": "ml", "factor": 5},
    "el": {"name_de": "Esslöffel", "name_en": "tablespoon", "category": "volume", "base_unit": "ml", "factor": 15},
    "tasse": {"name_de": "Tasse", "name_en": "cup", "category": "volume", "base_unit": "ml", "factor": 250},

    # Stückzahl
    "stück": {"name_de": "Stück", "name_en": "pieces", "category": "count", "base_unit": "stück"},
    "stk": {"name_de": "Stück", "name_en": "pieces", "category": "count", "base_unit": "stück"},
    "bund": {"name_de": "Bund", "name_en": "bunch", "category": "count", "base_unit": "bund"},
    "prise": {"name_de": "Prise", "name_en": "pinch", "category": "count", "base_unit": "prise"},
}

def convert_to_base_unit(quantity: float, unit: str) -> tuple:
    """Konvertiert in Basis-Einheit (1.5kg → 1500g)"""
    unit_lower = unit.lower()

    if unit_lower not in UNITS:
        return quantity, unit

    unit_info = UNITS[unit_lower]
    base_unit = unit_info["base_unit"]
    factor = unit_info.get("factor", 1)

    return quantity * factor, base_unit

def get_unit_category(unit: str) -> str:
    """Gibt Kategorie zurück (weight/volume/count)"""
    unit_lower = unit.lower()
    if unit_lower in UNITS:
        return UNITS[unit_lower]["category"]
    return "unknown"
