"""
Storage Manager for AI Locus Agent

This module handles safe storage of analysis data based on data classification.
Implements Phase 1 minimal storage with compliance features.
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
from data_classifier import DataClassifier, DataClassification

logger = logging.getLogger(__name__)

class StorageManager:
    """Manages safe storage of analysis data"""
    
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = Path(storage_dir)
        self.data_classifier = DataClassifier()
        
        # Create storage directories
        self._create_storage_directories()
        
        # Storage configuration
        self.retention_policies = {
            "clinical_output": 30,  # 30 days
            "analysis_metadata": 90,  # 90 days
            "sensitive_patient_data": 0,  # Never store
            "unknown": 0  # Never store
        }
    
    def _create_storage_directories(self):
        """Create necessary storage directories"""
        directories = [
            self.storage_dir / "clinical_output",
            self.storage_dir / "analysis_metadata",
            self.storage_dir / "audit_logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created storage directory: {directory}")
    
    def store_analysis_result(self, analysis_result: Dict[str, Any]) -> Optional[str]:
        """
        Store analysis result if it's safe to do so
        
        Args:
            analysis_result: The AI analysis result
            
        Returns:
            Storage ID if stored, None if not stored
        """
        try:
            # Classify the data
            classification = self.data_classifier.classify_analysis_data(analysis_result)
            
            # Log the classification decision
            logger.info(f"Data classification: {classification.data_type} - Can store: {classification.can_store}")
            
            if not classification.can_store:
                logger.warning(f"Not storing data: {classification.reason}")
                return None
            
            # Create safe storage data
            safe_data = self.data_classifier.create_safe_storage_data(analysis_result)
            
            # Generate storage ID
            storage_id = self._generate_storage_id()
            safe_data["storage_id"] = storage_id
            safe_data["classification"] = {
                "data_type": classification.data_type,
                "sensitivity_level": classification.sensitivity_level,
                "retention_days": classification.retention_days,
                "audit_required": classification.audit_required
            }
            
            # Store the data
            storage_path = self._get_storage_path(classification.data_type, storage_id)
            self._write_data(storage_path, safe_data)
            
            # Log audit trail
            self._log_audit_trail(storage_id, "store", classification.data_type)
            
            logger.info(f"Successfully stored analysis result: {storage_id}")
            return storage_id
            
        except Exception as e:
            logger.error(f"Error storing analysis result: {e}")
            return None
    
    def retrieve_analysis_result(self, storage_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve stored analysis result
        
        Args:
            storage_id: The storage ID
            
        Returns:
            Stored data if found, None if not found
        """
        try:
            # Search in all storage directories
            for data_type in ["clinical_output", "analysis_metadata"]:
                storage_path = self._get_storage_path(data_type, storage_id)
                if storage_path.exists():
                    data = self._read_data(storage_path)
                    
                    # Log audit trail
                    self._log_audit_trail(storage_id, "retrieve", data_type)
                    
                    logger.info(f"Retrieved analysis result: {storage_id}")
                    return data
            
            logger.warning(f"Analysis result not found: {storage_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving analysis result: {e}")
            return None
    
    def delete_analysis_result(self, storage_id: str) -> bool:
        """
        Delete stored analysis result (GDPR compliance)
        
        Args:
            storage_id: The storage ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            # Search in all storage directories
            for data_type in ["clinical_output", "analysis_metadata"]:
                storage_path = self._get_storage_path(data_type, storage_id)
                if storage_path.exists():
                    storage_path.unlink()
                    
                    # Log audit trail
                    self._log_audit_trail(storage_id, "delete", data_type)
                    
                    logger.info(f"Deleted analysis result: {storage_id}")
                    return True
            
            logger.warning(f"Analysis result not found for deletion: {storage_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting analysis result: {e}")
            return False
    
    def cleanup_expired_data(self) -> int:
        """
        Clean up expired data based on retention policies
        
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        try:
            for data_type, retention_days in self.retention_policies.items():
                if retention_days == 0:
                    continue  # Skip data types that should never be stored
                
                storage_dir = self.storage_dir / data_type
                if not storage_dir.exists():
                    continue
                
                cutoff_date = datetime.now() - timedelta(days=retention_days)
                
                for file_path in storage_dir.glob("*.json"):
                    try:
                        data = self._read_data(file_path)
                        timestamp_str = data.get("timestamp")
                        
                        if timestamp_str:
                            file_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                            
                            if file_timestamp < cutoff_date:
                                file_path.unlink()
                                deleted_count += 1
                                logger.info(f"Deleted expired file: {file_path}")
                                
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {e}")
            
            logger.info(f"Cleanup completed: {deleted_count} files deleted")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return deleted_count
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics
        
        Returns:
            Dictionary with storage statistics
        """
        stats = {
            "total_files": 0,
            "data_types": {},
            "total_size_bytes": 0
        }
        
        try:
            for data_type in ["clinical_output", "analysis_metadata"]:
                storage_dir = self.storage_dir / data_type
                if storage_dir.exists():
                    files = list(storage_dir.glob("*.json"))
                    stats["data_types"][data_type] = len(files)
                    stats["total_files"] += len(files)
                    
                    for file_path in files:
                        stats["total_size_bytes"] += file_path.stat().st_size
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return stats
    
    def _generate_storage_id(self) -> str:
        """Generate unique storage ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}"
    
    def _get_storage_path(self, data_type: str, storage_id: str) -> Path:
        """Get storage file path"""
        return self.storage_dir / data_type / f"{storage_id}.json"
    
    def _write_data(self, file_path: Path, data: Dict[str, Any]):
        """Write data to file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _read_data(self, file_path: Path) -> Dict[str, Any]:
        """Read data from file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _log_audit_trail(self, storage_id: str, action: str, data_type: str):
        """Log audit trail entry"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "storage_id": storage_id,
            "action": action,
            "data_type": data_type
        }
        
        audit_file = self.storage_dir / "audit_logs" / f"audit_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Load existing audit log or create new one
        if audit_file.exists():
            with open(audit_file, 'r') as f:
                audit_log = json.load(f)
        else:
            audit_log = []
        
        audit_log.append(audit_entry)
        
        # Write updated audit log
        with open(audit_file, 'w') as f:
            json.dump(audit_log, f, indent=2, default=str)

def get_storage_manager(storage_dir: str = "storage") -> StorageManager:
    """Factory function to create storage manager"""
    return StorageManager(storage_dir)

