"""Vector retrieval and ranking module (T011, T021, T024, T025)"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
import logging

from ..config import get_settings
from ..models import IndexedChunk, Citation

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """Result from retrieval operation"""

    chunk: IndexedChunk
    similarity_score: float
    rank: int


class RetrieverService:
    """Handles vector similarity search and retrieval from Qdrant"""

    def __init__(self, qdrant_client):
        self.qdrant_client = qdrant_client
        self.settings = get_settings()

    def retrieve_relevant_chunks(
        self,
        query_embedding: np.ndarray,
        top_k: Optional[int] = None,
        min_threshold: Optional[float] = None
    ) -> List[RetrievalResult]:
        """Retrieve top-K similar chunks from Qdrant (T011, T021)"""

        top_k = top_k or self.settings.top_k_retrieval
        min_threshold = min_threshold or self.settings.min_relevance_threshold

        logger.info(f"Retrieving top-{top_k} chunks with threshold {min_threshold}")

        try:
            # Search in Qdrant collection
            search_results = self.qdrant_client.search(
                collection_name=self.settings.qdrant_collection_name,
                query_vector=query_embedding.tolist(),
                limit=top_k * 2,  # Fetch extra to filter by threshold
                score_threshold=0.0,  # We'll apply threshold manually
                with_payload=True
            )

            results = []
            for rank, search_result in enumerate(search_results):
                similarity_score = search_result.score

                # Filter by minimum relevance threshold (T021)
                if similarity_score < min_threshold:
                    logger.debug(
                        f"Skipping chunk {search_result.id}: "
                        f"score {similarity_score:.2f} below threshold {min_threshold}"
                    )
                    continue

                # Reconstruct IndexedChunk from Qdrant payload
                chunk_data = search_result.payload
                chunk = IndexedChunk(
                    id=str(search_result.id),
                    chapter_id=chunk_data.get("chapter_id"),
                    section_name=chunk_data.get("section_name"),
                    section_number=chunk_data.get("section_number"),
                    content_text=chunk_data.get("content_text"),
                    embedding_model=chunk_data.get("embedding_model", "bge-small-en-v1.5"),
                    page_number=chunk_data.get("page_number")
                )

                results.append(RetrievalResult(
                    chunk=chunk,
                    similarity_score=similarity_score,
                    rank=rank
                ))

            logger.info(
                f"Retrieved {len(results)} chunks above threshold "
                f"(searched top {min(len(search_results), top_k*2)})"
            )
            return results[:top_k]

        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            raise

    def calculate_confidence_score(
        self,
        similarity_scores: List[float]
    ) -> float:
        """Calculate confidence from retrieval scores (T024, T025)"""

        if not similarity_scores:
            return 0.0

        # Average similarity with floor at 0
        avg_similarity = np.mean(similarity_scores)

        # Confidence is average similarity normalized to [0, 1]
        confidence = float(np.clip(avg_similarity, 0.0, 1.0))

        return confidence

    def normalize_scores(
        self,
        scores: List[float]
    ) -> List[float]:
        """Normalize relevance scores to [0, 1] range (T011)"""

        if not scores:
            return []

        scores = np.array(scores)
        min_score = scores.min()
        max_score = scores.max()

        # Avoid division by zero
        if max_score == min_score:
            return [0.5] * len(scores)

        normalized = (scores - min_score) / (max_score - min_score)
        return normalized.tolist()

    def extract_citations(
        self,
        chunks: List[IndexedChunk]
    ) -> List[Citation]:
        """Extract citation metadata from chunks (T036)"""

        citations = []
        seen_sections = set()

        for chunk in chunks:
            # Avoid duplicate citations
            section_key = (chunk.chapter_id, chunk.section_number)
            if section_key in seen_sections:
                continue

            seen_sections.add(section_key)

            citation = Citation(
                chunk_id=chunk.id,
                chapter_name=f"Chapter {chunk.chapter_id}: {chunk.section_name}",
                section_name=chunk.section_name,
                section_number=chunk.section_number,
                page_number=chunk.page_number,
                link_anchor=f"ch{chunk.chapter_id}-{chunk.section_number.replace('.', '-')}"
            )
            citations.append(citation)

        return citations
