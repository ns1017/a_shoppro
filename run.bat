@echo off
REM AutoShop Pro Launcher
REM This script activates the venv, runs migrations, and starts the Django server

setlocal enabledelayedexpansion

echo ===============================================
echo AutoShop Pro - Launching...
echo ===============================================

REM Check if venv exists
if not exist ".venv\Scripts\activate.bat" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate venv
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist ".venv\Lib\site-packages\django" (
    echo Installing Python dependencies... An internet connection is required for this step.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Build CSS if style.css doesn't exist
if not exist "static\css\style.css" (
    echo Building Tailwind CSS...
    if not exist "node_modules" (
        call npm install
        if errorlevel 1 (
            echo WARNING: npm install failed. You may need to install Node.js from https://nodejs.org/
        )
    )
    if exist "node_modules" (
        call npm run build:css
    )
)

REM Run migrations
echo Running database migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)

REM Create superuser if needed
echo.
echo Creating admin account (if you don't have one yet)...
python manage.py createsuperuser
echo.
echo.
echo ===============================================
echo Server starting at http://127.0.0.1:8000/
echo Press Ctrl+C to stop
echo ===============================================
echo.

python manage.py runserver

pause
