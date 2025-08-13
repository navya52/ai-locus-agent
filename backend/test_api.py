"""
Test suite for AI Locus Agent Flask Backend

This module provides comprehensive testing for the AI locus agent API,
including patient data processing, error handling, and compliance features.
"""

import json
import sys
from datetime import datetime
from typing import Dict, Any, List

import requests


class APITester:
    """Test suite for AI Locus Agent API endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the API tester.
        
        Args:
            base_url: Base URL for the API server
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Locus-Agent-Test-Suite/1.0'
        })
        
    def test_patient_data_processing(self) -> None:
        """
        Test patient data processing with various medical scenarios.
        
        Tests different types of patient data to ensure proper
        processing and AI analysis functionality.
        """
        print("Testing AI Locus Agent Patient Data Processing API")
        print("=" * 70)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Comprehensive test cases for medical scenarios
        test_cases = [
            {
                "description": "Chest pain symptoms (cardiac)",
                "patient_data": (
                    "Patient presents with acute chest pain, shortness of breath, "
                    "and sweating. History of hypertension and diabetes. "
                    "Pain radiates to left arm. Duration: 30 minutes."
                ),
                "expected_risk": "high"
            },
            {
                "description": "Neurological symptoms (stroke)",
                "patient_data": (
                    "Patient reports severe headache, confusion, and difficulty "
                    "speaking. No history of migraines. Symptoms started 2 hours ago. "
                    "Right-sided weakness noted."
                ),
                "expected_risk": "high"
            },
            {
                "description": "Gastrointestinal issues (appendicitis)",
                "patient_data": (
                    "Patient complains of abdominal pain, nausea, and vomiting "
                    "for the past 24 hours. No fever. Pain is localized to "
                    "right lower quadrant. No previous similar episodes."
                ),
                "expected_risk": "medium"
            },
            {
                "description": "Respiratory symptoms (pneumonia)",
                "patient_data": (
                    "Patient has persistent cough, fever of 101.5°F, and fatigue "
                    "for 5 days. No shortness of breath. No recent travel history. "
                    "Productive cough with yellow sputum."
                ),
                "expected_risk": "medium"
            },
            {
                "description": "Chronic conditions exacerbation",
                "patient_data": (
                    "Patient with history of COPD, heart failure, and diabetes. "
                    "Currently experiencing increased dyspnea and ankle swelling. "
                    "Blood pressure elevated at 160/95. Weight gain of 5 lbs in 1 week."
                ),
                "expected_risk": "medium"
            },
            {
                "description": "Minor symptoms (low risk)",
                "patient_data": (
                    "Patient reports mild headache and fatigue for 2 days. "
                    "No fever, no neurological symptoms. History of tension headaches. "
                    "Stressful week at work."
                ),
                "expected_risk": "low"
            }
        ]
        
        successful_tests = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test Case {i}/{total_tests}: {test_case['description']}")
            print("-" * 60)
            
            # Truncate patient data for display
            display_data = test_case['patient_data'][:80] + "..." if len(test_case['patient_data']) > 80 else test_case['patient_data']
            print(f"Patient Data: '{display_data}'")
            
            try:
                response = self._make_request(
                    f"{self.base_url}/api/v1/process-patient-data",
                    json={"patient_data": test_case['patient_data']}
                )
                
                if response.status_code == 200:
                    successful_tests += 1
                    result = response.json()
                    print(f"✅ Status: {response.status_code} - SUCCESS")
                    print(f"   Processing Time: {result.get('processing_time_seconds', 'N/A')}s")
                    print(f"   AI Confidence: {result.get('ai_analysis', {}).get('confidence_score', 'N/A')}")
                    print(f"   Risk Level: {result.get('ai_analysis', {}).get('risk_level', 'N/A')}")
                else:
                    print(f"❌ Status: {response.status_code} - FAILED")
                    print(f"   Error: {response.json().get('message', 'Unknown error')}")
                
            except requests.exceptions.ConnectionError:
                print("❌ Connection Error: Could not connect to the server.")
                print("   Make sure the Flask app is running with: python app.py")
                break
            except Exception as e:
                print(f"❌ Unexpected Error: {e}")
            
            print()  # Add spacing between test cases
        
        print(f"Test Results: {successful_tests}/{total_tests} tests passed")
        print("=" * 70)
    
    def test_error_scenarios(self) -> None:
        """
        Test various error scenarios to ensure proper error handling.
        
        Validates that the API properly handles invalid inputs,
        missing data, and other error conditions.
        """
        print("Testing Error Scenarios")
        print("=" * 70)
        
        error_tests = [
            {
                "description": "Missing patient_data field",
                "payload": {"wrong_field": "some data"},
                "expected_status": 400
            },
            {
                "description": "Empty JSON body",
                "payload": {},
                "expected_status": 400
            },
            {
                "description": "Empty patient data",
                "payload": {"patient_data": ""},
                "expected_status": 400
            },
            {
                "description": "Whitespace-only patient data",
                "payload": {"patient_data": "   "},
                "expected_status": 400
            },
            {
                "description": "Non-string patient data",
                "payload": {"patient_data": 123},
                "expected_status": 400
            },
            {
                "description": "Excessively long patient data",
                "payload": {"patient_data": "A" * 15000},  # Exceeds 10k limit
                "expected_status": 400
            }
        ]
        
        successful_error_tests = 0
        total_error_tests = len(error_tests)
        
        for i, test_case in enumerate(error_tests, 1):
            print(f"Error Test {i}/{total_error_tests}: {test_case['description']}")
            print("-" * 50)
            
            try:
                response = self._make_request(
                    f"{self.base_url}/api/v1/process-patient-data",
                    json=test_case['payload']
                )
                
                if response.status_code == test_case['expected_status']:
                    successful_error_tests += 1
                    print(f"✅ Status: {response.status_code} - EXPECTED")
                    error_msg = response.json().get('message', 'No error message')
                    print(f"   Error Message: {error_msg}")
                else:
                    print(f"❌ Status: {response.status_code} - UNEXPECTED")
                    print(f"   Expected: {test_case['expected_status']}")
                
            except Exception as e:
                print(f"❌ Test Error: {e}")
            
            print()
        
        print(f"Error Test Results: {successful_error_tests}/{total_error_tests} tests passed")
        print("=" * 70)
    
    def test_health_endpoints(self) -> None:
        """
        Test health and status endpoints for monitoring.
        
        Validates that health check and status endpoints
        return proper information for system monitoring.
        """
        print("Testing Health and Status Endpoints")
        print("=" * 70)
        
        health_endpoints = [
            {
                "name": "Health Check",
                "url": f"{self.base_url}/api/v1/health",
                "method": "GET"
            },
            {
                "name": "Status Check",
                "url": f"{self.base_url}/api/v1/status",
                "method": "GET"
            }
        ]
        
        for endpoint in health_endpoints:
            print(f"Testing {endpoint['name']}: {endpoint['url']}")
            print("-" * 50)
            
            try:
                response = self._make_request(endpoint['url'])
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Status: {response.status_code} - HEALTHY")
                    print(f"   Service: {result.get('service', 'N/A')}")
                    print(f"   Version: {result.get('version', 'N/A')}")
                    print(f"   Timestamp: {result.get('timestamp', 'N/A')}")
                else:
                    print(f"❌ Status: {response.status_code} - UNHEALTHY")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
    
    def _make_request(self, url: str, **kwargs) -> requests.Response:
        """
        Make HTTP request with proper error handling.
        
        Args:
            url: Target URL
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        try:
            return self.session.request('POST' if 'json' in kwargs else 'GET', url, **kwargs)
        except requests.exceptions.RequestException as e:
            raise e


def main():
    """Main test execution function."""
    print("AI Locus Agent API Test Suite")
    print("=" * 70)
    
    # Initialize tester
    tester = APITester()
    
    try:
        # Run all test suites
        tester.test_health_endpoints()
        tester.test_patient_data_processing()
        tester.test_error_scenarios()
        
        print("🎉 All tests completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
