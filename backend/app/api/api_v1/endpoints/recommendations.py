"""
Recommendation API Endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    TrendingRequest,
    SearchSuggestionRequest,
    SearchSuggestionResponse
)
from app.schemas.product import ProductResponse
from app.services.recommendation_service import recommendation_service
from app.services.redis_service import redis_service
from app.data.mock_database import mock_db
from datetime import datetime

router = APIRouter()


@router.post("/personalized", response_model=RecommendationResponse)
async def get_personalized_recommendations(
    user_id: str = Query(..., description="User ID"),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    algorithm: str = Query("hybrid", description="Algorithm: user_based, item_based, hybrid, matrix_factorization")
):
    """
    Get personalized product recommendations for a user
    
    Algorithms:
    - **user_based**: Collaborative filtering based on similar users
    - **item_based**: Recommendations based on similar products
    - **hybrid**: Combines collaborative and content-based filtering (recommended)
    - **matrix_factorization**: SVD-based latent feature model
    """
    try:
        # Get user interactions to understand preferences
        interactions = mock_db.get_user_interactions(user_id)
        user = mock_db.get_user_by_id(user_id)
        
        # Get user preferred categories
        preferred_categories = user.get("preferred_categories", []) if user else []
        
        # Get recommendations from ML service (fallback to mock if not available)
        try:
            recommendations = await recommendation_service.get_personalized_recommendations(
                user_id=user_id,
                n_recommendations=limit,
                algorithm=algorithm
            )
        except:
            recommendations = None
        
        # If ML service not available, use simple recommendation based on preferences
        if not recommendations:
            # Filter products by user's preferred categories or get trending
            if preferred_categories:
                products = mock_db.get_products(category=preferred_categories[0], limit=limit)
            else:
                products = mock_db.get_trending_products(limit=limit)
        else:
            # Map recommendation IDs to products
            product_ids = [r.get('product_id', '') for r in recommendations if isinstance(r, dict)]
            products = [mock_db.get_product_by_id(pid) for pid in product_ids if pid]
            products = [p for p in products if p]  # Remove None values
        
        # Convert to ProductResponse format
        product_responses = []
        for p in products[:limit]:
            if p:
                product_responses.append(ProductResponse(
                    id=p["id"],
                    name=p["name"],
                    name_sw=p.get("name_sw", p["name"]),
                    description=p["description"],
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
        
        return RecommendationResponse(
            products=product_responses,
            algorithm_used=algorithm if recommendations else "preference_based",
            explanation=f"Personalized recommendations based on your preferences and activity"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar/{product_id}", response_model=RecommendationResponse)
async def get_similar_products(
    product_id: str,
    limit: int = Query(10, ge=1, le=50),
    algorithm: str = Query("item_based", description="Algorithm to use")
):
    """
    Get products similar to a given product
    
    Perfect for "You may also like" sections and product pages
    """
    try:
        # Check cache
        cached_similar = await redis_service.get_similar_products(product_id)
        if cached_similar:
            return RecommendationResponse(
                products=[],
                algorithm_used=algorithm,
                explanation="Products similar to this item"
            )
        
        # Get similar products
        similar_products = await recommendation_service.get_similar_products(
            product_id=product_id,
            n_similar=limit,
            algorithm=algorithm
        )
        
        if not similar_products:
            raise HTTPException(
                status_code=404,
                detail="No similar products found"
            )
        
        # Cache results
        await redis_service.cache_similar_products(product_id, similar_products)
        
        return RecommendationResponse(
            products=[],
            algorithm_used=algorithm,
            confidence_scores=[p['similarity'] for p in similar_products],
            explanation="Products similar to the one you're viewing"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending", response_model=RecommendationResponse)
async def get_trending_products(
    county: Optional[str] = Query(None, description="Filter by county"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get trending products based on recent user activity
    
    Supports regional filtering (county-based)
    """
    try:
        # Get trending products from mock database
        products = mock_db.get_trending_products(county=county, limit=limit)
        
        # Convert to ProductResponse format
        product_responses = []
        for p in products:
            product_responses.append(ProductResponse(
                id=p["id"],
                name=p["name"],
                name_sw=p.get("name_sw", p["name"]),
                description=p["description"],
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
        
        county_text = f" in {county}" if county else " nationwide"
        
        return RecommendationResponse(
            products=product_responses,
            algorithm_used="trending",
            explanation=f"Most popular products{county_text} based on ratings and reviews"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bundle")
async def get_frequently_bought_together(
    product_ids: List[str] = Query(..., description="Product IDs in cart"),
    limit: int = Query(5, ge=1, le=20)
):
    """
    Get products frequently bought together with the given products
    
    Perfect for "Frequently bought together" and bundle suggestions
    """
    try:
        bundle_recs = await recommendation_service.get_frequently_bought_together(
            product_ids=product_ids,
            n_recommendations=limit
        )
        
        return {
            "bundle_recommendations": bundle_recs,
            "explanation": "Products frequently bought together"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/context-aware", response_model=RecommendationResponse)
async def get_context_aware_recommendations(
    user_id: str = Query(...),
    time_of_day: Optional[str] = Query(None, description="morning, afternoon, evening, night"),
    county: Optional[str] = Query(None),
    season: Optional[str] = Query(None, description="rainy, dry, festive"),
    weather: Optional[str] = Query(None, description="sunny, rainy, cold"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get context-aware recommendations based on time, location, and season
    
    Takes into account:
    - Time of day (morning coffee vs evening snacks)
    - Location (county-specific preferences)
    - Season (rainy season gear, festive items)
    - Weather conditions
    """
    try:
        context = {
            "time_of_day": time_of_day,
            "county": county,
            "season": season,
            "weather": weather
        }
        
        recommendations = await recommendation_service.get_context_aware_recommendations(
            user_id=user_id,
            context=context,
            n_recommendations=limit
        )
        
        return RecommendationResponse(
            products=[],
            algorithm_used="context_aware",
            explanation="Recommendations tailored to your current context"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/suggestions", response_model=SearchSuggestionResponse)
async def get_search_suggestions(
    query: str = Query(..., min_length=2),
    language: str = Query("en", description="Language: en or sw"),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Get search auto-suggestions
    
    Returns popular search queries matching the prefix
    """
    try:
        suggestions = await redis_service.get_search_suggestions(
            prefix=query,
            language=language,
            limit=limit
        )
        
        # Track this search
        await redis_service.add_to_search_suggestions(query, language)
        
        return SearchSuggestionResponse(
            suggestions=suggestions,
            products=[]  # Would also return matching products
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/homepage/{user_id}")
async def get_personalized_homepage(
    user_id: str,
    county: Optional[str] = None
):
    """
    Get a complete personalized homepage feed
    
    Includes:
    - Personalized recommendations
    - Trending in your area
    - Recently viewed
    - Seasonal picks
    """
    try:
        # Get multiple recommendation types
        personalized = await recommendation_service.get_personalized_recommendations(
            user_id, n_recommendations=10, algorithm="hybrid"
        )
        
        trending = await recommendation_service.get_trending_products(
            interactions=[],
            time_window="24h",
            county=county,
            n_items=10
        )
        
        # Context-aware
        context = {"county": county, "time_of_day": "afternoon"}
        context_aware = await recommendation_service.get_context_aware_recommendations(
            user_id, context, n_recommendations=10
        )
        
        return {
            "sections": {
                "for_you": personalized,
                "trending_nearby": trending,
                "smart_picks": context_aware,
                "local_vendors": []  # Would filter for local vendors
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

