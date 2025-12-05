"""Tests for the FastAPI routes."""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.src.main import app


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)

    def test_health_endpoint(self):
        """Test GET /api/health endpoint."""
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check required fields
        self.assertIn("status", data)
        self.assertIn("components", data)
        self.assertEqual(data["status"], "ok")

    def test_health_includes_component_status(self):
        """Test that health endpoint returns component status."""
        response = self.client.get("/api/health")
        data = response.json()

        components = data.get("components", {})
        # Should report on embeddings, retrieval, answer_generation
        self.assertIsInstance(components, dict)

    @patch("backend.src.api.routes.AnswerGenerationService.synthesize_answer")
    @patch("backend.src.api.routes.RetrievalService.search_chapters")
    @patch("backend.src.api.routes.EmbeddingService.embed_text")
    def test_chat_endpoint_success(
        self,
        mock_embed,
        mock_retrieve,
        mock_synthesize,
    ):
        """Test successful POST /api/chat request."""
        # Setup mocks
        mock_embed.return_value = [0.1] * 384
        mock_retrieve.return_value = [
            {
                "chapter_id": "ch1",
                "chapter_title": "Introduction",
                "section_id": "sec1",
                "section_title": "Basics",
                "text": "This is sample text.",
            }
        ]
        mock_synthesize.return_value = (
            "Answer from the textbook.",
            [
                {
                    "chapter_id": "ch1",
                    "chapter_title": "Introduction",
                    "section_id": "sec1",
                    "section_title": "Basics",
                    "excerpt": "This is sample text.",
                }
            ],
        )

        # Make request
        response = self.client.post(
            "/api/chat",
            json={
                "query": "What is robotics?",
                "session_id": "test-session-123",
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check response structure
        self.assertIn("status", data)
        self.assertIn("answer", data)
        self.assertIn("sources", data)
        self.assertEqual(data["status"], "success")

    def test_chat_missing_query(self):
        """Test POST /api/chat with missing query."""
        response = self.client.post(
            "/api/chat",
            json={"session_id": "test-session"},
        )

        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_chat_empty_query(self):
        """Test POST /api/chat with empty query."""
        response = self.client.post(
            "/api/chat",
            json={
                "query": "",
                "session_id": "test-session",
            },
        )

        # Should reject empty query
        self.assertNotEqual(response.status_code, 200)

    @patch("backend.src.api.routes.RetrievalService.search_chapters")
    @patch("backend.src.api.routes.EmbeddingService.embed_text")
    def test_chat_no_results(self, mock_embed, mock_retrieve):
        """Test chat when no results are found."""
        # Setup mocks
        mock_embed.return_value = [0.1] * 384
        mock_retrieve.return_value = []  # No results

        # Make request
        response = self.client.post(
            "/api/chat",
            json={
                "query": "Very obscure question about quantum robotics",
                "session_id": "test-session",
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Should return response even with no sources
        self.assertIn("answer", data)
        self.assertEqual(len(data.get("sources", [])), 0)


if __name__ == "__main__":
    unittest.main()
