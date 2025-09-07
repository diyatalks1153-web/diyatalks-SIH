#!/usr/bin/env python3
"""
Test script to verify login functionality for AcademiaVeritas
"""
import requests
import json
import sys
from utils.database import test_db_connection

def test_database():
    print("Testing database connection...")
    result = test_db_connection()
    print(f"Database connection: {'✓ SUCCESS' if result else '✗ FAILED'}")
    return result

def test_backend_health():
    print("\nTesting backend health endpoint...")
    try:
        response = requests.get('http://localhost:5001/health', timeout=5)
        if response.status_code == 200:
            print("✓ Backend health check passed")
            return True
        else:
            print(f"✗ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running or not accessible")
        return False
    except Exception as e:
        print(f"✗ Backend health check error: {e}")
        return False

def test_institution_login():
    print("\nTesting institution login...")
    try:
        login_data = {
            'email': 'test@institution.com',
            'password': 'testpass123'
        }
        
        response = requests.post(
            'http://localhost:5001/api/institution/login',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("✓ Institution login successful")
                print(f"  Token received: {data['token'][:50]}...")
                return True
            else:
                print("✗ Institution login failed: No token in response")
                return False
        else:
            print(f"✗ Institution login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Institution login error: {e}")
        return False

def test_verifier_login():
    print("\nTesting verifier login...")
    try:
        login_data = {
            'email': 'test@verifier.com',
            'password': 'testpass123'
        }
        
        response = requests.post(
            'http://localhost:5001/api/verifier/login',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("✓ Verifier login successful")
                print(f"  Token received: {data['token'][:50]}...")
                return True
            else:
                print("✗ Verifier login failed: No token in response")
                return False
        else:
            print(f"✗ Verifier login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Verifier login error: {e}")
        return False

def main():
    print("=== AcademiaVeritas Login Test ===\n")
    
    # Test database connection
    db_ok = test_database()
    if not db_ok:
        print("\n❌ Database connection failed. Cannot proceed with tests.")
        sys.exit(1)
    
    # Test backend health
    backend_ok = test_backend_health()
    if not backend_ok:
        print("\n❌ Backend server is not running. Please start it first:")
        print("   python app.py")
        sys.exit(1)
    
    # Test login endpoints
    institution_ok = test_institution_login()
    verifier_ok = test_verifier_login()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Database Connection: {'✓' if db_ok else '✗'}")
    print(f"Backend Health: {'✓' if backend_ok else '✗'}")
    print(f"Institution Login: {'✓' if institution_ok else '✗'}")
    print(f"Verifier Login: {'✓' if verifier_ok else '✗'}")
    
    if institution_ok and verifier_ok:
        print("\n🎉 All login tests passed! Your login system is working correctly.")
        print("\nTest credentials:")
        print("  Institution: test@institution.com / testpass123")
        print("  Verifier: test@verifier.com / testpass123")
    else:
        print("\n❌ Some tests failed. Please check the backend logs for more details.")

if __name__ == "__main__":
    main()
