from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.models.user import User
from app.models.diet_profile import DietProfile
from app.utils.database import get_db
from app.utils.auth import get_current_user
from app.services.diabetes_service import diabetes_service
import json

router = APIRouter(prefix="/diabetes", tags=["Diabetes"])


class InsulinCalculationRequest(BaseModel):
    """Request for insulin calculation"""
    carbs_grams: float = Field(..., ge=0, le=500, description="Carbohydrates in grams")
    current_blood_sugar: Optional[float] = Field(None, ge=20, le=600, description="Current BG in mg/dL")
    target_blood_sugar: Optional[float] = Field(100, ge=70, le=180, description="Target BG in mg/dL")


class InsulinCalculationResponse(BaseModel):
    """Response with insulin calculation"""
    meal_insulin: float
    correction_insulin: float
    total_insulin: float
    carbs_grams: float
    icr: float
    isf: Optional[float]
    current_bg: Optional[float]
    target_bg: Optional[float]
    unit: str
    ke: float
    be: float
    disclaimer: str


@router.post("/calculate-insulin", response_model=InsulinCalculationResponse)
def calculate_insulin(
    request: InsulinCalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate insulin bolus for meal

    - Uses active diabetes profile settings (ICR, ISF)
    - Calculates meal insulin + optional correction insulin
    - Returns KE/BE values for carb counting

    **Requires active diabetes profile with ICR/ISF settings!**
    """
    # Get active diabetes profile
    active_profile = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == "diabetic",
        DietProfile.is_active == True
    ).first()

    if not active_profile:
        raise HTTPException(
            status_code=404,
            detail="Kein aktives Diabetes-Profil gefunden. Bitte erst ein Profil erstellen."
        )

    # Parse settings
    try:
        settings = json.loads(active_profile.settings_json) if active_profile.settings_json else {}
    except:
        settings = {}

    # Get ICR and ISF
    icr = settings.get("icr")
    isf = settings.get("isf")

    if not icr:
        raise HTTPException(
            status_code=400,
            detail="ICR (Insulin-to-Carb Ratio) nicht im Profil hinterlegt. Bitte Profil-Einstellungen ergänzen."
        )

    # Calculate insulin
    result = diabetes_service.calculate_bolus_insulin(
        carbs_grams=request.carbs_grams,
        icr=icr,
        current_blood_sugar=request.current_blood_sugar,
        target_blood_sugar=request.target_blood_sugar,
        isf=isf
    )

    # Add KE/BE
    ke_be = diabetes_service.calculate_ke_be(request.carbs_grams)

    return InsulinCalculationResponse(
        **result,
        ke=ke_be["ke"],
        be=ke_be["be"],
        disclaimer="⚠️ Diese Berechnung ist nur eine Hilfe. Konsultiere immer deinen Arzt bei Insulin-Anpassungen!"
    )


@router.get("/ke-be/{carbs}")
def calculate_ke_be(
    carbs: float = Query(..., ge=0, le=500, description="Carbohydrates in grams"),
    current_user: User = Depends(get_current_user)
):
    """
    Quick KE/BE calculation from carbs

    - **carbs**: Carbohydrates in grams
    - Returns KE (1 KE = 10g) and BE (1 BE = 12g)
    """
    return diabetes_service.calculate_ke_be(carbs)


@router.get("/settings/recommended")
def get_recommended_settings(
    current_user: User = Depends(get_current_user)
):
    """
    Get recommended ICR/ISF starting points

    ⚠️ **IMPORTANT:** These are general guidelines only!
    Individual settings MUST be determined by your healthcare provider.
    """
    return diabetes_service.get_recommended_settings()


@router.post("/estimate-bg-impact")
def estimate_bg_impact(
    carbs_grams: float = Query(..., ge=0, le=500),
    insulin_units: float = Query(..., ge=0, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Estimate blood sugar impact from meal + insulin

    - Uses active profile ICR/ISF settings
    - Returns estimated BG change in mg/dL

    ⚠️ **Estimation only - not medical advice!**
    """
    # Get active diabetes profile
    active_profile = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == "diabetic",
        DietProfile.is_active == True
    ).first()

    if not active_profile:
        raise HTTPException(status_code=404, detail="Kein aktives Diabetes-Profil gefunden")

    try:
        settings = json.loads(active_profile.settings_json) if active_profile.settings_json else {}
    except:
        settings = {}

    icr = settings.get("icr")
    isf = settings.get("isf")

    if not icr or not isf:
        raise HTTPException(
            status_code=400,
            detail="ICR und ISF müssen im Profil hinterlegt sein"
        )

    return diabetes_service.estimate_blood_sugar_impact(
        carbs_grams=carbs_grams,
        insulin_units=insulin_units,
        isf=isf,
        icr=icr
    )
