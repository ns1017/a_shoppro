@echo off
REM AutoShop Pro Launcher - Fixed version
setlocal enabledelayedexpansion

echo ===============================================
echo          AutoShop Pro - Launcher
echo ===============================================
echo.

:: Check folder name
for %%i in (.) do set "CURRENT_DIR=%%~ni"
if not "%CURRENT_DIR%"=="a_shop" (
    echo WARNING: Folder is named "%CURRENT_DIR%". Expected "a_shop".
    echo.
)

:: Check virtual environment
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Python virtual environment not found.
    echo Please run install.bat first.
    pause
    exit /b 1
)

:: Activate venv
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
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
echo Network Configuration
echo ===============================================
echo.
echo 1) Local Only (127.0.0.1:8000) - Default
echo 2) Network-Wide (0.0.0.0:8000)
echo 3) Custom Host:Port
echo.

choice /C 123 /D 1 /T 30 /M "Select option [1-3, default 1]: "
set MENU_CHOICE=!errorlevel!

set SERVER_HOST=127.0.0.1
set SERVER_PORT=8000
set ACCESS_URL=http://127.0.0.1:8000/
set HOST_IP=Unavailable

REM Detect first IPv4 address from ipconfig output (host LAN IP)
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
    if "!HOST_IP!"=="Unavailable" (
        set "HOST_IP=%%i"
        set "HOST_IP=!HOST_IP: =!"
    )
)

if !MENU_CHOICE! equ 2 (
    set SERVER_HOST=0.0.0.0
    set DJANGO_ALLOWED_HOSTS=*

    if not "!HOST_IP!"=="Unavailable" (
        set ACCESS_URL=http://!HOST_IP!:!SERVER_PORT!/
    )
    echo Network-wide mode enabled.

) else if !MENU_CHOICE! equ 3 (
    set /p CUSTOM_ADDR="Enter host:port [default 127.0.0.1:8000]: "
    if not "!CUSTOM_ADDR!"=="" (
        for /f "tokens=1,2 delims=:" %%a in ("!CUSTOM_ADDR!") do (
            set SERVER_HOST=%%a
            if not "%%b"=="" set SERVER_PORT=%%b
        )
        set ACCESS_URL=http://!CUSTOM_ADDR!/
    )
)

echo.
echo ===============================================
echo Launching AutoShop Pro...
echo Server will be available at: !ACCESS_URL!
echo Host device IP (LAN): !HOST_IP!
if !MENU_CHOICE! equ 2 if not "!HOST_IP!"=="Unavailable" echo Network access URL: http://!HOST_IP!:!SERVER_PORT!/
echo Press Ctrl+C to stop the server.
echo ===============================================
echo.

:: Run server with error handling
python manage.py runserver !SERVER_HOST!:!SERVER_PORT!

echo.
echo Server has stopped or crashed.
pause
