"""
M-Pesa Payment API Endpoints
"""
from fastapi import APIRouter, HTTPException, Body
from typing import Dict
from app.services.mpesa_service import mpesa_service

router = APIRouter()


@router.post("/stk-push")
async def initiate_stk_push(
    phone_number: str = Body(..., description="Phone number (254XXXXXXXXX)"),
    amount: int = Body(..., description="Amount in KES"),
    order_id: str = Body(..., description="Order ID / Reference")
):
    """
    Initiate M-Pesa STK Push payment
    
    Sends payment prompt to customer's phone
    
    **Phone Format**: 254XXXXXXXXX (Kenyan format)
    """
    try:
        result = await mpesa_service.initiate_stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=order_id,
            transaction_desc=f"Payment for order {order_id}"
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"M-Pesa payment failed: {str(e)}"
        )


@router.get("/query/{checkout_request_id}")
async def query_payment_status(checkout_request_id: str):
    """
    Query M-Pesa payment status
    
    Check if payment was completed successfully
    """
    try:
        result = await mpesa_service.query_stk_status(checkout_request_id)
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )


@router.post("/callback")
async def mpesa_callback(callback_data: Dict = Body(...)):
    """
    M-Pesa callback endpoint
    
    Receives payment confirmation from Safaricom
    
    **Note**: This endpoint is called by Safaricom's servers
    """
    try:
        result = await mpesa_service.process_callback(callback_data)
        
        if result.get('success'):
            # Update order status in database
            # Send confirmation email/SMS
            print(f"✅ Payment successful: {result}")
        else:
            # Handle failed payment
            print(f"❌ Payment failed: {result}")
        
        # Return success to Safaricom
        return {
            "ResultCode": 0,
            "ResultDesc": "Success"
        }
    
    except Exception as e:
        print(f"Callback error: {e}")
        return {
            "ResultCode": 1,
            "ResultDesc": "Failed"
        }

