"""
Yonca Rule-Based Agricultural Advisory System
FastAPI Backend Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.chatbot.routes import router as chatbot_router
from app.core.config import settings
from app.services.rule_loader import RuleLoader


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load rules on startup"""
    # Initialize rule loader and load all rules
    rule_loader = RuleLoader()
    app.state.rule_loader = rule_loader
    app.state.rules = rule_loader.load_all_rules()
    app.state.constants = rule_loader.load_constants()
    app.state.profiles = rule_loader.load_profiles()
    
    print(f"✅ Loaded {len(app.state.rules)} rule categories")
    print(f"✅ Loaded {len(app.state.constants)} constant files")
    print(f"✅ Loaded {len(app.state.profiles)} farm profiles")
    
    yield
    
    # Cleanup on shutdown
    print("👋 Shutting down Yonca API...")


app = FastAPI(
    title="Yonca Rule-Based Advisory API",
    description="Azərbaycan kənd təsərrüfatı üçün qayda əsaslı məsləhət sistemi",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - reads from environment variable CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")
app.include_router(chatbot_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Yonca Rule-Based Advisory API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rules_loaded": hasattr(app.state, 'rules'),
        "constants_loaded": hasattr(app.state, 'constants'),
        "profiles_loaded": hasattr(app.state, 'profiles')
    }
