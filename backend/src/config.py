"""Configuration management for RAG chatbot backend (T002)"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings with support for embedding model switching"""

    # Environment
    environment: str = "development"
    debug: bool = True

    # Embedding Model Configuration (T002)
    embedding_model: Literal[
        "all-MiniLM-L6-v2",
        "bge-small-en-v1.5",
        "e5-small-v2"
    ] = "bge-small-en-v1.5"

    embedding_dimension: int = 384
    embedding_cache_size: int = 1000

    # Retrieval Configuration
    top_k_retrieval: int = 5
    min_relevance_threshold: float = 0.70

    # Qdrant Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection_name: str = "documents"

    # Neon PostgreSQL Configuration
    neon_db_url: str | None = None

    # Quality Monitoring (T002)
    log_quality_metrics: bool = True
    hallucination_detection_enabled: bool = True

    # Performance
    max_query_length: int = 1000
    min_query_length: int = 10
    query_timeout_seconds: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings singleton"""
    return Settings()
