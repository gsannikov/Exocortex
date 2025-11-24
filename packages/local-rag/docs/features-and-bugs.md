# Features and Bugs

This document tracks planned features, known bugs, and improvement ideas for 2ndBrain_RAG.

---

## Feature Requests

### High Priority

#### 1. Incremental Indexing
**Status**: Planned for v0.3.0
**Priority**: P0
**Effort**: Medium

**Description**: Currently, any change to a file triggers a full reindex of that file. This is inefficient for large documents.

**Proposal**:
- Track chunks with individual hashes
- On file change, compare chunk hashes
- Update only modified chunks
- Preserve unchanged chunks

**Benefits**:
- Faster reindexing (especially for large PDFs)
- Lower resource usage
- Better user experience

**Implementation**:
```python
# Store chunk metadata
{
  "file_hash": "abc123",
  "chunks": [
    {"id": "abc123:0:3000", "hash": "def456"},
    {"id": "abc123:3000:6000", "hash": "ghi789"}
  ]
}

# On file change
- Read new file
- Chunk new content
- Compare chunk hashes
- Upsert only changed chunks
- Delete removed chunks
```

**Blockers**: None

**References**: See [roadmap.md](roadmap.md) Q1 2025

---

#### 2. Configuration Validation
**Status**: Planned for v0.3.0
**Priority**: P0
**Effort**: Low

**Description**: Currently, invalid configuration values cause cryptic errors or silent failures.

**Proposal**:
- Validate `.env` on startup
- Check required variables are set
- Validate types and ranges
- Provide clear error messages

**Example**:
```python
# Validation rules
validators = {
    "ROOT_DIR": lambda v: Path(v).exists(),
    "CHUNK_SIZE": lambda v: 100 <= int(v) <= 10000,
    "EMBED_MODEL": lambda v: v in SUPPORTED_MODELS
}

# On startup
errors = []
for key, validator in validators.items():
    value = os.getenv(key)
    if not validator(value):
        errors.append(f"Invalid {key}: {value}")

if errors:
    raise ValueError("\n".join(errors))
```

**Blockers**: None

---

#### 3. Error Recovery and Retry
**Status**: Planned for v0.3.0
**Priority**: P1
**Effort**: Medium

**Description**: Transient errors (network, file locks, OOM) cause permanent failures.

**Proposal**:
- Retry logic for transient errors
- Exponential backoff
- Max retry limits
- Graceful degradation

**Example**:
```python
@retry(max_attempts=3, backoff=2.0)
def read_file_with_ocr(path: Path) -> str:
    """Read file with retry logic."""
    pass

# Logs
ERROR: Failed to read file.pdf (attempt 1/3): PermissionError
INFO: Retrying in 2.0 seconds...
ERROR: Failed to read file.pdf (attempt 2/3): PermissionError
INFO: Retrying in 4.0 seconds...
SUCCESS: Read file.pdf (attempt 3/3)
```

**Blockers**: None

---

### Medium Priority

#### 4. Hybrid Search (BM25 + Semantic)
**Status**: Planned for v0.5.0
**Priority**: P1
**Effort**: High

**Description**: Semantic search misses exact keyword matches. BM25 misses conceptual matches. Hybrid is best of both.

**Proposal**:
- Add BM25 index (using `rank-bm25` library)
- Query both indexes
- Combine scores using RRF (Reciprocal Rank Fusion)
- Configurable weighting

**Implementation**:
```python
# Query both
semantic_results = chroma.query(embedding, k=20)
bm25_results = bm25_index.search(query, k=20)

# Combine with RRF
combined = reciprocal_rank_fusion(
    [semantic_results, bm25_results],
    k=60  # RRF parameter
)

return combined[:k]
```

**Benefits**:
- Better accuracy
- Handles both use cases
- Configurable for different corpora

**Blockers**: Needs benchmarking data

**References**: [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

---

#### 5. Configuration TUI
**Status**: Planned for v0.4.0
**Priority**: P2
**Effort**: Medium

**Description**: `.env` files are intimidating for non-technical users.

**Proposal**:
- Interactive TUI using `textual` or `rich`
- Guided setup wizard
- Input validation
- Save to `.env`

**UI Mockup**:
```
┌─────────────────────────────────────────┐
│ 2ndBrain_RAG Configuration              │
├─────────────────────────────────────────┤
│ Documents Folder:                       │
│ /home/user/Documents   [Browse]         │
│                                         │
│ Allowed Extensions:                     │
│ .pdf, .txt, .md, .docx [Default]       │
│                                         │
│ Chunk Size:                             │
│ 3000 characters        [Recommended]    │
│                                         │
│ OCR Engine:                             │
│ ○ Surya (Fast, CPU)                    │
│ ○ PaddleOCR (Balanced)                 │
│ ○ DeepSeek (Accurate, Slow)            │
│                                         │
│ [Save] [Cancel] [Reset to Defaults]    │
└─────────────────────────────────────────┘
```

**Blockers**: None

---

#### 6. Search History and Suggestions
**Status**: Planned for v0.5.0
**Priority**: P2
**Effort**: Low

**Description**: Users often repeat similar searches. Suggestions would improve UX.

**Proposal**:
- Track search queries (locally)
- Suggest similar past queries
- Learn common query patterns
- Expose via MCP tool

**Privacy**: All data stored locally, no telemetry

**Blockers**: Needs UX design

---

### Low Priority

#### 7. Multi-Modal Search (Images)
**Status**: Planned for v0.5.0
**Priority**: P3
**Effort**: High

**Description**: Can't search for images or diagrams conceptually.

**Proposal**:
- Extract images from documents
- Generate visual embeddings (CLIP)
- Enable image-to-image search
- Enable text-to-image search

**Example**:
```python
# Text-to-image search
results = search_images("architecture diagram with database")

# Image-to-image search
results = search_images(query_image=Path("example.png"))
```

**Blockers**: Requires CLIP or similar model (~500MB)

---

#### 8. Temporal Search
**Status**: Idea stage
**Priority**: P3
**Effort**: Medium

**Description**: "When did I work on X?" queries are common but unsupported.

**Proposal**:
- Track document access/modification times
- Index by time periods
- Enable temporal queries

**Example**:
```python
# Search documents modified in date range
results = search(
    query="machine learning",
    date_from="2024-01-01",
    date_to="2024-03-31"
)
```

**Blockers**: Needs user research

---

## Known Bugs

### Critical (P0)

#### None currently

---

### High Priority (P1)

#### 1. File Watcher Race Condition
**Status**: Open
**Affected Versions**: v0.2.0+
**Priority**: P1

**Description**: Rapid file changes can cause race conditions between watcher and indexer.

**Reproduction**:
1. Edit large file
2. Save rapidly multiple times
3. Observe: Multiple indexing jobs start simultaneously

**Expected**: Debounce changes, process once

**Actual**: Multiple concurrent indexing attempts

**Workaround**: Wait for indexing to complete before next save

**Fix**: Implement proper debouncing with locks

```python
from threading import Lock

index_lock = Lock()
pending_changes = {}

def on_file_change(path):
    # Cancel existing timer
    if path in pending_changes:
        pending_changes[path].cancel()

    # Schedule with debounce
    timer = Timer(1.0, lambda: index_with_lock(path))
    pending_changes[path] = timer
    timer.start()

def index_with_lock(path):
    with index_lock:
        do_ingest(path)
```

**Target**: v0.3.0

---

#### 2. Large PDF Memory Usage
**Status**: Open
**Affected Versions**: All
**Priority**: P1

**Description**: Loading large PDFs (>100MB) can cause OOM errors.

**Reproduction**:
1. Add 500+ page PDF with images
2. Trigger indexing
3. Observe: Memory usage spikes to 4GB+

**Expected**: Controlled memory usage (<2GB)

**Actual**: Unbounded memory usage

**Workaround**: Split large PDFs into smaller files

**Fix**: Stream PDF processing page-by-page

```python
def read_pdf_streaming(path: Path) -> str:
    """Process PDF page by page to limit memory usage."""
    text_parts = []
    with pypdf.PdfReader(path) as reader:
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text_parts.append(page.extract_text())
            # Yield chunks periodically
            if len(text_parts) > 10:
                yield "\n".join(text_parts)
                text_parts.clear()
```

**Target**: v0.3.0

---

### Medium Priority (P2)

#### 3. Empty Search Results for Known Content
**Status**: Open
**Affected Versions**: All
**Priority**: P2

**Description**: Sometimes returns no results even when content definitely exists.

**Possible Causes**:
- Chunking split relevant content
- Embedding model bias
- Query phrasing mismatch

**Investigation**:
```python
# Debug script
query = "specific content"
embedding = model.encode(query)
results = COLL.query(embedding, n_results=100)

# Check if ANY result contains query text
for result in results:
    if query.lower() in result.lower():
        print(f"Found in result #{i}, score: {score}")
```

**Workaround**: Try different query phrasings, increase `k` parameter

**Target**: v0.5.0 (hybrid search should help)

---

#### 4. OCR Quality Varies Widely
**Status**: Known limitation
**Affected Versions**: All
**Priority**: P2

**Description**: OCR accuracy depends heavily on input quality.

**Factors**:
- Scan resolution (DPI)
- Image quality (blur, noise)
- Font types and sizes
- Language and special characters

**Mitigation**:
- Increase DPI for specific files
- Pre-process images (deskew, denoise)
- Use higher-accuracy OCR engine (DeepSeek)

**Not a Bug**: Inherent limitation of OCR technology

**Improvement**: Add pre-processing pipeline (v0.6.0)

---

### Low Priority (P3)

#### 5. Unicode Handling in Filenames
**Status**: Open
**Affected Versions**: All
**Priority**: P3

**Description**: Files with non-ASCII characters in names may not be indexed correctly.

**Example**: `résumé.pdf`, `日本語.txt`

**Workaround**: Use ASCII filenames

**Fix**: Proper Unicode normalization

```python
import unicodedata

def normalize_path(path: Path) -> Path:
    """Normalize Unicode in file paths."""
    normalized = unicodedata.normalize("NFC", str(path))
    return Path(normalized)
```

**Target**: v0.4.0

---

#### 6. Windows Path Handling
**Status**: Open
**Affected Versions**: All
**Priority**: P3

**Description**: Hardcoded `/` separators may break on Windows.

**Fix**: Use `pathlib.Path` everywhere (partially done)

**Target**: v0.4.0

---

## Feature Ideas (Backlog)

Ideas without concrete plans yet:

### Search & Retrieval
- [ ] Fuzzy matching for names and terms
- [ ] Query expansion using synonyms
- [ ] Multi-query search (OR, AND, NOT)
- [ ] Search within specific file types
- [ ] Date range filtering
- [ ] Author/metadata filtering
- [ ] Citation graph visualization

### Document Processing
- [ ] Table extraction and querying
- [ ] Code snippet extraction
- [ ] Equation recognition (LaTeX)
- [ ] Bibliography extraction
- [ ] Footnote handling
- [ ] Multi-column layout handling

### User Experience
- [ ] Progress indicators for indexing
- [ ] Estimated time remaining
- [ ] Preview of search results
- [ ] Highlight query terms in results
- [ ] "Did you mean?" suggestions
- [ ] Keyboard shortcuts

### Performance
- [ ] Parallel document processing
- [ ] GPU acceleration for embeddings
- [ ] Caching for frequent queries
- [ ] Index compression
- [ ] Incremental embedding updates

### Integration
- [ ] Zotero bibliography sync
- [ ] Obsidian bidirectional links
- [ ] Git repository indexing
- [ ] Email archive indexing
- [ ] Browser history/bookmarks

### Advanced
- [ ] Knowledge graph extraction
- [ ] Entity recognition (NER)
- [ ] Automatic summarization
- [ ] Topic clustering
- [ ] Duplicate detection
- [ ] Automated tagging

---

## Bug Reporting

### How to Report Bugs

1. Check if already reported in this document
2. Search existing GitHub issues
3. Create new issue with template:

```markdown
**Bug Description**: Brief summary

**Steps to Reproduce**:
1. Step one
2. Step two
3. ...

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: macOS 14.1 (M2)
- Python: 3.11.5
- Version: v0.2.0

**Logs**: Paste relevant error messages

**Workaround**: If known
```

### Bug Triage Process

**Labels**:
- `bug` - Confirmed bugs
- `feature` - Feature requests
- `enhancement` - Improvements to existing features
- `documentation` - Doc issues
- `good-first-issue` - Easy for newcomers
- `help-wanted` - Looking for contributors

**Priority**:
- `P0` - Critical, affects all users
- `P1` - High, affects many users
- `P2` - Medium, affects some users
- `P3` - Low, edge cases or nice-to-haves

---

## Feature Request Process

### How to Request Features

1. Check [roadmap.md](roadmap.md) and this document
2. Open GitHub issue with template:

```markdown
**Feature Description**: Brief summary

**Use Case**: Why is this needed?

**Proposed Solution**: How might this work?

**Alternatives Considered**: Other approaches?

**Impact**: Who benefits? How much?

**Complexity**: Rough estimate (Low/Med/High)
```

### Feature Evaluation Criteria

We evaluate features based on:

1. **Alignment with Vision**: Does it fit our local-first, privacy-focused philosophy?
2. **User Impact**: How many users benefit?
3. **Complexity**: Development effort vs. value
4. **Maintenance**: Long-term support burden
5. **Performance**: Impact on speed/memory
6. **Security**: Risk to user privacy/data

**Examples**:

| Feature | Vision | Impact | Complexity | Decision |
|---------|--------|--------|------------|----------|
| Incremental indexing | ✅ | High | Medium | Accept |
| Cloud sync | ❌ | Medium | High | Reject |
| Hybrid search | ✅ | High | Medium | Accept |
| Real-time collab | ⚠️ | Low | Very High | Defer |

---

## Contributing

Want to fix a bug or implement a feature?

1. Read [coding-conventions.md](coding-conventions.md)
2. Check [backlog.md](backlog.md) for tasks
3. Comment on issue to claim it
4. Submit PR with clear description
5. Ensure tests pass
6. Update documentation

**Good first issues**:
- Configuration validation
- Unicode normalization
- Better error messages
- Documentation improvements

---

## References

- [roadmap.md](roadmap.md) - Long-term plans
- [backlog.md](backlog.md) - Task breakdown
- [changelog.md](changelog.md) - Version history
- [GitHub Issues](https://github.com/yourusername/2ndBrain_RAG/issues)

---

**Last Updated**: 2025-11-13
**Next Review**: 2025-12-13 (monthly review)

**Questions?** Open an issue or discussion on GitHub.
