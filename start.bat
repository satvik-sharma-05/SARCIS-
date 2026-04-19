@echo off
echo ========================================
echo   SARCIS - Clean MVP Startup
echo ========================================
echo.

echo Starting Backend...
cd backend
start "Backend" cmd /k "python main.py"
cd ..

timeout /t 3 /nobreak >nul

echo Starting Frontend...
cd frontend
start "Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo ========================================
