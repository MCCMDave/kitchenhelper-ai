from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.models.ingredient import Ingredient
from app.models.user import User
from app.utils.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.get("/", response_model=List[IngredientResponse])
def get_ingredients(
    category: Optional[str] = Query(None, description="Filter nach Kategorie"),
    expired: Optional[bool] = Query(None, description="Nur abgelaufene (true) oder gültige (false)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Alle Zutaten des Users abrufen
    
    **Filter:**
    - `category`: Nur bestimmte Kategorie (z.B. "Gemüse")
    - `expired`: true = nur abgelaufene, false = nur gültige, null = alle
    """
    query = db.query(Ingredient).filter(Ingredient.user_id == current_user.id)
    
    # Filter nach Kategorie (case-insensitive)
    if category:
        query = query.filter(Ingredient.category.ilike(category))
    
    # Filter nach Ablaufdatum
    if expired is not None:
        now = datetime.utcnow()
        if expired:
            # Nur abgelaufene (expiry_date < jetzt)
            query = query.filter(
                Ingredient.expiry_date.isnot(None),
                Ingredient.expiry_date < now
            )
        else:
            # Nur gültige (kein expiry_date ODER expiry_date >= jetzt)
            query = query.filter(
                (Ingredient.expiry_date.is_(None)) | (Ingredient.expiry_date >= now)
            )
    
    ingredients = query.order_by(Ingredient.added_at.desc()).all()
    return ingredients

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient_data: IngredientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Neue Zutat hinzufügen
    
    - **name**: Name der Zutat (Pflicht)
    - **category**: Kategorie wie "Gemüse", "Fleisch", "Gewürze"
    - **expiry_date**: Ablaufdatum (ISO format)
    - **is_permanent**: true für haltbare Zutaten wie Salz
    """
    # Normalisiere Namen zu Title Case (Tomaten, nicht TOMATEN oder tomaten)
    normalized_name = ingredient_data.name.strip().title()
    normalized_category = ingredient_data.category.strip().title() if ingredient_data.category else None
    
    new_ingredient = Ingredient(
        user_id=current_user.id,
        name=normalized_name,
        category=normalized_category,
        expiry_date=ingredient_data.expiry_date,
        is_permanent=ingredient_data.is_permanent
    )
    
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    
    return new_ingredient

@router.patch("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Zutat aktualisieren
    
    Nur Felder, die übergeben werden, werden geändert.
    """
    # Zutat suchen
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.user_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )
    
    # Nur übergebene Felder aktualisieren
    update_data = ingredient_data.model_dump(exclude_unset=True)
    
    # Normalisiere Namen und Kategorie
    if "name" in update_data and update_data["name"]:
        update_data["name"] = update_data["name"].strip().title()
    if "category" in update_data and update_data["category"]:
        update_data["category"] = update_data["category"].strip().title()
    
    for field, value in update_data.items():
        setattr(ingredient, field, value)
    
    db.commit()
    db.refresh(ingredient)
    
    return ingredient

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Zutat löschen
    """
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.user_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )
    
    db.delete(ingredient)
    db.commit()
    
    return None