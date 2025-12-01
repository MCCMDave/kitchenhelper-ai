"""
AI Recipe Generator with Gemini (Pro) and Ollama (Free) Support
- Pro users: Fast Gemini API with Ollama fallback
- Free users: Local Ollama (cost-free, privacy-friendly)
"""
import os
import logging
from typing import List, Dict, Optional
import requests
import json

logger = logging.getLogger(__name__)


class AIRecipeGenerator:
    """Intelligenter Recipe Generator mit Tier-basierter AI-Auswahl"""

    def __init__(self):
        # API Keys
        self.gemini_api_key = os.getenv("GOOGLE_AI_API_KEY")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Model Configuration
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")

        # Check availability
        self.gemini_available = bool(self.gemini_api_key)
        self.ollama_available = self._check_ollama_available()

        logger.info(f"AI Generator initialized - Gemini: {self.gemini_available}, Ollama: {self.ollama_available}")

    def _check_ollama_available(self) -> bool:
        """Check if Ollama server is reachable"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False

    def generate_recipes(
        self,
        ingredients: List[str],
        count: int = 3,
        servings: int = 2,
        diet_profiles: List[str] = None,
        diabetes_unit: str = "KE",
        language: str = "en",
        user_tier: str = "free"
    ) -> List[Dict]:
        """
        Generate recipes using appropriate AI provider based on user tier

        Args:
            ingredients: List of available ingredients
            count: Number of recipes to generate
            servings: Number of servings per recipe
            diet_profiles: Dietary restrictions (vegan, gluten-free, etc.)
            diabetes_unit: "KE" or "BE"
            language: "en" or "de"
            user_tier: "free" or "pro"

        Returns:
            List of recipe dictionaries
        """
        # Pro users: Try Gemini first, fallback to Ollama
        if user_tier == "pro":
            if self.gemini_available:
                try:
                    logger.info("Pro user - Using Gemini API")
                    return self._generate_with_gemini(
                        ingredients, count, servings, diet_profiles, diabetes_unit, language
                    )
                except Exception as e:
                    logger.error(f"Gemini failed: {e} - Falling back to Ollama")
                    if self.ollama_available:
                        return self._generate_with_ollama(
                            ingredients, count, servings, diet_profiles, diabetes_unit, language
                        )
                    else:
                        raise Exception("Both Gemini and Ollama unavailable")
            elif self.ollama_available:
                logger.warning("Pro user but Gemini not configured - Using Ollama")
                return self._generate_with_ollama(
                    ingredients, count, servings, diet_profiles, diabetes_unit, language
                )
            else:
                raise Exception("No AI provider available")

        # Free users: Ollama only
        else:
            if self.ollama_available:
                logger.info("Free user - Using Ollama")
                return self._generate_with_ollama(
                    ingredients, count, servings, diet_profiles, diabetes_unit, language
                )
            else:
                raise Exception("Ollama not available")

    def _generate_with_gemini(
        self,
        ingredients: List[str],
        count: int,
        servings: int,
        diet_profiles: Optional[List[str]],
        diabetes_unit: str,
        language: str
    ) -> List[Dict]:
        """Generate recipes using Gemini API"""
        prompt = self._build_prompt(ingredients, count, servings, diet_profiles, diabetes_unit, language)

        # Gemini API Request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.gemini_api_key}

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
            }
        }

        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        response.raise_for_status()

        # Parse response
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # Extract JSON from markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        recipes = json.loads(text)

        # Add AI provider info
        for recipe in recipes:
            recipe["ai_provider"] = "gemini"

        return recipes

    def _generate_with_ollama(
        self,
        ingredients: List[str],
        count: int,
        servings: int,
        diet_profiles: Optional[List[str]],
        diabetes_unit: str,
        language: str
    ) -> List[Dict]:
        """Generate recipes using local Ollama"""
        prompt = self._build_prompt(ingredients, count, servings, diet_profiles, diabetes_unit, language)

        # Ollama API Request
        url = f"{self.ollama_base_url}/api/generate"
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 2048,
            }
        }

        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()

        result = response.json()
        text = result["response"]

        # Extract JSON from markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        recipes = json.loads(text)

        # Add AI provider info
        for recipe in recipes:
            recipe["ai_provider"] = "ollama"

        return recipes

    def generate_with_streaming(
        self,
        ingredients: List[str],
        count: int,
        servings: int,
        diet_profiles: Optional[List[str]],
        diabetes_unit: str,
        language: str,
        user_tier: str = "free"
    ):
        """
        Stream recipe generation tokens in real-time (SSE-compatible)
        Yields text chunks as they arrive from Ollama

        NOTE: Gemini API doesn't support streaming in the same way,
        so this is Ollama-only for now. Pro users get fast non-streamed Gemini.
        """
        prompt = self._build_prompt(ingredients, count, servings, diet_profiles, diabetes_unit, language)

        # Ollama API Request with streaming
        url = f"{self.ollama_base_url}/api/generate"
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": True,  # Enable streaming!
            "options": {
                "temperature": 0.7,
                "num_predict": 2048,
            }
        }

        # Stream response
        response = requests.post(url, json=payload, stream=True, timeout=180)
        response.raise_for_status()

        # Yield chunks as they arrive
        full_text = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if "response" in chunk:
                    token = chunk["response"]
                    full_text += token
                    yield token

        # After streaming completes, parse and return final JSON
        # (This will be handled by the route, not yielded here)

    def _build_prompt(
        self,
        ingredients: List[str],
        count: int,
        servings: int,
        diet_profiles: Optional[List[str]],
        diabetes_unit: str,
        language: str
    ) -> str:
        """Build recipe generation prompt"""
        lang_text = "German" if language == "de" else "English"
        diet_text = f"\nDietary restrictions: {', '.join(diet_profiles)}" if diet_profiles else ""

        prompt = f"""You are a professional chef assistant. Generate {count} creative and delicious recipes using the following ingredients:

Ingredients: {', '.join(ingredients)}
Servings: {servings}
Language: {lang_text}{diet_text}

IMPORTANT: Return ONLY valid JSON array, no markdown formatting, no explanations.

Format:
[
  {{
    "name": "Recipe name",
    "description": "Brief description (1-2 sentences)",
    "difficulty": 1-5 (1=easy, 5=expert),
    "cooking_time": "XX min",
    "method": "Cooking method (oven/pan/pot/etc)",
    "ingredients": [
      {{"name": "ingredient", "amount": "XXg/ml/pieces", "carbs": XX}}
    ],
    "nutrition_per_serving": {{
      "calories": XX,
      "protein": XX,
      "carbs": XX,
      "fat": XX,
      "{diabetes_unit.lower()}": XX
    }},
    "used_ingredients": ["ingredient1", "ingredient2"],
    "leftover_tips": "Tips for using leftover ingredients"
  }}
]

Calculate {diabetes_unit} values: {"KE = carbs/10" if diabetes_unit == "KE" else "BE = carbs/12"}
Ensure recipes are realistic, nutritionally balanced, and suitable for the dietary restrictions."""

        return prompt


# Singleton Instance
ai_generator = AIRecipeGenerator()
