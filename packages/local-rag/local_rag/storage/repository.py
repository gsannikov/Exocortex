"""
Vector store repository abstraction.

This wraps concrete vector store implementations to provide idempotent upserts
and a minimal lifecycle API (count/close). Keeps the rest of the codebase
agnostic to Chroma vs Qdrant.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from ..adapters.vectorstore import BaseVectorStore, VectorStoreType, get_vector_store
from ..settings import LocalRagSettings


class VectorStoreRepository:
    """Thin repository wrapper around a vector store."""

    def __init__(self, store: BaseVectorStore):
        self.store = store

    def upsert_documents(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None,
    ):
        """Idempotent add/update where supported, fallback to delete+add."""
        if hasattr(self.store, "upsert_documents"):
            return getattr(self.store, "upsert_documents")(
                ids=ids,
                texts=texts,
                embeddings=embeddings,
                metadatas=metadatas,
            )

        # Fallback path
        self.store.delete_documents(ids=ids)
        return self.store.add_documents(
            ids=ids,
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def delete_documents(self, ids: List[str] = None, where: Dict = None):
        """Delete documents by id or filter."""
        return self.store.delete_documents(ids=ids, where=where)

    def count(self) -> int:
        """Return total document count."""
        return self.store.count()

    def close(self):
        """Close underlying resources if supported."""
        client = getattr(self.store, "client", None)
        if client and hasattr(client, "close"):
            client.close()


def create_repository(
    settings: LocalRagSettings,
    factory: Optional[Callable[..., BaseVectorStore]] = None,
) -> VectorStoreRepository:
    """Factory to create a repository from settings."""
    try:
        store_type = VectorStoreType(settings.vector_store)
    except ValueError:
        store_type = VectorStoreType.CHROMA

    store_factory = factory or get_vector_store
    store = store_factory(
        store_type=store_type,
        collection_name=settings.collection_name,
        persist_dir=str(settings.paths["persist_dir"]),
    )
    return VectorStoreRepository(store)
