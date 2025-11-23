from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import re

# Request Schemas (Input)
class UserCreate(BaseModel):
    """User Registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    emoji: Optional[str] = "👤"

    @field_validator('username')
    @classmethod
    def username_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Benutzername darf nur Buchstaben, Zahlen, - und _ enthalten')
        return v.lower()


class UserLogin(BaseModel):
    """User Login - mit Email ODER Username"""
    email_or_username: str = Field(..., description="E-Mail oder Benutzername")
    password: str


# Response Schemas (Output)
class UserResponse(BaseModel):
    """User Info (oeffentlich)"""
    id: int
    email: str
    username: str
    emoji: Optional[str] = None
    subscription_tier: str
    daily_recipe_count: int
    daily_limit: int
    created_at: datetime

    class Config:
        from_attributes = True  # Erlaubt SQLAlchemy Models


class Token(BaseModel):
    """JWT Token Response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT Payload"""
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserUpdate(BaseModel):
    """User-Daten aktualisieren"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    emoji: Optional[str] = None

    @field_validator('username')
    @classmethod
    def username_valid(cls, v):
        if v is None:
            return v
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Benutzername darf nur Buchstaben, Zahlen, - und _ enthalten')
        return v.lower()


class PasswordResetRequest(BaseModel):
    """Passwort-Reset anfordern"""
    email: EmailStr


class PasswordReset(BaseModel):
    """Passwort zuruecksetzen"""
    token: str
    new_password: str
