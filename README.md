# 🛒 E-Commerce Recommendation System - Kenya Edition

A production-ready, AI-powered e-commerce recommendation system built specifically for the Kenyan market, featuring ML-based personalization, M-Pesa integration, regional insights, and dual-language support.

## 🌟 Key Features

### 🎯 Recommendation Engine
- ✅ **User-based Collaborative Filtering** - Find similar users and recommend their preferences
- ✅ **Item-based Collaborative Filtering** - Recommend similar products
- ✅ **Hybrid Model** - Combines collaborative + content-based filtering using LightFM
- ✅ **Trending Items** - Real-time most viewed/sold products
- ✅ **Personalized Homepage** - Dynamic user-specific product feeds
- ✅ **Context-Aware Suggestions** - Time/location/season-based recommendations
- ✅ **Search Auto-Suggestions** - Intelligent search completions
- ✅ **Dynamic Discounts & Bundles** - Smart promotional strategies

### 🧠 Machine Learning
- **KNN (K-Nearest Neighbors)** - Similarity-based recommendations
- **Matrix Factorization (SVD)** - Latent feature extraction
- **LightFM** - Hybrid collaborative and content filtering
- **Real-time Updates** - Redis caching for instant responses
- **A/B Testing** - Continuous recommendation optimization

### 🇰🇪 Kenya-Specific Features
- 💳 **M-Pesa Integration** - STK Push payment support
- 📍 **Regional Product Trends** - 47 county-based insights
- 📶 **Low-Data Optimization** - Optimized for slow connections
- 📴 **Offline Capability** - PWA with offline browsing
- 🌐 **Dual Language** - Swahili & English support
- 🏪 **Local Vendor Promotion** - Priority for Kenyan businesses

## 📁 Project Structure

```
.
├── backend/                    # FastAPI Python Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── endpoints/     # Route handlers
│   │   │   └── deps.py        # Dependencies
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings
│   │   │   └── security.py    # Auth & security
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   ├── recommendations/  # ML recommendation service
│   │   │   ├── mpesa/         # M-Pesa integration
│   │   │   └── analytics/     # Analytics service
│   │   ├── ml/                # ML models & training
│   │   │   ├── collaborative_filtering.py
│   │   │   ├── content_based.py
│   │   │   └── hybrid_model.py
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # App router
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities
│   │   ├── services/          # API integration
│   │   └── i18n/              # Translations
│   ├── public/
│   ├── package.json
│   └── next.config.js
│
├── data/                       # Sample datasets
├── models/                     # Trained ML models
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB 6.0+
- Redis 7.0+

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
```

### Docker Setup (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Backend Environment Variables (`.env`)

```env
# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=ecommerce_kenya
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# M-Pesa
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/v1/mpesa/callback

# ML Configuration
MIN_RECOMMENDATIONS=5
MAX_RECOMMENDATIONS=20
MODEL_RETRAIN_INTERVAL=86400
```

### Frontend Environment Variables (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_NAME=ShopKE
NEXT_PUBLIC_DEFAULT_LANGUAGE=en
```

## 📊 Machine Learning Models

### 1. User-Based Collaborative Filtering
Analyzes user behavior patterns to find similar users and recommend products they enjoyed.

### 2. Item-Based Collaborative Filtering
Recommends products similar to those the user has interacted with.

### 3. Hybrid Model (LightFM)
Combines user-item interactions with product metadata (category, brand, price, reviews) for superior recommendations.

### 4. Context-Aware Engine
- **Time-based**: Morning vs evening product preferences
- **Location-based**: County-specific trending items
- **Seasonal**: Weather and season-appropriate products

## 🌍 Regional Features

### County-Based Analytics
Track and analyze product preferences across all 47 Kenyan counties to optimize inventory and marketing.

### Language Support
- Automatic language detection
- Seamless switching between English and Swahili
- Translated product descriptions and UI

### Low-Bandwidth Optimization
- Compressed responses
- Progressive image loading
- Lazy loading components
- Service worker caching

## 💳 M-Pesa Integration

Complete mobile money integration:
- **STK Push**: Automatic payment prompts
- **Payment Verification**: Real-time transaction status
- **Transaction History**: Complete payment records
- **Refunds**: Automated refund processing

## 📈 Analytics & A/B Testing

### Built-in Analytics
- User behavior tracking
- Conversion funnel analysis
- Recommendation performance metrics
- Revenue attribution

### A/B Testing Framework
- Algorithm comparison
- UI/UX variations
- Pricing strategy testing
- Promotional effectiveness

## 🔒 Security Features

- JWT-based authentication
- Rate limiting per endpoint
- CORS protection
- Input validation & sanitization
- Secure payment processing
- Data encryption at rest

## 📚 API Documentation

Once running, access interactive API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚢 Deployment

### AWS Deployment
```bash
# Deploy backend to AWS Lambda
# Deploy frontend to Vercel/Netlify
# MongoDB Atlas for database
# ElastiCache for Redis
```

### Google Cloud
```bash
# Cloud Run for backend
# Cloud Storage for static assets
# Firestore/MongoDB Atlas for database
```

### Traditional VPS
```bash
# Use docker-compose.yml
docker-compose -f docker-compose.prod.yml up -d
```

## 📞 Support & Contributing

For issues, questions, or contributions, please open a GitHub issue or pull request.

## 📄 License

MIT License - feel free to use this project for commercial purposes.

---

**Made with ❤️ for Kenya's growing e-commerce ecosystem**

