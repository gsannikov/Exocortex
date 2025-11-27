#!/usr/bin/env python3
"""
Vector store abstraction for Local RAG.

Provides a unified interface for different vector databases:
- ChromaDB (default, local)
- Qdrant (optional, local or cloud)

Allows easy switching between backends without changing application code.
"""

import os

# Disable ChromaDB telemetry before any imports
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["CHROMA_TELEMETRY"] = "false"

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class VectorStoreType(str, Enum):
    """Available vector store backends."""
    CHROMA = "chroma"
    QDRANT = "qdrant"


@dataclass
class Document:
    """A document with embedding and metadata."""
    id: str
    text: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """A search result from the vector store."""
    id: str
    text: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseVectorStore(ABC):
    """Abstract base class for vector stores."""

    def __init__(self, collection_name: str = "docs", persist_dir: str = None):
        self.collection_name = collection_name
        self.persist_dir = persist_dir

    @abstractmethod
    def add_documents(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None
    ):
        """Add documents to the store."""
        pass

    @abstractmethod
    def delete_documents(self, ids: List[str] = None, where: Dict = None):
        """Delete documents by ID or filter."""
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: List[float],
        k: int = 10,
        where: Dict = None
    ) -> List[SearchResult]:
        """Search for similar documents."""
        pass

    @abstractmethod
    def get_documents(self, ids: List[str]) -> List[Document]:
        """Get documents by ID."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Get total document count."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all documents."""
        pass


class ChromaVectorStore(BaseVectorStore):
    """ChromaDB vector store implementation."""

    def __init__(
        self,
        collection_name: str = "docs",
        persist_dir: str = None,
        distance_metric: str = "cosine"
    ):
        super().__init__(collection_name, persist_dir)
        self.distance_metric = distance_metric
        self._client = None
        self._collection = None

    @property
    def client(self):
        """Lazy initialize ChromaDB client."""
        if self._client is None:
            import chromadb
            from chromadb.config import Settings

            if self.persist_dir:
                Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
                if hasattr(chromadb, "PersistentClient"):
                    # Chroma >=0.4 persistent client signature
                    self._client = chromadb.PersistentClient(
                        path=str(self.persist_dir),
                        settings=Settings(anonymized_telemetry=False),
                    )
                else:
                    # Older client signature
                    self._client = chromadb.Client(
                        Settings(
                            anonymized_telemetry=False,
                            persist_directory=str(self.persist_dir),
                        )
                    )
            else:
                self._client = chromadb.Client(
                    Settings(anonymized_telemetry=False)
                )
        return self._client

    @property
    def collection(self):
        """Get or create collection."""
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
        return self._collection

    def add_documents(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None
    ):
        """Add documents to ChromaDB."""
        if not ids:
            return

        # Ensure embeddings are lists (not numpy arrays)
        embeddings_list = [
            e.tolist() if hasattr(e, 'tolist') else list(e)
            for e in embeddings
        ]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings_list,
            metadatas=metadatas or [{} for _ in ids]
        )

    def upsert_documents(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None
    ):
        """Upsert documents (add or update)."""
        if not ids:
            return

        embeddings_list = [
            e.tolist() if hasattr(e, 'tolist') else list(e)
            for e in embeddings
        ]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings_list,
            metadatas=metadatas or [{} for _ in ids]
        )

    def delete_documents(self, ids: List[str] = None, where: Dict = None):
        """Delete documents from ChromaDB."""
        if ids:
            self.collection.delete(ids=ids)
        elif where:
            self.collection.delete(where=where)

    def search(
        self,
        query_embedding: List[float],
        k: int = 10,
        where: Dict = None
    ) -> List[SearchResult]:
        """Search ChromaDB."""
        query_emb = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else list(query_embedding)

        kwargs = {
            'query_embeddings': [query_emb],
            'n_results': k,
            'include': ['documents', 'metadatas', 'distances']
        }
        if where:
            kwargs['where'] = where

        results = self.collection.query(**kwargs)

        search_results = []
        if results.get('ids') and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                distance = results['distances'][0][i]
                # Convert distance to similarity (cosine distance -> similarity)
                score = 1 - distance

                search_results.append(SearchResult(
                    id=results['ids'][0][i],
                    text=results['documents'][0][i],
                    score=score,
                    metadata=results['metadatas'][0][i] if results.get('metadatas') else {}
                ))

        return search_results

    def get_documents(self, ids: List[str]) -> List[Document]:
        """Get documents by ID."""
        results = self.collection.get(ids=ids, include=['documents', 'metadatas', 'embeddings'])

        documents = []
        if results.get('ids'):
            for i, doc_id in enumerate(results['ids']):
                documents.append(Document(
                    id=doc_id,
                    text=results['documents'][i] if results.get('documents') else '',
                    embedding=results['embeddings'][i] if results.get('embeddings') else None,
                    metadata=results['metadatas'][i] if results.get('metadatas') else {}
                ))

        return documents

    def count(self) -> int:
        """Get document count."""
        return self.collection.count()

    def clear(self):
        """Clear all documents."""
        self.client.delete_collection(self.collection_name)
        self._collection = None


class QdrantVectorStore(BaseVectorStore):
    """
    Qdrant vector store implementation.

    Supports both local (in-memory/disk) and cloud deployments.
    """

    def __init__(
        self,
        collection_name: str = "docs",
        persist_dir: str = None,
        url: str = None,
        api_key: str = None,
        vector_size: int = 384,  # all-MiniLM-L6-v2 dimension
        distance_metric: str = "cosine"
    ):
        super().__init__(collection_name, persist_dir)
        self.url = url or os.getenv("QDRANT_URL")
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.vector_size = vector_size
        self.distance_metric = distance_metric
        self._client = None

    @property
    def client(self):
        """Lazy initialize Qdrant client."""
        if self._client is None:
            try:
                from qdrant_client import QdrantClient
                from qdrant_client.models import Distance, VectorParams
            except ImportError:
                raise ImportError(
                    "qdrant-client not installed. Run: pip install qdrant-client"
                )

            if self.url:
                # Remote Qdrant instance
                self._client = QdrantClient(
                    url=self.url,
                    api_key=self.api_key
                )
            elif self.persist_dir:
                # Local persistent storage
                Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
                self._client = QdrantClient(path=str(self.persist_dir))
            else:
                # In-memory
                self._client = QdrantClient(":memory:")

            # Create collection if it doesn't exist
            self._ensure_collection()

        return self._client

    def _ensure_collection(self):
        """Ensure collection exists."""
        from qdrant_client.models import Distance, VectorParams

        distance_map = {
            'cosine': Distance.COSINE,
            'euclidean': Distance.EUCLID,
            'dot': Distance.DOT
        }

        collections = self._client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self._client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=distance_map.get(self.distance_metric, Distance.COSINE)
                )
            )

    def add_documents(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None
    ):
        """Add documents to Qdrant."""
        if not ids:
            return

        from qdrant_client.models import PointStruct

        points = []
        for i, (doc_id, text, embedding) in enumerate(zip(ids, texts, embeddings)):
            # Convert embedding to list if needed
            emb_list = embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)

            # Prepare payload
            payload = metadatas[i] if metadatas else {}
            payload['text'] = text

            # Qdrant needs integer or UUID IDs
            point_id = self._to_point_id(doc_id)

            points.append(PointStruct(
                id=point_id,
                vector=emb_list,
                payload={**payload, '_original_id': doc_id}
            ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def _to_point_id(self, doc_id: str) -> str:
        """Convert document ID to Qdrant-compatible UUID."""
        # Create deterministic UUID from string ID
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))

    def delete_documents(self, ids: List[str] = None, where: Dict = None):
        """Delete documents from Qdrant."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        if ids:
            point_ids = [self._to_point_id(doc_id) for doc_id in ids]
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=point_ids
            )
        elif where:
            # Convert where dict to Qdrant filter
            conditions = []
            for key, value in where.items():
                conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )
            if conditions:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=Filter(must=conditions)
                )

    def search(
        self,
        query_embedding: List[float],
        k: int = 10,
        where: Dict = None
    ) -> List[SearchResult]:
        """Search Qdrant."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        query_emb = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else list(query_embedding)

        # Build filter if provided
        query_filter = None
        if where:
            conditions = []
            for key, value in where.items():
                conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )
            if conditions:
                query_filter = Filter(must=conditions)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_emb,
            limit=k,
            query_filter=query_filter,
            with_payload=True
        )

        search_results = []
        for result in results:
            payload = result.payload or {}
            text = payload.pop('text', '')
            original_id = payload.pop('_original_id', str(result.id))

            search_results.append(SearchResult(
                id=original_id,
                text=text,
                score=result.score,
                metadata=payload
            ))

        return search_results

    def get_documents(self, ids: List[str]) -> List[Document]:
        """Get documents by ID."""
        point_ids = [self._to_point_id(doc_id) for doc_id in ids]

        results = self.client.retrieve(
            collection_name=self.collection_name,
            ids=point_ids,
            with_payload=True,
            with_vectors=True
        )

        documents = []
        for result in results:
            payload = result.payload or {}
            text = payload.pop('text', '')
            original_id = payload.pop('_original_id', str(result.id))

            documents.append(Document(
                id=original_id,
                text=text,
                embedding=result.vector,
                metadata=payload
            ))

        return documents

    def count(self) -> int:
        """Get document count."""
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count

    def clear(self):
        """Clear all documents."""
        self.client.delete_collection(self.collection_name)
        self._ensure_collection()


def get_vector_store(
    store_type: VectorStoreType = VectorStoreType.CHROMA,
    collection_name: str = "docs",
    persist_dir: str = None,
    **kwargs
) -> BaseVectorStore:
    """
    Factory function to create a vector store.

    Args:
        store_type: Type of vector store to create
        collection_name: Name of the collection
        persist_dir: Directory for persistent storage
        **kwargs: Additional arguments for specific store types

    Returns:
        Vector store instance
    """
    stores = {
        VectorStoreType.CHROMA: ChromaVectorStore,
        VectorStoreType.QDRANT: QdrantVectorStore,
    }

    store_class = stores.get(store_type, ChromaVectorStore)
    return store_class(
        collection_name=collection_name,
        persist_dir=persist_dir,
        **kwargs
    )


def get_vector_store_from_env(
    collection_name: str = "docs",
    persist_dir: str = None
) -> BaseVectorStore:
    """
    Create vector store based on environment variables.

    Environment variables:
        VECTOR_STORE: "chroma" or "qdrant"
        QDRANT_URL: Qdrant server URL (optional)
        QDRANT_API_KEY: Qdrant API key (optional)
    """
    store_type_str = os.getenv("VECTOR_STORE", "chroma").lower()

    try:
        store_type = VectorStoreType(store_type_str)
    except ValueError:
        store_type = VectorStoreType.CHROMA

    kwargs = {}
    if store_type == VectorStoreType.QDRANT:
        kwargs['url'] = os.getenv("QDRANT_URL")
        kwargs['api_key'] = os.getenv("QDRANT_API_KEY")

    return get_vector_store(
        store_type=store_type,
        collection_name=collection_name,
        persist_dir=persist_dir,
        **kwargs
    )
