"""
Test script for AWS Storage Manager

This script tests the AWS S3 and DynamoDB integration
to ensure it correctly handles data storage and retrieval.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aws_storage_manager import get_aws_storage_manager

def test_aws_storage():
    """Test the AWS storage manager with different operations"""
    
    print("☁️ Testing AWS Storage Manager")
    print("=" * 50)
    
    try:
        # Create AWS storage manager
        storage_manager = get_aws_storage_manager()
        print("✅ AWS Storage Manager initialized successfully")
        
        # Test 1: Store safe clinical data
        print("\n1. Testing Safe Clinical Data Storage:")
        safe_data = {
            "analysis_id": "test-aws-123",
            "urgency_level": "urgent",
            "care_level": "hdu",
            "confidence_score": 0.89,
            "processing_time": 1.2,
            "model_used": "gpt-3.5-turbo",
            "risk_factors": ["chest pain", "hypertension"],
            "recommendations": ["immediate assessment", "cardiac monitoring"]
        }
        
        storage_id = storage_manager.store_analysis_result(safe_data)
        print(f"   Input Data: {safe_data}")
        print(f"   Storage ID: {storage_id}")
        print(f"   Success: {storage_id is not None}")
        
        # Test 2: Store sensitive data (should not store)
        print("\n2. Testing Sensitive Data Storage:")
        sensitive_data = {
            "patient_name": "John Smith",
            "nhs_number": "1234567890",
            "symptoms": "chest pain",
            "urgency_level": "urgent"
        }
        
        storage_id_sensitive = storage_manager.store_analysis_result(sensitive_data)
        print(f"   Input Data: {sensitive_data}")
        print(f"   Storage ID: {storage_id_sensitive}")
        print(f"   Success: {storage_id_sensitive is None} (should be None)")
        
        # Test 3: Retrieve stored data
        print("\n3. Testing Data Retrieval:")
        if storage_id:
            retrieved_data = storage_manager.retrieve_analysis_result(storage_id)
            print(f"   Storage ID: {storage_id}")
            print(f"   Retrieved: {retrieved_data is not None}")
            if retrieved_data:
                print(f"   Data Keys: {list(retrieved_data.keys())}")
                print(f"   Classification: {retrieved_data.get('classification', 'N/A')}")
        
        # Test 4: Storage statistics
        print("\n4. Testing Storage Statistics:")
        stats = storage_manager.get_storage_stats()
        print(f"   Storage Type: {stats.get('storage_type', 'unknown')}")
        print(f"   Total Files: {stats.get('total_files', 0)}")
        print(f"   Data Types: {stats.get('data_types', {})}")
        print(f"   DynamoDB Items: {stats.get('dynamodb_items', 0)}")
        
        # Test 5: Delete stored data (GDPR compliance)
        print("\n5. Testing Data Deletion (GDPR):")
        if storage_id:
            deleted = storage_manager.delete_analysis_result(storage_id)
            print(f"   Storage ID: {storage_id}")
            print(f"   Deleted: {deleted}")
            
            # Try to retrieve deleted data
            retrieved_after_delete = storage_manager.retrieve_analysis_result(storage_id)
            print(f"   Retrieved After Delete: {retrieved_after_delete is not None} (should be None)")
        
        print("\n" + "=" * 50)
        print("✅ AWS Storage Tests Complete!")
        
    except Exception as e:
        print(f"❌ AWS Storage Test Failed: {e}")
        print("\nThis might be due to:")
        print("- AWS credentials not configured")
        print("- S3 bucket or DynamoDB table not created")
        print("- Network connectivity issues")
        print("- AWS permissions not set up")

def test_aws_connectivity():
    """Test basic AWS connectivity"""
    
    print("\n🔗 Testing AWS Connectivity")
    print("=" * 30)
    
    try:
        import boto3
        
        # Test S3 connectivity
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        print(f"✅ S3 Connectivity: {len(response['Buckets'])} buckets found")
        
        # Test DynamoDB connectivity
        dynamodb = boto3.resource('dynamodb')
        tables = list(dynamodb.tables.all())
        print(f"✅ DynamoDB Connectivity: {len(tables)} tables found")
        
        return True
        
    except Exception as e:
        print(f"❌ AWS Connectivity Failed: {e}")
        return False

if __name__ == "__main__":
    # First test connectivity
    if test_aws_connectivity():
        # Then test storage functionality
        test_aws_storage()
    else:
        print("\n⚠️  AWS not configured. Please set up:")
        print("1. AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
        print("2. S3 bucket: ai-locus-agent-storage")
        print("3. DynamoDB table: ai-locus-agent-analyses")
        print("4. Proper IAM permissions")
