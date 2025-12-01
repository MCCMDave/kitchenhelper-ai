from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
)
from app.middleware.logger import APIRequestLoggerMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
import os

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered recipe generator from available ingredients",
    version=settings.APP_VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Request Logger (only in DEBUG mode)
if os.getenv("DEBUG", "False").lower() == "true":
    app.add_middleware(APIRequestLoggerMiddleware)

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
