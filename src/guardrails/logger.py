"""
Guardrail Event Logger
Logs all guardrail events for monitoring and auditing.
"""

import logging
import json
from datetime import datetime
from pathlib import Path

# Setup guardrail-specific logger
guardrail_logger = logging.getLogger("guardrails")
guardrail_logger.setLevel(logging.INFO)

# File handler for guardrail events
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(log_dir / "guardrails.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
guardrail_logger.addHandler(file_handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - GUARDRAIL - %(message)s'))
guardrail_logger.addHandler(console_handler)


class GuardrailLogger:
    """Logger for guardrail events."""
    
    def log_event(self, event_type: str, rule: str, content: str, details: dict):
        """
        Log a guardrail event.
        
        Args:
            event_type: Type of event (INPUT_BLOCKED, OUTPUT_BLOCKED, etc.)
            rule: Which rule was triggered
            content: The content that triggered (truncated)
            details: Additional details about the event
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "rule": rule,
            "content_preview": content[:100] if content else "",
            "details": details
        }
        
        # Log based on severity
        if "BLOCKED" in event_type:
            guardrail_logger.warning(json.dumps(event))
        elif "WARNING" in event_type:
            guardrail_logger.info(json.dumps(event))
        else:
            guardrail_logger.debug(json.dumps(event))
    
    def get_stats(self, log_file: Path = None) -> dict:
        """Get statistics from guardrail logs."""
        if log_file is None:
            log_file = log_dir / "guardrails.log"
        
        stats = {
            "total_events": 0,
            "blocked_inputs": 0,
            "blocked_outputs": 0,
            "warnings": 0,
            "by_rule": {}
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "INPUT_BLOCKED" in line:
                        stats["blocked_inputs"] += 1
                    elif "OUTPUT_BLOCKED" in line:
                        stats["blocked_outputs"] += 1
                    elif "WARNING" in line:
                        stats["warnings"] += 1
                    stats["total_events"] += 1
        except FileNotFoundError:
            pass
        
        return stats
