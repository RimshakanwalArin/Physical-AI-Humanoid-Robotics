"""Qdrant vector database client and utilities (T004, T012)"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional
import logging

from .config import get_settings
from .models import IndexedChunk

logger = logging.getLogger(__name__)


class QdrantServiceClient:
    """Wrapper around Qdrant client for collection management"""

    def __init__(self):
        self.settings = get_settings()
        self.client = QdrantClient(
            url=self.settings.qdrant_url,
            api_key=self.settings.qdrant_api_key if self.settings.qdrant_api_key else None
        )

    def collection_exists(self, collection_name: str) -> bool:
        """Check if collection exists"""
        try:
            self.client.get_collection(collection_name)
            return True
        except:
            return False

    def create_collection(
        self,
        collection_name: str,
        vector_size: int = 384,
        distance_metric: str = "Cosine"
    ):
        """Create new Qdrant collection (T012)"""
        logger.info(f"Creating collection: {collection_name}")

        if self.collection_exists(collection_name):
            logger.warning(f"Collection {collection_name} already exists")
            return

        # Create collection with specified vector size
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Collection {collection_name} created successfully")

    def create_collection_alias(
        self,
        collection_name: str,
        alias_name: str
    ):
        """Create alias for collection (T012)"""
        logger.info(f"Creating alias {alias_name} -> {collection_name}")

        try:
            self.client.create_alias(
                collection_name=collection_name,
                alias_name=alias_name
            )
            logger.info(f"Alias {alias_name} created successfully")
        except Exception as e:
            logger.error(f"Failed to create alias: {e}")
            raise

    def switch_alias(
        self,
        old_collection: str,
        new_collection: str,
        alias_name: str
    ):
        """Atomically switch alias from old to new collection (T012)"""
        logger.info(f"Switching alias {alias_name}: {old_collection} -> {new_collection}")

        try:
            self.client.update_collection_aliases(
                change_aliases_operations=[
                    models.AliasOperations(
                        delete_alias=models.DeleteAlias(
                            alias_name=alias_name
                        )
                    ),
                    models.AliasOperations(
                        create_alias=models.CreateAlias(
                            collection_name=new_collection,
                            alias_name=alias_name
                        )
                    )
                ]
            )
            logger.info(f"Alias {alias_name} switched successfully")
        except Exception as e:
            logger.error(f"Failed to switch alias: {e}")
            raise

    def upsert_points(
        self,
        collection_name: str,
        points: List[models.PointStruct]
    ):
        """Upsert points into collection"""
        logger.info(f"Upserting {len(points)} points into {collection_name}")

        try:
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.info(f"Successfully upserted {len(points)} points")
        except Exception as e:
            logger.error(f"Failed to upsert points: {e}")
            raise

    def search_similar(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.0
    ) -> List[models.ScoredPoint]:
        """Search for similar vectors in collection"""
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True,
                with_vectors=False
            )
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def get_collection_stats(self, collection_name: str) -> dict:
        """Get collection statistics"""
        try:
            collection_info = self.client.get_collection(collection_name)
            return {
                "points_count": collection_info.points_count,
                "vectors_count": collection_info.vectors_count,
                "status": str(collection_info.status),
                "config": collection_info.config
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            raise

    def get_search_client(self):
        """Get raw Qdrant client for advanced operations"""
        return self.client


# Singleton instance
_qdrant_service: Optional[QdrantServiceClient] = None


def get_qdrant_service() -> QdrantServiceClient:
    """Get Qdrant service singleton"""
    global _qdrant_service
    if _qdrant_service is None:
        _qdrant_service = QdrantServiceClient()
    return _qdrant_service
