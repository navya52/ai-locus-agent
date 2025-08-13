"""
Configuration module for AI Locus Agent Backend.

This module contains all configuration settings for different environments
and compliance requirements for medical data processing.
"""

import os
from typing import List, Dict, Any


class Config:
    """Base configuration class with common settings."""
    
    # API Configuration
    API_VERSION = os.getenv('API_VERSION', '1.0.0')
    API_TITLE = 'AI Locus Agent Backend'
    API_DESCRIPTION = 'Medical AI system for patient data processing and locus identification'
    
    # Server Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Data Processing Limits
    MAX_PATIENT_DATA_LENGTH = int(os.getenv('MAX_PATIENT_DATA_LENGTH', '10000'))
    MAX_PROCESSING_TIME = int(os.getenv('MAX_PROCESSING_TIME', '30'))  # seconds
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))  # requests per minute
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # Development AI settings
    AI_MODEL_PATH = os.getenv('AI_MODEL_PATH', './models/dev_model')
    AI_CONFIDENCE_THRESHOLD = 0.7


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Production security settings
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Must be set in production
    
    # Production CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
    
    # Production AI settings
    AI_MODEL_PATH = os.getenv('AI_MODEL_PATH', '/app/models/prod_model')
    AI_CONFIDENCE_THRESHOLD = 0.8
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Database configuration (if needed)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Redis configuration (for caching and rate limiting)
    REDIS_URL = os.getenv('REDIS_URL')


class TestingConfig(Config):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    
    # Testing-specific settings
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS = ['http://localhost:3000']
    
    # Test AI settings
    AI_MODEL_PATH = './tests/test_models'
    AI_CONFIDENCE_THRESHOLD = 0.5


class ComplianceConfig:
    """Compliance and regulatory configuration."""
    
    # GDPR Compliance
    GDPR_ENABLED = os.getenv('GDPR_ENABLED', 'True').lower() == 'true'
    DATA_RETENTION_DAYS = int(os.getenv('DATA_RETENTION_DAYS', '30'))
    RIGHT_TO_BE_FORGOTTEN = os.getenv('RIGHT_TO_BE_FORGOTTEN', 'True').lower() == 'true'
    
    # HIPAA Compliance (US)
    HIPAA_ENABLED = os.getenv('HIPAA_ENABLED', 'True').lower() == 'true'
    PHI_DETECTION_ENABLED = os.getenv('PHI_DETECTION_ENABLED', 'True').lower() == 'true'
    
    # Data Encryption
    ENCRYPTION_ENABLED = os.getenv('ENCRYPTION_ENABLED', 'True').lower() == 'true'
    ENCRYPTION_ALGORITHM = os.getenv('ENCRYPTION_ALGORITHM', 'AES-256')
    
    # Audit Logging
    AUDIT_LOGGING_ENABLED = os.getenv('AUDIT_LOGGING_ENABLED', 'True').lower() == 'true'
    AUDIT_LOG_RETENTION_DAYS = int(os.getenv('AUDIT_LOG_RETENTION_DAYS', '90'))
    
    # Data Processing Agreements
    DPA_ENABLED = os.getenv('DPA_ENABLED', 'True').lower() == 'true'
    
    # Consent Management
    CONSENT_MANAGEMENT_ENABLED = os.getenv('CONSENT_MANAGEMENT_ENABLED', 'True').lower() == 'true'
    
    # Data Minimization
    DATA_MINIMIZATION_ENABLED = os.getenv('DATA_MINIMIZATION_ENABLED', 'True').lower() == 'true'
    MAX_DATA_FIELDS = int(os.getenv('MAX_DATA_FIELDS', '50'))
    
    # Privacy by Design
    PRIVACY_BY_DEFAULT = os.getenv('PRIVACY_BY_DEFAULT', 'True').lower() == 'true'
    
    # Data Protection Impact Assessment (DPIA)
    DPIA_ENABLED = os.getenv('DPIA_ENABLED', 'True').lower() == 'true'
    
    # Breach Notification
    BREACH_NOTIFICATION_ENABLED = os.getenv('BREACH_NOTIFICATION_ENABLED', 'True').lower() == 'true'
    BREACH_NOTIFICATION_HOURS = int(os.getenv('BREACH_NOTIFICATION_HOURS', '72'))


class SecurityConfig:
    """Security configuration settings."""
    
    # Authentication
    AUTH_ENABLED = os.getenv('AUTH_ENABLED', 'True').lower() == 'true'
    AUTH_TYPE = os.getenv('AUTH_TYPE', 'JWT')  # JWT, OAuth2, API Key
    
    # API Security
    API_KEY_ENABLED = os.getenv('API_KEY_ENABLED', 'True').lower() == 'true'
    API_KEY_HEADER = os.getenv('API_KEY_HEADER', 'X-API-Key')
    
    # Input Validation
    INPUT_SANITIZATION_ENABLED = os.getenv('INPUT_SANITIZATION_ENABLED', 'True').lower() == 'true'
    SQL_INJECTION_PROTECTION = os.getenv('SQL_INJECTION_PROTECTION', 'True').lower() == 'true'
    XSS_PROTECTION = os.getenv('XSS_PROTECTION', 'True').lower() == 'true'
    
    # HTTPS/TLS
    HTTPS_REQUIRED = os.getenv('HTTPS_REQUIRED', 'True').lower() == 'true'
    TLS_VERSION = os.getenv('TLS_VERSION', '1.3')
    
    # Headers Security
    SECURITY_HEADERS_ENABLED = os.getenv('SECURITY_HEADERS_ENABLED', 'True').lower() == 'true'
    
    # Session Security
    SESSION_SECURE = os.getenv('SESSION_SECURE', 'True').lower() == 'true'
    SESSION_HTTPONLY = os.getenv('SESSION_HTTPONLY', 'True').lower() == 'true'
    SESSION_SAMESITE = os.getenv('SESSION_SAMESITE', 'Strict')


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """
    Get configuration based on environment.
    
    Args:
        config_name: Name of the configuration to load
        
    Returns:
        Configuration object
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])


def get_compliance_config() -> ComplianceConfig:
    """Get compliance configuration."""
    return ComplianceConfig()


def get_security_config() -> SecurityConfig:
    """Get security configuration."""
    return SecurityConfig()
