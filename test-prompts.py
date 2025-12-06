#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Kitchen AI prompts with different user preferences
Uses identical ingredients but varies dietary preferences/constraints
"""

import requests
import json
from datetime import datetime
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

# Test ingredients (identical for all scenarios)
TEST_INGREDIENTS = ["Hähnchenbrust", "Tomate", "Mozzarella", "Basilikum", "Olivenöl"]


def generate_recipe(system_prompt, user_prompt, scenario_name):
    """Generate recipe using Ollama API"""

    print(f"\n{'='*80}")
    print(f"🧪 TEST: {scenario_name}")
    print(f"{'='*80}")
    print(f"\n📝 System Prompt:\n{system_prompt[:200]}...")
    print(f"\n📝 User Prompt:\n{user_prompt[:200]}...")

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    start_time = datetime.now()

    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=120)
        response.raise_for_status()

        elapsed = (datetime.now() - start_time).total_seconds()
        result = response.json()
        recipe_text = result.get("response", "")

        print(f"\n⏱️  Generation Time: {elapsed:.2f}s")
        print(f"\n🍳 Generated Recipe:\n{recipe_text[:500]}...")

        # Try to parse JSON
        try:
            # Extract JSON from response (might have markdown code blocks)
            if "```json" in recipe_text:
                json_start = recipe_text.find("```json") + 7
                json_end = recipe_text.find("```", json_start)
                recipe_json = json.loads(recipe_text[json_start:json_end].strip())
            elif "```" in recipe_text:
                json_start = recipe_text.find("```") + 3
                json_end = recipe_text.find("```", json_start)
                recipe_json = json.loads(recipe_text[json_start:json_end].strip())
            else:
                recipe_json = json.loads(recipe_text)

            print(f"\n✅ Valid JSON Response")
            print(f"   - Name: {recipe_json.get('name', 'N/A')}")
            print(f"   - Kalorien: {recipe_json.get('nutrition', {}).get('calories', 'N/A')}")
            print(f"   - Zubereitungszeit: {recipe_json.get('prepTime', 'N/A')} + {recipe_json.get('cookTime', 'N/A')}")
            print(f"   - Schritte: {len(recipe_json.get('instructions', []))}")

        except json.JSONDecodeError as e:
            print(f"\n❌ Invalid JSON: {e}")
            print(f"   Raw response: {recipe_text[:200]}...")

        return {
            "scenario": scenario_name,
            "time": elapsed,
            "response": recipe_text,
            "success": True
        }

    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {e}")
        return {
            "scenario": scenario_name,
            "time": 0,
            "error": str(e),
            "success": False
        }


# Test Scenario 1: Vegetarisch
def test_vegetarian():
    system_prompt = """Du bist ein professioneller vegetarischer Koch-Assistent mit 15 Jahren Erfahrung.

WICHTIG: Antworte NUR mit JSON, keine zusätzlichen Erklärungen."""

    user_prompt = f"""Erstelle ein vegetarisches Rezept mit folgenden Zutaten:
{', '.join(TEST_INGREDIENTS)}

PRÄFERENZEN:
- Vegetarisch (keine tierischen Produkte außer Milchprodukte und Eier)
- Diät-Anforderung: Ersetze nicht-vegetarische Zutaten durch vegetarische Alternativen

WICHTIG: Hähnchenbrust ist NICHT vegetarisch - ersetze es durch eine vegetarische Alternative (z.B. Halloumi, Tofu, Tempeh)

Antworte im JSON-Format:
{{
  "name": "Rezeptname",
  "description": "Kurzbeschreibung",
  "servings": 2,
  "prepTime": "15 min",
  "cookTime": "20 min",
  "difficulty": "Mittel",
  "ingredients": [
    {{"item": "Zutat", "amount": "Menge"}}
  ],
  "instructions": ["Schritt 1", "Schritt 2"],
  "nutrition": {{
    "calories": 400,
    "protein": "30g",
    "carbs": "20g",
    "fat": "15g"
  }},
  "tags": ["vegetarisch"]
}}"""

    return generate_recipe(system_prompt, user_prompt, "Vegetarisch")


# Test Scenario 2: Low-Carb
def test_low_carb():
    system_prompt = """Du bist ein professioneller Ernährungs-Coach mit Spezialisierung auf Low-Carb Ernährung.

WICHTIG: Antworte NUR mit JSON, keine zusätzlichen Erklärungen."""

    user_prompt = f"""Erstelle ein Low-Carb Rezept mit folgenden Zutaten:
{', '.join(TEST_INGREDIENTS)}

PRÄFERENZEN:
- Low-Carb (MAXIMAL 10g Kohlenhydrate pro Portion)
- Diät-Ziel: Gewichtsverlust
- Fokus auf hohen Proteingehalt (mindestens 40g pro Portion)

WICHTIG:
- Max 10g Kohlenhydrate pro Portion
- Vermeide Brot, Nudeln, Reis, Kartoffeln
- Fokus auf Protein und gesunde Fette

Antworte im JSON-Format:
{{
  "name": "Rezeptname",
  "description": "Kurzbeschreibung",
  "servings": 2,
  "prepTime": "10 min",
  "cookTime": "15 min",
  "difficulty": "Einfach",
  "ingredients": [
    {{"item": "Zutat", "amount": "Menge"}}
  ],
  "instructions": ["Schritt 1", "Schritt 2"],
  "nutrition": {{
    "calories": 500,
    "protein": "50g",
    "carbs": "8g",
    "fat": "25g"
  }},
  "tags": ["low-carb", "high-protein"]
}}"""

    return generate_recipe(system_prompt, user_prompt, "Low-Carb")


# Test Scenario 3: Schnell (<20min)
def test_quick():
    system_prompt = """Du bist ein professioneller Koch-Assistent mit Fokus auf schnelle, einfache Gerichte für Anfänger.

WICHTIG: Antworte NUR mit JSON, keine zusätzlichen Erklärungen."""

    user_prompt = f"""Erstelle ein schnelles, einfaches Rezept mit folgenden Zutaten:
{', '.join(TEST_INGREDIENTS)}

PRÄFERENZEN:
- Schnell (MAXIMAL 20 Minuten Gesamtzeit)
- Einfach (Anfänger-freundlich)
- MAXIMAL 5 Zubereitungsschritte

WICHTIG:
- Gesamtzeit (Vorbereitung + Kochen) max 20 Minuten
- Maximal 5 einfache Schritte
- Keine komplizierten Techniken
- Wenig Geschirr

Antworte im JSON-Format:
{{
  "name": "Rezeptname",
  "description": "Kurzbeschreibung",
  "servings": 2,
  "prepTime": "5 min",
  "cookTime": "10 min",
  "difficulty": "Einfach",
  "ingredients": [
    {{"item": "Zutat", "amount": "Menge"}}
  ],
  "instructions": ["Schritt 1", "Schritt 2", "Schritt 3", "Schritt 4", "Schritt 5"],
  "nutrition": {{
    "calories": 350,
    "protein": "35g",
    "carbs": "12g",
    "fat": "18g"
  }},
  "tags": ["schnell", "einfach"]
}}"""

    return generate_recipe(system_prompt, user_prompt, "Schnell (<20min)")


# Test Scenario 4: Gourmet
def test_gourmet():
    system_prompt = """Du bist ein Sternekoch-Assistent aus einem 2-Sterne Michelin Restaurant mit 20 Jahren Erfahrung.

WICHTIG: Antworte NUR mit JSON, keine zusätzlichen Erklärungen."""

    user_prompt = f"""Erstelle ein Gourmet-Rezept mit folgenden Zutaten:
{', '.join(TEST_INGREDIENTS)}

PRÄFERENZEN:
- Gourmet / Fine Dining
- Komplexe Aromen und Texturen
- Restaurant-Qualität
- Beeindruckende Präsentation

WICHTIG:
- Nutze fortgeschrittene Koch-Techniken (Reduktion, Sous-Vide, Confit, etc.)
- Erstelle komplexe Geschmacksschichten
- Plating-Anweisungen für Restaurant-Präsentation
- Weinempfehlung

Antworte im JSON-Format:
{{
  "name": "Rezeptname (französisch/italienisch)",
  "description": "Detaillierte Beschreibung",
  "servings": 2,
  "prepTime": "30 min",
  "cookTime": "45 min",
  "difficulty": "Fortgeschritten",
  "ingredients": [
    {{"item": "Zutat", "amount": "Menge"}}
  ],
  "instructions": ["Detaillierter Schritt 1", "Schritt 2"],
  "nutrition": {{
    "calories": 650,
    "protein": "45g",
    "carbs": "30g",
    "fat": "35g"
  }},
  "plating": "Anrichte-Anweisungen",
  "wine_pairing": "Weinempfehlung",
  "tags": ["gourmet", "fine-dining"]
}}"""

    return generate_recipe(system_prompt, user_prompt, "Gourmet")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 KITCHEN AI - PROMPT TESTING SUITE")
    print("="*80)
    print(f"\nModel: {MODEL}")
    print(f"Test Ingredients: {', '.join(TEST_INGREDIENTS)}")
    print(f"\nTesting 4 scenarios with identical ingredients but different preferences...")

    results = []

    # Run all tests
    results.append(test_vegetarian())
    results.append(test_low_carb())
    results.append(test_quick())
    results.append(test_gourmet())

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)

    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]

    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")

    if successful:
        avg_time = sum(r["time"] for r in successful) / len(successful)
        print(f"\n⏱️  Average Generation Time: {avg_time:.2f}s")
        print(f"   Fastest: {min(r['time'] for r in successful):.2f}s")
        print(f"   Slowest: {max(r['time'] for r in successful):.2f}s")

    print("\n" + "="*80)
    print("✅ Testing complete!")
    print("="*80)
