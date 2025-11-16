"""
Healthcare Symptom Navigator Agent - Medical Information Assistant
Helps users understand symptoms, navigate healthcare options, and find resources
IMPORTANT: This provides educational information only, not medical diagnosis
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from utils.observability import AgentLogger, AgentTracer, MetricsCollector
from utils.gemini_client import get_gemini_client

logger = AgentLogger("HealthcareNavigatorAgent")
tracer = AgentTracer()
metrics = MetricsCollector()


class HealthcareNavigatorAgent:
    """
    Medical information navigator that helps users:
    - Understand symptoms and possible causes
    - Navigate healthcare system (when to see doctor, ER, urgent care)
    - Find appropriate medical resources
    - Learn about conditions and treatments
    
    ⚠️ DISCLAIMER: Educational purposes only. Always consult healthcare professionals.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "Healthcare Navigator"
        self.api_key = api_key
        self.gemini_client = None
        
        # Try to initialize Gemini client
        if api_key:
            self.gemini_client = get_gemini_client(api_key)
            if self.gemini_client:
                logger.info("Gemini API integration enabled for Healthcare Navigator")
        
        # Medical disclaimer
        self.disclaimer = """
        ⚠️ IMPORTANT MEDICAL DISCLAIMER ⚠️
        This agent provides educational information only and is NOT a substitute for 
        professional medical advice, diagnosis, or treatment. Always seek the advice 
        of your physician or other qualified health provider with any questions you 
        may have regarding a medical condition. If you think you may have a medical 
        emergency, call your doctor or dial 112 (Emergency) / 102/108 (Ambulance) immediately.
        """
        
        # Urgency levels
        self.urgency_levels = {
            "emergency": {
                "action": "🚨 CALL 112 (Emergency) or 102/108 (Ambulance) IMMEDIATELY",
                "timeframe": "Now - this is life-threatening"
            },
            "urgent": {
                "action": "⚡ See doctor today or go to Urgent Care within 2-4 hours",
                "timeframe": "Within 24 hours"
            },
            "soon": {
                "action": "📞 Schedule doctor appointment within next few days",
                "timeframe": "Within 2-7 days"
            },
            "routine": {
                "action": "📅 Bring up at next regular checkup or schedule appointment",
                "timeframe": "Within 2-4 weeks"
            },
            "self_care": {
                "action": "🏠 Can typically manage at home with self-care",
                "timeframe": "Monitor and see doctor if worsens"
            }
        }
        
        # Emergency red flags
        self.emergency_keywords = [
            "chest pain", "difficulty breathing", "can't breathe", "severe bleeding",
            "loss of consciousness", "passed out", "stroke", "heart attack",
            "severe head injury", "suicidal", "overdose", "poisoning",
            "severe allergic reaction", "anaphylaxis", "not breathing",
            "choking", "seizure lasting", "severe burn", "major trauma"
        ]
        
        # Body systems for organization
        self.body_systems = {
            "cardiovascular": ["heart", "blood pressure", "circulation", "chest"],
            "respiratory": ["lungs", "breathing", "cough", "asthma"],
            "digestive": ["stomach", "nausea", "diarrhea", "constipation", "appetite"],
            "neurological": ["headache", "dizziness", "numbness", "confusion", "memory"],
            "musculoskeletal": ["joint", "muscle", "back", "bone", "injury"],
            "mental_health": ["anxiety", "depression", "stress", "sleep", "mood"],
            "dermatological": ["skin", "rash", "itch", "wound"],
            "general": ["fever", "fatigue", "weight", "pain"]
        }
        
    def navigate(self,
                query: str,
                age_group: str = "adult",
                duration: Optional[str] = None,
                severity: Optional[str] = None,
                trace_id: Optional[str] = None) -> Dict:
        """
        Main navigation function for healthcare information
        
        Args:
            query: User's health question or symptom description
            age_group: child, teen, adult, senior
            duration: How long symptoms have been present
            severity: mild, moderate, severe
            trace_id: Tracing ID for observability
            
        Returns:
            Dict with urgency assessment, information, resources, next steps
        """
        start_time = datetime.now()
        trace_id = trace_id or tracer.generate_trace_id()
        
        logger.info(f"[{trace_id}] Healthcare query: {query[:50]}...")
        
        try:
            # Check for emergency situations first
            urgency = self._assess_urgency(query, severity)
            
            if urgency == "emergency":
                logger.warning(f"[{trace_id}] EMERGENCY DETECTED: {query[:100]}")
                return self._emergency_response(query)
            
            # Classify the query type
            query_type = self._classify_query(query)
            logger.info(f"[{trace_id}] Query type: {query_type}")
            
            # Identify body system(s) involved
            systems = self._identify_systems(query)
            
            # Generate response based on query type
            if query_type == "symptom":
                response = self._explain_symptom(query, age_group, duration, severity, urgency)
            elif query_type == "condition":
                response = self._explain_condition(query, age_group)
            elif query_type == "treatment":
                response = self._explain_treatment(query)
            elif query_type == "prevention":
                response = self._prevention_guidance(query)
            else:
                response = self._general_health_info(query, age_group)
            
            # Add urgency assessment
            response["urgency"] = {
                "level": urgency,
                "action": self.urgency_levels[urgency]["action"],
                "timeframe": self.urgency_levels[urgency]["timeframe"]
            }
            
            # Add resources
            response["resources"] = self._find_resources(query, urgency, age_group)
            
            # Add when to seek help
            response["when_to_see_doctor"] = self._when_to_see_doctor(query, urgency)
            
            # Add self-care tips if appropriate
            if urgency in ["routine", "self_care"]:
                response["self_care"] = self._self_care_tips(query, systems)
            
            # Add metadata
            duration_time = (datetime.now() - start_time).total_seconds()
            response["metadata"] = {
                "age_group": age_group,
                "urgency_level": urgency,
                "body_systems": systems,
                "query_type": query_type,
                "duration_seconds": round(duration_time, 2),
                "timestamp": datetime.now().isoformat(),
                "disclaimer": self.disclaimer
            }
            
            metrics.record_metric("healthcare_query", duration_time, {
                "urgency": urgency,
                "type": query_type
            })
            
            logger.info(f"[{trace_id}] Healthcare navigation completed in {duration_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"[{trace_id}] Error in healthcare navigation: {str(e)}")
            return {
                "error": str(e),
                "message": "Unable to process health query. Please consult a healthcare professional directly.",
                "emergency_contacts": self._get_emergency_contacts(),
                "metadata": {"disclaimer": self.disclaimer}
            }
    
    def _assess_urgency(self, query: str, severity: Optional[str]) -> str:
        """Assess urgency level of the situation"""
        query_lower = query.lower()
        
        # Check for emergency keywords
        for keyword in self.emergency_keywords:
            if keyword in query_lower:
                return "emergency"
        
        # Check severity indicator
        if severity == "severe":
            # Severe + certain symptoms = urgent
            if any(word in query_lower for word in ["pain", "bleeding", "fever", "breathing"]):
                return "urgent"
        
        # Urgent indicators
        urgent_patterns = [
            "sudden", "severe", "acute", "intense", "worsening rapidly",
            "can't eat", "can't sleep", "can't function", "high fever",
            "spreading rapidly", "getting worse", "unbearable"
        ]
        if any(pattern in query_lower for pattern in urgent_patterns):
            return "urgent"
        
        # Soon indicators
        soon_patterns = [
            "persistent", "hasn't improved", "lasting", "won't go away",
            "recurring", "concerning", "worried about"
        ]
        if any(pattern in query_lower for pattern in soon_patterns):
            return "soon"
        
        # Routine or self-care
        minor_patterns = [
            "mild", "occasional", "minor", "slight", "small",
            "prevention", "how to avoid", "general question"
        ]
        if any(pattern in query_lower for pattern in minor_patterns):
            return "self_care"
        
        # Default to routine
        return "routine"
    
    def _emergency_response(self, query: str) -> Dict:
        """Immediate response for emergency situations"""
        return {
            "🚨 EMERGENCY": "CALL 112 (All Emergencies) or 102/108 (Ambulance) IMMEDIATELY",
            "urgency": {
                "level": "emergency",
                "action": "🚨 CALL 112 or 102/108 IMMEDIATELY or go to nearest Emergency Room",
                "timeframe": "NOW - This may be life-threatening"
            },
            "immediate_steps": [
                "1. 📞 Call 112 (all emergencies) or 102/108 (ambulance) or have someone call for you",
                "2. 🏥 Go to nearest Emergency Room if safe to do so",
                "3. 👥 Stay with someone - don't be alone",
                "4. 📋 If unconscious, not breathing, or severe bleeding, start first aid if trained"
            ],
            "emergency_contacts": self._get_emergency_contacts(),
            "symptoms": query,
            "message": "This appears to be a medical emergency. Seek immediate professional medical help.",
            "metadata": {
                "urgency_level": "emergency",
                "disclaimer": self.disclaimer
            }
        }
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of health query"""
        query_lower = query.lower()
        
        # Symptom queries
        if any(word in query_lower for word in ["symptom", "feel", "pain", "hurt", "ache", "experiencing"]):
            return "symptom"
        
        # Condition/disease queries
        if any(word in query_lower for word in ["what is", "disease", "condition", "disorder", "syndrome", "diagnosis"]):
            return "condition"
        
        # Treatment queries
        if any(word in query_lower for word in ["treatment", "cure", "medicine", "medication", "therapy", "how to treat"]):
            return "treatment"
        
        # Prevention queries
        if any(word in query_lower for word in ["prevent", "avoid", "reduce risk", "protection", "prevention"]):
            return "prevention"
        
        return "general"
    
    def _identify_systems(self, query: str) -> List[str]:
        """Identify which body systems are involved"""
        query_lower = query.lower()
        involved_systems = []
        
        for system, keywords in self.body_systems.items():
            if any(keyword in query_lower for keyword in keywords):
                involved_systems.append(system)
        
        return involved_systems if involved_systems else ["general"]
    
    def _explain_symptom(self, query: str, age_group: str, duration: Optional[str], 
                        severity: Optional[str], urgency: str) -> Dict:
        """Explain possible causes and what symptom might indicate"""
        return {
            "symptom": query,
            "overview": f"Understanding your symptom: {query}",
            "possible_causes": self._get_possible_causes(query, age_group),
            "common_associated_symptoms": self._get_associated_symptoms(query),
            "assessment_factors": {
                "duration": duration or "Not specified - important for assessment",
                "severity": severity or "Not specified - important for assessment",
                "age_considerations": self._get_age_considerations(query, age_group)
            },
            "red_flags": self._get_red_flags(query),
            "information": f"""
📋 **Symptom Information:**
Your symptom requires evaluation considering multiple factors including duration, 
severity, associated symptoms, and your personal medical history.

🔍 **What to Monitor:**
Pay attention to any changes, new symptoms, or worsening. Keep track of when it 
occurs, what makes it better or worse, and any patterns you notice.

📝 **For Your Doctor:**
Write down when the symptom started, how often it occurs, what you were doing when 
it began, any medications you're taking, and questions you want to ask.
"""
        }
    
    def _get_possible_causes(self, query: str, age_group: str) -> List[Dict]:
        """List possible causes for symptoms (educational)"""
        return [
            {
                "category": "Common Causes",
                "description": "More frequent, typically less serious conditions",
                "note": "These are general possibilities - not a diagnosis"
            },
            {
                "category": "Systemic Causes",
                "description": "Conditions affecting multiple body systems",
                "note": "May require comprehensive evaluation"
            },
            {
                "category": "Age-Related Considerations",
                "description": f"Factors specific to {age_group} age group",
                "note": "Different age groups may have different risk factors"
            },
            {
                "category": "Serious Causes to Rule Out",
                "description": "Less common but important to exclude",
                "note": "Your doctor will evaluate for these"
            }
        ]
    
    def _get_associated_symptoms(self, query: str) -> List[str]:
        """Symptoms that commonly occur together"""
        return [
            "Tell your doctor if you also experience any of these:",
            "• Changes in other body systems",
            "• New or worsening symptoms",
            "• Fever or chills",
            "• Changes in appetite or weight",
            "• Sleep disturbances",
            "• Mood changes"
        ]
    
    def _get_age_considerations(self, query: str, age_group: str) -> str:
        """Age-specific considerations"""
        considerations = {
            "child": "Children may not be able to clearly describe symptoms. Watch for behavior changes, irritability, or reduced activity.",
            "teen": "Teens may experience symptoms related to growth, hormonal changes, or stress. Mental health screening is important.",
            "adult": "Consider lifestyle factors, work stress, family history, and any chronic conditions.",
            "senior": "Older adults may have atypical symptom presentation. Consider medication interactions and multiple conditions."
        }
        return considerations.get(age_group, considerations["adult"])
    
    def _get_red_flags(self, query: str) -> List[str]:
        """Warning signs that require immediate attention"""
        return [
            "🚩 Seek immediate care if you experience:",
            "• Sudden, severe worsening",
            "• New chest pain or difficulty breathing",
            "• Confusion or change in consciousness",
            "• Severe, persistent pain",
            "• Signs of infection (high fever, spreading redness)",
            "• Symptoms affecting safety (severe dizziness, loss of balance)"
        ]
    
    def _explain_condition(self, query: str, age_group: str) -> Dict:
        """Explain a health condition"""
        return {
            "condition": query,
            "overview": {
                "description": "Understanding this health condition",
                "key_points": [
                    "What it is and how it develops",
                    "Who is typically affected",
                    "Common symptoms and signs",
                    "How it's diagnosed and treated"
                ]
            },
            "living_with_condition": [
                "📚 Education about the condition",
                "💊 Treatment options and management",
                "🏥 Regular monitoring and checkups",
                "👥 Support groups and resources",
                "🎯 Lifestyle modifications"
            ],
            "questions_for_doctor": self._generate_doctor_questions(query),
            "information": """
Your healthcare provider can give you personalized information about:
- Your specific risk factors
- Treatment options best suited for you
- Expected outcomes and prognosis
- Warning signs to watch for
- Lifestyle changes that can help
"""
        }
    
    def _explain_treatment(self, query: str) -> Dict:
        """Explain treatment options"""
        return {
            "treatment_topic": query,
            "overview": "Understanding treatment approaches",
            "types_of_treatment": [
                {
                    "category": "Medical Treatment",
                    "description": "Medications, procedures, therapies prescribed by doctors",
                    "note": "Always follow your healthcare provider's instructions"
                },
                {
                    "category": "Lifestyle Interventions",
                    "description": "Diet, exercise, stress management, sleep hygiene",
                    "note": "Often works best in combination with medical treatment"
                },
                {
                    "category": "Complementary Approaches",
                    "description": "Approaches used alongside conventional medicine",
                    "note": "Discuss with your doctor before starting any complementary therapy"
                }
            ],
            "important_notes": [
                "⚕️ Never start, stop, or change medications without consulting your doctor",
                "📋 Keep a list of all medications and supplements you take",
                "💬 Ask about potential side effects and interactions",
                "📞 Know who to contact if you have questions or concerns",
                "⏰ Follow the prescribed schedule and dosage exactly"
            ]
        }
    
    def _prevention_guidance(self, query: str) -> Dict:
        """Provide prevention and wellness guidance"""
        return {
            "prevention_topic": query,
            "overview": "Taking steps to protect your health",
            "key_prevention_strategies": [
                {
                    "area": "🏃 Physical Activity",
                    "recommendation": "Regular exercise appropriate for your fitness level",
                    "goal": "At least 150 minutes moderate activity per week"
                },
                {
                    "area": "🥗 Nutrition",
                    "recommendation": "Balanced diet rich in fruits, vegetables, whole grains",
                    "goal": "Varied, colorful plate with appropriate portions"
                },
                {
                    "area": "😴 Sleep",
                    "recommendation": "Consistent sleep schedule with adequate hours",
                    "goal": "7-9 hours for adults; more for children"
                },
                {
                    "area": "🧘 Stress Management",
                    "recommendation": "Regular stress-reduction activities",
                    "goal": "Daily practice of relaxation or mindfulness"
                },
                {
                    "area": "🏥 Preventive Care",
                    "recommendation": "Regular checkups and recommended screenings",
                    "goal": "Stay current with age-appropriate screenings"
                }
            ],
            "risk_reduction_tips": self._get_prevention_tips(query)
        }
    
    def _get_prevention_tips(self, query: str) -> List[str]:
        """Specific prevention tips"""
        return [
            "✓ Know your family medical history",
            "✓ Maintain a healthy weight for your body",
            "✓ Don't smoke; limit alcohol consumption",
            "✓ Manage chronic conditions with your doctor",
            "✓ Stay up to date with vaccinations",
            "✓ Practice good hygiene and safety habits",
            "✓ Build strong social connections",
            "✓ Monitor your health - know what's normal for you"
        ]
    
    def _general_health_info(self, query: str, age_group: str) -> Dict:
        """General health information"""
        return {
            "topic": query,
            "information": "General health guidance and information",
            "healthy_habits": [
                "🏃 Stay physically active",
                "🥗 Eat a balanced, nutritious diet",
                "😴 Get adequate sleep",
                "💧 Stay hydrated",
                "🧘 Manage stress",
                "👥 Maintain social connections",
                "🏥 Get regular checkups",
                "🧠 Keep your mind active"
            ],
            "wellness_focus": f"""
For {age_group}s, focus on:
- Age-appropriate health screenings
- Preventive care and vaccinations
- Healthy lifestyle habits
- Mental health and wellbeing
- Building a relationship with a primary care provider
"""
        }
    
    def _when_to_see_doctor(self, query: str, urgency: str) -> Dict:
        """Guidance on when professional help is needed"""
        return {
            "general_guidance": "See a doctor if:",
            "warning_signs": [
                "• Symptoms persist or worsen despite self-care",
                "• Symptoms interfere with daily activities",
                "• New or unusual symptoms develop",
                "• You have concerns or questions about your health",
                "• Symptoms are different from previous experiences",
                "• You have risk factors or pre-existing conditions"
            ],
            "prepare_for_visit": [
                "📝 Write down all symptoms and when they started",
                "💊 List all medications and supplements",
                "📋 Note any questions you want to ask",
                "👥 Consider bringing a family member or friend",
                "📸 Take photos of visible symptoms if applicable"
            ]
        }
    
    def _self_care_tips(self, query: str, systems: List[str]) -> Dict:
        """Self-care recommendations for appropriate situations"""
        return {
            "self_care_measures": [
                "🏠 Rest and allow your body to recover",
                "💧 Stay well hydrated with water",
                "🍲 Eat nutritious, easy-to-digest foods",
                "😴 Get adequate sleep",
                "🌡️ Monitor your symptoms",
                "📊 Keep a symptom diary"
            ],
            "over_the_counter_options": {
                "note": "Consider OTC options if appropriate",
                "reminder": "Read labels carefully and follow directions",
                "caution": "Ask pharmacist or doctor if unsure about any medication"
            },
            "when_to_escalate": "If symptoms don't improve in a reasonable timeframe or worsen, contact your healthcare provider."
        }
    
    def _find_resources(self, query: str, urgency: str, age_group: str) -> List[Dict]:
        """Find relevant healthcare resources - India specific"""
        resources = []
        
        # Emergency resources
        if urgency == "emergency":
            resources.append({
                "name": "🚨 Emergency Services - India",
                "contact": "112 (All emergencies) | 102/108 (Ambulance)",
                "description": "For life-threatening emergencies - Call immediately"
            })
        
        # India-specific healthcare resources
        resources.extend([
            {
                "name": "🇮🇳 Government Health Services",
                "type": "official",
                "resources": [
                    "Aarogya Setu App - COVID-19 tracking & health info",
                    "National Health Portal - https://www.nhp.gov.in",
                    "e-Sanjeevani - Free telemedicine: https://esanjeevani.in",
                    "Ayushman Bharat - Health insurance scheme",
                    "Swasth Bharat - Health ministry portal"
                ]
            },
            {
                "name": "🏥 Online Doctor Consultation (India)",
                "type": "telehealth",
                "platforms": [
                    "Practo - https://www.practo.com (Book doctors, online consultation)",
                    "1mg - https://www.1mg.com (Doctors, medicines, lab tests)",
                    "Apollo 24/7 - https://www.apollo247.com (24/7 consultation)",
                    "Tata Health - Online consultations & pharmacy",
                    "PharmEasy - https://pharmeasy.in (Medicines & health services)",
                    "Lybrate - https://www.lybrate.com (Find doctors & consult online)",
                    "DocsApp - Specialist doctor consultations",
                    "MFine - AI-powered health assistant"
                ]
            },
            {
                "name": "🏥 Major Hospital Networks (India)",
                "type": "hospitals",
                "networks": [
                    "AIIMS (All India Institute of Medical Sciences) - Delhi & across India",
                    "Apollo Hospitals - Pan-India network",
                    "Fortis Healthcare - Major cities",
                    "Max Healthcare - North India",
                    "Manipal Hospitals - Pan-India",
                    "Medanta - Gurugram & other cities",
                    "Narayana Health - Bangalore & multiple cities",
                    "Lilavati Hospital - Mumbai",
                    "Kokilaben Hospital - Mumbai",
                    "Sir Ganga Ram Hospital - Delhi",
                    "Christian Medical College (CMC) - Vellore",
                    "Government Medical Colleges - Each state capital"
                ]
            },
            {
                "name": "💊 Online Pharmacies (India)",
                "type": "pharmacy",
                "services": [
                    "1mg - Medicine delivery across India",
                    "PharmEasy - Medicines & health products",
                    "Netmeds - Online pharmacy",
                    "Apollo Pharmacy - Trusted pharmacy chain",
                    "Medlife - Medicines & diagnostics"
                ]
            },
            {
                "name": "🔬 Diagnostic & Lab Services (India)",
                "type": "diagnostics",
                "providers": [
                    "Dr. Lal PathLabs - Pan-India lab network",
                    "Thyrocare - Affordable diagnostic services",
                    "SRL Diagnostics - Comprehensive testing",
                    "Metropolis Healthcare - Advanced diagnostics",
                    "Redcliffe Labs - Home sample collection",
                    "Healthians - Preventive health checkups"
                ]
            },
            {
                "name": "🧠 Mental Health Support (India)",
                "type": "mental_health",
                "helplines": [
                    "TISS iCall - 1800-599-0019 (Mon-Sat, 8 AM-10 PM)",
                    "Vandrevala Foundation - +91-9820466726 (24/7)",
                    "NIMHANS - 080-46110007 (Bangalore)",
                    "Sumaitri - 011-23389090 (Delhi)",
                    "Aasra - 022-27546669 (Mumbai, 24/7)",
                    "Sneha - 044-24640050 (Chennai, 24/7)",
                    "Connecting Trust - +91-9922001122 (Pune)",
                    "MantraCare - https://mantracare.org - Online therapy",
                    "BetterLYF - Online counseling platform",
                    "InnerHour - Mental health app"
                ]
            },
            {
                "name": "📱 Health Apps & Portals (India)",
                "type": "digital",
                "apps": [
                    "Aarogya Setu - Official COVID-19 & health app",
                    "mySugr - Diabetes management",
                    "HealthifyMe - Diet & fitness tracking",
                    "Practo - Find doctors & book appointments",
                    "1mg - Complete health management",
                    "DigiLocker - Store health records digitally",
                    "UMANG - Government services including health"
                ]
            },
            {
                "name": "📚 Trusted Health Information (India)",
                "type": "educational",
                "sources": [
                    "National Health Portal - https://www.nhp.gov.in",
                    "Ministry of Health - https://www.mohfw.gov.in",
                    "Indian Medical Association - https://www.ima-india.org",
                    "WHO India - https://www.who.int/india",
                    "ICMR - https://www.icmr.gov.in (Indian Council of Medical Research)",
                    "AIIMS - https://www.aiims.edu (Medical information)"
                ]
            },
            {
                "name": "🆘 Specialized Helplines (India)",
                "type": "helplines",
                "services": [
                    "Women Helpline - 1091 / 181 (24/7)",
                    "Child Helpline - 1098",
                    "Senior Citizen Helpline - 1291 / 14567",
                    "COVID-19 Helpline - 1075",
                    "National Tobacco Quitline - 1800-112-356",
                    "National AIDS Helpline - 1097",
                    "Poison Information - 1066 (AIIMS)"
                ]
            },
            {
                "name": "💳 Health Insurance & Schemes (India)",
                "type": "insurance",
                "schemes": [
                    "Ayushman Bharat (PMJAY) - Free health coverage up to ₹5 lakhs",
                    "ESIC - Employee State Insurance for workers",
                    "CGHS - Central Government Health Scheme",
                    "Rashtriya Swasthya Bima Yojana (RSBY)",
                    "Private Insurance - Star Health, HDFC Ergo, Care Health, etc."
                ]
            },
            {
                "name": "🚑 Ambulance Services (India)",
                "type": "emergency",
                "services": [
                    "National Ambulance - 102 / 108 (Free in most states)",
                    "Dial 4242 - Private ambulance booking",
                    "Red Cross Ambulance - Local numbers",
                    "State-specific ambulance numbers",
                    "Hospital ambulances - Contact nearest hospital"
                ]
            }
        ])
        
        # Add age-specific resources
        if age_group == "child":
            resources.append({
                "name": "👶 Pediatric Care (India)",
                "specialists": [
                    "Rainbow Children's Hospitals",
                    "Cloudnine Hospitals - Mother & child care",
                    "Government pediatric wards in medical colleges",
                    "Child Helpline - 1098 for emergencies"
                ]
            })
        elif age_group == "senior":
            resources.append({
                "name": "👴 Senior Care (India)",
                "services": [
                    "Senior Citizen Helpline - 1291 / 14567",
                    "Government hospitals with geriatric departments",
                    "Elder care services through NGOs",
                    "Home healthcare services via Portea, Nightingales, etc."
                ]
            })
        
        return resources
    
    def _get_emergency_contacts(self) -> Dict:
        """Emergency contact information - India specific"""
        return {
            "🇮🇳 INDIA EMERGENCY NUMBERS": {
                "🚨 Emergency (All Services)": "112",
                "🚑 Ambulance": "102 / 108",
                "🚓 Police": "100",
                "🚒 Fire": "101",
                "👮 Women Helpline": "1091 / 181",
                "👶 Child Helpline": "1098",
                "🧠 Mental Health Helpline": "1800-599-0019 (TISS iCall)",
                "🆘 Mental Health Support": "+91-9820466726 (Vandrevala Foundation - 24/7)",
                "☠️ Poison Control": "1066 (AIIMS)",
                "🏥 COVID-19 Helpline": "1075",
                "💊 Senior Citizen Helpline": "1291 / 14567",
                "🚨 Disaster Management": "1070",
                "📞 Railway Accidents": "1072",
                "🚗 Road Accidents": "1073"
            },
            "🌐 ONLINE DOCTOR CONSULTATION": {
                "Practo": "https://www.practo.com - Book appointments & online consultation",
                "1mg": "https://www.1mg.com - Medicine delivery & doctor consultation",
                "Apollo 24/7": "https://www.apollo247.com - 24/7 doctor consultation",
                "Tata 1mg": "Online pharmacy & health services",
                "PharmEasy": "https://pharmeasy.in - Medicine & lab tests"
            },
            "📍 Find Nearest Hospital": "Search 'hospitals near me' or use Google Maps"
        }
    
    def _generate_doctor_questions(self, query: str) -> List[str]:
        """Generate helpful questions to ask your doctor"""
        return [
            "❓ What is causing my symptoms?",
            "❓ What tests or evaluations do I need?",
            "❓ What are my treatment options?",
            "❓ What are the benefits and risks of each option?",
            "❓ What should I expect for recovery/management?",
            "❓ What warning signs should I watch for?",
            "❓ When should I follow up?",
            "❓ Are there lifestyle changes that would help?",
            "❓ How will this affect my daily life?",
            "❓ What resources are available for support?"
        ]


# Example usage
if __name__ == "__main__":
    navigator = HealthcareNavigatorAgent()
    
    # Test 1: Symptom query
    result = navigator.navigate(
        query="I have a persistent headache for 3 days",
        age_group="adult",
        duration="3 days",
        severity="moderate"
    )
    print(json.dumps(result, indent=2))
    
    # Test 2: Prevention query
    result = navigator.navigate(
        query="How can I prevent heart disease?",
        age_group="adult"
    )
    print(json.dumps(result, indent=2))
