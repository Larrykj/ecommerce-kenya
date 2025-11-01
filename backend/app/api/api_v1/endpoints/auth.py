"""
Authentication API Endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta, datetime
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from app.core.config import settings
from app.data.mock_database import mock_db

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user
    
    Creates a new user account with email and password
    """
    try:
        # Check if user already exists
        existing_user = mock_db.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user data dict
        user_dict = {
            "email": str(user_data.email),
            "username": str(user_data.username),
            "full_name": str(user_data.full_name) if user_data.full_name else "",
            "password_hash": hashed_password,
            "phone_number": str(user_data.phone_number) if user_data.phone_number else "",
            "county": str(user_data.county) if user_data.county else "Nairobi",
            "city": str(user_data.city) if user_data.city else "",
            "preferred_language": str(user_data.preferred_language) if user_data.preferred_language else "en",
            "preferred_categories": list(user_data.preferred_categories) if user_data.preferred_categories else []
        }
        
        # Create user in mock database
        new_user = mock_db.create_user(user_dict)
        
        # Parse created_at safely
        try:
            created_at = datetime.fromisoformat(new_user["created_at"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            created_at = datetime.utcnow()
        
        # Create access token
        access_token = create_access_token(
            data={"sub": new_user["id"], "email": new_user["email"]}
        )
        
        # Create user response
        user_response = UserResponse(
            id=str(new_user["id"]),
            email=str(new_user["email"]),
            username=str(new_user["username"]),
            full_name=str(new_user["full_name"]),
            phone_number=str(new_user["phone_number"]),
            county=str(new_user["county"]),
            city=str(new_user["city"]),
            preferred_language=str(new_user["preferred_language"]),
            is_active=bool(new_user["is_active"]),
            is_verified=bool(new_user["is_verified"]),
            created_at=created_at,
            preferred_categories=list(new_user.get("preferred_categories", []))
        )
        
        return Token(
            access_token=access_token,
            user=user_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Registration error: {error_details}")  # Debug log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with email and password
    
    Returns JWT access token for authenticated requests
    """
    try:
        # Find user by email
        user = mock_db.get_user_by_email(credentials.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password (using demo123 for demo users, or verify against stored hash)
        # For demo: password is "demo123" for existing users
        if not verify_password(credentials.password, user["password_hash"]):
            # Check if it's a demo password
            demo_password_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyK5vGpW1pSa"
            if credentials.password != "demo123" or user["password_hash"] != demo_password_hash:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
        
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled"
            )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user["id"], "email": user["email"]}
        )
        
        # Create user response
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            username=user["username"],
            full_name=user["full_name"],
            phone_number=user["phone_number"],
            county=user["county"],
            city=user["city"],
            preferred_language=user["preferred_language"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
            created_at=datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")),
            last_login=datetime.utcnow(),
            preferred_categories=user.get("preferred_categories", [])
        )
        
        return Token(
            access_token=access_token,
            user=user_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    try:
        user_id = current_user.get("user_id") or current_user.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user from database
        user = mock_db.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            username=user["username"],
            full_name=user["full_name"],
            phone_number=user["phone_number"],
            county=user["county"],
            city=user["city"],
            preferred_language=user["preferred_language"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
            created_at=datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")),
            preferred_categories=user.get("preferred_categories", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )

