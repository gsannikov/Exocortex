"""
Centralized runtime settings for Local RAG.

Pydantic Settings gives us a single source of truth for defaults and environment
parsing. CLI and MCP should load this once and pass the object into services.
"""

from __future__ import annotations

import os
import platform
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_user_data_dir() -> Path:
    """Use a mac-friendly Application Support path, fall back to home on other OSes."""
    if platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / "local-rag"
    return Path.home() / ".local-rag-data"


class LocalRagSettings(BaseSettings):
    """Typed, centralized configuration."""

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )

    # Paths / storage
    user_data_dir: Path = Field(default_factory=_default_user_data_dir, env="USER_DATA_DIR")
    collection_name: str = Field(default="docs", env="COLLECTION_NAME")
    vector_store: str = Field(default="chroma", env="VECTOR_STORE")

    # Embeddings / chunking
    embed_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", env="EMBED_MODEL")
    chunk_size: int = Field(default=3000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=400, env="CHUNK_OVERLAP")
    chunking_strategy: str = Field(default="template", env="CHUNKING_STRATEGY")
    chunk_min_chars: int = Field(default=40, env="CHUNK_MIN_CHARS")
    chunk_strip_control: bool = Field(default=True, env="CHUNK_STRIP_CONTROL")
    chunk_min_entropy: float = Field(default=0.0, env="CHUNK_MIN_ENTROPY")

    # Search
    search_method: str = Field(default="hybrid", env="SEARCH_METHOD")
    vector_weight: float = Field(default=0.7, env="VECTOR_WEIGHT")
    bm25_weight: float = Field(default=0.3, env="BM25_WEIGHT")
    use_reranker: bool = Field(default=False, env="USE_RERANKER")

    # OCR
    ocr_enabled: bool = Field(default=True, env="OCR_ENABLED")
    ocr_engine: str = Field(default="paddle", env="OCR_ENGINE")
    ocr_lang: str = Field(default="en,he", env="OCR_LANG")
    ocr_max_pages: int = Field(default=120, env="OCR_MAX_PAGES")
    ocr_page_dpi: int = Field(default=200, env="OCR_PAGE_DPI")
    ocr_cache_dir: Optional[Path] = Field(default=None, env="OCR_CACHE_DIR")

    # Execution / ergonomics
    tokenizers_parallelism: bool = Field(default=False, env="TOKENIZERS_PARALLELISM")
    parallel_workers: Optional[int] = Field(default=6, env="LOCAL_RAG_PARALLEL")
    max_errors: Optional[int] = Field(default=20, env="LOCAL_RAG_MAX_ERRORS")
    include_globs: List[str] = Field(default_factory=list, env="LOCAL_RAG_INCLUDE")
    exclude_globs: List[str] = Field(default_factory=list, env="LOCAL_RAG_EXCLUDE")

    def apply_runtime_env(self):
        """
        Apply runtime env tweaks that should be consistent for the process.

        Note: This is intentionally idempotent.
        """
        if not self.tokenizers_parallelism:
            os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    @property
    def paths(self) -> dict[str, Path]:
        """Standardize all user data paths off user_data_dir."""
        base = Path(self.user_data_dir).expanduser()
        return {
            "base": base,
            "persist_dir": base / "vectordb",
            "state_path": base / "state" / "ingest_state.json",
            "bm25_path": base / "state" / "bm25_index.json",
        }


@lru_cache(maxsize=1)
def get_settings(**overrides) -> LocalRagSettings:
    """
    Load settings once per process; allows overrides for tests or CLI injection.
    """
    settings = LocalRagSettings(**overrides)
    settings.apply_runtime_env()
    return settings
