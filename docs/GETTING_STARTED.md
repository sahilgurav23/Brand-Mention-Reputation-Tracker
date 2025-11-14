# Getting Started

## 🚀 Start in 3 Steps

### Step 1: Database
```bash
cd database
docker-compose up -d
```

### Step 2: Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Step 3: Frontend
```bash
cd frontend
npm install
npm run dev
```

## ✅ Done!

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📚 Documentation

- **[README.md](./README.md)** - Project overview
- **[API.md](./API.md)** - All API endpoints
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design
- **[SETUP.md](./SETUP.md)** - Detailed setup
- **[QUICK_START.md](./QUICK_START.md)** - 5-minute start
