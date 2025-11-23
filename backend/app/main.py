from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.database import init_db
from app.routes import auth, users, ingredients, recipes, favorites, diet_profiles

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered recipe generator from available ingredients",
    version=settings.APP_VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES EINBINDEN
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(ingredients.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")
app.include_router(diet_profiles.router, prefix="/api")

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
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}