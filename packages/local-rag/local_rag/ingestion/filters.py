"""Chunk quality filters and sanitizers."""

from __future__ import annotations

import math
import string
from typing import Iterable, List, Tuple

from .chunking import Chunk

CONTROL_CHARS = "".join(map(chr, range(0, 32))) + chr(127)
CONTROL_TRANS = str.maketrans("", "", CONTROL_CHARS)


def strip_control_chars(text: str) -> str:
    """Remove control characters while preserving newlines and tabs."""
    # Keep newline and tab; drop other control chars.
    keep = {"\n", "\t"}
    filtered = []
    for ch in text:
        if ch in keep:
            filtered.append(ch)
        elif ch in CONTROL_CHARS:
            continue
        else:
            filtered.append(ch)
    return "".join(filtered)


def _entropy(text: str) -> float:
    """Compute Shannon entropy; low entropy often means low-quality content."""
    if not text:
        return 0.0
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    length = len(text)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def filter_chunks(
    chunks: Iterable[Chunk],
    min_chars: int = 40,
    min_entropy: float = 0.0,
    strip_control: bool = True,
) -> Tuple[List[Chunk], int]:
    """
    Apply basic quality filters to chunks.

    Returns (filtered_chunks, dropped_count).
    """
    kept = []
    dropped = 0

    for chunk in chunks:
        text = chunk.text or ""
        if strip_control:
            text = strip_control_chars(text)

        if len(text.strip()) < min_chars:
            dropped += 1
            continue

        if min_entropy and _entropy(text) < min_entropy:
            dropped += 1
            continue

        kept.append(Chunk(text=text, start=chunk.start, end=chunk.end, metadata=chunk.metadata))

    return kept, dropped
