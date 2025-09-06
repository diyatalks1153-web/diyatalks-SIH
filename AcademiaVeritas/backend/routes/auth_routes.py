
"""
Authentication routes module for AcademiaVeritas project.

This module provides secure authentication endpoints for educational institutions and verifiers,
including registration and login functionality with JWT token management.
"""

import os
import jwt
import datetime
import psycopg2
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from utils.database import get_db_connection
from utils.hashing import hash_password, check_password
from flask_dance.consumer import OAuth2ConsumerBlueprint

# Load SECRET_KEY from environment variables for JWT signing
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the authentication blueprint
auth_bp = Blueprint('auth', __name__)

# Google OAuth setup
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Institution Google OAuth blueprint
google_bp_institution = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=["profile", "email"],
    redirect_url="/api/institution/google/callback",
    reprompt_consent=True,
    redirect_to=None
)

from flask_dance.consumer import OAuth2ConsumerBlueprint
# Verifier Google OAuth blueprint
google_bp_verifier = OAuth2ConsumerBlueprint(
    "google_verifier",
    __name__,
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=["profile", "email"],
    base_url="https://www.googleapis.com/oauth2/v2/",
    authorization_url="https://accounts.google.com/o/oauth2/auth",
    token_url="https://accounts.google.com/o/oauth2/token",
    redirect_url="/api/verifier/google/callback"
)



# --- Institution Registration ---
@auth_bp.route('/api/institution/register', methods=['POST'])
def register_institution():
    """
    Register a new educational institution.
    
    This endpoint allows educational institutions to create new accounts in the system.
    It validates input data, checks for duplicate emails, securely hashes passwords,
    and stores the institution data in the database.
    
    Expected JSON Input:
        {
            "name": "University of Technology",
            "email": "admin@university.edu",
            "password": "secure_password"
        }
    
    Returns:
        JSON response with success message and 201 status code on success,
        or error message with appropriate status code on failure.
    """
    try:
        # Extract and validate input data from JSON request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Validate that all required fields are present
        if not name or not email or not password:
            return jsonify({
                "error": "Missing required fields. Please provide name, email, and password."
            }), 400
        
        # Validate email format (basic validation)
        if '@' not in email or '.' not in email:
            return jsonify({
                "error": "Invalid email format"
            }), 400
        
        # Validate password strength (minimum 6 characters)
        if len(password) < 6:
            return jsonify({
                "error": "Password must be at least 6 characters long"
            }), 400
        
        # Get database connection
        connection = get_db_connection()
        if not connection:
            return jsonify({
                "error": "Database connection failed"
            }), 500
        
        try:
            cursor = connection.cursor()
            
            # Check if institution with this email already exists
            cursor.execute(
                "SELECT id FROM institutions WHERE email = %s",
                (email,)
            )
            
            if cursor.fetchone():
                return jsonify({
                    "error": "Email already registered"
                }), 409
            
            # Hash the password securely
            password_hash = hash_password(password)
            
            # Insert new institution into database
            cursor.execute(
                "INSERT INTO institutions (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, password_hash)
            )
            
            # Commit the transaction
            connection.commit()
            
            return jsonify({
                "message": "Institution registered successfully"
            }), 201
            
        except psycopg2.Error as e:
            # Rollback transaction on database error
            connection.rollback()
            print(f"Database error during registration: {e}")
            return jsonify({
                "error": "Database error occurred during registration"
            }), 500
            
        finally:
            # Always close the database connection
            if connection:
                connection.close()
                
    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500


# --- Institution Login ---
@auth_bp.route('/api/institution/login', methods=['POST'])
def login_institution():
    """
    Authenticate an educational institution and return a JWT token.
    
    This endpoint validates institution credentials and returns a JWT token
    for authenticated sessions. The token contains the institution ID and
    has a 24-hour expiration time.
    
    Expected JSON Input:
        {
            "email": "admin@university.edu",
            "password": "secure_password"
        }
    
    Returns:
        JSON response with JWT token and 200 status code on success,
        or error message with appropriate status code on failure.
    """
    try:
        # Extract and validate input data from JSON request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Validate that both email and password are provided
        if not email or not password:
            return jsonify({
                "error": "Missing required fields. Please provide email and password."
            }), 400
        
        # Validate SECRET_KEY is available for JWT signing
        if not SECRET_KEY:
            print("Error: SECRET_KEY environment variable is not set")
            return jsonify({
                "error": "Server configuration error"
            }), 500
        
        # Get database connection
        connection = get_db_connection()
        if not connection:
            return jsonify({
                "error": "Database connection failed"
            }), 500
        
        try:
            cursor = connection.cursor()
            
            # Fetch institution data by email
            cursor.execute(
                "SELECT id, password_hash FROM institutions WHERE email = %s",
                (email,)
            )
            
            institution_data = cursor.fetchone()
            
            # Check if institution exists
            if not institution_data:
                return jsonify({
                    "error": "Invalid credentials"
                }), 401
            
            institution_id, stored_password_hash = institution_data
            
            # Verify the provided password against the stored hash
            if not check_password(stored_password_hash, password):
                return jsonify({
                    "error": "Invalid credentials"
                }), 401
            
            # Create JWT payload with institution ID, user type, and expiration time
            payload = {
                'user_id': institution_id,
                'user_type': 'institution',
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                'iat': datetime.datetime.utcnow()
            }
            
            # Generate JWT token
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                "token": token,
                "message": "Login successful",
                "institution_id": institution_id
            }), 200
            
        except psycopg2.Error as e:
            print(f"Database error during login: {e}")
            return jsonify({
                "error": "Database error occurred during login"
            }), 500
            
        finally:
            # Always close the database connection
            if connection:
                connection.close()
                
    except jwt.InvalidTokenError as e:
        print(f"JWT error during login: {e}")
        return jsonify({
            "error": "Token generation failed"
        }), 500
        
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500


# --- Verifier Registration ---
@auth_bp.route('/api/verifier/register', methods=['POST'])
def register_verifier():
    """
    Register a new verifier.
    This endpoint allows verifiers to create new accounts in the system.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name or not email or not password:
            return jsonify({"error": "Missing required fields. Please provide name, email, and password."}), 400
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM verifiers WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already registered"}), 409
            password_hash = hash_password(password)
            cursor.execute("INSERT INTO verifiers (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password_hash))
            connection.commit()
            return jsonify({"message": "Verifier registered successfully"}), 201
        except psycopg2.Error as e:
            connection.rollback()
            print(f"Database error during verifier registration: {e}")
            return jsonify({"error": "Database error occurred during registration"}), 500
        finally:
            if connection:
                connection.close()
    except Exception as e:
        print(f"Unexpected error during verifier registration: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# --- Verifier Login ---
@auth_bp.route('/api/verifier/login', methods=['POST'])
def login_verifier():
    """
    Authenticate a verifier and return a JWT token.
    This endpoint validates verifier credentials and returns a JWT token for authenticated sessions.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Missing required fields. Please provide email and password."}), 400
        if not SECRET_KEY:
            print("Error: SECRET_KEY environment variable is not set")
            return jsonify({"error": "Server configuration error"}), 500
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, password_hash FROM verifiers WHERE email = %s", (email,))
            verifier_data = cursor.fetchone()
            if not verifier_data:
                return jsonify({"error": "Invalid credentials"}), 401
            verifier_id, stored_password_hash = verifier_data
            if not check_password(stored_password_hash, password):
                return jsonify({"error": "Invalid credentials"}), 401
            payload = {
                'user_id': verifier_id,
                'user_type': 'verifier',
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({
                "token": token,
                "message": "Login successful",
                "verifier_id": verifier_id
            }), 200
        except psycopg2.Error as e:
            print(f"Database error during verifier login: {e}")
            return jsonify({"error": "Database error occurred during login"}), 500
        finally:
            if connection:
                connection.close()
    except jwt.InvalidTokenError as e:
        print(f"JWT error during verifier login: {e}")
        return jsonify({"error": "Token generation failed"}), 500
    except Exception as e:
        print(f"Unexpected error during verifier login: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# --- Google OAuth Routes ---
@auth_bp.route('/api/institution/google')
def google_login_institution():
    return redirect(url_for('google.login'))

@auth_bp.route('/api/institution/google/callback')
def google_callback_institution():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    email = user_info["email"]
    name = user_info.get("name", "Google User")
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM institutions WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            institution_id = row[0]
        else:
            cursor.execute("INSERT INTO institutions (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id", (name, email, ''),)
            institution_id = cursor.fetchone()[0]
            connection.commit()
        payload = {
            'user_id': institution_id,
            'user_type': 'institution',
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        redirect_url = f"{frontend_url}/google-auth-callback?token={token}"
        return redirect(redirect_url)
    except Exception as e:
        print(f"Error in Google institution callback: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if connection:
            connection.close()

@auth_bp.route('/api/verifier/google')
def google_login_verifier():
    return redirect(url_for('google_verifier.login'))

@auth_bp.route('/api/verifier/google/callback')
def google_callback_verifier():
    if not google_bp_verifier.session.authorized:
        return redirect(url_for('google_verifier.login'))
    resp = google_bp_verifier.session.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    email = user_info["email"]
    name = user_info.get("name", "Google User")
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM verifiers WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            verifier_id = row[0]
        else:
            cursor.execute("INSERT INTO verifiers (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id", (name, email, ''),)
            verifier_id = cursor.fetchone()[0]
            connection.commit()
        payload = {
            'user_id': verifier_id,
            'user_type': 'verifier',
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        redirect_url = f"{frontend_url}/google-auth-callback?token={token}"
        return redirect(redirect_url)
    except Exception as e:
        print(f"Error in Google verifier callback: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if connection:
            connection.close()


# --- Token Verification ---
@auth_bp.route('/api/verify-token', methods=['POST'])
def verify_token():
    """
    Verify the validity of a JWT token.
    
    This endpoint can be used to verify if a JWT token is valid and not expired.
    It's useful for frontend applications to check token status.
    
    Expected JSON Input:
        {
            "token": "jwt_token_here"
        }
    
    Returns:
        JSON response with token validity status and user information.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        token = data.get('token')
        
        if not token:
            return jsonify({"error": "No token provided"}), 400
        
        if not SECRET_KEY:
            return jsonify({"error": "Server configuration error"}), 500
        
        try:
            # Decode and verify the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            return jsonify({
                "valid": True,
                "user_id": payload.get('user_id'),
                "user_type": payload.get('user_type'),
                "email": payload.get('email'),
                "expires_at": payload.get('exp')
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                "valid": False,
                "error": "Token has expired"
            }), 401
            
        except jwt.InvalidTokenError:
            return jsonify({
                "valid": False,
                "error": "Invalid token"
            }), 401
            
    except Exception as e:
        print(f"Unexpected error during token verification: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500
