"""
Test script for Storage Manager

This script tests the storage manager with various operations
to ensure it correctly handles data storage, retrieval, and compliance.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage_manager import get_storage_manager
from data_classifier import get_data_classifier

def test_storage_manager():
    """Test the storage manager with different operations"""
    
    print("🧪 Testing Storage Manager")
    print("=" * 50)
    
    # Create storage manager with test directory
    storage_manager = get_storage_manager("test_storage")
    
    # Test 1: Store safe clinical data
    print("\n1. Testing Safe Clinical Data Storage:")
    safe_data = {
        "analysis_id": "test-123",
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
    
    # Test 4: Retrieve non-existent data
    print("\n4. Testing Non-Existent Data Retrieval:")
    fake_storage_id = "fake_12345"
    retrieved_fake = storage_manager.retrieve_analysis_result(fake_storage_id)
    print(f"   Fake Storage ID: {fake_storage_id}")
    print(f"   Retrieved: {retrieved_fake is not None} (should be None)")
    
    # Test 5: Storage statistics
    print("\n5. Testing Storage Statistics:")
    stats = storage_manager.get_storage_stats()
    print(f"   Total Files: {stats['total_files']}")
    print(f"   Data Types: {stats['data_types']}")
    print(f"   Total Size: {stats['total_size_bytes']} bytes")
    
    # Test 6: Delete stored data (GDPR compliance)
    print("\n6. Testing Data Deletion (GDPR):")
    if storage_id:
        deleted = storage_manager.delete_analysis_result(storage_id)
        print(f"   Storage ID: {storage_id}")
        print(f"   Deleted: {deleted}")
        
        # Try to retrieve deleted data
        retrieved_after_delete = storage_manager.retrieve_analysis_result(storage_id)
        print(f"   Retrieved After Delete: {retrieved_after_delete is not None} (should be None)")
    
    # Test 7: Delete non-existent data
    print("\n7. Testing Non-Existent Data Deletion:")
    deleted_fake = storage_manager.delete_analysis_result(fake_storage_id)
    print(f"   Fake Storage ID: {fake_storage_id}")
    print(f"   Deleted: {deleted_fake} (should be False)")
    
    # Test 8: Store multiple records and test cleanup
    print("\n8. Testing Multiple Records:")
    for i in range(3):
        test_data = {
            "analysis_id": f"test-multi-{i}",
            "urgency_level": "medium",
            "care_level": "ward",
            "confidence_score": 0.75 + (i * 0.05),
            "processing_time": 1.0 + (i * 0.1),
            "model_used": "gpt-3.5-turbo",
            "risk_factors": [f"factor_{i}"],
            "recommendations": [f"recommendation_{i}"]
        }
        storage_id = storage_manager.store_analysis_result(test_data)
        print(f"   Stored record {i+1}: {storage_id}")
    
    # Get updated stats
    stats_after_multi = storage_manager.get_storage_stats()
    print(f"   Total Files After Multiple: {stats_after_multi['total_files']}")
    
    # Test 9: Audit trail verification
    print("\n9. Testing Audit Trail:")
    audit_dir = storage_manager.storage_dir / "audit_logs"
    if audit_dir.exists():
        audit_files = list(audit_dir.glob("*.json"))
        print(f"   Audit Files: {len(audit_files)}")
        if audit_files:
            print(f"   Latest Audit File: {audit_files[-1].name}")
    
    print("\n" + "=" * 50)
    print("✅ Storage Manager Tests Complete!")
    
    # Cleanup test storage
    print("\n🧹 Cleaning up test storage...")
    import shutil
    if storage_manager.storage_dir.exists():
        shutil.rmtree(storage_manager.storage_dir)
        print("   Test storage cleaned up")

def test_storage_integration():
    """Test integration between data classifier and storage manager"""
    
    print("\n🔗 Testing Data Classifier + Storage Manager Integration")
    print("=" * 60)
    
    storage_manager = get_storage_manager("test_integration")
    classifier = get_data_classifier()
    
    # Test data that should be classified and stored
    test_cases = [
        {
            "name": "Clinical Output",
            "data": {
                "urgency_level": "high",
                "care_level": "ward",
                "confidence_score": 0.85,
                "processing_time": 1.5,
                "model_used": "gpt-3.5-turbo",
                "risk_factors": ["fever", "infection"],
                "recommendations": ["antibiotics", "monitoring"]
            }
        },
        {
            "name": "System Metadata",
            "data": {
                "analysis_id": "meta-123",
                "timestamp": "2025-08-11T14:30:00Z",
                "processing_time": 0.8,
                "model_used": "gpt-3.5-turbo",
                "created_at": "2025-08-11T14:30:00Z"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        
        # Step 1: Classify data
        classification = classifier.classify_analysis_data(test_case['data'])
        print(f"   Classification: {classification.data_type}")
        print(f"   Can Store: {classification.can_store}")
        
        # Step 2: Store data
        storage_id = storage_manager.store_analysis_result(test_case['data'])
        print(f"   Storage ID: {storage_id}")
        print(f"   Stored Successfully: {storage_id is not None}")
        
        # Step 3: Verify storage matches classification
        if storage_id:
            retrieved = storage_manager.retrieve_analysis_result(storage_id)
            if retrieved:
                stored_classification = retrieved.get('classification', {})
                print(f"   Stored Classification: {stored_classification.get('data_type')}")
                print(f"   Classification Match: {stored_classification.get('data_type') == classification.data_type}")
    
    # Cleanup
    import shutil
    if storage_manager.storage_dir.exists():
        shutil.rmtree(storage_manager.storage_dir)

if __name__ == "__main__":
    test_storage_manager()
    test_storage_integration()
