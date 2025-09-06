-- CertiSure Database Schema
-- This SQL script creates the necessary tables for the CertiSure application

-- Create verifiers table for verifier authentication
CREATE TABLE verifiers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Create institutions table for institution authentication
CREATE TABLE institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Create certificates table for certificate records
CREATE TABLE certificates (
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
);

-- Create indexes for better performance
CREATE INDEX idx_certificates_institution_id ON certificates(institution_id);
CREATE INDEX idx_certificates_certificate_hash ON certificates(certificate_hash);
CREATE INDEX idx_certificates_roll_number ON certificates(roll_number);
CREATE INDEX idx_verifiers_email ON verifiers(email);
CREATE INDEX idx_institutions_email ON institutions(email);

-- Insert sample data for testing (optional)
-- INSERT INTO institutions (name, email, password_hash) VALUES 
-- ('Jharkhand University', 'admin@jhu.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2');

-- INSERT INTO verifiers (name, email, password_hash) VALUES 
-- ('Test Verifier', 'verifier@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2');
