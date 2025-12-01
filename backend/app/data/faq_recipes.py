"""
FAQ Recipe Prompts - Vorgefertigte Rezeptanfragen
10 häufige Kategorien für schnellen Zugriff
"""
from typing import List, Dict


FAQ_CATEGORIES: List[Dict] = [
    # === SNACKS (Low-KE for Diabetics) ===
    {
        "id": "snack-low-ke-1",
        "title_de": "Snack: Gemüse-Sticks (0,5 KE)",
        "title_en": "Snack: Veggie Sticks (0.5 KE)",
        "description_de": "Knackige Gemüse-Snacks, ideal für zwischendurch",
        "description_en": "Crunchy veggie snacks, perfect for in-between",
        "ingredients": ["Gurke", "Karotten", "Paprika", "Hummus"],
        "diet_profiles": ["diabetic", "low_carb", "vegan"],
        "servings": 1,
        "max_time": 5
    },
    {
        "id": "snack-low-ke-2",
        "title_de": "Snack: Käse-Würfel mit Nüssen (0,8 KE)",
        "title_en": "Snack: Cheese Cubes with Nuts (0.8 KE)",
        "description_de": "Proteinreicher Snack, sehr sättigend",
        "description_en": "High-protein snack, very filling",
        "ingredients": ["Käse", "Mandeln", "Walnüsse"],
        "diet_profiles": ["diabetic", "low_carb", "high_protein"],
        "servings": 1,
        "max_time": 3
    },
    {
        "id": "snack-low-ke-3",
        "title_de": "Snack: Beeren mit Joghurt (1,5 KE)",
        "title_en": "Snack: Berries with Yogurt (1.5 KE)",
        "description_de": "Fruchtig-frischer Snack, nicht zu süß",
        "description_en": "Fruity-fresh snack, not too sweet",
        "ingredients": ["Heidelbeeren", "Erdbeeren", "Naturjoghurt", "Zimt"],
        "diet_profiles": ["diabetic"],
        "servings": 1,
        "max_time": 5
    },
    {
        "id": "snack-low-ke-4",
        "title_de": "Snack: Hart gekochtes Ei (0 KE)",
        "title_en": "Snack: Hard Boiled Egg (0 KE)",
        "description_de": "Perfekter Protein-Snack ohne Kohlenhydrate",
        "description_en": "Perfect protein snack without carbs",
        "ingredients": ["Eier", "Salz", "Pfeffer"],
        "diet_profiles": ["diabetic", "low_carb", "high_protein", "keto"],
        "servings": 1,
        "max_time": 10
    },
    {
        "id": "snack-low-ke-5",
        "title_de": "Snack: Avocado-Happen (0,3 KE)",
        "title_en": "Snack: Avocado Bites (0.3 KE)",
        "description_de": "Gesunde Fette, lange Sättigung",
        "description_en": "Healthy fats, long-lasting satiety",
        "ingredients": ["Avocado", "Zitrone", "Salz", "Chili"],
        "diet_profiles": ["diabetic", "low_carb", "keto", "vegan"],
        "servings": 1,
        "max_time": 5
    },

    # === MAIN MEALS ===
    {
        "id": "quick-dinner-veg",
        "title_de": "Schnelles vegetarisches Abendessen",
        "title_en": "Quick Vegetarian Dinner",
        "description_de": "Gesundes vegetarisches Gericht in unter 30 Minuten",
        "description_en": "Healthy vegetarian meal in under 30 minutes",
        "ingredients": ["Tomaten", "Zwiebeln", "Knoblauch", "Olivenöl", "Pasta"],
        "diet_profiles": ["vegetarian"],
        "servings": 2,
        "max_time": 30
    },
    {
        "id": "quick-dinner-vegan",
        "title_de": "Schnelles veganes Abendessen",
        "title_en": "Quick Vegan Dinner",
        "description_de": "100% pflanzlich, schnell und lecker",
        "description_en": "100% plant-based, fast and delicious",
        "ingredients": ["Kichererbsen", "Spinat", "Kokosmilch", "Curry", "Reis"],
        "diet_profiles": ["vegan"],
        "servings": 2,
        "max_time": 30
    },
    {
        "id": "quick-dinner-meat",
        "title_de": "Schnelles Fleischgericht",
        "title_en": "Quick Meat Dish",
        "description_de": "Proteinreiches Abendessen mit Fleisch",
        "description_en": "High-protein dinner with meat",
        "ingredients": ["Hähnchenbrust", "Paprika", "Zwiebeln", "Sojasauce", "Reis"],
        "diet_profiles": [],
        "servings": 2,
        "max_time": 30
    },
    {
        "id": "diabetic-breakfast",
        "title_de": "Diabetes-freundliches Frühstück",
        "title_en": "Diabetic-Friendly Breakfast",
        "description_de": "Niedriger glykämischer Index, ausgewogen",
        "description_en": "Low glycemic index, balanced",
        "ingredients": ["Haferflocken", "Mandeln", "Beeren", "Joghurt", "Zimt"],
        "diet_profiles": ["diabetic", "low_carb"],
        "servings": 1,
        "max_time": 15
    },
    {
        "id": "diabetic-lunch",
        "title_de": "Diabetes-freundliches Mittagessen",
        "title_en": "Diabetic-Friendly Lunch",
        "description_de": "Ausgewogenes Mittagessen mit kontrollierten Kohlenhydraten",
        "description_en": "Balanced lunch with controlled carbs",
        "ingredients": ["Lachs", "Brokkoli", "Quinoa", "Zitrone", "Olivenöl"],
        "diet_profiles": ["diabetic"],
        "servings": 2,
        "max_time": 40
    },
    {
        "id": "low-carb",
        "title_de": "Low-Carb Gericht",
        "title_en": "Low-Carb Meal",
        "description_de": "Wenig Kohlenhydrate, viel Protein",
        "description_en": "Low carbs, high protein",
        "ingredients": ["Hähnchen", "Zucchini", "Paprika", "Feta", "Olivenöl"],
        "diet_profiles": ["low_carb"],
        "servings": 2,
        "max_time": 35
    },
    {
        "id": "high-protein",
        "title_de": "Proteinreiches Gericht",
        "title_en": "High-Protein Meal",
        "description_de": "Ideal nach dem Sport, viel Eiweiß",
        "description_en": "Perfect post-workout, high in protein",
        "ingredients": ["Rindfleisch", "Eier", "Quark", "Linsen", "Spinat"],
        "diet_profiles": ["high_protein"],
        "servings": 2,
        "max_time": 40
    },
    {
        "id": "family-friendly",
        "title_de": "Familienfreundlich (Kinder)",
        "title_en": "Family-Friendly (Kids)",
        "description_de": "Kinderfreundlich, einfach, lecker",
        "description_en": "Kid-approved, simple, delicious",
        "ingredients": ["Kartoffeln", "Karotten", "Erbsen", "Hähnchen", "Käse"],
        "diet_profiles": [],
        "servings": 4,
        "max_time": 45
    },
    {
        "id": "budget-friendly",
        "title_de": "Budget-freundlich",
        "title_en": "Budget-Friendly",
        "description_de": "Günstig, einfach, sättigend",
        "description_en": "Affordable, simple, filling",
        "ingredients": ["Nudeln", "Tomaten", "Zwiebeln", "Ei", "Parmesan"],
        "diet_profiles": [],
        "servings": 4,
        "max_time": 30
    },
    {
        "id": "meal-prep",
        "title_de": "Meal Prep (Wochenvorbereitung)",
        "title_en": "Meal Prep (Weekly)",
        "description_de": "Gut vorzubereiten, haltbar, portionierbar",
        "description_en": "Easy to prep, keeps well, portionable",
        "ingredients": ["Reis", "Hähnchen", "Brokkoli", "Süßkartoffeln", "Olivenöl"],
        "diet_profiles": [],
        "servings": 5,
        "max_time": 60
    }
]


def get_faq_category(category_id: str, language: str = "en") -> Dict:
    """
    Get FAQ category by ID
    Returns category with localized title/description
    """
    for category in FAQ_CATEGORIES:
        if category["id"] == category_id:
            title_key = f"title_{language}"
            desc_key = f"description_{language}"

            return {
                "id": category["id"],
                "title": category.get(title_key, category["title_en"]),
                "description": category.get(desc_key, category["description_en"]),
                "ingredients": category["ingredients"],
                "diet_profiles": category["diet_profiles"],
                "servings": category["servings"]
            }

    return None


def get_all_faq_categories(language: str = "en") -> List[Dict]:
    """
    Get all FAQ categories with localized titles/descriptions
    """
    result = []
    for category in FAQ_CATEGORIES:
        title_key = f"title_{language}"
        desc_key = f"description_{language}"

        result.append({
            "id": category["id"],
            "title": category.get(title_key, category["title_en"]),
            "description": category.get(desc_key, category["description_en"]),
            "servings": category["servings"]
        })

    return result
