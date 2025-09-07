# 🚀 AcademiaVeritas - Quick Start Guide

## 🎯 What is AcademiaVeritas?

AcademiaVeritas is a comprehensive **certificate verification system** that combines:
- 🔒 **Blockchain Technology** for tamper-proof verification
- 🤖 **AI-powered OCR** for certificate scanning
- 🌐 **Modern Web Interface** for easy access
- 🔐 **Secure Authentication** for institutions and verifiers

---

## ⚡ Super Quick Start (Recommended)

1. **Open Terminal/Command Prompt** in the project directory
2. **Run the automated setup**:
   ```bash
   python start_project.py
   ```
3. **Follow the prompts** - the script will handle everything!

---

## 🛠️ What You Need

Before starting, make sure you have:

- ✅ **Python 3.8+** (you already have 3.13.7 - perfect!)
- ✅ **Node.js 18+** (you already have v22.19.0 - excellent!)
- ⚠️ **MySQL Server 8.0+** (needs to be installed)

### Installing MySQL (if needed):

**Windows:**
```bash
# Download from: https://dev.mysql.com/downloads/mysql/
# Or use Chocolatey:
choco install mysql
```

**macOS:**
```bash
brew install mysql
```

**Linux:**
```bash
sudo apt update
sudo apt install mysql-server
```

---

## 📁 Project Structure

```
AcademiaVeritas/
├── backend/          # Python Flask API
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   ├── utils/        # Helper functions
│   └── app.py        # Main application
├── frontend/         # React web application
│   └── src/          # React components
├── blockchain/       # Smart contracts
├── start_project.py  # 🌟 Magic setup script
└── QUICK_START.md    # This file
```

---

## 🚀 Getting Started

### Option 1: Automated Setup (Easiest!)

```bash
python start_project.py
```

This will:
1. ✅ Check all prerequisites
2. ✅ Set up the backend environment
3. ✅ Configure MySQL database
4. ✅ Install frontend dependencies
5. ✅ Give you options to start servers

### Option 2: Manual Setup

#### Step 1: Backend Setup
```bash
cd backend
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Database Setup
```bash
# Still in backend directory
python setup_database.py
```

#### Step 3: Start Backend
```bash
python app.py
```
**Backend runs on**: http://localhost:5000

#### Step 4: Frontend Setup (new terminal)
```bash
cd frontend
npm install
npm run dev
```
**Frontend runs on**: http://localhost:5173

---

## 🎮 How to Use

### 1. Institution Portal
- **Register/Login** as an educational institution
- **Add certificates** for your students
- **Manage** your certificate database

### 2. Verification Portal  
- **Register/Login** as a verifier (employer, etc.)
- **Upload certificate images** for verification
- **Get instant results** with blockchain proof

### 3. Key Features
- 🔍 **OCR-powered scanning** - Upload any certificate image
- ⛓️ **Blockchain verification** - Tamper-proof validation
- 🏛️ **Institution management** - Secure certificate issuance
- 📱 **Modern UI** - Beautiful, responsive design

---

## 🔑 Test Credentials

After setup, you can test with these sample accounts:

### Institution Login
- **Email**: `admin@jhu.edu`
- **Password**: `admin123`

### Verifier Login
- **Email**: `verifier@test.com` 
- **Password**: `verifier123`

---

## 🌐 Access Points

Once running:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

---

## 🐳 Docker Alternative

If you prefer Docker:

```bash
# Production
docker-compose up --build -d

# Development
docker-compose -f docker-compose.dev.yml up --build -d
```

**Docker Access:**
- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:5001
- **MySQL**: localhost:3306

---

## ❓ Common Issues & Solutions

### "MySQL connection failed"
```bash
# Start MySQL service
# Windows:
net start mysql
# macOS:
brew services start mysql
# Linux:
sudo systemctl start mysql
```

### "Port already in use"
- Close other applications using ports 5000/5173
- Or modify ports in configuration files

### "Module not found"
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

---

## 🎯 Testing the System

### 1. Full Workflow Test
1. **Start both servers** (backend + frontend)
2. **Open** http://localhost:5173
3. **Register** as an institution
4. **Add a sample certificate**
5. **Register** as a verifier
6. **Try verification** (upload any certificate image)

### 2. API Testing
```bash
# Health check
curl http://localhost:5000/health

# Database test
cd backend
python -c "from utils.database import test_db_connection; test_db_connection()"
```

---

## 📚 Additional Resources

- 📖 **Full Documentation**: `RUN_PROJECT.md`
- 🔄 **Migration Guide**: `MYSQL_MIGRATION.md`
- 🐳 **Docker Guide**: `DOCKER_SETUP.md`
- ⛓️ **Blockchain Integration**: `backend/BLOCKCHAIN_INTEGRATION.md`

---

## 🎉 Success Indicators

You'll know everything is working when you see:

✅ **Backend**: `Running on http://localhost:5000`  
✅ **Frontend**: `Local: http://localhost:5173`  
✅ **Database**: `MySQL connection successful!`  
✅ **Health Check**: `{"status": "healthy"}`

---

## 🆘 Need Help?

1. **Run the automated setup**: `python start_project.py`
2. **Check prerequisites**: Python, Node.js, MySQL installed?
3. **Verify database**: Run `python setup_database.py`
4. **Check ports**: Make sure 5000 and 5173 are free
5. **Look at logs**: Read error messages carefully

---

## 🌟 What Makes This Special?

- 🔒 **Blockchain Security** - Certificates can't be forged
- 🤖 **AI-Powered OCR** - Scan any certificate format
- 🏛️ **Institution Focus** - Built for educational institutions
- 🌐 **Modern Tech Stack** - React + Flask + MySQL + Web3
- 📱 **Responsive Design** - Works on all devices

---

**Ready to get started?** Run `python start_project.py` and see the magic happen! ✨
