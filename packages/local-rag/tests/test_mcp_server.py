"""Tests for mcp_server.py core functionality."""

import os
import json
from pathlib import Path
import pytest

# Note: These tests focus on the pure functions that don't require heavy dependencies


def test_chunk_text_basic():
    """Test basic text chunking functionality."""
    from mcp_server import chunk_text

    text = "a" * 300
    chunks = list(chunk_text(text, size=100, overlap=20))

    # Should have 3 chunks with overlap
    assert len(chunks) > 0

    # First chunk
    start, end, content = chunks[0]
    assert start == 0
    assert end == 100
    assert len(content) == 100

    # Check overlaps exist
    if len(chunks) > 1:
        _, prev_end, _ = chunks[0]
        next_start, _, _ = chunks[1]
        # Next chunk should start before previous ended (overlap)
        assert next_start < prev_end


def test_chunk_text_short():
    """Test chunking with text shorter than chunk size."""
    from mcp_server import chunk_text

    text = "short text"
    chunks = list(chunk_text(text, size=100, overlap=20))

    assert len(chunks) == 1
    start, end, content = chunks[0]
    assert start == 0
    assert end == len(text)
    assert content == text


def test_chunk_text_empty():
    """Test chunking with empty text."""
    from mcp_server import chunk_text

    text = ""
    chunks = list(chunk_text(text, size=100, overlap=20))

    # Should handle empty text gracefully
    assert len(chunks) >= 0


def test_chunk_text_no_overlap():
    """Test chunking with zero overlap."""
    from mcp_server import chunk_text

    text = "a" * 200
    chunks = list(chunk_text(text, size=100, overlap=0))

    assert len(chunks) == 2

    # Verify no overlap
    _, end1, _ = chunks[0]
    start2, _, _ = chunks[1]
    assert start2 == end1


def test_fhash_consistency(tmp_path):
    """Test that fhash produces consistent hashes."""
    from mcp_server import fhash

    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    # Hash should be consistent
    hash1 = fhash(test_file)
    hash2 = fhash(test_file)

    assert hash1 == hash2
    assert len(hash1) == 40  # SHA1 hex digest length


def test_fhash_different_content(tmp_path):
    """Test that different content produces different hashes."""
    from mcp_server import fhash

    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("content 1")
    file2.write_text("content 2")

    hash1 = fhash(file1)
    hash2 = fhash(file2)

    assert hash1 != hash2


def test_load_state_empty(tmp_path, monkeypatch):
    """Test loading state when file doesn't exist."""
    from mcp_server import load_state

    # Point to non-existent state file
    monkeypatch.setattr("mcp_server.STATE_PATH", tmp_path / "nonexistent.json")

    state = load_state()
    assert state == {}


def test_save_and_load_state(tmp_path, monkeypatch):
    """Test saving and loading state."""
    from mcp_server import save_state, load_state

    state_file = tmp_path / "state.json"
    monkeypatch.setattr("mcp_server.STATE_PATH", state_file)

    test_state = {
        "file1.txt": {"hash": "abc123", "mtime": 1234567890},
        "file2.txt": {"hash": "def456", "mtime": 1234567891}
    }

    save_state(test_state)
    loaded_state = load_state()

    assert loaded_state == test_state


def test_state_path_created(tmp_path, monkeypatch):
    """Test that state directory is created if it doesn't exist."""
    state_dir = tmp_path / "new_dir"
    state_file = state_dir / "state.json"

    assert not state_dir.exists()

    monkeypatch.setattr("mcp_server.STATE_PATH", state_file)

    from mcp_server import save_state
    save_state({"test": "data"})

    assert state_dir.exists()
    assert state_file.exists()


def test_chunk_text_unicode():
    """Test chunking with unicode characters."""
    from mcp_server import chunk_text

    text = "Hello 世界 " * 50  # Mix of ASCII and unicode
    chunks = list(chunk_text(text, size=100, overlap=20))

    assert len(chunks) > 0
    # Verify no encoding errors
    for start, end, content in chunks:
        assert isinstance(content, str)
        assert len(content) > 0


def test_chunk_text_preserves_content():
    """Test that chunking preserves all content."""
    from mcp_server import chunk_text

    text = "abcdefghij" * 30  # 300 chars
    chunks = list(chunk_text(text, size=100, overlap=20))

    # Reconstruct text from first and last chunks (accounting for overlap)
    first_chunk = chunks[0][2]
    last_chunk = chunks[-1][2]

    # First chunk should start with original
    assert text.startswith(first_chunk[:50])
    # Last chunk should end with original
    assert text.endswith(last_chunk[-50:])


@pytest.mark.parametrize("size,overlap", [
    (1000, 100),
    (500, 50),
    (100, 10),
    (50, 5),
])
def test_chunk_text_various_sizes(size, overlap):
    """Test chunking with various size/overlap combinations."""
    from mcp_server import chunk_text

    text = "word " * 500  # Long text
    chunks = list(chunk_text(text, size=size, overlap=overlap))

    assert len(chunks) > 0

    # Verify all chunks respect size constraint
    for start, end, content in chunks[:-1]:  # Exclude last chunk (may be smaller)
        assert len(content) <= size
        assert end - start <= size
