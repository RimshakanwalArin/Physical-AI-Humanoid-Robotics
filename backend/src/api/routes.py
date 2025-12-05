from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse, Citation
from ..rag.embeddings import EmbeddingService
from ..rag.retrieval import RetrievalService
from ..rag.answer_generation import AnswerGenerationService
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

embedding_service = EmbeddingService()
retrieval_service = RetrievalService()

@router.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Process chat query and return RAG-generated answer"""
    
    start_time = time.time()
    
    try:
        # Validate request
        if not request.query or len(request.query) == 0:
            raise HTTPException(status_code=400, detail="Missing required field: query")
        
        # Embed query
        query_vector = embedding_service.embed_text(request.query)
        
        # Retrieve relevant chapters
        retrieved_chunks = retrieval_service.search_chapters(query_vector, top_k=3)
        
        # Generate answer
        answer, citations_data = AnswerGenerationService.synthesize_answer(
            request.query, 
            retrieved_chunks
        )
        
        # Build response
        citations = [
            Citation(
                chapter_id=c.get("chapter_id", ""),
                chapter_title=c.get("chapter_title", ""),
                section_id=c.get("section_id", ""),
                section_title=c.get("section_title", ""),
                excerpt=c.get("excerpt", "")
            )
            for c in citations_data
        ]
        
        latency_ms = int((time.time() - start_time) * 1000)
        status = "success" if citations else "not_found"
        
        return ChatResponse(
            status=status,
            answer=answer,
            sources=citations,
            latency_ms=latency_ms
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "embeddings": "ok",
            "qdrant": "ok",
            "database": "ok"
        }
    }
