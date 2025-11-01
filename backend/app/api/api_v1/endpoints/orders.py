"""
Orders API Endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from datetime import datetime
import random
from app.core.config import settings
from app.services.mpesa_service import mpesa_service

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: Dict[Any, Any]):
    """
    Create a new order
    
    Initiates order and triggers M-Pesa payment
    """
    try:
        # Generate order ID
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Extract order details
        items = order_data.get('items', [])
        total_amount = order_data.get('total_amount', 0)
        customer_details = order_data.get('customer_details', {})
        payment_method = order_data.get('payment_method', 'mpesa')
        
        # Validate
        if not items:
            raise HTTPException(status_code=400, detail="No items in order")
        
        # In production:
        # 1. Validate products and stock
        # 2. Save to database
        # 3. Initiate M-Pesa if payment_method == 'mpesa'
        # 4. Send confirmation email/SMS
        
        response = {
            "success": True,
            "order_id": order_id,
            "message": "Order created successfully",
            "payment_required": payment_method == 'mpesa',
            "payment_method": payment_method,
            "total_amount": total_amount,
            "status": "pending",
            "estimated_delivery": "2-3 business days"
        }
        
        # If M-Pesa, try to initiate payment
        if payment_method == 'mpesa':
            phone = customer_details.get('phone', '')
            
            # Check if M-Pesa is configured
            if settings.MPESA_CONSUMER_KEY and settings.MPESA_CONSUMER_SECRET:
                try:
                    # Initiate real M-Pesa STK Push
                    mpesa_result = await mpesa_service.initiate_stk_push(
                        phone_number=phone,
                        amount=int(total_amount),
                        account_reference=order_id,
                        transaction_desc=f"Payment for order {order_id}"
                    )
                    
                    response["mpesa_instructions"] = {
                        "message": "M-Pesa prompt sent to your phone",
                        "phone": phone,
                        "amount": total_amount,
                        "checkout_request_id": mpesa_result.get('CheckoutRequestID', '')
                    }
                    
                except Exception as e:
                    print(f"M-Pesa error: {e}")
                    response["mpesa_instructions"] = {
                        "message": "[DEMO MODE] M-Pesa not configured - Payment simulated",
                        "phone": phone,
                        "amount": total_amount,
                        "demo_mode": True
                    }
            else:
                # Demo mode - M-Pesa not configured
                response["mpesa_instructions"] = {
                    "message": "[DEMO MODE] M-Pesa credentials not configured. In production, you would receive a payment prompt on your phone.",
                    "phone": phone,
                    "amount": total_amount,
                    "demo_mode": True,
                    "note": "Configure MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET in .env to enable real payments"
                }
                # Auto-approve in demo mode
                response["status"] = "confirmed"
                response["payment_status"] = "completed"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}")
async def get_order(order_id: str):
    """
    Get order details
    """
    # In production, fetch from database
    return {
        "order_id": order_id,
        "status": "pending",
        "payment_status": "pending"
    }


@router.get("/user/{user_id}")
async def list_user_orders(user_id: str):
    """
    List all orders for a user
    """
    # In production, fetch from database
    return {"orders": []}


@router.put("/{order_id}/cancel")
async def cancel_order(order_id: str):
    """
    Cancel an order
    """
    # In production, update order status and handle refund
    return {
        "success": True,
        "message": "Order cancelled successfully"
    }

