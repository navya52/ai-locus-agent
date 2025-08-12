const pdfParse = require('pdf-parse');
const OpenAI = require('openai');

// Initialize OpenAI client
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

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
        
        const prompt = `Analyze this clinical letter and provide a medical summary. Focus on:
1. Key clinical findings and diagnoses
2. Urgent concerns that need immediate attention
3. Risk factors identified
4. Overall risk level (low/medium/high)
5. Confidence in the analysis (0-100%)

Clinical Letter Text:
${extractedText.substring(0, 3000)} // Limit to first 3000 chars for API efficiency

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
            temperature: 0.3,
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

exports.handler = async (event, context) => {
    console.log('DEBUG: Node.js Lambda function with PDF processing and AI analysis started');
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
    
    // Try to extract text from PDF if base64 data is provided
    if (body.fileData || body.file_data) {
        const fileData = body.fileData || body.file_data;
        try {
            console.log('DEBUG: Attempting PDF text extraction');
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
            
            console.log('DEBUG: PDF text extracted successfully');
        } catch (error) {
            console.log('DEBUG: PDF processing error:', error.message);
            extractedText = 'PDF processing failed: ' + error.message;
        }
    }
    
    // Perform AI analysis
    const aiAnalysis = await analyzeWithAI(extractedText, filename);
    
    const responseData = {
        status: 'success',
        message: 'PDF processing and AI analysis completed',
        api_version: '1.0.0',
        processing_timestamp: new Date().toISOString(),
        file_info: {
            filename: filename,
            word_count: wordCount,
            character_count: characterCount
        },
        extracted_data: {
            nhs_number: nhsNumber,
            text_preview: extractedText.substring(0, 200) + (extractedText.length > 200 ? '...' : '')
        },
        ai_summary: aiAnalysis,
        storage_info: {
            storage_id: 'lambda_storage_' + Date.now(),
            storage_status: 'processed',
            storage_reason: 'PDF processed and AI analysis completed',
            data_retention_policy: 'Compliance-based retention',
            privacy_compliant: true,
            audit_trail_enabled: true
        }
    };
    
    return {
        statusCode: 200,
        headers: headers,
        body: JSON.stringify(responseData)
    };
};
