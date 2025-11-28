"""Pytest configuration, fixtures, and lightweight stubs to keep tests fast."""

import hashlib
import io
import os
import sys
import tempfile
import types
from pathlib import Path
import json

import pytest

os.environ.setdefault("OCR_CACHE_DIR", str(Path(tempfile.gettempdir()) / "local-rag-test-ocr"))


# -------------------------
# Lightweight dependency stubs
# -------------------------
os.environ.setdefault("OCR_ENGINE", "unsupported")

# sentence-transformers stub (avoid torch download)
fake_st = types.ModuleType("sentence_transformers")


class FakeSentenceTransformer:
    def __init__(self, name=None):
        self.name = name

    def encode(self, texts, normalize_embeddings=True, batch_size=None):
        if isinstance(texts, str):
            texts = [texts]

        class FakeEmbeddings(list):
            def tolist(self):
                return list(self)

        class FakeVector(list):
            def tolist(self):
                return list(self)

        embeddings = FakeEmbeddings()
        for text in texts:
            base = float((len(text) % 10) + 1)
            embeddings.append(FakeVector([base, base / 2, base / 3, base / 4]))
        return embeddings


class FakeCrossEncoder:
    def __init__(self, name=None):
        self.name = name

    def predict(self, pairs):
        return [0.5 for _ in pairs]


fake_st.SentenceTransformer = FakeSentenceTransformer
fake_st.CrossEncoder = FakeCrossEncoder
sys.modules["sentence_transformers"] = fake_st

# rapidfuzz stub
fake_rf = types.ModuleType("rapidfuzz")
fake_rf.fuzz = types.SimpleNamespace(partial_ratio=lambda a, b: 100)
sys.modules["rapidfuzz"] = fake_rf

# pypdf/pdf2image/PIL stubs (minimal for tests)
class FakeImage:
    def __init__(self, content=None, **_kwargs):
        self.mode = "RGB"
        self.size = (1, 1)
        self._content = b"" if content is None else str(content).encode()

    @staticmethod
    def new(mode, size, color=None):
        return FakeImage(content=color)

    @staticmethod
    def open(*_args, **_kwargs):
        return FakeImage()

    def convert(self, *_args, **_kwargs):
        return self

    def save(self, fp, format=None):
        if hasattr(fp, "write"):
            fp.write(self._content)


fake_pypdf = types.ModuleType("pypdf")
fake_pypdf.PdfReader = lambda *args, **kwargs: types.SimpleNamespace(pages=[])
sys.modules["pypdf"] = fake_pypdf

fake_pdf2image = types.ModuleType("pdf2image")
fake_pdf2image.convert_from_path = lambda *args, **kwargs: []
sys.modules["pdf2image"] = fake_pdf2image

fake_pil = types.ModuleType("PIL")
fake_pil.Image = FakeImage
sys.modules["PIL"] = fake_pil
sys.modules["PIL.Image"] = FakeImage

# paddleocr / paddlepaddle stubs
fake_paddleocr = types.ModuleType("paddleocr")


class FakePaddleOCR:
    def __init__(self, *args, **kwargs):
        pass

    def ocr(self, *_args, **_kwargs):
        return [[]]


fake_paddleocr.PaddleOCR = FakePaddleOCR
sys.modules["paddleocr"] = fake_paddleocr
sys.modules["paddlepaddle"] = types.ModuleType("paddlepaddle")

# surya stub (used if engine set to surya)
fake_surya = types.ModuleType("surya")
fake_surya.ocr = types.SimpleNamespace(run_ocr=lambda arr: [[{"text_blocks": []}]])
sys.modules["surya"] = fake_surya

# numpy stub (only minimal use in OCR paths)
fake_np = types.ModuleType("numpy")
fake_np.array = lambda x: x
sys.modules["numpy"] = fake_np

# -------------------------
# Stub mcp_server module (missing in repo)
# -------------------------
fake_mcp = types.ModuleType("mcp_server")
fake_mcp.STATE_PATH = Path("state/test_state.json")


def chunk_text(text: str, size: int = 100, overlap: int = 20):
    if not text:
        return []
    chunks = []
    i = 0
    n = len(text)
    while i < n:
        j = min(n, i + size)
        chunks.append((i, j, text[i:j]))
        if j == n:
            break
        i = j - overlap
    return chunks


def fhash(path: Path) -> str:
    h = hashlib.sha1()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_state():
    if fake_mcp.STATE_PATH.exists():
        try:
            return json.loads(fake_mcp.STATE_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_state(state):
    path = fake_mcp.STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state))


fake_mcp.chunk_text = chunk_text
fake_mcp.fhash = fhash
fake_mcp.load_state = load_state
fake_mcp.save_state = save_state
sys.modules["mcp_server"] = fake_mcp

# -------------------------
# Project import path + in-memory vector store stub
# -------------------------
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACKAGE_ROOT))

import local_rag.vectorstore as vectorstore  # noqa: E402
from local_rag.ingest import ocr as ingest_ocr  # noqa: E402
from local_rag.ingest import extractor as ingest_extractor  # noqa: E402
from local_rag.ingest import utils as ingest_utils  # noqa: E402
import local_rag.ingest as ingest  # noqa: E402

# Provide legacy module aliases for tests that import the old layout
sys.modules["vectorstore"] = vectorstore
sys.modules["ingest"] = ingest
sys.modules["ingest.ocr"] = ingest_ocr
sys.modules["ingest.extractor"] = ingest_extractor
sys.modules["ingest.utils"] = ingest_utils
import local_rag.indexer as indexer  # noqa: E402
sys.modules["indexer"] = indexer
import local_rag.query as query  # noqa: E402
sys.modules["query"] = query

_GLOBAL_STORE = {}


class InMemoryVectorStore(vectorstore.BaseVectorStore):
    """Minimal vector store used across tests."""

    def __init__(self, collection_name: str = "docs", persist_dir: str = None):
        super().__init__(collection_name, persist_dir)
        key = (persist_dir or "memory", collection_name)
        self._key = key
        if key not in _GLOBAL_STORE:
            _GLOBAL_STORE[key] = {}
        self._docs = _GLOBAL_STORE[key]
        if persist_dir:
            Path(persist_dir).mkdir(parents=True, exist_ok=True)

    def add_documents(self, ids, texts, embeddings, metadatas=None):
        metadatas = metadatas or [{} for _ in ids]
        for doc_id, text, emb, meta in zip(ids, texts, embeddings, metadatas):
            self._docs[doc_id] = {
                "text": text,
                "embedding": list(emb),
                "metadata": meta or {}
            }

    def upsert_documents(self, ids, texts, embeddings, metadatas=None):
        self.add_documents(ids, texts, embeddings, metadatas)

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
            emb = data.get("embedding") or []
            score = 0.0
            if emb and query_embedding:
                diff = sum(abs(float(a) - float(b)) for a, b in zip(query_embedding, emb))
                score = -diff
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


def _get_store(*_args, collection_name="docs", persist_dir=None, **_kwargs):
    return InMemoryVectorStore(collection_name=collection_name, persist_dir=persist_dir)


vectorstore.ChromaVectorStore = InMemoryVectorStore
vectorstore.get_vector_store = _get_store
vectorstore.get_vector_store_from_env = lambda *_args, **_kwargs: _get_store()

import local_rag.indexer as indexer  # noqa: E402
import local_rag.query as query  # noqa: E402

indexer.get_vector_store = _get_store
query.get_vector_store = _get_store


# -------------------------
# Standard fixtures
# -------------------------
@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_file(temp_dir):
    """Create a sample text file for testing."""
    file_path = temp_dir / "sample.txt"
    file_path.write_text("This is a sample text file for testing.\nIt has multiple lines.")
    return file_path


@pytest.fixture
def sample_md_file(temp_dir):
    """Create a sample markdown file for testing."""
    file_path = temp_dir / "sample.md"
    file_path.write_text("# Sample Markdown\n\nThis is a test document.")
    return file_path


@pytest.fixture
def mock_env(monkeypatch, temp_dir):
    """Set up mock environment variables for testing."""
    monkeypatch.setenv("ROOT_DIR", str(temp_dir))
    monkeypatch.setenv("ALLOWED_EXTS", ".txt,.md,.pdf")
    monkeypatch.setenv("CHUNK_SIZE", "100")
    monkeypatch.setenv("CHUNK_OVERLAP", "20")
    monkeypatch.setenv("PERSIST_DIR", str(temp_dir / ".chromadb"))
    monkeypatch.setenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    return temp_dir


@pytest.fixture
def sample_long_text():
    """Create a long text for chunking tests."""
    return "word " * 100  # 500 characters (100 words * 5 chars each)
