@echo off
REM HackCamp - Restaurant Finder Master Startup Script (Windows)
REM Usage: run.bat <GEMINI_API_KEY> <GOOGLE_MAPS_API_KEY>
REM Example: run.bat AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo.
    echo HackCamp - Restaurant Finder
    echo.
    echo ERROR: Missing API keys!
    echo.
    echo Usage: run.bat ^<GEMINI_API_KEY^> ^<GOOGLE_MAPS_API_KEY^>
    echo.
    echo Example:
    echo   run.bat AIzaSyAB8Bd87WX51mNeSkkDAb2sfDd4wu_5-Ks yAIzaSyD1RfZ4-onqnSVPN-tJVGThxWPOTTz3qFs
    echo.
    exit /b 1
)

if "%~2"=="" (
    echo.
    echo ERROR: Missing Google Maps API key!
    echo.
    echo Usage: run.bat ^<GEMINI_API_KEY^> ^<GOOGLE_MAPS_API_KEY^>
    echo.
    exit /b 1
)

set GEMINI_KEY=%~1
set MAPS_KEY=%~2

echo.
echo ============================================================
echo HackCamp - Restaurant Finder Starting
echo ============================================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM ========================================================
REM BACKEND SETUP
REM ========================================================

echo [Backend] Setting up backend...
set BACKEND_DIR=%SCRIPT_DIR%backend
cd /d "%BACKEND_DIR%"

echo [Backend] Configuring environment variables...
(
    echo GOOGLE_MAPS_API_KEY=%MAPS_KEY%
    echo GEMINI_API_KEY=%GEMINI_KEY%
    echo BACKEND_URL=http://localhost:8000
    echo FRONTEND_URL=http://localhost:3000
) > .env
echo [Backend] ✓ .env file created

REM Check if virtual environment exists
if not exist "venv" (
    echo [Backend] Creating Python virtual environment...
    python -m venv venv
    echo [Backend] ✓ Virtual environment created
)

REM Activate virtual environment
echo [Backend] Activating virtual environment...
call venv\Scripts\activate.bat
echo [Backend] ✓ Virtual environment activated

REM Check if requirements are installed
if not exist "venv\Scripts\uvicorn.exe" (
    echo [Backend] Installing Python dependencies...
    pip install -r requirements.txt > nul 2>&1
    echo [Backend] ✓ Python dependencies installed
) else (
    echo [Backend] ✓ Python dependencies already installed
)

REM Start backend server
echo [Backend] Starting FastAPI backend server on http://localhost:8000...
start "Backend - FastAPI" python run.py
echo [Backend] ✓ Backend server started

REM Wait for backend to be ready
echo [Backend] Waiting for backend to be ready...
timeout /t 5 /nobreak

REM ========================================================
REM FRONTEND SETUP
REM ========================================================

echo [Frontend] Setting up frontend...
set FRONTEND_DIR=%SCRIPT_DIR%frontend
cd /d "%FRONTEND_DIR%"

echo [Frontend] Configuring environment variables...
(
    echo REACT_APP_GOOGLE_MAPS_API_KEY=%MAPS_KEY%
    echo REACT_APP_BACKEND_URL=http://localhost:8000
) > .env
echo [Frontend] ✓ .env file created

REM Check if node_modules exists
if not exist "node_modules" (
    echo [Frontend] Installing npm dependencies (this may take a few minutes)...
    call npm install > nul 2>&1
    echo [Frontend] ✓ npm dependencies installed
) else (
    echo [Frontend] ✓ npm dependencies already installed
)

REM Start frontend server
echo [Frontend] Starting React frontend server on http://localhost:3000...
start "Frontend - React" cmd /k "npm start"
echo [Frontend] ✓ Frontend server started

REM ========================================================
REM SUCCESS
REM ========================================================

echo.
echo ============================================================
echo HackCamp is Running!
echo ============================================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close the windows to stop the servers.
echo.
pause
