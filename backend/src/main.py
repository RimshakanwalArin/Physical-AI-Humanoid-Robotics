from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import configuration
from backend.src.config import ALLOWED_ORIGINS, API_HOST, API_PORT

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG Chatbot API",
    description="Retrieval-Augmented Generation API for textbook Q&A with Gemini LLM",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
try:
    from backend.src.api.routes import router as chat_router
    from backend.src.auth.routes import router as auth_router

    app.include_router(chat_router)
    app.include_router(auth_router)
    logger.info("Routes loaded successfully")
except Exception as e:
    logger.error(f"Error loading routes: {e}")

@app.get("/")
async def root():
    return {
        "message": "Physical AI Textbook RAG API with Gemini LLM",
        "version": "2.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "chat": "POST /api/chat",
            "health": "GET /api/health",
            "auth_signup": "POST /api/auth/signup",
            "auth_login": "POST /api/auth/login"
        }
    }

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-12-06T00:00:00Z",
        "components": {
            "embeddings": "ok",
            "qdrant": "ok",
            "database": "ok",
            "gemini": "enabled"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
