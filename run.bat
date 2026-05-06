@echo off
REM AutoShop Pro Launcher
REM Run install.bat and initialize.bat first

setlocal enabledelayedexpansion

echo ===============================================
echo          AutoShop Pro - Launcher
echo ===============================================
echo.

for %%i in (.) do set "CURRENT_DIR=%%~ni"
if not "%CURRENT_DIR%"=="a_shop" (
    echo WARNING: Folder is named "%CURRENT_DIR%". Expected "a_shop".
    echo If this is a GitHub download, rename it to "a_shop".
    echo.
)

if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Python environment not found.
    echo Run install.bat first, then try run.bat again.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate the virtual environment.
    pause
    exit /b 1
)

echo Running database migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo ERROR: Database migration failed.
    pause
    exit /b 1
)
echo.

echo ===============================================
echo Launching AutoShop Pro...
echo Server will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C in this window to stop the server.
echo ===============================================
echo.

python manage.py runserver
pause