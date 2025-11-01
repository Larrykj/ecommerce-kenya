"""
Configuration Settings
Loads environment variables and application settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "E-Commerce Recommendation System Kenya"
    ENVIRONMENT: str = "development"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://localhost:8080"
    ]
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "ecommerce_kenya"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # M-Pesa Configuration
    MPESA_ENVIRONMENT: str = "sandbox"  # sandbox or production
    MPESA_CONSUMER_KEY: str = ""
    MPESA_CONSUMER_SECRET: str = ""
    MPESA_SHORTCODE: str = "174379"
    MPESA_PASSKEY: str = ""
    MPESA_CALLBACK_URL: str = ""
    
    # ML Model Configuration
    MIN_RECOMMENDATIONS: int = 5
    MAX_RECOMMENDATIONS: int = 20
    MODEL_RETRAIN_INTERVAL: int = 86400  # 24 hours in seconds
    MIN_RATINGS_FOR_RECOMMENDATION: int = 3
    KNN_NEIGHBORS: int = 20
    SVD_FACTORS: int = 50
    
    # Feature Flags
    ENABLE_KAFKA: bool = False
    ENABLE_AB_TESTING: bool = True
    ENABLE_REGIONAL_FEATURES: bool = True
    ENABLE_OFFLINE_MODE: bool = True
    
    # Cache Configuration
    CACHE_TTL: int = 3600  # 1 hour
    TRENDING_ITEMS_CACHE_TTL: int = 300  # 5 minutes
    
    # Kenya Counties (47 counties)
    KENYA_COUNTIES: List[str] = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
        "Thika", "Malindi", "Kitale", "Garissa", "Kakamega",
        "Nyeri", "Meru", "Machakos", "Kiambu", "Kajiado",
        "Narok", "Kisii", "Kericho", "Bomet", "Bungoma",
        "Migori", "Homa Bay", "Siaya", "Busia", "Vihiga",
        "Baringo", "Laikipia", "Nyandarua", "Murang'a", "Embu",
        "Tharaka-Nithi", "Kirinyaga", "Mombasa", "Kwale", "Kilifi",
        "Tana River", "Lamu", "Taita-Taveta", "Wajir", "Mandera",
        "Marsabit", "Isiolo", "Samburu", "Trans-Nzoia", "Uasin Gishu",
        "Elgeyo-Marakwet", "Nandi", "West Pokot", "Turkana"
    ]
    
    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "sw"]  # English, Swahili
    DEFAULT_LANGUAGE: str = "en"
    
    # Analytics
    GOOGLE_ANALYTICS_ID: Optional[str] = None
    ENABLE_CUSTOM_ANALYTICS: bool = True
    
    # AWS Configuration (Optional)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

