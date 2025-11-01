#!/usr/bin/env python3
"""
Quick script to check M-Pesa configuration status
"""
import os
from dotenv import load_dotenv

load_dotenv()

def check_mpesa_config():
    print("\n" + "="*60)
    print("M-PESA CONFIGURATION STATUS CHECK")
    print("="*60 + "\n")
    
    consumer_key = os.getenv('MPESA_CONSUMER_KEY', '')
    consumer_secret = os.getenv('MPESA_CONSUMER_SECRET', '')
    passkey = os.getenv('MPESA_PASSKEY', '')
    
    # Check if credentials are placeholders
    is_configured = (
        consumer_key and 
        consumer_secret and 
        passkey and
        consumer_key != 'your_consumer_key' and
        consumer_secret != 'your_consumer_secret' and
        passkey != 'your_passkey'
    )
    
    if is_configured:
        print("[SUCCESS] M-PESA IS CONFIGURED")
        print("\nCredentials found:")
        print(f"   Consumer Key: {consumer_key[:10]}...")
        print(f"   Consumer Secret: {consumer_secret[:10]}...")
        print(f"   Passkey: {passkey[:20]}...")
        print("\n[INFO] Real M-Pesa STK Push will be sent to phones!")
    else:
        print("[WARNING] M-PESA NOT CONFIGURED (Demo Mode)")
        print("\nCurrent values:")
        print(f"   Consumer Key: {consumer_key}")
        print(f"   Consumer Secret: {consumer_secret}")
        print(f"   Passkey: {passkey}")
        print("\n[INFO] Using placeholder values - No real M-Pesa prompts will be sent")
        print("\n[ACTION] To enable real M-Pesa:")
        print("   1. Get credentials from https://developer.safaricom.co.ke/")
        print("   2. Update backend/.env with real values")
        print("   3. Restart backend server")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    check_mpesa_config()
