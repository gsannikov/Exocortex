"""Integration-style index + search round-trip tests."""

import math
import sys
import types
from pathlib import Path

import pytest


class FakeSentenceTransformer:
    """Lightweight deterministic embedding model for tests."""

    def __init__(self, name=None):
        self.name = name

    def encode(self, texts, normalize_embeddings=True, batch_size=None):
        if isinstance(texts, str):
            texts = [texts]

        class FakeEmbeddings(list):
            def tolist(self):
                return list(self)

        embeddings = FakeEmbeddings()
        for text in texts:
            # Simple deterministic embedding based on text length
            base = float((len(text) % 10) + 1)
            class FakeVector(list):
                def tolist(self):
                    return list(self)

            embeddings.append(FakeVector([base, base / 2, base / 3, base / 4]))
        return embeddings


class FakeCrossEncoder:
    """Stub cross-encoder with deterministic scores."""

    def __init__(self, name=None):
        self.name = name

    def predict(self, pairs):
        return [0.5 for _ in pairs]


def _cosine_similarity(a, b):
    """Compute cosine similarity between two equal-length vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a)) or 1.0
    norm_b = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (norm_a * norm_b)


# Inject lightweight stubs before importing project modules
fake_st = types.ModuleType("sentence_transformers")
fake_st.SentenceTransformer = FakeSentenceTransformer
fake_st.CrossEncoder = FakeCrossEncoder
sys.modules["sentence_transformers"] = fake_st

fake_rf = types.ModuleType("rapidfuzz")
fake_rf.fuzz = types.SimpleNamespace(partial_ratio=lambda a, b: 100)
sys.modules["rapidfuzz"] = fake_rf

# Stub heavy file/OCR dependencies
class _FakePdfReader:
    def __init__(self, *_args, **_kwargs):
        self.pages = []

fake_pypdf = types.ModuleType("pypdf")
fake_pypdf.PdfReader = _FakePdfReader
sys.modules["pypdf"] = fake_pypdf

fake_pdf2image = types.ModuleType("pdf2image")
fake_pdf2image.convert_from_path = lambda *args, **kwargs: []
sys.modules["pdf2image"] = fake_pdf2image

class _FakeImage:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def open(*_args, **_kwargs):
        return _FakeImage()

    def convert(self, *_args, **_kwargs):
        return self

from local_rag.services.index_service import DocumentIndexer
from local_rag.services.search_service import DocumentSearcher
from local_rag import search
from local_rag.adapters import vectorstore


class InMemoryChroma(vectorstore.BaseVectorStore):
    """Minimal in-memory stand-in for ChromaDB used in tests."""

    def __init__(self, collection_name: str = "docs", persist_dir: str = None):
        super().__init__(collection_name, persist_dir)
        self._docs = {}
        if persist_dir:
            Path(persist_dir).mkdir(parents=True, exist_ok=True)

    @property
    def collection(self):
        # HybridSearcher expects a Chroma-like collection with query()
        return self

    def add_documents(self, ids, texts, embeddings, metadatas=None):
        metadatas = metadatas or [{} for _ in ids]
        for doc_id, text, emb, meta in zip(ids, texts, embeddings, metadatas):
            self._docs[doc_id] = {
                "text": text,
                "embedding": list(emb),
                "metadata": meta or {}
            }

    def delete_documents(self, ids=None, where=None):
        if ids:
            for doc_id in ids:
                self._docs.pop(doc_id, None)
        elif where:
            self._docs = {
                doc_id: data
                for doc_id, data in self._docs.items()
                if not all(data["metadata"].get(k) == v for k, v in where.items())
            }

    def _filter_ids(self, where):
        if not where:
            return list(self._docs.keys())
        return [
            doc_id
            for doc_id, data in self._docs.items()
            if all(data["metadata"].get(k) == v for k, v in where.items())
        ]

    def search(self, query_embedding, k=10, where=None):
        candidates = self._filter_ids(where)
        scored = []
        for doc_id in candidates:
            data = self._docs[doc_id]
            score = _cosine_similarity(query_embedding, data["embedding"])
            scored.append(
                vectorstore.SearchResult(
                    id=doc_id,
                    text=data["text"],
                    score=score,
                    metadata=data["metadata"]
                )
            )
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:k]

    def get_documents(self, ids):
        docs = []
        for doc_id in ids:
            if doc_id in self._docs:
                data = self._docs[doc_id]
                docs.append(
                    vectorstore.Document(
                        id=doc_id,
                        text=data["text"],
                        metadata=data["metadata"]
                    )
                )
        return docs

    def count(self):
        return len(self._docs)

    def clear(self):
        self._docs.clear()

    # Chroma-like query interface used by HybridSearcher
    def query(self, query_embeddings, n_results, include, where=None):
        query_embedding = query_embeddings[0]
        results = self.search(query_embedding, k=n_results, where=where)
        distances = [[max(0.0, 1 - r.score) for r in results]]
        return {
            "ids": [[r.id for r in results]],
            "documents": [[r.text for r in results]],
            "metadatas": [[r.metadata for r in results]],
            "distances": distances
        }


@pytest.fixture
def patched_vector_store(monkeypatch):
    """Patch vector store creation to use in-memory implementation."""
    stores = {}

    def get_store(store_type=None, collection_name="docs", persist_dir=None):
        key = (collection_name, persist_dir or "memory")
        if key not in stores:
            stores[key] = InMemoryChroma(collection_name=collection_name, persist_dir=persist_dir)
        return stores[key]

    monkeypatch.setattr("vectorstore.ChromaVectorStore", InMemoryChroma)
    monkeypatch.setattr("local_rag.adapters.vectorstore.ChromaVectorStore", InMemoryChroma)
    monkeypatch.setattr("local_rag.services.index_service.get_vector_store", get_store)
    monkeypatch.setattr("local_rag.services.search_service.get_vector_store", get_store)
    return get_store


@pytest.fixture
def patched_embeddings(monkeypatch):
    """Patch sentence transformers to avoid heavy model downloads."""
    return FakeSentenceTransformer


@pytest.mark.integration
def test_index_and_search_round_trip(tmp_path, patched_vector_store, patched_embeddings):
    """Index sample docs then search and validate relevance + metadata."""
    source_dir = tmp_path / "docs"
    source_dir.mkdir()
    user_data_dir = tmp_path / "user-data"

    dogs = source_dir / "dogs.md"
    cats = source_dir / "cats.md"
    misc = source_dir / "notes.txt"

    dogs.write_text("Dogs are loyal pets that love to fetch balls and run.")
    cats.write_text("Cats prefer quiet naps on sunny windowsills and purr softly.")
    misc.write_text("Coffee beans are roasted and ground before brewing.")

    indexer = DocumentIndexer(
        user_data_dir=str(user_data_dir),
        chunk_size=256,
        chunk_overlap=32,
        chunking_strategy="fixed",
        parallel_workers=1,  # Force serial processing to avoid threading issues
    )

    # Ensure we are using the in-memory stand-in to keep the test lightweight
    assert isinstance(indexer.vector_store, InMemoryChroma)

    # Debug: verify files exist
    print(f"\nDEBUG: source_dir = {source_dir}")
    print(f"DEBUG: Files in source_dir:")
    for f in source_dir.iterdir():
        print(f"  - {f.name} ({f.stat().st_size} bytes)")
    
    stats = indexer.index_directory(source_dir)

    assert stats["files_processed"] == 3
    assert indexer.vector_store.count() >= 3
    assert indexer.bm25_index is not None
    assert indexer.bm25_index.doc_count >= 3

    searcher = DocumentSearcher(
        user_data_dir=str(user_data_dir),
        search_method="hybrid",
    )

    results = searcher.search("loyal dogs that fetch", k=3)
    assert results, "Expected search results for dog query"
    top_paths = [Path(item["path"]).name for item in results]
    assert "dogs.md" in top_paths[:2], "Dog document should rank near the top"

    cat_filtered = searcher.search(
        "quiet pets",
        k=3,
        metadata_filter={"filename": "cats.md"},
    )
    cat_filtered = [item for item in cat_filtered if Path(item["path"]).name == "cats.md"]
    assert cat_filtered, "Expected filtered result for cats"
    assert searcher.hybrid_searcher.bm25_index.doc_count >= 3
