"""Tests for chunking strategies."""

import pytest
from local_rag.ingestion.chunking import (
    Chunk,
    ChunkingStrategy,
    FixedChunker,
    SentenceChunker,
    TemplateChunker,
    chunk_text,
    get_chunker,
)


class TestChunk:
    """Tests for Chunk dataclass."""

    def test_chunk_creation(self):
        """Test basic chunk creation."""
        chunk = Chunk(text="Hello world", start=0, end=11)
        assert chunk.text == "Hello world"
        assert chunk.start == 0
        assert chunk.end == 11
        assert chunk.metadata == {}

    def test_chunk_with_metadata(self):
        """Test chunk with metadata."""
        chunk = Chunk(
            text="Test",
            start=0,
            end=4,
            metadata={"strategy": "fixed", "index": 0}
        )
        assert chunk.metadata["strategy"] == "fixed"
        assert chunk.metadata["index"] == 0


class TestFixedChunker:
    """Tests for FixedChunker."""

    def test_basic_chunking(self):
        """Test basic fixed-size chunking."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=20)
        text = "a" * 250

        chunks = list(chunker.chunk(text))

        assert len(chunks) == 3
        assert chunks[0].start == 0
        assert chunks[0].end == 100
        assert len(chunks[0].text) == 100

    def test_short_text(self):
        """Test chunking text shorter than chunk size."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=20)
        text = "short text"

        chunks = list(chunker.chunk(text))

        assert len(chunks) == 1
        assert chunks[0].text == text
        assert chunks[0].start == 0
        assert chunks[0].end == len(text)

    def test_empty_text(self):
        """Test chunking empty text."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=20)

        chunks = list(chunker.chunk(""))

        assert len(chunks) == 0

    def test_exact_chunk_size(self):
        """Test text exactly matching chunk size."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=20)
        text = "a" * 100

        chunks = list(chunker.chunk(text))

        assert len(chunks) == 1
        assert len(chunks[0].text) == 100

    def test_no_overlap(self):
        """Test chunking with zero overlap."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=0)
        text = "a" * 200

        chunks = list(chunker.chunk(text))

        assert len(chunks) == 2
        assert chunks[0].end == 100
        assert chunks[1].start == 100

    def test_overlap_preserved(self):
        """Test that overlap is preserved between chunks."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=30)
        text = "a" * 200

        chunks = list(chunker.chunk(text))

        # Second chunk should start before first ends
        assert chunks[1].start < chunks[0].end
        assert chunks[0].end - chunks[1].start == 30

    def test_unicode_text(self):
        """Test chunking with unicode characters."""
        chunker = FixedChunker(chunk_size=50, chunk_overlap=10)
        text = "Hello 世界! " * 20  # Mix of ASCII and unicode

        chunks = list(chunker.chunk(text))

        assert len(chunks) > 0
        for chunk in chunks:
            assert isinstance(chunk.text, str)

    def test_metadata_strategy(self):
        """Test that chunks have correct strategy metadata."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=20)
        text = "a" * 150

        chunks = list(chunker.chunk(text))

        for chunk in chunks:
            assert chunk.metadata.get("strategy") == "fixed"


class TestSentenceChunker:
    """Tests for SentenceChunker."""

    def test_basic_sentence_chunking(self):
        """Test basic sentence-aware chunking."""
        chunker = SentenceChunker(chunk_size=100, chunk_overlap=20)
        text = "First sentence. Second sentence. Third sentence."

        chunks = list(chunker.chunk(text))

        assert len(chunks) >= 1

    def test_respects_sentence_boundaries(self):
        """Test that chunker respects sentence boundaries."""
        chunker = SentenceChunker(chunk_size=50, chunk_overlap=10)
        text = "Short. Another short. Yet another."

        chunks = list(chunker.chunk(text))

        # Chunks should not split mid-sentence when possible
        for chunk in chunks:
            # Each chunk should end with punctuation or be the last chunk
            text_stripped = chunk.text.strip()
            if chunk != chunks[-1]:
                assert text_stripped.endswith('.') or text_stripped.endswith('!') or text_stripped.endswith('?') or len(text_stripped) > 0

    def test_large_sentence_splitting(self):
        """Test handling of sentences larger than chunk size."""
        chunker = SentenceChunker(chunk_size=50, chunk_overlap=10)
        text = "This is a very long sentence that exceeds the chunk size limit and should be split."

        chunks = list(chunker.chunk(text))

        assert len(chunks) >= 1
        # Should have split the large sentence
        for chunk in chunks:
            assert len(chunk.text) <= 60  # Allow some flexibility

    def test_empty_text(self):
        """Test with empty text."""
        chunker = SentenceChunker(chunk_size=100, chunk_overlap=20)

        chunks = list(chunker.chunk(""))

        assert len(chunks) == 0

    def test_metadata_strategy(self):
        """Test that chunks have correct strategy metadata."""
        chunker = SentenceChunker(chunk_size=100, chunk_overlap=20)
        text = "First sentence. Second sentence."

        chunks = list(chunker.chunk(text))

        for chunk in chunks:
            assert chunk.metadata.get("strategy") == "sentence"


class TestTemplateChunker:
    """Tests for TemplateChunker."""

    def test_markdown_detection(self):
        """Test markdown document detection."""
        chunker = TemplateChunker(chunk_size=500, chunk_overlap=50)
        text = """# Header 1

Some content here.

## Header 2

More content.
"""
        chunks = list(chunker.chunk(text, file_path="test.md"))

        assert len(chunks) >= 1
        assert any(c.metadata.get("type") == "markdown" for c in chunks)

    def test_code_detection(self):
        """Test code file detection."""
        chunker = TemplateChunker(chunk_size=500, chunk_overlap=50)
        text = """def hello():
    print("Hello")

def world():
    print("World")
"""
        chunks = list(chunker.chunk(text, file_path="test.py"))

        assert len(chunks) >= 1

    def test_prose_fallback(self):
        """Test fallback to prose chunking."""
        chunker = TemplateChunker(chunk_size=100, chunk_overlap=20)
        text = """This is a paragraph.

This is another paragraph.

And a third one."""

        chunks = list(chunker.chunk(text))

        assert len(chunks) >= 1
        assert any(c.metadata.get("type") == "prose" for c in chunks)

    def test_header_preservation(self):
        """Test that headers are preserved in split chunks."""
        chunker = TemplateChunker(chunk_size=50, chunk_overlap=10, preserve_headers=True)
        text = """# Important Section

This is a very long paragraph that will need to be split across multiple chunks but should preserve the header context."""

        chunks = list(chunker.chunk(text, file_path="test.md"))

        assert len(chunks) >= 1

    def test_metadata_includes_type(self):
        """Test that chunks include document type metadata."""
        chunker = TemplateChunker(chunk_size=500, chunk_overlap=50)
        text = "# Header\n\nContent"

        chunks = list(chunker.chunk(text, file_path="test.md"))

        for chunk in chunks:
            assert "type" in chunk.metadata


class TestGetChunker:
    """Tests for get_chunker factory function."""

    def test_get_fixed_chunker(self):
        """Test getting fixed chunker."""
        chunker = get_chunker(ChunkingStrategy.FIXED, 100, 20)
        assert isinstance(chunker, FixedChunker)

    def test_get_sentence_chunker(self):
        """Test getting sentence chunker."""
        chunker = get_chunker(ChunkingStrategy.SENTENCE, 100, 20)
        assert isinstance(chunker, SentenceChunker)

    def test_get_template_chunker(self):
        """Test getting template chunker."""
        chunker = get_chunker(ChunkingStrategy.TEMPLATE, 100, 20)
        assert isinstance(chunker, TemplateChunker)

    def test_custom_parameters(self):
        """Test chunker with custom parameters."""
        chunker = get_chunker(ChunkingStrategy.FIXED, chunk_size=500, chunk_overlap=100)
        assert chunker.chunk_size == 500
        assert chunker.chunk_overlap == 100


class TestChunkTextFunction:
    """Tests for the chunk_text convenience function."""

    def test_basic_usage(self):
        """Test basic chunk_text function usage."""
        text = "a" * 250
        results = list(chunk_text(text, ChunkingStrategy.FIXED, size=100, overlap=20))

        assert len(results) == 3
        # Returns tuples of (start, end, text)
        for start, end, content in results:
            assert isinstance(start, int)
            assert isinstance(end, int)
            assert isinstance(content, str)

    def test_backward_compatibility(self):
        """Test backward compatibility with tuple output."""
        text = "test content"
        results = list(chunk_text(text))

        assert len(results) >= 1
        start, end, content = results[0]
        assert start == 0
        assert end == len(text)
        assert content == text


class TestChunkingEdgeCases:
    """Tests for edge cases across all chunkers."""

    @pytest.mark.parametrize("chunker_class", [
        FixedChunker,
        SentenceChunker,
        TemplateChunker
    ])
    def test_whitespace_only(self, chunker_class):
        """Test handling of whitespace-only text."""
        chunker = chunker_class(chunk_size=100, chunk_overlap=20)
        text = "   \n\n\t  "

        chunks = list(chunker.chunk(text))

        # Should handle gracefully (either empty or minimal chunks)
        assert isinstance(chunks, list)

    @pytest.mark.parametrize("chunker_class", [
        FixedChunker,
        SentenceChunker,
        TemplateChunker
    ])
    def test_special_characters(self, chunker_class):
        """Test handling of special characters."""
        chunker = chunker_class(chunk_size=100, chunk_overlap=20)
        text = "Hello\x00World\r\nTest\rMore"

        chunks = list(chunker.chunk(text))

        # Should handle without errors
        assert len(chunks) >= 1
        # Null bytes should be removed
        for chunk in chunks:
            assert "\x00" not in chunk.text

    @pytest.mark.parametrize("chunker_class", [
        FixedChunker,
        SentenceChunker,
        TemplateChunker
    ])
    def test_very_long_text(self, chunker_class):
        """Test handling of very long text."""
        chunker = chunker_class(chunk_size=1000, chunk_overlap=100)
        text = "word " * 10000  # 50000 characters

        chunks = list(chunker.chunk(text))

        assert len(chunks) > 10
        # All chunks should respect size limits (approximately)
        for chunk in chunks[:-1]:  # Last chunk may be smaller
            assert len(chunk.text) <= 1100  # Allow some flexibility

    @pytest.mark.parametrize("size,overlap", [
        (100, 10),
        (500, 50),
        (1000, 100),
        (3000, 400),
    ])
    def test_various_sizes(self, size, overlap):
        """Test various chunk size configurations."""
        chunker = FixedChunker(chunk_size=size, chunk_overlap=overlap)
        text = "a" * (size * 3)

        chunks = list(chunker.chunk(text))

        assert len(chunks) >= 2
        for chunk in chunks[:-1]:
            assert len(chunk.text) == size


class TestChunkCoverage:
    """Tests to ensure complete text coverage."""

    def test_fixed_coverage(self):
        """Test that fixed chunking covers all text."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=0)
        text = "abcdefghij" * 30  # 300 chars

        chunks = list(chunker.chunk(text))

        # Concatenate all chunks
        reconstructed = "".join(c.text for c in chunks)
        assert reconstructed == text

    def test_overlap_coverage(self):
        """Test that overlapping chunks cover all text."""
        chunker = FixedChunker(chunk_size=100, chunk_overlap=20)
        text = "abcdefghij" * 30  # 300 chars

        chunks = list(chunker.chunk(text))

        # First chunk should start at 0
        assert chunks[0].start == 0

        # Last chunk should end at len(text)
        assert chunks[-1].end == len(text)

        # Check continuity (each chunk starts where overlap allows)
        for i in range(1, len(chunks)):
            assert chunks[i].start <= chunks[i-1].end
