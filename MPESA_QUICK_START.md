# M-Pesa Setup - Quick Checklist

## 5-Minute Setup Process

### ☐ Step 1: Register (3 minutes)
- [x] Browser opened to: https://developer.safaricom.co.ke/
- [ ] Click "Sign Up"
- [ ] Enter email, phone, name
- [ ] Verify email
- [ ] Login to Daraja Portal

### ☐ Step 2: Create App (1 minute)
- [ ] Click "My Apps"
- [ ] Click "Create New App"
- [ ] Name: `ShopKE` or any name
- [ ] Check: ✅ **Lipa Na M-Pesa Online**
- [ ] Click "Create App"

### ☐ Step 3: Get Credentials (30 seconds)
- [ ] Go to "My Apps" → Your App
- [ ] Click "Sandbox" tab
- [ ] Copy **Consumer Key**
- [ ] Copy **Consumer Secret**

**Sandbox defaults (copy these):**
```
Shortcode: 174379
Passkey: bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
```

### ☐ Step 4: Update Configuration (30 seconds)

**Option A: Use the helper script**
```powershell
cd backend
.\venv\Scripts\python.exe update_mpesa_credentials.py
# Paste your Consumer Key and Consumer Secret when prompted
# Press 'y' for sandbox defaults
```

**Option B: Manual edit**
Edit `backend/.env`:
```env
MPESA_CONSUMER_KEY=paste_your_key_here
MPESA_CONSUMER_SECRET=paste_your_secret_here
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
```

### ☐ Step 5: Restart Backend (10 seconds)
```powershell
# Stop current server (Ctrl+C)
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### ☐ Step 6: Test Payment (1 minute)
1. Open app: http://localhost:3001
2. Add products to cart
3. Checkout
4. Use test phone: `254708374149`
5. Select M-Pesa payment
6. Complete order

---

## What You'll See in Sandbox

✅ Order created successfully  
✅ M-Pesa API called  
✅ Request logged in Daraja Portal  
✅ Payment simulated (sandbox mode)

---

## Verify It's Working

Check in Daraja Portal:
1. Go to "My Apps" → Your App
2. Click "Sandbox" tab
3. Scroll to "API Logs"
4. You'll see your STK Push request!

---

## Test Phone Numbers (Sandbox)

Use these for testing:
- `254708374149`
- `254708374148`
- `254708374147`

---

## Need Help?

📖 Full guide: `MPESA_REGISTRATION_GUIDE.md`
🔧 Troubleshooting: `MPESA_SETUP.md`

---

## After Registration, Run This:

```powershell
cd backend
.\venv\Scripts\python.exe update_mpesa_credentials.py
```

This will guide you through updating your credentials!
