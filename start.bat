@echo off
REM Brand Mention & Reputation Tracker - Quick Start Script (Windows)
REM This script starts all services for development

echo.
echo ============================================
echo Brand Mention & Reputation Tracker
echo Quick Start Script
echo ============================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [1/3] Starting Database...
cd database
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start database
    pause
    exit /b 1
)
cd ..
echo Database started successfully!
echo.

REM Wait for database to be ready
echo Waiting for database to be ready...
timeout /t 3 /nobreak

echo [2/3] Starting Backend...
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

echo [3/3] Starting Frontend...
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
echo Database:  localhost:5432
echo.
echo Press any key to continue...
pause

echo.
echo To stop all services:
echo 1. Close the Backend and Frontend windows
echo 2. Run: docker-compose -f database/docker-compose.yml down
echo.
