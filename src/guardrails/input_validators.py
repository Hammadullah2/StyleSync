"""
Input Validation Guardrails
- PII Detection: Blocks queries containing personal information
- Prompt Injection Filter: Blocks attempts to manipulate the model
"""

import re
from typing import Tuple
from .logger import GuardrailLogger

logger = GuardrailLogger()


class InputGuardrails:
    """Input validation guardrails for the RAG pipeline."""
    
    # PII Patterns
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    PHONE_PATTERN = re.compile(r'(\+?1?[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    SSN_PATTERN = re.compile(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b')
    
    # Prompt Injection Patterns
    INJECTION_PATTERNS = [
        re.compile(r'ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?)', re.IGNORECASE),
        re.compile(r'disregard\s+(all\s+)?(previous|prior|above)', re.IGNORECASE),
        re.compile(r'forget\s+(everything|all|your)\s+(instructions?|rules?)', re.IGNORECASE),
        re.compile(r'you\s+are\s+now\s+(a|an)\s+', re.IGNORECASE),
        re.compile(r'pretend\s+(to\s+be|you\s+are)', re.IGNORECASE),
        re.compile(r'act\s+as\s+(if|a|an)', re.IGNORECASE),
        re.compile(r'system\s*:\s*', re.IGNORECASE),
        re.compile(r'<\s*system\s*>', re.IGNORECASE),
        re.compile(r'jailbreak', re.IGNORECASE),
        re.compile(r'bypass\s+(safety|filter|guard)', re.IGNORECASE),
    ]
    
    def validate(self, query: str) -> Tuple[bool, str, dict]:
        """
        Validate input query against all guardrails.
        
        Returns:
            Tuple of (is_valid, message, details)
        """
        # Check PII
        pii_result = self._check_pii(query)
        if not pii_result[0]:
            logger.log_event("INPUT_BLOCKED", "PII_DETECTED", query, pii_result[2])
            return pii_result
        
        # Check Prompt Injection
        injection_result = self._check_prompt_injection(query)
        if not injection_result[0]:
            logger.log_event("INPUT_BLOCKED", "PROMPT_INJECTION", query, injection_result[2])
            return injection_result
        
        logger.log_event("INPUT_PASSED", "ALL_CHECKS", query, {})
        return (True, "Query passed all input validations", {})
    
    def _check_pii(self, query: str) -> Tuple[bool, str, dict]:
        """Check for PII in the query."""
        detected = {}
        
        if self.EMAIL_PATTERN.search(query):
            detected["email"] = True
        if self.PHONE_PATTERN.search(query):
            detected["phone"] = True
        if self.SSN_PATTERN.search(query):
            detected["ssn"] = True
        if self.CREDIT_CARD_PATTERN.search(query):
            detected["credit_card"] = True
        
        if detected:
            return (
                False,
                "Query blocked: Personal information detected. Please remove sensitive data.",
                {"pii_types": list(detected.keys())}
            )
        
        return (True, "No PII detected", {})
    
    def _check_prompt_injection(self, query: str) -> Tuple[bool, str, dict]:
        """Check for prompt injection attempts."""
        for pattern in self.INJECTION_PATTERNS:
            match = pattern.search(query)
            if match:
                return (
                    False,
                    "Query blocked: Potentially harmful prompt pattern detected.",
                    {"matched_pattern": match.group()}
                )
        
        return (True, "No injection detected", {})
