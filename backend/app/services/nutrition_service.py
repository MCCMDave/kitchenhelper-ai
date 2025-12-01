# Nutrition Service - OpenFoodFacts API Integration
import httpx
from typing import Optional, Dict, Any, List
import re


class NutritionService:
    """
    Service for fetching real nutrition data from OpenFoodFacts API.
    Free, open-source database with millions of food products.
    """

    BASE_URL = "https://world.openfoodfacts.org"
    SEARCH_URL = f"{BASE_URL}/cgi/search.pl"

    # Fallback nutrition values per 100g for common ingredients
    FALLBACK_NUTRITION = {
        # Vegetables (per 100g)
        'tomato': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2},
        'tomate': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2},
        'potato': {'calories': 77, 'protein': 2.0, 'carbs': 17.0, 'fat': 0.1, 'fiber': 2.2},
        'kartoffel': {'calories': 77, 'protein': 2.0, 'carbs': 17.0, 'fat': 0.1, 'fiber': 2.2},
        'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 10.0, 'fat': 0.2, 'fiber': 2.8},
        'karotte': {'calories': 41, 'protein': 0.9, 'carbs': 10.0, 'fat': 0.2, 'fiber': 2.8},
        'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7},
        'zwiebel': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7},
        'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 7.0, 'fat': 0.4, 'fiber': 2.6},
        'brokkoli': {'calories': 34, 'protein': 2.8, 'carbs': 7.0, 'fat': 0.4, 'fiber': 2.6},
        'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2},
        'spinat': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2},
        'pepper': {'calories': 31, 'protein': 1.0, 'carbs': 6.0, 'fat': 0.3, 'fiber': 2.1},
        'paprika': {'calories': 31, 'protein': 1.0, 'carbs': 6.0, 'fat': 0.3, 'fiber': 2.1},
        'cucumber': {'calories': 15, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5},
        'gurke': {'calories': 15, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5},
        'zucchini': {'calories': 17, 'protein': 1.2, 'carbs': 3.1, 'fat': 0.3, 'fiber': 1.0},
        'mushroom': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3, 'fiber': 1.0},
        'pilze': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3, 'fiber': 1.0},
        'champignon': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3, 'fiber': 1.0},

        # Meat (per 100g)
        'chicken': {'calories': 165, 'protein': 31.0, 'carbs': 0.0, 'fat': 3.6, 'fiber': 0.0},
        'haehnchen': {'calories': 165, 'protein': 31.0, 'carbs': 0.0, 'fat': 3.6, 'fiber': 0.0},
        'hahnchen': {'calories': 165, 'protein': 31.0, 'carbs': 0.0, 'fat': 3.6, 'fiber': 0.0},
        'beef': {'calories': 250, 'protein': 26.0, 'carbs': 0.0, 'fat': 15.0, 'fiber': 0.0},
        'rind': {'calories': 250, 'protein': 26.0, 'carbs': 0.0, 'fat': 15.0, 'fiber': 0.0},
        'pork': {'calories': 242, 'protein': 27.0, 'carbs': 0.0, 'fat': 14.0, 'fiber': 0.0},
        'schwein': {'calories': 242, 'protein': 27.0, 'carbs': 0.0, 'fat': 14.0, 'fiber': 0.0},
        'salmon': {'calories': 208, 'protein': 20.0, 'carbs': 0.0, 'fat': 13.0, 'fiber': 0.0},
        'lachs': {'calories': 208, 'protein': 20.0, 'carbs': 0.0, 'fat': 13.0, 'fiber': 0.0},
        'egg': {'calories': 155, 'protein': 13.0, 'carbs': 1.1, 'fat': 11.0, 'fiber': 0.0},
        'ei': {'calories': 155, 'protein': 13.0, 'carbs': 1.1, 'fat': 11.0, 'fiber': 0.0},
        'eier': {'calories': 155, 'protein': 13.0, 'carbs': 1.1, 'fat': 11.0, 'fiber': 0.0},

        # Dairy (per 100g)
        'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5.0, 'fat': 1.0, 'fiber': 0.0},
        'milch': {'calories': 42, 'protein': 3.4, 'carbs': 5.0, 'fat': 1.0, 'fiber': 0.0},
        'cheese': {'calories': 402, 'protein': 25.0, 'carbs': 1.3, 'fat': 33.0, 'fiber': 0.0},
        'kaese': {'calories': 402, 'protein': 25.0, 'carbs': 1.3, 'fat': 33.0, 'fiber': 0.0},
        'butter': {'calories': 717, 'protein': 0.9, 'carbs': 0.1, 'fat': 81.0, 'fiber': 0.0},
        'cream': {'calories': 340, 'protein': 2.1, 'carbs': 2.8, 'fat': 37.0, 'fiber': 0.0},
        'sahne': {'calories': 340, 'protein': 2.1, 'carbs': 2.8, 'fat': 37.0, 'fiber': 0.0},
        'yogurt': {'calories': 59, 'protein': 10.0, 'carbs': 3.6, 'fat': 0.7, 'fiber': 0.0},
        'joghurt': {'calories': 59, 'protein': 10.0, 'carbs': 3.6, 'fat': 0.7, 'fiber': 0.0},

        # Carbs (per 100g)
        'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28.0, 'fat': 0.3, 'fiber': 0.4},
        'reis': {'calories': 130, 'protein': 2.7, 'carbs': 28.0, 'fat': 0.3, 'fiber': 0.4},
        'pasta': {'calories': 131, 'protein': 5.0, 'carbs': 25.0, 'fat': 1.1, 'fiber': 1.8},
        'nudeln': {'calories': 131, 'protein': 5.0, 'carbs': 25.0, 'fat': 1.1, 'fiber': 1.8},
        'spaghetti': {'calories': 131, 'protein': 5.0, 'carbs': 25.0, 'fat': 1.1, 'fiber': 1.8},
        'bread': {'calories': 265, 'protein': 9.0, 'carbs': 49.0, 'fat': 3.2, 'fiber': 2.7},
        'brot': {'calories': 265, 'protein': 9.0, 'carbs': 49.0, 'fat': 3.2, 'fiber': 2.7},
        'flour': {'calories': 364, 'protein': 10.0, 'carbs': 76.0, 'fat': 1.0, 'fiber': 2.7},
        'mehl': {'calories': 364, 'protein': 10.0, 'carbs': 76.0, 'fat': 1.0, 'fiber': 2.7},

        # Fruits (per 100g)
        'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14.0, 'fat': 0.2, 'fiber': 2.4},
        'apfel': {'calories': 52, 'protein': 0.3, 'carbs': 14.0, 'fat': 0.2, 'fiber': 2.4},
        'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23.0, 'fat': 0.3, 'fiber': 2.6},
        'banane': {'calories': 89, 'protein': 1.1, 'carbs': 23.0, 'fat': 0.3, 'fiber': 2.6},
        'orange': {'calories': 47, 'protein': 0.9, 'carbs': 12.0, 'fat': 0.1, 'fiber': 2.4},
        'lemon': {'calories': 29, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.3, 'fiber': 2.8},
        'zitrone': {'calories': 29, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.3, 'fiber': 2.8},

        # Oils & Fats (per 100g)
        'oil': {'calories': 884, 'protein': 0.0, 'carbs': 0.0, 'fat': 100.0, 'fiber': 0.0},
        'oel': {'calories': 884, 'protein': 0.0, 'carbs': 0.0, 'fat': 100.0, 'fiber': 0.0},
        'olivenoel': {'calories': 884, 'protein': 0.0, 'carbs': 0.0, 'fat': 100.0, 'fiber': 0.0},

        # Spices & Herbs (per 100g - typically used in small amounts)
        'salt': {'calories': 0, 'protein': 0.0, 'carbs': 0.0, 'fat': 0.0, 'fiber': 0.0},
        'salz': {'calories': 0, 'protein': 0.0, 'carbs': 0.0, 'fat': 0.0, 'fiber': 0.0},
        'pepper': {'calories': 251, 'protein': 10.0, 'carbs': 64.0, 'fat': 3.3, 'fiber': 25.0},
        'pfeffer': {'calories': 251, 'protein': 10.0, 'carbs': 64.0, 'fat': 3.3, 'fiber': 25.0},
        'garlic': {'calories': 149, 'protein': 6.4, 'carbs': 33.0, 'fat': 0.5, 'fiber': 2.1},
        'knoblauch': {'calories': 149, 'protein': 6.4, 'carbs': 33.0, 'fat': 0.5, 'fiber': 2.1},

        # Default fallback
        'default': {'calories': 100, 'protein': 5.0, 'carbs': 15.0, 'fat': 3.0, 'fiber': 2.0},
    }

    def __init__(self):
        pass  # No persistent client needed - async methods create their own

    async def search_product(self, query: str, language: str = "de") -> Optional[Dict[str, Any]]:
        """
        Search for a product in OpenFoodFacts database.

        Args:
            query: Product name to search
            language: Language code (de, en, etc.)

        Returns:
            Product data dict or None if not found
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                params = {
                    "search_terms": query,
                    "search_simple": 1,
                    "action": "process",
                    "json": 1,
                    "page_size": 5,
                    "lc": language
                }

                response = await client.get(self.SEARCH_URL, params=params)

                if response.status_code == 200:
                    data = response.json()
                    products = data.get("products", [])

                    if products:
                        # Return first product with nutrition data
                        for product in products:
                            if product.get("nutriments"):
                                return self._extract_nutrition(product)

                return None

        except Exception as e:
            print(f"[NutritionService] Error searching product: {e}")
            return None

    def _extract_nutrition(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Extract nutrition info from OpenFoodFacts product data"""
        nutriments = product.get("nutriments", {})

        return {
            "name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", ""),
            "calories": nutriments.get("energy-kcal_100g", 0),
            "protein": nutriments.get("proteins_100g", 0),
            "carbs": nutriments.get("carbohydrates_100g", 0),
            "fat": nutriments.get("fat_100g", 0),
            "fiber": nutriments.get("fiber_100g", 0),
            "sugar": nutriments.get("sugars_100g", 0),
            "sodium": nutriments.get("sodium_100g", 0),
            "per": "100g",
            "source": "OpenFoodFacts",
            "image_url": product.get("image_front_small_url", "")
        }

    def get_nutrition_sync(self, ingredient_name: str) -> Dict[str, Any]:
        """
        Get nutrition data synchronously (for mock generator).
        Uses fallback database if API fails.

        Args:
            ingredient_name: Name of the ingredient

        Returns:
            Nutrition data dict
        """
        normalized = ingredient_name.lower().strip()

        # Remove common prefixes/suffixes
        normalized = re.sub(r'^\d+\s*(g|kg|ml|l|stueck|stück)?\s*', '', normalized)
        normalized = re.sub(r'\s*(frisch|gehackt|gewürfelt|geschnitten)$', '', normalized)

        # Check fallback database first (faster)
        for key, nutrition in self.FALLBACK_NUTRITION.items():
            if key in normalized or normalized in key:
                return {
                    **nutrition,
                    "name": ingredient_name,
                    "per": "100g",
                    "source": "fallback_database"
                }

        # Try OpenFoodFacts API (sync)
        try:
            params = {
                "search_terms": ingredient_name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 1,
            }

            # Create sync client for this call
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.SEARCH_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])

                if products and products[0].get("nutriments"):
                    return self._extract_nutrition(products[0])

        except Exception as e:
            print(f"[NutritionService] API error for '{ingredient_name}': {e}")

        # Return default fallback
        return {
            **self.FALLBACK_NUTRITION['default'],
            "name": ingredient_name,
            "per": "100g",
            "source": "estimated"
        }

    def calculate_recipe_nutrition(
        self,
        ingredients: List[Dict[str, Any]],
        servings: int = 2
    ) -> Dict[str, Any]:
        """
        Calculate total nutrition for a recipe based on ingredients.

        Args:
            ingredients: List of dicts with 'name' and 'amount'
            servings: Number of servings

        Returns:
            Nutrition per serving
        """
        total = {
            "calories": 0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0,
            "fiber": 0.0
        }

        for ingredient in ingredients:
            name = ingredient.get("name", "")
            amount_str = ingredient.get("amount", "100g")

            # Parse amount (extract number)
            amount_match = re.search(r'(\d+(?:\.\d+)?)', amount_str)
            amount_g = float(amount_match.group(1)) if amount_match else 100

            # Adjust for common units
            if 'kg' in amount_str.lower():
                amount_g *= 1000
            elif 'ml' in amount_str.lower() or 'l' in amount_str.lower():
                # Assume 1ml ≈ 1g for liquids
                if 'l' in amount_str.lower() and 'ml' not in amount_str.lower():
                    amount_g *= 1000
            elif 'el' in amount_str.lower() or 'tbsp' in amount_str.lower():
                amount_g = float(amount_match.group(1)) * 15 if amount_match else 15
            elif 'tl' in amount_str.lower() or 'tsp' in amount_str.lower():
                amount_g = float(amount_match.group(1)) * 5 if amount_match else 5
            elif 'stueck' in amount_str.lower() or 'stück' in amount_str.lower():
                # Estimate piece weights
                if 'ei' in name.lower():
                    amount_g = float(amount_match.group(1)) * 60 if amount_match else 60
                else:
                    amount_g = float(amount_match.group(1)) * 100 if amount_match else 100

            # Get nutrition per 100g
            nutrition = self.get_nutrition_sync(name)

            # Scale to actual amount
            factor = amount_g / 100

            total["calories"] += int(nutrition.get("calories", 0) * factor)
            total["protein"] += nutrition.get("protein", 0) * factor
            total["carbs"] += nutrition.get("carbs", 0) * factor
            total["fat"] += nutrition.get("fat", 0) * factor
            total["fiber"] += nutrition.get("fiber", 0) * factor

        # Calculate per serving
        per_serving = {
            "calories": int(total["calories"] / servings),
            "protein": round(total["protein"] / servings, 1),
            "carbs": round(total["carbs"] / servings, 1),
            "fat": round(total["fat"] / servings, 1),
            "fiber": round(total["fiber"] / servings, 1),
            # Calculate KE/BE (1 KE = 10g carbs, 1 BE = 12g carbs)
            "ke": round((total["carbs"] / servings) / 10, 1),
            "be": round((total["carbs"] / servings) / 12, 1),
        }

        return per_serving


# Global instance
nutrition_service = NutritionService()
