"""
Workflow Automation Engine for AI Locus Agent

This module provides advanced workflow automation including:
- Referral prioritization and triage
- Resource allocation optimization
- Follow-up scheduling
- Clinical documentation assistance

Goes beyond simple AI wrapper to provide comprehensive clinical workflow automation.
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from ai_processor import AIProcessor, AIAnalysisResult

logger = logging.getLogger(__name__)

class UrgencyLevel(Enum):
    """Clinical urgency levels"""
    CRITICAL = "critical"      # Immediate intervention required
    URGENT = "urgent"         # Within 1 hour
    HIGH = "high"             # Within 4 hours
    MEDIUM = "medium"         # Within 24 hours
    LOW = "low"               # Routine care

class CareLevel(Enum):
    """Care level recommendations"""
    ICU = "icu"               # Intensive care unit
    HDU = "hdu"               # High dependency unit
    WARD = "ward"             # General ward
    AMBULATORY = "ambulatory" # Outpatient care
    DISCHARGE = "discharge"   # Safe for discharge

@dataclass
class WorkflowStep:
    """Individual step in clinical workflow"""
    step_id: str
    title: str
    description: str
    urgency: UrgencyLevel
    estimated_duration: int  # minutes
    required_resources: List[str]
    dependencies: List[str]  # step_ids that must complete first
    automated: bool = False

@dataclass
class ResourceAllocation:
    """Resource allocation recommendation"""
    care_level: CareLevel
    bed_type: str
    monitoring_level: str
    estimated_los: int  # length of stay in hours
    required_equipment: List[str]
    staffing_needs: List[str]

@dataclass
class FollowUpSchedule:
    """Follow-up scheduling recommendation"""
    next_review: datetime
    review_interval: timedelta
    escalation_triggers: List[str]
    discharge_criteria: List[str]

@dataclass
class ClinicalDocumentation:
    """Generated clinical documentation"""
    chief_complaint: str
    history_of_present_illness: str
    assessment: str
    plan: str
    icd_codes: List[str]
    medications: List[str]
    orders: List[str]

@dataclass
class WorkflowResult:
    """Complete workflow automation result"""
    ai_analysis: AIAnalysisResult
    urgency_level: UrgencyLevel
    care_level: CareLevel
    workflow_steps: List[WorkflowStep]
    resource_allocation: ResourceAllocation
    follow_up_schedule: FollowUpSchedule
    clinical_documentation: ClinicalDocumentation
    processing_time: float
    confidence_score: float

class ClinicalRulesEngine:
    """Applies clinical rules and guidelines"""
    
    def __init__(self):
        self.critical_indicators = [
            "cardiac arrest", "respiratory arrest", "severe bleeding",
            "anaphylaxis", "severe trauma", "stroke symptoms",
            "chest pain", "unconscious", "seizure"
        ]
        
        self.urgent_indicators = [
            "fever", "shortness of breath", "severe pain",
            "altered mental status", "dehydration", "infection"
        ]
    
    def determine_urgency(self, ai_analysis: AIAnalysisResult) -> UrgencyLevel:
        """Determine clinical urgency based on AI analysis and clinical rules"""
        text_lower = ai_analysis.summary.lower()
        
        # Check for critical indicators
        for indicator in self.critical_indicators:
            if indicator in text_lower:
                return UrgencyLevel.CRITICAL
        
        # Check for urgent indicators
        for indicator in self.urgent_indicators:
            if indicator in text_lower:
                return UrgencyLevel.URGENT
        
        # Use AI risk assessment
        risk_level = ai_analysis.risk_assessment.get('overall_risk', 'low')
        if risk_level == 'high':
            return UrgencyLevel.HIGH
        elif risk_level == 'medium':
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW

class ResourceOptimizer:
    """Optimizes resource allocation based on patient needs"""
    
    def __init__(self):
        self.care_level_criteria = {
            CareLevel.ICU: ["ventilator", "vasopressors", "continuous monitoring", "critical care"],
            CareLevel.HDU: ["high monitoring", "frequent observations", "specialized care"],
            CareLevel.WARD: ["general care", "routine monitoring", "standard treatment"],
            CareLevel.AMBULATORY: ["outpatient", "home care", "follow-up"],
            CareLevel.DISCHARGE: ["stable", "no acute needs", "safe for discharge"]
        }
    
    def optimize_care_level(self, ai_analysis: AIAnalysisResult, urgency: UrgencyLevel) -> CareLevel:
        """Determine optimal care level"""
        text_lower = ai_analysis.summary.lower()
        
        # Critical cases go to ICU
        if urgency == UrgencyLevel.CRITICAL:
            return CareLevel.ICU
        
        # Check for specific care needs
        for care_level, criteria in self.care_level_criteria.items():
            for criterion in criteria:
                if criterion in text_lower:
                    return care_level
        
        # Default based on urgency
        if urgency == UrgencyLevel.URGENT:
            return CareLevel.HDU
        elif urgency == UrgencyLevel.HIGH:
            return CareLevel.WARD
        elif urgency == UrgencyLevel.MEDIUM:
            return CareLevel.AMBULATORY
        else:
            return CareLevel.DISCHARGE

class WorkflowGenerator:
    """Generates structured clinical workflows"""
    
    def __init__(self):
        self.workflow_templates = {
            UrgencyLevel.CRITICAL: self._critical_workflow,
            UrgencyLevel.URGENT: self._urgent_workflow,
            UrgencyLevel.HIGH: self._high_workflow,
            UrgencyLevel.MEDIUM: self._medium_workflow,
            UrgencyLevel.LOW: self._low_workflow
        }
    
    def generate_workflow(self, ai_analysis: AIAnalysisResult, urgency: UrgencyLevel) -> List[WorkflowStep]:
        """Generate workflow steps based on urgency and AI analysis"""
        template_func = self.workflow_templates.get(urgency, self._low_workflow)
        return template_func(ai_analysis)
    
    def _critical_workflow(self, ai_analysis: AIAnalysisResult) -> List[WorkflowStep]:
        """Critical care workflow"""
        return [
            WorkflowStep(
                step_id="immediate_assessment",
                title="Immediate Assessment",
                description="ABC assessment and stabilization",
                urgency=UrgencyLevel.CRITICAL,
                estimated_duration=5,
                required_resources=["monitoring", "emergency_equipment"],
                dependencies=[],
                automated=False
            ),
            WorkflowStep(
                step_id="emergency_intervention",
                title="Emergency Intervention",
                description="Immediate life-saving measures",
                urgency=UrgencyLevel.CRITICAL,
                estimated_duration=15,
                required_resources=["icu_bed", "specialist_team"],
                dependencies=["immediate_assessment"],
                automated=False
            ),
            WorkflowStep(
                step_id="continuous_monitoring",
                title="Continuous Monitoring",
                description="24/7 intensive monitoring",
                urgency=UrgencyLevel.CRITICAL,
                estimated_duration=1440,  # 24 hours
                required_resources=["icu_monitoring", "nursing_staff"],
                dependencies=["emergency_intervention"],
                automated=True
            )
        ]
    
    def _urgent_workflow(self, ai_analysis: AIAnalysisResult) -> List[WorkflowStep]:
        """Urgent care workflow"""
        return [
            WorkflowStep(
                step_id="rapid_assessment",
                title="Rapid Assessment",
                description="Quick clinical evaluation",
                urgency=UrgencyLevel.URGENT,
                estimated_duration=10,
                required_resources=["monitoring", "nursing_staff"],
                dependencies=[],
                automated=False
            ),
            WorkflowStep(
                step_id="urgent_treatment",
                title="Urgent Treatment",
                description="Immediate treatment initiation",
                urgency=UrgencyLevel.URGENT,
                estimated_duration=30,
                required_resources=["treatment_equipment", "medications"],
                dependencies=["rapid_assessment"],
                automated=False
            )
        ]
    
    def _high_workflow(self, ai_analysis: AIAnalysisResult) -> List[WorkflowStep]:
        """High priority workflow"""
        return [
            WorkflowStep(
                step_id="comprehensive_assessment",
                title="Comprehensive Assessment",
                description="Detailed clinical evaluation",
                urgency=UrgencyLevel.HIGH,
                estimated_duration=20,
                required_resources=["examination_room", "medical_staff"],
                dependencies=[],
                automated=False
            ),
            WorkflowStep(
                step_id="treatment_planning",
                title="Treatment Planning",
                description="Develop treatment strategy",
                urgency=UrgencyLevel.HIGH,
                estimated_duration=15,
                required_resources=["consultation_room", "specialist"],
                dependencies=["comprehensive_assessment"],
                automated=False
            )
        ]
    
    def _medium_workflow(self, ai_analysis: AIAnalysisResult) -> List[WorkflowStep]:
        """Medium priority workflow"""
        return [
            WorkflowStep(
                step_id="routine_assessment",
                title="Routine Assessment",
                description="Standard clinical evaluation",
                urgency=UrgencyLevel.MEDIUM,
                estimated_duration=30,
                required_resources=["clinic_room", "general_staff"],
                dependencies=[],
                automated=False
            )
        ]
    
    def _low_workflow(self, ai_analysis: AIAnalysisResult) -> List[WorkflowStep]:
        """Low priority workflow"""
        return [
            WorkflowStep(
                step_id="basic_assessment",
                title="Basic Assessment",
                description="Simple clinical evaluation",
                urgency=UrgencyLevel.LOW,
                estimated_duration=15,
                required_resources=["basic_equipment"],
                dependencies=[],
                automated=False
            )
        ]

class DocumentationGenerator:
    """Generates clinical documentation"""
    
    def generate_documentation(self, ai_analysis: AIAnalysisResult, workflow_steps: List[WorkflowStep]) -> ClinicalDocumentation:
        """Generate comprehensive clinical documentation"""
        
        # Extract key information from AI analysis
        summary = ai_analysis.summary
        findings = ai_analysis.key_findings
        recommendations = ai_analysis.recommendations
        
        # Generate structured documentation
        chief_complaint = self._extract_chief_complaint(summary)
        history = self._generate_history(summary, findings)
        assessment = self._generate_assessment(ai_analysis)
        plan = self._generate_plan(recommendations, workflow_steps)
        
        return ClinicalDocumentation(
            chief_complaint=chief_complaint,
            history_of_present_illness=history,
            assessment=assessment,
            plan=plan,
            icd_codes=self._suggest_icd_codes(summary),
            medications=self._suggest_medications(recommendations),
            orders=self._generate_orders(workflow_steps)
        )
    
    def _extract_chief_complaint(self, summary: str) -> str:
        """Extract chief complaint from summary"""
        # Simple extraction - in production, use NLP
        if "chest pain" in summary.lower():
            return "Chest pain"
        elif "shortness of breath" in summary.lower():
            return "Shortness of breath"
        elif "fever" in summary.lower():
            return "Fever"
        else:
            return "Patient evaluation"
    
    def _generate_history(self, summary: str, findings: List[str]) -> str:
        """Generate history of present illness"""
        return f"Patient presents with {summary.lower()}. Key findings include: {', '.join(findings[:3])}."
    
    def _generate_assessment(self, ai_analysis: AIAnalysisResult) -> str:
        """Generate clinical assessment"""
        risk_level = ai_analysis.risk_assessment.get('overall_risk', 'unknown')
        return f"Clinical assessment indicates {risk_level} risk level with {ai_analysis.confidence_score:.0%} confidence."
    
    def _generate_plan(self, recommendations: List[str], workflow_steps: List[WorkflowStep]) -> str:
        """Generate treatment plan"""
        plan_items = recommendations[:3] + [f"Follow {step.title}" for step in workflow_steps[:2]]
        return f"Treatment plan: {'; '.join(plan_items)}."
    
    def _suggest_icd_codes(self, summary: str) -> List[str]:
        """Suggest ICD-10 codes based on summary"""
        # Simplified - in production, use medical NLP
        if "chest pain" in summary.lower():
            return ["R07.9", "I20.9"]  # Chest pain, unspecified; Angina pectoris
        elif "fever" in summary.lower():
            return ["R50.9", "A41.9"]  # Fever, unspecified; Sepsis
        else:
            return ["Z00.00"]  # Encounter for general adult medical examination
    
    def _suggest_medications(self, recommendations: List[str]) -> List[str]:
        """Suggest medications based on recommendations"""
        # Simplified - in production, use drug databases
        meds = []
        for rec in recommendations:
            if "aspirin" in rec.lower():
                meds.append("Aspirin 325mg")
            elif "antibiotic" in rec.lower():
                meds.append("Empiric antibiotic therapy")
        return meds
    
    def _generate_orders(self, workflow_steps: List[WorkflowStep]) -> List[str]:
        """Generate clinical orders based on workflow"""
        orders = []
        for step in workflow_steps:
            if "monitoring" in step.required_resources:
                orders.append(f"Continuous monitoring for {step.title}")
            if "assessment" in step.title.lower():
                orders.append(f"Complete {step.title}")
        return orders

class WorkflowEngine:
    """Main workflow automation engine"""
    
    def __init__(self, ai_processor: AIProcessor):
        self.ai_processor = ai_processor
        self.clinical_rules = ClinicalRulesEngine()
        self.resource_optimizer = ResourceOptimizer()
        self.workflow_generator = WorkflowGenerator()
        self.documentation_generator = DocumentationGenerator()
    
    def process_patient_workflow(self, patient_data: str) -> WorkflowResult:
        """
        Process patient data and generate comprehensive workflow
        
        Args:
            patient_data: Raw patient data text
            
        Returns:
            WorkflowResult with complete workflow automation
        """
        start_time = time.time()
        
        # Stage 1: AI Analysis
        ai_analysis = self.ai_processor.analyze_patient_data(patient_data)
        
        # Stage 2: Clinical Rules Engine
        urgency_level = self.clinical_rules.determine_urgency(ai_analysis)
        
        # Stage 3: Resource Optimization
        care_level = self.resource_optimizer.optimize_care_level(ai_analysis, urgency_level)
        
        # Stage 4: Workflow Generation
        workflow_steps = self.workflow_generator.generate_workflow(ai_analysis, urgency_level)
        
        # Stage 5: Resource Allocation
        resource_allocation = self._generate_resource_allocation(care_level, urgency_level)
        
        # Stage 6: Follow-up Scheduling
        follow_up_schedule = self._generate_follow_up_schedule(urgency_level, care_level)
        
        # Stage 7: Documentation Generation
        clinical_documentation = self.documentation_generator.generate_documentation(ai_analysis, workflow_steps)
        
        processing_time = time.time() - start_time
        
        return WorkflowResult(
            ai_analysis=ai_analysis,
            urgency_level=urgency_level,
            care_level=care_level,
            workflow_steps=workflow_steps,
            resource_allocation=resource_allocation,
            follow_up_schedule=follow_up_schedule,
            clinical_documentation=clinical_documentation,
            processing_time=processing_time,
            confidence_score=ai_analysis.confidence_score
        )
    
    def _generate_resource_allocation(self, care_level: CareLevel, urgency: UrgencyLevel) -> ResourceAllocation:
        """Generate resource allocation recommendation"""
        los_mapping = {
            CareLevel.ICU: 72,      # 3 days
            CareLevel.HDU: 48,      # 2 days
            CareLevel.WARD: 24,     # 1 day
            CareLevel.AMBULATORY: 4, # 4 hours
            CareLevel.DISCHARGE: 1   # 1 hour
        }
        
        equipment_mapping = {
            CareLevel.ICU: ["ventilator", "monitoring", "iv_pump"],
            CareLevel.HDU: ["monitoring", "iv_pump"],
            CareLevel.WARD: ["basic_monitoring"],
            CareLevel.AMBULATORY: ["basic_equipment"],
            CareLevel.DISCHARGE: ["none"]
        }
        
        return ResourceAllocation(
            care_level=care_level,
            bed_type=care_level.value,
            monitoring_level=f"{care_level.value}_monitoring",
            estimated_los=los_mapping[care_level],
            required_equipment=equipment_mapping[care_level],
            staffing_needs=[f"{care_level.value}_staff"]
        )
    
    def _generate_follow_up_schedule(self, urgency: UrgencyLevel, care_level: CareLevel) -> FollowUpSchedule:
        """Generate follow-up scheduling recommendation"""
        interval_mapping = {
            UrgencyLevel.CRITICAL: timedelta(hours=1),
            UrgencyLevel.URGENT: timedelta(hours=4),
            UrgencyLevel.HIGH: timedelta(hours=12),
            UrgencyLevel.MEDIUM: timedelta(days=1),
            UrgencyLevel.LOW: timedelta(days=7)
        }
        
        next_review = datetime.now() + interval_mapping[urgency]
        
        return FollowUpSchedule(
            next_review=next_review,
            review_interval=interval_mapping[urgency],
            escalation_triggers=["deterioration", "new_symptoms", "abnormal_vitals"],
            discharge_criteria=["stable_vitals", "improved_symptoms", "no_complications"]
        )

def get_workflow_engine(ai_processor: AIProcessor) -> WorkflowEngine:
    """Factory function to create workflow engine"""
    return WorkflowEngine(ai_processor)

