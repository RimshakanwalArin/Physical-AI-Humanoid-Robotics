"""Answer generation and formatting (T020, T022, T024, T038, T039, T042, T043)"""

import logging
from typing import List, Tuple
import time

from ..models import IndexedChunk, Citation, RagResponse
from .quality import get_quality_monitor, QualityMonitor
from ..config import get_settings

logger = logging.getLogger(__name__)


class AnswerGenerator:
    """Generates formatted RAG responses with citations"""

    def __init__(self, quality_monitor: QualityMonitor = None):
        self.settings = get_settings()
        self.quality_monitor = quality_monitor or get_quality_monitor()

    def generate_response(
        self,
        query_id: str,
        query_text: str,
        retrieved_chunks: List[IndexedChunk],
        similarity_scores: List[float],
        embedding_model: str = "bge-small-en-v1.5"
    ) -> Tuple[RagResponse, bool]:
        """Generate formatted answer with citations (T024, T038, T042)"""

        start_time = time.time()
        logger.info(f"Generating response for query {query_id}")

        # Check if we have relevant chunks (T021)
        if not retrieved_chunks or not similarity_scores:
            logger.warning(f"No relevant chunks for query {query_id}")
            response_text = self.quality_monitor.generate_not_in_textbook_response()
            confidence_score = 0.0
            is_valid = False
        else:
            # Validate source-only constraint (T020)
            source_texts = [chunk.content_text for chunk in retrieved_chunks]
            is_valid, validation_msg = self.quality_monitor.validate_source_only_response(
                "",  # Will validate after formatting
                source_texts,
                similarity_scores
            )

            if not is_valid:
                logger.warning(f"Source validation failed: {validation_msg}")
                response_text = self.quality_monitor.generate_not_in_textbook_response()
                confidence_score = 0.0
            else:
                # Format answer from source chunks (T024)
                response_text = self._format_answer_from_chunks(retrieved_chunks)

                # Calculate confidence (T025)
                confidence_score = self._calculate_confidence(similarity_scores)

                # Add citations (T038, T039)
                citations = self._extract_and_deduplicate_citations(retrieved_chunks)
                response_text = self._append_citations(response_text, citations)

        # Detect hallucinations (T023)
        source_texts = [chunk.content_text for chunk in retrieved_chunks] if retrieved_chunks else []
        is_hallucinated, _ = self.quality_monitor.detect_hallucination(
            response_text,
            source_texts,
            confidence_score
        )

        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000

        # Create response object (T041, T042)
        response = RagResponse(
            query_id=query_id,
            query_text=query_text,
            response_text=response_text,
            sources=[],  # Will populate from citations
            source_chunk_ids=[chunk.id for chunk in retrieved_chunks],
            confidence_score=confidence_score,
            hallucination_detected=is_hallucinated,
            latency_ms=latency_ms,
            embedding_model=embedding_model
        )

        # Add citations to response
        if retrieved_chunks:
            response.sources = self._extract_and_deduplicate_citations(retrieved_chunks)

        # Log metrics (T028)
        self.quality_monitor.log_query_metrics(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=len(retrieved_chunks),
            confidence_score=confidence_score,
            is_hallucinated=is_hallucinated,
            latency_ms=latency_ms,
            embedding_model=embedding_model
        )

        return response, is_hallucinated

    def _format_answer_from_chunks(self, chunks: List[IndexedChunk]) -> str:
        """Format chunks into readable answer (T024)"""
        if not chunks:
            return ""

        # Join chunks with section headers
        formatted_parts = []
        for i, chunk in enumerate(chunks, 1):
            section_header = f"**Section {i}: {chunk.section_name}**"
            formatted_parts.append(f"{section_header}\n{chunk.content_text}")

        return "\n\n".join(formatted_parts)

    def _calculate_confidence(self, similarity_scores: List[float]) -> float:
        """Calculate confidence score from similarity (T025)"""
        if not similarity_scores:
            return 0.0

        import numpy as np
        avg_score = float(np.mean(similarity_scores))
        return min(max(avg_score, 0.0), 1.0)

    def _extract_and_deduplicate_citations(
        self,
        chunks: List[IndexedChunk]
    ) -> List[Citation]:
        """Extract citations and remove duplicates (T036, T039)"""
        seen_sections = set()
        citations = []

        for chunk in chunks:
            section_key = (chunk.chapter_id, chunk.section_number)
            if section_key in seen_sections:
                continue

            seen_sections.add(section_key)

            citation = Citation(
                chunk_id=chunk.id,
                chapter_name=f"Chapter {chunk.chapter_id}",
                section_name=chunk.section_name,
                section_number=chunk.section_number,
                page_number=chunk.page_number,
                link_anchor=f"ch{chunk.chapter_id.replace('_', '-')}-{chunk.section_number.replace('.', '-')}"
            )
            citations.append(citation)

        return citations

    def _append_citations(
        self,
        response_text: str,
        citations: List[Citation]
    ) -> str:
        """Append formatted citations to response (T038, T042)"""
        if not citations:
            return response_text

        # Format citations section
        citations_section = "\n\n**Sources:**\n"
        for citation in citations:
            source_ref = (
                f"- [{citation.chapter_name}: {citation.section_name}]"
                f"(#{citation.link_anchor})"
            )
            if citation.page_number:
                source_ref = source_ref[:-1] + f", Page {citation.page_number})"
            citations_section += source_ref + "\n"

        return response_text + citations_section

    def validate_response_quality(self, response: RagResponse) -> Tuple[bool, str]:
        """Validate response meets quality criteria (T043)"""
        issues = []

        # Check 1: Response should not be empty (unless intentionally out-of-scope)
        if not response.response_text or len(response.response_text.strip()) == 0:
            issues.append("Response is empty")

        # Check 2: If sources exist, must have citations
        if response.source_chunk_ids and not response.sources:
            issues.append("Retrieved sources but no citations provided")

        # Check 3: Confidence should be consistent with sources
        if response.confidence_score < 0.5 and response.sources:
            issues.append("Low confidence despite having sources")

        # Check 4: No hallucinations allowed
        if response.hallucination_detected:
            issues.append("Hallucination detected in response")

        is_valid = len(issues) == 0
        message = "; ".join(issues) if issues else "Response is valid"

        logger.info(f"Response validation: {message}")
        return is_valid, message
