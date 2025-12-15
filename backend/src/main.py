"""FastAPI main application for RAG chatbot (T029)"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
import uuid
from typing import Optional

from .config import get_settings
from .models import RagQuery, RagResponse
from .rag.embeddings import get_embedding_encoder
from .rag.retrieval import RetrieverService
from .rag.answer_generation import AnswerGenerator
from .rag.quality import get_quality_monitor
from .qdrant_client import get_qdrant_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI Robotics Textbook",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get settings and services
settings = get_settings()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting RAG Chatbot API...")

    try:
        # Initialize embedding model
        embedding_encoder = get_embedding_encoder()
        model_info = embedding_encoder.get_model_info()
        logger.info(f"Embedding model loaded: {model_info}")

        # Initialize Qdrant connection
        qdrant_service = get_qdrant_service()
        logger.info(f"Qdrant connection ready: {settings.qdrant_url}")

        logger.info("RAG Chatbot API startup complete")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "service": "RAG Chatbot API",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "rag-chatbot",
        "timestamp": time.time()
    }


@app.get("/api/rag/status", tags=["System"])
async def rag_status():
    """Get RAG system status and model information (T029)"""
    try:
        settings = get_settings()
        embedding_encoder = get_embedding_encoder()

        return {
            "status": "healthy",
            "embedding_model": settings.embedding_model,
            "embedding_dimension": settings.embedding_dimension,
            "qdrant_url": settings.qdrant_url,
            "qdrant_collection": settings.qdrant_collection_name,
            "model_info": embedding_encoder.get_model_info(),
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/query", response_model=RagResponse, tags=["RAG"])
async def query_chatbot(
    query_text: str = Query(..., min_length=10, max_length=1000),
    student_id: Optional[str] = None
) -> RagResponse:
    """
    Submit a question to the RAG chatbot

    - **query_text**: Student question (10-1000 characters)
    - **student_id**: Optional student identifier

    Returns RagResponse with answer and citations
    """
    start_time = time.time()
    query_id = str(uuid.uuid4())

    logger.info(f"Query {query_id}: {query_text[:50]}...")

    try:
        # Initialize services
        embedding_encoder = get_embedding_encoder()
        qdrant_service = get_qdrant_service()
        quality_monitor = get_quality_monitor()
        answer_generator = AnswerGenerator(quality_monitor)

        # Step 1: Encode query (T009)
        logger.debug("Encoding query...")
        query_embedding = embedding_encoder.encode_query(query_text)

        # Step 2: Retrieve relevant chunks from Qdrant
        logger.debug("Retrieving relevant chunks...")
        retriever = RetrieverService(qdrant_service.get_search_client())

        retrieval_results = retriever.retrieve_relevant_chunks(
            query_embedding=query_embedding,
            top_k=settings.top_k_retrieval,
            min_threshold=settings.min_relevance_threshold
        )

        # Extract chunks and scores
        retrieved_chunks = [result.chunk for result in retrieval_results]
        similarity_scores = [result.similarity_score for result in retrieval_results]

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")

        # Step 3: Generate response with citations (T024, T038, T042)
        logger.debug("Generating response...")
        response, is_hallucinated = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=retrieved_chunks,
            similarity_scores=similarity_scores,
            embedding_model=settings.embedding_model
        )

        # Validate response quality (T043)
        is_valid, validation_msg = answer_generator.validate_response_quality(response)
        if not is_valid:
            logger.warning(f"Response validation warning: {validation_msg}")

        latency_ms = (time.time() - start_time) * 1000
        response.latency_ms = latency_ms

        logger.info(
            f"Query {query_id} complete: "
            f"confidence={response.confidence_score:.2f}, "
            f"latency={latency_ms:.0f}ms, "
            f"hallucination={is_hallucinated}"
        )

        return response

    except Exception as e:
        logger.error(f"Query {query_id} failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/metrics", tags=["Monitoring"])
async def log_query_metrics(
    response_id: str,
    actual_source_correct: Optional[bool] = None,
    relevance_feedback: Optional[float] = None,
    hallucination_detected: Optional[bool] = None
):
    """
    Log quality metrics for a response

    Allows students to provide feedback on answer quality
    """
    try:
        quality_monitor = get_quality_monitor()

        logger.info(
            f"Metrics logged for {response_id}: "
            f"correct={actual_source_correct}, "
            f"hallucination={hallucination_detected}"
        )

        return {
            "recorded": True,
            "metric_id": str(uuid.uuid4()),
            "timestamp": time.time()
        }

    except Exception as e:
        logger.error(f"Metrics logging error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc}")
    return {
        "error": "Validation failed",
        "detail": str(exc)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
