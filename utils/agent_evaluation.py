"""
Agent Evaluation Framework
Evaluates agent performance, quality, and effectiveness
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from utils.observability import AgentLogger, metrics

logger = AgentLogger("AgentEvaluation")


class AgentEvaluator:
    """
    Evaluates agent performance across multiple dimensions:
    - Accuracy: How correct are the results?
    - Relevance: How relevant to the query?
    - Completeness: Does it cover all aspects?
    - Quality: Overall output quality
    - Performance: Speed and efficiency
    - Accessibility: WCAG compliance for accessibility agents
    """
    
    def __init__(self):
        self.evaluation_history = []
        
    def evaluate_research_agent(self, query: str, results: List[Dict], 
                               duration: float) -> Dict:
        """Evaluate Research Agent performance"""
        
        # Relevance scoring
        relevance_score = self._score_relevance(query, results)
        
        # Coverage scoring
        coverage_score = self._score_coverage(results)
        
        # Quality scoring
        quality_score = self._score_quality(results)
        
        # Performance scoring (speed)
        performance_score = self._score_performance(duration, target=3.0)
        
        # Overall score
        overall_score = (
            relevance_score * 0.3 +
            coverage_score * 0.3 +
            quality_score * 0.2 +
            performance_score * 0.2
        )
        
        evaluation = {
            "agent": "ResearchAgent",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "scores": {
                "relevance": round(relevance_score, 2),
                "coverage": round(coverage_score, 2),
                "quality": round(quality_score, 2),
                "performance": round(performance_score, 2),
                "overall": round(overall_score, 2)
            },
            "metrics": {
                "results_count": len(results),
                "duration_seconds": round(duration, 2),
                "avg_snippet_length": self._avg_snippet_length(results)
            },
            "rating": self._get_rating(overall_score),
            "recommendations": self._generate_recommendations("research", overall_score, {
                "relevance": relevance_score,
                "coverage": coverage_score,
                "performance": performance_score
            })
        }
        
        self.evaluation_history.append(evaluation)
        metrics.record_metric("agent_evaluation_score", overall_score, {"agent": "research"})
        
        logger.info(f"Research Agent evaluation: {overall_score:.2f}/100")
        return evaluation
    
    def evaluate_education_agent(self, query: str, response: Dict, 
                                 duration: float) -> Dict:
        """Evaluate Education Tutor Agent"""
        
        # Educational value
        educational_score = self._score_educational_value(response)
        
        # Clarity and comprehension
        clarity_score = self._score_clarity(response)
        
        # Completeness
        completeness_score = self._score_educational_completeness(response)
        
        # Performance
        performance_score = self._score_performance(duration, target=2.0)
        
        overall_score = (
            educational_score * 0.4 +
            clarity_score * 0.3 +
            completeness_score * 0.2 +
            performance_score * 0.1
        )
        
        evaluation = {
            "agent": "EducationTutorAgent",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "scores": {
                "educational_value": round(educational_score, 2),
                "clarity": round(clarity_score, 2),
                "completeness": round(completeness_score, 2),
                "performance": round(performance_score, 2),
                "overall": round(overall_score, 2)
            },
            "metrics": {
                "has_examples": "examples" in response,
                "has_practice": "problems" in response,
                "has_resources": "resources" in response,
                "duration_seconds": round(duration, 2)
            },
            "rating": self._get_rating(overall_score),
            "recommendations": self._generate_recommendations("education", overall_score, {
                "educational": educational_score,
                "clarity": clarity_score
            })
        }
        
        self.evaluation_history.append(evaluation)
        metrics.record_metric("agent_evaluation_score", overall_score, {"agent": "education"})
        
        logger.info(f"Education Agent evaluation: {overall_score:.2f}/100")
        return evaluation
    
    def evaluate_healthcare_agent(self, query: str, response: Dict, 
                                  duration: float) -> Dict:
        """Evaluate Healthcare Navigator Agent"""
        
        # Safety scoring (most important)
        safety_score = self._score_healthcare_safety(response)
        
        # Information quality
        info_quality_score = self._score_healthcare_info_quality(response)
        
        # Urgency assessment accuracy
        urgency_score = self._score_urgency_assessment(response)
        
        # Performance
        performance_score = self._score_performance(duration, target=2.0)
        
        overall_score = (
            safety_score * 0.5 +  # Safety is paramount
            info_quality_score * 0.25 +
            urgency_score * 0.15 +
            performance_score * 0.1
        )
        
        evaluation = {
            "agent": "HealthcareNavigatorAgent",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "scores": {
                "safety": round(safety_score, 2),
                "information_quality": round(info_quality_score, 2),
                "urgency_assessment": round(urgency_score, 2),
                "performance": round(performance_score, 2),
                "overall": round(overall_score, 2)
            },
            "metrics": {
                "has_disclaimer": "disclaimer" in str(response),
                "urgency_level": response.get("metadata", {}).get("urgency_level"),
                "has_resources": "resources" in response,
                "duration_seconds": round(duration, 2)
            },
            "rating": self._get_rating(overall_score),
            "recommendations": self._generate_recommendations("healthcare", overall_score, {
                "safety": safety_score,
                "quality": info_quality_score
            })
        }
        
        self.evaluation_history.append(evaluation)
        metrics.record_metric("agent_evaluation_score", overall_score, {"agent": "healthcare"})
        
        logger.info(f"Healthcare Agent evaluation: {overall_score:.2f}/100")
        return evaluation
    
    def evaluate_accessibility_agent(self, content: Dict, validation: Dict) -> Dict:
        """Evaluate Accessibility Agent"""
        
        # WCAG compliance
        wcag_score = validation.get('accessibility_score', 0)
        
        # Screen reader optimization
        screen_reader_score = self._score_screen_reader_optimization(content)
        
        # Audio readiness
        audio_score = self._score_audio_readiness(content)
        
        # Overall accessibility
        overall_score = (
            wcag_score * 0.5 +
            screen_reader_score * 0.3 +
            audio_score * 0.2
        )
        
        evaluation = {
            "agent": "AccessibilityAgent",
            "timestamp": datetime.now().isoformat(),
            "scores": {
                "wcag_compliance": round(wcag_score, 2),
                "screen_reader": round(screen_reader_score, 2),
                "audio_ready": round(audio_score, 2),
                "overall": round(overall_score, 2)
            },
            "metrics": {
                "wcag_level": validation.get('wcag_level', 'Unknown'),
                "compliant": validation.get('compliant', False),
                "issues_count": len(validation.get('issues', []))
            },
            "rating": self._get_rating(overall_score),
            "recommendations": self._generate_recommendations("accessibility", overall_score, {
                "wcag": wcag_score,
                "screen_reader": screen_reader_score
            })
        }
        
        self.evaluation_history.append(evaluation)
        metrics.record_metric("agent_evaluation_score", overall_score, {"agent": "accessibility"})
        
        logger.info(f"Accessibility Agent evaluation: {overall_score:.2f}/100")
        return evaluation
    
    # Scoring methods
    
    def _score_relevance(self, query: str, results: List[Dict]) -> float:
        """Score how relevant results are to query"""
        if not results:
            return 0.0
        
        query_keywords = set(query.lower().split())
        relevance_scores = []
        
        for result in results:
            text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
            matches = sum(1 for keyword in query_keywords if keyword in text)
            relevance_scores.append(min(matches / len(query_keywords) * 100, 100))
        
        return sum(relevance_scores) / len(relevance_scores)
    
    def _score_coverage(self, results: List[Dict]) -> float:
        """Score breadth of coverage"""
        if not results:
            return 0.0
        
        # Good coverage: 3-10 results
        count = len(results)
        if count == 0:
            return 0.0
        elif count < 3:
            return count * 33.3
        elif count <= 10:
            return 100.0
        else:
            return max(100 - (count - 10) * 5, 70)  # Penalize too many results
    
    def _score_quality(self, results: List[Dict]) -> float:
        """Score quality of results"""
        if not results:
            return 0.0
        
        quality_points = 0
        max_points = len(results) * 4
        
        for result in results:
            if result.get('title'):
                quality_points += 1
            if result.get('url'):
                quality_points += 1
            if result.get('snippet') and len(result['snippet']) > 50:
                quality_points += 1
            if result.get('source'):
                quality_points += 1
        
        return (quality_points / max_points) * 100 if max_points > 0 else 0
    
    def _score_performance(self, duration: float, target: float) -> float:
        """Score based on speed"""
        if duration <= target:
            return 100.0
        elif duration <= target * 2:
            return 100 - ((duration - target) / target * 50)
        else:
            return max(50 - ((duration - target * 2) / target * 10), 0)
    
    def _score_educational_value(self, response: Dict) -> float:
        """Score educational value"""
        score = 50  # Base score
        
        if 'explanation' in response:
            score += 20
        if 'examples' in response:
            score += 15
        if 'key_points' in response:
            score += 10
        if 'recommendations' in response:
            score += 5
        
        return min(score, 100)
    
    def _score_clarity(self, response: Dict) -> float:
        """Score clarity of explanation"""
        score = 60  # Base score
        
        explanation = response.get('explanation', '')
        if len(explanation) > 100:
            score += 20
        if 'step' in str(response).lower():
            score += 10
        if 'example' in str(response).lower():
            score += 10
        
        return min(score, 100)
    
    def _score_educational_completeness(self, response: Dict) -> float:
        """Score completeness of educational content"""
        components = ['explanation', 'examples', 'practice', 'resources', 'recommendations']
        present = sum(1 for comp in components if comp in str(response).lower())
        return (present / len(components)) * 100
    
    def _score_healthcare_safety(self, response: Dict) -> float:
        """Score healthcare safety measures"""
        score = 0
        
        # Disclaimer present
        if 'disclaimer' in str(response).lower():
            score += 40
        
        # Urgency assessment present
        if 'urgency' in response:
            score += 30
        
        # Emergency detection
        if response.get('metadata', {}).get('urgency_level') == 'emergency':
            score += 20
        
        # Resources provided
        if 'resources' in response:
            score += 10
        
        return score
    
    def _score_healthcare_info_quality(self, response: Dict) -> float:
        """Score quality of health information"""
        score = 50
        
        if 'overview' in response or 'information' in response:
            score += 25
        if 'resources' in response:
            score += 15
        if 'when_to_see_doctor' in response:
            score += 10
        
        return min(score, 100)
    
    def _score_urgency_assessment(self, response: Dict) -> float:
        """Score urgency assessment accuracy"""
        # This is a simplified version
        # In production, would compare against expert labels
        
        urgency_level = response.get('metadata', {}).get('urgency_level')
        
        if urgency_level in ['emergency', 'urgent', 'soon', 'routine', 'self_care']:
            return 85  # Has valid urgency level
        return 50  # Missing or invalid
    
    def _score_screen_reader_optimization(self, content: Dict) -> float:
        """Score screen reader optimization"""
        score = 60
        
        if content.get('semantic_structure'):
            score += 20
        if content.get('alt_text'):
            score += 10
        if content.get('navigation'):
            score += 10
        
        return min(score, 100)
    
    def _score_audio_readiness(self, content: Dict) -> float:
        """Score audio readiness"""
        score = 60
        
        if content.get('audio_description'):
            score += 20
        if content.get('ssml'):
            score += 10
        if content.get('speech_chunks'):
            score += 10
        
        return min(score, 100)
    
    def _avg_snippet_length(self, results: List[Dict]) -> int:
        """Calculate average snippet length"""
        if not results:
            return 0
        snippets = [len(r.get('snippet', '')) for r in results]
        return sum(snippets) // len(snippets) if snippets else 0
    
    def _get_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 90:
            return "Excellent ⭐⭐⭐⭐⭐"
        elif score >= 80:
            return "Very Good ⭐⭐⭐⭐"
        elif score >= 70:
            return "Good ⭐⭐⭐"
        elif score >= 60:
            return "Satisfactory ⭐⭐"
        else:
            return "Needs Improvement ⭐"
    
    def _generate_recommendations(self, agent_type: str, overall_score: float, 
                                 sub_scores: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if overall_score >= 90:
            recommendations.append("✅ Agent performing excellently!")
        
        if agent_type == "research":
            if sub_scores.get('relevance', 100) < 70:
                recommendations.append("🔍 Improve query matching and relevance scoring")
            if sub_scores.get('coverage', 100) < 70:
                recommendations.append("📚 Expand search sources for better coverage")
            if sub_scores.get('performance', 100) < 70:
                recommendations.append("⚡ Optimize search speed and caching")
        
        elif agent_type == "education":
            if sub_scores.get('educational', 100) < 70:
                recommendations.append("📖 Add more examples and practice problems")
            if sub_scores.get('clarity', 100) < 70:
                recommendations.append("💡 Simplify explanations and use clearer language")
        
        elif agent_type == "healthcare":
            if sub_scores.get('safety', 100) < 90:
                recommendations.append("⚠️ CRITICAL: Ensure all safety disclaimers are prominent")
            if sub_scores.get('quality', 100) < 70:
                recommendations.append("📋 Enhance information depth and resources")
        
        elif agent_type == "accessibility":
            if sub_scores.get('wcag', 100) < 90:
                recommendations.append("♿ Improve WCAG compliance to Level AA")
            if sub_scores.get('screen_reader', 100) < 80:
                recommendations.append("🔊 Enhance screen reader optimization")
        
        if not recommendations:
            recommendations.append("🎯 Maintain current quality standards")
        
        return recommendations
    
    def get_evaluation_summary(self) -> Dict:
        """Get summary of all evaluations"""
        if not self.evaluation_history:
            return {"message": "No evaluations yet"}
        
        agents = {}
        for eval_data in self.evaluation_history:
            agent_name = eval_data['agent']
            if agent_name not in agents:
                agents[agent_name] = {
                    "evaluations": 0,
                    "avg_score": 0,
                    "scores": []
                }
            
            agents[agent_name]['evaluations'] += 1
            agents[agent_name]['scores'].append(eval_data['scores']['overall'])
        
        # Calculate averages
        for agent_name in agents:
            scores = agents[agent_name]['scores']
            agents[agent_name]['avg_score'] = round(sum(scores) / len(scores), 2)
            agents[agent_name]['min_score'] = round(min(scores), 2)
            agents[agent_name]['max_score'] = round(max(scores), 2)
            del agents[agent_name]['scores']  # Remove raw scores
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "agents": agents,
            "latest_evaluation": self.evaluation_history[-1] if self.evaluation_history else None
        }
    
    def export_evaluations(self, filepath: str):
        """Export evaluation history to JSON"""
        with open(filepath, 'w') as f:
            json.dump({
                "evaluations": self.evaluation_history,
                "summary": self.get_evaluation_summary()
            }, f, indent=2)
        
        logger.info(f"Exported {len(self.evaluation_history)} evaluations to {filepath}")


# Global evaluator instance
evaluator = AgentEvaluator()
