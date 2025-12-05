"""Gemini LLM integration for enhanced answer generation."""

import os
from typing import Optional, Tuple, List, Dict
import google.generativeai as genai
from backend.src.config import settings


class GeminiLLM:
    """Wrapper for Google Gemini LLM."""

    def __init__(self):
        """Initialize Gemini client."""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_answer(
        self,
        query: str,
        context: List[str],
        max_tokens: int = 500
    ) -> Tuple[str, List[Dict]]:
        """
        Generate an answer using Gemini LLM with RAG context.

        Args:
            query: User's question
            context: List of relevant text chunks from retrieval
            max_tokens: Maximum tokens in response

        Returns:
            Tuple of (answer, citations)
        """
        # Build prompt with context
        prompt = self._build_prompt(query, context)

        try:
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )

            answer = response.text

            # Extract citations from context
            citations = self._extract_citations(context)

            return answer, citations

        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")

    def _build_prompt(self, query: str, context: List[str]) -> str:
        """Build a prompt with RAG context."""
        context_str = "\n\n".join(
            [f"[Source {i+1}]\n{text}" for i, text in enumerate(context)]
        )

        prompt = f"""You are an expert AI tutor for a Physical AI and Humanoid Robotics textbook.

Use the following context from the textbook to answer the question. Always cite your sources.

CONTEXT:
{context_str}

QUESTION: {query}

INSTRUCTIONS:
1. Provide a clear, concise answer based on the context
2. If the context doesn't contain the answer, say "This topic is not covered in the current textbook"
3. Cite which sources you used (e.g., [Source 1])
4. Keep the answer educational and detailed
5. Use simple language suitable for students

ANSWER:"""

        return prompt

    def _extract_citations(self, context: List[str]) -> List[Dict]:
        """Extract citation information from context."""
        citations = []
        for i, text in enumerate(context):
            # This is a simplified extraction - in production, you'd have structured metadata
            citations.append({
                "source_id": i + 1,
                "excerpt": text[:200] + "..." if len(text) > 200 else text
            })
        return citations

    def answer_with_rag(
        self,
        query: str,
        retrieved_chunks: List[Dict]
    ) -> Tuple[str, List[Dict]]:
        """
        Generate answer using retrieved chunks as RAG context.

        Args:
            query: User's question
            retrieved_chunks: List of dicts with 'content' key from Qdrant

        Returns:
            Tuple of (answer, formatted_citations)
        """
        # Extract text content from retrieved chunks
        context = [chunk.get('content') or chunk.get('text')
                   for chunk in retrieved_chunks]

        # Generate answer with Gemini
        answer, _ = self.generate_answer(query, context)

        # Format citations with metadata
        citations = []
        for i, chunk in enumerate(retrieved_chunks):
            citation = {
                "source_id": i + 1,
                "chapter_title": chunk.get('chapter_title', 'Unknown'),
                "section_title": chunk.get('section_title', 'Unknown'),
                "excerpt": chunk.get('content')[:150] if chunk.get('content') else ""
            }
            citations.append(citation)

        return answer, citations


# Singleton instance
_gemini_instance = None


def get_gemini_client() -> GeminiLLM:
    """Get or create Gemini client."""
    global _gemini_instance

    if _gemini_instance is None:
        try:
            _gemini_instance = GeminiLLM()
        except ValueError:
            # If Gemini not configured, return None
            return None

    return _gemini_instance
