#!/usr/bin/env python3
"""
Simple script to start the AcademiaVeritas backend server
"""
import os
from app import create_app

def main():
    print("Starting AcademiaVeritas Backend Server...")
    print("=" * 50)
    
    # Set port
    os.environ['PORT'] = '5001'
    
    # Create app
    app = create_app()
    
    print(f"Server starting on http://localhost:5001")
    print("Available endpoints:")
    print("  GET  /health                     - Health check")
    print("  POST /api/institution/register   - Institution registration")
    print("  POST /api/institution/login      - Institution login")
    print("  POST /api/verifier/register      - Verifier registration") 
    print("  POST /api/verifier/login         - Verifier login")
    print("\nTest credentials:")
    print("  Institution: test@institution.com / testpass123")
    print("  Verifier: test@verifier.com / testpass123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start server
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )

if __name__ == "__main__":
    main()
