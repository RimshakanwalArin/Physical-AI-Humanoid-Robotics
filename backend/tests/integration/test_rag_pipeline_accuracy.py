"""Integration tests for RAG pipeline accuracy (T018)"""

import pytest
import json
from pathlib import Path
import uuid

# Load test data
test_data_path = Path(__file__).parent.parent / "fixtures" / "rag_test_data.json"
with open(test_data_path) as f:
    TEST_DATA = json.load(f)


class TestRAGPipelineAccuracy:
    """Integration tests for end-to-end RAG pipeline"""

    @pytest.fixture
    def sample_chunks(self):
        """Load sample chunks"""
        from models import IndexedChunk

        chunks = []
        for chunk_data in TEST_DATA["sample_chunks"]:
            chunk = IndexedChunk(
                id=chunk_data["id"],
                chapter_id=chunk_data["chapter_id"],
                section_name=chunk_data["section_name"],
                section_number=chunk_data["section_number"],
                content_text=chunk_data["content"],
                page_number=chunk_data["page_number"]
            )
            chunks.append(chunk)
        return chunks

    @pytest.fixture
    def answer_generator(self):
        """Initialize answer generator"""
        from rag.answer_generation import AnswerGenerator
        return AnswerGenerator()

    def test_rag_pipeline_with_relevant_chunks(self, answer_generator, sample_chunks):
        """Test RAG pipeline returns structured response (acceptance scenario 1)"""
        # Given: Query about embodied intelligence
        query_id = str(uuid.uuid4())
        query_text = "What is embodied intelligence?"

        # Find relevant chunk
        relevant_chunks = [c for c in sample_chunks if "embodied" in c.content_text.lower()]
        assert len(relevant_chunks) > 0, "Should have test data for this query"

        # Simulate retrieval with confidence scores
        similarity_scores = [0.87, 0.82]  # Good scores > 0.85 avg

        # When: Generating response
        response, is_hallucinated = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=relevant_chunks[:2],
            similarity_scores=similarity_scores,
            embedding_model="bge-small-en-v1.5"
        )

        # Then: Should return valid response with citations
        assert response.query_id == query_id
        assert response.query_text == query_text
        assert len(response.response_text) > 0
        assert response.confidence_score > 0.8, "Should have high confidence"
        assert not is_hallucinated, "Should not detect hallucination for in-scope query"
        # Citations should be present if chunks were retrieved
        if relevant_chunks:
            assert len(response.sources) > 0, "Should include citations"

    def test_rag_pipeline_with_no_relevant_chunks(self, answer_generator):
        """Test RAG pipeline rejects out-of-scope queries (acceptance scenario 2)"""
        # Given: Out-of-scope query with no relevant chunks
        query_id = str(uuid.uuid4())
        query_text = "What is machine learning?"

        # No chunks retrieved
        relevant_chunks = []
        similarity_scores = []

        # When: Generating response
        response, is_hallucinated = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=relevant_chunks,
            similarity_scores=similarity_scores,
            embedding_model="bge-small-en-v1.5"
        )

        # Then: Should return "not in textbook" response
        assert "not covered in the textbook" in response.response_text.lower()
        assert response.confidence_score == 0.0
        assert len(response.sources) == 0, "No citations for out-of-scope"

    def test_citation_accuracy(self, answer_generator, sample_chunks):
        """Test that citations correctly reference source chapters"""
        # Given: Retrieve relevant chunks
        query_id = str(uuid.uuid4())
        query_text = "Tell me about bipedal locomotion"

        relevant_chunks = [c for c in sample_chunks if "bipedal" in c.content_text.lower()]
        similarity_scores = [0.86]

        # When: Generating response
        response, _ = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=relevant_chunks,
            similarity_scores=similarity_scores
        )

        # Then: Citations should match source chunks
        if relevant_chunks and response.sources:
            assert len(response.sources) == len(relevant_chunks), \
                "Should have citation for each unique source"

            for citation in response.sources:
                # Citation should reference actual chunk
                assert citation.chapter_name is not None
                assert citation.section_name is not None
                assert citation.section_number is not None

    def test_response_format_validation(self, answer_generator, sample_chunks):
        """Test that response follows required format"""
        query_id = str(uuid.uuid4())
        query_text = "Explain ROS 2"

        relevant_chunks = [c for c in sample_chunks if "ros" in c.content_text.lower()]
        similarity_scores = [0.85] if relevant_chunks else []

        response, _ = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=relevant_chunks,
            similarity_scores=similarity_scores
        )

        # Response must have required fields
        assert response.id is not None
        assert response.query_id == query_id
        assert response.query_text == query_text
        assert response.response_text is not None
        assert 0.0 <= response.confidence_score <= 1.0
        assert isinstance(response.hallucination_detected, bool)
        assert response.latency_ms > 0
        assert response.embedding_model == "bge-small-en-v1.5"

    def test_response_latency_tracking(self, answer_generator, sample_chunks):
        """Test that response includes latency measurement"""
        query_id = str(uuid.uuid4())
        query_text = "Query for latency test"

        relevant_chunks = sample_chunks[:1]
        similarity_scores = [0.85]

        response, _ = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=relevant_chunks,
            similarity_scores=similarity_scores
        )

        # Latency should be reasonable (<5 seconds for unit test)
        assert 0 < response.latency_ms < 5000, "Response latency out of expected range"

    def test_confidence_score_calculation(self, answer_generator, sample_chunks):
        """Test confidence score reflects similarity scores"""
        query_id = str(uuid.uuid4())
        query_text = "Test confidence"

        # Test with high similarity scores
        relevant_chunks = sample_chunks[:2]
        high_scores = [0.95, 0.92]

        response_high, _ = answer_generator.generate_response(
            query_id=query_id,
            query_text=query_text,
            retrieved_chunks=relevant_chunks,
            similarity_scores=high_scores
        )

        # Test with low similarity scores
        low_scores = [0.55, 0.50]

        response_low, _ = answer_generator.generate_response(
            query_id=str(uuid.uuid4()),
            query_text=query_text,
            retrieved_chunks=relevant_chunks,
            similarity_scores=low_scores
        )

        # High confidence should be higher than low confidence
        assert response_high.confidence_score > response_low.confidence_score, \
            "Confidence should reflect similarity scores"
