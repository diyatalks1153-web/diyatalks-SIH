#!/usr/bin/env python3
"""
MySQL Database Setup Script for AcademiaVeritas

This script sets up the MySQL database for the AcademiaVeritas project.
It creates the database, tables, and inserts sample data if needed.
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from utils.hashing import hash_password

# Load environment variables
load_dotenv()


def create_database_connection():
    """
    Create a connection to MySQL server (without specifying database)
    to create the database if it doesn't exist.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'admin'),
            password=os.getenv('DB_PASSWORD', 'admin'),
            charset='utf8mb4'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def setup_database():
    """
    Set up the MySQL database with tables and initial data.
    """
    connection = create_database_connection()
    if not connection:
        print("Failed to connect to MySQL server")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Read and execute the database schema
        schema_file = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
        with open(schema_file, 'r', encoding='utf-8') as file:
            schema_sql = file.read()
        
        # Split SQL statements and execute them
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        print("Database schema created successfully!")
        
        # Insert sample data
        insert_sample_data(cursor)
        connection.commit()
        
        print("Database setup completed successfully!")
        return True
        
    except Error as e:
        print(f"Error setting up database: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def insert_sample_data(cursor):
    """
    Insert sample data for testing.
    """
    try:
        # Hash passwords for sample data
        institution_password = hash_password('admin123')
        verifier_password = hash_password('verifier123')
        
        # Insert sample institutions
        institutions_data = [
            ('Jharkhand University', 'admin@jhu.edu', institution_password),
            ('Indian Institute of Technology', 'admin@iit.ac.in', institution_password)
        ]
        
        cursor.execute("USE academia_veritas")
        
        insert_institution_query = """
        INSERT IGNORE INTO institutions (name, email, password_hash) 
        VALUES (%s, %s, %s)
        """
        
        cursor.executemany(insert_institution_query, institutions_data)
        
        # Insert sample verifiers
        verifiers_data = [
            ('Test Verifier', 'verifier@test.com', verifier_password),
            ('HR Department', 'hr@company.com', verifier_password)
        ]
        
        insert_verifier_query = """
        INSERT IGNORE INTO verifiers (name, email, password_hash) 
        VALUES (%s, %s, %s)
        """
        
        cursor.executemany(insert_verifier_query, verifiers_data)
        
        print("Sample data inserted successfully!")
        
    except Error as e:
        print(f"Error inserting sample data: {e}")
        raise


def test_connection():
    """
    Test the database connection.
    """
    from utils.database import get_db_connection
    
    connection = get_db_connection()
    if connection:
        print("✅ Database connection successful!")
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM institutions")
            institution_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM verifiers")
            verifier_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM certificates")
            certificate_count = cursor.fetchone()[0]
            
            print(f"📊 Database Statistics:")
            print(f"   - Institutions: {institution_count}")
            print(f"   - Verifiers: {verifier_count}")
            print(f"   - Certificates: {certificate_count}")
            
        except Error as e:
            print(f"Error querying database: {e}")
        finally:
            connection.close()
        
        return True
    else:
        print("❌ Database connection failed!")
        return False


if __name__ == '__main__':
    print("🚀 Setting up AcademiaVeritas MySQL Database...")
    print("=" * 50)
    
    # Setup database
    if setup_database():
        print("\n🔍 Testing database connection...")
        test_connection()
        
        print("\n✅ Database setup completed successfully!")
        print("\n📝 Sample Login Credentials:")
        print("   Institution: admin@jhu.edu / admin123")
        print("   Verifier: verifier@test.com / verifier123")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your MySQL configuration and try again.")

#!/usr/bin/env python3
"""
Database setup script for AcademiaVeritas
This script creates the necessary tables in PostgreSQL
"""

import psycopg2
from psycopg2 import sql
import sys
from getpass import getpass

def create_tables(conn):
    """Create all necessary tables"""
    cur = conn.cursor()
    
    # Create verifiers table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS verifiers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    print("✓ Created verifiers table")
    
    # Create institutions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS institutions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    print("✓ Created institutions table")
    
    # Create certificates table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id SERIAL PRIMARY KEY,
            institution_id INTEGER NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
            student_name VARCHAR(255) NOT NULL,
            roll_number VARCHAR(100) NOT NULL,
            course_name VARCHAR(255) NOT NULL,
            grade VARCHAR(50) NOT NULL,
            issue_date DATE NOT NULL,
            certificate_hash VARCHAR(255) UNIQUE NOT NULL,
            blockchain_tx_hash VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created certificates table")
    
    # Create indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_certificates_institution_id ON certificates(institution_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_certificates_certificate_hash ON certificates(certificate_hash)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_certificates_roll_number ON certificates(roll_number)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_verifiers_email ON verifiers(email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_institutions_email ON institutions(email)")
    print("✓ Created indexes")
    
    conn.commit()
    cur.close()

def main():
    print("=== AcademiaVeritas Database Setup ===\n")
    
    # First, grant permissions using postgres user
    postgres_password = getpass("Enter PostgreSQL 'postgres' user password: ")
    
    try:
        # Connect as postgres to grant permissions
        print("\nConnecting as postgres user...")
        conn = psycopg2.connect(
            host="localhost",
            database="academia_veritas",
            user="postgres",
            password=postgres_password
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Grant schema permissions to admin
        cur.execute("GRANT CREATE ON SCHEMA public TO admin")
        cur.execute("GRANT ALL ON SCHEMA public TO admin")
        cur.execute("GRANT ALL PRIVILEGES ON DATABASE academia_veritas TO admin")
        print("✓ Granted permissions to admin user")
        
        cur.close()
        conn.close()
        
        # Now connect as admin to create tables
        print("\nConnecting as admin user...")
        conn = psycopg2.connect(
            host="localhost",
            database="academia_veritas",
            user="admin",
            password="admin"
        )
        
        # Create tables
        create_tables(conn)
        
        conn.close()
        
        print("\n✅ Database setup completed successfully!")
        print("\nYou can now run the Flask application.")
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Connection error: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL service is running")
        print("2. Database 'academia_veritas' exists")
        print("3. User 'admin' with password 'admin' exists")
        return 1
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
