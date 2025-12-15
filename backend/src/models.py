"""Data models for RAG chatbot (T035, T040)"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class Citation(BaseModel):
    """Citation model pointing to source in textbook (T035)"""

    chunk_id: str = Field(..., description="UUID of source chunk")
    chapter_name: str = Field(..., description="Chapter name (e.g., 'Chapter 1: Introduction to Physical AI')")
    section_name: str = Field(..., description="Section name")
    section_number: str = Field(..., description="Section number (e.g., '1.2', '2.3.4')")
    page_number: Optional[int] = Field(None, description="Page number in textbook")
    link_anchor: str = Field(..., description="URL anchor for direct link")


class IndexedChunk(BaseModel):
    """Textbook chunk with embedding and metadata (T040)"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chapter_id: str = Field(..., description="Chapter identifier")
    section_name: str = Field(..., description="Section title")
    section_number: str = Field(..., description="Section number")
    content_text: str = Field(..., description="Text content of chunk")
    embedding_vector: Optional[List[float]] = Field(None, description="384-dim embedding vector")
    embedding_model: str = Field(default="bge-small-en-v1.5", description="Model used for embedding")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    page_number: Optional[int] = Field(None, description="Page number")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "chunk-123",
                "chapter_id": "ch1",
                "section_name": "Embodied Intelligence",
                "section_number": "1.2",
                "content_text": "Embodied intelligence refers to...",
                "embedding_model": "bge-small-en-v1.5",
                "page_number": 12
            }
        }


class RagQuery(BaseModel):
    """Student question/query"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_text: str = Field(..., min_length=10, max_length=1000)
    student_id: Optional[str] = Field(None, description="Optional student ID")
    embedding_model: str = Field(default="bge-small-en-v1.5")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RagResponse(BaseModel):
    """Generated RAG response with citations (T041)"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_id: str = Field(..., description="FK to RagQuery")
    query_text: str = Field(...)
    response_text: str = Field(..., description="Formatted markdown answer")
    sources: List[Citation] = Field(default_factory=list, description="Source citations")
    source_chunk_ids: List[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    hallucination_detected: bool = Field(default=False)
    latency_ms: float = Field(...)
    embedding_model: str = Field(default="bge-small-en-v1.5")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "response-123",
                "query_id": "query-456",
                "query_text": "What is embodied intelligence?",
                "response_text": "Embodied intelligence refers to...\n\n**Sources:**\n- Chapter 1: Introduction to Physical AI",
                "sources": [
                    {
                        "chunk_id": "chunk-1",
                        "chapter_name": "Chapter 1: Introduction to Physical AI",
                        "section_name": "Embodied Intelligence",
                        "section_number": "1.2",
                        "page_number": 12,
                        "link_anchor": "ch1-embodied-intelligence"
                    }
                ],
                "confidence_score": 0.87,
                "hallucination_detected": False,
                "latency_ms": 340,
                "embedding_model": "bge-small-en-v1.5"
            }
        }
