# Agent Guide for Claude Code

**Target Audience**: Claude Code AI assistant working on this repository

**Purpose**: Get up to speed quickly and work effectively on 2ndBrain_RAG

---

## Quick Start: 30-Second Context

You're working on **2ndBrain_RAG**, a local RAG system that lets Claude Desktop/Code search and retrieve context from a user's personal document collection via MCP protocol.

**Key Tech**: Python 3.11+, MCP, ChromaDB, sentence-transformers, OCR (Surya/PaddleOCR)

**Code Structure**:
- `mcp_server.py` - Main MCP server with 5 tools
- `ingest/` - Document extraction and OCR
- `state/` - Persistent state tracking
- `docs/` - Documentation (this file)

---

## Project Mental Model

Think of this as **"grep for meaning"** + **automatic indexing** + **Claude integration**.

```
User saves PDF → Auto-indexed → Claude can search it → Returns relevant passages
```

This is NOT:
- A web service (it's an MCP server)
- A chat interface (it's a tool backend)
- A document manager (it's a search/retrieval system)

---

## Common Tasks

### Task: Add Support for New File Format

**Files to modify**:
1. `ingest/extractor.py` - Add extraction logic
2. Update `ALLOWED_EXTS` in environment/docs

**Example**:
```python
# In extractor.py
def read_text_with_ocr(path: Path) -> str:
    ext = path.suffix.lower()
    # Add your format here
    if ext == '.epub':
        return extract_epub(path)
    # ... existing code
```

**Test**: Add sample file to ROOT_DIR, trigger reindex, verify searchable

---

### Task: Fix OCR Quality Issue

**Primary file**: `ingest/ocr.py`

**Quick wins**:
- Increase DPI (200 → 300) for specific files
- Add pre-processing (deskew, denoise)
- Try different OCR engine (Surya → PaddleOCR → DeepSeek)

**Location**: See `_ocr_surya()`, `_ocr_paddle()` functions

---

### Task: Improve Search Relevance

**Key areas**:
1. **Chunking**: `mcp_server.py` `chunk_text()` function
   - Adjust `CHUNK_SIZE` (default 3000)
   - Adjust `CHUNK_OVERLAP` (default 400)

2. **Embedding model**: Change `EMBED_MODEL` env var
   - Current: `all-MiniLM-L6-v2` (fast, 384-dim)
   - Better: `all-mpnet-base-v2` (slower, 768-dim)

3. **Reranking**: Add in `handle_search()` tool
   - Use rapidfuzz (already imported)
   - Combine semantic + lexical scores

---

### Task: Add New MCP Tool

**Pattern**:
```python
@server.list_tools()
async def list_tools():
    return [
        # ... existing tools
        types.Tool(
            name="rag.your_tool",
            description="Clear description for Claude",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "..."}
                },
                "required": ["param"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, args: dict):
    if name == "rag.your_tool":
        result = your_implementation(args["param"])
        return [TextContent(type="text", text=result)]
    # ... existing tools
```

---

### Task: Debug Indexing Issues

**Check in order**:

1. **File watcher logs**: Is event firing?
   - Add debug print in `FSHandler` class

2. **State tracking**: Is file state recorded?
   - Check `state/ingest_state.json`
   - Verify hash matches file content

3. **ChromaDB**: Are embeddings stored?
   - Check `COLL.count()` in `stats` tool
   - Query directly: `COLL.peek()`

4. **File permissions**: Can Python read the file?
   - Try manual read: `Path(file).read_text()`

**Quick reset**:
```bash
# Clear everything and reindex
rm -rf .chromadb state/ingest_state.json
python mcp_server.py  # (then trigger via Claude)
```

---

## Code Navigation

### Critical Functions

| Function | File | Purpose | Line Ref |
|----------|------|---------|----------|
| `chunk_text()` | mcp_server.py | Split documents | ~45 |
| `fhash()` | mcp_server.py | File hash for change detection | ~32 |
| `do_ingest()` | mcp_server.py | Main indexing logic | ~60+ |
| `read_text_with_ocr()` | ingest/extractor.py | Extract text from files | ~10+ |
| `handle_search()` | mcp_server.py | Search tool implementation | ~120+ |

### Data Flow Cheat Sheet

**Indexing**:
```
File change → FSHandler.on_modified() → debounce → do_ingest(path)
                                                          ↓
                                                    read_text()
                                                          ↓
                                                    chunk_text()
                                                          ↓
                                                    model.encode()
                                                          ↓
                                                    COLL.upsert()
```

**Searching**:
```
Claude → rag.search → handle_search(query, k)
                             ↓
                       model.encode(query)
                             ↓
                       COLL.query(embedding, n_results=k)
                             ↓
                       Format results → Return to Claude
```

---

## Configuration Reference

### Environment Variables (.env)

```bash
ROOT_DIR=/path/to/docs          # Where to index
ALLOWED_EXTS=.pdf,.txt,.md      # File types
CHUNK_SIZE=3000                 # Chunk size in chars
CHUNK_OVERLAP=400               # Overlap for context
PERSIST_DIR=.chromadb           # ChromaDB location
EMBED_MODEL=all-MiniLM-L6-v2    # Embedding model
```

### Typical Tuning

**For code/technical docs**: Smaller chunks (1500-2000)
**For prose/articles**: Larger chunks (3000-5000)
**For scanned PDFs**: Increase OCR DPI, use DeepSeek-OCR

---

## Architecture Quick Reference

```
┌─────────────────────┐
│   Claude Desktop    │
└──────────┬──────────┘
           │ MCP (stdio)
┌──────────▼──────────┐
│   mcp_server.py     │
│   ┌──────────────┐  │
│   │ 5 MCP Tools  │  │
│   └──────────────┘  │
└─────┬───────────┬───┘
      │           │
┌─────▼─────┐ ┌──▼─────────┐
│  Ingest   │ │ File Watch │
│  Pipeline │ │ (watchdog) │
└─────┬─────┘ └──┬─────────┘
      │           │
      └─────┬─────┘
      ┌─────▼──────┐
      │  ChromaDB  │
      └────────────┘
```

---

## Common Pitfalls

### 1. Forgetting to Reindex After Changes

**Problem**: Changed chunking logic, but search still uses old chunks

**Solution**: Either:
- Clear `.chromadb/` and `state/`
- Call `rag.invalidate` on affected files
- Trigger full reindex via file watcher or manual call

### 2. Path Handling on Different OSes

**Problem**: Hardcoded `/` or `\` separators

**Solution**: Always use `pathlib.Path`
```python
# Good
from pathlib import Path
p = Path(root) / "subdir" / "file.pdf"

# Bad
p = root + "/subdir/file.pdf"
```

### 3. Assuming Text Extraction Always Works

**Problem**: PDF is scanned, but code expects text

**Solution**: Always handle OCR fallback in `extractor.py`

### 4. Ignoring Embeddings Model Changes

**Problem**: Changed `EMBED_MODEL`, but didn't reindex

**Solution**: Embeddings are model-specific. Must reindex when model changes.

### 5. Not Handling File Deletions

**Problem**: Deleted file still appears in search results

**Solution**: File watcher handles this via `FSHandler.on_deleted()`

---

## Testing Strategy

### Manual Testing Flow

```bash
# 1. Start server (via Claude Desktop config)
# 2. Add test document
echo "Machine learning is the future" > ~/2ndBrain_RAG/test.txt

# 3. Wait for auto-index or trigger manually in Claude:
# "Can you reindex my documents?"

# 4. Search
# "Search for documents about machine learning"

# 5. Verify results include test.txt
```

### Unit Test Locations

No formal tests yet (TODO), but you can add them:

```
tests/
├── test_extractor.py      # Document extraction
├── test_chunking.py       # Chunk logic
├── test_ocr.py            # OCR engines
└── test_integration.py    # End-to-end
```

**Pattern**:
```python
import pytest
from ingest.extractor import read_text_with_ocr

def test_pdf_extraction(tmp_path):
    # Create test PDF
    pdf_path = tmp_path / "test.pdf"
    # ... create PDF

    text = read_text_with_ocr(pdf_path)
    assert "expected content" in text
```

---

## Debugging Tips

### Problem: "No results found" for known content

**Checklist**:
1. Is file indexed? Check `rag.stats`
2. Is query semantically similar? Try exact phrase first
3. Is k parameter too small? Increase in search call
4. Check ChromaDB: `COLL.peek()` in Python shell

### Problem: OCR not detecting text

**Checklist**:
1. Is image clear/high-res?
2. Is Surya working? Try PaddleOCR
3. Check DPI setting in ocr.py
4. Try manual OCR: `python -c "from ingest.ocr import *; print(ocr_image(...))"

### Problem: High memory usage

**Causes**:
- Large CHUNK_SIZE + many files = many embeddings
- Embedding model loaded in memory (~500MB)
- ChromaDB cache

**Solutions**:
- Increase CHUNK_SIZE (fewer chunks)
- Switch to smaller embedding model
- Limit ROOT_DIR scope

### Problem: File watcher not triggering

**Checklist**:
1. Is file in ROOT_DIR (recursively)?
2. Is extension in ALLOWED_EXTS?
3. Check watchdog has file permissions
4. Look for errors in server output

---

## Code Style and Conventions

See [coding-conventions.md](coding-conventions.md) for full details.

**Quick rules**:
- Use `pathlib.Path` for all file operations
- Type hints for function signatures
- Docstrings for public functions
- Keep functions < 50 lines
- Prefer explicit over clever

**Example**:
```python
def chunk_text(text: str, size: int = 3000, overlap: int = 400) -> list[tuple[int, int, str]]:
    """Split text into overlapping chunks.

    Args:
        text: Input text to chunk
        size: Maximum chunk size in characters
        overlap: Overlap between consecutive chunks

    Returns:
        List of (start_offset, end_offset, chunk_text) tuples
    """
    # Implementation
```

---

## Working with the MCP Protocol

### Key Concepts

**Tools**: Functions Claude can call (like API endpoints)
**Resources**: Data Claude can access (not used in this project)
**Prompts**: Reusable prompt templates (not used in this project)

### Tool Design Guidelines

1. **Clear names**: Use `rag.verb` pattern (search, get, reindex)
2. **Simple schemas**: Avoid complex nested objects
3. **Good descriptions**: Claude reads these to decide when to call
4. **Validate inputs**: Check types, ranges before using
5. **Return structured data**: Use consistent format

**Example Tool Schema**:
```python
types.Tool(
    name="rag.search",
    description="Semantic search over indexed documents. Returns top-k most relevant passages with metadata.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language search query"
            },
            "k": {
                "type": "integer",
                "description": "Number of results to return (default: 5)",
                "default": 5
            }
        },
        "required": ["query"]
    }
)
```

---

## Performance Tuning

### Bottlenecks

| Operation | Bottleneck | Solution |
|-----------|------------|----------|
| Indexing large PDFs | OCR speed | Reduce DPI, use Surya (fastest) |
| Embedding generation | CPU-bound | Batch encoding, reduce chunk count |
| Search latency | ChromaDB query | Increase CHUNK_SIZE (fewer vectors) |
| Memory usage | Model + embeddings | Use smaller model, limit corpus size |

### Benchmarking

```python
import time

# Measure indexing
start = time.time()
do_ingest(path)
print(f"Indexed in {time.time() - start:.2f}s")

# Measure search
start = time.time()
results = handle_search(query, k=10)
print(f"Searched in {time.time() - start:.2f}s")
```

---

## Security Considerations

**Current state**: Development/personal use only

**When modifying**:
- Validate all file paths (no `../` escapes)
- Sanitize user input before passing to shell
- Don't expose ChromaDB to network
- Be careful with `eval()` or `exec()` (never use)

**Production TODO** (see [features-and-bugs.md](features-and-bugs.md)):
- Add input validation
- Implement rate limiting
- Add authentication
- Use HTTPS if exposing API
- Audit dependencies for CVEs

---

## Integration Points

### With Claude Desktop

**Config location**: `~/.config/claude/mcp.json` (Linux/Mac) or `%APPDATA%\Claude\mcp.json` (Windows)

**Example**:
```json
{
  "mcpServers": {
    "local-rag": {
      "command": "python",
      "args": ["-u", "/absolute/path/to/mcp_server.py"],
      "cwd": "/absolute/path/to/2ndBrain_RAG",
      "env": {
        "PYTHONUNBUFFERED": "1",
        "ROOT_DIR": "/path/to/documents"
      }
    }
  }
}
```

**Restart required**: After config changes, restart Claude Desktop

---

## Resources and References

### Documentation
- [architecture.md](architecture.md) - System architecture
- [problem-and-vision.md](problem-and-vision.md) - Project goals
- [coding-conventions.md](coding-conventions.md) - Code style
- [roadmap.md](roadmap.md) - Future plans

### External
- [MCP Protocol](https://github.com/anthropics/mcp) - Protocol spec
- [ChromaDB Docs](https://docs.trychroma.com) - Vector DB
- [sentence-transformers](https://www.sbert.net) - Embeddings
- [watchdog](https://python-watchdog.readthedocs.io) - File monitoring

### Code Examples
- `mcp_server.py` - Main server implementation
- `ingest/extractor.py` - Document extraction patterns
- `ingest/ocr.py` - OCR integration examples

---

## Key Constraints

Remember these when making changes:

1. **Must run offline**: After model download, no internet required
2. **Must run on laptops**: No GPU required, modest RAM/CPU
3. **Must be simple**: Minimal dependencies, clear code
4. **Must preserve privacy**: No telemetry, no cloud calls
5. **Must integrate with Claude**: MCP protocol, not standalone
6. **Must handle real documents**: PDFs, scanned images, varied formats

---

## Quick Decision Matrix

| If you need to... | Then... |
|-------------------|---------|
| Add file format support | Modify `ingest/extractor.py` |
| Improve search quality | Tune chunking or embedding model |
| Fix OCR issues | Modify `ingest/ocr.py` |
| Add MCP tool | Add to `list_tools()` and `call_tool()` |
| Debug indexing | Check `state/ingest_state.json` and ChromaDB |
| Change behavior | Check `.env.example` for config options |
| Understand flow | Read `architecture.md` diagrams |
| Find prior art | Check `problem-and-vision.md` references |

---

## Final Checklist: Before Pushing Changes

- [ ] Code follows conventions (see coding-conventions.md)
- [ ] Added/updated docstrings for public functions
- [ ] Tested manually with sample documents
- [ ] No hardcoded paths or secrets
- [ ] Updated relevant docs (README, architecture, etc.)
- [ ] Considered backward compatibility
- [ ] No breaking changes to MCP tool schemas (or documented)
- [ ] Ran basic smoke test (index → search → retrieve)

---

**Version**: 1.0
**Last Updated**: 2025-11-13
**Maintained By**: Repository contributors

**Questions?** Check existing docs or open an issue.
