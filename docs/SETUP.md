# Setup Guide - Brand Mention & Reputation Tracker

This guide will walk you through setting up the Brand Mention & Reputation Tracker application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose** - [Download](https://www.docker.com/products/docker-desktop)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.10+** - [Download](https://www.python.org/)
- **Git** - [Download](https://git-scm.com/)

## Project Structure

```
Brand-Mention-Reputation-Tracker/
├── docs/                  # Documentation folder
├── frontend/              # Next.js React application
├── backend/               # FastAPI Python application
├── database/              # PostgreSQL with pgvector
└── README.md              # Project documentation
```

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Brand-Mention-Reputation-Tracker
```

## Step 2: Database Setup

### Start PostgreSQL with Docker

Navigate to the database directory and start the PostgreSQL container:

```bash
cd database
docker-compose up -d
```

This will:
- Pull the PostgreSQL 16 image with pgvector extension
- Initialize the database with the schema from `init/schema.sql`
- Create a volume for data persistence
- Expose the database on `localhost:5432`

**Database Credentials:**
- Host: `localhost`
- Port: `5432`
- Database: `trackerdb`
- Username: `tracker`
- Password: `password123`

### Verify Database Connection

```bash
# Using psql (if installed)
psql -h localhost -U tracker -d trackerdb

# Or using Docker
docker exec -it brand_tracker_db psql -U tracker -d trackerdb
```

## Step 3: Backend Setup

### Navigate to Backend Directory

```bash
cd backend
```

### Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the `backend` directory with the following content:

```env
# Database Configuration
DATABASE_URL=postgresql://tracker:password123@localhost:5432/trackerdb

# API Keys (Add your own - these are optional for development)
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
NEWS_API_KEY=your_news_api_key_here

# ML Models (Pre-trained models will be downloaded on first use)
SENTIMENT_MODEL=distilbert-base-uncased-finetuned-sst-2-english
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Alert Settings
ALERT_THRESHOLD=2.5
ALERT_WINDOW_HOURS=24

# Logging
LOG_LEVEL=INFO

# CORS Origins
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://127.0.0.1:3000"]
```

### Run Backend Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### First Run Notes

On the first run, the backend will download the ML models:
- `distilbert-base-uncased-finetuned-sst-2-english` (~250MB)
- `all-MiniLM-L6-v2` (~60MB)

This may take a few minutes. Subsequent runs will use cached models.

## Step 4: Frontend Setup

### Navigate to Frontend Directory

```bash
cd frontend
```

### Install Dependencies

```bash
npm install
```

### Configure Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Run Development Server

```bash
npm run dev
```

The frontend will start at `http://localhost:3000`

## Step 5: Verify Everything is Running

### Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### Check Frontend

Open your browser and navigate to `http://localhost:3000`

You should see the Brand Tracker dashboard with mock data.

## 🔄 Development Workflow

### Running All Services

**Terminal 1 - Database:**
```bash
cd database
docker-compose up
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Code Quality

**Backend:**
```bash
cd backend

# Format code
black app/
isort app/

# Lint
flake8 app/

# Type checking
mypy app/

# Run tests
pytest
```

**Frontend:**
```bash
cd frontend

# Lint
npm run lint

# Format (if configured)
npx prettier --write .
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:e2e  # End-to-end tests
```

## 🚀 Deployment

### Docker Deployment

Build and run all services with Docker:

```bash
docker-compose up -d
```

### Production Checklist

- [ ] Set strong database password
- [ ] Configure HTTPS/SSL
- [ ] Set up environment variables for production
- [ ] Enable CORS for production domain
- [ ] Set up proper database backups
- [ ] Configure logging and monitoring
- [ ] Set up rate limiting
- [ ] Enable authentication/authorization
- [ ] Test all API endpoints
- [ ] Load test the application

## 🐛 Troubleshooting

### Database Connection Issues

**Error: "could not connect to server"**

1. Verify Docker container is running:
   ```bash
   docker ps | grep brand_tracker_db
   ```

2. Check logs:
   ```bash
   docker logs brand_tracker_db
   ```

3. Restart container:
   ```bash
   docker-compose restart
   ```

### Backend Won't Start

**Error: "ModuleNotFoundError"**

1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

**Error: "Address already in use"**

The port 8000 is already in use. Either:
- Kill the process using port 8000
- Run on a different port: `uvicorn app.main:app --port 8001`

### Frontend Build Issues

**Error: "Cannot find module"**

1. Clear node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. Clear Next.js cache:
   ```bash
   rm -rf .next
   npm run dev
   ```

### ML Model Download Issues

**Error: "Connection timeout downloading model"**

The models are large and may take time to download. If you experience timeouts:

1. Set a longer timeout:
   ```bash
   export HF_HUB_TIMEOUT=600  # 10 minutes
   ```

2. Manually download models:
   ```python
   from sentence_transformers import SentenceTransformer
   from transformers import pipeline
   
   # Download sentiment model
   pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
   
   # Download embedding model
   SentenceTransformer("all-MiniLM-L6-v2")
   ```

---

**For more information, see:**
- [README.md](./README.md) - Main documentation
- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Quick commands
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [API.md](./API.md) - API reference
