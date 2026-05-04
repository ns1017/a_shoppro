@echo off
REM AutoShop Pro Initializer - prepares the database and first-time data

setlocal enabledelayedexpansion

echo ===============================================
echo      AutoShop Pro - Initialize
echo ===============================================
echo.

for %%i in (.) do set "CURRENT_DIR=%%~ni"
if not "%CURRENT_DIR%"=="a_shop" (
    echo WARNING: Folder is named "%CURRENT_DIR%". Expected "a_shop".
    echo If this is a GitHub download, rename it to "a_shop".
    echo.
)

if not exist ".venv\Scripts\activate.bat" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create the virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Python environment not found.
    echo Please install Python and try initialize.bat again.
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

echo Creating a superuser is optional but recommended.
echo If you want admin access, follow the prompts now.
choice /c YN /m "Create or update a superuser now"
if errorlevel 2 goto skip_superuser
python manage.py createsuperuser
if errorlevel 1 (
    echo Warning: createsuperuser did not complete successfully.
)
echo.

:skip_superuser
echo Loading demo data is optional.
choice /c YN /m "Seed demo data now"
if errorlevel 2 goto done
python manage.py seed_demo_data
if errorlevel 1 (
    echo Warning: seed_demo_data did not complete successfully.
)

:done
echo.
echo Initialize complete.
echo Next: run.bat to launch the app.
pause