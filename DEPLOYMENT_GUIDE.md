# 🚀 Deployment Guide - E-Commerce Kenya

## Overview

This guide will help you deploy your E-Commerce Recommendation System to production using free/low-cost platforms.

**Recommended Stack:**
- **Frontend**: Vercel (Free)
- **Backend**: Render (Free tier)
- **Database**: MongoDB Atlas (Free tier)
- **Cache**: Redis Cloud (Free tier)
- **Images**: Cloudinary (Free tier)

---

## 📋 Pre-Deployment Checklist

### 1. Sign Up for Required Services

- [ ] Vercel account (https://vercel.com)
- [ ] Render account (https://render.com)
- [ ] MongoDB Atlas (https://www.mongodb.com/cloud/atlas)
- [ ] Redis Cloud (https://redis.com/try-free/)
- [ ] Cloudinary (https://cloudinary.com) - Optional for images
- [ ] M-Pesa Production credentials from Safaricom

### 2. Prepare Your Code

- [ ] All environment variables documented
- [ ] Database migrations ready
- [ ] Test data or seed scripts prepared
- [ ] Production environment files created

---

## 🗄️ Step 1: Deploy Database (MongoDB Atlas)

### 1.1 Create MongoDB Cluster

1. Go to https://cloud.mongodb.com
2. Click "Build a Database"
3. Choose **FREE** (M0 Sandbox)
4. Select region closest to Kenya (e.g., AWS / eu-central-1)
5. Name your cluster: `ecommerce-kenya`

### 1.2 Configure Database Access

1. Database Access → Add New Database User
   - Username: `ecommerce_admin`
   - Password: Generate secure password (save it!)
   - Role: `Atlas admin`

2. Network Access → Add IP Address
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - This is needed for Render/Vercel to connect

### 1.3 Get Connection String

1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy the connection string:
   ```
   mongodb+srv://ecommerce_admin:<password>@ecommerce-kenya.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Save this for backend deployment

---

## 🔴 Step 2: Deploy Cache (Redis Cloud)

### 2.1 Create Redis Database

1. Go to https://redis.com/try-free/
2. Sign up for free tier
3. Create new subscription:
   - Cloud: AWS
   - Region: Closest to Kenya
   - Name: `ecommerce-kenya-cache`

### 2.2 Get Redis URL

1. Go to your database
2. Copy the connection details:
   ```
   redis://default:password@redis-xxxxx.cloud.redislabs.com:12345
   ```
3. Save for backend deployment

---

## 🖥️ Step 3: Deploy Backend (Render)

### 3.1 Push Code to GitHub

```bash
# Initialize git if not already
cd "C:\Users\HomePC\Desktop\E-Commerce REcommendations system"
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub and push
git remote add origin https://github.com/yourusername/ecommerce-kenya.git
git branch -M main
git push -u origin main
```

### 3.2 Deploy on Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ecommerce-kenya-backend`
   - **Region**: Frankfurt (closest to Kenya)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

### 3.3 Add Environment Variables

In Render dashboard, add these environment variables:

```env
ENVIRONMENT=production
PROJECT_NAME=E-Commerce Recommendation System Kenya

# Database
MONGODB_URL=mongodb+srv://ecommerce_admin:password@cluster.mongodb.net/ecommerce_kenya
MONGODB_DB_NAME=ecommerce_kenya

# Redis
REDIS_URL=redis://default:password@redis-server.cloud.redislabs.com:12345
REDIS_DB=0

# Security
SECRET_KEY=your-secure-random-string-here-min-32-chars

# M-Pesa (Use sandbox first, then production)
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://ecommerce-kenya-backend.onrender.com/api/v1/mpesa/callback

# CORS (will update after frontend deployment)
BACKEND_CORS_ORIGINS=["https://your-site.vercel.app"]
```

### 3.4 Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your backend will be at: `https://ecommerce-kenya-backend.onrender.com`
4. Test: `https://ecommerce-kenya-backend.onrender.com/health`

---

## 🌐 Step 4: Deploy Frontend (Vercel)

### 4.1 Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### 4.2 Deploy via Vercel Dashboard

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 4.3 Add Environment Variables

```env
NEXT_PUBLIC_API_URL=https://ecommerce-kenya-backend.onrender.com
NEXT_PUBLIC_SITE_URL=https://your-site.vercel.app
```

### 4.4 Deploy

1. Click "Deploy"
2. Wait 2-3 minutes
3. Your site will be at: `https://your-project.vercel.app`

### 4.5 Update Backend CORS

Go back to Render → Environment Variables → Update:

```env
BACKEND_CORS_ORIGINS=["https://your-project.vercel.app","https://www.your-domain.com"]
```

---

## 🔒 Step 5: Configure M-Pesa for Production

### 5.1 Apply for Production Access

1. Go to https://developer.safaricom.co.ke
2. Login to your account
3. Go to "My Apps" → Your App
4. Click "Request Production Keys"
5. Fill in the application form
6. Wait for approval (1-3 business days)

### 5.2 Update M-Pesa Credentials

Once approved, update in Render:

```env
MPESA_ENVIRONMENT=production
MPESA_CONSUMER_KEY=your_production_key
MPESA_CONSUMER_SECRET=your_production_secret
MPESA_SHORTCODE=your_production_shortcode
MPESA_PASSKEY=your_production_passkey
MPESA_CALLBACK_URL=https://ecommerce-kenya-backend.onrender.com/api/v1/mpesa/callback
```

---

## 📊 Step 6: Add Real Product Data

### 6.1 Access MongoDB

1. MongoDB Atlas → Browse Collections
2. Connect via MongoDB Compass or Shell
3. Use connection string from Step 1

### 6.2 Seed Database

```bash
# Run seed script
cd backend
python seed_database.py
```

Or manually add products via Admin panel:
- https://your-site.vercel.app/admin

---

## 🎨 Step 7: Setup Image CDN (Optional but Recommended)

### 7.1 Cloudinary Setup

1. Sign up at https://cloudinary.com
2. Get your Cloud Name, API Key, API Secret
3. Upload product images
4. Update product image URLs in database

### Alternative: Use Unsplash (Current)
- No setup needed
- Free to use
- Already configured in mock data

---

## 🌍 Step 8: Custom Domain (Optional)

### 8.1 Buy Domain

- Namecheap, GoDaddy, or any registrar
- Recommended: `.co.ke` for Kenya

### 8.2 Configure Vercel

1. Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain: `www.yourstore.co.ke`
3. Follow DNS instructions

### 8.3 Update Backend CORS

```env
BACKEND_CORS_ORIGINS=["https://www.yourstore.co.ke","https://yourstore.co.ke"]
```

---

## ✅ Step 9: Post-Deployment Checklist

### Test Everything

- [ ] Homepage loads with products
- [ ] Product images display
- [ ] Search works
- [ ] Categories work
- [ ] Add to cart works
- [ ] Checkout form works
- [ ] M-Pesa payment initiates
- [ ] Order confirmation shows
- [ ] Language toggle works
- [ ] Admin panel accessible
- [ ] Mobile responsive

### Performance

- [ ] Test on fast 4G connection
- [ ] Test on slow 2G connection
- [ ] Check page load times (<3 seconds)
- [ ] Optimize images if needed

### Security

- [ ] HTTPS enabled (automatic on Vercel)
- [ ] Environment variables not exposed
- [ ] API keys secure
- [ ] CORS configured correctly

### Monitoring

- [ ] Set up Render alerts
- [ ] Configure Vercel analytics
- [ ] Monitor error logs
- [ ] Track API response times

---

## 📱 Quick Deploy Commands

### Deploy Frontend Only
```bash
cd frontend
vercel --prod
```

### Deploy Backend Only
- Push to GitHub
- Render auto-deploys

### Update Environment Variables
- Render: Dashboard → Environment → Edit
- Vercel: Dashboard → Settings → Environment Variables

---

## 🆘 Troubleshooting

### Frontend not connecting to backend

**Issue**: API calls fail  
**Solution**: Check `NEXT_PUBLIC_API_URL` in Vercel env vars

### M-Pesa not working

**Issue**: No STK Push  
**Solution**: 
1. Verify M-Pesa credentials in Render
2. Check callback URL is public
3. Test with sandbox first

### Images not loading

**Issue**: 404 on images  
**Solution**: 
1. Check Unsplash URLs
2. Consider Cloudinary migration
3. Verify image URLs in database

### Database connection fails

**Issue**: Backend can't connect to MongoDB  
**Solution**:
1. Verify MongoDB URL in env vars
2. Check IP whitelist (allow 0.0.0.0/0)
3. Verify username/password

### CORS errors

**Issue**: Browser blocks API calls  
**Solution**:
1. Add frontend URL to `BACKEND_CORS_ORIGINS`
2. Include both www and non-www versions
3. Restart backend service

---

## 💰 Cost Breakdown

### Free Tier Limits

| Service | Free Tier | Upgrade Cost |
|---------|-----------|--------------|
| Vercel | 100 GB bandwidth/month | $20/month |
| Render | 750 hours/month | $7/month |
| MongoDB Atlas | 512 MB storage | $9/month |
| Redis Cloud | 30 MB storage | $5/month |
| Cloudinary | 25 GB storage/month | $89/month |

**Total Free**: $0/month for MVP  
**Total Paid** (if needed): ~$50/month

---

## 🚀 Launch Checklist

### Before Launch

- [ ] All tests passing
- [ ] Real product data loaded
- [ ] M-Pesa tested (sandbox)
- [ ] Admin credentials secured
- [ ] Analytics set up
- [ ] Error tracking configured
- [ ] Backup strategy in place

### Launch Day

- [ ] Deploy to production
- [ ] Test all critical flows
- [ ] Monitor error logs
- [ ] Have rollback plan ready
- [ ] Announce on social media
- [ ] Monitor first transactions

### Post-Launch

- [ ] Collect user feedback
- [ ] Monitor performance
- [ ] Fix any bugs quickly
- [ ] Plan feature updates
- [ ] Scale as needed

---

## 📞 Support

### Platform Support

- **Vercel**: https://vercel.com/support
- **Render**: https://render.com/docs
- **MongoDB**: https://www.mongodb.com/docs/atlas/
- **M-Pesa**: https://developer.safaricom.co.ke/support

### Community

- Next.js Discord: https://nextjs.org/discord
- FastAPI Discussions: https://github.com/tiangolo/fastapi/discussions

---

## 🎉 Your App is Now Live!

**Frontend**: https://your-project.vercel.app  
**Backend**: https://ecommerce-kenya-backend.onrender.com  
**Admin**: https://your-project.vercel.app/admin

Share your store and start selling! 🛍️🇰🇪

---

**Deployment Date**: [Add date here]  
**Version**: 1.0.0  
**Status**: PRODUCTION READY ✅
