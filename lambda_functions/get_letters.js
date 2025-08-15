const AWS = require('aws-sdk');

// Initialize DynamoDB
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.DYNAMODB_TABLE_NAME;
const ENVIRONMENT = process.env.ENVIRONMENT;

if (!TABLE_NAME) {
    throw new Error('DYNAMODB_TABLE_NAME environment variable is required');
}

console.log(`Using table: ${TABLE_NAME} in environment: ${ENVIRONMENT}`);

exports.handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json'
    };
    
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: headers,
            body: ''
        };
    }
    
    try {
        console.log('DEBUG: Fetching all letters from DynamoDB');
        
        // Scan DynamoDB table to get all letters
        const params = {
            TableName: TABLE_NAME,
            // Optional: Add pagination if needed
            Limit: 100
        };
        
        const result = await dynamodb.scan(params).promise();
        
        // Sort by timestamp (newest first)
        const sortedLetters = result.Items.sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        );
        
        console.log(`DEBUG: Found ${sortedLetters.length} letters`);
        
        return {
            statusCode: 200,
            headers: headers,
            body: JSON.stringify({
                status: 'success',
                message: 'Letters retrieved successfully',
                count: sortedLetters.length,
                letters: sortedLetters
            })
        };
        
    } catch (error) {
        console.error('ERROR: Failed to fetch letters:', error);
        
        return {
            statusCode: 500,
            headers: headers,
            body: JSON.stringify({
                status: 'error',
                message: 'Failed to retrieve letters',
                error: error.message
            })
        };
    }
};
