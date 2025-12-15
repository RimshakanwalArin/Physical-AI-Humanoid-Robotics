"""Quality monitoring and hallucination detection (T014, T023, T044)"""

import re
from typing import List, Tuple
import logging

from ..logger import quality_logger
from ..config import get_settings

logger = logging.getLogger(__name__)


class QualityMonitor:
    """Monitors RAG response quality, hallucinations, and source validation"""

    def __init__(self):
        self.settings = get_settings()
        # Keywords indicating external knowledge (not from textbook)
        self.external_knowledge_patterns = [
            r"according to\s+(?!the textbook|chapter)",
            r"in my knowledge",
            r"i know that",
            r"in general",
            r"typically",
            r"usually",
            r"from my understanding",
            r"as far as i know",
            r"recent research shows",
            r"studies have found"
        ]

    def detect_hallucination(
        self,
        response_text: str,
        source_chunks: List[str],
        confidence_score: float
    ) -> Tuple[bool, List[str]]:
        """Detect if response contains hallucinated external knowledge (T023)"""

        if not self.settings.hallucination_detection_enabled:
            return False, []

        hallucination_indicators = []

        # Check 1: Low confidence indicates potential hallucination (T023)
        if confidence_score < 0.5:
            hallucination_indicators.append("low_confidence_score")
            logger.warning(f"Low confidence score: {confidence_score}")

        # Check 2: Response longer than source content (possible elaboration)
        source_length = sum(len(chunk) for chunk in source_chunks)
        response_length = len(response_text)

        if source_length > 0 and response_length > source_length * 2:
            hallucination_indicators.append("response_longer_than_sources")
            logger.debug(f"Response {response_length} >> sources {source_length}")

        # Check 3: Keyword pattern matching for external knowledge
        response_lower = response_text.lower()
        detected_patterns = []

        for pattern in self.external_knowledge_patterns:
            if re.search(pattern, response_lower, re.IGNORECASE):
                match = re.search(pattern, response_lower, re.IGNORECASE)
                detected_patterns.append(match.group(0))
                hallucination_indicators.append("external_knowledge_pattern")

        if detected_patterns:
            logger.warning(f"Detected external knowledge patterns: {detected_patterns}")

        # Final verdict: hallucination if multiple indicators
        is_hallucination = len(hallucination_indicators) > 1

        return is_hallucination, detected_patterns

    def validate_source_only_response(
        self,
        response_text: str,
        source_chunks: List[str],
        similarity_scores: List[float]
    ) -> Tuple[bool, str]:
        """Validate that response is sourced strictly from chunks (T020)"""

        if not source_chunks or not similarity_scores:
            return False, "No source chunks provided"

        # Check if average similarity is above threshold
        avg_similarity = sum(similarity_scores) / len(similarity_scores)
        if avg_similarity < self.settings.min_relevance_threshold:
            return False, f"Average similarity {avg_similarity:.2f} below threshold"

        # Check for hallucination patterns
        is_hallucinated, patterns = self.detect_hallucination(
            response_text,
            source_chunks,
            avg_similarity
        )

        if is_hallucinated:
            return False, f"Hallucination detected: {patterns}"

        return True, "Valid source-only response"

    def generate_not_in_textbook_response(self) -> str:
        """Generate response for out-of-scope queries (T022)"""
        return (
            "This topic is not covered in the textbook. "
            "Please refer to one of these topics covered in the book:\n"
            "- Chapter 1: Introduction to Physical AI\n"
            "- Chapter 2: Basics of Humanoid Robotics\n"
            "- Chapter 3: ROS 2 Fundamentals\n"
            "- Chapter 4: Digital Twin Simulation\n"
            "- Chapter 5: Vision-Language-Action Systems\n"
            "- Chapter 6: Capstone Project"
        )

    def log_query_metrics(
        self,
        query_id: str,
        query_text: str,
        retrieved_chunks: int,
        confidence_score: float,
        is_hallucinated: bool,
        latency_ms: float,
        embedding_model: str
    ):
        """Log comprehensive query metrics (T028)"""

        quality_logger.log_query(
            query_id=query_id,
            query_text=query_text,
            embedding_model=embedding_model
        )

        quality_logger.log_response(
            query_id=query_id,
            response_text="",  # Text logged separately
            confidence_score=confidence_score,
            hallucination_detected=is_hallucinated,
            latency_ms=latency_ms
        )

        if is_hallucinated:
            quality_logger.log_hallucination(
                query_id=query_id,
                detected_external_knowledge=[],
                confidence_threshold_missed=confidence_score < 0.5
            )

    def get_retrieval_success_rate(
        self,
        total_queries: int,
        successful_retrievals: int
    ) -> float:
        """Calculate retrieval success rate for monitoring (T014)"""
        if total_queries == 0:
            return 0.0
        return successful_retrievals / total_queries


# Singleton instance
_quality_monitor: QualityMonitor | None = None


def get_quality_monitor() -> QualityMonitor:
    """Get quality monitor singleton"""
    global _quality_monitor
    if _quality_monitor is None:
        _quality_monitor = QualityMonitor()
    return _quality_monitor
