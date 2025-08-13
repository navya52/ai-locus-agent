"""
PDF Processor for Clinical Letters

This module handles PDF processing, text extraction, and NHS number detection
for clinical letters in the AI Locus Agent system.
"""

import re
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import PyPDF2
import pdfplumber

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF processing and data extraction from clinical letters"""
    
    def __init__(self):
        # NHS number regex pattern (10 digits, may have spaces)
        self.nhs_pattern = re.compile(r'\b\d{3}\s*\d{3}\s*\d{4}\b')
        
        # Alternative NHS patterns (with or without spaces)
        self.nhs_patterns = [
            r'\b\d{3}\s*\d{3}\s*\d{4}\b',  # Standard format: 123 456 7890
            r'\b\d{10}\b',                  # No spaces: 1234567890
            r'\bNHS\s*Number[:\s]*(\d{3}\s*\d{3}\s*\d{4})\b',  # With "NHS Number:" prefix
            r'\bNHS\s*No[:\s]*(\d{3}\s*\d{3}\s*\d{4})\b',     # With "NHS No:" prefix
        ]
        
        logger.info("PDF Processor initialized")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text_content = ""
            
            # Try pdfplumber first (better for complex layouts)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
                
                logger.info(f"Successfully extracted text using pdfplumber from {pdf_path}")
                return text_content.strip()
                
            except Exception as e:
                logger.warning(f"pdfplumber failed, trying PyPDF2: {e}")
                
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
                
                logger.info(f"Successfully extracted text using PyPDF2 from {pdf_path}")
                return text_content.strip()
                
        except Exception as e:
            logger.error(f"Failed to extract text from PDF {pdf_path}: {e}")
            raise ValueError(f"Could not extract text from PDF: {str(e)}")
    
    def extract_nhs_number(self, text: str) -> Optional[str]:
        """
        Extract NHS number from text content
        
        Args:
            text: Text content to search
            
        Returns:
            NHS number if found, None otherwise
        """
        try:
            # Try all patterns
            for pattern in self.nhs_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Clean up the match (remove spaces, normalize format)
                    nhs_number = re.sub(r'\s+', '', str(matches[0]))
                    logger.info(f"Found NHS number: {nhs_number}")
                    return nhs_number
            
            logger.warning("No NHS number found in text")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting NHS number: {e}")
            return None
    
    def process_clinical_letter(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a clinical letter PDF and extract key information
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted data
        """
        try:
            # Extract text from PDF
            text_content = self.extract_text_from_pdf(pdf_path)
            
            if not text_content:
                raise ValueError("No text content extracted from PDF")
            
            # Extract NHS number
            nhs_number = self.extract_nhs_number(text_content)
            
            # Basic text analysis
            word_count = len(text_content.split())
            character_count = len(text_content)
            
            # Extract first few lines as preview
            lines = text_content.split('\n')
            preview = '\n'.join(lines[:5]) if lines else ""
            
            result = {
                'text_content': text_content,
                'nhs_number': nhs_number,
                'word_count': word_count,
                'character_count': character_count,
                'preview': preview,
                'processing_successful': True
            }
            
            logger.info(f"Successfully processed clinical letter: {word_count} words, NHS: {nhs_number}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to process clinical letter {pdf_path}: {e}")
            return {
                'text_content': "",
                'nhs_number': None,
                'word_count': 0,
                'character_count': 0,
                'preview': "",
                'processing_successful': False,
                'error': str(e)
            }

def get_pdf_processor() -> PDFProcessor:
    """Factory function to create PDF processor"""
    return PDFProcessor()

