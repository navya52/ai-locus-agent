"""
Test script for Frontend Integration

This script tests the complete frontend-backend integration
for the clinical letter upload functionality.
"""

import requests
import os
import sys

def test_frontend_integration():
    """Test the complete frontend-backend integration"""
    print("🧪 Testing Frontend-Backend Integration...")
    
    # Test frontend is accessible
    try:
        frontend_response = requests.get('http://localhost:3000', timeout=5)
        print(f"✅ Frontend accessible: {frontend_response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        return False
    
    # Test backend is accessible
    try:
        backend_response = requests.get('http://localhost:5002/api/v1/health', timeout=5)
        print(f"✅ Backend accessible: {backend_response.status_code}")
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False
    
    # Test upload endpoint with sample letter
    sample_path = "../sample_data/Sample Letter 1.pdf"
    
    if not os.path.exists(sample_path):
        print(f"❌ Sample letter not found at: {sample_path}")
        return False
    
    try:
        with open(sample_path, 'rb') as file:
            files = {'file': ('Sample Letter 1.pdf', file, 'application/pdf')}
            
            print("📤 Testing file upload...")
            response = requests.post('http://localhost:5002/api/v1/upload-letter', files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Upload successful!")
                
                print(f"\n📋 Integration Test Results:")
                print(f"   Status: {data['status']}")
                print(f"   NHS Number: {data['extracted_data']['nhs_number']}")
                print(f"   AI Summary: {data['ai_summary']['summary'][:100]}...")
                print(f"   Storage Status: {data['storage_info']['storage_status']}")
                
                return True
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend_integration()
    if success:
        print("\n✅ Frontend-Backend integration test completed successfully!")
        print("\n🌐 You can now:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Upload the sample PDF file")
        print("   3. See the AI processing results")
    else:
        print("\n❌ Frontend-Backend integration test failed!")
        sys.exit(1)

