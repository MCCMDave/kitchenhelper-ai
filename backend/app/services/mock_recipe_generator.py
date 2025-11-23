"""
Mock Recipe Generator - 100% kostenlos!
Generiert Rezepte basierend auf Templates OHNE API-Calls
"""
import random
from typing import List, Dict

class MockRecipeGenerator:
    """Mock-Rezepte Generator mit Templates"""
    
    # Rezept-Templates
    TEMPLATES = {
        "pasta": {
            "name": "Mediterrane Pasta mit {ingredient1}",
            "description": "Schnelle und leckere Pasta mit frischen Zutaten. Perfekt für den Feierabend!",
            "difficulty": 2,
            "cooking_time": "25 Min",
            "method": "Pfanne",
            "ingredients": [
                {"name": "Vollkornnudeln", "amount": "200g", "carbs": 60},
                {"name": "{ingredient1}", "amount": "300g", "carbs": 9},
                {"name": "Olivenöl", "amount": "2 EL", "carbs": 0},
                {"name": "Knoblauch", "amount": "2 Zehen", "carbs": 2},
                {"name": "Salz & Pfeffer", "amount": "nach Geschmack", "carbs": 0},
            ],
            "nutrition": {"calories": 450, "protein": 15, "carbs": 71, "fat": 12},
        },
        "salad": {
            "name": "Frischer {ingredient1}-Salat mit Hähnchen",
            "description": "Leichter und proteinreicher Salat - ideal für Low-Carb!",
            "difficulty": 1,
            "cooking_time": "15 Min",
            "method": "Schneiden",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "200g", "carbs": 6},
                {"name": "Hähnchenbrust", "amount": "150g", "carbs": 0},
                {"name": "Gurke", "amount": "1 Stück", "carbs": 4},
                {"name": "Olivenöl", "amount": "2 EL", "carbs": 0},
                {"name": "Zitronensaft", "amount": "1 EL", "carbs": 1},
            ],
            "nutrition": {"calories": 320, "protein": 35, "carbs": 11, "fat": 15},
        },
        "soup": {
            "name": "Cremige {ingredient1}-Suppe",
            "description": "Wärmende Suppe mit viel Gemüse - perfekt für kalte Tage!",
            "difficulty": 2,
            "cooking_time": "35 Min",
            "method": "Topf",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "400g", "carbs": 20},
                {"name": "Kartoffeln", "amount": "200g", "carbs": 30},
                {"name": "Gemüsebrühe", "amount": "500ml", "carbs": 2},
                {"name": "Sahne", "amount": "100ml", "carbs": 4},
                {"name": "Zwiebeln", "amount": "1 Stück", "carbs": 8},
            ],
            "nutrition": {"calories": 280, "protein": 8, "carbs": 32, "fat": 14},
        },
        "stirfry": {
            "name": "Asiatisches Wok-Gemüse mit {ingredient1}",
            "description": "Schnelles Pfannengericht im Asia-Style - knackig und gesund!",
            "difficulty": 2,
            "cooking_time": "20 Min",
            "method": "Wok/Pfanne",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "250g", "carbs": 12},
                {"name": "Paprika", "amount": "1 Stück", "carbs": 6},
                {"name": "Sojasauce", "amount": "3 EL", "carbs": 3},
                {"name": "Ingwer", "amount": "1 Stück", "carbs": 1},
                {"name": "Reis", "amount": "150g", "carbs": 45},
            ],
            "nutrition": {"calories": 380, "protein": 12, "carbs": 67, "fat": 8},
        },
        "bake": {
            "name": "Überbackenes {ingredient1}-Gratin",
            "description": "Herzhafter Auflauf mit Käse überbacken - comfort food deluxe!",
            "difficulty": 3,
            "cooking_time": "45 Min",
            "method": "Ofen",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "400g", "carbs": 20},
                {"name": "Käse", "amount": "150g", "carbs": 2},
                {"name": "Sahne", "amount": "200ml", "carbs": 8},
                {"name": "Muskatnuss", "amount": "1 Prise", "carbs": 0},
                {"name": "Butter", "amount": "30g", "carbs": 0},
            ],
            "nutrition": {"calories": 520, "protein": 22, "carbs": 30, "fat": 38},
        },
    }
    
    def generate_recipes(
        self,
        ingredients: List[str],
        count: int = 3,
        servings: int = 2,
        diet_profiles: List[str] = None,
        diabetes_unit: str = "KE"
    ) -> List[Dict]:
        """
        Generiere Mock-Rezepte basierend auf Zutaten

        Args:
            ingredients: Liste von Zutatennamen
            count: Anzahl Rezepte
            servings: Portionen
            diet_profiles: Diaet-Profile
            diabetes_unit: "KE" oder "BE" - nur diese Einheit berechnen

        Returns:
            Liste von Rezept-Dictionaries
        """
        recipes = []
        template_keys = list(self.TEMPLATES.keys())

        # Waehle zufaellige Templates
        selected_templates = random.sample(template_keys, min(count, len(template_keys)))

        for template_key in selected_templates:
            template = self.TEMPLATES[template_key].copy()

            # Waehle Hauptzutat
            main_ingredient = random.choice(ingredients) if ingredients else "Gemuese"

            # Ersetze Platzhalter
            recipe = {
                "name": template["name"].replace("{ingredient1}", main_ingredient),
                "description": template["description"],
                "difficulty": template["difficulty"],
                "cooking_time": template["cooking_time"],
                "method": template["method"],
                "servings": servings,
                "used_ingredients": [main_ingredient],
                "leftover_tips": f"Uebrige {main_ingredient} koennen fuer Salat oder Smoothie verwendet werden.",
                "ingredients": [],
                "nutrition_per_serving": {},
                "ai_provider": "mock"
            }

            # Kopiere und passe Zutaten an
            for ing in template["ingredients"]:
                ingredient_copy = ing.copy()
                ingredient_copy["name"] = ingredient_copy["name"].replace("{ingredient1}", main_ingredient)
                recipe["ingredients"].append(ingredient_copy)

            # Naehrwerte berechnen
            nutrition = template["nutrition"].copy()
            carbs_per_serving = nutrition["carbs"]

            # Nur die gewaehlte Einheit berechnen (KE oder BE)
            # KE = Kohlenhydrate / 10, BE = Kohlenhydrate / 12
            if diabetes_unit == "BE":
                nutrition["be"] = round(carbs_per_serving / 12, 1)
                nutrition["ke"] = None  # Nicht berechnet
            else:  # Default: KE
                nutrition["ke"] = round(carbs_per_serving / 10, 1)
                nutrition["be"] = None  # Nicht berechnet

            recipe["nutrition_per_serving"] = nutrition

            recipes.append(recipe)

        return recipes

# Singleton Instance
mock_generator = MockRecipeGenerator()