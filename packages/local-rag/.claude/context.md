# 2ndBrain_RAG - Context Priming for Claude

**Use this file to get Claude up-to-speed on the project in seconds.**

---

## TL;DR - One Paragraph

2ndBrain_RAG is a FastAPI server that implements local RAG (Retrieval-Augmented Generation). Users add documents to a folder; the system indexes them with ChromaDB, monitors for changes, and serves semantic search + LLM chat endpoints. It integrates with Claude Desktop via MCP protocol. No cloud, no API keys, fully private.

---

## Essential Context

### What It Does
- Indexes local documents (PDFs, notes, etc.) into vector database
- Performs semantic search on those documents
- Answers questions with LLM (Ollama) grounded in document context
- Automatically reindexes when files change
- MCP-compatible for Claude Desktop integration

### Tech Stack (TL;DR)
```
FastAPI (API) + ChromaDB (Vector DB) + sentence-transformers (Embeddings)
+ Ollama (Local LLM) + watchdog (File monitoring) + LangChain (Document processing)
```

### 4 API Endpoints
```
GET  /status              → Check indexing status
POST /ingest              → Load & index documents
GET  /search?q=...&k=5    → Find relevant documents
POST /chat                → Ask questions with context
```

### Key Files
| File | Purpose |
|------|---------|
| `rag_mcp_server.py` | Main FastAPI app + endpoints |
| `utils/loader.py` | Load & chunk documents |
| `utils/embedder.py` | Store/retrieve vectors |
| `utils/llm.py` | Call Ollama for chat |
| `utils/watcher.py` | Monitor file changes |

---

## Quick Reference

### Start Server
```bash
source .venv/bin/activate
uvicorn rag_mcp_server:app --host 0.0.0.0 --port 8000
```

### Test Endpoints
```bash
# Check status
curl http://localhost:8000/status

# Search
curl "http://localhost:8000/search?q=topic&k=5"

# Chat
curl -X POST http://localhost:8000/chat \
  -d '{"query": "What is RAG?", "k": 5}' \
  -H "Content-Type: application/json"
```

### Reindex Documents
```bash
curl -X POST http://localhost:8000/ingest
```

---

## Architecture in 30 Seconds

```
User Question
    ↓
FastAPI receives request
    ↓
[Search path] Query text → embed → ChromaDB → similar docs
[Chat path]   Retrieve docs → format context → Ollama → answer + citations
    ↓
File watcher (background) monitors folder → triggers reindex on changes
```

---

## Configuration

### Environment Variables
```bash
RAG_FOLDER=/path/to/docs          # Documents to index
OLLAMA_HOST=http://localhost:11434 # Ollama endpoint
OLLAMA_MODEL=llama3                # LLM model
```

### Code Tweaks
- **Chunk size**: `utils/loader.py:20` (chunk_size=800, overlap=120)
- **Embedding model**: `rag_mcp_server.py:32` (sentence-transformers/all-MiniLM-L6-v2)
- **Chat prompt**: `rag_mcp_server.py:68-77` (system message & formatting)

---

## Dependencies

### Runtime
- fastapi, uvicorn (web framework)
- langchain (document loading)
- chromadb (vector store)
- sentence-transformers (embeddings)
- watchdog (file monitoring)
- requests (HTTP client to Ollama)

### External (Manual Install)
- Ollama (https://ollama.com)
- Python 3.8+

### Install
```bash
pip install -r requirements.txt
```

---

## Common Tasks

### Add Support for New File Type
1. Edit `SUPPORTED_EXTS` in `utils/loader.py:6-10`
2. Test with sample file

### Modify Chat Prompt
1. Edit prompt template in `rag_mcp_server.py:68-77`
2. Restart server

### Change Embedding Model
1. Edit `rag_mcp_server.py:32`
2. Restart and run `POST /ingest?full_rebuild=true`

### Integrate with Claude Desktop
1. Edit `~/.mcp/config.json`
2. Add 2ndBrain_RAG server entry
3. Restart Claude Desktop

---

## Known Limitations

- ❌ No authentication (development only)
- ❌ Reindexes everything on file change (inefficient)
- ❌ No incremental updates
- ⚠️ Single threading + background watcher can race
- ⚠️ No error recovery

---

## Security Notes

**Current**: Development/personal use only
- No API key required
- No input validation
- No rate limiting

**To use in production**:
1. Add API key authentication
2. Validate input lengths
3. Add rate limiting
4. Use HTTPS
5. See CODE_AUDIT.md for full list

---

## Testing the System

### Manual Test Flow
```bash
1. Start server: uvicorn rag_mcp_server:app
2. Check status: curl http://localhost:8000/status
3. Add test file: echo "Machine learning is..." > ~/2ndBrain_RAG/test.txt
4. Ingest: curl -X POST http://localhost:8000/ingest
5. Search: curl "http://localhost:8000/search?q=learning"
6. Chat: curl -X POST http://localhost:8000/chat -d '{"query": "What is ML?"}'
```

---

## For Claude: Working with This Code

### Before Modifying
1. Read ARCHITECTURE.md for system design
2. Read CODE_AUDIT.md for known issues
3. Understand the 4 API routes and data flow

### When Fixing Bugs
1. Check CODE_AUDIT.md for known issues
2. Add input validation if query-related
3. Add error handling if external service related
4. Test with test files in ~/2ndBrain_RAG/example*.txt

### When Adding Features
1. Keep it simple (this is a learning project)
2. Consider performance implications
3. Update corresponding docs
4. Test end-to-end

### Key Constraints
- Must work offline (after model download)
- Must not require cloud services
- Should run on consumer hardware
- Must stay < 500 lines of code (core)

---

## Performance Targets

| Operation | Target | Actual |
|-----------|--------|--------|
| Index 100 docs | < 15s | ~10s |
| Search 100k vectors | < 500ms | ~150ms |
| Chat response | < 30s | 3-30s (varies by model) |
| File watch trigger | < 1s | < 1s |

---

## Debugging Tips

### Ollama Not Running
```bash
# Error: "Is Ollama running?"
# Fix: Start Ollama separately
ollama serve
# Or pull model first
ollama pull llama3
```

### Port Already in Use
```bash
# Error: "Address already in use"
# Fix: Use different port
uvicorn rag_mcp_server:app --port 8001
```

### Search Returns No Results
1. Check `/status` endpoint - verify documents indexed
2. Run `POST /ingest?full_rebuild=true`
3. Add test documents to RAG_FOLDER
4. Search for exact phrases first

### File Watcher Not Triggering
1. Check file is in RAG_FOLDER (recursive)
2. Check file extension is supported
3. Check server logs for errors
4. Verify watchdog has file permission

---

## File Reference

### Path: `rag_mcp_server.py` (86 lines)
**Main entry point. Contains:**
- FastAPI app setup
- ChromaDB initialization
- 4 HTTP endpoints
- File watcher startup

**Key Functions:**
- `status()` - Get index stats
- `ingest()` - Load & index docs
- `search()` - Semantic search
- `chat()` - RAG Q&A

### Path: `utils/loader.py` (36 lines)
**Document loading pipeline.**

**Key Functions:**
- `load_documents(path)` - Load, parse, chunk all files
- `_iter_files(root)` - Recursively find supported files

**Formats Supported**: txt, md, pdf, docx, etc. (13 total)

### Path: `utils/embedder.py` (21 lines)
**Vector database operations.**

**Key Functions:**
- `upsert_documents(db, docs)` - Add/update vectors
- `reset_index(db)` - Clear all data

### Path: `utils/llm.py` (24 lines)
**Ollama integration.**

**Key Functions:**
- `ollama_chat(prompt, system, model)` - Call local LLM

### Path: `utils/watcher.py` (34 lines)
**File system monitoring.**

**Key Classes:**
- `RAGHandler` - Event handler
- `start_watcher()` - Start monitoring thread

---

## Quick Decisions

### Architectural Choices Made

| Choice | Why | Alternative |
|--------|-----|-------------|
| FastAPI | Modern, async, type hints | Flask, Django |
| ChromaDB | Local, simple, persistent | Weaviate, Milvus |
| sentence-transformers | Fast, FOSS, no API key | OpenAI embeddings |
| Ollama | Local inference, privacy | vLLM, LM Studio |
| watchdog | Event-driven, efficient | polling os.walk() |

---

## Questions Claude Might Ask

**Q: Where should I add caching?**
A: See Performance section in ARCHITECTURE.md. Best place: `search()` endpoint or ChromaDB queries.

**Q: How do I handle large documents?**
A: Adjust chunk_size and chunk_overlap in utils/loader.py. Larger chunks = fewer queries but less precision.

**Q: Can I use different embedding models?**
A: Yes, change HuggingFaceEmbeddings model_name in rag_mcp_server.py:32. Must rebuild index after change.

**Q: How do I add authentication?**
A: Add FastAPI dependency in routes. See CODE_AUDIT.md P0 recommendations.

**Q: Can this scale to 1M documents?**
A: Technically yes (ChromaDB supports it), but would need incremental indexing (TODO).

---

## Learning Resources

- **RAG Pattern**: https://docs.anthropic.com/en/docs/build-a-rag-chatbot
- **FastAPI**: https://fastapi.tiangolo.com
- **ChromaDB**: https://docs.trychroma.com
- **Ollama**: https://ollama.ai
- **LangChain**: https://python.langchain.com

---

**Context Version**: 1.0
**Last Updated**: October 22, 2025
**For Claude**: Use this + CLAUDE_GUIDE.md to get started quickly
