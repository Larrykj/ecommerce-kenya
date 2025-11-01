"""
FastAPI Main Application
E-Commerce Recommendation System for Kenya
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_router

# Optional imports
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    print("[WARNING] Prometheus not available - metrics disabled")

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

# Prometheus metrics (optional)
if PROMETHEUS_AVAILABLE:
    try:
        Instrumentator().instrument(app).expose(app)
    except Exception as e:
        print(f"[WARNING] Prometheus setup failed: {e}")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("=" * 60)
    print(f"[STARTUP] Starting {settings.PROJECT_NAME}")
    print(f"[INFO] Environment: {settings.ENVIRONMENT}")
    print(f"[INFO] Regional Features: {'Enabled' if settings.ENABLE_REGIONAL_FEATURES else 'Disabled'}")
    print(f"[INFO] A/B Testing: {'Enabled' if settings.ENABLE_AB_TESTING else 'Disabled'}")
    print("=" * 60)
    
    # Try to connect to databases (optional)
    try:
        from app.core.database import db_manager
        await db_manager.connect_mongodb()
        await db_manager.connect_redis()
    except Exception as e:
        print(f"[WARNING] Database connection error: {e}")
        print("   App will continue with mock data")
    
    print("=" * 60)
    print("[SUCCESS] Application ready!")
    print(f"[INFO] API Docs: http://localhost:8000/docs")
    print(f"[INFO] Health: http://localhost:8000/health")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("=" * 60)
    print("[SHUTDOWN] Shutting down gracefully...")
    
    try:
        from app.core.database import db_manager
        await db_manager.close_mongodb()
        await db_manager.close_redis()
    except:
        pass
    
    print("[SUCCESS] Shutdown complete")
    print("=" * 60)


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

