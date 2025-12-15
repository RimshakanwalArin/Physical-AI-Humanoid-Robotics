"""RAG service models and data classes"""

from dataclasses import dataclass
from typing import List


@dataclass
class EmbeddingMetadata:
    """Metadata about an embedding operation"""
    model_name: str
    dimension: int
    batch_size: int
    total_chunks: int
    processing_time_seconds: float


@dataclass
class RetrievalMetrics:
    """Metrics from retrieval operation"""
    total_chunks_searched: int
    chunks_above_threshold: int
    avg_similarity: float
    max_similarity: float
    min_similarity: float
