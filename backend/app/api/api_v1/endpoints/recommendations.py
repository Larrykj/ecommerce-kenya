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
        # Check cache first
        cached_recs = await redis_service.get_user_recommendations(user_id, algorithm)
        if cached_recs:
            return RecommendationResponse(
                products=[],  # Would need to fetch full product details
                algorithm_used=algorithm,
                explanation="Personalized recommendations based on your activity"
            )
        
        # Get recommendations from ML service
        recommendations = await recommendation_service.get_personalized_recommendations(
            user_id=user_id,
            n_recommendations=limit,
            algorithm=algorithm
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail="No recommendations available. User may need more interaction history."
            )
        
        # Cache results
        await redis_service.cache_user_recommendations(
            user_id, recommendations, algorithm
        )
        
        # Track view
        await redis_service.track_user_activity(user_id, "view_recommendations")
        
        return RecommendationResponse(
            products=[],  # Would fetch full product details from DB
            algorithm_used=algorithm,
            confidence_scores=[r['score'] for r in recommendations],
            explanation=f"These recommendations were generated using {algorithm} algorithm based on your browsing and purchase history."
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


@router.post("/trending", response_model=RecommendationResponse)
async def get_trending_products(
    time_window: str = Query("24h", description="Time window: 1h, 24h, 7d, 30d"),
    county: Optional[str] = Query(None, description="Filter by county"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get trending products based on recent user activity
    
    Supports regional filtering (county-based) and category filtering
    """
    try:
        # Check cache
        cached_trending = await redis_service.get_trending_products(
            category, county, time_window
        )
        if cached_trending:
            return RecommendationResponse(
                products=[],
                algorithm_used="trending",
                explanation=f"Trending products in the last {time_window}"
            )
        
        # Get trending products (would need actual interactions from DB)
        trending = await recommendation_service.get_trending_products(
            interactions=[],  # Would fetch from database
            time_window=time_window,
            county=county,
            category=category,
            n_items=limit
        )
        
        # Cache results (shorter TTL for trending)
        await redis_service.cache_trending_products(
            trending, category, county, time_window
        )
        
        county_text = f" in {county}" if county else " nationwide"
        category_text = f" in {category}" if category else ""
        
        return RecommendationResponse(
            products=[],
            algorithm_used="trending",
            explanation=f"Most popular products{county_text}{category_text} in the last {time_window}"
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

