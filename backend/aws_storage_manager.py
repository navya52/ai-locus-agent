"""
AWS Storage Manager for AI Locus Agent

This module handles AWS S3 and DynamoDB integration for storing
analysis results with healthcare-grade compliance and scalability.
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from data_classifier import DataClassifier, DataClassification

logger = logging.getLogger(__name__)

class AWSStorageManager:
    """Manages AWS S3 and DynamoDB storage for analysis data"""
    
    def __init__(self):
        # Initialize AWS clients
        self.s3_client = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Configuration from environment
        self.s3_bucket = os.getenv('AWS_S3_BUCKET', 'ai-locus-agent-storage')
        self.dynamodb_table = os.getenv('AWS_DYNAMODB_TABLE', 'ai-locus-agent-analyses')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        # Initialize data classifier
        self.data_classifier = DataClassifier()
        
        # Storage configuration
        self.retention_policies = {
            "clinical_output": 30,  # 30 days
            "analysis_metadata": 90,  # 90 days
            "sensitive_patient_data": 0,  # Never store
            "unknown": 0  # Never store
        }
        
        # Initialize table reference
        self.table = self.dynamodb.Table(self.dynamodb_table)
        
        logger.info(f"AWS Storage Manager initialized - S3: {self.s3_bucket}, DynamoDB: {self.dynamodb_table}")
    
    def store_analysis_result(self, analysis_result: Dict[str, Any]) -> Optional[str]:
        """
        Store analysis result in AWS S3 and DynamoDB
        
        Args:
            analysis_result: The AI analysis result
            
        Returns:
            Storage ID if stored, None if not stored
        """
        try:
            # Classify the data
            classification = self.data_classifier.classify_analysis_data(analysis_result)
            
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
            
            # Store in S3
            s3_key = f"{classification.data_type}/{storage_id}.json"
            self._store_in_s3(s3_key, safe_data)
            
            # Store metadata in DynamoDB
            self._store_in_dynamodb(storage_id, safe_data, classification)
            
            # Log audit trail
            self._log_audit_trail(storage_id, "store", classification.data_type)
            
            logger.info(f"Successfully stored analysis result in AWS: {storage_id}")
            return storage_id
            
        except Exception as e:
            logger.error(f"Error storing analysis result in AWS: {e}")
            return None
    
    def retrieve_analysis_result(self, storage_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve stored analysis result from AWS
        
        Args:
            storage_id: The storage ID
            
        Returns:
            Stored data if found, None if not found
        """
        try:
            # First check DynamoDB for metadata
            response = self.table.get_item(Key={'storage_id': storage_id})
            
            if 'Item' not in response:
                logger.warning(f"Analysis result not found in DynamoDB: {storage_id}")
                return None
            
            item = response['Item']
            data_type = item.get('data_type', 'clinical_output')
            
            # Retrieve from S3
            s3_key = f"{data_type}/{storage_id}.json"
            data = self._retrieve_from_s3(s3_key)
            
            if data:
                # Log audit trail
                self._log_audit_trail(storage_id, "retrieve", data_type)
                logger.info(f"Retrieved analysis result from AWS: {storage_id}")
                return data
            
            logger.warning(f"Analysis result not found in S3: {storage_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving analysis result from AWS: {e}")
            return None
    
    def delete_analysis_result(self, storage_id: str) -> bool:
        """
        Delete stored analysis result from AWS (GDPR compliance)
        
        Args:
            storage_id: The storage ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            # First check DynamoDB for metadata
            response = self.table.get_item(Key={'storage_id': storage_id})
            
            if 'Item' not in response:
                logger.warning(f"Analysis result not found for deletion: {storage_id}")
                return False
            
            item = response['Item']
            data_type = item.get('data_type', 'clinical_output')
            
            # Delete from S3
            s3_key = f"{data_type}/{storage_id}.json"
            self._delete_from_s3(s3_key)
            
            # Delete from DynamoDB
            self.table.delete_item(Key={'storage_id': storage_id})
            
            # Log audit trail
            self._log_audit_trail(storage_id, "delete", data_type)
            
            logger.info(f"Deleted analysis result from AWS: {storage_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting analysis result from AWS: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics from AWS
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            stats = {
                "total_files": 0,
                "data_types": {},
                "total_size_bytes": 0,
                "storage_type": "aws"
            }
            
            # Get S3 statistics
            try:
                s3_response = self.s3_client.list_objects_v2(Bucket=self.s3_bucket)
                if 'Contents' in s3_response:
                    stats["total_files"] = len(s3_response['Contents'])
                    stats["total_size_bytes"] = sum(obj['Size'] for obj in s3_response['Contents'])
                    
                    # Count by data type
                    for obj in s3_response['Contents']:
                        key = obj['Key']
                        data_type = key.split('/')[0] if '/' in key else 'unknown'
                        stats["data_types"][data_type] = stats["data_types"].get(data_type, 0) + 1
            except ClientError as e:
                logger.warning(f"Could not get S3 stats: {e}")
            
            # Get DynamoDB statistics
            try:
                dynamo_response = self.table.scan(Select='COUNT')
                stats["dynamodb_items"] = dynamo_response['Count']
            except ClientError as e:
                logger.warning(f"Could not get DynamoDB stats: {e}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting AWS storage stats: {e}")
            return {"error": str(e), "storage_type": "aws"}
    
    def _store_in_s3(self, key: str, data: Dict[str, Any]):
        """Store data in S3"""
        try:
            json_data = json.dumps(data, default=str)
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=key,
                Body=json_data,
                ContentType='application/json',
                Metadata={
                    'created_at': datetime.utcnow().isoformat(),
                    'data_type': 'analysis_result'
                }
            )
            logger.debug(f"Stored data in S3: {key}")
        except ClientError as e:
            logger.error(f"Error storing in S3: {e}")
            raise
    
    def _retrieve_from_s3(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=key)
            data = json.loads(response['Body'].read().decode('utf-8'))
            logger.debug(f"Retrieved data from S3: {key}")
            return data
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"Key not found in S3: {key}")
                return None
            logger.error(f"Error retrieving from S3: {e}")
            raise
    
    def _delete_from_s3(self, key: str):
        """Delete data from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.s3_bucket, Key=key)
            logger.debug(f"Deleted data from S3: {key}")
        except ClientError as e:
            logger.error(f"Error deleting from S3: {e}")
            raise
    
    def _store_in_dynamodb(self, storage_id: str, data: Dict[str, Any], classification: DataClassification):
        """Store metadata in DynamoDB"""
        try:
            item = {
                'storage_id': storage_id,
                'analysis_id': data.get('analysis_id'),
                'timestamp': data.get('timestamp'),
                'data_type': classification.data_type,
                'sensitivity_level': classification.sensitivity_level,
                'retention_days': classification.retention_days,
                'processing_time': data.get('processing_time'),
                'model_used': data.get('model_used'),
                'confidence_score': data.get('confidence_score'),
                'created_at': datetime.utcnow().isoformat()
            }
            
            self.table.put_item(Item=item)
            logger.debug(f"Stored metadata in DynamoDB: {storage_id}")
        except ClientError as e:
            logger.error(f"Error storing in DynamoDB: {e}")
            raise
    
    def _generate_storage_id(self) -> str:
        """Generate unique storage ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}"
    
    def _log_audit_trail(self, storage_id: str, action: str, data_type: str):
        """Log audit trail to S3"""
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "storage_id": storage_id,
                "action": action,
                "data_type": data_type,
                "storage_type": "aws"
            }
            
            audit_key = f"audit_logs/audit_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Try to get existing audit log
            try:
                existing_data = self._retrieve_from_s3(audit_key)
                audit_log = existing_data if existing_data else []
            except:
                audit_log = []
            
            audit_log.append(audit_entry)
            
            # Store updated audit log
            self._store_in_s3(audit_key, audit_log)
            
        except Exception as e:
            logger.error(f"Error logging audit trail: {e}")

def get_aws_storage_manager() -> AWSStorageManager:
    """Factory function to create AWS storage manager"""
    return AWSStorageManager()
