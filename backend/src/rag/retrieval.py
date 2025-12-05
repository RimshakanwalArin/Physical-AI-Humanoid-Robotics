from qdrant_client import QdrantClient
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class RetrievalService:
    """Service for semantic search and retrieval from Qdrant"""
    
    def __init__(self, qdrant_url: str = "http://localhost:6333"):
        try:
            self.client = QdrantClient(url=qdrant_url)
            logger.info(f"Connected to Qdrant at {qdrant_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.client = None
    
    def search_chapters(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        """Search for relevant chapters given a query vector"""
        if self.client is None:
            logger.warning("Qdrant client not initialized")
            return []
        
        try:
            results = self.client.search(
                collection_name="textbook_chunks",
                query_vector=query_vector,
                limit=top_k
            )
            
            chunks = []
            for result in results:
                chunk = {
                    "id": result.id,
                    "score": result.score,
                    "chapter_id": result.payload.get("chapter_id"),
                    "section_id": result.payload.get("section_id"),
                    "chapter_title": result.payload.get("chapter_title"),
                    "section_title": result.payload.get("section_title"),
                    "text": result.payload.get("text"),
                }
                chunks.append(chunk)
            
            return chunks
        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            return []
