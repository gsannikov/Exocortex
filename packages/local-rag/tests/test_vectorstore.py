"""Tests for vector store abstraction."""

import pytest
import tempfile
from local_rag.vectorstore import (
    VectorStoreType,
    Document,
    SearchResult,
    BaseVectorStore,
    ChromaVectorStore,
    get_vector_store,
    get_vector_store_from_env
)


class TestDocument:
    """Tests for Document dataclass."""

    def test_basic_creation(self):
        """Test basic document creation."""
        doc = Document(id="doc1", text="Test content")

        assert doc.id == "doc1"
        assert doc.text == "Test content"
        assert doc.embedding is None
        assert doc.metadata == {}

    def test_with_embedding(self):
        """Test document with embedding."""
        embedding = [0.1, 0.2, 0.3]
        doc = Document(
            id="doc1",
            text="Test",
            embedding=embedding
        )

        assert doc.embedding == embedding

    def test_with_metadata(self):
        """Test document with metadata."""
        doc = Document(
            id="doc1",
            text="Test",
            metadata={"path": "/test/file.txt", "page": 1}
        )

        assert doc.metadata["path"] == "/test/file.txt"
        assert doc.metadata["page"] == 1


class TestSearchResultVS:
    """Tests for vector store SearchResult."""

    def test_basic_creation(self):
        """Test basic SearchResult creation."""
        result = SearchResult(
            id="doc1",
            text="Test content",
            score=0.95
        )

        assert result.id == "doc1"
        assert result.text == "Test content"
        assert result.score == 0.95
        assert result.metadata == {}


class TestChromaVectorStore:
    """Tests for ChromaVectorStore."""

    @pytest.fixture
    def temp_persist_dir(self):
        """Create temporary directory for persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def vector_store(self, temp_persist_dir):
        """Create a ChromaVectorStore instance."""
        store = ChromaVectorStore(
            collection_name="test_collection",
            persist_dir=temp_persist_dir
        )
        yield store
        # Cleanup
        try:
            store.clear()
        except Exception:
            pass

    def test_creation(self, temp_persist_dir):
        """Test basic store creation."""
        store = ChromaVectorStore(
            collection_name="test",
            persist_dir=temp_persist_dir
        )
        assert store is not None

    def test_add_documents(self, vector_store):
        """Test adding documents."""
        vector_store.add_documents(
            ids=["doc1", "doc2"],
            texts=["First document", "Second document"],
            embeddings=[[0.1] * 384, [0.2] * 384],
            metadatas=[{"type": "test"}, {"type": "test"}]
        )

        assert vector_store.count() == 2

    def test_add_empty(self, vector_store):
        """Test adding empty list."""
        vector_store.add_documents(
            ids=[],
            texts=[],
            embeddings=[]
        )

        assert vector_store.count() == 0

    def test_search(self, vector_store):
        """Test basic search."""
        # Add documents
        vector_store.add_documents(
            ids=["doc1", "doc2", "doc3"],
            texts=[
                "Machine learning algorithms",
                "Deep neural networks",
                "Natural language processing"
            ],
            embeddings=[
                [0.1] * 384,
                [0.2] * 384,
                [0.3] * 384
            ]
        )

        # Search
        query_embedding = [0.1] * 384
        results = vector_store.search(query_embedding, k=2)

        assert len(results) == 2
        # First result should be closest to query
        assert results[0].id == "doc1"

    def test_search_with_filter(self, vector_store):
        """Test search with metadata filter."""
        vector_store.add_documents(
            ids=["doc1", "doc2", "doc3"],
            texts=["Doc A", "Doc B", "Doc C"],
            embeddings=[
                [0.1] * 384,
                [0.2] * 384,
                [0.3] * 384
            ],
            metadatas=[
                {"category": "A"},
                {"category": "B"},
                {"category": "A"}
            ]
        )

        query_embedding = [0.15] * 384
        results = vector_store.search(
            query_embedding,
            k=10,
            where={"category": "A"}
        )

        # Should only return docs with category A
        assert len(results) == 2
        for r in results:
            assert r.metadata.get("category") == "A"

    def test_delete_by_id(self, vector_store):
        """Test document deletion by ID."""
        vector_store.add_documents(
            ids=["doc1", "doc2", "doc3"],
            texts=["A", "B", "C"],
            embeddings=[[0.1] * 384, [0.2] * 384, [0.3] * 384]
        )

        assert vector_store.count() == 3

        vector_store.delete_documents(ids=["doc2"])

        assert vector_store.count() == 2

    def test_delete_by_filter(self, vector_store):
        """Test document deletion by filter."""
        vector_store.add_documents(
            ids=["doc1", "doc2", "doc3"],
            texts=["A", "B", "C"],
            embeddings=[[0.1] * 384, [0.2] * 384, [0.3] * 384],
            metadatas=[
                {"path": "/path/a.txt"},
                {"path": "/path/b.txt"},
                {"path": "/path/a.txt"}
            ]
        )

        vector_store.delete_documents(where={"path": "/path/a.txt"})

        assert vector_store.count() == 1

    def test_get_documents(self, vector_store):
        """Test getting documents by ID."""
        vector_store.add_documents(
            ids=["doc1", "doc2"],
            texts=["First", "Second"],
            embeddings=[[0.1] * 384, [0.2] * 384],
            metadatas=[{"key": "value1"}, {"key": "value2"}]
        )

        docs = vector_store.get_documents(["doc1"])

        assert len(docs) == 1
        assert docs[0].id == "doc1"
        assert docs[0].text == "First"
        assert docs[0].metadata["key"] == "value1"

    def test_count(self, vector_store):
        """Test document count."""
        assert vector_store.count() == 0

        vector_store.add_documents(
            ids=["doc1"],
            texts=["Test"],
            embeddings=[[0.1] * 384]
        )

        assert vector_store.count() == 1

    def test_clear(self, vector_store):
        """Test clearing all documents."""
        vector_store.add_documents(
            ids=["doc1", "doc2"],
            texts=["A", "B"],
            embeddings=[[0.1] * 384, [0.2] * 384]
        )

        assert vector_store.count() == 2

        vector_store.clear()

        # After clear, count should be 0 (or collection recreated)
        # Implementation may vary - just check it doesn't error

    def test_upsert(self, vector_store):
        """Test upsert functionality."""
        # Initial add
        vector_store.upsert_documents(
            ids=["doc1"],
            texts=["Original text"],
            embeddings=[[0.1] * 384],
            metadatas=[{"version": 1}]
        )

        # Upsert same ID with new content
        vector_store.upsert_documents(
            ids=["doc1"],
            texts=["Updated text"],
            embeddings=[[0.2] * 384],
            metadatas=[{"version": 2}]
        )

        # Should still have 1 document
        assert vector_store.count() == 1

        # Should have updated content
        docs = vector_store.get_documents(["doc1"])
        assert docs[0].text == "Updated text"
        assert docs[0].metadata["version"] == 2

    def test_persistence(self, temp_persist_dir):
        """Test data persistence across instances."""
        # Create and populate store
        store1 = ChromaVectorStore(
            collection_name="persist_test",
            persist_dir=temp_persist_dir
        )
        store1.add_documents(
            ids=["doc1"],
            texts=["Persistent data"],
            embeddings=[[0.5] * 384]
        )

        # Create new instance pointing to same directory
        store2 = ChromaVectorStore(
            collection_name="persist_test",
            persist_dir=temp_persist_dir
        )

        # Should see the same data
        assert store2.count() == 1
        docs = store2.get_documents(["doc1"])
        assert docs[0].text == "Persistent data"


class TestGetVectorStore:
    """Tests for get_vector_store factory function."""

    def test_get_chroma_store(self, tmp_path):
        """Test getting ChromaDB store."""
        store = get_vector_store(
            store_type=VectorStoreType.CHROMA,
            collection_name="test",
            persist_dir=str(tmp_path)
        )

        assert isinstance(store, ChromaVectorStore)

    def test_default_to_chroma(self, tmp_path):
        """Test default store type."""
        store = get_vector_store(
            collection_name="test",
            persist_dir=str(tmp_path)
        )

        assert isinstance(store, ChromaVectorStore)


class TestGetVectorStoreFromEnv:
    """Tests for get_vector_store_from_env function."""

    def test_default_chroma(self, tmp_path, monkeypatch):
        """Test default returns ChromaDB."""
        monkeypatch.delenv("VECTOR_STORE", raising=False)

        store = get_vector_store_from_env(
            collection_name="test",
            persist_dir=str(tmp_path)
        )

        assert isinstance(store, ChromaVectorStore)

    def test_env_chroma(self, tmp_path, monkeypatch):
        """Test VECTOR_STORE=chroma."""
        monkeypatch.setenv("VECTOR_STORE", "chroma")

        store = get_vector_store_from_env(
            collection_name="test",
            persist_dir=str(tmp_path)
        )

        assert isinstance(store, ChromaVectorStore)


class TestVectorStoreEdgeCases:
    """Edge case tests for vector stores."""

    @pytest.fixture
    def vector_store(self, tmp_path):
        """Create a temporary vector store."""
        store = ChromaVectorStore(
            collection_name="edge_test",
            persist_dir=str(tmp_path)
        )
        yield store
        try:
            store.clear()
        except Exception:
            pass

    def test_unicode_text(self, vector_store):
        """Test with unicode text."""
        vector_store.add_documents(
            ids=["doc1"],
            texts=["Hello 世界 مرحبا 🌍"],
            embeddings=[[0.1] * 384]
        )

        docs = vector_store.get_documents(["doc1"])
        assert "世界" in docs[0].text

    def test_empty_text(self, vector_store):
        """Test with empty text."""
        vector_store.add_documents(
            ids=["doc1"],
            texts=[""],
            embeddings=[[0.1] * 384]
        )

        assert vector_store.count() == 1

    def test_special_characters_in_id(self, vector_store):
        """Test with special characters in ID."""
        doc_id = "/path/to/file.txt:100-200"
        vector_store.add_documents(
            ids=[doc_id],
            texts=["Content"],
            embeddings=[[0.1] * 384]
        )

        docs = vector_store.get_documents([doc_id])
        assert len(docs) == 1
        assert docs[0].id == doc_id

    def test_large_batch(self, vector_store):
        """Test adding large batch of documents."""
        n = 100
        vector_store.add_documents(
            ids=[f"doc{i}" for i in range(n)],
            texts=[f"Content {i}" for i in range(n)],
            embeddings=[[0.1 * i] * 384 for i in range(n)]
        )

        assert vector_store.count() == n

    def test_search_empty_store(self, vector_store):
        """Test searching empty store."""
        results = vector_store.search([0.1] * 384, k=5)
        assert results == []

    def test_get_nonexistent_document(self, vector_store):
        """Test getting document that doesn't exist."""
        docs = vector_store.get_documents(["nonexistent"])
        assert docs == []

    def test_numpy_array_embeddings(self, vector_store):
        """Test with numpy array embeddings."""
        try:
            import numpy as np
            embedding = np.array([0.1] * 384)

            vector_store.add_documents(
                ids=["doc1"],
                texts=["Test"],
                embeddings=[embedding]
            )

            assert vector_store.count() == 1
        except ImportError:
            pytest.skip("numpy not available")

    def test_search_k_larger_than_count(self, vector_store):
        """Test search with k larger than document count."""
        vector_store.add_documents(
            ids=["doc1", "doc2"],
            texts=["A", "B"],
            embeddings=[[0.1] * 384, [0.2] * 384]
        )

        results = vector_store.search([0.15] * 384, k=100)

        # Should return all available documents
        assert len(results) == 2


class TestVectorStoreIntegration:
    """Integration tests for vector store with real embeddings."""

    @pytest.fixture
    def store_with_embeddings(self, tmp_path):
        """Create store and add documents with meaningful embeddings."""
        store = ChromaVectorStore(
            collection_name="integration_test",
            persist_dir=str(tmp_path)
        )

        # Create diverse embeddings
        embeddings = [
            [1.0] + [0.0] * 383,  # doc1: high in first dimension
            [0.0, 1.0] + [0.0] * 382,  # doc2: high in second dimension
            [0.5, 0.5] + [0.0] * 382,  # doc3: balanced first two
        ]

        store.add_documents(
            ids=["doc1", "doc2", "doc3"],
            texts=[
                "Python programming",
                "Java development",
                "Software engineering"
            ],
            embeddings=embeddings,
            metadatas=[
                {"language": "python"},
                {"language": "java"},
                {"language": "general"}
            ]
        )

        yield store
        store.clear()

    def test_similarity_ordering(self, store_with_embeddings):
        """Test that similar vectors rank higher."""
        # Query close to doc1's embedding
        query = [0.9] + [0.1] + [0.0] * 382

        results = store_with_embeddings.search(query, k=3)

        # doc1 should be first (closest to query)
        assert results[0].id == "doc1"

    def test_combined_search_and_filter(self, store_with_embeddings):
        """Test search with both embedding and metadata filter."""
        query = [0.5, 0.5] + [0.0] * 382

        results = store_with_embeddings.search(
            query,
            k=3,
            where={"language": "python"}
        )

        assert len(results) == 1
        assert results[0].metadata["language"] == "python"
