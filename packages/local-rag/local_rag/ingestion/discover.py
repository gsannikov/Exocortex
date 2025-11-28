"""File discovery utilities with include/exclude globs."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path
from typing import Iterable, List, Set


def _is_excluded_dir(path: Path, exclude_dirs: Set[str]) -> bool:
    """Check if any parent directory is excluded by name."""
    return any(parent.name in exclude_dirs for parent in path.parents)


def _matches_globs(rel_path: str, globs: List[str]) -> bool:
    return any(fnmatch(rel_path, pattern) for pattern in globs)


def discover_files(
    root: Path,
    allowed_exts: Set[str],
    exclude_dirs: Set[str],
    include_globs: List[str] | None = None,
    exclude_globs: List[str] | None = None,
) -> Iterable[Path]:
    """
    Yield files under root that match extensions and glob filters.

    include_globs: if provided, only files matching any pattern are kept.
    exclude_globs: files matching any pattern are skipped.
    """
    include_globs = include_globs or []
    exclude_globs = exclude_globs or []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if _is_excluded_dir(path, exclude_dirs):
            continue

        if path.suffix.lower() not in allowed_exts:
            continue

        rel = path.relative_to(root)
        rel_str = str(rel)

        if include_globs and not _matches_globs(rel_str, include_globs):
            continue

        if exclude_globs and _matches_globs(rel_str, exclude_globs):
            continue

        yield path
