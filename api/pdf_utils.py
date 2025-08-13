"""
PDF Utilities for Vercel Serverless Functions

Simplified version of PDF processing for clinical letters.
"""

import re
import io
import base64
from typing import Dict, Any, Optional

try:
    import PyPDF2
    import pdfplumber
    PDF_LIBS_AVAILABLE = True
except ImportError:
    PDF_LIBS_AVAILABLE = False

class PDFProcessor:
    """Simplified PDF processor for serverless functions"""
    
    def __init__(self):
        # NHS number regex patterns
        self.nhs_patterns = [
            r'\b\d{3}\s*\d{3}\s*\d{4}\b',  # Standard format: 123 456 7890
            r'\b\d{10}\b',                  # No spaces: 1234567890
            r'\bNHS\s*Number[:\s]*(\d{3}\s*\d{3}\s*\d{4})\b',  # With "NHS Number:" prefix
            r'\bNHS\s*No[:\s]*(\d{3}\s*\d{3}\s*\d{4})\b',     # With "NHS No:" prefix
        ]
    
    def extract_text_from_pdf_bytes(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        if not PDF_LIBS_AVAILABLE:
            return "PDF processing libraries not available"
        
        try:
            text_content = ""
            
            # Try pdfplumber first
            try:
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
                return text_content.strip()
                
            except Exception:
                # Fallback to PyPDF2
                with io.BytesIO(pdf_bytes) as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
                return text_content.strip()
                
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def extract_nhs_number(self, text: str) -> Optional[str]:
        """Extract NHS number from text content"""
        try:
            for pattern in self.nhs_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Clean up the match (remove spaces, normalize format)
                    nhs_number = re.sub(r'\s+', '', str(matches[0]))
                    return nhs_number
            return None
        except Exception:
            return None
    
    def process_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Process PDF and extract information"""
        try:
            # Extract text
            text_content = self.extract_text_from_pdf_bytes(pdf_bytes)
            
            if not text_content or text_content.startswith("Error"):
                return {
                    'processing_successful': False,
                    'error': text_content
                }
            
            # Extract NHS number
            nhs_number = self.extract_nhs_number(text_content)
            
            # Basic analysis
            word_count = len(text_content.split())
            character_count = len(text_content)
            
            # Preview (first 200 characters)
            preview = text_content[:200] + "..." if len(text_content) > 200 else text_content
            
            return {
                'processing_successful': True,
                'text_content': text_content,
                'nhs_number': nhs_number,
                'word_count': word_count,
                'character_count': character_count,
                'preview': preview
            }
            
        except Exception as e:
            return {
                'processing_successful': False,
                'error': str(e)
            }
