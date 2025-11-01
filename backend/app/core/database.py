"""
Database Connection Management
Optional - app works without database for testing
"""
from typing import Optional

# Optional database imports
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    MOTOR_AVAILABLE = True
except ImportError:
    MOTOR_AVAILABLE = False
    print("[WARNING] Motor/MongoDB not available - using mock data")

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("[WARNING] Redis not available - caching disabled")

from app.core.config import settings


class DatabaseManager:
    """Manages database connections"""
    
    def __init__(self):
        self.mongodb_client: Optional[any] = None
        self.mongodb_db: Optional[any] = None
        self.redis_client: Optional[any] = None
        
    async def connect_mongodb(self):
        """Connect to MongoDB"""
        if not MOTOR_AVAILABLE:
            print("[WARNING] MongoDB connection skipped - motor not installed")
            return
            
        try:
            self.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.mongodb_db = self.mongodb_client[settings.MONGODB_DB_NAME]
            # Test connection
            await self.mongodb_client.server_info()
            print("[SUCCESS] MongoDB connected successfully")
        except Exception as e:
            print(f"[WARNING] MongoDB connection failed: {e}")
            print("   App will run with mock data")
            self.mongodb_client = None
            self.mongodb_db = None
    
    async def connect_redis(self):
        """Connect to Redis"""
        if not REDIS_AVAILABLE:
            print("[WARNING] Redis connection skipped - redis not installed")
            return
            
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            self.redis_client.ping()
            print("[SUCCESS] Redis connected successfully")
        except Exception as e:
            print(f"[WARNING] Redis connection failed: {e}")
            print("   App will run without caching")
            self.redis_client = None
    
    async def close_mongodb(self):
        """Close MongoDB connection"""
        if self.mongodb_client:
            self.mongodb_client.close()
            print("[INFO] MongoDB disconnected")
    
    async def close_redis(self):
        """Close Redis connection"""
        if self.redis_client:
            self.redis_client.close()
            print("[INFO] Redis disconnected")


# Global database manager
db_manager = DatabaseManager()


async def get_database():
    """Dependency to get database"""
    if db_manager.mongodb_db is None:
        return None
    return db_manager.mongodb_db


async def get_redis():
    """Dependency to get redis"""
    if db_manager.redis_client is None:
        return None
    return db_manager.redis_client

