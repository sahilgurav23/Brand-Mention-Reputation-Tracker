#!/bin/bash

# Brand Mention & Reputation Tracker - Quick Start Script (macOS/Linux)
# This script no longer uses Docker. It either:
# - On Railway: starts only the FastAPI backend with uvicorn.
# - Locally: starts backend + frontend for development, assuming PostgreSQL
#   is already running (e.g. on localhost:5432).

set -e

echo ""
echo "============================================"
echo "Brand Mention & Reputation Tracker"
echo "Quick Start Script (No Docker)"
echo "============================================"
echo ""

if [ -n "${RAILWAY_ENVIRONMENT:-}" ]; then
  echo "Running inside Railway – starting backend only (no Docker, no frontend)."

  cd backend

  # Check if venv exists
  if [ ! -d "venv" ]; then
      echo "Creating virtual environment..."
      python3 -m venv venv
  fi

  # Activate venv and install dependencies
  # shellcheck disable=SC1091
  source venv/bin/activate
  pip install -q -r requirements.txt

  PORT_TO_USE="${PORT:-8000}"
  echo "Starting uvicorn on port ${PORT_TO_USE}..."
  exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT_TO_USE}"
fi

# Local development path (non-Railway)
echo "Running locally – starting backend and frontend. Ensure PostgreSQL is already running."

cleanup() {
    echo ""
    echo "Cleaning up..."
    jobs -p | xargs -r kill 2>/dev/null || true
}

trap cleanup EXIT

echo "[1/2] Starting Backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
# shellcheck disable=SC1091
source venv/bin/activate
pip install -q -r requirements.txt

# Start backend in background
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
cd ..
echo ""

# Wait for backend to start
sleep 3

echo "[2/2] Starting Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
cd ..
echo ""

echo "============================================"
echo "All services are running!"
echo "============================================"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo "Database:  localhost:5432 (ensure this is running separately; this script does not start it)"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait
