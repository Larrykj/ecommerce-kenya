"""
FastAPI Main Application
E-Commerce Recommendation System for Kenya
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.api.api_v1.api import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="AI-Powered E-Commerce Recommendation System for Kenya",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Middleware - Compress responses for low-bandwidth optimization
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print(f"🚀 Starting {settings.PROJECT_NAME}")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🇰🇪 Regional Features: {'Enabled' if settings.ENABLE_REGIONAL_FEATURES else 'Disabled'}")
    print(f"📊 A/B Testing: {'Enabled' if settings.ENABLE_AB_TESTING else 'Disabled'}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down gracefully...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "E-Commerce Recommendation System - Kenya Edition",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "features": {
            "user_based_filtering": True,
            "item_based_filtering": True,
            "hybrid_recommendations": True,
            "trending_items": True,
            "context_aware": True,
            "mpesa_integration": True,
            "regional_insights": settings.ENABLE_REGIONAL_FEATURES,
            "dual_language": True,
            "ab_testing": settings.ENABLE_AB_TESTING
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }

