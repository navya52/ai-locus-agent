"""
Test script for Data Classification System

This script tests the data classifier with various types of data
to ensure it correctly identifies what can be safely stored.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_classifier import get_data_classifier

def test_data_classifier():
    """Test the data classifier with different data types"""
    
    print("🧪 Testing Data Classification System")
    print("=" * 50)
    
    classifier = get_data_classifier()
    
    # Test 1: Safe clinical output (should be stored)
    print("\n1. Testing Safe Clinical Output:")
    safe_data = {
        "urgency_level": "urgent",
        "care_level": "hdu",
        "confidence_score": 0.89,
        "processing_time": 1.2,
        "model_used": "gpt-3.5-turbo",
        "risk_factors": ["chest pain", "hypertension"],
        "recommendations": ["immediate assessment", "cardiac monitoring"]
    }
    
    result = classifier.classify_analysis_data(safe_data)
    print(f"   Data: {safe_data}")
    print(f"   Can Store: {result.can_store}")
    print(f"   Data Type: {result.data_type}")
    print(f"   Reason: {result.reason}")
    
    # Test 2: Sensitive patient data (should NOT be stored)
    print("\n2. Testing Sensitive Patient Data:")
    sensitive_data = {
        "patient_name": "John Smith",
        "nhs_number": "1234567890",
        "date_of_birth": "1980-05-15",
        "symptoms": "chest pain",
        "urgency_level": "urgent"
    }
    
    result = classifier.classify_analysis_data(sensitive_data)
    print(f"   Data: {sensitive_data}")
    print(f"   Can Store: {result.can_store}")
    print(f"   Data Type: {result.data_type}")
    print(f"   Reason: {result.reason}")
    
    # Test 3: System metadata (should be stored)
    print("\n3. Testing System Metadata:")
    metadata = {
        "analysis_id": "uuid-12345",
        "timestamp": "2025-08-11T14:30:00Z",
        "processing_time": 1.2,
        "model_used": "gpt-3.5-turbo",
        "created_at": "2025-08-11T14:30:00Z"
    }
    
    result = classifier.classify_analysis_data(metadata)
    print(f"   Data: {metadata}")
    print(f"   Can Store: {result.can_store}")
    print(f"   Data Type: {result.data_type}")
    print(f"   Reason: {result.reason}")
    
    # Test 4: Unknown data (should NOT be stored)
    print("\n4. Testing Unknown Data:")
    unknown_data = {
        "random_field": "random_value",
        "unknown_type": "something_weird"
    }
    
    result = classifier.classify_analysis_data(unknown_data)
    print(f"   Data: {unknown_data}")
    print(f"   Can Store: {result.can_store}")
    print(f"   Data Type: {result.data_type}")
    print(f"   Reason: {result.reason}")
    
    # Test 5: Safe storage data creation
    print("\n5. Testing Safe Storage Data Creation:")
    original_data = {
        "analysis_id": "uuid-12345",
        "urgency_level": "urgent",
        "care_level": "hdu",
        "confidence_score": 0.89,
        "processing_time": 1.2,
        "model_used": "gpt-3.5-turbo",
        "risk_factors": ["chest pain", "hypertension"],
        "recommendations": ["immediate assessment"],
        "patient_name": "John Smith",  # This should be filtered out
        "nhs_number": "1234567890"     # This should be filtered out
    }
    
    safe_data = classifier.create_safe_storage_data(original_data)
    print(f"   Original Data: {original_data}")
    print(f"   Safe Storage Data: {safe_data}")
    
    print("\n" + "=" * 50)
    print("✅ Data Classification Tests Complete!")

if __name__ == "__main__":
    test_data_classifier()

