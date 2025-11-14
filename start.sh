#!/bin/bash

# Brand Mention & Reputation Tracker - Quick Start Script (macOS/Linux)
# This script starts all services for development

set -e

echo ""
echo "============================================"
echo "Brand Mention & Reputation Tracker"
echo "Quick Start Script"
echo "============================================"
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Cleaning up..."
    # Kill background processes
    jobs -p | xargs -r kill 2>/dev/null || true
}

trap cleanup EXIT

echo "[1/3] Starting Database..."
cd database
docker-compose up -d
cd ..
echo "Database started successfully!"
echo ""

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 3

echo "[2/3] Starting Backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
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

echo "[3/3] Starting Frontend..."
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
echo "Database:  localhost:5432"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait
