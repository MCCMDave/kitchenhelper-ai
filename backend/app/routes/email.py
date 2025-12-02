"""
Email Routes for KitchenHelper-AI

Handles:
- Email verification for new users
- Password reset emails
- Email status checking
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Dict
import secrets
from datetime import datetime, timedelta
import jwt

from app.models.user import User
from app.utils.database import get_db
from app.utils.auth import get_current_user
from app.services.email_service import EmailService
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["Email"])

# Initialize email service
email_service = EmailService()

# Temporary storage for verification tokens (Production: Use Redis or DB)
verification_tokens = {}
reset_tokens = {}


class EmailVerificationRequest(BaseModel):
    """Request email verification"""
    email: EmailStr


class VerifyTokenRequest(BaseModel):
    """Verify email token"""
    token: str


class PasswordResetRequest(BaseModel):
    """Request password reset"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with new password"""
    token: str
    new_password: str


def generate_token(email: str, expiry_hours: int = 24) -> str:
    """Generate JWT token for email verification or password reset"""
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=expiry_hours),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> str:
    """Verify JWT token and return email"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("email")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token ist abgelaufen. Bitte fordere einen neuen an."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ungültiger Token"
        )


@router.post("/send-verification")
def send_verification_email(
    request: EmailVerificationRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Send email verification link to user

    - **email**: User's email address

    Returns success message
    """
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kein Account mit dieser E-Mail gefunden"
        )

    # Check if already verified
    if user.email_verified:
        return {
            "success": True,
            "message": "E-Mail ist bereits verifiziert"
        }

    # Generate verification token
    token = generate_token(user.email, expiry_hours=24)

    # Create verification URL (adjust domain for production)
    base_url = "http://192.168.2.54:8081"  # TODO: Get from env
    verification_url = f"{base_url}/verify-email.html?token={token}"

    try:
        # Send email
        result = email_service.send_verification_email(
            to=user.email,
            verification_url=verification_url,
            user_name=user.username
        )

        logger.info(f"Verification email sent to {user.email}")

        return {
            "success": True,
            "message": "Verifizierungs-E-Mail wurde gesendet",
            "email_id": result.get("email_id")
        }

    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"E-Mail konnte nicht gesendet werden: {str(e)}"
        )


@router.post("/verify")
def verify_email(request: VerifyTokenRequest, db: Session = Depends(get_db)) -> Dict:
    """
    Verify email address with token

    - **token**: Verification token from email

    Returns success message and marks email as verified
    """
    # Verify token and extract email
    email = verify_token(request.token)

    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden"
        )

    # Mark as verified
    if not user.email_verified:
        user.email_verified = True
        user.email_verified_at = datetime.utcnow()
        db.commit()
        logger.info(f"Email verified for user: {user.email}")

    return {
        "success": True,
        "message": "E-Mail erfolgreich verifiziert!",
        "email": user.email
    }


@router.post("/request-password-reset")
def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Send password reset email

    - **email**: User's email address

    Returns success message
    """
    # Find user
    user = db.query(User).filter(User.email == request.email).first()

    # Always return success (security: don't reveal if email exists)
    # But only send email if user actually exists
    if not user:
        logger.warning(f"Password reset requested for non-existent email: {request.email}")
        return {
            "success": True,
            "message": "Falls ein Account mit dieser E-Mail existiert, wurde ein Reset-Link gesendet"
        }

    # Generate reset token
    token = generate_token(user.email, expiry_hours=24)

    # Create reset URL
    base_url = "http://192.168.2.54:8081"  # TODO: Get from env
    reset_url = f"{base_url}/reset-password.html?token={token}"

    try:
        # Send email
        result = email_service.send_password_reset_email(
            to=user.email,
            reset_url=reset_url,
            user_name=user.username
        )

        logger.info(f"Password reset email sent to {user.email}")

        return {
            "success": True,
            "message": "Falls ein Account mit dieser E-Mail existiert, wurde ein Reset-Link gesendet",
            "email_id": result.get("email_id")
        }

    except Exception as e:
        logger.error(f"Failed to send password reset email: {str(e)}")
        # Still return success for security (don't reveal errors)
        return {
            "success": True,
            "message": "Falls ein Account mit dieser E-Mail existiert, wurde ein Reset-Link gesendet"
        }


@router.post("/reset-password")
def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Reset password with token

    - **token**: Reset token from email
    - **new_password**: New password (min 6 characters)

    Returns success message
    """
    # Verify token
    email = verify_token(request.token)

    # Validate password
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwort muss mindestens 6 Zeichen lang sein"
        )

    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benutzer nicht gefunden"
        )

    # Update password
    from app.utils.password import hash_password
    user.hashed_password = hash_password(request.new_password)
    db.commit()

    logger.info(f"Password reset successful for user: {user.email}")

    return {
        "success": True,
        "message": "Passwort erfolgreich zurückgesetzt",
        "email": user.email
    }


@router.get("/resend-verification")
def resend_verification_email(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Resend verification email to current user

    Requires authentication.
    """
    if current_user.email_verified:
        return {
            "success": True,
            "message": "E-Mail ist bereits verifiziert"
        }

    # Generate new token
    token = generate_token(current_user.email, expiry_hours=24)

    # Create verification URL
    base_url = "http://192.168.2.54:8081"  # TODO: Get from env
    verification_url = f"{base_url}/verify-email.html?token={token}"

    try:
        # Send email
        result = email_service.send_verification_email(
            to=current_user.email,
            verification_url=verification_url,
            user_name=current_user.username
        )

        logger.info(f"Verification email resent to {current_user.email}")

        return {
            "success": True,
            "message": "Verifizierungs-E-Mail wurde erneut gesendet",
            "email_id": result.get("email_id")
        }

    except Exception as e:
        logger.error(f"Failed to resend verification email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"E-Mail konnte nicht gesendet werden: {str(e)}"
        )


@router.get("/status")
def get_email_status(current_user: User = Depends(get_current_user)) -> Dict:
    """
    Get current user's email verification status

    Requires authentication.
    """
    return {
        "email": current_user.email,
        "verified": current_user.email_verified,
        "verified_at": current_user.email_verified_at.isoformat() if current_user.email_verified_at else None
    }
