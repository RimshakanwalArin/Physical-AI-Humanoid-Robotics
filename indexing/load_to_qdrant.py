#!/usr/bin/env python3
"""
Load embeddings into Qdrant vector database.

This script:
1. Loads embeddings from JSON
2. Creates Qdrant collection
3. Stores embeddings with metadata
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Payload,
)


class QdrantIndexer:
    """Index embeddings in Qdrant vector database."""

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        api_key: str = None,
    ):
        """Initialize Qdrant client."""
        self.client = QdrantClient(
            url=qdrant_url,
            api_key=api_key,
        )
        self.collection_name = "robotics_textbook"

    def create_collection(self, vector_size: int = 384):
        """Create Qdrant collection for storing embeddings."""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists")
        except Exception:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
            print(
                f"Created collection '{self.collection_name}' with vector size {vector_size}"
            )

    def index_embeddings(
        self, embeddings: List[Dict[str, Any]]
    ) -> int:
        """Upload embeddings to Qdrant."""
        points = []

        for i, embedding_entry in enumerate(embeddings):
            # Create point
            point = PointStruct(
                id=i,
                vector=embedding_entry["embedding"],
                payload={
                    "section_id": embedding_entry["section_id"],
                    "chapter_id": embedding_entry["chapter_id"],
                    "chapter_title": embedding_entry["chapter_title"],
                    "chapter_position": embedding_entry["chapter_position"],
                    "section_title": embedding_entry["section_title"],
                    "section_level": embedding_entry["section_level"],
                    "content": embedding_entry["content"],
                    "embedding_model": embedding_entry["embedding_model"],
                },
            )
            points.append(point)

        # Upload in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i : i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch,
            )
            print(f"Uploaded {min(i + batch_size, len(points))}/{len(points)} points")

        return len(points)

    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar sections."""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "score": result.score,
                    "section_id": result.payload["section_id"],
                    "chapter_id": result.payload["chapter_id"],
                    "chapter_title": result.payload["chapter_title"],
                    "section_title": result.payload["section_title"],
                    "content": result.payload["content"],
                }
            )

        return formatted_results

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": info.config.collection_name if hasattr(info, 'config') else self.collection_name,
            "points_count": info.points_count,
            "vectors_count": info.vectors_count if hasattr(info, 'vectors_count') else None,
        }


def main():
    """Load embeddings into Qdrant."""
    # Load embeddings
    embeddings_file = Path("indexing/embeddings.json")

    if not embeddings_file.exists():
        print(f"Error: {embeddings_file} not found")
        print("Run 'python indexing/embed.py' first")
        return

    with open(embeddings_file, "r", encoding="utf-8") as f:
        embeddings = json.load(f)

    print(f"Loaded {len(embeddings)} embeddings")

    # Get vector size from first embedding
    vector_size = embeddings[0]["embedding_dimension"]

    # Initialize Qdrant indexer
    indexer = QdrantIndexer()

    # Create collection
    indexer.create_collection(vector_size=vector_size)

    # Index embeddings
    uploaded = indexer.index_embeddings(embeddings)
    print(f"Uploaded {uploaded} vectors to Qdrant")

    # Print collection info
    info = indexer.get_collection_info()
    print(f"\nCollection Info:")
    print(f"  Name: {info['name']}")
    print(f"  Points: {info['points_count']}")


if __name__ == "__main__":
    main()
