"""
Products API Endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.schemas.product import ProductResponse, ProductListResponse
from app.services.redis_service import redis_service

router = APIRouter()


@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    county: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    language: str = Query("en", description="Language: en or sw")
):
    """
    List products with filtering and pagination
    
    Supports:
    - Category filtering
    - Regional filtering (county)
    - Price range filtering
    - Search
    - Bilingual display (English/Swahili)
    """
    # In production, query MongoDB with filters
    # Mock response
    return ProductListResponse(
        products=[],
        total=0,
        page=page,
        page_size=page_size,
        has_next=False,
        has_prev=False
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    language: str = Query("en")
):
    """
    Get detailed product information
    
    Returns product details in the specified language
    """
    # Track view
    await redis_service.increment_view_count(product_id)
    
    # In production, fetch from MongoDB
    # Mock response
    from datetime import datetime
    return ProductResponse(
        id=product_id,
        name="Sample Product",
        name_sw="Bidhaa ya Sampuli",
        description="A great product",
        description_sw="Bidhaa nzuri",
        category="Electronics",
        brand="TechBrand",
        tags=["smartphone", "android"],
        price=25000,
        currency="KES",
        stock_quantity=50,
        discount_percentage=0,
        in_stock=True,
        images=[],
        thumbnail=None,
        average_rating=4.5,
        review_count=120,
        view_count=1500,
        purchase_count=230,
        is_featured=False,
        is_local_vendor=True,
        created_at=datetime.utcnow()
    )


@router.get("/categories/list")
async def list_categories():
    """
    Get all product categories
    
    Returns categories in both English and Swahili
    """
    categories = [
        {"id": "electronics", "name": "Electronics", "name_sw": "Elektroniki"},
        {"id": "fashion", "name": "Fashion", "name_sw": "Mitindo"},
        {"id": "home", "name": "Home & Living", "name_sw": "Nyumbani na Maisha"},
        {"id": "beauty", "name": "Beauty & Health", "name_sw": "Urembo na Afya"},
        {"id": "food", "name": "Food & Groceries", "name_sw": "Chakula na Vitu vya Dukani"},
        {"id": "sports", "name": "Sports & Outdoors", "name_sw": "Michezo na Nje"},
        {"id": "books", "name": "Books & Media", "name_sw": "Vitabu na Vyombo vya Habari"},
        {"id": "toys", "name": "Toys & Kids", "name_sw": "Vifaa vya Kuchezea na Watoto"}
    ]
    
    return {"categories": categories}


@router.get("/vendors/local")
async def list_local_vendors(
    county: Optional[str] = None
):
    """
    List local Kenyan vendors
    
    Promotes local businesses. Can filter by county.
    """
    # In production, query vendors from database
    return {"vendors": []}

