# 🔄 MySQL Migration Guide - AcademiaVeritas

This document outlines the complete migration from PostgreSQL to MySQL for the AcademiaVeritas project.

## ✅ Migration Status: COMPLETED

All components have been successfully migrated from PostgreSQL to MySQL 8.0.

---

## 🗄️ Database Changes

### Configuration Updates

**Before (PostgreSQL):**
```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/academia_veritas
```

**After (MySQL):**
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=academia_veritas
DB_USER=admin
DB_PASSWORD=admin
```

### Schema Conversion

- ✅ **Auto-increment**: `SERIAL` → `INT AUTO_INCREMENT`
- ✅ **Foreign Keys**: Updated to MySQL syntax
- ✅ **Character Set**: Added `utf8mb4` support
- ✅ **Indexes**: Optimized for MySQL performance
- ✅ **Data Types**: All PostgreSQL types converted to MySQL equivalents

---

## 🔧 Technical Changes Made

### 1. Backend Dependencies
```diff
- psycopg2-binary>=2.9
+ mysql-connector-python>=8.0
```

### 2. Database Connection (`utils/database.py`)
- ✅ Replaced `psycopg2` with `mysql.connector`
- ✅ Updated connection parameters
- ✅ Added proper error handling for MySQL
- ✅ Enhanced UTF-8 support

### 3. Route Updates (`routes/`)
- ✅ Updated all `psycopg2.Error` → `mysql.connector.Error`
- ✅ Fixed `RETURNING` clause compatibility (MySQL uses `lastrowid`)
- ✅ Updated query syntax for MySQL

### 4. Configuration (`config.py`)
- ✅ Added separate MySQL connection parameters
- ✅ Updated environment variable handling

### 5. Docker Configuration
- ✅ `docker-compose.yml`: PostgreSQL → MySQL 8.0
- ✅ `docker-compose.dev.yml`: Development environment updated
- ✅ Health checks updated for MySQL

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
python start_project.py
```

### Option 2: Manual Setup

#### 1. Install MySQL
```bash
# Windows (using Chocolatey)
choco install mysql

# macOS (using Homebrew)
brew install mysql

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
```

#### 2. Configure MySQL
```sql
-- Create database and user
CREATE DATABASE academia_veritas;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON academia_veritas.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. Setup Backend
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python setup_database.py
```

#### 4. Start Backend
```bash
python app.py
```

#### 5. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🛠️ Environment Configuration

Create/update your `.env` file in the backend directory:

```env
# Database configuration (MySQL)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=academia_veritas
DB_USER=admin
DB_PASSWORD=admin

# Flask configuration
SECRET_KEY=your-secret-key-change-in-production

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost:5173
OAUTHLIB_INSECURE_TRANSPORT=1

# Blockchain configuration (optional)
INFURA_API_KEY=your-infura-api-key
CONTRACT_ADDRESS=your-contract-address
WALLET_PRIVATE_KEY=your-wallet-private-key
WALLET_ADDRESS=your-wallet-address
```

---

## 🐳 Docker Setup

### Production
```bash
docker-compose up --build -d
```

### Development
```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

**Access Points:**
- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:5001
- **MySQL**: localhost:3306

---

## 📊 Database Schema

The MySQL schema includes:

### Tables
- ✅ **institutions** - Educational institution accounts
- ✅ **verifiers** - Certificate verification accounts  
- ✅ **certificates** - Certificate records with blockchain hashes

### Features
- ✅ **Foreign Key Constraints** - Data integrity
- ✅ **Indexes** - Optimized queries
- ✅ **UTF-8 Support** - International character support
- ✅ **Auto-increment IDs** - Unique record identifiers
- ✅ **Timestamps** - Created/updated tracking

---

## 🔍 Verification & Testing

### Database Connection Test
```bash
cd backend
python -c "from utils.database import test_db_connection; test_db_connection()"
```

### API Health Check
```bash
curl http://localhost:5000/health
```

### Full Setup Verification
```bash
python setup_database.py
```

**Expected Output:**
```
🚀 Setting up AcademiaVeritas MySQL Database...
==================================================
✅ Database connection successful!
📊 Database Statistics:
   - Institutions: 2
   - Verifiers: 2
   - Certificates: 0
```

---

## 🎯 Sample Credentials

After running the database setup, you can use these test accounts:

### Institution Login
- **Email**: `admin@jhu.edu`
- **Password**: `admin123`

### Verifier Login  
- **Email**: `verifier@test.com`
- **Password**: `verifier123`

---

## ❓ Troubleshooting

### Common Issues

#### 1. "MySQL connection failed"
```bash
# Check if MySQL service is running
# Windows
net start mysql

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

#### 2. "Access denied for user 'admin'"
```sql
-- Reset user permissions
DROP USER IF EXISTS 'admin'@'localhost';
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON academia_veritas.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. "Database does not exist"
```bash
cd backend
python setup_database.py
```

#### 4. Port conflicts
Update `.env` file with different ports:
```env
DB_PORT=3307  # If 3306 is occupied
```

---

## 🔧 Manual Database Setup

If the automated script fails, you can set up manually:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE IF NOT EXISTS academia_veritas 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON academia_veritas.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

-- Use database
USE academia_veritas;

-- Run the schema file
SOURCE /path/to/backend/database_schema.sql;
```

---

## 📈 Performance Optimizations

The MySQL migration includes several performance improvements:

- ✅ **Optimized Indexes** - Faster queries
- ✅ **Connection Pooling** - Better resource management  
- ✅ **UTF-8mb4 Charset** - Full Unicode support
- ✅ **InnoDB Engine** - ACID compliance and performance
- ✅ **Query Optimization** - MySQL-specific query patterns

---

## 🎉 Migration Complete!

Your AcademiaVeritas project is now running on MySQL 8.0 with:

- ✅ **Full Feature Parity** - All original functionality preserved
- ✅ **Improved Performance** - MySQL optimizations
- ✅ **Better Compatibility** - Wider deployment options
- ✅ **Enhanced Security** - Updated authentication methods
- ✅ **Docker Ready** - Complete containerization support

**Next Steps:**
1. Run `python start_project.py` to get started
2. Test all functionality with the sample credentials
3. Configure blockchain integration (optional)
4. Deploy to your preferred hosting platform

---

## 📞 Need Help?

If you encounter any issues:

1. **Check Prerequisites**: Python 3.8+, MySQL 8.0+, Node.js 18+
2. **Verify Environment**: Ensure `.env` file is properly configured
3. **Test Database**: Run `python setup_database.py`
4. **Check Logs**: Look for error messages in terminal output
5. **Manual Setup**: Follow the step-by-step manual setup guide above

The migration is complete and the project is ready to run! 🚀
