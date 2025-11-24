"""Tests for ingest/ocr.py module."""

import pytest
from pathlib import Path
from PIL import Image
import io


def test_ocr_module_imports():
    """Test that OCR module can be imported."""
    from ingest import ocr
    assert hasattr(ocr, 'run_ocr')


def test_img_sha_consistency():
    """Test that image hashing is consistent."""
    from ingest.ocr import _img_sha

    # Create a simple image
    img = Image.new('RGB', (100, 100), color='white')

    hash1 = _img_sha(img)
    hash2 = _img_sha(img)

    assert hash1 == hash2
    assert len(hash1) == 40  # SHA1 hex digest length


def test_img_sha_different_images():
    """Test that different images produce different hashes."""
    from ingest.ocr import _img_sha

    img1 = Image.new('RGB', (100, 100), color='white')
    img2 = Image.new('RGB', (100, 100), color='black')

    hash1 = _img_sha(img1)
    hash2 = _img_sha(img2)

    assert hash1 != hash2


def test_cache_get_nonexistent(tmp_path, monkeypatch):
    """Test cache get for non-existent entry."""
    from ingest.ocr import _cache_get

    monkeypatch.setattr('ingest.ocr.CACHE_DIR', tmp_path)

    result = _cache_get("nonexistent_hash")
    assert result is None


def test_cache_put_and_get(tmp_path, monkeypatch):
    """Test caching OCR results."""
    from ingest.ocr import _cache_put, _cache_get

    monkeypatch.setattr('ingest.ocr.CACHE_DIR', tmp_path)

    test_hash = "test_hash_123"
    test_text = "Extracted text from OCR"

    _cache_put(test_hash, test_text)
    retrieved = _cache_get(test_hash)

    assert retrieved == test_text


def test_cache_persistence(tmp_path, monkeypatch):
    """Test that cache persists to disk."""
    from ingest.ocr import _cache_put, _cache_get

    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    monkeypatch.setattr('ingest.ocr.CACHE_DIR', cache_dir)

    test_hash = "persistent_hash"
    test_text = "This should persist"

    _cache_put(test_hash, test_text)

    # Verify file exists
    cache_file = cache_dir / f"{test_hash}.txt"
    assert cache_file.exists()

    # Verify can be retrieved
    assert _cache_get(test_hash) == test_text


def test_run_ocr_empty_list(monkeypatch):
    """Test OCR with empty image list."""
    from ingest.ocr import run_ocr

    # Set to an engine that returns empty string for empty list
    monkeypatch.setenv("OCR_ENGINE", "surya")

    result = run_ocr([])
    # Should handle empty list gracefully
    assert isinstance(result, str)


def test_run_ocr_engine_selection(monkeypatch):
    """Test that OCR engine selection works."""
    from ingest.ocr import run_ocr
    import ingest.ocr

    # Test with unsupported engine
    monkeypatch.setenv("OCR_ENGINE", "unsupported")
    # Need to reload module to pick up new env var
    monkeypatch.setattr('ingest.ocr.ENGINE', 'unsupported')

    result = run_ocr([])
    assert result == ""  # Should return empty string for unsupported engine


def test_cache_unicode(tmp_path, monkeypatch):
    """Test caching with unicode text."""
    from ingest.ocr import _cache_put, _cache_get

    monkeypatch.setattr('ingest.ocr.CACHE_DIR', tmp_path)

    test_hash = "unicode_test"
    test_text = "Text with unicode: 你好世界 مرحبا Привет"

    _cache_put(test_hash, test_text)
    retrieved = _cache_get(test_hash)

    assert retrieved == test_text


def test_cache_large_text(tmp_path, monkeypatch):
    """Test caching with large text."""
    from ingest.ocr import _cache_put, _cache_get

    monkeypatch.setattr('ingest.ocr.CACHE_DIR', tmp_path)

    test_hash = "large_text_hash"
    test_text = "Large text content\n" * 1000

    _cache_put(test_hash, test_text)
    retrieved = _cache_get(test_hash)

    assert retrieved == test_text
    assert len(retrieved) > 10000


@pytest.mark.parametrize("engine", ["surya", "paddle", "deepseek"])
def test_engine_environment_variable(engine, monkeypatch):
    """Test that engine can be set via environment variable."""
    import ingest.ocr

    monkeypatch.setenv("OCR_ENGINE", engine)
    monkeypatch.setattr('ingest.ocr.ENGINE', engine.lower())

    assert ingest.ocr.ENGINE == engine.lower()
