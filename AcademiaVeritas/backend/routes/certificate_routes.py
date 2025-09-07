"""
Certificate management routes module for AcademiaVeritas project.

This module provides secure certificate management endpoints for educational institutions
and public certificate verification functionality with file upload support.
"""

import os
import jwt
import functools
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.database import get_db_connection
from utils.hashing import generate_certificate_hash

# Load SECRET_KEY from environment variables for JWT signing
SECRET_KEY = os.getenv('SECRET_KEY')

# Define allowed file extensions for certificate uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Initialize the certificate management blueprint
cert_bp = Blueprint('certificate', __name__)


def token_required(allowed_user_types=None):
    """
    Custom JWT decorator for route protection with role-based access control.
    
    This decorator validates JWT tokens from the Authorization header and checks
    if the user type is in the allowed list. It ensures that only authenticated
    users with appropriate roles can access protected endpoints.
    
    Args:
        allowed_user_types (list): List of allowed user types (e.g., ['institution', 'verifier'])
        
    Returns:
        Decorated function that validates JWT tokens and user roles before execution
        
    Raises:
        401 Unauthorized: If token is missing, invalid, or expired
        403 Forbidden: If user type is not in allowed list
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            # Check for Authorization header
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return jsonify({
                    "error": "Authorization header is missing"
                }), 401
            
            # Validate Bearer token format
            try:
                auth_type, token = auth_header.split(' ', 1)
                if auth_type.lower() != 'bearer':
                    return jsonify({
                        "error": "Invalid authorization type. Use 'Bearer <token>'"
                    }), 401
            except ValueError:
                return jsonify({
                    "error": "Invalid authorization header format. Use 'Bearer <token>'"
                }), 401
            
            # Validate SECRET_KEY availability
            if not SECRET_KEY:
                print("Error: SECRET_KEY environment variable is not set")
                return jsonify({
                    "error": "Server configuration error"
                }), 500
            
            try:
                # Decode and validate the JWT token
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                user_type = payload.get('user_type')
                
                if not user_id or not user_type:
                    return jsonify({
                        "error": "Invalid token payload"
                    }), 401
                
                # Check if user type is allowed
                if allowed_user_types and user_type not in allowed_user_types:
                    return jsonify({
                        "error": f"Access denied. Required user types: {', '.join(allowed_user_types)}"
                    }), 403
                
                # Pass the user_id and user_type to the decorated function
                return f(user_id, user_type, *args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                return jsonify({
                    "error": "Token has expired"
                }), 401
                
            except jwt.InvalidTokenError:
                return jsonify({
                    "error": "Invalid token"
                }), 401
                
            except Exception as e:
                print(f"Unexpected error during token validation: {e}")
                return jsonify({
                    "error": "Token validation failed"
                }), 401
        
        return decorated
    return decorator


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): The name of the uploaded file
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@cert_bp.route('/api/certificate/add', methods=['POST'])
@token_required(allowed_user_types=['institution'])
def add_certificate(user_id, user_type):
    """
    Add a new certificate record to the database.
    
    This endpoint allows authenticated institutions to add new certificate records
    to the system. It validates input data, generates integrity hashes, and stores
    the certificate information in the database.
    
    Expected JSON Input:
        {
            "student_name": "Jane Doe",
            "roll_number": "R-98765",
            "course_name": "Bachelor of Information Technology",
            "grade": "First Class",
            "issue_date": "2025-10-15"
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
        
        student_name = data.get('student_name')
        roll_number = data.get('roll_number')
        course_name = data.get('course_name')
        grade = data.get('grade')
        issue_date = data.get('issue_date')
        
        # Validate that all required fields are present
        if not all([student_name, roll_number, course_name, grade, issue_date]):
            return jsonify({
                "error": "Missing required fields. Please provide student_name, roll_number, course_name, grade, and issue_date."
            }), 400
        
        # Validate date format (basic validation)
        try:
            # Convert string date to date object for validation
            from datetime import datetime
            datetime.strptime(issue_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "error": "Invalid date format. Please use YYYY-MM-DD format."
            }), 400
        
        # Generate secure certificate hash with enhanced cryptography
        from utils.hashing import generate_secure_certificate_hash, generate_certificate_signature
        
        certificate_hash, salt = generate_secure_certificate_hash(
            student_name, roll_number, course_name, issue_date, str(user_id)
        )
        
        # Generate digital signature for the certificate
        certificate_signature = generate_certificate_signature(certificate_hash)
        
        # Get database connection
        connection = get_db_connection()
        if not connection:
            return jsonify({
                "error": "Database connection failed"
            }), 500
        
        try:
            cursor = connection.cursor()
            
            # Check if certificate with this hash already exists
            cursor.execute(
                "SELECT id FROM certificates WHERE certificate_hash = %s",
                (certificate_hash,)
            )
            
            if cursor.fetchone():
                return jsonify({
                    "error": "Certificate with these details already exists"
                }), 409
            
            # Store certificate hash on blockchain
            from services.blockchain_service import add_hash
            
            blockchain_tx_hash = add_hash(certificate_hash)
            
            # Insert new certificate into database with enhanced security
            cursor.execute(
                """INSERT INTO certificates 
                   (institution_id, student_name, roll_number, course_name, grade, issue_date, certificate_hash, blockchain_tx_hash, certificate_signature, salt) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (user_id, student_name, roll_number, course_name, grade, issue_date, certificate_hash, blockchain_tx_hash, certificate_signature, salt)
            )
            
            # Commit the transaction
            connection.commit()
            
            response_data = {
                "message": "Certificate added successfully with enhanced security",
                "certificate_hash": certificate_hash,
                "blockchain_tx_hash": blockchain_tx_hash,
                "certificate_signature": certificate_signature[:20] + "...",  # Show partial signature for confirmation
                "security_features": {
                    "cryptographic_signature": "Applied",
                    "blockchain_storage": "Completed" if blockchain_tx_hash else "Failed",
                    "hash_algorithm": "HMAC-SHA256 with salt",
                    "temporal_uniqueness": "Enabled"
                }
            }
            
            if not blockchain_tx_hash:
                response_data["blockchain_warning"] = "Certificate stored in database but blockchain storage failed"
            
            return jsonify(response_data), 201
            
        except Exception as e:
            # Rollback transaction on error
            connection.rollback()
            print(f"Database error during certificate addition: {e}")
            return jsonify({
                "error": "Database error occurred during certificate addition"
            }), 500
            
        finally:
            # Always close the database connection
            if connection:
                connection.close()
                
    except Exception as e:
        print(f"Unexpected error during certificate addition: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500


@cert_bp.route('/api/verify', methods=['POST'])
@token_required(allowed_user_types=['verifier'])
def verify_certificate(user_id, user_type):
    """
    Verify a certificate by uploading an image file.
    
    This endpoint allows authenticated verifiers to upload a certificate image for verification.
    It validates the file type, saves it temporarily, and processes it for verification.
    
    Expected Input:
        Multipart form data with a file field containing the certificate image
        
    Returns:
        JSON response with verification status and file information.
    """
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided. Please upload a certificate image."
            }), 400
        
        file = request.files['file']
        
        # Check if file is actually selected
        if file.filename == '':
            return jsonify({
                "error": "No file selected. Please choose a certificate image."
            }), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Sanitize filename for security
        filename = secure_filename(file.filename)
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Generate unique filename to prevent conflicts
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        try:
            # Save the uploaded file temporarily
            file.save(file_path)
            
            # Import OCR service for certificate processing
            from services.ocr_service import parse_details_from_image, validate_extracted_data
            from services.blockchain_service import verify_hash
            from utils.hashing import generate_certificate_hash
            
            # Extract details from the uploaded certificate
            extracted_details = parse_details_from_image(file_path)
            
            # Validate extracted data
            validated_details = validate_extracted_data(extracted_details)
            
            # Check if extraction was successful
            if validated_details.get('error'):
                return jsonify({
                    "error": f"Certificate processing failed: {validated_details['error']}"
                }), 400
            
            # Check if we have the minimum required data
            required_fields = ['student_name', 'roll_number', 'course_name', 'issue_date']
            missing_fields = [field for field in required_fields if not validated_details.get(field)]
            
            if missing_fields:
                return jsonify({
                    "error": f"Could not extract required information: {', '.join(missing_fields)}. Please ensure the certificate is clear and readable."
                }), 400
            
            # Try to find certificate using multiple approaches
            # since we now have enhanced security hash format
            
            connection = get_db_connection()
            if not connection:
                return jsonify({
                    "error": "Database connection failed"
                }), 500
            
            try:
                cursor = connection.cursor()
                certificate_record = None
                
                # Approach 1: Search by basic certificate data (name, roll, course, date)
                # This handles certificates regardless of hash format
                cursor.execute(
                    """SELECT c.*, i.name as institution_name 
                       FROM certificates c 
                       JOIN institutions i ON c.institution_id = i.id 
                       WHERE LOWER(c.student_name) = LOWER(%s) 
                       AND LOWER(c.roll_number) = LOWER(%s)
                       AND LOWER(c.course_name) = LOWER(%s)
                       AND c.issue_date = %s""",
                    (
                        validated_details['student_name'].strip(),
                        validated_details['roll_number'].strip(), 
                        validated_details['course_name'].strip(),
                        validated_details['issue_date']
                    )
                )
                
                certificate_record = cursor.fetchone()
                
                if certificate_record:
                    # Certificate found in database - perform comprehensive verification
                    
                    # Extract data from database record (adjusted for new schema)
                    cert_id = certificate_record[0]
                    institution_id = certificate_record[1]
                    student_name = certificate_record[2]
                    roll_number = certificate_record[3] 
                    course_name = certificate_record[4]
                    grade = certificate_record[5]
                    issue_date = certificate_record[6]
                    certificate_hash = certificate_record[7]
                    blockchain_tx_hash = certificate_record[8]
                    created_at = certificate_record[9]
                    updated_at = certificate_record[10]
                    # New security columns (may be None for older certificates)
                    certificate_signature = certificate_record[11] if len(certificate_record) > 11 else None
                    salt = certificate_record[12] if len(certificate_record) > 12 else None
                    institution_name = certificate_record[13] if len(certificate_record) > 13 else certificate_record[-1]
                    
                    # Perform multi-factor verification
                    blockchain_verified = False
                    signature_verified = False
                    
                    try:
                        # Factor 1: Database verification (already confirmed)
                        # Factor 2: Blockchain verification 
                        if blockchain_tx_hash:
                            blockchain_verified = verify_hash(certificate_hash)
                        
                        # Factor 3: Digital signature verification (if available)
                        if certificate_signature:
                            from utils.hashing import verify_certificate_signature
                            signature_verified = verify_certificate_signature(certificate_hash, certificate_signature)
                    except Exception as e:
                        print(f"Verification check error: {e}")
                    
                    result_data = {
                        "student_name": student_name,
                        "roll_number": roll_number,
                        "course_name": course_name,
                        "grade": grade,
                        "issue_date": issue_date.isoformat() if issue_date else None,
                        "institution_name": institution_name,
                        "certificate_hash": certificate_hash[:16] + "...",  # Truncate for display
                        "blockchain_tx_hash": blockchain_tx_hash[:16] + "..." if blockchain_tx_hash else None,
                        "verification_factors": {
                            "database_verified": True,
                            "blockchain_verified": blockchain_verified,
                            "signature_verified": signature_verified,
                            "enhanced_security": bool(certificate_signature)
                        }
                    }
                    
                    # Determine verification status based on comprehensive checks
                    total_factors = 1  # Database always verified if we reach here
                    verified_factors = 1  # Database verification
                    
                    if blockchain_tx_hash:
                        total_factors += 1
                        if blockchain_verified:
                            verified_factors += 1
                    
                    if certificate_signature:
                        total_factors += 1
                        if signature_verified:
                            verified_factors += 1
                    
                    # Determine status based on verification factors
                    if verified_factors == total_factors and total_factors >= 2:
                        result_data["status"] = "FULLY_VERIFIED"
                        result_data["verification_message"] = f"Certificate fully verified ({verified_factors}/{total_factors} factors)"
                        result_data["confidence_level"] = "HIGH"
                    elif verified_factors >= 2:
                        result_data["status"] = "PARTIALLY_VERIFIED"
                        result_data["verification_message"] = f"Certificate verified ({verified_factors}/{total_factors} factors)"
                        result_data["confidence_level"] = "MEDIUM"
                    else:
                        result_data["status"] = "BASIC_VERIFICATION"
                        result_data["verification_message"] = "Certificate found in database only"
                        result_data["confidence_level"] = "LOW"
                        result_data["warning"] = "Limited verification - consider additional authentication"
                    
                    return jsonify(result_data), 200
                else:
                    # Certificate not found in database
                    # Provide helpful information for troubleshooting
                    search_info = {
                        "searched_for": {
                            "student_name": validated_details.get('student_name', 'Not detected'),
                            "roll_number": validated_details.get('roll_number', 'Not detected'),
                            "course_name": validated_details.get('course_name', 'Not detected'),
                            "issue_date": validated_details.get('issue_date', 'Not detected')
                        }
                    }
                    
                    return jsonify({
                        "error": "Certificate not found in our database",
                        "details": "This certificate may not be issued by a registered institution, may be fraudulent, or the OCR extraction may have failed to read the certificate correctly.",
                        "extracted_data": search_info,
                        "suggestions": [
                            "Verify the certificate details are clearly visible",
                            "Ensure the certificate is from a registered institution",
                            "Check if the institution has added this certificate to the system",
                            "For real OCR accuracy, install Tesseract OCR"
                        ]
                    }), 404
                    
            except Exception as e:
                print(f"Database error during verification: {e}")
                return jsonify({
                    "error": "Database error occurred during verification"
                }), 500
            finally:
                if connection:
                    connection.close()
            
        except Exception as e:
            print(f"Error processing uploaded file: {e}")
            return jsonify({
                "error": "Error processing uploaded file"
            }), 500
            
        finally:
            # Clean up: delete the temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting temporary file: {e}")
                
    except Exception as e:
        print(f"Unexpected error during certificate verification: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500


@cert_bp.route('/api/certificate/extract', methods=['POST'])
@token_required(allowed_user_types=['institution'])
def extract_certificate_data(user_id, user_type):
    """
    Extract certificate data from uploaded image/PDF for institution use.
    
    This endpoint allows institutions to upload a certificate file and extract
    structured data using OCR. It's used for the drag-and-drop functionality.
    
    Expected Input:
        Multipart form data with:
        - file: Certificate image or PDF
        - extract_only: Flag to only extract data (optional)
        
    Returns:
        JSON response with extracted certificate data.
    """
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided. Please upload a certificate image or PDF."
            }), 400
        
        file = request.files['file']
        
        # Check if file is actually selected
        if file.filename == '':
            return jsonify({
                "error": "No file selected. Please choose a certificate file."
            }), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Sanitize filename for security
        filename = secure_filename(file.filename)
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Generate unique filename to prevent conflicts
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        try:
            # Save the uploaded file temporarily
            file.save(file_path)
            
            # Import OCR service for certificate processing
            from services.ocr_service import parse_details_from_image, validate_extracted_data
            
            # Extract details from the uploaded certificate
            extracted_details = parse_details_from_image(file_path)
            
            # Validate extracted data
            validated_details = validate_extracted_data(extracted_details)
            
            # Check if extraction was successful
            if validated_details.get('error'):
                return jsonify({
                    "error": f"Certificate processing failed: {validated_details['error']}",
                    "extracted_data": validated_details
                }), 400
            
            # Return extracted data for institution review
            return jsonify({
                "message": "Certificate data extracted successfully",
                "extracted_data": {
                    "student_name": validated_details.get('student_name'),
                    "roll_number": validated_details.get('roll_number'),
                    "course_name": validated_details.get('course_name'),
                    "grade": validated_details.get('grade'),
                    "issue_date": validated_details.get('issue_date'),
                    "institution_name": validated_details.get('institution_name')
                },
                "raw_text_preview": validated_details.get('raw_text', '')[:200] + "..." if validated_details.get('raw_text') else None
            }), 200
            
        except Exception as e:
            print(f"Error processing uploaded file: {e}")
            return jsonify({
                "error": "Error processing uploaded file. Please ensure the file is a valid certificate image or PDF."
            }), 500
            
        finally:
            # Clean up: delete the temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting temporary file: {e}")
                
    except Exception as e:
        print(f"Unexpected error during certificate extraction: {e}")
        return jsonify({
            "error": "An unexpected error occurred during file processing"
        }), 500


@cert_bp.route('/api/certificate/list', methods=['GET'])
@token_required(allowed_user_types=['institution'])
def list_certificates(user_id, user_type):
    """
    List all certificates issued by the authenticated institution.
    
    This endpoint allows authenticated institutions to retrieve a list of all
    certificates they have issued, with optional pagination support.
    
    Query Parameters:
        page (int): Page number for pagination (default: 1)
        limit (int): Number of certificates per page (default: 10)
        
    Returns:
        JSON response with list of certificates and pagination information.
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # Validate pagination parameters
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({
                "error": "Invalid pagination parameters. Page must be >= 1, limit must be between 1 and 100."
            }), 400
        
        # Calculate offset for pagination
        offset = (page - 1) * limit
        
        # Get database connection
        connection = get_db_connection()
        if not connection:
            return jsonify({
                "error": "Database connection failed"
            }), 500
        
        try:
            cursor = connection.cursor()
            
            # Get total count of certificates for this institution
            cursor.execute(
                "SELECT COUNT(*) FROM certificates WHERE institution_id = %s",
                (user_id,)
            )
            total_count = cursor.fetchone()[0]
            
            # Get paginated certificates
            cursor.execute(
                """SELECT id, student_name, roll_number, course_name, grade, issue_date, 
                          certificate_hash, blockchain_tx_hash, created_at
                   FROM certificates 
                   WHERE institution_id = %s 
                   ORDER BY created_at DESC 
                   LIMIT %s OFFSET %s""",
                (user_id, limit, offset)
            )
            
            certificates = cursor.fetchall()
            
            # Convert to list of dictionaries
            certificate_list = []
            for cert in certificates:
                certificate_list.append({
                    "id": cert[0],
                    "student_name": cert[1],
                    "roll_number": cert[2],
                    "course_name": cert[3],
                    "grade": cert[4],
                    "issue_date": cert[5].isoformat() if cert[5] else None,
                    "certificate_hash": cert[6],
                    "blockchain_tx_hash": cert[7],
                    "created_at": cert[8].isoformat() if cert[8] else None
                })
            
            # Calculate pagination info
            total_pages = (total_count + limit - 1) // limit
            has_next = page < total_pages
            has_prev = page > 1
            
            return jsonify({
                "certificates": certificate_list,
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_count": total_count,
                    "limit": limit,
                    "has_next": has_next,
                    "has_prev": has_prev
                }
            }), 200
            
        except Exception as e:
            print(f"Database error during certificate listing: {e}")
            return jsonify({
                "error": "Database error occurred during certificate listing"
            }), 500
            
        finally:
            # Always close the database connection
            if connection:
                connection.close()
                
    except Exception as e:
        print(f"Unexpected error during certificate listing: {e}")
        return jsonify({
            "error": "An unexpected error occurred"
        }), 500
