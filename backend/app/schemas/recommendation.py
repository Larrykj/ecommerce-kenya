"""
Recommendation Pydantic Schemas
"""
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.product import ProductResponse


class RecommendationRequest(BaseModel):
    """Schema for recommendation request"""
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    category: Optional[str] = None
    limit: int = 10
    algorithm: str = "hybrid"  # user_based, item_based, hybrid, trending


class RecommendationResponse(BaseModel):
    """Schema for recommendation response"""
    products: List[ProductResponse]
    algorithm_used: str
    confidence_scores: Optional[List[float]] = None
    explanation: Optional[str] = None


class TrendingRequest(BaseModel):
    """Schema for trending items request"""
    county: Optional[str] = None
    category: Optional[str] = None
    time_window: str = "24h"  # 1h, 24h, 7d, 30d
    limit: int = 10


class SearchSuggestionRequest(BaseModel):
    """Schema for search suggestions"""
    query: str
    limit: int = 5
    language: str = "en"


class SearchSuggestionResponse(BaseModel):
    """Schema for search suggestion response"""
    suggestions: List[str]
    products: List[ProductResponse]

