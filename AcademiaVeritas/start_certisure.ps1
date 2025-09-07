# CertiSure Application Startup Script
# This script starts both backend and frontend servers for the AcademiaVeritas project

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "🚀 Starting CertiSure Application" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Get the project root directory
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendPath = Join-Path $ProjectRoot "backend"
$FrontendPath = Join-Path $ProjectRoot "frontend"

# Function to check if a service is running on a specific port
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to start backend server
function Start-Backend {
    Write-Host "🔧 Starting Backend Server..." -ForegroundColor Yellow
    
    # Check if backend is already running
    if (Test-Port -Port 5001) {
        Write-Host "✅ Backend server is already running on port 5001" -ForegroundColor Green
        return
    }
    
    # Navigate to backend directory
    Push-Location $BackendPath
    
    try {
        # Check if virtual environment exists
        if (!(Test-Path ".venv")) {
            Write-Host "   Creating Python virtual environment..." -ForegroundColor White
            python -m venv .venv
        }
        
        # Start backend as background job
        Write-Host "   Starting backend server on port 5001..." -ForegroundColor White
        $backendJob = Start-Job -ScriptBlock {
            param($BackendPath)
            Set-Location $BackendPath
            & ".\.venv\Scripts\python.exe" "app.py"
        } -ArgumentList $BackendPath
        
        # Wait a moment for the server to start
        Start-Sleep -Seconds 3
        
        # Check if backend started successfully
        if (Test-Port -Port 5001) {
            Write-Host "✅ Backend server started successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Backend server failed to start" -ForegroundColor Red
        }
    }
    finally {
        Pop-Location
    }
}

# Function to start frontend server
function Start-Frontend {
    Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Yellow
    
    # Check if frontend is already running
    if (Test-Port -Port 5173) {
        Write-Host "✅ Frontend server is already running on port 5173" -ForegroundColor Green
        return
    }
    
    # Navigate to frontend directory
    Push-Location $FrontendPath
    
    try {
        # Check if node_modules exists
        if (!(Test-Path "node_modules")) {
            Write-Host "   Installing Node.js dependencies..." -ForegroundColor White
            npm install
        }
        
        Write-Host "   Starting frontend server on port 5173..." -ForegroundColor White
        Write-Host "   Frontend will be available at: http://localhost:5173" -ForegroundColor Cyan
        Write-Host "   Backend API is available at: http://localhost:5001" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Press Ctrl+C to stop the servers" -ForegroundColor Yellow
        Write-Host ""
        
        # Start frontend (this will run in foreground)
        npm run dev
    }
    finally {
        Pop-Location
    }
}

# Function to check prerequisites
function Test-Prerequisites {
    Write-Host "🔍 Checking Prerequisites..." -ForegroundColor Yellow
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
        return $false
    }
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>$null
        Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
        return $false
    }
    
    # Check MySQL
    try {
        $mysqlServices = Get-Service | Where-Object { $_.Name -like "*MySQL*" -and $_.Status -eq "Running" }
        if ($mysqlServices) {
            Write-Host "✅ MySQL service is running" -ForegroundColor Green
        } else {
            Write-Host "❌ MySQL service is not running" -ForegroundColor Red
            Write-Host "   Please start MySQL service manually" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "⚠️  Could not verify MySQL status" -ForegroundColor Yellow
    }
    
    return $true
}

# Main execution
try {
    # Check prerequisites
    if (!(Test-Prerequisites)) {
        Write-Host ""
        Write-Host "❌ Prerequisites check failed. Please install missing components." -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    
    # Start backend
    Start-Backend
    
    Write-Host ""
    
    # Start frontend (this will keep the script running)
    Start-Frontend
}
catch {
    Write-Host ""
    Write-Host "❌ An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    # Cleanup: Stop background jobs when script exits
    Get-Job | Stop-Job
    Get-Job | Remove-Job
    Write-Host ""
    Write-Host "👋 CertiSure application stopped" -ForegroundColor Cyan
}
