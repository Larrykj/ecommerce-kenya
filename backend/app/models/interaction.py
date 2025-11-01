"""
User-Product Interaction Model
For tracking user behavior and training ML models
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Optional MongoDB import
try:
    from bson import ObjectId
    BSON_AVAILABLE = True
except ImportError:
    BSON_AVAILABLE = False
    class ObjectId:
        @staticmethod
        def __call__():
            import uuid
            return str(uuid.uuid4())


class Interaction(BaseModel):
    """User-product interaction model"""
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    
    # Core data
    user_id: str
    product_id: str
    
    # Interaction types
    interaction_type: str  # view, click, add_to_cart, purchase, wishlist, review
    
    # Rating (for purchases/reviews)
    rating: Optional[float] = None  # 1-5 stars
    
    # Context
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None
    
    # User context
    county: Optional[str] = None
    language: str = "en"
    device_type: Optional[str] = None  # mobile, desktop, tablet
    
    # Time context
    hour_of_day: int = Field(default_factory=lambda: datetime.now().hour)
    day_of_week: int = Field(default_factory=lambda: datetime.now().weekday())
    
    # Additional metadata
    duration_seconds: Optional[int] = None  # For views
    came_from: Optional[str] = None  # recommendation, search, trending, etc.
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "product_id": "prod456",
                "interaction_type": "purchase",
                "rating": 4.5,
                "county": "Nairobi",
                "language": "en"
            }
        }

