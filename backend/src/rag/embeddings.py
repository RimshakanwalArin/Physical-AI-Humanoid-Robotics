from sentence_transformers import SentenceTransformer
from typing import List
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for embedding text using Sentence Transformers"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            logger.info("Loading Sentence Transformers model: all-MiniLM-L6-v2")
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Model loaded successfully")
    
    def embed_text(self, text: str) -> List[float]:
        """Embed text and return vector representation"""
        try:
            embedding = self._model.encode(text, convert_to_tensor=True)
            return embedding.cpu().numpy().tolist()
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            raise
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts in batch"""
        try:
            embeddings = self._model.encode(texts, convert_to_tensor=True)
            return embeddings.cpu().numpy().tolist()
        except Exception as e:
            logger.error(f"Error embedding batch: {e}")
            raise
