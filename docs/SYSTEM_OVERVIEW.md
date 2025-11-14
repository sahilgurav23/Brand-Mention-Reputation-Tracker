# System Overview

## Architecture

```
Frontend (Next.js)
    ↓ HTTP/REST
Backend (FastAPI)
    ↓ SQL
Database (PostgreSQL)
```

## Components

### Frontend
- Dashboard with charts
- Real-time metrics
- Alert notifications
- Mention feed

### Backend
- 22 REST API endpoints
- Sentiment analysis
- Topic clustering
- Spike detection
- Alert management

### Database
- PostgreSQL 16
- pgvector for embeddings
- 4 tables: mentions, alerts, alert_configs, analytics_cache

## Data Flow

```
External Sources
    ↓
API Endpoint
    ↓
Sentiment Analysis (DistilBERT)
    ↓
Topic Clustering (Embeddings)
    ↓
Database Storage
    ↓
Alert Evaluation
    ↓
Frontend Display
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, SQLAlchemy |
| Database | PostgreSQL, pgvector |
| ML/NLP | HuggingFace Transformers, Sentence Transformers |
| DevOps | Docker, Docker Compose |

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture.
