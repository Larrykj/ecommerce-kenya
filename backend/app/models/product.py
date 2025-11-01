"""
Product Database Model
"""
from typing import List, Optional, Dict
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


class Product(BaseModel):
    """Product model"""
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    
    # Basic Info
    name: str
    name_sw: Optional[str] = None  # Swahili translation
    description: str
    description_sw: Optional[str] = None
    
    # Categorization
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    tags: List[str] = []
    
    # Pricing
    price: float
    original_price: Optional[float] = None  # For discounts
    currency: str = "KES"
    discount_percentage: float = 0.0
    
    # Inventory
    stock_quantity: int = 0
    in_stock: bool = True
    
    # Media
    images: List[str] = []
    thumbnail: Optional[str] = None
    
    # Reviews & Ratings
    average_rating: float = 0.0
    review_count: int = 0
    ratings: Dict[str, int] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    
    # Regional Data
    popular_counties: List[str] = []  # Counties where product is popular
    
    # Vendor Info
    vendor_id: Optional[str] = None
    vendor_name: Optional[str] = None
    is_local_vendor: bool = False  # Kenyan vendor
    
    # Analytics
    view_count: int = 0
    purchase_count: int = 0
    add_to_cart_count: int = 0
    
    # Context-Aware
    seasonal: bool = False  # Seasonal product
    season_tags: List[str] = []  # e.g., ["rainy_season", "christmas"]
    time_of_day_preference: Optional[str] = None  # morning, afternoon, evening
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    is_featured: bool = False
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Smartphone XYZ",
                "name_sw": "Simu XYZ",
                "description": "High-quality smartphone",
                "category": "Electronics",
                "brand": "TechBrand",
                "price": 25000,
                "currency": "KES",
                "stock_quantity": 50,
                "vendor_name": "Nairobi Electronics",
                "is_local_vendor": True
            }
        }

