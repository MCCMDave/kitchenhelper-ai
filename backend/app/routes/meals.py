from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta

from app.models.user import User
from app.models.meal_log import MealLog
from app.models.recipe import Recipe
from app.models.diet_profile import DietProfile
from app.utils.database import get_db
from app.utils.auth import get_current_user
import json

router = APIRouter(prefix="/meals", tags=["Meal Tracking"])


class MealLogCreate(BaseModel):
    """Create new meal log entry"""
    recipe_id: Optional[int] = None
    meal_name: str = Field(..., min_length=1, max_length=200)
    meal_type: Optional[str] = Field(None, regex="^(breakfast|lunch|dinner|snack)$")
    servings: float = Field(1.0, ge=0.1, le=20)
    carbs_grams: float = Field(..., ge=0, le=500)
    calories: Optional[int] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)
    fat: Optional[float] = Field(None, ge=0)
    consumed_at: Optional[datetime] = None


class MealLogResponse(BaseModel):
    """Meal log response"""
    id: int
    meal_name: str
    meal_type: Optional[str]
    servings: float
    carbs_grams: float
    ke: float
    be: float
    calories: Optional[int]
    protein: Optional[float]
    fat: Optional[float]
    consumed_at: datetime
    logged_at: datetime

    class Config:
        from_attributes = True


class DailyTrackingResponse(BaseModel):
    """Daily carb tracking summary"""
    date: str
    total_carbs: float
    total_ke: float
    total_be: float
    total_calories: int
    daily_limit_ke: Optional[float]
    remaining_ke: Optional[float]
    percentage_used: Optional[float]
    meals: List[MealLogResponse]
    meal_count: int


@router.post("/log", response_model=MealLogResponse)
def log_meal(
    meal: MealLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Log a consumed meal

    - Can log from existing recipe (recipe_id) or custom meal
    - Automatically calculates KE/BE from carbs
    - Timestamps when meal was consumed

    Returns the logged meal entry
    """
    # Calculate KE/BE
    ke = round(meal.carbs_grams / 10, 1)
    be = round(meal.carbs_grams / 12, 1)

    # Create meal log
    new_log = MealLog(
        user_id=current_user.id,
        recipe_id=meal.recipe_id,
        meal_name=meal.meal_name,
        meal_type=meal.meal_type,
        servings=meal.servings,
        carbs_grams=meal.carbs_grams,
        ke=ke,
        be=be,
        calories=meal.calories,
        protein=meal.protein,
        fat=meal.fat,
        consumed_at=meal.consumed_at or datetime.utcnow()
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


@router.get("/today", response_model=DailyTrackingResponse)
def get_today_tracking(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get today's meal tracking summary

    - Shows all meals logged today
    - Total carbs/KE/BE consumed
    - Progress vs daily limit (if diabetes profile active)
    - Remaining KE for the day

    Perfect for dashboard display!
    """
    # Get today's date range
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    # Get today's meals
    meals = db.query(MealLog).filter(
        MealLog.user_id == current_user.id,
        MealLog.consumed_at >= start_of_day,
        MealLog.consumed_at <= end_of_day
    ).order_by(MealLog.consumed_at.asc()).all()

    # Calculate totals
    total_carbs = sum(m.carbs_grams for m in meals)
    total_ke = sum(m.ke for m in meals)
    total_be = sum(m.be for m in meals)
    total_calories = sum(m.calories for m in meals if m.calories)

    # Get daily limit from active diabetes profile
    daily_limit_ke = None
    remaining_ke = None
    percentage_used = None

    active_profile = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == "diabetic",
        DietProfile.is_active == True
    ).first()

    if active_profile and active_profile.settings_json:
        try:
            settings = json.loads(active_profile.settings_json)
            daily_carb_limit = settings.get("daily_carb_limit")
            if daily_carb_limit:
                daily_limit_ke = round(daily_carb_limit / 10, 1)
                remaining_ke = round(daily_limit_ke - total_ke, 1)
                percentage_used = round((total_ke / daily_limit_ke) * 100, 1) if daily_limit_ke > 0 else 0
        except:
            pass

    return DailyTrackingResponse(
        date=today.isoformat(),
        total_carbs=round(total_carbs, 1),
        total_ke=round(total_ke, 1),
        total_be=round(total_be, 1),
        total_calories=total_calories,
        daily_limit_ke=daily_limit_ke,
        remaining_ke=remaining_ke,
        percentage_used=percentage_used,
        meals=[MealLogResponse.from_orm(m) for m in meals],
        meal_count=len(meals)
    )


@router.get("/history", response_model=List[DailyTrackingResponse])
def get_meal_history(
    days: int = Query(7, ge=1, le=90),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get meal tracking history

    - **days**: Number of days to retrieve (default 7, max 90)
    - Returns daily summaries for each day

    Useful for trends/charts!
    """
    results = []

    for i in range(days):
        target_date = date.today() - timedelta(days=i)
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

        # Get day's meals
        meals = db.query(MealLog).filter(
            MealLog.user_id == current_user.id,
            MealLog.consumed_at >= start_of_day,
            MealLog.consumed_at <= end_of_day
        ).order_by(MealLog.consumed_at.asc()).all()

        if not meals and i > 0:  # Skip empty days (except today)
            continue

        # Calculate totals
        total_carbs = sum(m.carbs_grams for m in meals)
        total_ke = sum(m.ke for m in meals)
        total_be = sum(m.be for m in meals)
        total_calories = sum(m.calories for m in meals if m.calories)

        results.append(DailyTrackingResponse(
            date=target_date.isoformat(),
            total_carbs=round(total_carbs, 1),
            total_ke=round(total_ke, 1),
            total_be=round(total_be, 1),
            total_calories=total_calories,
            daily_limit_ke=None,  # Could add if needed
            remaining_ke=None,
            percentage_used=None,
            meals=[MealLogResponse.from_orm(m) for m in meals],
            meal_count=len(meals)
        ))

    return results


@router.delete("/{meal_id}")
def delete_meal_log(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a meal log entry"""
    meal = db.query(MealLog).filter(
        MealLog.id == meal_id,
        MealLog.user_id == current_user.id
    ).first()

    if not meal:
        raise HTTPException(status_code=404, detail="Meal log nicht gefunden")

    db.delete(meal)
    db.commit()

    return {"message": "Meal log gelöscht"}
