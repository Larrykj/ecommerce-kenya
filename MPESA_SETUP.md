# M-Pesa Integration Setup Guide

## Current Status: DEMO MODE

The application is currently running in **DEMO MODE** because M-Pesa credentials are not configured. Orders work, but payments are simulated.

## What's Working in Demo Mode

✅ Full shopping cart functionality  
✅ Complete checkout process  
✅ Order creation and tracking  
✅ All UI/UX features  
❌ Real M-Pesa payment prompts (simulated instead)

## How to Enable Real M-Pesa Payments

### Step 1: Get M-Pesa Credentials from Safaricom

1. Go to [Safaricom Daraja Portal](https://developer.safaricom.co.ke/)
2. Create an account and login
3. Create a new app in the portal
4. Note down these credentials:
   - **Consumer Key**
   - **Consumer Secret**
   - **Business Shortcode** (e.g., 174379 for sandbox)
   - **Passkey** (for Lipa Na M-Pesa Online)

### Step 2: Configure Backend

Edit `backend/.env` file:

```env
# M-Pesa Configuration
MPESA_ENVIRONMENT=sandbox  # Use "production" for live
MPESA_CONSUMER_KEY=your_consumer_key_here
MPESA_CONSUMER_SECRET=your_consumer_secret_here
MPESA_SHORTCODE=174379  # Your business shortcode
MPESA_PASSKEY=your_passkey_here
MPESA_CALLBACK_URL=https://yourdomain.com/api/v1/mpesa/callback
```

### Step 3: Set Up Callback URL

For M-Pesa to send payment confirmations, you need a **public URL**:

**For Testing (Local Development):**
```bash
# Use ngrok to expose your local server
ngrok http 8000

# Copy the https URL (e.g., https://abc123.ngrok.io)
# Update MPESA_CALLBACK_URL in .env:
MPESA_CALLBACK_URL=https://abc123.ngrok.io/api/v1/mpesa/callback
```

**For Production:**
```env
MPESA_CALLBACK_URL=https://yourdomain.com/api/v1/mpesa/callback
```

### Step 4: Restart Backend

```powershell
# Stop current backend (Ctrl+C in terminal)
# Then restart:
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Test M-Pesa Payment

1. Go to checkout
2. Select M-Pesa payment
3. Enter phone number in format: `254712345678`
4. Complete order
5. You should receive an STK Push prompt on your phone
6. Enter M-Pesa PIN to complete payment

## M-Pesa Sandbox Testing

### Test Credentials (Sandbox)
- **Shortcode**: 174379
- **Test Phone**: 254708374149
- **Test Amount**: Any amount between 1-70000 KES

### Sandbox Limitations
- Only works with specific test phone numbers
- Payments are simulated (no real money)
- Perfect for development and testing

## Troubleshooting

### Issue: "M-Pesa not configured"
**Solution**: Add credentials to `backend/.env` file

### Issue: "Callback not received"
**Solution**: 
- Ensure callback URL is publicly accessible
- Use ngrok for local testing
- Check Daraja portal logs

### Issue: "Invalid credentials"
**Solution**:
- Verify Consumer Key and Secret are correct
- Ensure you're using the right environment (sandbox vs production)
- Regenerate credentials if needed

## Production Checklist

Before going live:

- [ ] Get production M-Pesa credentials
- [ ] Update `MPESA_ENVIRONMENT=production` in `.env`
- [ ] Set production callback URL (must be HTTPS)
- [ ] Test with small amounts first
- [ ] Monitor callback logs
- [ ] Set up error alerting

## Code Structure

The M-Pesa integration is fully implemented:

- **Service**: `backend/app/services/mpesa_service.py` - Core M-Pesa logic
- **Endpoints**: `backend/app/api/api_v1/endpoints/mpesa.py` - API routes
- **Orders Integration**: `backend/app/api/api_v1/endpoints/orders.py` - Order creation with M-Pesa

## Support

For M-Pesa API issues:
- [Daraja API Documentation](https://developer.safaricom.co.ke/Documentation)
- [API Testing Tool](https://developer.safaricom.co.ke/test)
- Safaricom Support: support@safaricom.co.ke

---

**Note**: The application works perfectly without M-Pesa configuration. All features are functional in demo mode for development and testing purposes.
