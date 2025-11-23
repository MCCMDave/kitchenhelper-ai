from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
from app.schemas.diet_profile import (
    DietProfileCreate,
    DietProfileUpdate,
    DietProfileResponse,
    DietProfileListResponse
)
from app.models.diet_profile import DietProfile
from app.models.user import User, SubscriptionTier
from app.utils.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/profiles", tags=["Diet Profiles"])

# Erlaubte Profile Types
ALLOWED_PROFILE_TYPES = [
    "diabetic",
    "keto",
    "vegan",
    "vegetarian",
    "low_carb",
    "high_protein",
    "gluten_free",
    "lactose_free"
]

# Standard-Templates fuer schnelle Profil-Erstellung
STANDARD_PROFILES = {
    "diabetic": {
        "name": "Diabetes Typ 2",
        "settings": {
            "unit": "KE",
            "daily_carb_limit": 180,
            "carbs_per_meal": 60
        }
    },
    "keto": {
        "name": "Ketogene Diaet",
        "settings": {
            "daily_carb_limit": 50,
            "daily_fat_min": 150,
            "daily_protein": 100
        }
    },
    "vegan": {
        "name": "Vegan",
        "settings": {
            "exclude_ingredients": ["Fleisch", "Fisch", "Eier", "Milch", "Kaese", "Butter"]
        }
    },
    "vegetarian": {
        "name": "Vegetarisch",
        "settings": {
            "exclude_ingredients": ["Fleisch", "Fisch"]
        }
    },
    "low_carb": {
        "name": "Low Carb",
        "settings": {
            "daily_carb_limit": 100
        }
    },
    "high_protein": {
        "name": "High Protein",
        "settings": {
            "daily_protein_min": 150
        }
    },
    "gluten_free": {
        "name": "Glutenfrei",
        "settings": {
            "exclude_ingredients": ["Weizen", "Roggen", "Gerste", "Dinkel"]
        }
    },
    "lactose_free": {
        "name": "Laktosefrei",
        "settings": {
            "exclude_ingredients": ["Milch", "Sahne", "Joghurt", "Quark"]
        }
    }
}


def validate_profile_type(profile_type: str) -> None:
    """Validiere ob profile_type erlaubt ist"""
    if profile_type not in ALLOWED_PROFILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid profile_type '{profile_type}'. Allowed: {ALLOWED_PROFILE_TYPES}"
        )


def check_profile_limit(user: User, db: Session) -> bool:
    """
    Pruefe ob User noch Profile erstellen darf

    Returns:
        True wenn unter dem Limit, False wenn Limit erreicht
    """
    current_count = db.query(DietProfile).filter(
        DietProfile.user_id == user.id
    ).count()

    limits = {
        SubscriptionTier.DEMO: 1,
        SubscriptionTier.BASIC: 3,
        SubscriptionTier.PREMIUM: 999999
    }

    limit = limits.get(user.subscription_tier, 1)
    return current_count < limit


def get_profile_limit(user: User) -> int:
    """Hole das Profil-Limit fuer den User"""
    limits = {
        SubscriptionTier.DEMO: 1,
        SubscriptionTier.BASIC: 3,
        SubscriptionTier.PREMIUM: 999999
    }
    return limits.get(user.subscription_tier, 1)


def validate_settings(profile_type: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    """Validiere Settings basierend auf profile_type"""

    # Diabetes-spezifische Validierung
    if profile_type == "diabetic":
        if "unit" in settings:
            if settings["unit"] not in ["KE", "BE"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="unit must be 'KE' or 'BE'"
                )
        if "daily_carb_limit" in settings:
            if not isinstance(settings["daily_carb_limit"], (int, float)) or settings["daily_carb_limit"] <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="daily_carb_limit must be a positive number"
                )

    # Keto-spezifische Validierung
    if profile_type == "keto":
        if "daily_carb_limit" in settings:
            if not isinstance(settings["daily_carb_limit"], (int, float)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="daily_carb_limit must be a number"
                )
            if settings["daily_carb_limit"] > 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Keto carb limit should be <= 100g"
                )

    return settings


def parse_settings_json(settings_json: Optional[str]) -> Dict[str, Any]:
    """Parse settings_json zu Dict"""
    if not settings_json:
        return {}
    try:
        return json.loads(settings_json)
    except json.JSONDecodeError:
        return {}


def profile_to_response(profile: DietProfile) -> DietProfileResponse:
    """Konvertiere DietProfile Model zu Response mit geparstem JSON"""
    return DietProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        profile_type=profile.profile_type,
        name=profile.name,
        settings=parse_settings_json(profile.settings_json),
        is_active=profile.is_active,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.get("/", response_model=DietProfileListResponse)
def get_profiles(
    active: Optional[bool] = Query(None, description="Filter: nur aktive (true) oder inaktive (false)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Alle Diet Profiles des Users abrufen

    **Filter:**
    - `active`: true = nur aktive, false = nur inaktive, null = alle
    """
    query = db.query(DietProfile).filter(DietProfile.user_id == current_user.id)

    if active is not None:
        query = query.filter(DietProfile.is_active == active)

    profiles = query.order_by(DietProfile.created_at.desc()).all()

    # Zaehle aktive Profile separat
    active_count = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.is_active == True
    ).count()

    return DietProfileListResponse(
        profiles=[profile_to_response(p) for p in profiles],
        count=len(profiles),
        active_count=active_count
    )


@router.post("/", response_model=DietProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: DietProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Neues Diet Profile erstellen

    **Tier-Limits:**
    - Demo: max 1 Profil
    - Basic: max 3 Profile
    - Premium: unbegrenzt

    **Erlaubte profile_types:**
    diabetic, keto, vegan, vegetarian, low_carb, high_protein, gluten_free, lactose_free
    """
    # 1. Validiere profile_type
    validate_profile_type(profile_data.profile_type)

    # 2. Pruefe Tier-Limit
    if not check_profile_limit(current_user, db):
        limit = get_profile_limit(current_user)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Profile limit reached ({limit}). Upgrade your subscription for more profiles."
        )

    # 3. Validiere Settings
    validated_settings = validate_settings(profile_data.profile_type, profile_data.settings or {})

    # 4. Pruefe auf Duplikat (gleicher profile_type + name)
    existing = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == profile_data.profile_type,
        DietProfile.name == profile_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile '{profile_data.name}' of type '{profile_data.profile_type}' already exists"
        )

    # 5. Profil erstellen
    new_profile = DietProfile(
        user_id=current_user.id,
        profile_type=profile_data.profile_type,
        name=profile_data.name,
        settings_json=json.dumps(validated_settings) if validated_settings else None,
        is_active=profile_data.is_active
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return profile_to_response(new_profile)


@router.post("/templates/{profile_type}", response_model=DietProfileResponse, status_code=status.HTTP_201_CREATED)
def create_from_template(
    profile_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Erstelle Profil aus Standard-Template

    Nutzt vordefinierte Einstellungen fuer den gewaehlten profile_type.
    """
    # Validiere profile_type
    if profile_type not in STANDARD_PROFILES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template not found. Available: {list(STANDARD_PROFILES.keys())}"
        )

    # Pruefe Tier-Limit
    if not check_profile_limit(current_user, db):
        limit = get_profile_limit(current_user)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Profile limit reached ({limit}). Upgrade your subscription for more profiles."
        )

    template = STANDARD_PROFILES[profile_type]

    # Pruefe auf Duplikat
    existing = db.query(DietProfile).filter(
        DietProfile.user_id == current_user.id,
        DietProfile.profile_type == profile_type,
        DietProfile.name == template["name"]
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Profile '{template['name']}' already exists"
        )

    # Erstelle Profil
    new_profile = DietProfile(
        user_id=current_user.id,
        profile_type=profile_type,
        name=template["name"],
        settings_json=json.dumps(template["settings"]),
        is_active=True
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return profile_to_response(new_profile)


@router.get("/templates", response_model=Dict[str, Any])
def get_templates():
    """
    Liste aller verfuegbaren Standard-Templates

    Keine Authentifizierung erforderlich.
    """
    return {
        "templates": STANDARD_PROFILES,
        "allowed_types": ALLOWED_PROFILE_TYPES
    }


@router.get("/{profile_id}", response_model=DietProfileResponse)
def get_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Einzelnes Diet Profile abrufen
    """
    profile = db.query(DietProfile).filter(
        DietProfile.id == profile_id,
        DietProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile_to_response(profile)


@router.patch("/{profile_id}", response_model=DietProfileResponse)
def update_profile(
    profile_id: int,
    profile_data: DietProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Diet Profile bearbeiten

    Nur Felder, die uebergeben werden, werden geaendert.
    """
    profile = db.query(DietProfile).filter(
        DietProfile.id == profile_id,
        DietProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    # Update Felder
    update_data = profile_data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"]:
        # Pruefe auf Duplikat bei Name-Aenderung
        existing = db.query(DietProfile).filter(
            DietProfile.user_id == current_user.id,
            DietProfile.profile_type == profile.profile_type,
            DietProfile.name == update_data["name"],
            DietProfile.id != profile_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Profile with name '{update_data['name']}' already exists"
            )

        profile.name = update_data["name"]

    if "settings" in update_data:
        # Validiere neue Settings
        validated_settings = validate_settings(profile.profile_type, update_data["settings"] or {})
        profile.settings_json = json.dumps(validated_settings) if validated_settings else None

    if "is_active" in update_data:
        profile.is_active = update_data["is_active"]

    db.commit()
    db.refresh(profile)

    return profile_to_response(profile)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Diet Profile loeschen
    """
    profile = db.query(DietProfile).filter(
        DietProfile.id == profile_id,
        DietProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    db.delete(profile)
    db.commit()

    return None
