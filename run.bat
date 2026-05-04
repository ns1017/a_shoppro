@echo off
REM AutoShop Pro Launcher
REM This script activates the venv, runs migrations, and starts the Django server

setlocal enabledelayedexpansion

echo ===============================================
echo AutoShop Pro - Launching...
echo ===============================================

REM Check and rename directory if it's in GitHub export format (a_shoppro-main, etc)
echo.
echo Checking directory name...
for %%i in (.) do set "CURRENT_DIR=%%~ni"
if "%CURRENT_DIR%"=="a_shoppro-main" (
    echo Found GitHub export folder name. Renaming to a_shop...
    cd ..
    ren a_shoppro-main a_shop
    if errorlevel 1 (
        echo ERROR: Could not rename directory. Please manually rename 'a_shoppro-main' to 'a_shop'
        pause
        exit /b 1
    )
    cd a_shop
    echo Directory renamed successfully to a_shop
) else if "%CURRENT_DIR%"=="a_shop" (
    echo Directory already named correctly: a_shop
) else (
    echo WARNING: Current directory is '%CURRENT_DIR%', not 'a_shop'
    echo If you downloaded from GitHub, the folder may need manual renaming for consistency
)

echo ===============================================

REM Check for Python
echo.
echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Attempting to install Python via winget...
    winget install -e --id Python.Python.3.11 >nul 2>&1
    if errorlevel 1 (
        echo.
        echo FAILED: Could not auto-install Python.
        echo Please install Python 3.10+ manually from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    ) else (
        echo Python installed successfully. Please restart this script.
        pause
        exit /b 0
    )
) else (
    echo Python found: 
    python --version
)

REM Check for Node.js/npm
echo.
echo Checking for Node.js and npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js/npm is not installed or not in PATH.
    echo.
    echo Attempting to install Node.js via winget...
    winget install -e --id OpenJS.NodeJS >nul 2>&1
    if errorlevel 1 (
        echo.
        echo FAILED: Could not auto-install Node.js.
        echo Please install Node.js from https://nodejs.org/
        echo After installation, please restart this script.
        echo.
        pause
        exit /b 1
    ) else (
        echo Node.js installed successfully. Please restart this script.
        pause
        exit /b 0
    )
) else (
    echo Node.js found:
    node --version
    echo npm found:
    npm --version
)

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
