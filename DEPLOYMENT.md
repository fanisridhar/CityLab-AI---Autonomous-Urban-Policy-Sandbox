# Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker and Docker Compose (optional)

### Backend Setup

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys and database URL
```

4. **Set up database:**
```bash
# Start PostgreSQL (if not running)
# Create database
createdb citylab_db

# Run migrations
alembic upgrade head
```

5. **Start Redis:**
```bash
redis-server
```

6. **Start backend server:**
```bash
uvicorn app.main:app --reload
```

7. **Start Celery worker (in separate terminal):**
```bash
celery -A app.celery_app worker --loglevel=info
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Set up environment variables:**
```bash
cp .env.example .env.local
# Edit .env.local with your API URL and Mapbox token
```

3. **Start development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Docker Deployment

### Using Docker Compose

1. **Set up environment variables:**
```bash
# Create .env file in project root
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
export NEXT_PUBLIC_MAPBOX_TOKEN=your_token
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Run database migrations:**
```bash
docker-compose exec backend alembic upgrade head
```

4. **Access services:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Individual Docker Containers

**Backend:**
```bash
cd backend
docker build -t citylab-backend .
docker run -p 8000:8000 --env-file .env citylab-backend
```

**Frontend:**
```bash
cd frontend
docker build -t citylab-frontend .
docker run -p 3000:3000 --env-file .env.local citylab-frontend
```

## Production Deployment

### Backend (FastAPI)

**Recommended platforms:**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Railway
- Render

**Environment variables needed:**
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key (optional)
- `SECRET_KEY`: Secret key for security
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins

**Database setup:**
- Use managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.)
- Run migrations: `alembic upgrade head`

**Celery workers:**
- Deploy separate worker instances
- Use Redis for message broker
- Consider using Flower for monitoring: `celery -A app.celery_app flower`

### Frontend (Next.js)

**Recommended platforms:**
- Vercel (optimized for Next.js)
- Netlify
- AWS Amplify
- Cloudflare Pages

**Build command:**
```bash
npm run build
```

**Environment variables:**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_MAPBOX_TOKEN`: Mapbox access token

### Database

**PostgreSQL:**
- Minimum: 2GB RAM, 1 CPU
- Recommended: 4GB+ RAM, 2+ CPUs
- Use connection pooling (PgBouncer recommended)

**Redis:**
- Minimum: 256MB RAM
- Recommended: 1GB+ RAM
- Use Redis Sentinel for high availability

### Vector Database

**Chroma (default):**
- Runs embedded in backend
- Data persisted to disk
- No separate deployment needed

**Pinecone (optional):**
- Managed service
- Set `USE_PINECONE=True` in backend config
- Provide `PINECONE_API_KEY` and `PINECONE_ENVIRONMENT`

## Scaling Considerations

1. **Horizontal scaling:**
   - Backend: Multiple FastAPI instances behind load balancer
   - Celery workers: Scale based on queue length
   - Frontend: CDN for static assets

2. **Database:**
   - Read replicas for read-heavy workloads
   - Connection pooling essential

3. **Caching:**
   - Redis for session storage and caching
   - CDN for frontend assets

4. **Monitoring:**
   - Application: Prometheus + Grafana
   - Logs: ELK stack or cloud logging
   - Errors: Sentry or similar

## Security Checklist

- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS/TLS
- [ ] Set proper CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable database SSL connections
- [ ] Regular security updates
- [ ] Rate limiting on API endpoints
- [ ] Input validation and sanitization
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention (React auto-escapes)

## Troubleshooting

### Backend won't start
- Check database connection
- Verify Redis is running
- Check environment variables
- Review logs: `docker-compose logs backend`

### Frontend build fails
- Clear `.next` directory: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node.js version (18+)

### Database migration errors
- Backup database first
- Check Alembic version: `alembic current`
- Review migration files

### Celery tasks not executing
- Verify Redis connection
- Check worker logs: `celery -A app.celery_app worker --loglevel=debug`
- Ensure task is registered

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/fanisridhar/CityLab-AI---Autonomous-Urban-Policy-Sandbox/issues)
- Documentation: See README.md
