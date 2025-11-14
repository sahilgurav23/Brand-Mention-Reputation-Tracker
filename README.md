# Brand Mention & Reputation Tracker

Real-time brand mention monitoring with sentiment analysis and alerts.

## 📚 Documentation

**All documentation is in the `docs/` folder:**

- **[docs/README.md](./docs/README.md)** - Project overview
- **[docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)** - 3-step setup
- **[docs/FEATURES.md](./docs/FEATURES.md)** - What's included
- **[docs/API_QUICK_REFERENCE.md](./docs/API_QUICK_REFERENCE.md)** - Common API calls
- **[docs/SYSTEM_OVERVIEW.md](./docs/SYSTEM_OVERVIEW.md)** - Architecture
- **[docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)** - Common issues
- **[docs/SETUP.md](./docs/SETUP.md)** - Detailed setup
- **[docs/API.md](./docs/API.md)** - Full API docs
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Deep dive
- **[docs/INDEX.md](./docs/INDEX.md)** - File index

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

## ✨ Features

✅ Real-time dashboard  
✅ Sentiment analysis  
✅ Topic clustering  
✅ Spike detection  
✅ Alert management  
✅ 22 REST API endpoints  
✅ Interactive charts  
✅ Mention feed  

## 🏗️ Tech Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: PostgreSQL, pgvector
- **ML/NLP**: HuggingFace Transformers, Sentence Transformers
- **DevOps**: Docker, Docker Compose

## 📁 Project Structure

```
Brand-Mention-Reputation-Tracker/
├── docs/              # All documentation
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── database/          # PostgreSQL setup
└── README.md          # This file
```

## 📞 Need Help?

→ **Start here**: [docs/README.md](./docs/README.md)

## 🗂️ Important Note

**All documentation is in the `docs/` folder!**

- ✅ Go to `docs/` folder for all documentation
- ✅ Start with `docs/README.md`
- ✅ All 14 markdown files are there

**Old .md files in root can be deleted** (they're duplicates)

See [docs/FILES_TO_DELETE.md](./docs/FILES_TO_DELETE.md) for cleanup instructions.

---

**Status**: ✅ MVP Ready | **Version**: 1.0.0-beta