"""
Products API Endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.schemas.product import ProductResponse, ProductListResponse
from app.services.redis_service import redis_service
from app.data.mock_database import mock_db
from datetime import datetime

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
    try:
        offset = (page - 1) * page_size
        products = mock_db.get_products(
            category=category,
            county=county,
            search=search,
            min_price=min_price,
            max_price=max_price,
            limit=page_size,
            offset=offset
        )
        
        # Convert to response format
        product_responses = []
        for p in products:
            product_responses.append(ProductResponse(
                id=p["id"],
                name=p["name"] if language == "en" else p.get("name_sw", p["name"]),
                name_sw=p.get("name_sw", p["name"]),
                description=p["description"] if language == "en" else p.get("description_sw", p["description"]),
                description_sw=p.get("description_sw", p["description"]),
                category=p["category"],
                brand=p.get("vendor_name", ""),
                tags=p.get("tags", []),
                price=p["price"],
                currency=p.get("currency", "KES"),
                stock_quantity=p.get("stock", 0),
                discount_percentage=0,
                in_stock=p.get("stock", 0) > 0,
                images=p.get("images", []),
                thumbnail=p.get("images", [""])[0] if p.get("images") else None,
                average_rating=p.get("rating", 0.0),
                review_count=p.get("review_count", 0),
                view_count=0,
                purchase_count=0,
                is_featured=False,
                is_local_vendor=True,
                created_at=datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
            ))
        
        # Get total count for pagination
        all_products = mock_db.get_products(
            category=category,
            county=county,
            search=search,
            min_price=min_price,
            max_price=max_price,
            limit=10000,
            offset=0
        )
        total = len(all_products)
        
        return ProductListResponse(
            products=product_responses,
            total=total,
            page=page,
            page_size=page_size,
            has_next=(offset + page_size) < total,
            has_prev=page > 1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    language: str = Query("en")
):
    """
    Get detailed product information
    
    Returns product details in the specified language
    """
    try:
        # Track view
        await redis_service.increment_view_count(product_id)
        
        # Get product from mock database
        product = mock_db.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            id=product["id"],
            name=product["name"] if language == "en" else product.get("name_sw", product["name"]),
            name_sw=product.get("name_sw", product["name"]),
            description=product["description"] if language == "en" else product.get("description_sw", product["description"]),
            description_sw=product.get("description_sw", product["description"]),
            category=product["category"],
            brand=product.get("vendor_name", ""),
            tags=product.get("tags", []),
            price=product["price"],
            currency=product.get("currency", "KES"),
            stock_quantity=product.get("stock", 0),
            discount_percentage=0,
            in_stock=product.get("stock", 0) > 0,
            images=product.get("images", []),
            thumbnail=product.get("images", [""])[0] if product.get("images") else None,
            average_rating=product.get("rating", 0.0),
            review_count=product.get("review_count", 0),
            view_count=0,
            purchase_count=0,
            is_featured=False,
            is_local_vendor=True,
            created_at=datetime.fromisoformat(product["created_at"].replace("Z", "+00:00"))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        vendors = mock_db.get_vendors(county=county)
        return {"vendors": vendors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

