from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import configuration
from config import ALLOWED_ORIGINS, API_HOST, API_PORT

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG Chatbot API",
    description="Retrieval-Augmented Generation API for textbook Q&A",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes (to be implemented)
# from api.routes import router
# app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Physical AI Textbook RAG API"}

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": "2025-12-06T00:00:00Z",
        "components": {
            "embeddings": "ok",
            "qdrant": "ok",
            "database": "ok"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
