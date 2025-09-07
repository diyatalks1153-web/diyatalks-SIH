"""
Database connection module for AcademiaVeritas project.

This module provides database connectivity functionality for the Flask backend,
handling MySQL connections with proper error handling and environment configuration.
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    """
    Establishes a connection to the MySQL database using environment variables.
    
    This function reads database configuration from environment variables and attempts
    to establish a connection to the MySQL database. It includes comprehensive
    error handling to gracefully manage connection failures.
    
    Returns:
        mysql.connector.connection: Database connection object on success
        None: Returns None if connection fails
        
    Raises:
        No exceptions are raised - all errors are caught and handled gracefully
    """
    try:
        # Read database configuration from environment variables
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306')
        db_name = os.getenv('DB_NAME', 'academia_veritas')
        db_user = os.getenv('DB_USER', 'admin')
        db_password = os.getenv('DB_PASSWORD', 'admin')
        
        # Validate that required environment variables are set
        if not all([db_host, db_port, db_name, db_user, db_password]):
            print("Error: Required database environment variables are not set")
            print("Please set: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
            return None
        
        # Establish connection to MySQL database
        connection = mysql.connector.connect(
            host=db_host,
            port=int(db_port),
            database=db_name,
            user=db_user,
            password=db_password,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            autocommit=False
        )
        
        # Print success message for debugging (remove in production)
        print(f"Successfully connected to MySQL database: {db_name}")
        
        return connection
        
    except Error as e:
        # Handle MySQL connection errors (invalid credentials, server down, etc.)
        print(f"MySQL connection error: {e}")
        print("Please check your database configuration and ensure MySQL is running")
        return None
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error occurred while connecting to database: {e}")
        return None


def close_db_connection(connection):
    """
    Safely closes a database connection.
    
    Args:
        connection: psycopg2 connection object to close
    """
    if connection:
        try:
            connection.close()
            print("Database connection closed successfully")
        except Exception as e:
            print(f"Error closing database connection: {e}")


def test_db_connection():
    """
    Test function to verify database connectivity.
    
    This function can be used during development to test if the database
    connection is working properly.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    connection = get_db_connection()
    if connection:
        close_db_connection(connection)
        return True
    return False
