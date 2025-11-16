@echo off
REM Brand Mention & Reputation Tracker - Quick Start Script (Windows)
REM This script now only starts the backend and frontend directly.
REM Make sure PostgreSQL is already running (for example on localhost:5432).

echo.
echo ============================================
echo Brand Mention & Reputation Tracker
echo Quick Start Script (No Docker)
echo ============================================
echo.

echo [1/2] Starting Backend...
cd backend

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and install dependencies
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Start backend in a new window
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo Backend started in new window!
cd ..
echo.

REM Wait a moment for backend to start
timeout /t 3 /nobreak

echo [2/2] Starting Frontend...
cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Installing npm dependencies...
    call npm install
)

REM Start frontend in a new window
start "Frontend Server" cmd /k "npm run dev"
echo Frontend started in new window!
cd ..
echo.

echo ============================================
echo All services are starting!
echo ============================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo Database:  localhost:5432  ^(ensure this is running separately; no Docker is started by this script^)
echo.
echo Press any key to continue...
pause

echo.
echo To stop all services, just close the Backend and Frontend windows.
echo.
