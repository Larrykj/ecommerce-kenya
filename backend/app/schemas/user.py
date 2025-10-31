"""
User Pydantic Schemas for API
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    preferred_language: str = "en"


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)
    mpesa_phone_number: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    preferred_language: Optional[str] = None
    mpesa_phone_number: Optional[str] = None
    preferred_categories: Optional[List[str]] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    preferred_categories: List[str] = []
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

