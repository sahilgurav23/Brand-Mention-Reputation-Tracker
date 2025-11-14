# ⚡ Quick Start - 5 Minutes

Get the Brand Mention & Reputation Tracker running in 5 minutes!

## Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.10+

## Step 1: Start Database (1 min)

```bash
cd database
docker-compose up -d
```

Wait for the container to start (~30 seconds).

## Step 2: Start Backend (1 min)

Open a new terminal:

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

## Step 3: Start Frontend (1 min)

Open another new terminal:

```bash
cd frontend
npm install
npm run dev
```

Wait for: `ready - started server on 0.0.0.0:3000`

## Step 4: Access the App (1 min)

Open your browser:

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## ✅ Done!

You should see the Brand Tracker dashboard with:
- Real-time metrics
- Interactive charts
- Alert feed
- Mentions feed

---

## 🔧 Common Issues

### "npm install" fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### "Port already in use"
```bash
# Change port in backend
python -m uvicorn app.main:app --reload --port 8001

# Change port in frontend
npm run dev -- -p 3001
```

### "Database connection failed"
```bash
# Check if Docker is running
docker ps

# Check database logs
docker logs brand_tracker_db

# Restart database
cd database
docker-compose restart
```

### "Module not found" errors
```bash
# Backend
cd backend
pip install -r requirements.txt --force-reinstall

# Frontend
cd frontend
npm install --legacy-peer-deps
```

---

## 📊 What You Get

✅ Real-time dashboard  
✅ Sentiment analysis  
✅ Topic clustering  
✅ Spike detection  
✅ Alert management  
✅ REST API (22 endpoints)  

---

## 🌐 Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Database | localhost:5432 |

---

## 📚 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Read the docs**: See [README.md](./README.md)
3. **Integrate data**: See [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)

---

## 🛑 Stop Services

```bash
# Stop frontend (Ctrl+C in frontend terminal)
# Stop backend (Ctrl+C in backend terminal)
# Stop database
cd database
docker-compose down
```

---

**For detailed setup, see [SETUP.md](./SETUP.md)**
