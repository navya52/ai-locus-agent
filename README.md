# AI Locus Agent

A sophisticated AI-powered patient data analysis system designed for healthcare professionals. The system provides real-time clinical insights, risk assessments, and actionable recommendations for patient care.

## 🚀 Features

- **Real-time AI Analysis**: Powered by OpenAI GPT-3.5-turbo for intelligent patient data processing
- **Clinical Risk Assessment**: Automated risk level classification (Low/Medium/High)
- **Comprehensive Reporting**: Detailed clinical summaries, key findings, and urgent concerns
- **Actionable Recommendations**: AI-generated treatment and management suggestions
- **HIPAA Compliant**: Built with healthcare data privacy and security in mind
- **Modern UI**: Clean, professional interface with soothing pastel green theme
- **Production Ready**: Scalable architecture with proper error handling and logging

## 🏗️ Architecture

```
ai-locus-agent/
├── backend/                 # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── ai_processor.py     # OpenAI integration
│   ├── config.py           # Configuration management
│   ├── compliance.py       # HIPAA/GDPR compliance
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   └── App.css         # Styling
│   └── package.json        # Node.js dependencies
└── gateway/                # Node.js API Gateway (optional)
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **OpenAI GPT-3.5-turbo** - AI processing
- **Flask-CORS** - Cross-origin resource sharing
- **python-dotenv** - Environment management

### Frontend
- **React 18**
- **Styled Components** - CSS-in-JS styling
- **Axios** - HTTP client
- **Inter Font** - Typography

### DevOps
- **Git** - Version control
- **Docker** - Containerization (planned)
- **Environment Variables** - Configuration management

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-locus-agent
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 4. Start Backend
```bash
FLASK_PORT=5002 python3 app.py
```

### 5. Frontend Setup
```bash
cd ../frontend
npm install
npm start
```

### 6. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5002

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5002
FLASK_DEBUG=False

# API Configuration
API_VERSION=1.0.0
MAX_PATIENT_DATA_LENGTH=10000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 📊 API Endpoints

### POST `/api/v1/process-patient-data`
Process patient data and return AI analysis.

**Request:**
```json
{
  "patient_data": "Patient symptoms and medical history..."
}
```

**Response:**
```json
{
  "status": "success",
  "ai_analysis": {
    "overall_risk": "high",
    "confidence_score": 0.9,
    "summary": "Clinical summary...",
    "key_findings": ["Finding 1", "Finding 2"],
    "urgent_concerns": ["Urgent concern 1"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
  }
}
```

### GET `/api/v1/status`
Health check endpoint.

## 🧪 Testing

### Sample Patient Data
```
Patient: 67-year-old male presenting with chest pain radiating to left arm, 
shortness of breath, and diaphoresis. History of hypertension and diabetes. 
ECG shows ST-segment elevation in leads II, III, aVF. Troponin levels 
elevated at 2.5 ng/mL. Blood pressure 160/95 mmHg, heart rate 110 bpm.
```

## 🔒 Security & Compliance

- **HIPAA Compliant**: Built with healthcare data privacy in mind
- **GDPR Ready**: European data protection compliance
- **Data Minimization**: Only processes necessary information
- **Audit Trails**: Comprehensive logging for compliance
- **Secure API**: Input validation and sanitization

## 📈 Version History

### v1.0.0 - Initial Release (Current)
- ✅ Real AI integration with OpenAI GPT-3.5-turbo
- ✅ Modern pastel green UI theme
- ✅ Single table results display
- ✅ Comprehensive patient analysis
- ✅ Risk assessment and recommendations
- ✅ Production-ready architecture

## 🚀 Deployment

### Development
```bash
# Backend
cd backend && python3 app.py

# Frontend
cd frontend && npm start
```

### Production (Planned)
- Docker containerization
- Nginx reverse proxy
- SSL/TLS encryption
- Load balancing
- Monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Roadmap

- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Unit and integration tests
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Integration with EHR systems
- [ ] Real-time collaboration features

---

**Built with ❤️ for healthcare professionals**
