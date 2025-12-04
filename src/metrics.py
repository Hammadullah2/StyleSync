"""
LLM Metrics for Prometheus
Tracks latency, token usage, cost, and guardrail violations.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
from functools import wraps

# --- Latency Metrics ---
LLM_REQUEST_LATENCY = Histogram(
    'llm_request_latency_seconds',
    'Time spent processing LLM requests',
    ['endpoint', 'status'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

RETRIEVAL_LATENCY = Histogram(
    'retrieval_latency_seconds',
    'Time spent on vector retrieval',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
)

GENERATION_LATENCY = Histogram(
    'generation_latency_seconds',
    'Time spent on LLM generation',
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

# --- Token Usage Metrics ---
TOKEN_USAGE = Counter(
    'llm_token_usage_total',
    'Total tokens used',
    ['type']  # input, output
)

# --- Cost Metrics ---
LLM_COST = Counter(
    'llm_cost_usd_total',
    'Estimated LLM cost in USD',
    ['model']
)

# --- Request Metrics ---
REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['endpoint', 'status']
)

# --- Guardrail Metrics ---
GUARDRAIL_VIOLATIONS = Counter(
    'guardrail_violations_total',
    'Total guardrail violations',
    ['type', 'rule']  # input/output, specific rule
)

GUARDRAIL_CHECKS = Counter(
    'guardrail_checks_total',
    'Total guardrail checks performed',
    ['type', 'result']  # input/output, passed/blocked
)

# --- Active Requests ---
ACTIVE_REQUESTS = Gauge(
    'llm_active_requests',
    'Number of currently active LLM requests'
)


class MetricsTracker:
    """Helper class to track metrics during request processing."""
    
    # Gemini pricing (approximate)
    PRICING = {
        'gemini-2.5-flash': {'input': 0.00025, 'output': 0.0005}  # per 1K tokens
    }
    
    def __init__(self):
        self.start_time = None
        self.retrieval_time = 0
        self.generation_time = 0
        self.input_tokens = 0
        self.output_tokens = 0
    
    def start_request(self):
        """Start tracking a request."""
        self.start_time = time.time()
        ACTIVE_REQUESTS.inc()
    
    def end_request(self, status: str = 'success'):
        """End tracking a request."""
        if self.start_time:
            latency = time.time() - self.start_time
            LLM_REQUEST_LATENCY.labels(endpoint='/chat', status=status).observe(latency)
            REQUEST_COUNT.labels(endpoint='/chat', status=status).inc()
        ACTIVE_REQUESTS.dec()
    
    def track_retrieval(self, duration: float):
        """Track retrieval latency."""
        self.retrieval_time = duration
        RETRIEVAL_LATENCY.observe(duration)
    
    def track_generation(self, duration: float, input_tokens: int = 0, output_tokens: int = 0):
        """Track generation latency and token usage."""
        self.generation_time = duration
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        
        GENERATION_LATENCY.observe(duration)
        TOKEN_USAGE.labels(type='input').inc(input_tokens)
        TOKEN_USAGE.labels(type='output').inc(output_tokens)
        
        # Estimate cost
        model = 'gemini-2.5-flash'
        if model in self.PRICING:
            cost = (input_tokens / 1000 * self.PRICING[model]['input'] +
                   output_tokens / 1000 * self.PRICING[model]['output'])
            LLM_COST.labels(model=model).inc(cost)
    
    def track_guardrail(self, guard_type: str, rule: str, passed: bool):
        """Track guardrail check results."""
        result = 'passed' if passed else 'blocked'
        GUARDRAIL_CHECKS.labels(type=guard_type, result=result).inc()
        
        if not passed:
            GUARDRAIL_VIOLATIONS.labels(type=guard_type, rule=rule).inc()


# Global metrics tracker factory
def create_metrics_tracker() -> MetricsTracker:
    return MetricsTracker()
