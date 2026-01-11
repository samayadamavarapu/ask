from typing import Tuple, Optional

class SafetyGuard:
    """
    Handles safety checks for user queries and responses.
    """
    
    PREGNANCY_KEYWORDS = [
        "pregnant", "pregnancy", "trimester", "expecting baby", "prenatal"
    ]
    
    DISEASE_KEYWORDS = [
        "hernia", "glaucoma", "blood pressure", "surgery", "fracture", 
        "detached retina", "sciatica", "slip disc", "epilepsy", "heart condition",
        "chronic pain", "injury", "diagnose", "cure", "treatment", "medicine"
    ]
    
    CRITICAL_KEYWORDS = ["suicide", "kill", "die", "death", "harm"]

    def check_query(self, query: str) -> Tuple[bool, str, Optional[str]]:
        """
        Analyzes the query for safety.
        Returns: (is_unsafe, safety_flag, message)
        """
        query_lower = query.lower()
        
        # 1. Critical Harm Detection
        if any(word in query_lower for word in self.CRITICAL_KEYWORDS):
            return True, "BLOCKED", "I cannot assist with this query. If you are in distress, please contact emergency services."

        # 2. Pregnancy Detection
        if any(word in query_lower for word in self.PREGNANCY_KEYWORDS):
            return True, "UNSAFE", self._get_safety_message("pregnancy")
            
        # 3. Disease/Medical Condition Detection
        if any(word in query_lower for word in self.DISEASE_KEYWORDS):
            return True, "UNSAFE", self._get_safety_message("medical")

        return False, "SAFE", None

    def _get_safety_message(self, context_type: str) -> str:
        """
        Returns the mandatory structured safety response.
        """
        base_msg = "Your question touches on an area that can be risky without personalized guidance.\n\n"
        
        if context_type == "pregnancy":
            base_msg += "Instead of deep twists or inversions, consider gentle prenatal poses and breathing work.\n"
        elif context_type == "medical":
            base_msg += "Instead of advanced poses, consider gentle restorative poses and breathing work.\n"
            
        base_msg += "Please consult a doctor or certified yoga therapist before attempting these poses."
        return base_msg

_safety_guard = None
def get_safety_guard() -> SafetyGuard:
    global _safety_guard
    if _safety_guard is None:
        _safety_guard = SafetyGuard()
    return _safety_guard
