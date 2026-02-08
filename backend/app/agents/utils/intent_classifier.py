"""
Intent Classification Module
Classifies user intent using LLM
"""

from typing import Dict, Any, Optional, Tuple
import json
from language_detector import LanguageDetector  

class IntentClassifier:
    """
    Classifies user intent using LLM
    """
    
    def __init__(self, llm):
        """
        Initialize intent classifier
        
        Args:
            llm: LangChain LLM instance
        """
        self.llm = llm
        self.language_detector = LanguageDetector()
        
        # Intent categories with examples
        self.intent_categories = {
            "BOOKING_AGENT": [
                "book", "appointment", "reserve", "schedule", "cancel", 
                "modify", "reschedule", "change appointment", "rdv"
            ],
            "PATIENT_AGENT": [
                "register", "patient", "cin", "id", "identity", "card",
                "update info", "my information", "patient data"
            ],
            "AVAILABILITY_AGENT": [
                "available", "when", "time", "slot", "free", "open",
                "schedule", "hours", "next available", "tomorrow"
            ],
            "FAQ_AGENT": [
                "question", "how much", "price", "cost", "insurance",
                "service", "clinic", "doctor", "information", "what"
            ]
        }
    
    def classify_with_llm(self, message: str, language: str = "en") -> Tuple[str, float]:
        """
        Classify intent using LLM
        
        Args:
            message: User message
            language: Language code
            
        Returns:
            Tuple of (agent_name, confidence_score)
        """
        from orchestrator.prompt import get_system_prompt
        
        try:
            # Get appropriate system prompt
            system_prompt = get_system_prompt(language)
            
            # Create messages for LLM
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Message to classify: {message}"}
            ]
            
            # Call LLM
            response = self.llm.invoke(messages)
            agent_name = response.content.strip().upper()
            
            # Validate response
            valid_agents = ["BOOKING_AGENT", "PATIENT_AGENT", "AVAILABILITY_AGENT", "FAQ_AGENT"]
            
            if agent_name in valid_agents:
                # Calculate confidence based on response quality
                confidence = self._calculate_confidence(message, agent_name, language)
                return agent_name, confidence
            else:
                # Fallback to rule-based if LLM returns invalid response
                return self.classify_with_rules(message), 0.6
        
        except Exception as e:
            print(f"LLM classification error: {e}")
            # Fallback to rule-based classification
            return self.classify_with_rules(message), 0.5
    
    def classify_with_rules(self, message: str) -> str:
        """
        Fallback rule-based intent classification
        
        Args:
            message: User message
            
        Returns:
            Agent name
        """
        message_lower = message.lower()
        
        # Check each intent category
        for agent_name, keywords in self.intent_categories.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return agent_name
        
        # Default to FAQ if no match
        return "FAQ_AGENT"
    
    def _calculate_confidence(self, message: str, agent_name: str, language: str) -> float:
        """
        Calculate confidence score for classification
        
        Args:
            message: User message
            agent_name: Classified agent name
            language: Language code
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        message_lower = message.lower()
        keywords = self.intent_categories.get(agent_name, [])
        
        # Base confidence
        confidence = 0.5
        
        # Check for keywords in message
        keyword_matches = 0
        for keyword in keywords:
            if keyword in message_lower:
                keyword_matches += 1
        
        # Adjust confidence based on keyword matches
        if keyword_matches > 0:
            confidence += 0.3
        
        # Adjust for message length (longer messages are clearer)
        if len(message.split()) > 3:
            confidence += 0.1
        
        # Cap confidence at 0.95
        return min(confidence, 0.95)
    
    def get_intent_explanation(self, agent_name: str, message: str, language: str) -> Dict[str, Any]:
        """
        Generate explanation for intent classification
        
        Args:
            agent_name: Classified agent
            message: User message
            language: Language code
            
        Returns:
            Explanation dictionary
        """
        explanations = {
            "BOOKING_AGENT": {
                "en": f"User wants appointment-related service: '{message}'",
                "fr": f"L'utilisateur veut un service lié aux rendez-vous: '{message}'",
                "ar": f"المستخدم يريد خدمة متعلقة بالمواعيد: '{message}'",
                "ma": f"L'utilisateur bgha service 3la rdv: '{message}'"
            },
            "PATIENT_AGENT": {
                "en": f"User needs patient registration or verification: '{message}'",
                "fr": f"L'utilisateur a besoin d'inscription ou vérification patient: '{message}'",
                "ar": f"المستخدم يحتاج لتسجيل أو تحقق مريض: '{message}'",
                "ma": f"L'utilisateur 7taj tsjil wla verification patient: '{message}'"
            },
            "AVAILABILITY_AGENT": {
                "en": f"User is asking about availability: '{message}'",
                "fr": f"L'utilisateur demande des disponibilités: '{message}'",
                "ar": f"المستخدم يسأل عن التوفر: '{message}'",
                "ma": f"L'utilisateur kayso2el 3la disponibilité: '{message}'"
            },
            "FAQ_AGENT": {
                "en": f"User has general questions: '{message}'",
                "fr": f"L'utilisateur a des questions générales: '{message}'",
                "ar": f"المستخدم لديه أسئلة عامة: '{message}'",
                "ma": f"L'utilisateur 3ndo questions 3adia: '{message}'"
            }
        }
        
        return {
            "agent": agent_name,
            "explanation": explanations.get(agent_name, {}).get(language, explanations[agent_name]["en"]),
            "confidence_reasoning": "Based on keyword analysis and LLM classification"
        }