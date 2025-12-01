from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
import json
import re

from app.schemas.recipe import (
    RecipeGenerateRequest,
    RecipeResponse,
    RecipeListResponse,
    RecipeIngredient,
    NutritionInfo
)
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.user import User
from app.models.diet_profile import DietProfile
from app.utils.database import get_db
from app.utils.auth import get_current_user
from app.services.mock_recipe_generator import mock_generator
from app.services.ai_recipe_generator import ai_generator
from app.services.pdf_generator import pdf_generator

router = APIRouter(prefix="/recipes", tags=["Recipes"])


def recipe_to_response(recipe: Recipe) -> RecipeResponse:
    """
    Convert Recipe DB model to RecipeResponse schema
    Handles JSON parsing for ingredients, nutrition, and used_ingredients
    """
    return RecipeResponse(
        id=recipe.id,
        user_id=recipe.user_id,
        name=recipe.name,
        description=recipe.description,
        difficulty=recipe.difficulty,
        cooking_time=recipe.cooking_time,
        method=recipe.method,
        servings=recipe.servings,
        used_ingredients=json.loads(recipe.used_ingredients) if recipe.used_ingredients else [],
        leftover_tips=recipe.leftover_tips,
        ingredients=[RecipeIngredient(**ing) for ing in json.loads(recipe.ingredients_json)] if recipe.ingredients_json else [],
        nutrition_per_serving=NutritionInfo(**json.loads(recipe.nutrition_json)) if recipe.nutrition_json else {},
        ai_provider=recipe.ai_provider,
        generated_at=recipe.generated_at
    )


def check_daily_limit(user: User, db: Session) -> bool:
    """Prüfe ob User noch Rezepte generieren darf"""
    today = date.today()
    
    # Reset Counter wenn neuer Tag
    if user.last_recipe_date is None or user.last_recipe_date.date() < today:
        user.daily_recipe_count = 0
        user.last_recipe_date = datetime.utcnow()
        db.commit()
    
    # Prüfe Limit
    return user.daily_recipe_count < user.daily_limit

def increment_recipe_count(user: User, db: Session):
    """Erhöhe täglichen Rezept-Counter"""
    user.daily_recipe_count += 1
    user.last_recipe_date = datetime.utcnow()
    db.commit()

@router.post("/generate/stream")
def generate_recipes_stream(
    request: RecipeGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Stream recipe generation in real-time (Server-Sent Events)

    - Returns text tokens as they are generated
    - User sees AI "typing" the recipe live
    - Only works with Ollama (Free tier) - Pro users use fast non-streaming Gemini
    """
    # 1. Daily Limit Check
    if not check_daily_limit(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"error": "daily_limit_reached", "message": "Tageslimit erreicht"}
        )

    # 2. Load ingredients
    ingredients = db.query(Ingredient).filter(
        Ingredient.id.in_(request.ingredient_ids),
        Ingredient.user_id == current_user.id
    ).all()

    if not ingredients:
        raise HTTPException(status_code=400, detail="Keine Zutaten gefunden")

    ingredient_names = [ing.name for ing in ingredients]

    # 3. Get diabetes unit
    diabetes_unit = request.diabetes_unit or "KE"
    active_diabetes_profile = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == "diabetic",
        DietProfile.is_active == True
    ).first()

    if active_diabetes_profile and active_diabetes_profile.settings_json:
        try:
            settings = json.loads(active_diabetes_profile.settings_json)
            diabetes_unit = settings.get("unit", "KE")
        except:
            pass

    # 4. Stream generator function
    def event_stream():
        """SSE format: data: <content>\n\n"""
        try:
            for token in ai_generator.generate_with_streaming(
                ingredients=ingredient_names,
                count=3,
                servings=request.servings,
                diet_profiles=request.diet_profiles,
                diabetes_unit=diabetes_unit,
                language=request.language,
                user_tier=current_user.subscription_tier.value
            ):
                # SSE format
                yield f"data: {json.dumps({'token': token})}\n\n"

            # Signal completion
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    # Increment counter
    increment_recipe_count(current_user, db)

    # Return SSE stream
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@router.post("/generate", response_model=RecipeListResponse)
def generate_recipes(
    request: RecipeGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rezepte generieren (Mock oder AI)

    - **ingredient_ids**: Liste von Zutaten-IDs
    - **ai_provider**: "mock" (template-based, kostenlos) oder "ai" (KI-generiert)
    - **diet_profiles**: z.B. ["diabetic", "vegan"]
    - **servings**: Anzahl Portionen (1-10)

    **AI Provider "ai":**
    - Free Tier: Ollama (lokal, datenschutzfreundlich, ~7-10s)
    - Pro Tier: Gemini Flash (schnell, ~2-3s) mit Ollama Fallback

    **Daily Limits:**
    - Demo: 3 Rezepte/Tag
    - Basic: 50 Rezepte/Tag
    - Premium: Unbegrenzt
    """
    # 1. Daily Limit Check
    if not check_daily_limit(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "daily_limit_reached",
                "message": f"Tageslimit erreicht ({current_user.daily_limit} Rezepte). Upgrade für mehr!",
                "daily_limit": current_user.daily_limit,
                "subscription_tier": current_user.subscription_tier.value
            }
        )
    
    # 2. Zutaten laden
    ingredients = db.query(Ingredient).filter(
        Ingredient.id.in_(request.ingredient_ids),
        Ingredient.user_id == current_user.id
    ).all()
    
    if not ingredients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keine gültigen Zutaten gefunden"
        )
    
    ingredient_names = [ing.name for ing in ingredients]
    
    # 3. Diabetes-Einheit aus aktivem Profil laden (oder aus Request)
    diabetes_unit = request.diabetes_unit or "KE"

    # Aktives Diabetes-Profil pruefen fuer Unit-Einstellung
    active_diabetes_profile = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == "diabetic",
        DietProfile.is_active == True
    ).first()

    if active_diabetes_profile and active_diabetes_profile.settings_json:
        try:
            settings = json.loads(active_diabetes_profile.settings_json)
            diabetes_unit = settings.get("unit", "KE")
        except (json.JSONDecodeError, TypeError):
            pass

    # 4. Generate recipes based on provider and user tier
    if request.ai_provider == "mock":
        # Mock Generator - Always free
        generated_recipes = mock_generator.generate_recipes(
            ingredients=ingredient_names,
            count=3,
            servings=request.servings,
            diet_profiles=request.diet_profiles,
            diabetes_unit=diabetes_unit,
            language=request.language
        )
    elif request.ai_provider == "ai":
        # AI Generator - Tier-based (Free: Ollama, Pro: Gemini with Ollama fallback)
        try:
            generated_recipes = ai_generator.generate_recipes(
                ingredients=ingredient_names,
                count=3,
                servings=request.servings,
                diet_profiles=request.diet_profiles,
                diabetes_unit=diabetes_unit,
                language=request.language,
                user_tier=current_user.subscription_tier.value
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "ai_generation_failed",
                    "message": f"AI-Generierung fehlgeschlagen: {str(e)}",
                    "fallback": "Bitte nutze 'mock' als Provider"
                }
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ungültiger AI Provider '{request.ai_provider}'. Nutze 'mock' oder 'ai'."
        )

    # 5. In Datenbank speichern
    saved_recipes = []
    for recipe_data in generated_recipes:
        new_recipe = Recipe(
            user_id=current_user.id,
            name=recipe_data["name"],
            description=recipe_data["description"],
            difficulty=recipe_data["difficulty"],
            cooking_time=recipe_data["cooking_time"],
            method=recipe_data["method"],
            servings=recipe_data["servings"],
            used_ingredients=json.dumps(recipe_data["used_ingredients"]),
            leftover_tips=recipe_data["leftover_tips"],
            ingredients_json=json.dumps(recipe_data["ingredients"]),
            nutrition_json=json.dumps(recipe_data["nutrition_per_serving"]),
            ai_provider=recipe_data["ai_provider"]
        )
        
        db.add(new_recipe)
        db.flush()  # Um ID zu bekommen
        
        # Response-Format erstellen
        recipe_response = RecipeResponse(
            id=new_recipe.id,
            user_id=new_recipe.user_id,
            name=new_recipe.name,
            description=new_recipe.description,
            difficulty=new_recipe.difficulty,
            cooking_time=new_recipe.cooking_time,
            method=new_recipe.method,
            servings=new_recipe.servings,
            used_ingredients=recipe_data["used_ingredients"],
            leftover_tips=recipe_data["leftover_tips"],
            ingredients=[RecipeIngredient(**ing) for ing in recipe_data["ingredients"]],
            nutrition_per_serving=NutritionInfo(**recipe_data["nutrition_per_serving"]),
            ai_provider=new_recipe.ai_provider,
            generated_at=new_recipe.generated_at
        )
        
        saved_recipes.append(recipe_response)
    
    db.commit()
    
    # 5. Counter erhöhen
    increment_recipe_count(current_user, db)
    
    # 6. Response
    remaining = current_user.daily_limit - current_user.daily_recipe_count
    
    return RecipeListResponse(
        recipes=saved_recipes,
        count=len(saved_recipes),
        daily_count_remaining=remaining,
        message=f"✅ {len(saved_recipes)} Rezepte generiert! Noch {remaining} heute verfügbar."
    )

@router.get("/history", response_model=List[RecipeResponse])
def get_recipe_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rezept-Historie abrufen
    
    - **limit**: Max. Anzahl Rezepte (default: 20)
    """
    recipes = db.query(Recipe).filter(
        Recipe.user_id == current_user.id
    ).order_by(Recipe.generated_at.desc()).limit(limit).all()
    
    # Parse JSON fields using helper function
    return [recipe_to_response(recipe) for recipe in recipes]

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Einzelnes Rezept abrufen"""
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rezept nicht gefunden"
        )

    return recipe_to_response(recipe)


@router.get("/{recipe_id}/portions", response_model=RecipeResponse)
def calculate_portions(
    recipe_id: int,
    servings: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate recipe portions (adjust ingredient amounts)

    - **recipe_id**: ID of the recipe
    - **servings**: Desired number of servings

    Returns: Recipe with adjusted ingredient amounts
    """
    # Validate servings
    if servings < 1 or servings > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Servings must be between 1 and 20"
        )

    # Load recipe
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Parse ingredients
    ingredients = json.loads(recipe.ingredients_json) if recipe.ingredients_json else []
    nutrition = json.loads(recipe.nutrition_json) if recipe.nutrition_json else {}

    # Calculate multiplier
    original_servings = recipe.servings or 2
    multiplier = servings / original_servings

    # Adjust ingredient amounts
    adjusted_ingredients = []
    for ing in ingredients:
        adjusted_ing = ing.copy()
        amount_str = ing.get("amount", "")

        # Try to parse and multiply numeric amounts
        match = re.match(r'(\d+(?:\.\d+)?)\s*(.+)', amount_str)
        if match:
            number = float(match.group(1))
            unit = match.group(2)
            new_amount = round(number * multiplier, 1)
            adjusted_ing["amount"] = f"{new_amount} {unit}"

        # Adjust carbs if present
        if "carbs" in ing and ing["carbs"]:
            adjusted_ing["carbs"] = round(ing["carbs"] * multiplier, 1)

        adjusted_ingredients.append(adjusted_ing)

    # Return adjusted recipe (without saving)
    return RecipeResponse(
        id=recipe.id,
        user_id=recipe.user_id,
        name=recipe.name,
        description=recipe.description,
        difficulty=recipe.difficulty,
        cooking_time=recipe.cooking_time,
        method=recipe.method,
        servings=servings,  # New servings
        used_ingredients=json.loads(recipe.used_ingredients) if recipe.used_ingredients else [],
        leftover_tips=recipe.leftover_tips,
        ingredients=[RecipeIngredient(**ing) for ing in adjusted_ingredients],
        nutrition_per_serving=NutritionInfo(**nutrition),  # Per serving stays same
        ai_provider=recipe.ai_provider,
        generated_at=recipe.generated_at
    )


@router.get("/{recipe_id}/export/pdf")
def export_recipe_as_pdf(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export recipe as PDF

    - **recipe_id**: ID of the recipe

    Returns: PDF Download
    """
    # Load recipe
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    # Prepare recipe data for PDF
    recipe_data = {
        "name": recipe.name,
        "description": recipe.description,
        "difficulty": recipe.difficulty,
        "cooking_time": recipe.cooking_time,
        "method": recipe.method,
        "servings": recipe.servings,
        "ingredients": json.loads(recipe.ingredients_json) if recipe.ingredients_json else [],
        "nutrition_per_serving": json.loads(recipe.nutrition_json) if recipe.nutrition_json else {}
    }

    # Generate PDF
    pdf_buffer = pdf_generator.generate(recipe_data)

    # Safe filename (no special characters)
    safe_name = re.sub(r'[^\w\s-]', '', recipe.name).replace(' ', '_')[:50]
    filename = f"recipe_{safe_name}.pdf"

    # Return PDF as download
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )