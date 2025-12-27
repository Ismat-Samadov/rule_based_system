# Yonca Deployment Guide

## 🚀 Quick Start with Docker Compose

The easiest way to deploy Yonca is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd rule_based_recommendation_system

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 📋 Prerequisites

### For Docker Deployment
- Docker 20.10+
- Docker Compose 2.0+

### For Manual Deployment
- Python 3.10+
- Node.js 20+
- npm 9+

---

## 🐳 Docker Deployment (Recommended)

### Build Images

```bash
# Build backend
cd backend
docker build -t yonca-backend .

# Build frontend
cd ../frontend
docker build -t yonca-frontend .
```

### Run Containers Individually

```bash
# Run backend
docker run -d \
  --name yonca-backend \
  -p 8000:8000 \
  -e DEBUG=True \
  yonca-backend

# Run frontend
docker run -d \
  --name yonca-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  yonca-frontend
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Check health status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 💻 Manual Deployment

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000

# Or run with gunicorn (production)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Development mode
npm run dev

# Production build and start
npm run build
npm start
```

---

## 🌐 Production Deployment

### Environment Variables

**Backend (.env)**
```env
DEBUG=False
CORS_ORIGINS=https://yourdomain.com
```

**Frontend (.env.production)**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Nginx Configuration

```nginx
# Backend proxy
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend proxy
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal is configured automatically
```

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    DEBUG: bool = False
    CORS_ORIGINS: list = ["https://yourdomain.com"]
    # Add more settings as needed
```

### Frontend Configuration

Edit `frontend/next.config.js`:

```javascript
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*`,
      },
    ];
  },
};
```

---

## 📊 Monitoring & Health Checks

### Health Check Endpoints

```bash
# Backend health
curl http://localhost:8000/health

# Backend stats
curl http://localhost:8000/api/v1/stats
```

### Docker Health Status

```bash
# Check container health
docker ps

# View detailed health
docker inspect yonca-backend | grep -A 10 Health
```

---

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart with Docker Compose
docker-compose down
docker-compose build
docker-compose up -d

# Or rebuild specific service
docker-compose up -d --build backend
```

### Update Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

**Frontend:**
```bash
cd frontend
npm update
```

### Backup Data

```bash
# Backup rule files
tar -czf yonca-data-backup-$(date +%Y%m%d).tar.gz backend/app/data/

# Restore from backup
tar -xzf yonca-data-backup-20251227.tar.gz
```

---

## 🐛 Troubleshooting

### Backend Issues

```bash
# Check logs
docker logs yonca-backend

# Manual deployment logs
cd backend
tail -f /tmp/yonca_backend.log

# Test Python imports
python -c "from app.main import app; print('OK')"
```

### Frontend Issues

```bash
# Check logs
docker logs yonca-frontend

# Clear Next.js cache
rm -rf frontend/.next
npm run build

# Check build errors
npm run build 2>&1 | grep -i error
```

### Network Issues

```bash
# Test backend from frontend container
docker exec yonca-frontend curl http://backend:8000/health

# Check Docker network
docker network inspect yonca-network

# Test CORS
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8000/api/v1/recommendations
```

---

## 📈 Performance Optimization

### Backend

- Use Gunicorn with multiple workers:
  ```bash
  gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
  ```

- Enable caching for rule loading (already implemented)

### Frontend

- Enable static export for pages that don't need SSR
- Use CDN for static assets
- Enable gzip compression in Nginx

### Database (Future Enhancement)

If you add a database:
- Use PostgreSQL for production
- Add connection pooling
- Implement Redis for caching

---

## 🔐 Security Recommendations

1. **Change default ports** in production
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** with SSL certificates
4. **Configure firewall** rules
5. **Regular updates** for dependencies
6. **Monitor logs** for suspicious activity
7. **Implement rate limiting** (TODO)

---

## 📞 Support

- GitHub Issues: <repository-url>/issues
- Documentation: See `/docs` folder
- API Docs: http://localhost:8000/docs

---

**Version:** 1.0.0
**Last Updated:** December 27, 2025
**Author:** Yonca Team - Digital Umbrella Challenge
