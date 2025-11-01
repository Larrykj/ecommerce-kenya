#!/usr/bin/env python3
"""
Verify M-Pesa configuration is loaded correctly
"""
from app.core.config import settings

print("\n" + "="*60)
print("M-PESA CONFIGURATION VERIFICATION")
print("="*60 + "\n")

print(f"Environment: {settings.MPESA_ENVIRONMENT}")
print(f"Consumer Key: {settings.MPESA_CONSUMER_KEY[:20]}...")
print(f"Consumer Secret: {settings.MPESA_CONSUMER_SECRET[:20]}...")
print(f"Shortcode: {settings.MPESA_SHORTCODE}")
print(f"Passkey: {settings.MPESA_PASSKEY[:30]}...")
print(f"Callback URL: {settings.MPESA_CALLBACK_URL}")

is_configured = (
    settings.MPESA_CONSUMER_KEY and
    settings.MPESA_CONSUMER_SECRET and
    settings.MPESA_PASSKEY and
    settings.MPESA_CONSUMER_KEY != "your_consumer_key"
)

print("\n" + "="*60)
if is_configured:
    print("[SUCCESS] M-Pesa IS CONFIGURED!")
    print("\nReal M-Pesa STK Push will be sent when users checkout.")
    print("\nTest with sandbox phone: 254708374149")
else:
    print("[WARNING] M-Pesa NOT properly configured")

print("="*60 + "\n")
