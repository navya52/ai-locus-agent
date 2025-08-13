"""
Health Check Serverless Function for AI Locus Agent

This function provides a health check endpoint for the Vercel deployment.
"""

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write('{"status": "healthy", "message": "API is working!"}'.encode())
