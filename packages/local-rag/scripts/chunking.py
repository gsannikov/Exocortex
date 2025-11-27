#!/usr/bin/env python3
"""
Chunking strategies for Local RAG.

Provides multiple chunking approaches:
- Fixed: Simple character-based chunking with overlap
- Sentence: Respects sentence boundaries
- Semantic: Groups related content using embeddings
- Template: Document-type aware chunking (markdown, code, etc.)
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generator, List, Optional, Tuple
from pathlib import Path


class ChunkingStrategy(str, Enum):
    """Available chunking strategies."""
    FIXED = "fixed"
    SENTENCE = "sentence"
    SEMANTIC = "semantic"
    TEMPLATE = "template"


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""
    text: str
    start: int
    end: int
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseChunker(ABC):
    """Abstract base class for chunking strategies."""

    def __init__(self, chunk_size: int = 3000, chunk_overlap: int = 400):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def chunk(self, text: str, **kwargs) -> Generator[Chunk, None, None]:
        """Split text into chunks."""
        pass

    def _sanitize_text(self, text: str) -> str:
        """Clean text before chunking."""
        # Normalize whitespace but preserve structure
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        # Remove null bytes
        text = text.replace('\x00', '')
        return text


class FixedChunker(BaseChunker):
    """Simple fixed-size character chunking with overlap."""

    def chunk(self, text: str, **kwargs) -> Generator[Chunk, None, None]:
        text = self._sanitize_text(text)
        n = len(text)
        if n == 0:
            return

        i = 0
        while i < n:
            j = min(n, i + self.chunk_size)
            yield Chunk(
                text=text[i:j],
                start=i,
                end=j,
                metadata={"strategy": "fixed"}
            )
            if j == n:
                break
            i = j - self.chunk_overlap


class SentenceChunker(BaseChunker):
    """Sentence-aware chunking that respects sentence boundaries."""

    # Sentence-ending patterns
    SENTENCE_ENDINGS = re.compile(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])\n+')

    def chunk(self, text: str, **kwargs) -> Generator[Chunk, None, None]:
        text = self._sanitize_text(text)
        if not text.strip():
            return

        # Split into sentences
        sentences = self._split_sentences(text)

        current_chunk = []
        current_length = 0
        chunk_start = 0

        for sentence, sent_start, sent_end in sentences:
            sent_length = len(sentence)

            # If single sentence exceeds chunk size, split it
            if sent_length > self.chunk_size:
                # Yield current chunk first
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    yield Chunk(
                        text=chunk_text,
                        start=chunk_start,
                        end=sent_start,
                        metadata={"strategy": "sentence"}
                    )
                    current_chunk = []
                    current_length = 0

                # Split large sentence using fixed chunking
                for sub_chunk in self._split_large_sentence(sentence, sent_start):
                    yield sub_chunk
                chunk_start = sent_end
                continue

            # Check if adding this sentence exceeds limit
            if current_length + sent_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                yield Chunk(
                    text=chunk_text,
                    start=chunk_start,
                    end=sent_start,
                    metadata={"strategy": "sentence"}
                )

                # Start new chunk with overlap (include last sentence(s) up to overlap size)
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) > self.chunk_overlap:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_length += len(s)

                current_chunk = overlap_sentences
                current_length = overlap_length
                chunk_start = sent_start - overlap_length

            current_chunk.append(sentence)
            current_length += sent_length

        # Yield remaining
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            yield Chunk(
                text=chunk_text,
                start=chunk_start,
                end=len(text),
                metadata={"strategy": "sentence"}
            )

    def _split_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """Split text into sentences with positions."""
        sentences = []
        last_end = 0

        for match in self.SENTENCE_ENDINGS.finditer(text):
            sent_end = match.start()
            sentence = text[last_end:sent_end + 1].strip()
            if sentence:
                sentences.append((sentence, last_end, sent_end + 1))
            last_end = match.end()

        # Add remaining text
        remaining = text[last_end:].strip()
        if remaining:
            sentences.append((remaining, last_end, len(text)))

        # If no sentences found, return whole text
        if not sentences:
            sentences.append((text.strip(), 0, len(text)))

        return sentences

    def _split_large_sentence(self, sentence: str, offset: int) -> Generator[Chunk, None, None]:
        """Split a large sentence using fixed chunking."""
        fixed = FixedChunker(self.chunk_size, self.chunk_overlap)
        for chunk in fixed.chunk(sentence):
            yield Chunk(
                text=chunk.text,
                start=offset + chunk.start,
                end=offset + chunk.end,
                metadata={"strategy": "sentence", "split_large": True}
            )


class SemanticChunker(BaseChunker):
    """
    Semantic chunking that groups related content.
    Uses embedding similarity to find natural breakpoints.
    """

    def __init__(
        self,
        chunk_size: int = 3000,
        chunk_overlap: int = 400,
        similarity_threshold: float = 0.5,
        embed_model = None
    ):
        super().__init__(chunk_size, chunk_overlap)
        self.similarity_threshold = similarity_threshold
        self._embed_model = embed_model

    @property
    def embed_model(self):
        """Lazy load embedding model."""
        if self._embed_model is None:
            from sentence_transformers import SentenceTransformer
            self._embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return self._embed_model

    def chunk(self, text: str, **kwargs) -> Generator[Chunk, None, None]:
        text = self._sanitize_text(text)
        if not text.strip():
            return

        # First split into sentences
        sentence_chunker = SentenceChunker(chunk_size=500, chunk_overlap=0)
        sentences = list(sentence_chunker.chunk(text))

        if len(sentences) <= 1:
            # Single sentence or empty - use fixed chunking
            yield from FixedChunker(self.chunk_size, self.chunk_overlap).chunk(text)
            return

        # Get embeddings for all sentences
        sentence_texts = [s.text for s in sentences]
        embeddings = self.embed_model.encode(sentence_texts, normalize_embeddings=True)

        # Find breakpoints based on similarity drops
        breakpoints = self._find_breakpoints(embeddings)

        # Group sentences into chunks
        current_group = []
        current_start = sentences[0].start
        current_length = 0

        for i, sentence in enumerate(sentences):
            is_breakpoint = i in breakpoints
            would_exceed = current_length + len(sentence.text) > self.chunk_size

            if (is_breakpoint or would_exceed) and current_group:
                chunk_text = ' '.join([s.text for s in current_group])
                yield Chunk(
                    text=chunk_text,
                    start=current_start,
                    end=sentence.start,
                    metadata={
                        "strategy": "semantic",
                        "sentence_count": len(current_group)
                    }
                )
                current_group = []
                current_start = sentence.start
                current_length = 0

            current_group.append(sentence)
            current_length += len(sentence.text)

        # Yield remaining
        if current_group:
            chunk_text = ' '.join([s.text for s in current_group])
            yield Chunk(
                text=chunk_text,
                start=current_start,
                end=sentences[-1].end,
                metadata={
                    "strategy": "semantic",
                    "sentence_count": len(current_group)
                }
            )

    def _find_breakpoints(self, embeddings) -> set:
        """Find indices where semantic similarity drops significantly."""
        import numpy as np

        breakpoints = set()

        if len(embeddings) < 2:
            return breakpoints

        # Calculate cosine similarities between consecutive sentences
        similarities = []
        for i in range(len(embeddings) - 1):
            sim = np.dot(embeddings[i], embeddings[i + 1])
            similarities.append(sim)

        if not similarities:
            return breakpoints

        # Find significant drops (below threshold or below mean - std)
        mean_sim = np.mean(similarities)
        std_sim = np.std(similarities)
        threshold = max(self.similarity_threshold, mean_sim - std_sim)

        for i, sim in enumerate(similarities):
            if sim < threshold:
                breakpoints.add(i + 1)  # Breakpoint is after the low-similarity pair

        return breakpoints


class TemplateChunker(BaseChunker):
    """
    Template-based chunking that understands document structure.
    Recognizes markdown headers, code blocks, paragraphs, etc.
    """

    # Patterns for different document elements
    PATTERNS = {
        'markdown_header': re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE),
        'code_block': re.compile(r'```[\s\S]*?```', re.MULTILINE),
        'paragraph': re.compile(r'\n\n+'),
        'list_item': re.compile(r'^[\s]*[-*+]\s+', re.MULTILINE),
        'numbered_list': re.compile(r'^[\s]*\d+[.)]\s+', re.MULTILINE),
    }

    def __init__(
        self,
        chunk_size: int = 3000,
        chunk_overlap: int = 400,
        preserve_headers: bool = True
    ):
        super().__init__(chunk_size, chunk_overlap)
        self.preserve_headers = preserve_headers

    def chunk(self, text: str, file_path: Optional[str] = None, **kwargs) -> Generator[Chunk, None, None]:
        text = self._sanitize_text(text)
        if not text.strip():
            return

        # Detect document type
        doc_type = self._detect_document_type(text, file_path)

        # Use appropriate chunking based on document type
        if doc_type == 'markdown':
            yield from self._chunk_markdown(text)
        elif doc_type == 'code':
            yield from self._chunk_code(text, file_path)
        else:
            yield from self._chunk_prose(text)

    def _detect_document_type(self, text: str, file_path: Optional[str]) -> str:
        """Detect document type from content and extension."""
        if file_path:
            ext = Path(file_path).suffix.lower()
            if ext in {'.md', '.markdown'}:
                return 'markdown'
            if ext in {'.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.go', '.rs'}:
                return 'code'

        # Content-based detection
        header_count = len(self.PATTERNS['markdown_header'].findall(text))
        code_block_count = len(self.PATTERNS['code_block'].findall(text))

        if header_count >= 2:
            return 'markdown'
        if code_block_count >= 1:
            return 'markdown'

        return 'prose'

    def _chunk_markdown(self, text: str) -> Generator[Chunk, None, None]:
        """Chunk markdown respecting header hierarchy."""
        # Find all headers with positions
        headers = []
        for match in self.PATTERNS['markdown_header'].finditer(text):
            level = len(match.group(1))
            title = match.group(2)
            headers.append({
                'level': level,
                'title': title,
                'start': match.start(),
                'end': match.end()
            })

        if not headers:
            # No headers - use prose chunking
            yield from self._chunk_prose(text)
            return

        # Create sections based on headers
        sections = []
        for i, header in enumerate(headers):
            start = header['start']
            end = headers[i + 1]['start'] if i + 1 < len(headers) else len(text)
            section_text = text[start:end].strip()

            sections.append({
                'text': section_text,
                'start': start,
                'end': end,
                'header': header['title'],
                'level': header['level']
            })

        # Add any text before first header
        if headers[0]['start'] > 0:
            preamble = text[:headers[0]['start']].strip()
            if preamble:
                sections.insert(0, {
                    'text': preamble,
                    'start': 0,
                    'end': headers[0]['start'],
                    'header': None,
                    'level': 0
                })

        # Merge small sections, split large ones
        current_chunk = []
        current_length = 0
        current_start = 0
        parent_header = None

        for section in sections:
            section_text = section['text']
            section_length = len(section_text)

            # Track parent header for context
            if section['level'] and (parent_header is None or section['level'] <= parent_header['level']):
                parent_header = section

            # If section alone exceeds chunk size, split it
            if section_length > self.chunk_size:
                # Yield current accumulated chunk
                if current_chunk:
                    yield Chunk(
                        text='\n\n'.join(current_chunk),
                        start=current_start,
                        end=section['start'],
                        metadata={
                            "strategy": "template",
                            "type": "markdown",
                            "header": parent_header['title'] if parent_header else None
                        }
                    )
                    current_chunk = []
                    current_length = 0

                # Split large section
                for sub_chunk in self._split_section(section, parent_header):
                    yield sub_chunk

                current_start = section['end']
                continue

            # Check if adding this section exceeds limit
            if current_length + section_length > self.chunk_size and current_chunk:
                yield Chunk(
                    text='\n\n'.join(current_chunk),
                    start=current_start,
                    end=section['start'],
                    metadata={
                        "strategy": "template",
                        "type": "markdown",
                        "header": parent_header.get('title') if parent_header else None
                    }
                )
                current_chunk = []
                current_length = 0
                current_start = section['start']

            current_chunk.append(section_text)
            current_length += section_length

        # Yield remaining
        if current_chunk:
            yield Chunk(
                text='\n\n'.join(current_chunk),
                start=current_start,
                end=len(text),
                metadata={
                    "strategy": "template",
                    "type": "markdown",
                    "header": parent_header.get('title') if parent_header else None
                }
            )

    def _chunk_code(self, text: str, file_path: Optional[str]) -> Generator[Chunk, None, None]:
        """Chunk code respecting function/class boundaries."""
        # Simple approach: split on blank lines and class/function definitions
        code_patterns = {
            'python': re.compile(r'^(class\s+\w+|def\s+\w+|async\s+def\s+\w+)', re.MULTILINE),
            'javascript': re.compile(r'^(class\s+\w+|function\s+\w+|const\s+\w+\s*=|export\s+)', re.MULTILINE),
        }

        ext = Path(file_path).suffix.lower() if file_path else ''

        if ext == '.py':
            pattern = code_patterns['python']
        elif ext in {'.js', '.ts'}:
            pattern = code_patterns['javascript']
        else:
            # Default to blank line splitting
            yield from self._chunk_prose(text)
            return

        # Find definition boundaries
        matches = list(pattern.finditer(text))

        if not matches:
            yield from self._chunk_prose(text)
            return

        # Create chunks at definition boundaries
        current_chunk = []
        current_start = 0
        current_length = 0

        # Add preamble (imports, etc.)
        if matches[0].start() > 0:
            preamble = text[:matches[0].start()].strip()
            if preamble:
                current_chunk.append(preamble)
                current_length = len(preamble)

        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[start:end].strip()
            block_length = len(block)

            if block_length > self.chunk_size:
                # Yield accumulated, then split large block
                if current_chunk:
                    yield Chunk(
                        text='\n\n'.join(current_chunk),
                        start=current_start,
                        end=start,
                        metadata={"strategy": "template", "type": "code"}
                    )
                    current_chunk = []
                    current_length = 0

                # Split large block
                for sub in FixedChunker(self.chunk_size, self.chunk_overlap).chunk(block):
                    yield Chunk(
                        text=sub.text,
                        start=start + sub.start,
                        end=start + sub.end,
                        metadata={"strategy": "template", "type": "code", "split": True}
                    )
                current_start = end
                continue

            if current_length + block_length > self.chunk_size and current_chunk:
                yield Chunk(
                    text='\n\n'.join(current_chunk),
                    start=current_start,
                    end=start,
                    metadata={"strategy": "template", "type": "code"}
                )
                current_chunk = []
                current_length = 0
                current_start = start

            current_chunk.append(block)
            current_length += block_length

        if current_chunk:
            yield Chunk(
                text='\n\n'.join(current_chunk),
                start=current_start,
                end=len(text),
                metadata={"strategy": "template", "type": "code"}
            )

    def _chunk_prose(self, text: str) -> Generator[Chunk, None, None]:
        """Chunk prose by paragraphs."""
        paragraphs = self.PATTERNS['paragraph'].split(text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        if not paragraphs:
            return

        current_chunk = []
        current_length = 0
        current_start = 0

        text_pos = 0
        for para in paragraphs:
            para_start = text.find(para, text_pos)
            para_end = para_start + len(para)
            para_length = len(para)
            text_pos = para_end

            if para_length > self.chunk_size:
                if current_chunk:
                    yield Chunk(
                        text='\n\n'.join(current_chunk),
                        start=current_start,
                        end=para_start,
                        metadata={"strategy": "template", "type": "prose"}
                    )
                    current_chunk = []
                    current_length = 0

                for sub in FixedChunker(self.chunk_size, self.chunk_overlap).chunk(para):
                    yield Chunk(
                        text=sub.text,
                        start=para_start + sub.start,
                        end=para_start + sub.end,
                        metadata={"strategy": "template", "type": "prose", "split": True}
                    )
                current_start = para_end
                continue

            if current_length + para_length > self.chunk_size and current_chunk:
                yield Chunk(
                    text='\n\n'.join(current_chunk),
                    start=current_start,
                    end=para_start,
                    metadata={"strategy": "template", "type": "prose"}
                )
                current_chunk = []
                current_length = 0
                current_start = para_start

            current_chunk.append(para)
            current_length += para_length

        if current_chunk:
            yield Chunk(
                text='\n\n'.join(current_chunk),
                start=current_start,
                end=len(text),
                metadata={"strategy": "template", "type": "prose"}
            )

    def _split_section(self, section: dict, parent_header: Optional[dict]) -> Generator[Chunk, None, None]:
        """Split a large section while preserving header context."""
        text = section['text']
        header_prefix = ""

        if self.preserve_headers and section.get('header'):
            header_prefix = f"# {section['header']}\n\n"

        effective_size = self.chunk_size - len(header_prefix)

        for sub in FixedChunker(effective_size, self.chunk_overlap).chunk(text):
            yield Chunk(
                text=header_prefix + sub.text if header_prefix else sub.text,
                start=section['start'] + sub.start,
                end=section['start'] + sub.end,
                metadata={
                    "strategy": "template",
                    "type": "markdown",
                    "header": section.get('header'),
                    "split": True
                }
            )


def get_chunker(
    strategy: ChunkingStrategy = ChunkingStrategy.TEMPLATE,
    chunk_size: int = 3000,
    chunk_overlap: int = 400,
    **kwargs
) -> BaseChunker:
    """Factory function to get a chunker by strategy name."""
    chunkers = {
        ChunkingStrategy.FIXED: FixedChunker,
        ChunkingStrategy.SENTENCE: SentenceChunker,
        ChunkingStrategy.SEMANTIC: SemanticChunker,
        ChunkingStrategy.TEMPLATE: TemplateChunker,
    }

    chunker_class = chunkers.get(strategy, TemplateChunker)
    return chunker_class(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)


def chunk_text(
    text: str,
    strategy: ChunkingStrategy = ChunkingStrategy.FIXED,
    size: int = 3000,
    overlap: int = 400,
    **kwargs
) -> Generator[Tuple[int, int, str], None, None]:
    """
    Convenience function maintaining backward compatibility.
    Returns tuples of (start, end, text) like the original implementation.
    """
    chunker = get_chunker(strategy, size, overlap, **kwargs)
    for chunk in chunker.chunk(text, **kwargs):
        yield chunk.start, chunk.end, chunk.text
