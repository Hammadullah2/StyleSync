"""
Unit tests for metrics module
"""
import pytest
from src.metrics import MetricsTracker, create_metrics_tracker


class TestMetricsTracker:
    """Tests for MetricsTracker."""
    
    def test_create_tracker(self):
        tracker = create_metrics_tracker()
        assert tracker is not None
        assert isinstance(tracker, MetricsTracker)
    
    def test_start_end_request(self):
        tracker = MetricsTracker()
        tracker.start_request()
        assert tracker.start_time is not None
        tracker.end_request('success')
    
    def test_track_retrieval(self):
        tracker = MetricsTracker()
        tracker.track_retrieval(0.5)
        assert tracker.retrieval_time == 0.5
    
    def test_track_generation(self):
        tracker = MetricsTracker()
        tracker.track_generation(2.0, input_tokens=100, output_tokens=200)
        assert tracker.generation_time == 2.0
        assert tracker.input_tokens == 100
        assert tracker.output_tokens == 200
    
    def test_track_guardrail_passed(self):
        tracker = MetricsTracker()
        tracker.track_guardrail('input', 'pii', True)
        # Should not raise
    
    def test_track_guardrail_blocked(self):
        tracker = MetricsTracker()
        tracker.track_guardrail('input', 'pii', False)
        # Should not raise
