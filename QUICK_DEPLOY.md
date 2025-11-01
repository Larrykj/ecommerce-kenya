# ⚡ Quick Deployment Guide (5 Minutes)

## Prerequisites
- GitHub account
- Vercel account  
- Render account

---

## Step 1: Push to GitHub (2 minutes)

```bash
# Open terminal in project folder
cd "C:\Users\HomePC\Desktop\E-Commerce REcommendations system"

# Initialize git
git init
git add .
git commit -m "Production ready deployment"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-kenya.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Frontend to Vercel (1 minute)

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Set these configurations:
   - **Root Directory**: `frontend`
   - **Framework**: Next.js (auto-detected)
4. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL = https://ecommerce-kenya-backend.onrender.com
   ```
5. Click **Deploy** (wait 2-3 minutes)
6. Copy your Vercel URL (e.g., `https://ecommerce-kenya.vercel.app`)

---

## Step 3: Deploy Backend to Render (2 minutes)

1. Go to https://render.com/create
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure:
   ```
   Name: ecommerce-kenya-backend
   Region: Frankfurt (EU)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. Add Environment Variables (click "Advanced"):
   ```env
   ENVIRONMENT=production
   SECRET_KEY=change-this-to-random-string-32-chars-min
   MONGODB_URL=mongodb://localhost:27017
   REDIS_URL=redis://localhost:6379
   MPESA_ENVIRONMENT=sandbox
   MPESA_CONSUMER_KEY=8wQFwY2zRlxSQr6r0fM9m80SZLJlG8DWlHsk9NAlWaWgtBuz
   MPESA_CONSUMER_SECRET=CKvEPnRc8IIHHbh3nVfIpFeFR2l59GxuhoSezVVFNxFgsQDL32MxVAGg9PvFcU1b
   MPESA_SHORTCODE=174379
   MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
   BACKEND_CORS_ORIGINS=["https://ecommerce-kenya.vercel.app"]
   ```
   
   **Replace** `ecommerce-kenya.vercel.app` with your actual Vercel URL!

6. Click **Create Web Service** (wait 5-10 minutes)

---

## Step 4: Update Frontend with Backend URL

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update `NEXT_PUBLIC_API_URL` with your Render URL:
   ```
   NEXT_PUBLIC_API_URL = https://ecommerce-kenya-backend.onrender.com
   ```
3. Go to Deployments → Redeploy latest

---

## Step 5: Test Your Live App! 🎉

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Test:
   - ✅ Homepage loads
   - ✅ Products display
   - ✅ Add to cart
   - ✅ Checkout
   - ✅ Admin panel: `https://your-app.vercel.app/admin`

---

## 🎯 Your App is Now Live!

**Customer Site**: https://your-app.vercel.app  
**Admin Panel**: https://your-app.vercel.app/admin  
**API Docs**: https://your-backend.onrender.com/docs  

**Cost**: $0 (Free tier)

---

## 🚨 Important Notes

### Free Tier Limitations

**Render Free Tier:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds to wake up
- 750 hours/month (enough for one app)

**Vercel Free Tier:**
- 100 GB bandwidth/month
- Unlimited deployments
- No sleep time

### To Add Database (Optional but Recommended)

**MongoDB Atlas** (Free 512MB):
1. https://www.mongodb.com/cloud/atlas/register
2. Create Free Cluster
3. Get connection string
4. Update `MONGODB_URL` in Render

**Redis Cloud** (Free 30MB):
1. https://redis.com/try-free/
2. Create database
3. Get connection URL
4. Update `REDIS_URL` in Render

---

## 🔄 Future Updates

**Update Frontend:**
```bash
git add .
git commit -m "Update"
git push
# Vercel auto-deploys!
```

**Update Backend:**
```bash
git push
# Render auto-deploys!
```

---

## 🆘 Common Issues

### Backend won't start
- Check Render logs
- Verify all env vars are set
- Check `requirements.txt` exists

### Frontend can't reach backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running (visit /health endpoint)
- Verify CORS settings in backend

### Images not loading
- Images use Unsplash (free)
- Should work automatically
- Check browser console for errors

---

## 🎊 Congratulations!

Your E-Commerce site is now live on the internet and accessible worldwide!

**Next Steps:**
1. Share your URL with friends
2. Add real products
3. Test M-Pesa payments
4. Monitor in Render/Vercel dashboards

Need help? See full `DEPLOYMENT_GUIDE.md` for detailed instructions.
