from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str
    session_id: str

class Citation(BaseModel):
    chapter_id: str
    chapter_title: str
    section_id: str
    section_title: str
    excerpt: str

class ChatResponse(BaseModel):
    status: str
    answer: str
    sources: List[Citation]
    latency_ms: int

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    components: dict

class ErrorResponse(BaseModel):
    error: str
    message: str
    status: int
