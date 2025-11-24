"""Tests for ingest/extractor.py module."""

import pytest
from pathlib import Path


def test_extractor_module_imports():
    """Test that extractor module can be imported."""
    from ingest import extractor
    assert hasattr(extractor, 'read_text_with_ocr')


def test_read_text_file(tmp_path):
    """Test reading a simple text file."""
    from ingest.extractor import read_text_with_ocr

    # Create test file
    test_file = tmp_path / "test.txt"
    content = "This is a test file.\nWith multiple lines."
    test_file.write_text(content)

    # Read and verify
    result = read_text_with_ocr(test_file)
    assert result == content


def test_read_markdown_file(tmp_path):
    """Test reading a markdown file."""
    from ingest.extractor import read_text_with_ocr

    test_file = tmp_path / "test.md"
    content = "# Header\n\nParagraph text."
    test_file.write_text(content)

    result = read_text_with_ocr(test_file)
    assert result == content


def test_read_nonexistent_file(tmp_path):
    """Test reading a file that doesn't exist."""
    from ingest.extractor import read_text_with_ocr

    nonexistent = tmp_path / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        read_text_with_ocr(nonexistent)


def test_read_empty_file(tmp_path):
    """Test reading an empty file."""
    from ingest.extractor import read_text_with_ocr

    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    result = read_text_with_ocr(empty_file)
    assert result == ""


def test_read_unicode_content(tmp_path):
    """Test reading files with unicode content."""
    from ingest.extractor import read_text_with_ocr

    test_file = tmp_path / "unicode.txt"
    content = "Hello 世界! Привет мир! مرحبا بالعالم"
    test_file.write_text(content, encoding='utf-8')

    result = read_text_with_ocr(test_file)
    assert result == content


def test_read_large_file(tmp_path):
    """Test reading a large file."""
    from ingest.extractor import read_text_with_ocr

    test_file = tmp_path / "large.txt"
    content = "Line of text\n" * 10000  # 10k lines
    test_file.write_text(content)

    result = read_text_with_ocr(test_file)
    assert len(result) > 0
    assert "Line of text" in result


@pytest.mark.parametrize("extension", [".txt", ".md", ".log"])
def test_read_various_extensions(tmp_path, extension):
    """Test reading files with various text extensions."""
    from ingest.extractor import read_text_with_ocr

    test_file = tmp_path / f"test{extension}"
    content = "Test content"
    test_file.write_text(content)

    result = read_text_with_ocr(test_file)
    assert result == content
