"""
Product Pydantic Schemas for API
"""
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    name_sw: Optional[str] = None
    description: str
    description_sw: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    tags: List[str] = []
    price: float = Field(..., gt=0)
    original_price: Optional[float] = None
    currency: str = "KES"
    stock_quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    images: List[str] = []
    vendor_id: Optional[str] = None
    vendor_name: Optional[str] = None
    is_local_vendor: bool = False


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = None
    name_sw: Optional[str] = None
    description: Optional[str] = None
    description_sw: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: str
    discount_percentage: float
    in_stock: bool
    images: List[str]
    thumbnail: Optional[str]
    average_rating: float
    review_count: int
    view_count: int
    purchase_count: int
    is_featured: bool
    is_local_vendor: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for paginated product list"""
    products: List[ProductResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

