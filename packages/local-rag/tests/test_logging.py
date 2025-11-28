"""
Test logging functionality in local RAG.
"""
import tempfile
from pathlib import Path
import pytest

from local_rag.services.index_service import DocumentIndexer from local_rag.settings import get_settings


def test_logging_initialization(tmp_path):
    """Verify logger is initialized with correct paths."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    
    indexer = DocumentIndexer(user_data_dir=str(tmp_path))
    
    # Check that logger is initialized
    assert indexer.logger is not None
    
    # Check that log directory is created
    log_dir = tmp_path / "logs"
    assert log_dir.exists()


def test_file_size_checking(tmp_path):
    """Verify files are skipped if they exceed max_file_size_mb."""
    # Create a large file (> default 100MB would be impractical in tests)
    # So we'll use small threshold for testing
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    
    large_file = test_dir / "large.txt"
    # Create a 2MB file
    large_file.write_text("x" * (2 * 1024 * 1024))
    
    # Create indexer with max_file_size_mb=1
    settings = get_settings(user_data_dir=str(tmp_path), max_file_size_mb=1)
    indexer = DocumentIndexer(settings=settings)
    
    # Index should skip the large file
    stats = indexer.index_directory(test_dir)
    
    # File should be in skipped_large
    assert len(stats["skipped_large"]) == 1
    assert "large.txt" in stats["skipped_large"][0]["path"]
    assert stats["files_processed"] == 0


def test_error_tracking(tmp_path):
    """Verify errors are tracked with details."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    
    # Create an unreadable file (permission denied) 
    # This is tricky to test cross-platform, so we'll skip for now
    # and verify the structure of error_details exists
    
    indexer = DocumentIndexer(user_data_dir=str(tmp_path))
    stats = indexer.index_directory(test_dir)
    
    # Verify error tracking structure exists
    assert "error_details" in stats
    assert "skipped_large" in stats  
    assert "skipped_unchanged" in stats
    assert isinstance(stats["error_details"], list)


def test_summary_stats(tmp_path):
    """Verify summary stats are comprehensive."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    
    # Create a small test file
    (test_dir / "test.txt").write_text("hello world")
    
    indexer = DocumentIndexer(user_data_dir=str(tmp_path))
    stats = indexer.index_directory(test_dir)
    
    # Verify all expected keys exist
    expected_keys = [
        "files_processed",
        "files_skipped", 
        "chunks_created",
        "chunks_filtered",
        "errors",
        "error_details",
        "skipped_large",
        "skipped_unchanged"
    ]
    
    for key in expected_keys:
        assert key in stats, f"Missing key: {key}"
