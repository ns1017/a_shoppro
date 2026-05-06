# AutoShop Pro Installer - installs runtime dependencies and builds assets

$ErrorActionPreference = "Continue"

Write-Host "==============================================="
Write-Host "        AutoShop Pro - Install"
Write-Host "==============================================="
Write-Host ""

$currentDir = (Get-Item .).BaseName
if ($currentDir -ne "a_shop") {
    Write-Host "WARNING: Folder is named '$currentDir'. Expected 'a_shop'."
    Write-Host "If this is a GitHub download, rename it to 'a_shop'."
    Write-Host ""
}

# Check Python
Write-Host "Checking Python..."
$pythonExists = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
if (-not $pythonExists) {
    Write-Host "Python not found."
    Write-Host "Attempting to install Python 3.11 via winget..."
    & winget install Python.Python.3
    Write-Host ""
    Write-Host "IMPORTANT: Python installation may still be running."
    Read-Host "Please wait until the Python installer finishes, then press Enter to continue"
    
    Write-Host "Re-checking Python..."
    $pythonExists = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
    if (-not $pythonExists) {
        Write-Host "Python is still not available."
        Write-Host "Please install it manually from https://www.python.org/downloads/ (check 'Add to PATH')"
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "Python found:"
    python --version
}
Write-Host ""

# Create venv
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create venv."
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Virtual environment created."
} else {
    Write-Host "Virtual environment already exists."
}
Write-Host ""

# Activate venv
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Virtual environment activation had issues, but continuing..."
}
Write-Host ""

# Install Python packages
Write-Host "Installing/updating Python packages..."
pip install -r requirements.txt --upgrade
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: pip install had issues. Check your internet connection."
}
Write-Host ""

# Check Node.js
Write-Host "Checking Node.js..."
$npmExists = $null -ne (Get-Command npm -ErrorAction SilentlyContinue)
if (-not $npmExists) {
    Write-Host "Node.js not found."
    Write-Host "Attempting to install Node.js via winget..."
    & winget install OpenJS.NodeJS
    Write-Host ""
    Write-Host "IMPORTANT: Node.js installation may still be running."
    Read-Host "Wait for it to finish, then press Enter to continue"
    
    Write-Host "Re-checking Node.js..."
    $npmExists = $null -ne (Get-Command npm -ErrorAction SilentlyContinue)
    if (-not $npmExists) {
        Write-Host "Node.js is still not available."
        Write-Host "Please install it manually from https://nodejs.org/"
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host "Node.js check passed."
node --version 2>$null
npm --version 2>$null
Write-Host ""

# Install npm dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "Running npm install..."
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: npm install had issues, but continuing..."
    }
} else {
    Write-Host "node_modules already exists."
}
Write-Host ""

# Build Tailwind CSS
Write-Host "Building Tailwind CSS..."
npm run build:css
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: npm CSS build had issues, but continuing..."
}
Write-Host "CSS build completed."
Write-Host ""

Write-Host "Install complete."
Write-Host "Next: run initialize.ps1 to set up the database, then run.ps1 to launch the app."
Read-Host "Press Enter to exit"
