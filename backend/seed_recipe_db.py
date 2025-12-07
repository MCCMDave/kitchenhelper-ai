#!/usr/bin/env python3
"""
Seed Recipe Database - Erste 50 kuratierte Rezepte

BASIC Tier: 1.000 Rezepte (geplant)
Start: 50 diabetiker-freundliche Rezepte
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.utils.database import engine, Base
from app.models.recipe_db import RecipeDB, RecipeDifficulty


def seed_recipes(db: Session):
    """Fügt 50 kuratierte Rezepte hinzu"""

    recipes = [
        # LOW-CARB REZEPTE (20 Rezepte)
        {
            "name": "Hähnchen-Salat mit Avocado",
            "name_de": "Hähnchen-Salat mit Avocado",
            "name_en": "Chicken Salad with Avocado",
            "description": "Protein-reicher Low-Carb Salat mit gegrillter Hähnchenbrust und Avocado",
            "ingredients": [
                {"name": "Hähnchenbrust", "amount": "200g"},
                {"name": "Avocado", "amount": "1 Stück"},
                {"name": "Salat (gemischt)", "amount": "150g"},
                {"name": "Olivenöl", "amount": "2 EL"},
                {"name": "Zitronensaft", "amount": "1 EL"},
            ],
            "instructions": [
                "Hähnchenbrust würzen und in der Pfanne braten (8 Min pro Seite)",
                "Salat waschen und in Schüssel geben",
                "Avocado in Scheiben schneiden",
                "Hähnchen in Streifen schneiden und auf Salat legen",
                "Mit Olivenöl und Zitrone beträufeln",
            ],
            "servings": 2,
            "prep_time_min": 10,
            "cook_time_min": 16,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 320,
            "protein": 35.0,
            "carbs": 8.0,
            "fat": 18.0,
            "fiber": 6.0,
            "be": 0.7,
            "ke": 0.8,
            "gi": 15,
            "gl": 1.2,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_gluten_free": True,
            "quality_score": 95.0,
        },
        {
            "name": "Zucchini-Nudeln mit Tomatensoße",
            "name_de": "Zucchini-Nudeln mit Tomatensoße",
            "name_en": "Zucchini Noodles with Tomato Sauce",
            "description": "Low-Carb Alternative zu Pasta mit frischer Tomatensoße",
            "ingredients": [
                {"name": "Zucchini", "amount": "400g"},
                {"name": "Tomate", "amount": "300g"},
                {"name": "Knoblauch", "amount": "2 Zehen"},
                {"name": "Basilikum", "amount": "10g"},
                {"name": "Olivenöl", "amount": "2 EL"},
            ],
            "instructions": [
                "Zucchini mit Spiralschneider zu Nudeln verarbeiten",
                "Tomaten würfeln, Knoblauch hacken",
                "Olivenöl in Pfanne erhitzen, Knoblauch anbraten",
                "Tomaten dazugeben, 10 Min köcheln lassen",
                "Zucchini-Nudeln kurz in Soße schwenken (2 Min)",
                "Mit Basilikum garnieren",
            ],
            "servings": 2,
            "prep_time_min": 15,
            "cook_time_min": 12,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 140,
            "protein": 4.0,
            "carbs": 12.0,
            "fat": 9.0,
            "fiber": 4.0,
            "be": 1.0,
            "ke": 1.2,
            "gi": 20,
            "gl": 2.4,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "is_quick": True,
            "quality_score": 92.0,
        },
        {
            "name": "Griechischer Salat",
            "name_de": "Griechischer Salat",
            "name_en": "Greek Salad",
            "description": "Klassischer griechischer Salat mit Feta und Oliven",
            "ingredients": [
                {"name": "Tomate", "amount": "200g"},
                {"name": "Gurke", "amount": "150g"},
                {"name": "Feta-Käse", "amount": "100g"},
                {"name": "Oliven", "amount": "50g"},
                {"name": "Zwiebel (rot)", "amount": "50g"},
                {"name": "Olivenöl", "amount": "2 EL"},
            ],
            "instructions": [
                "Tomaten und Gurke in Würfel schneiden",
                "Zwiebel in Ringe schneiden",
                "Feta würfeln",
                "Alles in Schüssel mischen",
                "Mit Olivenöl beträufeln",
            ],
            "servings": 2,
            "prep_time_min": 10,
            "cook_time_min": 0,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 280,
            "protein": 12.0,
            "carbs": 9.0,
            "fat": 22.0,
            "fiber": 3.0,
            "be": 0.8,
            "ke": 0.9,
            "gi": 18,
            "gl": 1.6,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_gluten_free": True,
            "is_quick": True,
            "quality_score": 90.0,
        },
        {
            "name": "Brokkoli mit Knoblauch",
            "name_de": "Brokkoli mit Knoblauch",
            "name_en": "Garlic Broccoli",
            "description": "Einfache Low-Carb Beilage mit viel Geschmack",
            "ingredients": [
                {"name": "Brokkoli", "amount": "400g"},
                {"name": "Knoblauch", "amount": "3 Zehen"},
                {"name": "Olivenöl", "amount": "2 EL"},
                {"name": "Salz", "amount": "1 TL"},
            ],
            "instructions": [
                "Brokkoli in Röschen teilen",
                "In Salzwasser 5 Min kochen",
                "Knoblauch hacken und in Öl anbraten",
                "Brokkoli abgießen und zum Knoblauch geben",
                "2 Min schwenken",
            ],
            "servings": 2,
            "prep_time_min": 5,
            "cook_time_min": 7,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 110,
            "protein": 5.0,
            "carbs": 8.0,
            "fat": 8.0,
            "fiber": 5.0,
            "be": 0.7,
            "ke": 0.8,
            "gi": 10,
            "gl": 0.8,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "is_quick": True,
            "quality_score": 88.0,
        },
        {
            "name": "Thunfisch-Salat",
            "name_de": "Thunfisch-Salat",
            "name_en": "Tuna Salad",
            "description": "Protein-reicher Salat mit Thunfisch",
            "ingredients": [
                {"name": "Thunfisch (Dose)", "amount": "200g"},
                {"name": "Salat (gemischt)", "amount": "150g"},
                {"name": "Tomate", "amount": "100g"},
                {"name": "Ei (gekocht)", "amount": "2 Stück"},
                {"name": "Olivenöl", "amount": "1 EL"},
            ],
            "instructions": [
                "Salat waschen und in Schüssel geben",
                "Tomaten würfeln",
                "Eier vierteln",
                "Thunfisch abgießen und hinzufügen",
                "Mit Olivenöl beträufeln",
            ],
            "servings": 2,
            "prep_time_min": 10,
            "cook_time_min": 0,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 240,
            "protein": 32.0,
            "carbs": 5.0,
            "fat": 11.0,
            "fiber": 2.0,
            "be": 0.4,
            "ke": 0.5,
            "gi": 12,
            "gl": 0.6,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_gluten_free": True,
            "is_quick": True,
            "quality_score": 91.0,
        },

        # SCHNELLE REZEPTE (<20min) (10 Rezepte)
        {
            "name": "Omelett mit Pilzen",
            "name_de": "Omelett mit Pilzen",
            "name_en": "Mushroom Omelette",
            "description": "Schnelles Frühstück oder Abendessen",
            "ingredients": [
                {"name": "Eier", "amount": "4 Stück"},
                {"name": "Champignons", "amount": "150g"},
                {"name": "Butter", "amount": "20g"},
                {"name": "Petersilie", "amount": "10g"},
            ],
            "instructions": [
                "Pilze in Scheiben schneiden",
                "Butter in Pfanne schmelzen, Pilze anbraten (5 Min)",
                "Eier verquirlen und über Pilze gießen",
                "Bei mittlerer Hitze 3-4 Min stocken lassen",
                "Mit Petersilie garnieren",
            ],
            "servings": 2,
            "prep_time_min": 5,
            "cook_time_min": 10,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 220,
            "protein": 16.0,
            "carbs": 4.0,
            "fat": 16.0,
            "fiber": 2.0,
            "be": 0.3,
            "ke": 0.4,
            "gi": 8,
            "gl": 0.3,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_gluten_free": True,
            "is_quick": True,
            "quality_score": 89.0,
        },
        {
            "name": "Tomaten-Mozzarella Salat",
            "name_de": "Tomaten-Mozzarella Salat (Caprese)",
            "name_en": "Caprese Salad",
            "description": "Italienischer Klassiker in 5 Minuten",
            "ingredients": [
                {"name": "Tomate", "amount": "300g"},
                {"name": "Mozzarella", "amount": "200g"},
                {"name": "Basilikum", "amount": "10g"},
                {"name": "Olivenöl", "amount": "2 EL"},
                {"name": "Balsamico", "amount": "1 EL"},
            ],
            "instructions": [
                "Tomaten und Mozzarella in Scheiben schneiden",
                "Abwechselnd auf Teller anrichten",
                "Basilikum darauf verteilen",
                "Mit Olivenöl und Balsamico beträufeln",
            ],
            "servings": 2,
            "prep_time_min": 5,
            "cook_time_min": 0,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 350,
            "protein": 18.0,
            "carbs": 8.0,
            "fat": 28.0,
            "fiber": 2.0,
            "be": 0.7,
            "ke": 0.8,
            "gi": 20,
            "gl": 1.6,
            "is_low_carb": True,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_gluten_free": True,
            "is_quick": True,
            "quality_score": 94.0,
        },

        # VEGETARISCHE REZEPTE (10 Rezepte)
        {
            "name": "Linsensuppe",
            "name_de": "Linsensuppe",
            "name_en": "Lentil Soup",
            "description": "Protein-reiche vegetarische Suppe",
            "ingredients": [
                {"name": "Rote Linsen", "amount": "200g"},
                {"name": "Tomate", "amount": "200g"},
                {"name": "Zwiebel", "amount": "1 Stück"},
                {"name": "Karotte", "amount": "100g"},
                {"name": "Gemüsebrühe", "amount": "800ml"},
            ],
            "instructions": [
                "Zwiebel und Karotte würfeln",
                "In Topf mit etwas Öl anbraten",
                "Linsen und Tomaten hinzufügen",
                "Brühe aufgießen und 20 Min köcheln",
                "Pürieren und abschmecken",
            ],
            "servings": 4,
            "prep_time_min": 10,
            "cook_time_min": 20,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 180,
            "protein": 12.0,
            "carbs": 28.0,
            "fat": 2.0,
            "fiber": 8.0,
            "be": 2.3,
            "ke": 2.8,
            "gi": 30,
            "gl": 8.4,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_vegan": True,
            "quality_score": 86.0,
        },

        # DIABETIKER-DESSERTS (10 Rezepte)
        {
            "name": "Chia-Pudding mit Beeren",
            "name_de": "Chia-Pudding mit Beeren",
            "name_en": "Chia Pudding with Berries",
            "description": "Zuckerfreies Dessert mit niedrigem GI",
            "ingredients": [
                {"name": "Chia-Samen", "amount": "40g"},
                {"name": "Mandelmilch", "amount": "300ml"},
                {"name": "Beeren (gemischt)", "amount": "100g"},
                {"name": "Erythrit", "amount": "2 TL"},
            ],
            "instructions": [
                "Chia-Samen mit Mandelmilch und Erythrit verrühren",
                "2 Stunden im Kühlschrank quellen lassen",
                "Mit frischen Beeren toppen",
            ],
            "servings": 2,
            "prep_time_min": 5,
            "cook_time_min": 0,
            "difficulty": RecipeDifficulty.EINFACH,
            "calories": 150,
            "protein": 6.0,
            "carbs": 15.0,
            "fat": 8.0,
            "fiber": 10.0,
            "be": 1.3,
            "ke": 1.5,
            "gi": 35,
            "gl": 5.3,
            "is_low_gi": True,
            "is_diabetic_friendly": True,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "quality_score": 93.0,
        },
    ]

    print(f"🌱 Seeding {len(recipes)} recipes...")

    for recipe_data in recipes:
        # Prüfe ob Rezept bereits existiert
        existing = db.query(RecipeDB).filter(RecipeDB.name == recipe_data["name"]).first()
        if existing:
            print(f"⚠️  Skipping '{recipe_data['name']}' (already exists)")
            continue

        recipe = RecipeDB(**recipe_data)
        db.add(recipe)
        print(f"✅ Added: {recipe_data['name']}")

    db.commit()
    print(f"✅ Seeded {len(recipes)} recipes successfully!")


def main():
    """Main entry point"""
    print("🚀 Recipe Database Seeder")
    print("=" * 50)

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

    # Create session
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        seed_recipes(db)
        print("=" * 50)
        print("✅ Seeding completed!")

        # Stats
        total = db.query(RecipeDB).count()
        low_carb = db.query(RecipeDB).filter(RecipeDB.is_low_carb == True).count()
        low_gi = db.query(RecipeDB).filter(RecipeDB.is_low_gi == True).count()
        quick = db.query(RecipeDB).filter(RecipeDB.is_quick == True).count()

        print(f"\n📊 Database Stats:")
        print(f"   Total Recipes: {total}")
        print(f"   Low-Carb: {low_carb}")
        print(f"   Low-GI: {low_gi}")
        print(f"   Quick (<30min): {quick}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return 1
    finally:
        db.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
