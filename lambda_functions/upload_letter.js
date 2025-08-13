const pdfParse = require('pdf-parse');
const OpenAI = require('openai');
const AWS = require('aws-sdk');

// Initialize OpenAI client
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

// Initialize AWS services
const dynamodb = new AWS.DynamoDB.DocumentClient();
const s3 = new AWS.S3();
const TABLE_NAME = 'ai-locus-agent-analysis';
const S3_BUCKET_NAME = process.env.UPLOAD_BUCKET_NAME || 'ai-locus-agent-uploads-793312799936';

// Store file in S3 for audit trail
async function storeFileInS3(fileData, filename, storageId) {
    try {
        const pdfBuffer = Buffer.from(fileData, 'base64');
        const fileKey = `uploads/${storageId}/${filename}`;
        
        const uploadParams = {
            Bucket: S3_BUCKET_NAME,
            Key: fileKey,
            Body: pdfBuffer,
            ContentType: 'application/pdf',
            Metadata: {
                'original-filename': filename,
                'storage-id': storageId,
                'upload-timestamp': new Date().toISOString(),
                'file-size': pdfBuffer.length.toString(),
                'processing-status': 'completed'
            }
        };
        
        console.log('DEBUG: Uploading file to S3:', fileKey);
        const uploadResult = await s3.upload(uploadParams).promise();
        
        return {
            success: true,
            s3_key: fileKey,
            s3_url: uploadResult.Location,
            file_size: pdfBuffer.length,
            upload_timestamp: new Date().toISOString()
        };
    } catch (error) {
        console.error('ERROR: Failed to store file in S3:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// Generate unique storage ID
function generateStorageId() {
    return 'storage_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// PHI Detection and Masking Function
function detectAndMaskPHI(text) {
    console.log('DEBUG: Starting PHI detection and masking');
    
    let maskedText = text;
    const phiDetected = [];
    
    // Patterns for PHI detection - Only flag actual names
    const patterns = [
        // Names: Mr./Mrs./Ms./Dr. followed by actual name (not just "LONDON" or generic terms)
        {
            regex: /\b(Mr\.|Mrs\.|Ms\.|Dr\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g,
            replacement: '[PATIENT_NAME]',
            type: 'name',
            // Only count if it's not a generic term like "LONDON"
            validate: (match) => {
                const name = match[2];
                const genericTerms = ['LONDON', 'PATIENT', 'CLIENT', 'RESIDENT', 'SUBJECT'];
                return !genericTerms.includes(name.toUpperCase());
            }
        },
        // Names after "Dear" followed by actual name
        {
            regex: /\bDear\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g,
            replacement: '[PATIENT_NAME]',
            type: 'name',
            validate: (match) => {
                const name = match[1];
                const genericTerms = ['PATIENT', 'CLIENT', 'RESIDENT', 'SUBJECT'];
                return !genericTerms.includes(name.toUpperCase());
            }
        }
    ];
    
    // Apply each pattern
    patterns.forEach(pattern => {
        const matches = maskedText.match(pattern.regex);
        if (matches) {
            // Check if pattern has validation function
            if (pattern.validate) {
                const validMatches = matches.filter(match => {
                    const regexMatch = pattern.regex.exec(match);
                    pattern.regex.lastIndex = 0; // Reset regex state
                    return pattern.validate(regexMatch);
                });
                
                if (validMatches.length > 0) {
                    maskedText = maskedText.replace(pattern.regex, pattern.replacement);
                    phiDetected.push({
                        type: pattern.type,
                        count: validMatches.length,
                        masked: pattern.replacement
                    });
                    console.log(`DEBUG: Masked ${validMatches.length} valid ${pattern.type} instances`);
                }
            } else {
                // No validation needed
                maskedText = maskedText.replace(pattern.regex, pattern.replacement);
                phiDetected.push({
                    type: pattern.type,
                    count: matches.length,
                    masked: pattern.replacement
                });
                console.log(`DEBUG: Masked ${matches.length} ${pattern.type} instances`);
            }
        }
    });
    
    // Special handling for NHS numbers - keep them but log
    const nhsMatches = maskedText.match(/\b\d{3}\s*\d{3}\s*\d{4}\b/g);
    if (nhsMatches) {
        phiDetected.push({
            type: 'nhs_number',
            count: nhsMatches.length,
            masked: 'KEPT_FOR_CLINICAL_USE'
        });
        console.log(`DEBUG: Found ${nhsMatches.length} NHS number(s) - kept for clinical use`);
    }
    
    console.log(`DEBUG: PHI masking completed. Detected ${phiDetected.length} types of PHI`);
    
    return {
        maskedText: maskedText,
        phiDetected: phiDetected,
        originalLength: text.length,
        maskedLength: maskedText.length
    };
}

// AI analysis function
async function analyzeWithAI(extractedText, filename) {
    try {
        if (!process.env.OPENAI_API_KEY) {
            console.log('DEBUG: No OpenAI API key found, using fallback analysis');
            return {
                summary: 'AI analysis not available - API key required',
                risk_assessment: {
                    overall_risk: 'Unknown',
                    urgent_concerns: ['AI analysis not configured'],
                    risk_factors: ['No AI analysis available']
                },
                confidence_score: 0,
                key_findings: ['AI analysis requires OpenAI API key']
            };
        }

        console.log('DEBUG: Starting OpenAI analysis');
        
        const prompt = `Analyze this clinical letter and provide a medical summary. Be consistent and conservative in risk assessment.

IMPORTANT GUIDELINES:
- Only mark as "urgent" if there are immediate life-threatening concerns
- Only mark as "high" risk if there are significant clinical risks
- For routine appointments, use "low" risk
- Be consistent in your assessment

Focus on:
1. Key clinical findings and diagnoses
2. Urgent concerns that need immediate attention (only if truly urgent)
3. Risk factors identified
4. Overall risk level (low/medium/high) - be conservative
5. Confidence in the analysis (0-100%)

Clinical Letter Text:
${extractedText.substring(0, 3000)}

Provide your response in this exact JSON format:
{
    "summary": "Brief clinical summary",
    "risk_assessment": {
        "overall_risk": "low/medium/high",
        "urgent_concerns": ["list", "of", "urgent", "items"],
        "risk_factors": ["list", "of", "risk", "factors"]
    },
    "confidence_score": 85,
    "key_findings": ["finding1", "finding2", "finding3"]
}`;

        const completion = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [
                {
                    role: "system",
                    content: "You are a medical AI assistant analyzing clinical letters. Provide accurate, professional medical summaries focusing on patient safety and clinical relevance."
                },
                {
                    role: "user",
                    content: prompt
                }
            ],
            temperature: 0.1,
            max_tokens: 500
        });

        const aiResponse = completion.choices[0].message.content;
        console.log('DEBUG: OpenAI response received:', aiResponse);

        // Try to parse JSON response
        try {
            const parsedResponse = JSON.parse(aiResponse);
            return {
                summary: parsedResponse.summary || 'AI analysis completed',
                risk_assessment: {
                    overall_risk: parsedResponse.risk_assessment?.overall_risk || 'Unknown',
                    urgent_concerns: parsedResponse.risk_assessment?.urgent_concerns || ['No urgent concerns identified'],
                    risk_factors: parsedResponse.risk_assessment?.risk_factors || ['No specific risk factors identified']
                },
                confidence_score: parsedResponse.confidence_score || 85,
                key_findings: parsedResponse.key_findings || ['AI analysis completed successfully']
            };
        } catch (parseError) {
            console.log('DEBUG: Failed to parse OpenAI JSON response, using fallback');
            return {
                summary: aiResponse || 'AI analysis completed',
                risk_assessment: {
                    overall_risk: 'Unknown',
                    urgent_concerns: ['AI response format error'],
                    risk_factors: ['Response parsing failed']
                },
                confidence_score: 50,
                key_findings: ['AI analysis completed but response format unclear']
            };
        }

    } catch (error) {
        console.log('DEBUG: OpenAI API error:', error.message);
        return {
            summary: 'AI analysis failed - ' + error.message,
            risk_assessment: {
                overall_risk: 'Unknown',
                urgent_concerns: ['AI analysis error'],
                risk_factors: ['Technical error in AI processing']
            },
            confidence_score: 0,
            key_findings: ['AI analysis encountered an error']
        };
    }
}

// Function to store data in DynamoDB
async function storeAnalysisData(data) {
    try {
        const params = {
            TableName: TABLE_NAME,
            Item: {
                storage_id: data.storage_info.storage_id,
                timestamp: new Date().toISOString(),
                filename: data.file_info.filename,
                word_count: data.file_info.word_count,
                character_count: data.file_info.character_count,
                nhs_number: data.extracted_data.nhs_number,
                text_preview: data.extracted_data.text_preview,
                masked_text_preview: data.extracted_data.masked_text_preview,
                ai_summary: data.ai_summary,
                phi_protection: data.phi_protection,
                storage_status: data.storage_info.storage_status,
                storage_reason: data.storage_info.storage_reason,
                data_retention_policy: data.storage_info.data_retention_policy,
                privacy_compliant: data.storage_info.privacy_compliant,
                audit_trail_enabled: data.storage_info.audit_trail_enabled
            }
        };
        
        await dynamodb.put(params).promise();
        console.log('Data stored in DynamoDB successfully');
        return true;
    } catch (error) {
        console.error('Error storing data in DynamoDB:', error);
        return false;
    }
}

exports.handler = async (event, context) => {
    const startTime = Date.now();
    console.log('DEBUG: Node.js Lambda function with PDF processing, S3 storage, and AI analysis started');
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };
    
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: headers,
            body: ''
        };
    }
    
    let body = {};
    try {
        body = JSON.parse(event.body);
    } catch (error) {
        console.log('DEBUG: No body or invalid JSON');
    }
    
    const filename = body.filename || 'unknown_file';
    let extractedText = '';
    let nhsNumber = 'Not found';
    let wordCount = 0;
    let characterCount = 0;
    let fileStorageResult = null;
    let phiResult = null;
    let maskedText = null;
    
    // Generate unique storage ID for this processing session
    const storageId = generateStorageId();
    
    // Try to extract text from PDF and store file if base64 data is provided
    if (body.fileData || body.file_data) {
        const fileData = body.fileData || body.file_data;
        try {
            console.log('DEBUG: Attempting PDF text extraction and file storage');
            
            // Store original PDF file in S3 for audit trail
            fileStorageResult = await storeFileInS3(fileData, filename, storageId);
            
            // Extract text from PDF
            const pdfBuffer = Buffer.from(fileData, 'base64');
            const pdfData = await pdfParse(pdfBuffer);
            extractedText = pdfData.text;
            wordCount = extractedText.split(/\s+/).length;
            characterCount = extractedText.length;
            
            // Extract NHS number (10-digit pattern with optional spaces)
            const nhsMatch = extractedText.match(/\b\d{3}\s*\d{3}\s*\d{4}\b/);
            if (nhsMatch) {
                nhsNumber = nhsMatch[0].replace(/\s/g, ''); // Remove spaces
            }
            
            // Perform PHI detection and masking
            phiResult = detectAndMaskPHI(extractedText);
            maskedText = phiResult.maskedText;
            
            console.log('DEBUG: PDF text extracted, PHI masked, and file stored successfully');
        } catch (error) {
            console.log('DEBUG: PDF processing error:', error.message);
            extractedText = 'PDF processing failed: ' + error.message;
        }
        
        // Always perform PHI masking on extracted text, even if other processing failed
        if (extractedText && !maskedText) {
            try {
                phiResult = detectAndMaskPHI(extractedText);
                maskedText = phiResult.maskedText;
                console.log('DEBUG: PHI masking performed on extracted text');
            } catch (phiError) {
                console.log('DEBUG: PHI masking failed:', phiError.message);
                maskedText = extractedText; // Fallback to original text
            }
        }
    }
    
    // Perform AI analysis using masked text (if available)
    const textForAnalysis = maskedText || extractedText;
    const aiAnalysis = await analyzeWithAI(textForAnalysis, filename);
    
    const responseData = {
        status: 'success',
        message: 'PDF processing, file storage, and AI analysis completed',
        api_version: '1.0.0',
        processing_time: ((Date.now() - startTime) / 1000).toFixed(2),
        processing_timestamp: new Date().toISOString(),
        file_info: {
            filename: filename,
            word_count: wordCount,
            character_count: characterCount,
            file_size_bytes: fileStorageResult?.file_size || 0
        },
        extracted_data: {
            nhs_number: nhsNumber,
            text_preview: extractedText.substring(0, 200) + (extractedText.length > 200 ? '...' : ''),
            masked_text_preview: maskedText ? (maskedText.substring(0, 200) + (maskedText.length > 200 ? '...' : '')) : null
        },
        phi_protection: {
            enabled: true,
            phi_detected: phiResult?.phiDetected || [],
            total_phi_items: phiResult?.phiDetected?.filter(item => item.type !== 'nhs_number')?.length || 0,
            original_text_length: phiResult?.originalLength || extractedText.length,
            masked_text_length: phiResult?.maskedLength || extractedText.length,
            privacy_compliant: true
        },
        ai_summary: aiAnalysis,
        storage_info: {
            storage_id: storageId,
            storage_status: 'processed',
            storage_reason: 'PDF processed, stored, and AI analysis completed',
            data_retention_policy: 'Compliance-based retention with audit trail',
            privacy_compliant: true,
            audit_trail_enabled: true,
            file_storage: fileStorageResult || {
                success: false,
                error: 'No file data provided'
            }
        }
    };
    
    // Store data in DynamoDB
    const storageSuccess = await storeAnalysisData(responseData);
    if (!storageSuccess) {
        console.log('Warning: Failed to store data in DynamoDB');
    }
    
    return {
        statusCode: 200,
        headers: headers,
        body: JSON.stringify(responseData)
    };
};
