@echo off
REM Physical AI Robotics Chatbot - Start Script for Windows
REM This script starts both the backend and frontend servers

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ================================================================
echo 🤖 Physical AI Robotics Chatbot - Startup Script
echo ================================================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Please create .env file with:
    echo   - DATABASE_URL (from Neon)
    echo   - ANTHROPIC_API_KEY (from Claude)
    echo.
    echo Copy from .env.example and add your credentials
    pause
    exit /b 1
)

echo ✓ .env file found
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found! Please install Python 3.10+
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if backend dependencies installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo ❚ Installing dependencies...
    cd backend
    pip install -r requirements.txt
    cd ..
    echo ✓ Dependencies installed
    echo.
)

echo.
echo ================================================================
echo Starting Servers...
echo ================================================================
echo.

REM Start backend in new window
echo [1/2] Starting Backend Server (Port 8000)...
start "Physical AI Chatbot - Backend" cmd /k "cd backend && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo.
echo ⏳ Waiting for backend to start (5 seconds)...
timeout /t 5 /nobreak

REM Start frontend in new window
echo.
echo [2/2] Starting Frontend Server (Port 3000)...
start "Physical AI Chatbot - Frontend" cmd /k "cd frontend && python server.py"

echo.
echo ================================================================
echo ✅ SERVERS STARTED!
echo ================================================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 📡 Backend:  http://localhost:8000
echo 📚 Docs:     http://localhost:8000/api/docs
echo.
echo ================================================================
echo.
echo 📝 Next steps:
echo    1. Open http://localhost:3000 in your browser
echo    2. Sign up or login
echo    3. Start asking questions!
echo.
echo ❌ To stop servers: Close both command windows
echo.
echo ⚠️  Keep these windows open while using the chatbot
echo.
pause
