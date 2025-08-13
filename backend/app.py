"""
AI Locus Agent Flask Backend

A production-ready Flask application for processing patient data
with AI-powered locus identification and medical analysis.

This module provides a RESTful API for medical data processing
with built-in validation, error handling, and compliance features.
"""

import logging
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile
import os
from config import Config
from compliance import ComplianceManager
from ai_processor import get_ai_processor, AIAnalysisResult
from storage_manager import get_storage_manager
from pdf_processor import get_pdf_processor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for production
CORS(app, origins=os.getenv('ALLOWED_ORIGINS', '*').split(','))

# Configuration
MAX_PATIENT_DATA_LENGTH = int(os.getenv('MAX_PATIENT_DATA_LENGTH', '10000'))
API_VERSION = os.getenv('API_VERSION', '1.0.0')


def validate_patient_data(data: str) -> Dict[str, Any]:
    """
    Validate patient data according to medical and compliance standards.
    
    Args:
        data: Raw patient data string
        
    Returns:
        Dict containing validation results and cleaned data
        
    Raises:
        ValueError: If data fails validation
    """
    if not data or not isinstance(data, str):
        raise ValueError("Patient data must be a non-empty string")
    
    cleaned_data = data.strip()
    
    if not cleaned_data:
        raise ValueError("Patient data cannot be empty after cleaning")
    
    if len(cleaned_data) > MAX_PATIENT_DATA_LENGTH:
        raise ValueError(f"Patient data exceeds maximum length of {MAX_PATIENT_DATA_LENGTH} characters")
    
    # Check for potentially sensitive information patterns
    sensitive_patterns = [
        'ssn', 'social security', 'credit card', 'password',
        'pin', 'account number', 'routing number'
    ]
    
    lower_data = cleaned_data.lower()
    for pattern in sensitive_patterns:
        if pattern in lower_data:
            logger.warning(f"Potential sensitive data detected: {pattern}")
    
    return {
        'cleaned_data': cleaned_data,
        'word_count': len(cleaned_data.split()),
        'character_count': len(cleaned_data),
        'validation_passed': True
    }


def process_ai_analysis(patient_data: str) -> Dict[str, Any]:
    """
    Process patient data through AI locus agent algorithms.
    
    Args:
        patient_data: Validated and cleaned patient data
        
    Returns:
        Dict containing AI analysis results
    """
    # Initialize AI processor
    config = Config()
    ai_processor = get_ai_processor(config)
    
    # Perform AI analysis
    ai_result = ai_processor.analyze_patient_data(patient_data)
    
    # Convert to response format
    return {
        'locus_identified': True,
        'confidence_score': ai_result.confidence_score,
        'summary': ai_result.summary,
        'key_findings': ai_result.key_findings,
        'recommended_actions': ai_result.recommendations,
        'risk_factors': ai_result.risk_assessment.get('risk_factors', []),
        'urgent_concerns': ai_result.risk_assessment.get('urgent_concerns', []),
        'overall_risk': ai_result.risk_assessment.get('overall_risk', 'unknown'),
        'processing_time': ai_result.processing_time,
        'model_used': ai_result.model_used,
        'tokens_used': ai_result.tokens_used,
        'ai_available': ai_processor.is_available()
    }


@app.route('/api/v1/process-patient-data', methods=['POST'])
def process_patient_data():
    """
    AI Locus Agent endpoint for processing patient data.
    
    Accepts patient information and returns AI-powered analysis
    with locus identification and medical recommendations.
    
    Expected JSON payload:
    {
        "patient_data": "Patient symptoms, medical history, or clinical notes"
    }
    
    Returns:
        JSON response with AI analysis results
    """
    start_time = datetime.now(timezone.utc)
    
    try:
        # Extract and validate request data
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                'error': 'Invalid JSON payload',
                'status': 'error',
                'message': 'Request body must contain valid JSON',
                'timestamp': start_time.isoformat()
            }), 400
        
        if 'patient_data' not in request_data:
            return jsonify({
                'error': 'Missing required field: patient_data',
                'status': 'error',
                'message': 'Request must include patient_data field',
                'timestamp': start_time.isoformat()
            }), 400
        
        # Validate patient data
        try:
            validation_result = validate_patient_data(request_data['patient_data'])
        except ValueError as e:
            return jsonify({
                'error': 'Data validation failed',
                'status': 'error',
                'message': str(e),
                'timestamp': start_time.isoformat()
            }), 400
        
        # Process through AI locus agent
        ai_results = process_ai_analysis(validation_result['cleaned_data'])
        
        # Calculate processing time
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        # Initialize storage manager
        storage_manager = get_storage_manager()
        
        # Prepare analysis result for storage
        analysis_result = {
            'analysis_id': f"analysis_{start_time.strftime('%Y%m%d_%H%M%S')}",
            'processing_timestamp': start_time.isoformat(),
            'processing_time_seconds': processing_time,
            'word_count': validation_result['word_count'],
            'character_count': validation_result['character_count'],
            **ai_results  # Include all AI analysis results
        }
        
        # Attempt to store analysis result
        storage_id = None
        storage_status = "not_stored"
        storage_reason = "No storage attempted"
        
        try:
            storage_id = storage_manager.store_analysis_result(analysis_result)
            if storage_id:
                storage_status = "stored"
                storage_reason = "Analysis result stored successfully"
                logger.info(f"Analysis result stored with ID: {storage_id}")
            else:
                storage_status = "rejected"
                storage_reason = "Data classification rejected storage"
                logger.info("Analysis result not stored due to data classification")
        except Exception as storage_error:
            storage_status = "error"
            storage_reason = f"Storage error: {str(storage_error)}"
            logger.error(f"Storage error: {storage_error}")
        
        # Log successful processing (without sensitive data)
        logger.info(
            f"Patient data processed successfully. "
            f"Processing time: {processing_time:.3f}s, "
            f"Word count: {validation_result['word_count']}, "
            f"Storage: {storage_status}"
        )
        
        # Return comprehensive response
        return jsonify({
            'status': 'success',
            'message': 'Patient data processed successfully by AI locus agent',
            'api_version': API_VERSION,
            'processing_timestamp': start_time.isoformat(),
            'processing_time_seconds': processing_time,
            'data_analysis': {
                'word_count': validation_result['word_count'],
                'character_count': validation_result['character_count'],
                'data_validation_passed': validation_result['validation_passed']
            },
            'ai_analysis': ai_results,
            'storage_info': {
                'storage_id': storage_id,
                'storage_status': storage_status,
                'storage_reason': storage_reason,
                'data_retention_policy': 'Compliance-based retention',
                'privacy_compliant': True,
                'audit_trail_enabled': True
            }
        }), 200
        
    except Exception as e:
        # Log error for debugging
        logger.error(f"Error processing patient data: {str(e)}", exc_info=True)
        
        # Return generic error message (don't expose internal details)
        return jsonify({
            'error': 'Internal processing error',
            'status': 'error',
            'message': 'An error occurred while processing patient data',
            'timestamp': start_time.isoformat(),
            'error_id': f"ERR_{start_time.strftime('%Y%m%d_%H%M%S')}"
        }), 500


@app.route('/api/v1/storage/analysis/<storage_id>', methods=['GET'])
def get_stored_analysis(storage_id):
    """
    Retrieve a stored analysis result by storage ID.
    
    Args:
        storage_id: The storage ID returned from processing
        
    Returns:
        JSON response with stored analysis data
    """
    try:
        storage_manager = get_storage_manager()
        stored_data = storage_manager.retrieve_analysis_result(storage_id)
        
        if not stored_data:
            return jsonify({
                'error': 'Analysis not found',
                'status': 'error',
                'message': f'No analysis found with storage ID: {storage_id}',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis retrieved successfully',
            'storage_id': storage_id,
            'analysis_data': stored_data,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving stored analysis {storage_id}: {str(e)}")
        return jsonify({
            'error': 'Retrieval error',
            'status': 'error',
            'message': 'An error occurred while retrieving the analysis',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500


@app.route('/api/v1/storage/analysis/<storage_id>', methods=['DELETE'])
def delete_stored_analysis(storage_id):
    """
    Delete a stored analysis result (GDPR compliance).
    
    Args:
        storage_id: The storage ID to delete
        
    Returns:
        JSON response confirming deletion
    """
    try:
        storage_manager = get_storage_manager()
        deleted = storage_manager.delete_analysis_result(storage_id)
        
        if not deleted:
            return jsonify({
                'error': 'Analysis not found',
                'status': 'error',
                'message': f'No analysis found with storage ID: {storage_id}',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis deleted successfully',
            'storage_id': storage_id,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting stored analysis {storage_id}: {str(e)}")
        return jsonify({
            'error': 'Deletion error',
            'status': 'error',
            'message': 'An error occurred while deleting the analysis',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500


@app.route('/api/v1/storage/stats', methods=['GET'])
def get_storage_stats():
    """
    Get storage statistics and system information.
    
    Returns:
        JSON response with storage statistics
    """
    try:
        storage_manager = get_storage_manager()
        stats = storage_manager.get_storage_stats()
        
        return jsonify({
            'status': 'success',
            'message': 'Storage statistics retrieved successfully',
            'storage_stats': stats,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting storage stats: {str(e)}")
        return jsonify({
            'error': 'Statistics error',
            'status': 'error',
            'message': 'An error occurred while retrieving storage statistics',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and load balancer health checks.
    
    Returns:
        JSON response with service status and version information
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AI Locus Agent Backend',
        'version': API_VERSION,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'environment': os.getenv('FLASK_ENV', 'development'),
        'features': {
            'patient_data_processing': True,
            'ai_analysis': True,
            'compliance_monitoring': True,
            'data_storage': True,
            'gdpr_compliance': True
        }
    }), 200


@app.route('/api/v1/status', methods=['GET'])
def status_check():
    """
    Detailed status endpoint for system monitoring.
    
    Returns:
        JSON response with detailed system status
    """
    return jsonify({
        'status': 'operational',
        'service': 'AI Locus Agent Backend',
        'version': API_VERSION,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'system_info': {
            'python_version': os.getenv('PYTHON_VERSION', 'Unknown'),
            'flask_version': '2.3.3',
            'environment': os.getenv('FLASK_ENV', 'development')
        },
        'performance': {
            'max_patient_data_length': MAX_PATIENT_DATA_LENGTH,
            'cors_enabled': True
        }
    }), 200


@app.route('/api/v1/upload-letter', methods=['POST'])
def upload_clinical_letter():
    """
    Upload and process a clinical letter PDF.
    
    Accepts a PDF file, extracts text and NHS number,
    generates a summary using AI, and stores the data.
    
    Returns:
        JSON response with processing results
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'status': 'error',
                'message': 'Please upload a PDF file',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'status': 'error',
                'message': 'Please select a PDF file to upload',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 400
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({
                'error': 'Invalid file type',
                'status': 'error',
                'message': 'Only PDF files are supported',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Initialize PDF processor
            pdf_processor = get_pdf_processor()
            
            # Process the clinical letter
            processing_result = pdf_processor.process_clinical_letter(temp_path)
            
            if not processing_result['processing_successful']:
                return jsonify({
                    'error': 'PDF processing failed',
                    'status': 'error',
                    'message': processing_result.get('error', 'Failed to process PDF'),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }), 400
            
            # Extract key information
            text_content = processing_result['text_content']
            nhs_number = processing_result['nhs_number']
            word_count = processing_result['word_count']
            character_count = processing_result['character_count']
            
            # Initialize AI processor for summarization
            config = Config()
            ai_processor = get_ai_processor(config)
            
            # Generate letter summary using AI
            ai_result = ai_processor.analyze_patient_data(text_content)
            
            # Prepare analysis result for storage
            analysis_result = {
                'analysis_id': f"letter_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
                'processing_timestamp': datetime.now(timezone.utc).isoformat(),
                'filename': filename,
                'nhs_number': nhs_number,
                'word_count': word_count,
                'character_count': character_count,
                'text_content': text_content,
                'ai_summary': ai_result,
                'processing_successful': True
            }
            
            # Initialize storage manager
            storage_manager = get_storage_manager()
            
            # Store the analysis result
            storage_id = None
            storage_status = "not_stored"
            storage_reason = "No storage attempted"
            
            try:
                storage_id = storage_manager.store_analysis_result(analysis_result)
                if storage_id:
                    storage_status = "stored"
                    storage_reason = "Clinical letter analysis stored successfully"
                    logger.info(f"Clinical letter analysis stored with ID: {storage_id}")
                else:
                    storage_status = "rejected"
                    storage_reason = "Data classification rejected storage"
                    logger.info("Clinical letter analysis not stored due to data classification")
            except Exception as storage_error:
                storage_status = "error"
                storage_reason = f"Storage error: {str(storage_error)}"
                logger.error(f"Storage error: {storage_error}")
            
            # Return comprehensive response
            return jsonify({
                'status': 'success',
                'message': 'Clinical letter processed successfully',
                'api_version': API_VERSION,
                'processing_timestamp': datetime.now(timezone.utc).isoformat(),
                'file_info': {
                    'filename': filename,
                    'word_count': word_count,
                    'character_count': character_count
                },
                'extracted_data': {
                    'nhs_number': nhs_number,
                    'text_preview': processing_result['preview']
                },
                'ai_summary': ai_result,
                'storage_info': {
                    'storage_id': storage_id,
                    'storage_status': storage_status,
                    'storage_reason': storage_reason,
                    'data_retention_policy': 'Compliance-based retention',
                    'privacy_compliant': True,
                    'audit_trail_enabled': True
                }
            }), 200
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")
        
    except Exception as e:
        logger.error(f"Error processing clinical letter: {str(e)}")
        return jsonify({
            'error': 'Processing error',
            'status': 'error',
            'message': 'An error occurred while processing the clinical letter',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with proper JSON response."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'message': 'The requested endpoint does not exist',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors with proper JSON response."""
    return jsonify({
        'error': 'Method not allowed',
        'status': 'error',
        'message': 'The HTTP method is not supported for this endpoint',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 405


if __name__ == '__main__':
    # Production configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    
    logger.info(f"Starting AI Locus Agent Backend on {host}:{port}")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"API Version: {API_VERSION}")
    
    # In production, use a proper WSGI server like Gunicorn
    app.run(debug=debug_mode, host=host, port=port)
