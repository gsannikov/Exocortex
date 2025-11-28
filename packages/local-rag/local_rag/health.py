"""Lightweight health/status helpers for Local RAG."""

from __future__ import annotations

import time
from typing import Optional, Dict, Any

from .settings import LocalRagSettings, get_settings
from .storage import create_repository
from .vectorstore import get_vector_store
from .services.index_service import load_state


def get_health(settings: Optional[LocalRagSettings] = None) -> Dict[str, Any]:
    """
    Return a small health snapshot: vector count and last index mtime.
    """
    settings = settings or get_settings()
    repo = create_repository(settings, factory=get_vector_store)
    count = repo.count()
    state = load_state(settings.paths["state_path"])
    last_index = None
    if state:
        try:
            last_index = max(entry.get("mtime", 0) for entry in state.values())
        except Exception:
            last_index = None

    return {
        "vector_count": count,
        "last_index_mtime": last_index,
        "last_index_readable": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_index))
        if last_index
        else None,
        "user_data_dir": str(settings.user_data_dir),
        "collection": settings.collection_name,
    }
