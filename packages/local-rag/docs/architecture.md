# Architecture

## Overview

2ndBrain_RAG is a local-first RAG (Retrieval-Augmented Generation) system that provides semantic search and context-aware retrieval over a local document collection. The system is designed to run entirely offline (after initial model downloads) and integrates with Claude Desktop via the Model Context Protocol (MCP).

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Desktop/Code                      │
│                    (MCP Client)                              │
└──────────────────────┬──────────────────────────────────────┘
                       │ MCP Protocol
                       │ (JSON-RPC over stdio)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Layer                          │
│                   (mcp_server.py)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tools: search, get, reindex, stats, invalidate      │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────┬──────────────────┬──────────────────────────────┘
            │                  │
            ▼                  ▼
┌─────────────────┐   ┌──────────────────┐
│  File Watcher   │   │  Ingestion       │
│  (watchdog)     │   │  Pipeline        │
│                 │   │                  │
│  • Monitors     │   │  • Text Extract  │
│    ROOT_DIR     │   │  • OCR           │
│  • Auto-reindex │   │  • Chunking      │
│    on changes   │   │  • Embedding     │
└────────┬────────┘   └────────┬─────────┘
         │                     │
         └──────────┬──────────┘
                    ▼
         ┌──────────────────────┐
         │   Vector Database    │
         │    (ChromaDB)        │
         │                      │
         │  • Persistent        │
         │  • Cosine Similarity │
         │  • HNSW Index        │
         └──────────────────────┘
                    ▲
                    │
         ┌──────────┴──────────┐
         │   Embedding Model   │
         │  sentence-transformers│
         │  all-MiniLM-L6-v2   │
         └─────────────────────┘
```

## System Components

### 1. MCP Server (`mcp_server.py`)

**Purpose**: Main entry point and MCP protocol implementation

**Key Responsibilities**:
- Expose RAG capabilities via MCP tools
- Manage ChromaDB client lifecycle
- Coordinate file watching and ingestion
- Handle tool requests from Claude

**MCP Tools Exposed**:
- `rag.search` - Semantic search over documents
- `rag.get` - Retrieve specific document excerpts
- `rag.reindex` - Trigger manual reindexing
- `rag.stats` - Get index statistics
- `rag.invalidate` - Remove documents from index

### 2. Ingestion Pipeline (`ingest/`)

**Purpose**: Extract and process documents for indexing

**Components**:

#### `extractor.py`
- Extract text from various file formats
- Delegate to OCR when needed
- Handle encoding and format detection

**Supported Formats**:
- PDF (text-based and scanned)
- Office documents (DOCX, PPTX, XLSX)
- Markdown, plain text
- Images (via OCR)

#### `ocr.py`
- Optical Character Recognition for scanned documents
- Multiple OCR engine support:
  - **Surya** (default, CPU-friendly)
  - **PaddleOCR** (optional)
  - **DeepSeek-OCR** (optional, high accuracy)
- Configurable DPI for quality/performance trade-off

#### `utils.py`
- Helper utilities for text processing
- File type detection
- Path normalization

### 3. Vector Database (ChromaDB)

**Purpose**: Persistent vector storage and similarity search

**Configuration**:
- **Distance Metric**: Cosine similarity
- **Index Type**: HNSW (Hierarchical Navigable Small World)
- **Persistence**: Local filesystem (`.chromadb/`)
- **Collection**: Single collection "docs"

**Document Schema**:
```python
{
  "id": "path:/file/path::offset:start-end",
  "embedding": [768-dim vector],
  "metadata": {
    "path": "/absolute/file/path",
    "start": chunk_start_offset,
    "end": chunk_end_offset,
    "mtime": file_modification_time
  },
  "document": "chunk text content"
}
```

### 4. File Watcher

**Purpose**: Automatically detect and reindex changed documents

**Technology**: `watchdog` library

**Behavior**:
- Monitors `ROOT_DIR` recursively
- Triggers on: create, modify, delete events
- Filters by `ALLOWED_EXTS`
- Debounces rapid changes

### 5. Embedding Model

**Default**: `sentence-transformers/all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Fast CPU inference
- Good balance of speed and accuracy

**Alternatives** (configurable via `EMBED_MODEL`):
- `all-mpnet-base-v2` - Higher accuracy, slower
- `all-distilroberta-v1` - Balanced option

## Data Flow

### Indexing Flow

```
1. File Change Detected (or manual trigger)
   ↓
2. Load file from disk
   ↓
3. Extract text (extractor.py)
   ├─ Text file → Direct read
   ├─ PDF → pypdf or OCR
   └─ Image → OCR
   ↓
4. Chunk text (CHUNK_SIZE, CHUNK_OVERLAP)
   ↓
5. Generate embeddings (batch)
   ↓
6. Upsert to ChromaDB
   ↓
7. Update state tracking (state/ingest_state.json)
```

### Search Flow

```
1. Claude calls rag.search via MCP
   ↓
2. Embed query text
   ↓
3. Query ChromaDB (cosine similarity)
   ↓
4. Retrieve top-k results
   ↓
5. Format results with metadata
   ↓
6. Return to Claude
```

### Retrieval Flow

```
1. Claude calls rag.get with path and offset
   ↓
2. Open file at path
   ↓
3. Seek to offset
   ↓
4. Read specified byte range
   ↓
5. Return text window
```

## Performance Characteristics

### Indexing Performance
- **Small files** (<1MB): ~0.1-0.5s per file
- **Large PDFs** (10-100MB): ~2-10s per file
- **OCR**: ~1-5s per page (depends on DPI, engine)
- **Batch embedding**: ~100 chunks/second

### Search Performance
- **Query latency**: <100ms for <10k documents
- **Scales to**: ~100k documents before noticeable slowdown
- **Memory usage**: ~50MB base + 1MB per 1000 documents

### Resource Requirements
- **CPU**: Modern multi-core processor
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB per 10k documents (varies with content)
- **GPU**: Optional (not used by default)

## Scalability Considerations

### Current Limitations
- Single-threaded ingestion
- Full reindex on file change (no incremental updates)
- In-memory embeddings during indexing
- No distributed architecture

### Scaling Strategies

**For larger corpora (>10GB)**:
1. Use Qdrant or Weaviate for vector DB
2. Implement incremental indexing
3. Add hybrid search (BM25 + vectors)
4. Batch processing with queues

**For multiple users**:
1. Add API layer (FastAPI)
2. Implement authentication
3. Add rate limiting
4. Use Redis for caching

## Security Model

**Current State**: Development/personal use only

**Security Assumptions**:
- Trusted local environment
- Single user
- No network exposure
- Trusted document sources

**Production Considerations**:
- Add input validation
- Sanitize file paths
- Implement access controls
- Add audit logging

## Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ROOT_DIR` | `.` | Documents folder to index |
| `ALLOWED_EXTS` | `.pdf,.txt,.md` | File extensions to process |
| `CHUNK_SIZE` | `3000` | Characters per chunk |
| `CHUNK_OVERLAP` | `400` | Overlap between chunks |
| `PERSIST_DIR` | `.chromadb` | ChromaDB storage path |
| `EMBED_MODEL` | `all-MiniLM-L6-v2` | Embedding model name |

### Tuning Guidelines

**For better accuracy**:
- Decrease `CHUNK_SIZE` (more granular)
- Increase `k` in search
- Use larger embedding model

**For better performance**:
- Increase `CHUNK_SIZE` (fewer chunks)
- Decrease `CHUNK_OVERLAP`
- Use smaller/faster embedding model

**For OCR quality**:
- Increase DPI (200 → 300)
- Use DeepSeek-OCR instead of Surya
- Pre-process images (deskew, denoise)

## Deployment Architecture

### Local Development
```
User Machine
├─ Claude Desktop
├─ MCP Server (Python process)
└─ ChromaDB (local filesystem)
```

### Production (Future)
```
Load Balancer
    ↓
API Servers (FastAPI)
    ↓
Message Queue (RabbitMQ)
    ↓
Worker Pool (Celery)
    ↓
Vector DB (Qdrant/Weaviate)
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Protocol | MCP | Claude integration |
| Language | Python 3.11+ | Implementation |
| Vector DB | ChromaDB | Storage & search |
| Embeddings | sentence-transformers | Vector generation |
| OCR | Surya/PaddleOCR | Image text extraction |
| File Watching | watchdog | Change detection |
| PDF | pypdf, pdfplumber | PDF parsing |
| Office | python-docx, openpyxl | Office formats |

## Design Principles

1. **Local-first**: No cloud dependencies after setup
2. **Privacy**: Documents never leave the machine
3. **Simplicity**: Minimal dependencies, clear code
4. **Performance**: Fast enough for personal use (not enterprise)
5. **Extensibility**: Easy to add new file formats, OCR engines
6. **Reliability**: Crash-safe state tracking

## Future Improvements

See [roadmap.md](roadmap.md) for detailed plans.

**Architecture Evolution**:
- Incremental indexing
- Multi-user support via API
- Distributed architecture
- Real-time collaboration
- Advanced query DSL
- Hybrid search (BM25 + semantic)
