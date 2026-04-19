@echo off
echo ========================================
echo   SARCIS - Simple Startup (No Docker)
echo ========================================
echo.

REM Kill any existing processes
echo Stopping existing processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *next*" 2>nul
timeout /t 2 /nobreak >nul

REM Start Backend
echo Starting Backend API...
cd backend
start "Backend API" cmd /k "python main.py"
cd ..
timeout /t 3 /nobreak >nul

REM Start Frontend
echo Starting Frontend...
cd frontend
start "Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo   All services started!
echo ========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   Docs:     http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to stop all services...
pause >nul

REM Stop all services
echo Stopping all services...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend API" 2>nul
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Frontend" 2>nul

echo All services stopped.
