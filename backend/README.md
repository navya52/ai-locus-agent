# AI Locus Agent Backend

A Flask-based AI locus agent backend that processes patient data for medical analysis and locus identification. This system is designed to accept patient information and provide AI-powered analysis for clinical decision support.

## Features

- **Patient Data Processing**: Single POST route `/process-patient-data` that accepts patient information
- **AI Analysis**: Placeholder structure for AI locus identification and medical analysis
- **JSON API**: RESTful API with JSON request/response format
- **Input Validation**: Comprehensive validation for patient data
- **Error Handling**: Robust error handling with meaningful error messages
- **CORS Support**: Enabled for frontend integration
- **Health Monitoring**: Health check endpoint for system monitoring

## Medical Use Cases

This AI locus agent can be used for:
- Symptom analysis and locus identification
- Medical entity recognition from patient notes
- Risk assessment and stratification
- Treatment recommendation generation
- Clinical decision support

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the AI locus agent:**
   ```bash
   python app.py
   ```

The AI locus agent will start on `http://localhost:5000`

## API Endpoints

### POST /process-patient-data
Accepts patient data and returns AI analysis results.

**Request:**
```json
{
  "patient_data": "Patient presents with acute chest pain, shortness of breath, and sweating. History of hypertension and diabetes."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Patient data processed successfully by AI locus agent",
  "original_patient_data": "Patient presents with acute chest pain...",
  "cleaned_patient_data": "Patient presents with acute chest pain...",
  "text_analysis": {
    "word_count": 15,
    "character_count": 120
  },
  "ai_analysis": {
    "locus_identified": true,
    "confidence_score": 0.85,
    "recommended_actions": ["Further clinical assessment", "Laboratory tests"],
    "risk_level": "moderate"
  },
  "processing_timestamp": "2024-01-01T12:00:00Z"
}
```

### GET /health
Health check endpoint to verify the AI locus agent is operational.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Locus Agent Backend",
  "message": "AI locus agent is running and ready to process patient data",
  "version": "1.0.0"
}
```

## Example Usage

### Using curl:
```bash
curl -X POST http://localhost:5000/process-patient-data \
  -H "Content-Type: application/json" \
  -d '{"patient_data": "Patient reports severe headache, confusion, and difficulty speaking. No history of migraines."}'
```

### Using Python requests:
```python
import requests

patient_data = {
    "patient_data": "Patient complains of abdominal pain, nausea, and vomiting for the past 24 hours."
}

response = requests.post('http://localhost:5000/process-patient-data', 
                        json=patient_data)
result = response.json()
print(f"AI Analysis: {result['ai_analysis']}")
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success - Patient data processed successfully
- `400`: Bad request - Missing or invalid patient data
- `500`: Internal server error - AI processing error

## Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

This will test various patient scenarios including:
- Chest pain symptoms
- Neurological symptoms
- Gastrointestinal issues
- Respiratory symptoms
- Error scenarios

## AI Integration Points

The current implementation includes placeholder structures for AI integration:

1. **Locus Identification**: `ai_analysis.locus_identified`
2. **Confidence Scoring**: `ai_analysis.confidence_score`
3. **Recommendation Generation**: `ai_analysis.recommended_actions`
4. **Risk Assessment**: `ai_analysis.risk_level`

## Customization

You can enhance the AI locus agent by:

1. **Adding NLP Processing**: Integrate medical NLP libraries for symptom extraction
2. **Medical Entity Recognition**: Add medical terminology recognition
3. **Locus Algorithms**: Implement specific locus identification algorithms
4. **Risk Models**: Add medical risk assessment models
5. **Treatment Logic**: Implement treatment recommendation algorithms

Modify the `process_patient_data()` function in `app.py` to add your specific AI processing logic.

## Security Considerations

For production use, consider:
- HIPAA compliance for patient data handling
- Authentication and authorization
- Data encryption in transit and at rest
- Audit logging for patient data access
- Rate limiting to prevent abuse
