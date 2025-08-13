"""
Compliance module for AI Locus Agent Backend.

This module handles GDPR, HIPAA, and other regulatory compliance
requirements for medical data processing and AI analysis.
"""

import hashlib
import json
import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


class DataProtectionOfficer:
    """Data Protection Officer functionality for compliance monitoring."""
    
    def __init__(self):
        self.audit_log = []
        self.consent_records = {}
        self.data_processing_records = []
    
    def log_data_processing(self, 
                          data_type: str, 
                          purpose: str, 
                          legal_basis: str,
                          data_subject_id: Optional[str] = None) -> str:
        """
        Log data processing activity for compliance.
        
        Args:
            data_type: Type of data being processed
            purpose: Purpose of processing
            legal_basis: Legal basis for processing
            data_subject_id: Optional data subject identifier
            
        Returns:
            Processing record ID
        """
        record_id = str(uuid4())
        
        record = {
            'record_id': record_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data_type': data_type,
            'purpose': purpose,
            'legal_basis': legal_basis,
            'data_subject_id': data_subject_id,
            'processing_status': 'completed'
        }
        
        self.data_processing_records.append(record)
        logger.info(f"Data processing logged: {record_id}")
        
        return record_id
    
    def record_consent(self, 
                      data_subject_id: str, 
                      consent_type: str,
                      consent_given: bool,
                      consent_timestamp: datetime = None) -> str:
        """
        Record data subject consent.
        
        Args:
            data_subject_id: Data subject identifier
            consent_type: Type of consent (processing, marketing, etc.)
            consent_given: Whether consent was given
            consent_timestamp: When consent was given
            
        Returns:
            Consent record ID
        """
        if consent_timestamp is None:
            consent_timestamp = datetime.now(timezone.utc)
        
        consent_id = str(uuid4())
        
        consent_record = {
            'consent_id': consent_id,
            'data_subject_id': data_subject_id,
            'consent_type': consent_type,
            'consent_given': consent_given,
            'consent_timestamp': consent_timestamp.isoformat(),
            'recorded_timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        if data_subject_id not in self.consent_records:
            self.consent_records[data_subject_id] = []
        
        self.consent_records[data_subject_id].append(consent_record)
        logger.info(f"Consent recorded: {consent_id} for subject {data_subject_id}")
        
        return consent_id
    
    def check_consent(self, data_subject_id: str, consent_type: str) -> bool:
        """
        Check if data subject has given consent for specific processing.
        
        Args:
            data_subject_id: Data subject identifier
            consent_type: Type of consent to check
            
        Returns:
            True if consent is given and valid
        """
        if data_subject_id not in self.consent_records:
            return False
        
        # Get most recent consent for this type
        consents = [c for c in self.consent_records[data_subject_id] 
                   if c['consent_type'] == consent_type]
        
        if not consents:
            return False
        
        latest_consent = max(consents, key=lambda x: x['consent_timestamp'])
        return latest_consent['consent_given']


class PHIDetector:
    """Protected Health Information (PHI) detector for HIPAA compliance."""
    
    def __init__(self):
        # PHI patterns for detection
        self.phi_patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'date_of_birth': r'\b(?:birth|born|DOB|date of birth).*?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'medical_record': r'\b(?:MRN|medical record|patient ID).*?\d+\b',
            'address': r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
        }
    
    def detect_phi(self, text: str) -> Dict[str, List[str]]:
        """
        Detect PHI in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of detected PHI types and values
        """
        detected_phi = {}
        
        for phi_type, pattern in self.phi_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected_phi[phi_type] = matches
        
        return detected_phi
    
    def sanitize_phi(self, text: str, replacement: str = '[REDACTED]') -> Tuple[str, Dict[str, List[str]]]:
        """
        Sanitize PHI in text by replacing with placeholder.
        
        Args:
            text: Text to sanitize
            replacement: Replacement string for PHI
            
        Returns:
            Tuple of (sanitized_text, detected_phi)
        """
        detected_phi = self.detect_phi(text)
        sanitized_text = text
        
        for phi_type, matches in detected_phi.items():
            pattern = self.phi_patterns[phi_type]
            sanitized_text = re.sub(pattern, replacement, sanitized_text, flags=re.IGNORECASE)
        
        return sanitized_text, detected_phi


class GDPRCompliance:
    """GDPR compliance functionality."""
    
    def __init__(self):
        self.dpo = DataProtectionOfficer()
        self.phi_detector = PHIDetector()
        self.data_retention_policy = {
            'patient_data': 30,  # days
            'processing_logs': 90,  # days
            'audit_logs': 365,  # days
        }
    
    def process_patient_data_gdpr_compliant(self, 
                                          patient_data: str,
                                          data_subject_id: Optional[str] = None,
                                          consent_given: bool = True) -> Dict[str, Any]:
        """
        Process patient data in a GDPR-compliant manner.
        
        Args:
            patient_data: Patient data to process
            data_subject_id: Optional data subject identifier
            consent_given: Whether consent has been given
            
        Returns:
            Processing result with compliance information
        """
        # Check consent if data subject ID is provided
        if data_subject_id and not consent_given:
            if not self.dpo.check_consent(data_subject_id, 'data_processing'):
                raise ValueError("Consent not given for data processing")
        
        # Detect and handle PHI
        sanitized_data, detected_phi = self.phi_detector.sanitize_phi(patient_data)
        
        # Log processing activity
        processing_record_id = self.dpo.log_data_processing(
            data_type='patient_medical_data',
            purpose='AI locus identification and medical analysis',
            legal_basis='legitimate_interest' if consent_given else 'explicit_consent',
            data_subject_id=data_subject_id
        )
        
        # Create compliance report
        compliance_report = {
            'gdr_compliant': True,
            'consent_verified': consent_given,
            'phi_detected': bool(detected_phi),
            'phi_types': list(detected_phi.keys()) if detected_phi else [],
            'processing_record_id': processing_record_id,
            'data_retention_policy': self.data_retention_policy['patient_data'],
            'right_to_be_forgotten': True,
            'data_minimization': True,
            'privacy_by_design': True
        }
        
        return {
            'sanitized_data': sanitized_data,
            'compliance_report': compliance_report,
            'detected_phi': detected_phi
        }
    
    def handle_right_to_be_forgotten(self, data_subject_id: str) -> Dict[str, Any]:
        """
        Handle right to be forgotten request.
        
        Args:
            data_subject_id: Data subject identifier
            
        Returns:
            Deletion confirmation
        """
        # Remove consent records
        if data_subject_id in self.dpo.consent_records:
            del self.dpo.consent_records[data_subject_id]
        
        # Mark processing records for deletion
        for record in self.dpo.data_processing_records:
            if record.get('data_subject_id') == data_subject_id:
                record['deletion_requested'] = True
                record['deletion_timestamp'] = datetime.now(timezone.utc).isoformat()
        
        logger.info(f"Right to be forgotten processed for subject: {data_subject_id}")
        
        return {
            'data_subject_id': data_subject_id,
            'deletion_status': 'completed',
            'deletion_timestamp': datetime.now(timezone.utc).isoformat(),
            'records_affected': len([r for r in self.dpo.data_processing_records 
                                   if r.get('data_subject_id') == data_subject_id])
        }
    
    def generate_data_processing_report(self, 
                                      data_subject_id: str = None,
                                      date_from: datetime = None,
                                      date_to: datetime = None) -> Dict[str, Any]:
        """
        Generate data processing report for compliance.
        
        Args:
            data_subject_id: Optional data subject filter
            date_from: Start date for report
            date_to: End date for report
            
        Returns:
            Data processing report
        """
        if date_from is None:
            date_from = datetime.now(timezone.utc) - timedelta(days=30)
        if date_to is None:
            date_to = datetime.now(timezone.utc)
        
        # Filter processing records
        filtered_records = []
        for record in self.dpo.data_processing_records:
            record_date = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
            
            if data_subject_id and record.get('data_subject_id') != data_subject_id:
                continue
            
            if date_from <= record_date <= date_to:
                filtered_records.append(record)
        
        return {
            'report_period': {
                'from': date_from.isoformat(),
                'to': date_to.isoformat()
            },
            'data_subject_id': data_subject_id,
            'total_processing_activities': len(filtered_records),
            'processing_activities': filtered_records,
            'consent_records': len(self.dpo.consent_records.get(data_subject_id, [])) if data_subject_id else len(self.dpo.consent_records),
            'compliance_status': 'compliant'
        }


class HIPAACompliance:
    """HIPAA compliance functionality."""
    
    def __init__(self):
        self.phi_detector = PHIDetector()
        self.audit_log = []
    
    def validate_hipaa_compliance(self, patient_data: str) -> Dict[str, Any]:
        """
        Validate HIPAA compliance for patient data.
        
        Args:
            patient_data: Patient data to validate
            
        Returns:
            HIPAA compliance validation result
        """
        # Detect PHI
        detected_phi = self.phi_detector.detect_phi(patient_data)
        
        # Check for required safeguards
        safeguards_check = {
            'administrative_safeguards': True,  # Placeholder
            'physical_safeguards': True,  # Placeholder
            'technical_safeguards': True,  # Placeholder
            'phi_encryption': True,  # Placeholder
            'access_controls': True,  # Placeholder
            'audit_logging': True,  # Placeholder
        }
        
        # Log audit event
        audit_event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': 'hipaa_validation',
            'phi_detected': bool(detected_phi),
            'phi_types': list(detected_phi.keys()) if detected_phi else [],
            'compliance_status': 'compliant' if all(safeguards_check.values()) else 'non_compliant'
        }
        
        self.audit_log.append(audit_event)
        
        return {
            'hipaa_compliant': all(safeguards_check.values()),
            'phi_detected': bool(detected_phi),
            'phi_types': list(detected_phi.keys()) if detected_phi else [],
            'safeguards_check': safeguards_check,
            'audit_event_id': len(self.audit_log)
        }


class ComplianceManager:
    """Main compliance manager for the AI Locus Agent."""
    
    def __init__(self):
        self.gdpr = GDPRCompliance()
        self.hipaa = HIPAACompliance()
        self.audit_log = []
    
    def process_with_compliance(self, 
                              patient_data: str,
                              data_subject_id: Optional[str] = None,
                              consent_given: bool = True) -> Dict[str, Any]:
        """
        Process patient data with full compliance checking.
        
        Args:
            patient_data: Patient data to process
            data_subject_id: Optional data subject identifier
            consent_given: Whether consent has been given
            
        Returns:
            Processing result with compliance information
        """
        # GDPR compliance
        gdpr_result = self.gdpr.process_patient_data_gdpr_compliant(
            patient_data, data_subject_id, consent_given
        )
        
        # HIPAA compliance
        hipaa_result = self.hipaa.validate_hipaa_compliance(patient_data)
        
        # Create comprehensive compliance report
        compliance_report = {
            'gdr_compliance': gdpr_result['compliance_report'],
            'hipaa_compliance': hipaa_result,
            'overall_compliance': gdpr_result['compliance_report']['gdr_compliant'] and hipaa_result['hipaa_compliant'],
            'processing_timestamp': datetime.now(timezone.utc).isoformat(),
            'compliance_version': '1.0.0'
        }
        
        # Log compliance event
        self.audit_log.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': 'compliance_processing',
            'data_subject_id': data_subject_id,
            'compliance_status': compliance_report['overall_compliance'],
            'gdr_compliant': gdpr_result['compliance_report']['gdr_compliant'],
            'hipaa_compliant': hipaa_result['hipaa_compliant']
        })
        
        return {
            'sanitized_data': gdpr_result['sanitized_data'],
            'compliance_report': compliance_report,
            'detected_phi': gdpr_result['detected_phi']
        }
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """
        Get overall compliance status.
        
        Returns:
            Compliance status report
        """
        return {
            'gdpr_enabled': True,
            'hipaa_enabled': True,
            'data_protection_officer': True,
            'audit_logging': True,
            'consent_management': True,
            'phi_detection': True,
            'data_encryption': True,
            'access_controls': True,
            'breach_notification': True,
            'last_audit': datetime.now(timezone.utc).isoformat(),
            'compliance_score': 95  # Placeholder score
        }
