"""
Test script for PDF Processor

This script tests the PDF processing functionality with the sample clinical letter.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_processor import get_pdf_processor

def test_pdf_processing():
    """Test PDF processing with sample letter"""
    print("🧪 Testing PDF Processor...")
    
    # Initialize processor
    processor = get_pdf_processor()
    
    # Test with sample letter
    sample_path = "../sample_data/Sample Letter 1.pdf"
    
    if not os.path.exists(sample_path):
        print(f"❌ Sample letter not found at: {sample_path}")
        return False
    
    print(f"📄 Processing: {sample_path}")
    
    try:
        # Process the clinical letter
        result = processor.process_clinical_letter(sample_path)
        
        print("\n📊 Processing Results:")
        print(f"✅ Success: {result['processing_successful']}")
        print(f"📝 Word Count: {result['word_count']}")
        print(f"🔢 Character Count: {result['character_count']}")
        print(f"🏥 NHS Number: {result['nhs_number']}")
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return False
        
        print("\n📋 Text Preview (first 5 lines):")
        print("-" * 50)
        print(result['preview'])
        print("-" * 50)
        
        print("\n🔍 NHS Number Detection:")
        if result['nhs_number']:
            print(f"✅ Found NHS Number: {result['nhs_number']}")
        else:
            print("❌ No NHS number found")
            print("🔍 Searching for any 10-digit patterns...")
            
            # Try to find any 10-digit numbers
            import re
            text = result['text_content']
            digit_patterns = re.findall(r'\b\d{10}\b', text)
            if digit_patterns:
                print(f"🔢 Found 10-digit numbers: {digit_patterns}")
            else:
                print("🔢 No 10-digit numbers found")
        
        return result['processing_successful']
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_processing()
    if success:
        print("\n✅ PDF Processor test completed successfully!")
    else:
        print("\n❌ PDF Processor test failed!")
        sys.exit(1)
