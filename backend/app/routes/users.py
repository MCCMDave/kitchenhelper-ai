from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserUpdate
from app.utils.password import hash_password
from app.models.user import User
from app.utils.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Aktuellen User abrufen (geschützt)
    
    Benötigt: Bearer Token im Authorization Header
    """
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User-Profil aktualisieren

    - **name**: Neuer Name
    - **email**: Neue Email (muss unique sein!)
    - **password**: Neues Passwort (wird gehasht)
    """
    update_fields = user_data.model_dump(exclude_unset=True)

    # Nichts zu updaten
    if not update_fields:
        return current_user

    # Email-Check (muss unique sein)
    if "email" in update_fields and update_fields["email"]:
        existing = db.query(User).filter(
            User.email == update_fields["email"],
            User.id != current_user.id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Passwort hashen wenn vorhanden
    if "password" in update_fields and update_fields["password"]:
        update_fields["hashed_password"] = hash_password(update_fields["password"])
        del update_fields["password"]

    # Update durchfuehren
    for field, value in update_fields.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Account loeschen (GDPR)

    Benoetigt: Bearer Token
    """
    db.delete(current_user)
    db.commit()
    return None