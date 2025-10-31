"""
Authentication API Endpoints
"""
from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user
    
    Creates a new user account with email and password
    """
    try:
        # In production, check if user exists in database
        # For now, return mock response
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user (would save to DB)
        user_id = "mock_user_id_123"
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_id, "email": user_data.email}
        )
        
        # Mock user response
        user_response = UserResponse(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            county=user_data.county,
            city=user_data.city,
            preferred_language=user_data.preferred_language,
            is_active=True,
            is_verified=False,
            created_at=datetime.utcnow(),
            preferred_categories=[]
        )
        
        return Token(
            access_token=access_token,
            user=user_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with email and password
    
    Returns JWT access token for authenticated requests
    """
    try:
        # In production, fetch user from database and verify password
        # For now, mock response
        
        # Mock user data
        user_id = "mock_user_id_123"
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_id, "email": credentials.email}
        )
        
        # Mock user response
        from datetime import datetime
        user_response = UserResponse(
            id=user_id,
            email=credentials.email,
            username="johndoe",
            full_name="John Doe",
            phone_number="+254712345678",
            county="Nairobi",
            city="Nairobi",
            preferred_language="en",
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow(),
            preferred_categories=["Electronics", "Fashion"]
        )
        
        return Token(
            access_token=access_token,
            user=user_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    # In production, decode token and fetch user from database
    # Mock response for now
    from datetime import datetime
    return UserResponse(
        id="mock_user_id_123",
        email="user@example.com",
        username="johndoe",
        full_name="John Doe",
        phone_number="+254712345678",
        county="Nairobi",
        city="Nairobi",
        preferred_language="en",
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow(),
        preferred_categories=["Electronics", "Fashion"]
    )

