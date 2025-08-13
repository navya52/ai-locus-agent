"""
Test script for the upload letter endpoint

This script tests the new /api/v1/upload-letter endpoint
with the sample clinical letter.
"""

import requests
import os
import sys

def test_upload_endpoint():
    """Test the upload letter endpoint"""
    print("🧪 Testing Upload Letter Endpoint...")
    
    # Endpoint URL
    url = "http://localhost:5002/api/v1/upload-letter"
    
    # Sample letter path
    sample_path = "../sample_data/Sample Letter 1.pdf"
    
    if not os.path.exists(sample_path):
        print(f"❌ Sample letter not found at: {sample_path}")
        return False
    
    try:
        # Prepare the file for upload
        with open(sample_path, 'rb') as file:
            files = {'file': ('Sample Letter 1.pdf', file, 'application/pdf')}
            
            print(f"📤 Uploading: {sample_path}")
            print(f"🌐 Endpoint: {url}")
            
            # Make the request
            response = requests.post(url, files=files, timeout=30)
            
            print(f"\n📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Upload successful!")
                
                print(f"\n📋 File Info:")
                print(f"   Filename: {data['file_info']['filename']}")
                print(f"   Word Count: {data['file_info']['word_count']}")
                print(f"   Character Count: {data['file_info']['character_count']}")
                
                print(f"\n🏥 Extracted Data:")
                print(f"   NHS Number: {data['extracted_data']['nhs_number']}")
                print(f"   Text Preview: {data['extracted_data']['text_preview'][:100]}...")
                
                print(f"\n🤖 AI Summary:")
                if 'ai_summary' in data:
                    ai_data = data['ai_summary']
                    print(f"   Risk Level: {ai_data.get('risk_level', 'N/A')}")
                    print(f"   Clinical Summary: {ai_data.get('clinical_summary', 'N/A')[:100]}...")
                    print(f"   Recommended Actions: {ai_data.get('recommended_actions', 'N/A')[:100]}...")
                
                print(f"\n💾 Storage Info:")
                print(f"   Storage ID: {data['storage_info']['storage_id']}")
                print(f"   Storage Status: {data['storage_info']['storage_status']}")
                
                return True
            else:
                print(f"❌ Upload failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the backend running on port 5002?")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_upload_endpoint()
    if success:
        print("\n✅ Upload endpoint test completed successfully!")
    else:
        print("\n❌ Upload endpoint test failed!")
        sys.exit(1)

