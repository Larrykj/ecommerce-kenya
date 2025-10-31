"""
M-Pesa Payment Integration Service
Handles STK Push and payment verification for Kenyan mobile payments
"""
import requests
import base64
from datetime import datetime
from typing import Optional, Dict
import asyncio
from app.core.config import settings


class MPesaService:
    """M-Pesa payment integration service"""
    
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        
        # URLs based on environment
        if settings.MPESA_ENVIRONMENT == "production":
            self.base_url = "https://api.safaricom.co.ke"
        else:
            self.base_url = "https://sandbox.safaricom.co.ke"
        
        self.access_token = None
        self.token_expiry = None
    
    async def get_access_token(self) -> Optional[str]:
        """
        Get OAuth access token from M-Pesa API
        
        Returns:
            Access token string or None if failed
        """
        # Check if we have a valid token
        if self.access_token and self.token_expiry:
            if datetime.now() < self.token_expiry:
                return self.access_token
        
        # Get new token
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        
        # Create authorization header
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            "Authorization": f"Basic {auth_b64}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data['access_token']
            # Token typically expires in 3600 seconds
            from datetime import timedelta
            self.token_expiry = datetime.now() + timedelta(seconds=3500)
            
            return self.access_token
        
        except Exception as e:
            print(f"Error getting M-Pesa access token: {e}")
            return None
    
    async def initiate_stk_push(
        self,
        phone_number: str,
        amount: int,
        account_reference: str,
        transaction_desc: str
    ) -> Dict:
        """
        Initiate STK Push (Lipa Na M-Pesa Online)
        
        Args:
            phone_number: Customer phone number (format: 254XXXXXXXXX)
            amount: Amount to charge (minimum 1 KES)
            account_reference: Order number or reference
            transaction_desc: Description of transaction
            
        Returns:
            Response dictionary with status and details
        """
        access_token = await self.get_access_token()
        
        if not access_token:
            return {
                "success": False,
                "message": "Failed to get M-Pesa access token"
            }
        
        # Format phone number
        if phone_number.startswith("+"):
            phone_number = phone_number[1:]
        if phone_number.startswith("0"):
            phone_number = f"254{phone_number[1:]}"
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Generate password
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        password_bytes = password_string.encode('ascii')
        password_b64 = base64.b64encode(password_bytes).decode('ascii')
        
        # Prepare request
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password_b64,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('ResponseCode') == '0':
                return {
                    "success": True,
                    "message": "STK Push initiated successfully",
                    "checkout_request_id": data.get('CheckoutRequestID'),
                    "merchant_request_id": data.get('MerchantRequestID'),
                    "customer_message": data.get('CustomerMessage')
                }
            else:
                return {
                    "success": False,
                    "message": data.get('ResponseDescription', 'STK Push failed'),
                    "error_code": data.get('ResponseCode')
                }
        
        except Exception as e:
            print(f"Error initiating STK Push: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    async def query_stk_status(
        self,
        checkout_request_id: str
    ) -> Dict:
        """
        Query STK Push transaction status
        
        Args:
            checkout_request_id: CheckoutRequestID from STK Push response
            
        Returns:
            Status dictionary
        """
        access_token = await self.get_access_token()
        
        if not access_token:
            return {
                "success": False,
                "message": "Failed to get M-Pesa access token"
            }
        
        # Generate timestamp and password
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        password_bytes = password_string.encode('ascii')
        password_b64 = base64.b64encode(password_bytes).decode('ascii')
        
        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password_b64,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "result_code": data.get('ResultCode'),
                "result_desc": data.get('ResultDesc'),
                "status": "completed" if data.get('ResultCode') == '0' else "pending"
            }
        
        except Exception as e:
            print(f"Error querying STK status: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    async def process_callback(self, callback_data: Dict) -> Dict:
        """
        Process M-Pesa callback data
        
        Args:
            callback_data: Callback payload from M-Pesa
            
        Returns:
            Processed transaction data
        """
        try:
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            
            if result_code == 0:
                # Payment successful
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                
                # Extract payment details
                payment_data = {}
                for item in callback_metadata:
                    name = item.get('Name')
                    value = item.get('Value')
                    payment_data[name] = value
                
                return {
                    "success": True,
                    "result_code": result_code,
                    "result_desc": result_desc,
                    "amount": payment_data.get('Amount'),
                    "mpesa_receipt_number": payment_data.get('MpesaReceiptNumber'),
                    "transaction_date": payment_data.get('TransactionDate'),
                    "phone_number": payment_data.get('PhoneNumber')
                }
            else:
                # Payment failed or cancelled
                return {
                    "success": False,
                    "result_code": result_code,
                    "result_desc": result_desc
                }
        
        except Exception as e:
            print(f"Error processing callback: {e}")
            return {
                "success": False,
                "message": f"Error processing callback: {str(e)}"
            }


# Global instance
mpesa_service = MPesaService()

