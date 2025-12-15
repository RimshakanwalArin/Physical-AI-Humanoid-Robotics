"""Logging and metrics infrastructure for RAG chatbot (T003)"""

import json
import logging
from datetime import datetime
from typing import Any, Optional
from pythonjsonlogger import jsonlogger


class QualityMetricsLogger:
    """Logger for RAG quality metrics - hallucination rate, retrieval success, relevance scores"""

    def __init__(self, logger_name: str = "rag_quality"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # JSON formatter for structured logging
        formatter = jsonlogger.JsonFormatter(
            fmt="%(timestamp)s %(level)s %(message)s"
        )

        # Console handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_query(
        self,
        query_id: str,
        query_text: str,
        embedding_model: str,
        student_id: Optional[str] = None
    ):
        """Log incoming query"""
        self.logger.info(
            json.dumps({
                "event": "query_received",
                "query_id": query_id,
                "query_text": query_text[:100],  # Truncate for privacy
                "embedding_model": embedding_model,
                "student_id": student_id,
                "timestamp": datetime.utcnow().isoformat()
            })
        )

    def log_retrieval(
        self,
        query_id: str,
        retrieved_chunk_count: int,
        relevance_scores: list[float],
        retrieval_success: bool
    ):
        """Log retrieval metrics (T014)"""
        self.logger.info(
            json.dumps({
                "event": "retrieval_complete",
                "query_id": query_id,
                "chunk_count": retrieved_chunk_count,
                "avg_relevance": sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0,
                "retrieval_success": retrieval_success,
                "timestamp": datetime.utcnow().isoformat()
            })
        )

    def log_response(
        self,
        query_id: str,
        response_text: str,
        confidence_score: float,
        hallucination_detected: bool,
        latency_ms: float
    ):
        """Log response generation metrics"""
        self.logger.info(
            json.dumps({
                "event": "response_generated",
                "query_id": query_id,
                "confidence_score": confidence_score,
                "hallucination_detected": hallucination_detected,
                "latency_ms": latency_ms,
                "response_length": len(response_text),
                "timestamp": datetime.utcnow().isoformat()
            })
        )

    def log_hallucination(
        self,
        query_id: str,
        detected_external_knowledge: list[str],
        confidence_threshold_missed: bool
    ):
        """Log hallucination detection"""
        self.logger.warning(
            json.dumps({
                "event": "hallucination_detected",
                "query_id": query_id,
                "external_knowledge_snippets": detected_external_knowledge[:3],  # Top 3
                "threshold_issue": confidence_threshold_missed,
                "timestamp": datetime.utcnow().isoformat()
            })
        )


# Singleton instance
quality_logger = QualityMetricsLogger()
