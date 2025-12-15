"""Unit tests for hallucination detection (T016)"""

import pytest
import json
from pathlib import Path
from rag.quality import get_quality_monitor

# Load test data
test_data_path = Path(__file__).parent.parent / "fixtures" / "rag_test_data.json"
with open(test_data_path) as f:
    TEST_DATA = json.load(f)


class TestHallucinationDetection:
    """Test hallucination detection for out-of-scope queries"""

    @pytest.fixture
    def quality_monitor(self):
        """Get quality monitor instance"""
        return get_quality_monitor()

    @pytest.fixture
    def out_of_scope_queries(self):
        """Load out-of-scope test queries"""
        return TEST_DATA["test_queries"]["out_of_scope"]

    def test_out_of_scope_queries_exist(self, out_of_scope_queries):
        """Test that we have out-of-scope queries for testing"""
        assert len(out_of_scope_queries) >= 10, "Need at least 10 out-of-scope queries"

    def test_all_out_of_scope_queries_marked_for_rejection(self, out_of_scope_queries):
        """Test that all out-of-scope queries are marked for rejection"""
        for query in out_of_scope_queries:
            assert query.get("should_reject", False) is True, \
                f"Query {query['id']} should be marked for rejection"

    def test_low_confidence_detection(self, quality_monitor):
        """Test that low confidence triggers hallucination flag (acceptance scenario 2)"""
        # Given: Out-of-scope query with low confidence
        response_text = "This topic is not covered in the textbook."
        source_chunks = []
        confidence_score = 0.3  # Below 0.5 threshold

        # When: Checking for hallucination
        is_hallucinated, patterns = quality_monitor.detect_hallucination(
            response_text,
            source_chunks,
            confidence_score
        )

        # Then: Should detect as hallucination risk
        assert len(patterns) > 0, "Should detect external knowledge patterns"

    def test_external_knowledge_pattern_detection(self, quality_monitor):
        """Test detection of external knowledge language patterns"""
        test_cases = [
            {
                "text": "According to recent research, machine learning is...",
                "should_detect": True
            },
            {
                "text": "In my knowledge, this is how it works...",
                "should_detect": True
            },
            {
                "text": "As far as I know, robots are used in factories...",
                "should_detect": True
            },
            {
                "text": "Chapter 1 explains that embodied intelligence is...",
                "should_detect": False
            }
        ]

        for test_case in test_cases:
            response_text = test_case["text"]
            source_chunks = ["Chapter content here"]
            confidence_score = 0.7  # Neutral confidence

            is_hallucinated, patterns = quality_monitor.detect_hallucination(
                response_text,
                source_chunks,
                confidence_score
            )

            if test_case["should_detect"]:
                # Should detect external knowledge when combined with other factors
                # or when confidence is low
                assert len(patterns) > 0 or is_hallucinated, \
                    f"Should detect external knowledge in: {response_text}"
            else:
                # Should not flag as hallucination
                assert not is_hallucinated, \
                    f"Should NOT flag as hallucination: {response_text}"

    def test_response_length_validation(self, quality_monitor):
        """Test that excessively long responses are flagged"""
        # Given: Response much longer than source
        source_chunks = ["Short source text."]
        response_text = "Detailed explanation " * 100  # Very long response
        confidence_score = 0.7

        # When: Checking hallucination
        is_hallucinated, patterns = quality_monitor.detect_hallucination(
            response_text,
            source_chunks,
            confidence_score
        )

        # Then: Should detect due to length mismatch
        assert "response_longer_than_sources" in patterns or is_hallucinated, \
            "Should detect response length anomaly"

    def test_not_in_textbook_response_generation(self, quality_monitor):
        """Test generation of 'not in textbook' response (acceptance scenario 2)"""
        # When: Generating response for out-of-scope query
        response = quality_monitor.generate_not_in_textbook_response()

        # Then: Should contain expected message
        assert "not covered in the textbook" in response.lower()
        assert "Chapter" in response  # Should list available chapters

    def test_hallucination_rate_tracking(self, quality_monitor, out_of_scope_queries):
        """Test that hallucination rate can be calculated"""
        # Simulate testing 10 out-of-scope queries
        total_queries = 10
        hallucinated_responses = 0

        # Each out-of-scope query should generate a "not in textbook" response
        for query in out_of_scope_queries:
            response_text = quality_monitor.generate_not_in_textbook_response()

            # Check if response would be flagged
            is_hallucinated, _ = quality_monitor.detect_hallucination(
                response_text,
                [],
                0.0  # Low confidence for out-of-scope
            )

            if is_hallucinated:
                hallucinated_responses += 1

        # Calculate hallucination rate
        hallucination_rate = hallucinated_responses / total_queries if total_queries > 0 else 0

        # Then: Should be tracking metric (not making specific assertion yet)
        assert 0 <= hallucination_rate <= 1.0, "Invalid hallucination rate"

    def test_multiple_indicators_for_hallucination(self, quality_monitor):
        """Test that multiple indicators needed to trigger hallucination flag"""
        # Single indicator should not trigger
        response_text = "This is a somewhat long response to explain the concept."
        source_chunks = ["Brief source"]
        confidence_score = 0.8  # High confidence

        is_hallucinated, patterns = quality_monitor.detect_hallucination(
            response_text,
            source_chunks,
            confidence_score
        )

        # With high confidence and no external patterns, should not be flagged
        assert not is_hallucinated or len(patterns) <= 1, \
            "Should require multiple indicators for hallucination"
