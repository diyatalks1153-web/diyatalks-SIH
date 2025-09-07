"""
Authentication routes module for AcademiaVeritas project.
This module provides secure authentication endpoints for educational institutions and verifiers.
"""

import os
import jwt
import datetime
import mysql.connector
from mysql.connector import Error
from flask import Blueprint, request, jsonify, redirect, url_for, current_app
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from utils.database import get_db_connection
from utils.hashing import hash_password, check_password

# Initialize the authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# --- Helper function to create JWT token ---
def create_jwt_token(user_id, user_type, email):
    secret_key = current_app.config['SECRET_KEY']
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

# --- Institution Authentication ---
@auth_bp.route('/institution/register', methods=['POST'])
def register_institution():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM institutions WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"error": "Email already registered"}), 409
        
        cur.execute(
            "INSERT INTO institutions (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Institution registered successfully"}), 201
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@auth_bp.route('/institution/login', methods=['POST'])
def login_institution():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM institutions WHERE email = %s", (email,))
        institution = cur.fetchone()
        cur.close()
        conn.close()

        if institution and check_password(institution[1], password):
            token = create_jwt_token(institution[0], 'institution', email)
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

# --- Verifier Authentication ---
@auth_bp.route('/verifier/register', methods=['POST'])
def register_verifier():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM verifiers WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"error": "Email already registered"}), 409
        
        cur.execute(
            "INSERT INTO verifiers (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Verifier registered successfully"}), 201
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@auth_bp.route('/verifier/login', methods=['POST'])
def login_verifier():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM verifiers WHERE email = %s", (email,))
        verifier = cur.fetchone()
        cur.close()
        conn.close()

        if verifier and check_password(verifier[1], password):
            token = create_jwt_token(verifier[0], 'verifier', email)
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


# --- Google OAuth Blueprints & Signal Handlers ---

# Institution Google OAuth Blueprint
google_bp_institution = make_google_blueprint(
    scope=["profile", "email"],
    redirect_to="handle_google_login" # A placeholder, the signal handler is what we use
)
google_bp_institution.name = "google_institution"
google_bp_institution.url_prefix = "/login/institution"

# Verifier Google OAuth Blueprint
google_bp_verifier = make_google_blueprint(
    scope=["profile", "email"],
    redirect_to="handle_google_login" # A placeholder
)
google_bp_verifier.name = "google_verifier"
google_bp_verifier.url_prefix = "/login/verifier"


@oauth_authorized.connect
def handle_google_login(blueprint, token):
    if not token:
        return jsonify({"error": "Failed to log in with Google."}), 400

    # Get user info from Google
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return jsonify({"error": "Failed to fetch user info from Google."}), 400
    
    user_info = resp.json()
    email = user_info["email"]
    name = user_info.get("name", "Google User")
    user_id = None
    
    # Determine if it's an institution or verifier
    user_type = 'institution' if blueprint.name == 'google_institution' else 'verifier'
    table_name = 'institutions' if user_type == 'institution' else 'verifiers'

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute(f"SELECT id FROM {table_name} WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if user:
            user_id = user[0]
        else:
            # Create a new user if they don't exist (MySQL doesn't support RETURNING)
            cur.execute(
                f"INSERT INTO {table_name} (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, 'google_oauth_user') # Placeholder for password
            )
            user_id = cur.lastrowid
            conn.commit()

        cur.close()
        conn.close()

        # Generate JWT and redirect to frontend
        jwt_token = create_jwt_token(user_id, user_type, email)
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000') # Use port from vite.config.js
        redirect_url = f"{frontend_url}/google-auth-callback?token={jwt_token}"
        
        return redirect(redirect_url)

    except Error as e:
        return jsonify({"error": f"Database error during Google login: {e}"}), 500

@oauth_error.connect
def google_error(blueprint, error, error_description=None, error_uri=None):
    # Log the error for debugging
    current_app.logger.error(f"OAuth error from {blueprint.name}: {error} description: {error_description}")
    # Redirect to a frontend error page or the login page with an error message
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    return redirect(f"{frontend_url}/portal?error=google_login_failed")

