#!/usr/bin/env python3
"""
AcademiaVeritas Project Startup Script

This script helps you set up and run the complete AcademiaVeritas project
with proper checks and error handling.
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    """Print project banner."""
    print("=" * 60)
    print("🚀 AcademiaVeritas - Certificate Verification System")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_mysql():
    """Check if MySQL is installed and running."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        else:
            result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MySQL - Installed")
            return True
        else:
            print("❌ MySQL - Not found")
            return False
    except FileNotFoundError:
        print("❌ MySQL - Not installed")
        print("   Please install MySQL Server 8.0 or later")
        return False

def check_node():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - OK")
            return True
        else:
            print("❌ Node.js - Not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js - Not installed")
        print("   Please install Node.js 18 or later")
        return False

def setup_backend():
    """Set up the backend environment."""
    print("\n🔧 Setting up Backend...")
    
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Change to backend directory
    os.chdir(backend_path)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("   Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        python_path = venv_path / "Scripts" / "python.exe"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        python_path = venv_path / "bin" / "python"
        pip_path = venv_path / "bin" / "pip"
    
    print("   Installing Python dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("   Creating .env file from template...")
        env_example = Path(".env.example")
        if env_example.exists():
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
        else:
            # Create basic .env file
            with open(env_file, 'w') as f:
                f.write("""# Database configuration (MySQL)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=academia_veritas
DB_USER=admin
DB_PASSWORD=admin

# Flask configuration
SECRET_KEY=academia-veritas-secret-key-2024
FRONTEND_URL=http://localhost:5173

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OAUTHLIB_INSECURE_TRANSPORT=1

# Blockchain (optional)
INFURA_API_KEY=
CONTRACT_ADDRESS=
WALLET_PRIVATE_KEY=
WALLET_ADDRESS=
""")
    
    print("✅ Backend setup completed")
    os.chdir("..")
    return True

def setup_database():
    """Set up the MySQL database."""
    print("\n🗄️  Setting up Database...")
    
    backend_path = Path("backend")
    os.chdir(backend_path)
    
    if platform.system() == "Windows":
        python_path = Path(".venv") / "Scripts" / "python.exe"
    else:
        python_path = Path(".venv") / "bin" / "python"
    
    try:
        print("   Running database setup...")
        subprocess.run([str(python_path), "setup_database.py"], check=True)
        print("✅ Database setup completed")
    except subprocess.CalledProcessError:
        print("❌ Database setup failed!")
        print("   Please make sure MySQL is running and credentials are correct")
        return False
    finally:
        os.chdir("..")
    
    return True

def setup_frontend():
    """Set up the frontend environment."""
    print("\n🎨 Setting up Frontend...")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        return False
    
    os.chdir(frontend_path)
    
    # Install npm dependencies
    print("   Installing Node.js dependencies...")
    subprocess.run(["npm", "install"], check=True)
    
    print("✅ Frontend setup completed")
    os.chdir("..")
    return True

def start_backend():
    """Start the backend server."""
    print("\n🚀 Starting Backend Server...")
    
    backend_path = Path("backend")
    os.chdir(backend_path)
    
    if platform.system() == "Windows":
        python_path = Path(".venv") / "Scripts" / "python.exe"
    else:
        python_path = Path(".venv") / "bin" / "python"
    
    print("   Backend server starting on http://localhost:5000")
    print("   Press Ctrl+C to stop")
    
    try:
        subprocess.run([str(python_path), "app.py"])
    except KeyboardInterrupt:
        print("\n   Backend server stopped")
    finally:
        os.chdir("..")

def start_frontend():
    """Start the frontend server."""
    print("\n🎨 Starting Frontend Server...")
    
    frontend_path = Path("frontend")
    os.chdir(frontend_path)
    
    print("   Frontend server starting on http://localhost:5173")
    print("   Press Ctrl+C to stop")
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        print("\n   Frontend server stopped")
    finally:
        os.chdir("..")

def main():
    """Main execution function."""
    print_banner()
    
    print("🔍 Checking Prerequisites...")
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_mysql():
        print("\n⚠️  MySQL is required for this project.")
        print("   Please install MySQL Server and try again.")
        return
    
    if not check_node():
        print("\n⚠️  Node.js is required for the frontend.")
        print("   Please install Node.js and try again.")
        return
    
    print("\n" + "=" * 60)
    print("🛠️  Setup Phase")
    print("=" * 60)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed!")
        return
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed!")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed!")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("What would you like to do?")
    print("1. Start Backend Server")
    print("2. Start Frontend Server")
    print("3. Exit")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        start_backend()
    elif choice == "2":
        start_frontend()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
