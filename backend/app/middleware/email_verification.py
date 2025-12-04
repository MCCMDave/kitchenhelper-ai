"""
Email Verification Middleware
Requires users to verify their email before accessing protected endpoints
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.jwt import decode_access_token
from app.utils.database import SessionLocal
from app.models.user import User
import os


class EmailVerificationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce email verification

    - Blocks unverified users from accessing protected endpoints
    - Allows access to: auth, email verification, public endpoints
    - Can be disabled in DEBUG mode for testing
    """

    # Public endpoints that don't require verification
    PUBLIC_PATHS = [
        "/",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/api/auth/register",
        "/api/auth/login",
        "/api/auth/request-password-reset",
        "/api/auth/reset-password",
        "/api/email/send-verification",
        "/api/email/verify",
        "/api/email/resend-verification",
        "/api/share/",  # Public share links
    ]

    async def dispatch(self, request: Request, call_next):
        # Skip verification in DEBUG mode (for testing)
        if os.getenv("DEBUG", "False").lower() == "true":
            return await call_next(request)

        # Check if path is public
        path = request.url.path
        if any(path.startswith(public_path) for public_path in self.PUBLIC_PATHS):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # No token = let auth middleware handle it
            return await call_next(request)

        try:
            token = auth_header.replace("Bearer ", "")
            payload = decode_access_token(token)
            user_id = payload.get("user_id")

            if not user_id:
                return await call_next(request)

            # Check if user's email is verified
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()

                if user and not user.email_verified:
                    # User exists but email not verified
                    return HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "error": "email_not_verified",
                            "message": "Bitte verifiziere deine E-Mail-Adresse, um fortzufahren.",
                            "email": user.email
                        }
                    ).json()
            finally:
                db.close()

        except Exception:
            # If token verification fails, let auth middleware handle it
            pass

        return await call_next(request)
