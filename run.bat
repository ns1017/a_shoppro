@echo off
REM AutoShop Pro Launcher - Improved Sequential Version
REM For non-technical users

setlocal enabledelayedexpansion

echo ===============================================
echo          AutoShop Pro - Launcher
echo ===============================================
echo.

REM === 1. Directory rename check ===
echo Checking folder name...
for %%i in (.) do set "CURRENT_DIR=%%~ni"
if "%CURRENT_DIR%"=="a_shoppro-main" (
    echo Renaming folder from a_shoppro-main to a_shop...
    cd ..
    ren a_shoppro-main a_shop
    if errorlevel 1 (
        echo ERROR: Could not rename folder.
        echo Please manually rename the folder to "a_shop" and run this script again.
        pause
        exit /b 1
    )
    cd a_shop
    echo Folder renamed successfully.
) else if "%CURRENT_DIR%"=="a_shop" (
    echo Folder name is correct.
) else (
    echo WARNING: Folder is named "%CURRENT_DIR%". Expected "a_shop".
    echo If this is a GitHub download, rename it to "a_shop".
)
echo.

REM === 2. Python Check & Install ===
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found.
    echo Attempting to install Python 3.11 via winget...
    winget install -e --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    echo.
    echo IMPORTANT: Python installation may still be running.
    echo Please wait until the Python installer finishes, THEN press any key to continue...
    pause
    echo Re-checking Python...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Python is still not available.
        echo Please install it manually from https://www.python.org/downloads/ (check "Add to PATH")
        pause
        exit /b 1
    )
) else (
    echo Python found: 
    python --version
)
echo.

REM === 3. Node.js Check & Install ===
echo Checking Node.js...
npm --version >nul 2>&1
if errorlevel 1 (
    echo Node.js not found.
    echo Attempting to install Node.js via winget...
    winget install -e --id OpenJS.NodeJS --accept-source-agreements --accept-package-agreements
    echo.
    echo IMPORTANT: Node.js installation may still be running.
    echo Wait for it to finish, THEN press any key...
    pause
    echo Re-checking Node.js...
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo Node.js is still not available.
        echo Please install it manually from https://nodejs.org/
        pause
        exit /b 1
    )
) else (
    echo Node.js found:
    node --version
    echo npm found:
    npm --version
)
echo ===============================================
echo.

REM === 4. Virtual Environment ===
if not exist ".venv\Scripts\activate.bat" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create venv.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

call .venv\Scripts\activate.bat
echo Virtual environment activated.
echo.

REM === 5. Python Dependencies ===
echo Installing/updating Python packages...
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo Warning: pip install had issues. Check your internet connection.
)
echo.

REM === 6. Tailwind CSS ===
if not exist "static\css\style.css" (
    echo Building Tailwind CSS...
    if not exist "node_modules" (
        echo Running npm install...
        call npm install
    )
    call npm run build:css
    echo CSS build completed.
) else (
    echo CSS file already exists.
)
echo.

REM === 7. Database Setup ===
echo Running database migrations...
python manage.py migrate --noinput
echo.

echo Setting up admin account (if needed)...
python manage.py createsuperuser
echo.

REM === 8. Start Server ===
echo ===============================================
echo Launching AutoShop Pro...
echo Server will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C in this window to stop the server.
echo ===============================================
echo.

python manage.py runserver
pause