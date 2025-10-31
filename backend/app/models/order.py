"""
Order Database Model
"""
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class OrderItem(BaseModel):
    """Individual item in an order"""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float


class Order(BaseModel):
    """Order model"""
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    
    # User info
    user_id: str
    user_email: str
    user_phone: str
    
    # Order details
    order_number: str
    items: List[OrderItem]
    
    # Pricing
    subtotal: float
    tax: float = 0.0
    shipping_cost: float
    discount: float = 0.0
    total_amount: float
    currency: str = "KES"
    
    # Delivery
    delivery_county: str
    delivery_city: str
    delivery_address: str
    delivery_notes: Optional[str] = None
    
    # Status
    status: str = "pending"  # pending, confirmed, processing, shipped, delivered, cancelled
    payment_status: str = "pending"  # pending, paid, failed, refunded
    
    # M-Pesa payment
    mpesa_transaction_id: Optional[str] = None
    mpesa_phone_number: Optional[str] = None
    mpesa_receipt_number: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    # Tracking
    tracking_number: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "user_email": "user@example.com",
                "user_phone": "+254712345678",
                "order_number": "ORD-2024-001",
                "total_amount": 5000,
                "delivery_county": "Nairobi",
                "status": "pending",
                "payment_status": "pending"
            }
        }

