from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import secrets
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, PasswordResetRequest, PasswordReset
from app.models.user import User
from app.utils.database import get_db
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Temporaere Speicherung fuer Reset Tokens (in Production: Redis oder DB)
reset_tokens = {}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Neuen User registrieren

    - **email**: Gueltige Email-Adresse
    - **username**: 3-20 Zeichen, nur Buchstaben, Zahlen, - und _
    - **password**: Mindestens 6 Zeichen
    """
    try:
        # Pruefen ob Email schon existiert
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Diese E-Mail ist bereits registriert."
            )

        # Pruefen ob Username schon existiert
        existing_username = db.query(User).filter(User.username == user_data.username.lower()).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dieser Benutzername ist bereits vergeben."
            )

        # Passwort validieren
        if len(user_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwort muss mindestens 6 Zeichen lang sein."
            )

        # Neuen User erstellen
        new_user = User(
            email=user_data.email,
            username=user_data.username.lower(),
            hashed_password=hash_password(user_data.password),
            emoji=user_data.emoji or "👤"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"[OK] User registered: {new_user.username} ({new_user.email})")
        return new_user

    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        print(f"[ERROR] IntegrityError: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-Mail oder Benutzername bereits vergeben."
        )
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registrierung fehlgeschlagen: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User einloggen mit E-Mail ODER Benutzername

    - **email_or_username**: E-Mail-Adresse oder Benutzername
    - **password**: Passwort

    Returns JWT Access Token
    """
    login_input = credentials.email_or_username.lower().strip()

    # Versuche zuerst per Email zu finden
    user = db.query(User).filter(User.email == login_input).first()

    # Falls nicht gefunden, versuche per Username
    if not user:
        user = db.query(User).filter(User.username == login_input).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-Mail/Benutzername oder Passwort falsch."
        )

    # Passwort pruefen
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-Mail/Benutzername oder Passwort falsch."
        )

    # JWT Token erstellen
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    print(f"[OK] User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/request-password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Passwort-Reset anfordern

    - **email**: E-Mail des Accounts

    Generiert einen Reset-Token (in Production: per E-Mail senden)
    """
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        # Security: Nicht verraten ob E-Mail existiert
        return {
            "message": "Falls ein Account mit dieser E-Mail existiert, wurde ein Reset-Link gesendet.",
            "dev_token": None
        }

    # Generate reset token
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = {
        "user_id": user.id,
        "email": user.email,
        "expires": datetime.utcnow() + timedelta(hours=1)
    }

    # TODO: In Production E-Mail senden
    print(f"[DEV] Reset Token fuer {request.email}: {token}")

    return {
        "message": "Reset-Link wurde gesendet! (Dev: Token in Console)",
        "dev_token": token  # NUR FUER DEVELOPMENT!
    }


@router.post("/reset-password")
def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    """
    Passwort mit Reset-Token zuruecksetzen

    - **token**: Reset-Token aus der E-Mail
    - **new_password**: Neues Passwort (mind. 6 Zeichen)
    """
    if request.token not in reset_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ungueltiger oder abgelaufener Reset-Link."
        )

    token_data = reset_tokens[request.token]

    # Check expiration
    if datetime.utcnow() > token_data["expires"]:
        del reset_tokens[request.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset-Link ist abgelaufen. Bitte fordere einen neuen an."
        )

    # Validate new password
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwort muss mindestens 6 Zeichen lang sein."
        )

    # Update password
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User nicht gefunden."
        )

    user.hashed_password = hash_password(request.new_password)
    db.commit()

    # Delete used token
    del reset_tokens[request.token]

    print(f"[OK] Password reset for: {user.email}")
    return {"message": "Passwort erfolgreich zurueckgesetzt! Du kannst dich jetzt anmelden."}
