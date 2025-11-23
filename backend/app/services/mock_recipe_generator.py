"""
Mock Recipe Generator - 100% free!
Generates recipes based on templates WITHOUT API calls
"""
import random
from typing import List, Dict

class MockRecipeGenerator:
    """Mock Recipe Generator with Templates"""

    TEMPLATES_EN = {
        "pasta": {
            "name": "Mediterranean Pasta with {ingredient1}",
            "description": "Quick and delicious pasta with fresh ingredients. Perfect for a weeknight dinner!",
            "difficulty": 2,
            "cooking_time": "25 min",
            "method": "Pan",
            "ingredients": [
                {"name": "Whole grain pasta", "amount": "200g", "carbs": 60},
                {"name": "{ingredient1}", "amount": "300g", "carbs": 9},
                {"name": "Olive oil", "amount": "2 tbsp", "carbs": 0},
                {"name": "Garlic", "amount": "2 cloves", "carbs": 2},
                {"name": "Salt & pepper", "amount": "to taste", "carbs": 0},
            ],
            "nutrition": {"calories": 450, "protein": 15, "carbs": 71, "fat": 12},
            "leftover_tip": "Leftover {ingredient1} can be used for salad or smoothie."
        },
        "salad": {
            "name": "Fresh {ingredient1} Salad with Chicken",
            "description": "Light and protein-rich salad - ideal for low-carb!",
            "difficulty": 1,
            "cooking_time": "15 min",
            "method": "Chopping",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "200g", "carbs": 6},
                {"name": "Chicken breast", "amount": "150g", "carbs": 0},
                {"name": "Cucumber", "amount": "1 piece", "carbs": 4},
                {"name": "Olive oil", "amount": "2 tbsp", "carbs": 0},
                {"name": "Lemon juice", "amount": "1 tbsp", "carbs": 1},
            ],
            "nutrition": {"calories": 320, "protein": 35, "carbs": 11, "fat": 15},
            "leftover_tip": "Leftover {ingredient1} stays fresh in the fridge for 2-3 days."
        },
        "soup": {
            "name": "Creamy {ingredient1} Soup",
            "description": "Warming soup with lots of vegetables - perfect for cold days!",
            "difficulty": 2,
            "cooking_time": "35 min",
            "method": "Pot",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "400g", "carbs": 20},
                {"name": "Potatoes", "amount": "200g", "carbs": 30},
                {"name": "Vegetable broth", "amount": "500ml", "carbs": 2},
                {"name": "Cream", "amount": "100ml", "carbs": 4},
                {"name": "Onions", "amount": "1 piece", "carbs": 8},
            ],
            "nutrition": {"calories": 280, "protein": 8, "carbs": 32, "fat": 14},
            "leftover_tip": "Soup freezes well for up to 3 months."
        },
        "stirfry": {
            "name": "Asian Stir-Fry with {ingredient1}",
            "description": "Quick pan dish Asian-style - crispy and healthy!",
            "difficulty": 2,
            "cooking_time": "20 min",
            "method": "Wok/Pan",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "250g", "carbs": 12},
                {"name": "Bell pepper", "amount": "1 piece", "carbs": 6},
                {"name": "Soy sauce", "amount": "3 tbsp", "carbs": 3},
                {"name": "Ginger", "amount": "1 piece", "carbs": 1},
                {"name": "Rice", "amount": "150g", "carbs": 45},
            ],
            "nutrition": {"calories": 380, "protein": 12, "carbs": 67, "fat": 8},
            "leftover_tip": "Leftover stir-fry makes a great lunch the next day."
        },
        "bake": {
            "name": "Baked {ingredient1} Gratin",
            "description": "Hearty casserole topped with cheese - comfort food deluxe!",
            "difficulty": 3,
            "cooking_time": "45 min",
            "method": "Oven",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "400g", "carbs": 20},
                {"name": "Cheese", "amount": "150g", "carbs": 2},
                {"name": "Cream", "amount": "200ml", "carbs": 8},
                {"name": "Nutmeg", "amount": "1 pinch", "carbs": 0},
                {"name": "Butter", "amount": "30g", "carbs": 0},
            ],
            "nutrition": {"calories": 520, "protein": 22, "carbs": 30, "fat": 38},
            "leftover_tip": "Reheat in oven at 180C for 15 minutes."
        },
    }

    TEMPLATES_DE = {
        "pasta": {
            "name": "Mediterrane Pasta mit {ingredient1}",
            "description": "Schnelle und leckere Pasta mit frischen Zutaten. Perfekt fuer den Feierabend!",
            "difficulty": 2,
            "cooking_time": "25 Min",
            "method": "Pfanne",
            "ingredients": [
                {"name": "Vollkornnudeln", "amount": "200g", "carbs": 60},
                {"name": "{ingredient1}", "amount": "300g", "carbs": 9},
                {"name": "Olivenoel", "amount": "2 EL", "carbs": 0},
                {"name": "Knoblauch", "amount": "2 Zehen", "carbs": 2},
                {"name": "Salz & Pfeffer", "amount": "nach Geschmack", "carbs": 0},
            ],
            "nutrition": {"calories": 450, "protein": 15, "carbs": 71, "fat": 12},
            "leftover_tip": "Uebrige {ingredient1} koennen fuer Salat oder Smoothie verwendet werden."
        },
        "salad": {
            "name": "Frischer {ingredient1}-Salat mit Haehnchen",
            "description": "Leichter und proteinreicher Salat - ideal fuer Low-Carb!",
            "difficulty": 1,
            "cooking_time": "15 Min",
            "method": "Schneiden",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "200g", "carbs": 6},
                {"name": "Haehnchenbrust", "amount": "150g", "carbs": 0},
                {"name": "Gurke", "amount": "1 Stueck", "carbs": 4},
                {"name": "Olivenoel", "amount": "2 EL", "carbs": 0},
                {"name": "Zitronensaft", "amount": "1 EL", "carbs": 1},
            ],
            "nutrition": {"calories": 320, "protein": 35, "carbs": 11, "fat": 15},
            "leftover_tip": "Uebrige {ingredient1} bleiben im Kuehlschrank 2-3 Tage frisch."
        },
        "soup": {
            "name": "Cremige {ingredient1}-Suppe",
            "description": "Waermende Suppe mit viel Gemuese - perfekt fuer kalte Tage!",
            "difficulty": 2,
            "cooking_time": "35 Min",
            "method": "Topf",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "400g", "carbs": 20},
                {"name": "Kartoffeln", "amount": "200g", "carbs": 30},
                {"name": "Gemuesebruehe", "amount": "500ml", "carbs": 2},
                {"name": "Sahne", "amount": "100ml", "carbs": 4},
                {"name": "Zwiebeln", "amount": "1 Stueck", "carbs": 8},
            ],
            "nutrition": {"calories": 280, "protein": 8, "carbs": 32, "fat": 14},
            "leftover_tip": "Suppe laesst sich gut einfrieren (bis zu 3 Monate)."
        },
        "stirfry": {
            "name": "Asiatisches Wok-Gemuese mit {ingredient1}",
            "description": "Schnelles Pfannengericht im Asia-Style - knackig und gesund!",
            "difficulty": 2,
            "cooking_time": "20 Min",
            "method": "Wok/Pfanne",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "250g", "carbs": 12},
                {"name": "Paprika", "amount": "1 Stueck", "carbs": 6},
                {"name": "Sojasauce", "amount": "3 EL", "carbs": 3},
                {"name": "Ingwer", "amount": "1 Stueck", "carbs": 1},
                {"name": "Reis", "amount": "150g", "carbs": 45},
            ],
            "nutrition": {"calories": 380, "protein": 12, "carbs": 67, "fat": 8},
            "leftover_tip": "Reste eignen sich perfekt als Mittagessen am naechsten Tag."
        },
        "bake": {
            "name": "Ueberbackenes {ingredient1}-Gratin",
            "description": "Herzhafter Auflauf mit Kaese ueberbacken - Comfort Food deluxe!",
            "difficulty": 3,
            "cooking_time": "45 Min",
            "method": "Ofen",
            "ingredients": [
                {"name": "{ingredient1}", "amount": "400g", "carbs": 20},
                {"name": "Kaese", "amount": "150g", "carbs": 2},
                {"name": "Sahne", "amount": "200ml", "carbs": 8},
                {"name": "Muskatnuss", "amount": "1 Prise", "carbs": 0},
                {"name": "Butter", "amount": "30g", "carbs": 0},
            ],
            "nutrition": {"calories": 520, "protein": 22, "carbs": 30, "fat": 38},
            "leftover_tip": "Im Ofen bei 180 Grad 15 Minuten aufwaermen."
        },
    }

    def generate_recipes(
        self,
        ingredients: List[str],
        count: int = 3,
        servings: int = 2,
        diet_profiles: List[str] = None,
        diabetes_unit: str = "KE",
        language: str = "en"
    ) -> List[Dict]:
        """
        Generate mock recipes based on ingredients

        Args:
            ingredients: List of ingredient names
            count: Number of recipes
            servings: Portions
            diet_profiles: Diet profiles
            diabetes_unit: "KE" or "BE" - only this unit is calculated
            language: "en" or "de"

        Returns:
            List of recipe dictionaries
        """
        recipes = []
        templates = self.TEMPLATES_EN if language == "en" else self.TEMPLATES_DE
        template_keys = list(templates.keys())

        # Select random templates
        selected_templates = random.sample(template_keys, min(count, len(template_keys)))

        for template_key in selected_templates:
            template = templates[template_key].copy()

            # Choose main ingredient
            main_ingredient = random.choice(ingredients) if ingredients else ("Vegetables" if language == "en" else "Gemuese")

            # Replace placeholders
            recipe = {
                "name": template["name"].replace("{ingredient1}", main_ingredient),
                "description": template["description"],
                "difficulty": template["difficulty"],
                "cooking_time": template["cooking_time"],
                "method": template["method"],
                "servings": servings,
                "used_ingredients": [main_ingredient],
                "leftover_tips": template.get("leftover_tip", "").replace("{ingredient1}", main_ingredient),
                "ingredients": [],
                "nutrition_per_serving": {},
                "ai_provider": "mock"
            }

            # Copy and adjust ingredients
            for ing in template["ingredients"]:
                ingredient_copy = ing.copy()
                ingredient_copy["name"] = ingredient_copy["name"].replace("{ingredient1}", main_ingredient)
                recipe["ingredients"].append(ingredient_copy)

            # Calculate nutrition
            nutrition = template["nutrition"].copy()
            carbs_per_serving = nutrition["carbs"]

            # Only calculate chosen unit (KE or BE)
            if diabetes_unit == "BE":
                nutrition["be"] = round(carbs_per_serving / 12, 1)
                nutrition["ke"] = None
            else:
                nutrition["ke"] = round(carbs_per_serving / 10, 1)
                nutrition["be"] = None

            recipe["nutrition_per_serving"] = nutrition
            recipes.append(recipe)

        return recipes

# Singleton Instance
mock_generator = MockRecipeGenerator()
