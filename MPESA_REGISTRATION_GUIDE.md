# Complete M-Pesa Setup Guide - Step by Step

## Part 1: Register on Safaricom Daraja Portal

### Step 1.1: Go to Daraja Portal
1. Open browser and visit: **https://developer.safaricom.co.ke/**
2. Click **"Sign Up"** (top right corner)

### Step 1.2: Create Account
Fill in the registration form:
- **Email**: Your valid email address
- **Phone**: Your Kenyan phone number (254XXXXXXXXX)
- **First Name**: Your first name
- **Last Name**: Your last name
- **Organization**: Your company/personal name
- Click **"Create Account"**

### Step 1.3: Verify Email
1. Check your email inbox
2. Click the verification link from Safaricom
3. Your account is now active!

---

## Part 2: Create Your First App

### Step 2.1: Login to Daraja
1. Go to: **https://developer.safaricom.co.ke/**
2. Click **"Login"**
3. Enter your email and password

### Step 2.2: Create New App
1. Click **"My Apps"** in the navigation menu
2. Click **"Create New App"** button
3. Fill in app details:
   - **App Name**: `ShopKE E-Commerce` (or any name)
   - **Description**: `E-commerce platform with M-Pesa payment`

### Step 2.3: Select APIs
**IMPORTANT**: Check these boxes:
- ✅ **Lipa Na M-Pesa Online** (This is what we need!)
- You can also select:
  - Customer to Business (C2B)
  - Business to Customer (B2C)

4. Click **"Create App"**

---

## Part 3: Get Your Credentials

### Step 3.1: View App Details
1. Go to **"My Apps"**
2. Click on your newly created app
3. You'll see two tabs: **"Sandbox"** and **"Production"**

### Step 3.2: Sandbox Credentials (For Testing)
1. Click **"Sandbox"** tab
2. You'll see:
   - **Consumer Key**: `Copy this` (looks like: A1b2C3d4E5f6...)
   - **Consumer Secret**: `Copy this` (looks like: X9y8Z7w6...)

### Step 3.3: Get Passkey
1. Scroll down on the Sandbox page
2. Look for **"Test Credentials"** section
3. Find **"Lipa Na M-Pesa Online Passkey"**
4. **Sandbox Passkey** (usually this):
   ```
   bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
   ```

### Step 3.4: Get Shortcode
- **Sandbox Shortcode**: `174379`
- This is the test business number

---

## Part 4: Configure Your Application

### Step 4.1: Update .env File

Open: `backend/.env`

Replace these lines with YOUR credentials:

```env
# M-Pesa Configuration
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=YOUR_CONSUMER_KEY_HERE_FROM_DARAJA
MPESA_CONSUMER_SECRET=YOUR_CONSUMER_SECRET_HERE_FROM_DARAJA
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=http://localhost:8000/api/v1/mpesa/callback
```

### Example (with fake credentials):
```env
MPESA_CONSUMER_KEY=A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6
MPESA_CONSUMER_SECRET=X9y8Z7w6V5u4T3s2R1q0P9o8N7m6L5k4
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
```

### Step 4.2: Restart Backend Server

```powershell
# In your terminal, stop the current server (Ctrl+C)
# Then restart:
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Part 5: Test M-Pesa Payment

### Step 5.1: Test Phone Numbers (Sandbox)
Safaricom provides test numbers:
- **Test Phone 1**: `254708374149`
- **Test Phone 2**: `254708374148`
- **Test Phone 3**: `254708374147`

### Step 5.2: Make Test Purchase
1. Go to your app: http://localhost:3001
2. Add items to cart
3. Go to checkout
4. Fill in details:
   - **Phone**: Use test number `254708374149`
   - **Payment Method**: Select M-Pesa
5. Click "Place Order"

### Step 5.3: What Happens in Sandbox
- ✅ You'll see success message
- ✅ Order created
- ✅ In sandbox, payment is simulated (no actual prompt)
- ✅ But the API call is made correctly

### Step 5.4: Check Daraja Logs
1. Go back to Daraja Portal
2. Click "My Apps" → Your App
3. Click "Sandbox" tab
4. Scroll to "API Logs"
5. You'll see your STK Push request logged!

---

## Part 6: Setup for Production (Real Payments)

### When Ready for Real Customers:

1. **Go Live Request**:
   - In Daraja Portal → Your App
   - Click "Production" tab
   - Click "Request to Go Live"
   - Fill out the form
   - Safaricom will review (takes 1-3 business days)

2. **Get Production Credentials**:
   - After approval, go to "Production" tab
   - Copy Consumer Key and Consumer Secret
   - Get your real business shortcode and passkey

3. **Update .env for Production**:
   ```env
   MPESA_ENVIRONMENT=production
   MPESA_CONSUMER_KEY=YOUR_PRODUCTION_KEY
   MPESA_CONSUMER_SECRET=YOUR_PRODUCTION_SECRET
   MPESA_SHORTCODE=YOUR_BUSINESS_SHORTCODE
   MPESA_PASSKEY=YOUR_PRODUCTION_PASSKEY
   MPESA_CALLBACK_URL=https://yourdomain.com/api/v1/mpesa/callback
   ```

---

## Troubleshooting

### Issue: "Invalid Credentials"
- Double-check you copied Consumer Key and Secret correctly
- Make sure no extra spaces
- Verify you're using Sandbox credentials in sandbox environment

### Issue: "STK Push Failed"
- Ensure phone number format: `254XXXXXXXXX` (no + sign)
- Use test phone numbers in sandbox
- Check amount is between 1-70000 KES

### Issue: "Callback URL not reachable"
- For local testing, use ngrok:
  ```bash
  ngrok http 8000
  # Copy the https URL
  # Update MPESA_CALLBACK_URL in .env
  ```

---

## Quick Reference

### Sandbox Test Data
- **Shortcode**: 174379
- **Passkey**: bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
- **Test Phone**: 254708374149
- **Test Amount**: 1-70000 KES

### Important Links
- **Daraja Portal**: https://developer.safaricom.co.ke/
- **Documentation**: https://developer.safaricom.co.ke/Documentation
- **API Reference**: https://developer.safaricom.co.ke/docs
- **Test Tool**: https://developer.safaricom.co.ke/test

### Support
- **Email**: support@safaricom.co.ke
- **Phone**: +254 722 002 222

---

## Next Steps After Setup

1. ✅ Register on Daraja Portal
2. ✅ Create app and get credentials
3. ✅ Update backend/.env file
4. ✅ Restart backend server
5. ✅ Test with sandbox phone numbers
6. ✅ Check API logs in Daraja Portal
7. 📝 When ready, apply for production access

---

**Need Help?** Check the API logs in Daraja Portal - they show exactly what's happening with each request!
