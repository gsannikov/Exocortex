"""Pytest configuration and fixtures for 2ndBrain_RAG tests."""

import os
import tempfile
from pathlib import Path
import pytest


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
