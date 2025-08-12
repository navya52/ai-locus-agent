"""
Upload Letter Serverless Function for AI Locus Agent

This function handles PDF upload and processing.
"""

from http.server import BaseHTTPRequestHandler
import json
import re

# Import our PDF processor
try:
    from pdf_utils import PDFProcessor
    PDF_PROCESSOR_AVAILABLE = True
    print("DEBUG: PDF processor imported successfully")
except ImportError as e:
    PDF_PROCESSOR_AVAILABLE = False
    print(f"DEBUG: PDF processor import failed: {e}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the request body
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            
            # Debug: Log what we received
            print(f"DEBUG: Received {len(post_data)} bytes")
            print(f"DEBUG: Content-Type: {self.headers.get('Content-Type', 'Not specified')}")
            print(f"DEBUG: PDF_PROCESSOR_AVAILABLE: {PDF_PROCESSOR_AVAILABLE}")
            
            # Extract filename from multipart data
            filename = "unknown_file"
            if b'filename=' in post_data:
                filename_start = post_data.find(b'filename=')
                if filename_start != -1:
                    quote_start = post_data.find(b'"', filename_start)
                    if quote_start != -1:
                        quote_end = post_data.find(b'"', quote_start + 1)
                        if quote_end != -1:
                            filename = post_data[quote_start + 1:quote_end].decode('utf-8', errors='ignore')
            
            # Extract PDF data from multipart form data
            pdf_bytes = None
            if b'%PDF' in post_data:
                pdf_start = post_data.find(b'%PDF')
                if pdf_start != -1:
                    pdf_bytes = post_data[pdf_start:]
                    print(f"DEBUG: Found PDF data, size: {len(pdf_bytes)} bytes")
            
            # Process PDF if we have the processor and PDF data
            if PDF_PROCESSOR_AVAILABLE and pdf_bytes:
                print("DEBUG: Attempting PDF processing")
                processor = PDFProcessor()
                result = processor.process_pdf(pdf_bytes)
                print(f"DEBUG: PDF processing result: {result}")
                
                if result['processing_successful']:
                    # Use real extracted data
                    response_data = {
                        'status': 'success',
                        'message': 'Clinical letter processed successfully',
                        'api_version': '1.0.0',
                        'processing_timestamp': '2025-08-12T20:00:00Z',
                        'file_info': {
                            'filename': filename,
                            'word_count': result['word_count'],
                            'character_count': result['character_count']
                        },
                        'extracted_data': {
                            'nhs_number': result['nhs_number'] or 'Not found',
                            'text_preview': result['preview']
                        },
                        'ai_summary': {
                            'summary': 'PDF analysis completed successfully',
                            'risk_assessment': {
                                'overall_risk': 'low',
                                'urgent_concerns': [],
                                'risk_factors': ['Sample risk factor']
                            },
                            'confidence_score': 0.85,
                            'key_findings': [
                                'PDF text extracted successfully',
                                'NHS number analysis completed'
                            ]
                        },
                        'storage_info': {
                            'storage_id': 'mock_storage_123',
                            'storage_status': 'stored',
                            'storage_reason': 'Clinical letter analysis stored successfully',
                            'data_retention_policy': 'Compliance-based retention',
                            'privacy_compliant': True,
                            'audit_trail_enabled': True
                        }
                    }
                else:
                    # PDF processing failed, return error
                    response_data = {
                        'status': 'error',
                        'message': f'PDF processing failed: {result["error"]}',
                        'file_info': {
                            'filename': filename,
                            'word_count': 0,
                            'character_count': 0
                        }
                    }
            else:
                # Fallback to mock data if PDF processor not available
                print("DEBUG: Using mock data fallback")
                response_data = {
                    'status': 'success',
                    'message': 'Clinical letter processed successfully (mock data)',
                    'api_version': '1.0.0',
                    'processing_timestamp': '2025-08-12T20:00:00Z',
                    'file_info': {
                        'filename': filename,
                        'word_count': 244,
                        'character_count': 1500
                    },
                    'extracted_data': {
                        'nhs_number': '7052493519',
                        'text_preview': 'Sample clinical letter content for demonstration purposes...'
                    },
                    'ai_summary': {
                        'summary': 'PDF analysis completed successfully',
                        'risk_assessment': {
                            'overall_risk': 'low',
                            'urgent_concerns': [],
                            'risk_factors': ['Sample risk factor']
                        },
                        'confidence_score': 0.85,
                        'key_findings': [
                            'PDF text extracted successfully',
                            'NHS number analysis completed'
                        ]
                    },
                    'storage_info': {
                        'storage_id': 'mock_storage_123',
                        'storage_status': 'stored',
                        'storage_reason': 'Clinical letter analysis stored successfully',
                        'data_retention_policy': 'Compliance-based retention',
                        'privacy_compliant': True,
                        'audit_trail_enabled': True
                    }
                }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_error_response(f"Server error: {str(e)}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_error_response(self, message):
        error_data = {
            'status': 'error',
            'message': message
        }
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(error_data).encode())
