from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from models import ChatRequest, ChatResponse, Citation
from ..rag.embeddings import EmbeddingService
from ..rag.retrieval import RetrievalService
from ..rag.answer_generation import AnswerGenerationService
from ..rag.gemini_llm import get_gemini_client
from ..auth.security import decode_token
from ..config import USE_GEMINI
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

embedding_service = EmbeddingService()
retrieval_service = RetrievalService()
gemini_client = get_gemini_client() if USE_GEMINI else None


def extract_user_from_token(authorization: Optional[str] = None) -> Optional[dict]:
    """Extract user info from bearer token."""
    if not authorization:
        return None

    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        token_data = decode_token(parts[1])
        if not token_data:
            return None

        return {"email": token_data.email}
    except Exception:
        return None


@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)
) -> ChatResponse:
    """Process chat query and return RAG-generated answer with Gemini LLM"""

    start_time = time.time()

    try:
        # Validate request
        if not request.query or len(request.query) == 0:
            raise HTTPException(status_code=400, detail="Missing required field: query")

        # Extract user from token (optional)
        user = extract_user_from_token(authorization)

        # Embed query
        query_vector = embedding_service.embed_text(request.query)

        # Retrieve relevant chapters
        retrieved_chunks = retrieval_service.search_chapters(query_vector, top_k=3)

        # Generate answer using Gemini if available, otherwise use LLM-free synthesis
        if gemini_client and retrieved_chunks:
            try:
                answer, citations_data = gemini_client.answer_with_rag(
                    request.query,
                    retrieved_chunks
                )
            except Exception as e:
                logger.warning(f"Gemini API error, falling back to synthesis: {e}")
                answer, citations_data = AnswerGenerationService.synthesize_answer(
                    request.query,
                    retrieved_chunks
                )
        else:
            # Fallback to LLM-free synthesis
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
    gemini_status = "ok" if gemini_client else "disabled"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "embeddings": "ok",
            "qdrant": "ok",
            "database": "ok",
            "gemini": gemini_status
        }
    }
