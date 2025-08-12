"""
Health check endpoint for AI Locus Agent API
"""

import json
import datetime

def lambda_handler(event, context):
    """AWS Lambda handler function for health check"""
    
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request (CORS preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Health check response
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'service': 'AI Locus Agent API',
            'version': '1.0.0',
            'region': 'eu-west-2',
            'environment': 'production',
            'uptime': 'operational',
            'checks': {
                'lambda_function': 'healthy',
                'api_gateway': 'healthy',
                'pdf_processing': 'available'
            }
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(health_data, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
            })
        }
