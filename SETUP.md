# 🚀 Setup Guide - E-Commerce Recommendation System (Kenya)

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Manual Setup](#manual-setup)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Training ML Models](#training-ml-models)

## Prerequisites

### Required Software
- **Python 3.9+**
- **Node.js 18+**
- **MongoDB 6.0+**
- **Redis 7.0+**
- **Docker & Docker Compose** (recommended)

### Optional
- **Git** for version control
- **Postman** for API testing

## Quick Start (Docker - Recommended)

### 1. Clone Repository
```bash
git clone <repository-url>
cd E-Commerce-REcommendations-system
```

### 2. Configure Environment
```bash
# Copy example environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit the files with your configuration
nano backend/.env
nano frontend/.env.local
```

### 3. Start All Services
```bash
docker-compose up -d
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Manual Setup

### Backend Setup

#### 1. Navigate to Backend Directory
```bash
cd backend
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

#### 5. Start Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Configure Environment
```bash
cp .env.example .env.local
# Edit .env.local with your settings
```

#### 4. Start Development Server
```bash
npm run dev
```

### Database Setup

#### MongoDB

**Option 1: Local Installation**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS
brew install mongodb-community

# Start service
sudo systemctl start mongodb
```

**Option 2: MongoDB Atlas (Cloud)**
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Add to `MONGODB_URL` in backend `.env`

#### Redis

**Local Installation:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start service
redis-server
```

**Or use Docker:**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Environment Configuration

### Backend (.env)

```env
# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=ecommerce_kenya
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# M-Pesa (Get from Safaricom Daraja)
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/v1/mpesa/callback

# ML Configuration
MIN_RECOMMENDATIONS=5
MAX_RECOMMENDATIONS=20
MODEL_RETRAIN_INTERVAL=86400
KNN_NEIGHBORS=20
SVD_FACTORS=50

# Features
ENABLE_AB_TESTING=true
ENABLE_REGIONAL_FEATURES=true
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_NAME=ShopKE
NEXT_PUBLIC_DEFAULT_LANGUAGE=en
NEXT_PUBLIC_GA_ID=your_google_analytics_id
```

## Running the Application

### Development Mode

**Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Production Mode

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

## Training ML Models

### Initial Training

The recommendation models need to be trained with interaction data:

```bash
cd backend
python -m app.scripts.train_models
```

**Note:** For the first run with no data, the models will train on sample data.

### Updating Models

Models should be retrained periodically as new interaction data accumulates:

```bash
# Set up a cron job (Linux/Mac)
crontab -e

# Add this line to retrain daily at 2 AM
0 2 * * * cd /path/to/backend && /path/to/venv/bin/python -m app.scripts.train_models
```

## Verifying Installation

### Check Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Check Frontend
Open browser to http://localhost:3000

### Check Database Connections
```bash
# MongoDB
mongosh mongodb://localhost:27017

# Redis
redis-cli ping
# Should return: PONG
```

## M-Pesa Integration Setup

### 1. Register on Daraja
1. Go to https://developer.safaricom.co.ke/
2. Create account and login
3. Create a new app

### 2. Get Credentials
- Consumer Key
- Consumer Secret
- Passkey (for Lipa Na M-Pesa Online)

### 3. Configure Callback URL
Set up a public URL for M-Pesa callbacks:
- Use ngrok for testing: `ngrok http 8000`
- Use your domain for production

### 4. Test STK Push
```bash
curl -X POST http://localhost:8000/api/v1/mpesa/stk-push \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "254712345678",
    "amount": 100,
    "order_id": "TEST001"
  }'
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
sudo systemctl status mongodb

# Start if not running
sudo systemctl start mongodb
```

### Redis Connection Failed
```bash
# Check if Redis is running
redis-cli ping

# Start if not running
redis-server
```

### Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. ✅ Set up development environment
2. ✅ Configure environment variables
3. ✅ Start backend and frontend
4. 📝 Add sample data to MongoDB
5. 🤖 Train ML models
6. 🧪 Test API endpoints
7. 🎨 Customize frontend
8. 🚀 Deploy to production

## Getting Help

- **Documentation**: See README.md and DEPLOYMENT.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: Open a GitHub issue
- **Community**: Join our Slack/Discord

---

**Ready to build the future of Kenyan e-commerce! 🇰🇪 🚀**

