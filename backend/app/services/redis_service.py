"""
Redis Caching Service
For fast access to recommendations and trending items
"""
import json
from typing import Optional, List, Dict, Any
from datetime import timedelta, datetime
from app.core.config import settings

# Optional Redis import
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not available - caching disabled")


class RedisService:
    """Redis caching service for recommendations and trending data"""
    
    def __init__(self):
        self.redis_client = None
        self.connect()
    
    def connect(self):
        """Connect to Redis"""
        if not REDIS_AVAILABLE:
            print("[WARNING] Redis package not installed - caching disabled")
            self.redis_client = None
            return
            
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            print("[SUCCESS] Connected to Redis")
        except Exception as e:
            print(f"[WARNING] Redis connection failed: {e}")
            print("   App will run without caching")
            self.redis_client = None
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if self.redis_client is None:
            return False
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self.is_connected():
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            Success status
        """
        if not self.is_connected():
            return False
        
        try:
            serialized = json.dumps(value)
            if ttl:
                self.redis_client.setex(key, ttl, serialized)
            else:
                self.redis_client.set(key, serialized)
            return True
        except Exception as e:
            print(f"Redis SET error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.is_connected():
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis DELETE error: {e}")
            return False
    
    async def get_user_recommendations(
        self,
        user_id: str,
        algorithm: str = "hybrid"
    ) -> Optional[List[Dict]]:
        """Get cached user recommendations"""
        key = f"recommendations:user:{user_id}:{algorithm}"
        return await self.get(key)
    
    async def cache_user_recommendations(
        self,
        user_id: str,
        recommendations: List[Dict],
        algorithm: str = "hybrid",
        ttl: int = 3600
    ) -> bool:
        """Cache user recommendations"""
        key = f"recommendations:user:{user_id}:{algorithm}"
        return await self.set(key, recommendations, ttl)
    
    async def get_similar_products(
        self,
        product_id: str
    ) -> Optional[List[Dict]]:
        """Get cached similar products"""
        key = f"recommendations:similar:{product_id}"
        return await self.get(key)
    
    async def cache_similar_products(
        self,
        product_id: str,
        similar_products: List[Dict],
        ttl: int = 7200
    ) -> bool:
        """Cache similar products"""
        key = f"recommendations:similar:{product_id}"
        return await self.set(key, similar_products, ttl)
    
    async def get_trending_products(
        self,
        category: Optional[str] = None,
        county: Optional[str] = None,
        time_window: str = "24h"
    ) -> Optional[List[Dict]]:
        """Get cached trending products"""
        key_parts = ["trending", time_window]
        if category:
            key_parts.append(f"cat:{category}")
        if county:
            key_parts.append(f"county:{county}")
        key = ":".join(key_parts)
        return await self.get(key)
    
    async def cache_trending_products(
        self,
        trending_products: List[Dict],
        category: Optional[str] = None,
        county: Optional[str] = None,
        time_window: str = "24h",
        ttl: int = 300
    ) -> bool:
        """Cache trending products"""
        key_parts = ["trending", time_window]
        if category:
            key_parts.append(f"cat:{category}")
        if county:
            key_parts.append(f"county:{county}")
        key = ":".join(key_parts)
        return await self.set(key, trending_products, ttl)
    
    async def increment_view_count(self, product_id: str) -> int:
        """Increment product view count"""
        if not self.is_connected() or not REDIS_AVAILABLE:
            return 0
        
        try:
            key = f"views:product:{product_id}"
            count = self.redis_client.incr(key)
            # Set expiry of 24 hours if new key
            if count == 1:
                self.redis_client.expire(key, 86400)
            return count
        except Exception as e:
            print(f"Redis INCR error: {e}")
            return 0
    
    async def add_to_search_suggestions(
        self,
        query: str,
        language: str = "en"
    ):
        """Add search query to suggestions"""
        if not self.is_connected() or not REDIS_AVAILABLE:
            return
        
        try:
            key = f"search_suggestions:{language}"
            # Use sorted set with score being the count
            self.redis_client.zincrby(key, 1, query.lower())
            # Keep only top 1000 suggestions
            self.redis_client.zremrangebyrank(key, 0, -1001)
        except Exception as e:
            print(f"Redis search suggestion error: {e}")
    
    async def get_search_suggestions(
        self,
        prefix: str,
        language: str = "en",
        limit: int = 5
    ) -> List[str]:
        """Get search suggestions"""
        if not self.is_connected() or not REDIS_AVAILABLE:
            return []
        
        try:
            key = f"search_suggestions:{language}"
            # Get all suggestions and filter by prefix
            all_suggestions = self.redis_client.zrevrange(key, 0, -1)
            matching = [
                s for s in all_suggestions
                if s.startswith(prefix.lower())
            ]
            return matching[:limit]
        except Exception as e:
            print(f"Redis get suggestions error: {e}")
            return []
    
    async def track_user_activity(
        self,
        user_id: str,
        activity_type: str,
        product_id: Optional[str] = None
    ):
        """Track user activity in real-time"""
        if not self.is_connected() or not REDIS_AVAILABLE:
            return
        
        try:
            # Add to user's recent activity stream
            key = f"activity:user:{user_id}"
            activity = {
                "type": activity_type,
                "product_id": product_id,
                "timestamp": str(datetime.now())
            }
            self.redis_client.lpush(key, json.dumps(activity))
            # Keep only last 100 activities
            self.redis_client.ltrim(key, 0, 99)
            # Set expiry of 7 days
            self.redis_client.expire(key, 604800)
        except Exception as e:
            print(f"Redis activity tracking error: {e}")
    
    def close(self):
        """Close Redis connection"""
        if self.redis_client:
            self.redis_client.close()


# Global instance
redis_service = RedisService()

