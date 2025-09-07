#!/usr/bin/env python3
"""
Script to create test users with proper password hashes
"""
from utils.database import get_db_connection
from utils.hashing import hash_password

def create_test_users():
    print("Creating test users...")
    
    # Get database connection
    conn = get_db_connection()
    if not conn:
        print("✗ Failed to connect to database")
        return False
    
    try:
        cur = conn.cursor()
        
        # Hash the password
        password_hash = hash_password('testpass123')
        print(f"Generated password hash: {password_hash}")
        
        # Create institution user
        print("\nCreating institution user...")
        cur.execute(
            "INSERT INTO institutions (name, email, password_hash) VALUES (%s, %s, %s)",
            ('Test Institution', 'test@institution.com', password_hash)
        )
        print("✓ Institution user created")
        
        # Create verifier user  
        print("Creating verifier user...")
        cur.execute(
            "INSERT INTO verifiers (name, email, password_hash) VALUES (%s, %s, %s)",
            ('Test Verifier', 'test@verifier.com', password_hash)
        )
        print("✓ Verifier user created")
        
        # Commit the changes
        conn.commit()
        print("✓ Changes committed to database")
        
        # Verify the users were created
        cur.execute("SELECT id, name, email FROM institutions WHERE email = %s", ('test@institution.com',))
        institution = cur.fetchone()
        print(f"Institution created: ID={institution[0]}, Name={institution[1]}, Email={institution[2]}")
        
        cur.execute("SELECT id, name, email FROM verifiers WHERE email = %s", ('test@verifier.com',))
        verifier = cur.fetchone()
        print(f"Verifier created: ID={verifier[0]}, Name={verifier[1]}, Email={verifier[2]}")
        
        cur.close()
        conn.close()
        
        print("\n🎉 Test users created successfully!")
        print("Credentials:")
        print("  Institution: test@institution.com / testpass123")
        print("  Verifier: test@verifier.com / testpass123")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating test users: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    create_test_users()
