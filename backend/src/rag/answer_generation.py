from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class AnswerGenerationService:
    """Service for generating answers from retrieved chunks (LLM-free synthesis)"""
    
    @staticmethod
    def synthesize_answer(
        query: str, 
        retrieved_chunks: List[Dict]
    ) -> Tuple[str, List[Dict]]:
        """Synthesize answer from retrieved chunks without LLM"""
        
        if not retrieved_chunks:
            return (
                "This topic is not covered in the Physical AI & Humanoid Robotics textbook. Please try a question related to the course content.",
                []
            )
        
        # Combine facts from chunks
        answer_parts = []
        citations = []
        
        for chunk in retrieved_chunks:
            text = chunk.get("text", "")
            if text:
                answer_parts.append(text)
            
            # Create citation
            citation = {
                "chapter_id": chunk.get("chapter_id"),
                "chapter_title": chunk.get("chapter_title"),
                "section_id": chunk.get("section_id"),
                "section_title": chunk.get("section_title"),
                "excerpt": text[:200] if text else ""
            }
            citations.append(citation)
        
        # Combine answer parts
        answer = " ".join(answer_parts)
        
        if not answer or len(answer) < 50:
            return (
                "This topic is not covered in the Physical AI & Humanoid Robotics textbook. Please try a question related to the course content.",
                []
            )
        
        return answer, citations
