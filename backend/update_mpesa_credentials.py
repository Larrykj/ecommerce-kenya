#!/usr/bin/env python3
"""
Quick script to update M-Pesa credentials in .env file
Run this after you get your credentials from Daraja Portal
"""

def update_mpesa_credentials():
    print("\n" + "="*60)
    print("M-PESA CREDENTIALS SETUP TOOL")
    print("="*60 + "\n")
    
    print("Please enter your credentials from Safaricom Daraja Portal:\n")
    
    # Get credentials from user
    consumer_key = input("Consumer Key: ").strip()
    consumer_secret = input("Consumer Secret: ").strip()
    
    print("\nFor Sandbox testing, use these defaults:")
    print("Shortcode: 174379")
    print("Passkey: bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919")
    
    use_defaults = input("\nUse default Sandbox values? (y/n): ").strip().lower()
    
    if use_defaults == 'y':
        shortcode = "174379"
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    else:
        shortcode = input("Shortcode: ").strip()
        passkey = input("Passkey: ").strip()
    
    # Read current .env file
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("\n[ERROR] .env file not found!")
        return
    
    # Update credentials
    updated_lines = []
    for line in lines:
        if line.startswith('MPESA_CONSUMER_KEY='):
            updated_lines.append(f'MPESA_CONSUMER_KEY={consumer_key}\n')
        elif line.startswith('MPESA_CONSUMER_SECRET='):
            updated_lines.append(f'MPESA_CONSUMER_SECRET={consumer_secret}\n')
        elif line.startswith('MPESA_SHORTCODE='):
            updated_lines.append(f'MPESA_SHORTCODE={shortcode}\n')
        elif line.startswith('MPESA_PASSKEY='):
            updated_lines.append(f'MPESA_PASSKEY={passkey}\n')
        else:
            updated_lines.append(line)
    
    # Write back to .env
    with open('.env', 'w') as f:
        f.writelines(updated_lines)
    
    print("\n" + "="*60)
    print("[SUCCESS] Credentials updated in .env file!")
    print("="*60)
    print("\nNext steps:")
    print("1. Restart your backend server")
    print("2. Test M-Pesa payment with sandbox phone: 254708374149")
    print("\nTo restart backend:")
    print("   cd backend")
    print("   .\\venv\\Scripts\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        update_mpesa_credentials()
    except KeyboardInterrupt:
        print("\n\n[INFO] Setup cancelled")
    except Exception as e:
        print(f"\n[ERROR] {e}")
