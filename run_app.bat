@echo off
echo ==========================================
echo UDA-Q Agent - Universal Data Quality Fixer
echo ==========================================
echo.

echo [1/2] Setting up Backend (Django)...
start "Backend Server" cmd /k "cd backend && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver || pause"

echo [2/2] Setting up Frontend (React)...
start "Frontend Client" cmd /k "cd frontend && npm install && npm run dev || pause"

echo.
echo ========================================================
echo Application is starting...
echo If a window closes immediately, there was an error.
echo ========================================================
pause
