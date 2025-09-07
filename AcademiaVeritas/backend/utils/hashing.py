"""
Hashing utilities module for AcademiaVeritas project.

This module provides secure password hashing and certificate integrity verification
functionality using industry-standard cryptographic methods.
"""

import hashlib
import hmac
import secrets
import base64
import time
from typing import Tuple, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def hash_password(password: str) -> str:
    """
    Securely hash a plain-text password using Werkzeug's password hashing.
    
    This function uses Werkzeug's built-in password hashing which employs
    PBKDF2 with SHA-256 and a random salt for secure password storage.
    
    Args:
        password (str): The plain-text password to be hashed
        
    Returns:
        str: A securely hashed password string that can be safely stored in the database
        
    Example:
        >>> hashed = hash_password("my_secure_password")
        >>> print(hashed)  # Output: pbkdf2:sha256:600000$...
    """
    return generate_password_hash(password)


def check_password(hashed_password: str, password: str) -> bool:
    """
    Verify a plain-text password against its hashed version.
    
    This function securely compares a plain-text password with a hashed password
    using Werkzeug's password checking functionality, which handles timing attacks
    and other security considerations.
    
    Args:
        hashed_password (str): The hashed password stored in the database
        password (str): The plain-text password to verify
        
    Returns:
        bool: True if the password matches the hash, False otherwise
        
    Example:
        >>> stored_hash = "pbkdf2:sha256:600000$..."
        >>> is_valid = check_password(stored_hash, "my_secure_password")
        >>> print(is_valid)  # Output: True or False
    """
    return check_password_hash(hashed_password, password)


def generate_certificate_hash(student_name: str, roll_number: str, course_name: str, issue_date: str) -> str:
    """
    Generate a deterministic SHA-256 hash for certificate data integrity verification.
    
    This function creates a unique, deterministic hash for each certificate by:
    1. Concatenating the input parameters in a fixed order
    2. Converting all inputs to lowercase strings
    3. Separating them with pipe (|) characters
    4. Applying SHA-256 hashing to the resulting string
    
    The resulting hash serves as a unique identifier for the certificate and ensures
    data integrity by detecting any modifications to the certificate data.
    
    Args:
        student_name (str): Full name of the student
        roll_number (str): Student's roll number or ID
        course_name (str): Name of the course or degree program
        issue_date (str): Date when the certificate was issued (YYYY-MM-DD format)
        
    Returns:
        str: A 64-character hexadecimal SHA-256 hash string
        
    Example:
        >>> hash_value = generate_certificate_hash(
        ...     "Jane Doe", 
        ...     "R-98765", 
        ...     "Information Technology", 
        ...     "2025-10-15"
        ... )
        >>> print(hash_value)  # Output: a1b2c3d4e5f6...
        
    Note:
        The input format for issue_date should be consistent (YYYY-MM-DD) to ensure
        deterministic hash generation across different systems.
    """
    # Create a deterministic string by concatenating inputs in fixed order
    # Convert all inputs to lowercase and separate with pipe characters
    certificate_string = f"{student_name.lower()}|{roll_number.lower()}|{course_name.lower()}|{issue_date.lower()}"
    
    # Apply SHA-256 hashing to the concatenated string
    hash_object = hashlib.sha256(certificate_string.encode('utf-8'))
    
    # Return the hexadecimal digest as a string
    return hash_object.hexdigest()


def generate_secure_certificate_hash(student_name: str, roll_number: str, 
                                    course_name: str, issue_date: str, 
                                    institution_id: str, salt: str = None) -> Tuple[str, str]:
    """
    Generate a secure, salted SHA-256 hash for certificate data with enhanced security.
    
    This function creates a cryptographically secure hash by:
    1. Adding a random salt if not provided
    2. Adding institution ID for uniqueness
    3. Adding timestamp for temporal uniqueness
    4. Using HMAC-SHA256 for additional security
    
    Args:
        student_name (str): Full name of the student
        roll_number (str): Student's roll number or ID
        course_name (str): Name of the course or degree program
        issue_date (str): Date when the certificate was issued
        institution_id (str): Unique identifier of the issuing institution
        salt (str, optional): Salt for the hash. If None, generates random salt
        
    Returns:
        Tuple[str, str]: A tuple containing (hash, salt)
    """
    # Generate random salt if not provided
    if salt is None:
        salt = secrets.token_hex(16)  # 32 character hex string
    
    # Add timestamp for temporal uniqueness
    timestamp = str(int(time.time()))
    
    # Create comprehensive certificate string
    certificate_data = (
        f"{student_name.lower().strip()}|"
        f"{roll_number.lower().strip()}|"
        f"{course_name.lower().strip()}|"
        f"{issue_date.strip()}|"
        f"{institution_id}|"
        f"{timestamp}|"
        f"{salt}"
    )
    
    # Use HMAC-SHA256 for additional security
    secret_key = f"academia_veritas_{institution_id}_{salt}"
    hash_object = hmac.new(
        secret_key.encode('utf-8'),
        certificate_data.encode('utf-8'),
        hashlib.sha256
    )
    
    return hash_object.hexdigest(), salt


def generate_certificate_signature(certificate_hash: str, private_key: str = None) -> str:
    """
    Generate a digital signature for the certificate hash.
    
    Args:
        certificate_hash (str): The certificate hash to sign
        private_key (str, optional): Private key for signing
        
    Returns:
        str: Base64 encoded digital signature
    """
    if private_key is None:
        private_key = "academia_veritas_default_key_2024"  # In production, use proper key management
    
    # Create HMAC signature
    signature = hmac.new(
        private_key.encode('utf-8'),
        certificate_hash.encode('utf-8'),
        hashlib.sha256
    )
    
    # Return base64 encoded signature
    return base64.b64encode(signature.digest()).decode('utf-8')


def verify_certificate_signature(certificate_hash: str, signature: str, private_key: str = None) -> bool:
    """
    Verify a certificate hash signature.
    
    Args:
        certificate_hash (str): The original certificate hash
        signature (str): Base64 encoded signature to verify
        private_key (str, optional): Private key for verification
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        if private_key is None:
            private_key = "academia_veritas_default_key_2024"
        
        # Decode the signature
        signature_bytes = base64.b64decode(signature)
        
        # Generate expected signature
        expected_signature = hmac.new(
            private_key.encode('utf-8'),
            certificate_hash.encode('utf-8'),
            hashlib.sha256
        )
        
        # Use secure comparison to prevent timing attacks
        return hmac.compare_digest(signature_bytes, expected_signature.digest())
        
    except Exception:
        return False


def encrypt_certificate_data(data: str, password: str) -> Tuple[str, str, str]:
    """
    Encrypt certificate data using AES encryption.
    
    Args:
        data (str): The data to encrypt
        password (str): Password for encryption
        
    Returns:
        Tuple[str, str, str]: (encrypted_data, salt, iv) all base64 encoded
    """
    # Generate random salt and IV
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    
    # Derive key from password using PBKDF2
    key = PBKDF2(password, salt, 32, count=100000, hmac_hash_module=SHA256)
    
    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the data to be multiple of 16 bytes
    pad_len = 16 - (len(data) % 16)
    padded_data = data + (chr(pad_len) * pad_len)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data.encode('utf-8'))
    
    # Return base64 encoded values
    return (
        base64.b64encode(encrypted_data).decode('utf-8'),
        base64.b64encode(salt).decode('utf-8'),
        base64.b64encode(iv).decode('utf-8')
    )


def decrypt_certificate_data(encrypted_data: str, salt: str, iv: str, password: str) -> Optional[str]:
    """
    Decrypt certificate data using AES decryption.
    
    Args:
        encrypted_data (str): Base64 encoded encrypted data
        salt (str): Base64 encoded salt
        iv (str): Base64 encoded initialization vector
        password (str): Password for decryption
        
    Returns:
        Optional[str]: Decrypted data or None if decryption failed
    """
    try:
        # Decode base64 values
        encrypted_bytes = base64.b64decode(encrypted_data)
        salt_bytes = base64.b64decode(salt)
        iv_bytes = base64.b64decode(iv)
        
        # Derive key from password
        key = PBKDF2(password, salt_bytes, 32, count=100000, hmac_hash_module=SHA256)
        
        # Create AES cipher
        cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
        
        # Decrypt the data
        decrypted_padded = cipher.decrypt(encrypted_bytes).decode('utf-8')
        
        # Remove padding
        pad_len = ord(decrypted_padded[-1])
        decrypted_data = decrypted_padded[:-pad_len]
        
        return decrypted_data
        
    except Exception:
        return None


def generate_merkle_root(certificate_hashes: list) -> str:
    """
    Generate a Merkle root hash from a list of certificate hashes.
    
    This creates a Merkle tree structure for batch verification of multiple certificates.
    
    Args:
        certificate_hashes (list): List of certificate hashes
        
    Returns:
        str: Merkle root hash
    """
    if not certificate_hashes:
        return hashlib.sha256(b'').hexdigest()
    
    if len(certificate_hashes) == 1:
        return certificate_hashes[0]
    
    # Ensure even number of hashes
    if len(certificate_hashes) % 2 == 1:
        certificate_hashes.append(certificate_hashes[-1])
    
    # Create next level of the tree
    next_level = []
    for i in range(0, len(certificate_hashes), 2):
        combined = certificate_hashes[i] + certificate_hashes[i + 1]
        next_level.append(hashlib.sha256(combined.encode('utf-8')).hexdigest())
    
    # Recursively build the tree
    return generate_merkle_root(next_level)
