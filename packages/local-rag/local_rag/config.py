import os
from pathlib import Path
from typing import Dict

# Vector Store Settings
VECTOR_STORE = os.getenv("VECTOR_STORE", "chroma")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docs")

# Embedding Settings
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Chunking Settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "3000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "400"))
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "template")

# Search Settings
SEARCH_METHOD = os.getenv("SEARCH_METHOD", "hybrid")
VECTOR_WEIGHT = float(os.getenv("VECTOR_WEIGHT", "0.7"))
BM25_WEIGHT = float(os.getenv("BM25_WEIGHT", "0.3"))
USE_RERANKER = os.getenv("USE_RERANKER", "false").lower() == "true"

# OCR Settings
OCR_ENABLED = os.getenv("OCR_ENABLED", "true").lower() == "true"
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
OCR_LANG = os.getenv("OCR_LANG", "en,he")
OCR_MAX_PAGES = int(os.getenv("OCR_MAX_PAGES", "120"))
OCR_PAGE_DPI = int(os.getenv("OCR_PAGE_DPI", "200"))

def get_paths(user_data_dir: str) -> Dict[str, Path]:
    """Get persistence paths based on user data directory."""
    base = Path(user_data_dir)
    return {
        'base': base,
        'persist_dir': base / "vectordb",
        'state_path': base / "state" / "ingest_state.json",
        'bm25_path': base / "state" / "bm25_index.json"
    }
