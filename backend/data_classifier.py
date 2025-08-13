"""
Data Classification System for AI Locus Agent

This module classifies patient data to determine what can be safely stored
while maintaining GDPR and healthcare compliance.
"""

import hashlib
import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class DataClassification:
    """Classification result for data storage decisions"""
    can_store: bool
    data_type: str
    sensitivity_level: str
    retention_days: int
    requires_consent: bool
    audit_required: bool
    reason: str

class DataClassifier:
    """Classifies data for storage compliance"""
    
    def __init__(self):
        # Define what we consider sensitive vs safe to store
        self.sensitive_indicators = [
            "name", "address", "phone", "email", "nhs_number",
            "date_of_birth", "postcode", "full_name"
        ]
        
        self.clinical_indicators = [
            "symptoms", "diagnosis", "treatment", "medication",
            "vital_signs", "lab_results", "medical_history"
        ]
        
        self.safe_metadata = [
            "timestamp", "processing_time", "model_used", 
            "confidence_score", "urgency_level", "care_level"
        ]
    
    def classify_analysis_data(self, analysis_result: Dict[str, Any]) -> DataClassification:
        """
        Classify AI analysis results for storage
        
        Args:
            analysis_result: The AI analysis output
            
        Returns:
            DataClassification with storage recommendations
        """
        logger.info("Classifying analysis data for storage compliance")
        
        # Check if this contains sensitive patient data
        if self._contains_sensitive_data(analysis_result):
            return DataClassification(
                can_store=False,
                data_type="sensitive_patient_data",
                sensitivity_level="high",
                retention_days=0,
                requires_consent=True,
                audit_required=True,
                reason="Contains sensitive patient information"
            )
        
        # Check if this is clinical output (safe to store)
        if self._is_clinical_output(analysis_result):
            return DataClassification(
                can_store=True,
                data_type="clinical_output",
                sensitivity_level="low",
                retention_days=30,
                requires_consent=False,
                audit_required=True,
                reason="Clinical analysis results without patient identifiers"
            )
        
        # Check if this is metadata (safe to store)
        if self._is_metadata(analysis_result):
            return DataClassification(
                can_store=True,
                data_type="analysis_metadata",
                sensitivity_level="none",
                retention_days=90,
                requires_consent=False,
                audit_required=False,
                reason="System metadata for performance monitoring"
            )
        
        # Default: don't store if unsure
        return DataClassification(
            can_store=False,
            data_type="unknown",
            sensitivity_level="unknown",
            retention_days=0,
            requires_consent=True,
            audit_required=True,
            reason="Unknown data type - defaulting to no storage for safety"
        )
    
    def _contains_sensitive_data(self, data: Dict[str, Any]) -> bool:
        """Check if data contains sensitive patient information"""
        data_str = str(data).lower()
        
        for indicator in self.sensitive_indicators:
            if indicator in data_str:
                logger.warning(f"Sensitive data detected: {indicator}")
                return True
        
        return False
    
    def _is_clinical_output(self, data: Dict[str, Any]) -> bool:
        """Check if data is clinical analysis output"""
        # Look for clinical analysis fields
        clinical_fields = [
            "urgency_level", "care_level", "risk_factors", 
            "recommendations", "confidence_score"
        ]
        
        return any(field in data for field in clinical_fields)
    
    def _is_metadata(self, data: Dict[str, Any]) -> bool:
        """Check if data is system metadata"""
        metadata_fields = [
            "processing_time", "model_used", "timestamp", 
            "analysis_id", "created_at"
        ]
        
        return any(field in data for field in metadata_fields)
    
    def create_safe_storage_data(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a safe version of data for storage
        
        Args:
            analysis_result: Original analysis result
            
        Returns:
            Dict containing only safe-to-store data
        """
        safe_data = {
            "analysis_id": analysis_result.get("analysis_id"),
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time": analysis_result.get("processing_time"),
            "model_used": analysis_result.get("model_used"),
            "confidence_score": analysis_result.get("confidence_score"),
            "urgency_level": analysis_result.get("urgency_level"),
            "care_level": analysis_result.get("care_level"),
            "data_hash": self._create_data_hash(analysis_result)
        }
        
        # Only include clinical outputs (no patient data)
        if "risk_factors" in analysis_result:
            safe_data["risk_factors"] = analysis_result["risk_factors"]
        
        if "recommendations" in analysis_result:
            safe_data["recommendations"] = analysis_result["recommendations"]
        
        # Remove any None values
        return {k: v for k, v in safe_data.items() if v is not None}
    
    def _create_data_hash(self, data: Dict[str, Any]) -> str:
        """Create a hash of the original data for audit purposes"""
        data_str = str(sorted(data.items()))
        return hashlib.sha256(data_str.encode()).hexdigest()

def get_data_classifier() -> DataClassifier:
    """Factory function to create data classifier"""
    return DataClassifier()
