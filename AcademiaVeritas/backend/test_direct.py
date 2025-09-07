#!/usr/bin/env python3
"""
Direct test of login functionality without running server
"""
import os
import sys
from app import create_app
from utils.database import get_db_connection
from utils.hashing import check_password

def test_direct_login():
    print("=== Direct Login Test ===\n")
    
    # Test database connection
    print("1. Testing database connection...")
    conn = get_db_connection()
    if not conn:
        print("✗ Database connection failed")
        return False
    else:
        print("✓ Database connection successful")
        
    # Test institution user exists
    print("\n2. Testing institution user exists...")
    cur = conn.cursor()
    cur.execute("SELECT id, email, password_hash FROM institutions WHERE email = %s", ('test@institution.com',))
    institution = cur.fetchone()
    
    if institution:
        print(f"✓ Institution user found: {institution[1]}")
        
        # Test password verification
        print("3. Testing password verification...")
        if check_password(institution[2], 'testpass123'):
            print("✓ Institution password verification successful")
        else:
            print("✗ Institution password verification failed")
    else:
        print("✗ Institution user not found")
    
    # Test verifier user exists
    print("\n4. Testing verifier user exists...")
    cur.execute("SELECT id, email, password_hash FROM verifiers WHERE email = %s", ('test@verifier.com',))
    verifier = cur.fetchone()
    
    if verifier:
        print(f"✓ Verifier user found: {verifier[1]}")
        
        # Test password verification
        print("5. Testing password verification...")
        if check_password(verifier[2], 'testpass123'):
            print("✓ Verifier password verification successful")
        else:
            print("✗ Verifier password verification failed")
    else:
        print("✗ Verifier user not found")
    
    cur.close()
    conn.close()
    
    # Test Flask app creation
    print("\n6. Testing Flask app creation...")
    try:
        app = create_app()
        print("✓ Flask app created successfully")
        
        # Test with app context
        with app.test_client() as client:
            # Test health endpoint
            print("\n7. Testing health endpoint...")
            response = client.get('/health')
            if response.status_code == 200:
                print("✓ Health endpoint working")
            else:
                print(f"✗ Health endpoint failed: {response.status_code}")
            
            # Test institution login
            print("\n8. Testing institution login endpoint...")
            login_data = {
                'email': 'test@institution.com',
                'password': 'testpass123'
            }
            response = client.post('/api/institution/login', 
                                 json=login_data,
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = response.get_json()
                if 'token' in data:
                    print("✓ Institution login successful")
                    print(f"  Token: {data['token'][:50]}...")
                else:
                    print("✗ Institution login: No token received")
            else:
                print(f"✗ Institution login failed: {response.status_code}")
                print(f"  Response: {response.get_data(as_text=True)}")
            
            # Test verifier login
            print("\n9. Testing verifier login endpoint...")
            login_data = {
                'email': 'test@verifier.com',
                'password': 'testpass123'
            }
            response = client.post('/api/verifier/login', 
                                 json=login_data,
                                 content_type='application/json')
            
            if response.status_code == 200:
                data = response.get_json()
                if 'token' in data:
                    print("✓ Verifier login successful")
                    print(f"  Token: {data['token'][:50]}...")
                else:
                    print("✗ Verifier login: No token received")
            else:
                print(f"✗ Verifier login failed: {response.status_code}")
                print(f"  Response: {response.get_data(as_text=True)}")
        
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False
    
    print("\n=== Test Complete ===")
    return True

if __name__ == "__main__":
    test_direct_login()
