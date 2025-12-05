#!/usr/bin/env python3
"""
Embed chapter sections using Sentence Transformers.

This script:
1. Loads extracted chapters
2. Generates embeddings for each section
3. Saves embeddings for storage in Qdrant
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer


class SectionEmbedder:
    """Generate embeddings for chapter sections."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with embedding model."""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def embed_sections(
        self, chapters_file: str = "indexing/extracted_chapters.json"
    ) -> List[Dict[str, Any]]:
        """Load chapters and generate embeddings."""
        # Load extracted chapters
        with open(chapters_file, "r", encoding="utf-8") as f:
            chapters_data = json.load(f)

        embeddings_data = []
        total_sections = 0

        for chapter in chapters_data:
            print(f"Processing chapter: {chapter['title']}")

            for section in chapter["sections"]:
                total_sections += 1

                # Generate embedding
                embedding = self.model.encode(
                    section["content"],
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )

                embedding_entry = {
                    "section_id": section["id"],
                    "chapter_id": chapter["id"],
                    "chapter_title": chapter["title"],
                    "chapter_position": chapter["position"],
                    "section_title": section["title"],
                    "section_level": section["level"],
                    "content": section["content"],
                    "embedding": embedding.tolist(),
                    "embedding_model": self.model_name,
                    "embedding_dimension": len(embedding),
                }

                embeddings_data.append(embedding_entry)

                # Print progress
                if total_sections % 5 == 0:
                    print(f"  Processed {total_sections} sections...")

        print(f"Total embeddings generated: {total_sections}")
        return embeddings_data

    def save_embeddings(
        self,
        embeddings: List[Dict[str, Any]],
        output_file: str = "indexing/embeddings.json",
    ):
        """Save embeddings to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(embeddings, f, indent=2)

        print(f"Embeddings saved to {output_path}")


def main():
    """Generate and save embeddings."""
    embedder = SectionEmbedder()

    # Generate embeddings
    embeddings = embedder.embed_sections()

    # Save to file
    embedder.save_embeddings(embeddings)

    # Print statistics
    if embeddings:
        embedding_dim = embeddings[0]["embedding_dimension"]
        print(f"\nEmbedding Statistics:")
        print(f"  Total sections: {len(embeddings)}")
        print(f"  Embedding dimension: {embedding_dim}")
        print(f"  Model: {embeddings[0]['embedding_model']}")


if __name__ == "__main__":
    main()
