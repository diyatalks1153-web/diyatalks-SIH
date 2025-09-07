# CertiSure Application - Startup Instructions

## Quick Start (Recommended)

### Option 1: Double-click the batch file
1. Simply double-click `start_certisure.bat` in the project root directory
2. This will automatically start both backend and frontend servers
3. Your browser will be able to access the application at `http://localhost:5173`

### Option 2: Run PowerShell script
1. Right-click on `start_certisure.ps1` and select "Run with PowerShell"
2. Or open PowerShell in the project directory and run: `.\start_certisure.ps1`

## Manual Startup (For Development)

### Backend Server
1. Open PowerShell/Command Prompt
2. Navigate to the `backend` directory
3. Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
4. Run: `python app.py`
5. Backend will be available at `http://localhost:5001`

### Frontend Server
1. Open another PowerShell/Command Prompt window
2. Navigate to the `frontend` directory  
3. Run: `npm run dev`
4. Frontend will be available at `http://localhost:5173`

## Troubleshooting

### "Cannot connect to server" Error
This error occurs when the backend server is not running. Solutions:
1. **Use the startup scripts**: Run `start_certisure.bat` or `start_certisure.ps1`
2. **Check if MySQL is running**: Ensure MySQL service is started
3. **Port conflicts**: Make sure ports 5001 (backend) and 5173 (frontend) are available
4. **Manual restart**: Stop all servers and use the startup scripts again

### Port Configuration
- **Backend**: Runs on port **5001** (configured in `backend/.env`)
- **Frontend**: Runs on port **5173** (Vite default)
- **API Endpoints**: All backend APIs are accessible at `http://localhost:5001/api/`

### Database Connection
- The application uses MySQL database `academia_veritas`
- Default credentials are in `backend/.env` file
- Make sure MySQL server is running before starting the application

## File Structure
```
AcademiaVeritas/
├── start_certisure.bat          # Quick start batch file
├── start_certisure.ps1          # PowerShell startup script
├── backend/
│   ├── .env                     # Environment variables (PORT=5001)
│   ├── app.py                   # Main Flask application
│   ├── .venv/                   # Python virtual environment
│   └── ...
├── frontend/
│   ├── src/apiService.js        # API configuration (port 5001)
│   ├── vite.config.js          # Frontend configuration
│   └── ...
└── STARTUP_INSTRUCTIONS.md     # This file
```

## Common Issues and Solutions

### 1. "Execution Policy" Error
If you get an execution policy error when running PowerShell scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. MySQL Connection Error  
- Ensure MySQL service is running: Check Windows Services
- Verify database credentials in `backend/.env`
- Make sure database `academia_veritas` exists

### 3. Port Already in Use
- Check what's using the ports: `netstat -ano | findstr :5001`
- Kill the process or use different ports
- Restart your computer if needed

### 4. Node.js Dependencies Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 5. Python Dependencies Issues
```bash
cd backend
.\.venv\Scripts\pip.exe install -r requirements.txt
```

## Application URLs
- **Frontend (User Interface)**: http://localhost:5173
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

## Contact
If you continue to experience issues, please check:
1. All prerequisites are installed (Python, Node.js, MySQL)
2. MySQL service is running
3. No other applications are using ports 5001 or 5173
4. All environment files are properly configured

---
*Last updated: September 2025*
