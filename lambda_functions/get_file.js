const AWS = require('aws-sdk');

// Initialize AWS services
const s3 = new AWS.S3();
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.DYNAMODB_TABLE_NAME;
const ENVIRONMENT = process.env.ENVIRONMENT;

if (!TABLE_NAME) {
    throw new Error('DYNAMODB_TABLE_NAME environment variable is required');
}

console.log(`Using table: ${TABLE_NAME} in environment: ${ENVIRONMENT}`);
const S3_BUCKET_NAME = process.env.UPLOAD_BUCKET_NAME || 'ai-locus-agent-uploads-793312799936';

exports.handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers: headers, body: '' };
    }

    try {
        // Get storage ID from query parameters
        const storageId = event.queryStringParameters?.storage_id;
        
        if (!storageId) {
            return {
                statusCode: 400,
                headers: headers,
                body: JSON.stringify({
                    status: 'error',
                    message: 'Storage ID is required',
                    error: 'Missing storage_id parameter'
                })
            };
        }

        console.log('DEBUG: Retrieving file for storage ID:', storageId);

        // First, get the record from DynamoDB to find the S3 file key
        const dbParams = {
            TableName: TABLE_NAME,
            Key: { storage_id: storageId }
        };

        const dbResult = await dynamodb.get(dbParams).promise();
        
        if (!dbResult.Item) {
            return {
                statusCode: 404,
                headers: headers,
                body: JSON.stringify({
                    status: 'error',
                    message: 'File not found',
                    error: 'No record found for the provided storage ID'
                })
            };
        }

        const fileStorage = dbResult.Item.storage_info?.file_storage;
        
        if (!fileStorage || !fileStorage.success || !fileStorage.s3_key) {
            return {
                statusCode: 404,
                headers: headers,
                body: JSON.stringify({
                    status: 'error',
                    message: 'Original file not found',
                    error: 'File was not stored in S3 or storage information is missing'
                })
            };
        }

        // Generate a pre-signed URL for secure file download
        const presignedUrlParams = {
            Bucket: S3_BUCKET_NAME,
            Key: fileStorage.s3_key,
            Expires: 3600, // URL expires in 1 hour
            ResponseContentDisposition: `attachment; filename="${dbResult.Item.file_info.filename}"`,
            ResponseContentType: 'application/pdf'
        };

        const presignedUrl = await s3.getSignedUrlPromise('getObject', presignedUrlParams);

        // Log the file access for audit trail
        console.log('DEBUG: File access logged for storage ID:', storageId, 'by user:', event.requestContext?.identity?.sourceIp || 'unknown');

        return {
            statusCode: 200,
            headers: headers,
            body: JSON.stringify({
                status: 'success',
                message: 'File access URL generated successfully',
                data: {
                    storage_id: storageId,
                    filename: dbResult.Item.file_info.filename,
                    file_size_bytes: fileStorage.file_size,
                    upload_timestamp: fileStorage.upload_timestamp,
                    download_url: presignedUrl,
                    expires_in_seconds: 3600,
                    audit_trail: {
                        access_timestamp: new Date().toISOString(),
                        access_method: 'presigned_url',
                        user_ip: event.requestContext?.identity?.sourceIp || 'unknown'
                    }
                }
            })
        };

    } catch (error) {
        console.error('ERROR: Failed to retrieve file:', error);
        return {
            statusCode: 500,
            headers: headers,
            body: JSON.stringify({
                status: 'error',
                message: 'Failed to retrieve file',
                error: error.message
            })
        };
    }
};
