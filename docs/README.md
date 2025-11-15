# Brand Mention & Reputation Tracker

Real-time brand mention monitoring with sentiment analysis and alerts.

## ✨ What It Does

- 📊 Tracks brand mentions across multiple platforms
- 😊 Analyzes sentiment (positive/negative/neutral)
- 🏷️ Groups mentions by topic
- 🚨 Detects mention spikes
- 📈 Beautiful dashboard with charts
- 🔔 Real-time alerts

## 🚀 Quick Start

```bash
# Terminal 1: Database
cd database
docker-compose up -d

# Terminal 2: Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 3: Frontend
cd frontend
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📚 Documentation

### Getting Started
| File | Purpose |
|------|---------|
| [GETTING_STARTED.md](./GETTING_STARTED.md) | 3-step setup |
| [BACKEND_SETUP_FIX.md](./BACKEND_SETUP_FIX.md) | Fix pydantic_settings error |
| [PSYCOPG2_FIX.md](./PSYCOPG2_FIX.md) | Fix psycopg2-binary build error |
| [FEATURES.md](./FEATURES.md) | What's included |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues |

### Integration & Data
| File | Purpose |
|------|---------|
| [FREE_DATA_SOURCES.md](./FREE_DATA_SOURCES.md) | Free data sources comparison |
| [DATA_INTEGRATION_GUIDE.md](./DATA_INTEGRATION_GUIDE.md) | How to integrate data sources |

### Reference
| File | Purpose |
|------|---------|
| [API_QUICK_REFERENCE.md](./API_QUICK_REFERENCE.md) | API endpoints |
| [SYSTEM_OVERVIEW.md](./SYSTEM_OVERVIEW.md) | Architecture |
| [SETUP.md](./SETUP.md) | Detailed setup |
| [API.md](./API.md) | Full API docs |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Deep dive |

## 🏗️ Tech Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: PostgreSQL, pgvector
- **ML/NLP**: HuggingFace Transformers, Sentence Transformers
- **DevOps**: Docker, Docker Compose

## 📊 Features

✅ Real-time dashboard  
✅ Sentiment analysis  
✅ Topic clustering  
✅ Spike detection  
✅ Alert management  
✅ 22 REST API endpoints  
✅ Interactive charts  
✅ Mention feed  

## 🔧 Project Structure

```
Brand-Mention-Reputation-Tracker/
├── docs/              # All documentation
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── database/          # PostgreSQL setup
└── README.md          # This file
```

## 📞 Need Help?

- **Getting started?** → [GETTING_STARTED.md](./GETTING_STARTED.md)
- **Issues?** → [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **API help?** → [API_QUICK_REFERENCE.md](./API_QUICK_REFERENCE.md)
- **Architecture?** → [SYSTEM_OVERVIEW.md](./SYSTEM_OVERVIEW.md)

---

**Status**: ✅ MVP Ready | **Version**: 1.0.0-beta
