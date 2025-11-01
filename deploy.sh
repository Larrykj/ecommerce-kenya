#!/bin/bash

# Quick Deploy Script
echo "🚀 E-Commerce Kenya - Quick Deploy"
echo "=================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Production ready"
fi

# Deploy Frontend to Vercel
echo ""
echo "🌐 Deploying Frontend to Vercel..."
cd frontend
npx vercel --prod

# Instructions for Backend
echo ""
echo "🖥️  Backend Deployment Instructions:"
echo "1. Push your code to GitHub"
echo "2. Go to https://render.com"
echo "3. Create new Web Service"
echo "4. Connect your GitHub repo"
echo "5. Set Root Directory to 'backend'"
echo "6. Add environment variables from .env.production"
echo ""
echo "✅ Frontend deployed! Backend needs manual setup on Render."
echo "📖 See DEPLOYMENT_GUIDE.md for full instructions"
