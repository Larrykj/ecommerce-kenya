# 🚀 Free Deployment Guide

This guide will help you deploy your E-Commerce Recommendation System for free using Vercel (Frontend) and Render.com (Backend).

## 📋 Prerequisites

1. GitHub account
2. Vercel account (free)
3. Render.com account (free)

## 🎯 Quick Deploy

### Option 1: Deploy Frontend to Vercel

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ecommerce-recommendations.git
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Root Directory: `frontend`
   - Framework Preset: Next.js
   - Environment Variables:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
     ```
   - Click "Deploy"

### Option 2: Deploy Backend to Render.com

1. **Prepare Backend**
   - Ensure `requirements.txt` is in the `backend` folder
   - Create `render.yaml` in root:
   ```yaml
   services:
     - type: web
       name: ecommerce-backend
       runtime: python
       buildCommand: cd backend && pip install -r requirements.txt
       startCommand: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
         - key: ENVIRONMENT
           value: production
   ```

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: ecommerce-backend
     - **Root Directory**: backend
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

3. **Update Frontend API URL**
   - In Vercel, update environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://ecommerce-backend.onrender.com
     ```
   - Redeploy frontend

## 🌐 Alternative: Deploy Both to Render.com

You can also deploy both frontend and backend to Render:

### Frontend on Render
1. Create new Web Service
2. Root Directory: `frontend`
3. Build Command: `npm install && npm run build`
4. Start Command: `npm start`
5. Environment Variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

## ✅ Post-Deployment Checklist

- [ ] Backend is accessible at `https://your-backend.onrender.com/health`
- [ ] Frontend is accessible at `https://your-app.vercel.app`
- [ ] API calls work from frontend
- [ ] Login/Register functionality works
- [ ] Products are loading correctly

## 🔧 Environment Variables

### Backend (Render.com)
```
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here (generate one)
PYTHON_VERSION=3.11.0
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## 📝 Notes

- **Free Tier Limits**:
  - Render: Backend sleeps after 15 min inactivity (wakes on first request)
  - Vercel: 100GB bandwidth/month
  - Both services are perfect for demo/prototype

- **For Production**:
  - Upgrade to paid tiers for 24/7 uptime
  - Add MongoDB Atlas (free tier available)
  - Add Redis (upgrade needed for persistence)

## 🎉 Your App is Live!

Visit your deployed frontend URL and start using your E-Commerce Recommendation System!
