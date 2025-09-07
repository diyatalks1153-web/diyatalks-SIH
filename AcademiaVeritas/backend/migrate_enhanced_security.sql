-- Migration script to add enhanced security features to existing database
-- This script adds the new columns for enhanced cryptographic security

USE academia_veritas;

-- Add new security columns to certificates table
ALTER TABLE certificates 
ADD COLUMN certificate_signature TEXT NULL COMMENT 'Digital signature of the certificate',
ADD COLUMN salt VARCHAR(255) NULL COMMENT 'Random salt used in hash generation';

-- Create indexes for the new columns
CREATE INDEX idx_certificates_signature ON certificates(certificate_signature(100));
CREATE INDEX idx_certificates_salt ON certificates(salt);

-- Display current table structure
DESCRIBE certificates;
