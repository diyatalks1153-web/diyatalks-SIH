-- AcademiaVeritas MySQL Database Schema
-- This SQL script creates the necessary tables for the AcademiaVeritas application

-- Set charset and collation for proper UTF-8 support
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS academia_veritas 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE academia_veritas;

-- Create verifiers table for verifier authentication
CREATE TABLE verifiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create institutions table for institution authentication
CREATE TABLE institutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create certificates table for certificate records
CREATE TABLE certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institution_id INT NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    roll_number VARCHAR(100) NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    grade VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    certificate_hash VARCHAR(255) UNIQUE NOT NULL,
    blockchain_tx_hash VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (institution_id) REFERENCES institutions(id) ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create indexes for better performance
CREATE INDEX idx_certificates_institution_id ON certificates(institution_id);
CREATE INDEX idx_certificates_certificate_hash ON certificates(certificate_hash);
CREATE INDEX idx_certificates_roll_number ON certificates(roll_number);
CREATE INDEX idx_certificates_created_at ON certificates(created_at);
CREATE INDEX idx_verifiers_email ON verifiers(email);
CREATE INDEX idx_institutions_email ON institutions(email);

-- Insert sample data for testing (optional)
-- Uncomment the following lines to insert test data
/*
INSERT INTO institutions (name, email, password_hash) VALUES 
('Jharkhand University', 'admin@jhu.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2'),
('Indian Institute of Technology', 'admin@iit.ac.in', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2');

INSERT INTO verifiers (name, email, password_hash) VALUES 
('Test Verifier', 'verifier@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2'),
('HR Department', 'hr@company.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2');
*/
