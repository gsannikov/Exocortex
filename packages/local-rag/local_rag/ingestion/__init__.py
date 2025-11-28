"""Ingestion helpers for Local RAG."""

from . import extractors as extractor  # backward compat alias

__all__ = ["extractors", "extractor", "ocr", "discover", "filters", "chunking", "utils"]
