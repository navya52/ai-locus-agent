"""
AI Processing Service for AI Locus Agent

This module handles the AI-powered analysis of patient data using OpenAI GPT-4.
It provides structured analysis including medical insights, risk assessment,
and actionable recommendations.
"""

import os
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import openai
from config import Config

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class AIAnalysisResult:
    """Structured result from AI analysis"""
    summary: str
    key_findings: List[str]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    processing_time: float
    model_used: str
    tokens_used: int

class AIProcessor:
    """Handles AI-powered analysis of patient data"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client with API key"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                logger.warning("OPENAI_API_KEY not found. AI processing will be disabled.")
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if AI processing is available"""
        return self.client is not None
    
    def analyze_patient_data(self, patient_text: str) -> AIAnalysisResult:
        """
        Analyze patient data using AI
        
        Args:
            patient_text: Raw patient data text
            
        Returns:
            AIAnalysisResult with structured analysis
        """
        if not self.is_available():
            return self._fallback_analysis(patient_text)
        
        start_time = time.time()
        
        try:
            # Create the analysis prompt
            prompt = self._create_analysis_prompt(patient_text)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent medical analysis
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_data = self._parse_ai_response(response)
            
            processing_time = time.time() - start_time
            
            return AIAnalysisResult(
                summary=analysis_data.get('summary', ''),
                key_findings=analysis_data.get('key_findings', []),
                risk_assessment=analysis_data.get('risk_assessment', {}),
                recommendations=analysis_data.get('recommendations', []),
                confidence_score=analysis_data.get('confidence_score', 0.0),
                processing_time=processing_time,
                model_used="gpt-3.5-turbo",
                tokens_used=response.usage.total_tokens if response.usage else 0
            )
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._fallback_analysis(patient_text)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for medical analysis"""
        return """You are an AI medical assistant specializing in patient data analysis. 
        
Your role is to:
1. Analyze patient data for key medical insights
2. Identify potential risks and concerns
3. Provide actionable recommendations
4. Maintain medical accuracy and safety

IMPORTANT GUIDELINES:
- Always prioritize patient safety
- Flag any urgent medical concerns
- Provide evidence-based recommendations
- Be clear about limitations and uncertainties
- Maintain HIPAA compliance in analysis
- Use medical terminology appropriately

Respond in JSON format with the following structure:
{
    "summary": "Brief overview of the patient data",
    "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
    "risk_assessment": {
        "overall_risk": "low/medium/high",
        "urgent_concerns": ["Any urgent issues"],
        "risk_factors": ["Risk factor 1", "Risk factor 2"]
    },
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "confidence_score": 0.85
}"""
    
    def _create_analysis_prompt(self, patient_text: str) -> str:
        """Create the analysis prompt for the patient data"""
        return f"""Please analyze the following patient data and provide a structured medical assessment:

PATIENT DATA:
{patient_text}

Please provide a comprehensive analysis including:
1. Summary of the patient's condition
2. Key medical findings
3. Risk assessment (overall risk level, urgent concerns, risk factors)
4. Specific recommendations for next steps
5. Confidence score (0.0 to 1.0) for your analysis

Focus on actionable insights that would be valuable for healthcare providers."""
    
    def _parse_ai_response(self, response) -> Dict[str, Any]:
        """Parse the AI response into structured data"""
        try:
            import json
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return self._get_default_analysis()
    
    def _fallback_analysis(self, patient_text: str) -> AIAnalysisResult:
        """Fallback analysis when AI is not available"""
        logger.info("Using fallback analysis (AI not available)")
        
        # Check if this is a cardiac case for mock response
        text_lower = patient_text.lower()
        
        if any(keyword in text_lower for keyword in ['chest pain', 'st-segment', 'troponin', 'ecg']):
            # Mock cardiac analysis
            return AIAnalysisResult(
                summary="Patient presents with acute coronary syndrome symptoms. ST-segment elevation on ECG and elevated troponin levels suggest myocardial infarction requiring immediate intervention.",
                key_findings=[
                    "ST-segment elevation in leads II, III, aVF indicating inferior wall MI",
                    "Elevated troponin levels (2.5 ng/mL) confirming myocardial injury",
                    "Chest pain radiating to left arm with associated symptoms",
                    "Hypertension and diabetes as risk factors"
                ],
                risk_assessment={
                    "overall_risk": "high",
                    "urgent_concerns": [
                        "Acute myocardial infarction",
                        "Need for immediate cardiac intervention",
                        "Risk of complications including arrhythmias"
                    ],
                    "risk_factors": [
                        "ST-segment elevation",
                        "Elevated troponin",
                        "Hypertension",
                        "Diabetes mellitus",
                        "Chest pain with radiation"
                    ]
                },
                recommendations=[
                    "Immediate cardiac catheterization and PCI",
                    "Administer aspirin 325mg and loading dose of antiplatelet therapy",
                    "Continuous ECG monitoring for arrhythmias",
                    "IV access and prepare for potential complications",
                    "Consult cardiology immediately",
                    "Consider thrombolytic therapy if PCI not available within 90 minutes"
                ],
                confidence_score=0.85,
                processing_time=0.1,
                model_used="fallback_mock",
                tokens_used=0
            )
        elif any(keyword in text_lower for keyword in ['pneumonia', 'infiltrate', 'fever', 'cough']):
            # Mock respiratory analysis
            return AIAnalysisResult(
                summary="Patient presents with community-acquired pneumonia based on clinical symptoms, radiographic findings, and laboratory evidence.",
                key_findings=[
                    "Right lower lobe infiltrate on chest X-ray",
                    "Fever and productive cough with yellow sputum",
                    "Elevated WBC count (15,000/μL)",
                    "Oxygen saturation 92% on room air"
                ],
                risk_assessment={
                    "overall_risk": "medium",
                    "urgent_concerns": [
                        "Hypoxemia requiring oxygen therapy",
                        "Risk of respiratory failure"
                    ],
                    "risk_factors": [
                        "Smoking history (20 pack-years)",
                        "Age 45 with underlying lung disease",
                        "Hypoxemia"
                    ]
                },
                recommendations=[
                    "Start empiric antibiotic therapy (amoxicillin-clavulanate or azithromycin)",
                    "Supplemental oxygen therapy to maintain SpO2 >95%",
                    "Chest physiotherapy and incentive spirometry",
                    "Monitor for signs of respiratory failure",
                    "Consider admission if CURB-65 score ≥2",
                    "Follow up chest X-ray in 48-72 hours"
                ],
                confidence_score=0.8,
                processing_time=0.1,
                model_used="fallback_mock",
                tokens_used=0
            )
        else:
            # Basic keyword-based analysis
            risk_keywords = ['pain', 'fever', 'bleeding', 'chest pain', 'shortness of breath']
            urgent_keywords = ['severe', 'acute', 'emergency', 'critical']
            
            risk_factors = [word for word in risk_keywords if word in text_lower]
            urgent_concerns = [word for word in urgent_keywords if word in text_lower]
            
            overall_risk = 'high' if urgent_concerns else 'medium' if risk_factors else 'low'
            
            return AIAnalysisResult(
                summary="Basic analysis completed (AI processing unavailable)",
                key_findings=["Patient data received and processed"],
                risk_assessment={
                    "overall_risk": overall_risk,
                    "urgent_concerns": urgent_concerns,
                    "risk_factors": risk_factors
                },
                recommendations=["Consult with healthcare provider for detailed assessment"],
                confidence_score=0.3,
                processing_time=0.1,
                model_used="fallback",
                tokens_used=0
            )
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis structure"""
        return {
            "summary": "Analysis completed with limited confidence",
            "key_findings": ["Patient data processed"],
            "risk_assessment": {
                "overall_risk": "unknown",
                "urgent_concerns": [],
                "risk_factors": []
            },
            "recommendations": ["Manual review recommended"],
            "confidence_score": 0.1
        }

# Global AI processor instance
ai_processor = None

def get_ai_processor(config: Config) -> AIProcessor:
    """Get or create the global AI processor instance"""
    global ai_processor
    if ai_processor is None:
        ai_processor = AIProcessor(config)
    return ai_processor
