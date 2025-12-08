from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.config import settings
from app.utils.database import init_db
from app.routes import (
    auth,
    users,
    ingredients,
    recipes,
    favorites,
    diet_profiles,
    shopping_list,
    share,
    nutrition,
    admin,
    scanner,
    faq,
    diabetes,
    meals,
    email,
    recipe_db_routes,
    stripe_routes,
)
from app.middleware.logger import APIRequestLoggerMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.email_verification import EmailVerificationMiddleware
from app.middleware.https_redirect import HTTPSRedirectMiddleware
import os

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered recipe generator from available ingredients",
    version=settings.APP_VERSION,
)

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        # Strict Transport Security (nur wenn HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# HTTPS Redirect (force HTTPS in production, except localhost/local networks)
app.add_middleware(HTTPSRedirectMiddleware)

# CORS - Secure Configuration (supports httpOnly cookies)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Nur definierte Origins (aus .env)
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Cookie"],
    expose_headers=["Set-Cookie"],
)

# API Request Logger (only in DEBUG mode)
if os.getenv("DEBUG", "False").lower() == "true":
    app.add_middleware(APIRequestLoggerMiddleware)

# Email Verification (blocks unverified users in production)
app.add_middleware(EmailVerificationMiddleware)

# Rate Limiting for AI generation (protects Pi from overload)
app.add_middleware(RateLimitMiddleware)

# ✅ ROUTES EINBINDEN
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(ingredients.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")
app.include_router(diet_profiles.router, prefix="/api")
app.include_router(shopping_list.router, prefix="/api")
app.include_router(share.router, prefix="/api")
app.include_router(nutrition.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(scanner.router, prefix="/api")
app.include_router(faq.router, prefix="/api")
app.include_router(diabetes.router, prefix="/api")
app.include_router(meals.router, prefix="/api")
app.include_router(email.router, prefix="/api")
app.include_router(recipe_db_routes.router, prefix="/api")
app.include_router(stripe_routes.router, prefix="/api")


# Startup Event
@app.on_event("startup")
def startup_event():
    init_db()
    print(f"[OK] {settings.APP_NAME} v{settings.APP_VERSION} started!")


@app.get("/")
def read_root():
    return {
        "message": f"{settings.APP_NAME} API is running!",
        "version": settings.APP_VERSION,
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
