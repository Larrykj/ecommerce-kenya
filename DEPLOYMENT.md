# 🚀 Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### 1. Clone and Configure

```bash
git clone <repository-url>
cd E-Commerce-REcommendations-system
```

### 2. Set Up Environment Variables

Create `.env` file in `backend/` directory:

```env
MONGODB_URL=mongodb://admin:password123@mongodb:27017
MONGODB_DB_NAME=ecommerce_kenya
REDIS_URL=redis://redis:6379
SECRET_KEY=your-production-secret-key-here
MPESA_CONSUMER_KEY=your_mpesa_key
MPESA_CONSUMER_SECRET=your_mpesa_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/v1/mpesa/callback
```

Create `.env.local` in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Services

```bash
docker-compose up -d
```

This will start:
- MongoDB on port 27017
- Redis on port 6379
- Backend API on port 8000
- Frontend on port 3000

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

## 🌐 Production Deployment

### AWS Deployment

#### Backend (Lambda + API Gateway)

1. **Prepare Backend**
```bash
cd backend
pip install -r requirements.txt -t ./package
cd package
zip -r ../deployment.zip .
cd ..
zip -g deployment.zip -r app/
```

2. **Create Lambda Function**
- Upload `deployment.zip`
- Runtime: Python 3.9
- Handler: `mangum_handler.handler`
- Environment variables from `.env`

3. **Configure API Gateway**
- Create REST API
- Configure routes
- Deploy to stage

#### Frontend (Vercel/Netlify)

**Vercel Deployment:**
```bash
cd frontend
vercel --prod
```

**Environment Variables in Vercel:**
- `NEXT_PUBLIC_API_URL`: Your Lambda API URL

#### Database (MongoDB Atlas)

1. Create cluster at mongodb.com/cloud/atlas
2. Configure network access
3. Get connection string
4. Update `MONGODB_URL` in backend environment

#### Cache (AWS ElastiCache)

1. Create Redis cluster in ElastiCache
2. Note endpoint URL
3. Update `REDIS_URL` in backend environment

### Google Cloud Deployment

#### Backend (Cloud Run)

1. **Build Container**
```bash
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/ecommerce-backend
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy ecommerce-backend \
  --image gcr.io/PROJECT_ID/ecommerce-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Frontend (Cloud Run or Firebase Hosting)

**Cloud Run:**
```bash
cd frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/ecommerce-frontend
gcloud run deploy ecommerce-frontend \
  --image gcr.io/PROJECT_ID/ecommerce-frontend \
  --platform managed \
  --allow-unauthenticated
```

**Firebase Hosting:**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
npm run build
firebase deploy
```

### VPS Deployment (DigitalOcean, Linode, etc.)

1. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

2. **Install Docker Compose**
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone and Deploy**
```bash
git clone <repository-url>
cd E-Commerce-REcommendations-system
docker-compose up -d
```

4. **Set Up Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

5. **SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📊 ML Model Training

### Initial Training

```bash
cd backend
python -m app.scripts.train_models
```

### Automated Retraining

Set up cron job:
```bash
0 2 * * * cd /path/to/backend && python -m app.scripts.train_models
```

Or use Celery Beat for scheduled tasks.

## 🔄 CI/CD Setup

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Cloud Run
        run: |
          # Your deployment commands

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## 📈 Monitoring

### Application Monitoring

- **Backend**: Built-in Prometheus metrics at `/metrics`
- **Frontend**: Google Analytics + custom events
- **Database**: MongoDB Atlas monitoring
- **Cache**: Redis monitoring tools

### Log Management

- Use CloudWatch (AWS) or Cloud Logging (GCP)
- Set up alerts for errors and performance issues

### Uptime Monitoring

- Use services like Pingdom, UptimeRobot
- Monitor `/health` endpoint

## 🔒 Security Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable database authentication
- [ ] Secure M-Pesa credentials
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor for suspicious activity

## 🔧 Troubleshooting

### Backend not starting
- Check MongoDB connection
- Verify environment variables
- Check logs: `docker-compose logs backend`

### Frontend not connecting to backend
- Verify NEXT_PUBLIC_API_URL
- Check CORS settings
- Ensure backend is running

### ML models not loading
- Run training script first
- Check models directory permissions
- Verify model file paths

## 📞 Support

For deployment issues, contact your development team or open an issue on GitHub.

