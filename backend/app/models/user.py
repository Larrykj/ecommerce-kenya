"""
User Database Model
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Optional MongoDB import
try:
    from bson import ObjectId as BsonObjectId
    BSON_AVAILABLE = True
except ImportError:
    BSON_AVAILABLE = False
    class BsonObjectId:
        @staticmethod
        def is_valid(v):
            return True
        def __init__(self, *args, **kwargs):
            import uuid
            self._id = str(uuid.uuid4())
        def __str__(self):
            return self._id


class PyObjectId(BsonObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    """User model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    
    # Location
    county: Optional[str] = None
    city: Optional[str] = None
    
    # Preferences
    preferred_language: str = "en"  # en or sw
    preferred_categories: List[str] = []
    
    # Activity
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Behavioral data
    viewed_products: List[str] = []
    purchased_products: List[str] = []
    search_history: List[str] = []
    
    # M-Pesa
    mpesa_phone_number: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "phone_number": "+254712345678",
                "county": "Nairobi",
                "preferred_language": "en"
            }
        }

