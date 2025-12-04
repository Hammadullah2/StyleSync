"""
Output Moderation Guardrails
- Toxicity Filter: Blocks offensive or harmful content
- Hallucination Check: Verifies response references retrieved products
"""

import re
from typing import Tuple, List
from .logger import GuardrailLogger

logger = GuardrailLogger()


class OutputGuardrails:
    """Output moderation guardrails for the RAG pipeline."""
    
    # Toxicity Patterns (simplified - production would use ML model)
    TOXIC_PATTERNS = [
        re.compile(r'\b(hate|kill|attack|destroy|murder)\b', re.IGNORECASE),
        re.compile(r'\b(stupid|idiot|dumb|moron)\b', re.IGNORECASE),
        re.compile(r'\b(racist|sexist|discriminat)\w*\b', re.IGNORECASE),
    ]
    
    # Off-topic patterns (not fashion related)
    OFF_TOPIC_PATTERNS = [
        re.compile(r'\b(politics|politician|election|vote)\b', re.IGNORECASE),
        re.compile(r'\b(religion|religious|church|mosque)\b', re.IGNORECASE),
        re.compile(r'\b(invest|stock|crypto|bitcoin)\b', re.IGNORECASE),
    ]
    
    def moderate(self, response: str, retrieved_products: List[dict]) -> Tuple[bool, str, dict]:
        """
        Moderate output response.
        
        Args:
            response: Generated response text
            retrieved_products: List of products that were retrieved
            
        Returns:
            Tuple of (is_safe, moderated_response, details)
        """
        # Check toxicity
        toxicity_result = self._check_toxicity(response)
        if not toxicity_result[0]:
            logger.log_event("OUTPUT_BLOCKED", "TOXICITY", response[:100], toxicity_result[2])
            return (False, "I apologize, but I cannot provide that response. Let me help you with fashion advice instead.", toxicity_result[2])
        
        # Check hallucination
        hallucination_result = self._check_hallucination(response, retrieved_products)
        if not hallucination_result[0]:
            logger.log_event("OUTPUT_WARNING", "HALLUCINATION", response[:100], hallucination_result[2])
            # Don't block, just log warning
        
        # Check off-topic
        offtopic_result = self._check_off_topic(response)
        if not offtopic_result[0]:
            logger.log_event("OUTPUT_WARNING", "OFF_TOPIC", response[:100], offtopic_result[2])
            # Don't block, just log warning
        
        logger.log_event("OUTPUT_PASSED", "ALL_CHECKS", response[:100], {})
        return (True, response, {"toxicity": "passed", "hallucination": hallucination_result[1]})
    
    def _check_toxicity(self, response: str) -> Tuple[bool, str, dict]:
        """Check for toxic content in response."""
        for pattern in self.TOXIC_PATTERNS:
            match = pattern.search(response)
            if match:
                return (
                    False,
                    "Toxic content detected",
                    {"matched_word": match.group()}
                )
        
        return (True, "No toxicity detected", {})
    
    def _check_hallucination(self, response: str, retrieved_products: List[dict]) -> Tuple[bool, str, dict]:
        """
        Check if response references products that weren't retrieved.
        Simple heuristic: Check if any product names are mentioned.
        """
        if not retrieved_products:
            return (True, "No products to verify", {})
        
        # Get product names
        product_names = [p.get("productDisplayName", "") for p in retrieved_products if p.get("productDisplayName")]
        
        # Check if at least one product is mentioned (or generic terms used)
        response_lower = response.lower()
        
        mentioned = False
        for name in product_names:
            # Check for partial matches (product names can be long)
            name_words = name.lower().split()[:3]  # First 3 words
            if any(word in response_lower for word in name_words if len(word) > 3):
                mentioned = True
                break
        
        # Also accept generic fashion terms
        fashion_terms = ["item", "product", "recommend", "suggest", "style", "outfit", "wear", "fashion"]
        if any(term in response_lower for term in fashion_terms):
            mentioned = True
        
        if not mentioned:
            return (
                False,
                "Response may contain hallucinated products",
                {"retrieved_products": [p.get("productDisplayName") for p in retrieved_products[:3]]}
            )
        
        return (True, "Response references retrieved products", {})
    
    def _check_off_topic(self, response: str) -> Tuple[bool, str, dict]:
        """Check if response goes off-topic from fashion."""
        for pattern in self.OFF_TOPIC_PATTERNS:
            match = pattern.search(response)
            if match:
                return (
                    False,
                    "Off-topic content detected",
                    {"matched_topic": match.group()}
                )
        
        return (True, "Response is on-topic", {})
