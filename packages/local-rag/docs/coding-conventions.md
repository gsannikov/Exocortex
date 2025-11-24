# Coding Conventions

## Overview

This document defines the coding standards and conventions for the 2ndBrain_RAG project. Following these conventions ensures code consistency, readability, and maintainability.

---

## General Principles

1. **Clarity over Cleverness**: Write code that's easy to understand
2. **Explicit over Implicit**: Make intentions clear
3. **Simple over Complex**: Choose the simpler solution when possible
4. **Tested over Untested**: Verify behavior with tests
5. **Documented over Undocumented**: Explain the "why", not just the "what"

---

## Python Style Guide

### Base Standard

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some project-specific additions.

**Quick Reference**:
- Line length: 100 characters (relaxed from PEP 8's 79)
- Indentation: 4 spaces (no tabs)
- Encoding: UTF-8
- Quotes: Double quotes for strings, single for internal usage

### Formatting

**Use Black for auto-formatting** (when available):
```bash
black mcp_server.py ingest/
```

**Manual formatting**:
```python
# Good: Clear, readable
def chunk_text(text: str, size: int = 3000) -> list[tuple[int, int, str]]:
    """Split text into chunks."""
    results = []
    i = 0
    while i < len(text):
        chunk = text[i:i + size]
        results.append((i, i + len(chunk), chunk))
        i += size - overlap
    return results

# Bad: Compressed, hard to read
def chunk_text(text,size=3000):
    r=[];i=0
    while i<len(text):r.append((i,i+size,text[i:i+size]));i+=size-overlap
    return r
```

---

## Naming Conventions

### General Rules

| Element | Convention | Example |
|---------|-----------|---------|
| Variables | `snake_case` | `chunk_size`, `file_path` |
| Functions | `snake_case` | `read_text()`, `do_ingest()` |
| Classes | `PascalCase` | `FSHandler`, `EmbeddingModel` |
| Constants | `UPPER_SNAKE_CASE` | `CHUNK_SIZE`, `ROOT_DIR` |
| Private | `_leading_underscore` | `_ocr_surya()`, `_internal` |
| Modules | `snake_case` | `extractor.py`, `ocr.py` |

### Specific Guidelines

**File paths**: Use `path` or specific name (`pdf_path`, `doc_path`)
```python
# Good
def read_file(path: Path) -> str:
    return path.read_text()

# Bad
def read_file(f) -> str:  # Too vague
    return f.read_text()
```

**Collections**: Use plural names
```python
# Good
documents = []
file_paths = [...]

# Bad
document_list = []
file_path_array = [...]
```

**Booleans**: Use `is_`, `has_`, `can_` prefixes
```python
# Good
is_indexed = True
has_content = len(text) > 0
can_process = extension in ALLOWED

# Bad
indexed = True
content = len(text) > 0  # Ambiguous
processable = extension in ALLOWED
```

---

## Type Hints

### Required

Use type hints for **all public function signatures**:

```python
# Good
def chunk_text(text: str, size: int = 3000, overlap: int = 400) -> list[tuple[int, int, str]]:
    """Split text into overlapping chunks."""
    pass

# Bad
def chunk_text(text, size=3000, overlap=400):  # No type hints
    """Split text into overlapping chunks."""
    pass
```

### Complex Types

Use `typing` module for complex types:

```python
from typing import Optional, Union, Dict, Any
from pathlib import Path

def load_config(path: Path) -> Dict[str, Any]:
    """Load configuration from file."""
    pass

def find_file(query: str) -> Optional[Path]:
    """Search for file, return None if not found."""
    pass

def read_text(path: Union[str, Path]) -> str:
    """Read text from file path (string or Path object)."""
    pass
```

### Python 3.10+ Syntax

Prefer modern syntax where available:

```python
# Good (Python 3.10+)
def process(items: list[str]) -> dict[str, int]:
    pass

# Old style (still acceptable for compatibility)
from typing import List, Dict
def process(items: List[str]) -> Dict[str, int]:
    pass
```

---

## Documentation

### Docstrings

Use **Google-style docstrings** for all public functions and classes:

```python
def read_text_with_ocr(path: Path, dpi: int = 200) -> str:
    """Extract text from file, using OCR if needed.

    Attempts to extract text directly from the file. If that fails
    or returns empty content, falls back to OCR processing.

    Args:
        path: Path to the file to process
        dpi: DPI for OCR rendering (default: 200)

    Returns:
        Extracted text content as a single string

    Raises:
        FileNotFoundError: If path does not exist
        ValueError: If file format is unsupported

    Example:
        >>> text = read_text_with_ocr(Path("scan.pdf"))
        >>> print(text[:100])
        'This is a scanned document...'
    """
    pass
```

**Required sections**:
- Summary (first line)
- Detailed description (if needed)
- Args (for parameters)
- Returns (for return values)
- Raises (for exceptions)

**Optional sections**:
- Example (for complex usage)
- Note (for important details)
- Warning (for gotchas)

### Comments

**When to comment**:
- Complex algorithms or logic
- Non-obvious optimizations
- Workarounds for bugs or limitations
- TODOs and FIXMEs

**When NOT to comment**:
- Obvious code (don't repeat what code says)
- Outdated information (remove or update)

```python
# Good: Explains WHY
# Use hash instead of mtime because some editors don't update it
file_hash = fhash(path)

# Bad: Explains WHAT (obvious from code)
# Calculate the file hash
file_hash = fhash(path)

# Good: Non-obvious optimization
# Process in batches to avoid OOM with large corpora
for batch in chunks(documents, size=100):
    embeddings = model.encode(batch)

# Good: TODO with context
# TODO(username): Add incremental indexing to avoid full reindex
# See issue #123 for discussion
```

---

## Error Handling

### Exceptions

**Prefer specific exceptions** over generic ones:

```python
# Good
if not path.exists():
    raise FileNotFoundError(f"File not found: {path}")

if not path.suffix in ALLOWED_EXTS:
    raise ValueError(f"Unsupported file type: {path.suffix}")

# Bad
if not path.exists():
    raise Exception("File not found")  # Too generic
```

### Try-Except

**Catch specific exceptions**, avoid bare `except:`:

```python
# Good
try:
    text = path.read_text(encoding="utf-8")
except UnicodeDecodeError:
    # Fallback to latin-1 for older documents
    text = path.read_text(encoding="latin-1")
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    raise

# Bad
try:
    text = path.read_text()
except:  # Catches everything, including KeyboardInterrupt!
    text = ""
```

### Logging vs Raising

**Log for debugging, raise for failures**:

```python
# Good: Log non-critical issues
logger.warning(f"Empty file, skipping: {path}")

# Good: Raise for critical failures
if collection is None:
    raise RuntimeError("ChromaDB collection not initialized")

# Bad: Silent failures
try:
    result = process_file(path)
except Exception:
    pass  # User has no idea something went wrong
```

---

## File Organization

### Module Structure

Organize imports in this order:

1. Standard library
2. Third-party libraries
3. Local modules

```python
# Standard library
import os
import json
from pathlib import Path
from typing import Optional

# Third-party
import chromadb
from sentence_transformers import SentenceTransformer
from watchdog.events import FileSystemEventHandler

# Local
from ingest.extractor import read_text_with_ocr
from ingest.utils import normalize_path
```

### File Layout

Organize file contents in this order:

1. Module docstring
2. Imports
3. Constants
4. Helper functions (private, prefixed with `_`)
5. Public functions/classes
6. Main execution (`if __name__ == "__main__":`)

```python
"""Module for document text extraction.

Supports PDF, DOCX, PPTX, and other common formats.
Falls back to OCR for scanned documents.
"""

# Imports...

# Constants
SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"]
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Private helpers
def _detect_encoding(path: Path) -> str:
    """Detect file encoding."""
    pass

# Public API
def read_text_with_ocr(path: Path) -> str:
    """Extract text from file."""
    pass

# Main (for testing)
if __name__ == "__main__":
    import sys
    print(read_text_with_ocr(Path(sys.argv[1])))
```

---

## Pathlib Usage

**Always use `pathlib.Path`** for file operations:

```python
from pathlib import Path

# Good
root = Path("/home/user/docs")
file_path = root / "subdir" / "file.pdf"
if file_path.exists():
    content = file_path.read_text()

# Bad
import os
root = "/home/user/docs"
file_path = os.path.join(root, "subdir", "file.pdf")  # String manipulation
if os.path.exists(file_path):
    with open(file_path) as f:
        content = f.read()
```

**Benefits**:
- Cross-platform (handles `/` vs `\` automatically)
- Clear, object-oriented API
- Less prone to path traversal bugs

---

## Function Guidelines

### Size

**Keep functions small** (< 50 lines ideal, < 100 max):

```python
# Good: Single responsibility
def load_documents(root: Path) -> list[str]:
    """Load all documents from directory."""
    paths = _find_files(root)
    return [_read_file(p) for p in paths]

def _find_files(root: Path) -> list[Path]:
    """Find all supported files recursively."""
    return list(root.rglob("*"))

def _read_file(path: Path) -> str:
    """Read single file."""
    return path.read_text()

# Bad: Does too much
def load_documents(root):
    """Load documents."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if os.path.splitext(path)[1] in [".pdf", ".txt"]:
                try:
                    with open(path) as f:
                        results.append(f.read())
                except:
                    pass
    return results
```

### Parameters

**Limit parameters** (< 5 ideal):

```python
# Good: Few, clear parameters
def chunk_text(text: str, size: int = 3000, overlap: int = 400) -> list[tuple[int, int, str]]:
    pass

# If more needed, use a config object
from dataclasses import dataclass

@dataclass
class ChunkConfig:
    size: int = 3000
    overlap: int = 400
    min_chunk_size: int = 100
    preserve_paragraphs: bool = True

def chunk_text(text: str, config: ChunkConfig) -> list[tuple[int, int, str]]:
    pass
```

### Return Values

**Be consistent** with return types:

```python
# Good: Always returns list (empty if none)
def find_matches(query: str) -> list[str]:
    if not query:
        return []
    return search(query)

# Bad: Sometimes list, sometimes None
def find_matches(query: str):
    if not query:
        return None  # Caller has to check for None
    return search(query)
```

---

## Testing Guidelines

### Test Organization

Structure tests to mirror source code:

```
2ndBrain_RAG/
├── mcp_server.py
├── ingest/
│   ├── extractor.py
│   └── ocr.py
└── tests/
    ├── test_mcp_server.py
    ├── test_extractor.py
    └── test_ocr.py
```

### Test Naming

```python
# Good: Descriptive test names
def test_chunk_text_with_overlap():
    """Test chunking with overlap preserves context."""
    pass

def test_read_pdf_with_scanned_pages():
    """Test OCR fallback for scanned PDFs."""
    pass

# Bad: Vague names
def test_chunk():
    pass

def test_pdf():
    pass
```

### Test Structure

Use **Arrange-Act-Assert** pattern:

```python
def test_chunk_text_returns_correct_offsets():
    """Verify chunk offsets match text positions."""
    # Arrange
    text = "a" * 1000
    chunk_size = 300
    overlap = 50

    # Act
    chunks = chunk_text(text, size=chunk_size, overlap=overlap)

    # Assert
    assert len(chunks) > 0
    for start, end, content in chunks:
        assert text[start:end] == content
```

---

## Performance Considerations

### Avoid Premature Optimization

Write clear code first, optimize if needed:

```python
# Good: Clear, readable
def filter_documents(docs: list[str], min_length: int) -> list[str]:
    return [doc for doc in docs if len(doc) >= min_length]

# Bad: "Optimized" but harder to read (unless proven bottleneck)
def filter_documents(docs, min_len):
    return list(filter(lambda d: len(d) >= min_len, docs))
```

### Profile Before Optimizing

```python
import time

# Measure performance
start = time.time()
result = expensive_operation()
print(f"Took {time.time() - start:.2f}s")

# Or use profiler
import cProfile
cProfile.run('expensive_operation()')
```

### Known Hotspots

In this project:
- **Embedding generation**: Batch when possible
- **OCR processing**: Most expensive operation
- **File I/O**: Buffer reads, avoid repeated opens

---

## Security Guidelines

### Input Validation

**Always validate user input**:

```python
# Good: Validate and sanitize
def get_document(path: str) -> str:
    # Prevent path traversal
    safe_path = Path(path).resolve()
    if not safe_path.is_relative_to(ROOT_DIR):
        raise ValueError("Path outside allowed directory")
    return safe_path.read_text()

# Bad: Trusts input
def get_document(path: str) -> str:
    return Path(path).read_text()  # Could access /etc/passwd!
```

### Secrets Management

**Never commit secrets**:

```python
# Good: Use environment variables
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not set")

# Bad: Hardcoded
api_key = "sk-1234567890abcdef"  # Never do this!
```

---

## Git Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(ocr): Add DeepSeek-OCR engine support

Integrate DeepSeek-OCR as an optional OCR engine for improved
accuracy on complex documents. Falls back to Surya if not available.

Closes #123
```

```
fix(extractor): Handle empty PDFs gracefully

Previously crashed on PDFs with no text content. Now returns
empty string and logs warning.
```

---

## Code Review Checklist

Before submitting code:

- [ ] Follows naming conventions
- [ ] Has type hints on public functions
- [ ] Has docstrings on public functions
- [ ] No hardcoded paths or secrets
- [ ] Uses `pathlib.Path` for file operations
- [ ] Handles errors appropriately
- [ ] Tests pass (if tests exist)
- [ ] No unnecessary complexity
- [ ] Updated relevant documentation
- [ ] Commit messages are clear

---

## Tools and Automation

### Recommended Tools

- **Black**: Auto-formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **pylint**: Linting
- **pytest**: Testing

### Setup

```bash
pip install black isort mypy pylint pytest

# Format code
black mcp_server.py ingest/

# Sort imports
isort mcp_server.py ingest/

# Type check
mypy mcp_server.py

# Lint
pylint mcp_server.py

# Run tests
pytest tests/
```

---

## References

- [PEP 8 – Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 – Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Real Python – Code Quality](https://realpython.com/python-code-quality/)

---

**Version**: 1.0
**Last Updated**: 2025-11-13

**Questions?** Open an issue or discussion on GitHub.
