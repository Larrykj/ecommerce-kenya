"""
API Router
Combines all API endpoints
"""
from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    products,
    recommendations,
    orders,
    mpesa,
    analytics
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(mpesa.router, prefix="/mpesa", tags=["M-Pesa Payment"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

