"""Tests for the embeddings service."""

import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from backend.src.rag.embeddings import EmbeddingService


class TestEmbeddingService(unittest.TestCase):
    """Test cases for EmbeddingService."""

    def setUp(self):
        """Set up test fixtures."""
        # Use small test model for speed
        self.service = EmbeddingService(model_name="all-MiniLM-L6-v2")

    def test_singleton_pattern(self):
        """Test that EmbeddingService follows singleton pattern."""
        service1 = EmbeddingService()
        service2 = EmbeddingService()

        # Should return same instance
        self.assertIs(service1, service2)

    def test_embed_text_returns_vector(self):
        """Test that embed_text returns a vector."""
        text = "This is a test sentence."
        embedding = self.service.embed_text(text)

        # Check type and shape
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 384)  # all-MiniLM-L6-v2 dimension

    def test_embed_text_numeric_values(self):
        """Test that embeddings contain numeric values."""
        text = "Test text for embedding."
        embedding = self.service.embed_text(text)

        # Check all values are numeric
        for val in embedding:
            self.assertIsInstance(val, (int, float))

    def test_embed_batch_returns_matrix(self):
        """Test that embed_batch returns a list of vectors."""
        texts = [
            "First test sentence.",
            "Second test sentence.",
            "Third test sentence.",
        ]
        embeddings = self.service.embed_batch(texts)

        # Check shape
        self.assertEqual(len(embeddings), 3)
        for embedding in embeddings:
            self.assertEqual(len(embedding), 384)

    def test_similar_texts_have_similar_embeddings(self):
        """Test that similar texts produce similar embeddings."""
        text1 = "The robot performs a grasp motion."
        text2 = "The robot executes a grasping action."
        text3 = "The weather is sunny today."

        emb1 = np.array(self.service.embed_text(text1))
        emb2 = np.array(self.service.embed_text(text2))
        emb3 = np.array(self.service.embed_text(text3))

        # Compute cosine similarities
        sim_1_2 = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        sim_1_3 = np.dot(emb1, emb3) / (np.linalg.norm(emb1) * np.linalg.norm(emb3))

        # Similar texts should have higher similarity
        self.assertGreater(sim_1_2, sim_1_3)

    def test_embed_empty_text(self):
        """Test embedding of empty text."""
        embedding = self.service.embed_text("")

        # Should return zero vector
        self.assertEqual(len(embedding), 384)

    def test_embed_long_text(self):
        """Test embedding of long text."""
        long_text = "This is a test. " * 100
        embedding = self.service.embed_text(long_text)

        # Should still return embedding
        self.assertEqual(len(embedding), 384)


if __name__ == "__main__":
    unittest.main()
