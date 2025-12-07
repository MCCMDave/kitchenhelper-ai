"""
Recipe Database Model - Kuratierte Rezepte für schnellere Generierung
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.utils.database import Base
import enum


class RecipeDifficulty(str, enum.Enum):
    """Schwierigkeitsgrad"""
    EINFACH = "einfach"
    MITTEL = "mittel"
    FORTGESCHRITTEN = "fortgeschritten"


class RecipeCategory(str, enum.Enum):
    """Rezept-Kategorien"""
    LOW_CARB = "low_carb"
    LOW_GI = "low_gi"
    DIABETIKER_FREUNDLICH = "diabetiker_freundlich"
    VEGETARISCH = "vegetarisch"
    VEGAN = "vegan"
    GLUTENFREI = "glutenfrei"
    SCHNELL = "schnell"  # <30min
    DESSERT = "dessert"


class RecipeDB(Base):
    """Kuratierte Rezepte-Datenbank"""
    __tablename__ = "recipe_db"

    id = Column(Integer, primary_key=True, index=True)

    # Rezept-Info
    name = Column(String, nullable=False, index=True)
    name_de = Column(String, nullable=False)
    name_en = Column(String, nullable=True)
    description = Column(Text, nullable=False)

    # Zutaten & Anleitung
    ingredients = Column(JSON, nullable=False)  # [{"name": "...", "amount": "..."}]
    instructions = Column(JSON, nullable=False)  # ["Schritt 1", "Schritt 2", ...]

    # Metadaten
    servings = Column(Integer, default=2)
    prep_time_min = Column(Integer, nullable=False)  # Zubereitungszeit in Minuten
    cook_time_min = Column(Integer, nullable=False)  # Kochzeit in Minuten
    difficulty = Column(Enum(RecipeDifficulty), default=RecipeDifficulty.EINFACH)

    # Nährwerte (pro Portion)
    calories = Column(Integer, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    fiber = Column(Float, default=0.0)

    # Diabetiker-spezifisch
    be = Column(Float, nullable=False)  # Broteinheiten (carbs / 12)
    ke = Column(Float, nullable=False)  # Kohlenhydrat-Einheiten (carbs / 10)
    gi = Column(Integer, default=50)  # Glykämischer Index (0-100)
    gl = Column(Float, default=0.0)  # Glykämische Last (GI * carbs / 100)

    # Kategorien (für Filterung)
    is_low_carb = Column(Boolean, default=False)  # <20g Kohlenhydrate
    is_low_gi = Column(Boolean, default=False)  # GI <55
    is_diabetic_friendly = Column(Boolean, default=False)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    is_quick = Column(Boolean, default=False)  # <30min Gesamtzeit

    # Popularität & Qualität
    quality_score = Column(Float, default=0.0)  # 0-100 (kuriert = höher)
    usage_count = Column(Integer, default=0)  # Wie oft verwendet
    avg_rating = Column(Float, default=0.0)  # Durchschnittsbewertung (falls User-Ratings)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<RecipeDB(name='{self.name}', carbs={self.carbs}g, gi={self.gi})>"

    @property
    def total_time_min(self) -> int:
        """Gesamtzeit = Vorbereitung + Kochen"""
        return self.prep_time_min + self.cook_time_min

    def to_dict(self):
        """Konvertiert zu Dict (API-Response kompatibel)"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "servings": self.servings,
            "prepTime": f"{self.prep_time_min} min",
            "cookTime": f"{self.cook_time_min} min",
            "totalTime": f"{self.total_time_min} min",
            "difficulty": self.difficulty.value,
            "nutrition": {
                "calories": self.calories,
                "protein": self.protein,
                "carbs": self.carbs,
                "fat": self.fat,
                "fiber": self.fiber,
                "be": self.be,
                "ke": self.ke,
                "gi": self.gi,
                "gl": self.gl,
            },
            "categories": {
                "low_carb": self.is_low_carb,
                "low_gi": self.is_low_gi,
                "diabetic_friendly": self.is_diabetic_friendly,
                "vegetarian": self.is_vegetarian,
                "vegan": self.is_vegan,
                "gluten_free": self.is_gluten_free,
                "quick": self.is_quick,
            },
            "source": "recipe_db",
        }
