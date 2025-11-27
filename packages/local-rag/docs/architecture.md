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
┌─────────────────┐   ┌──────────────────────────────────────┐
│  File Watcher   │   │       Ingestion Pipeline              │
│  (watchdog)     │   │                                       │
│                 │   │  ┌─────────────┐  ┌───────────────┐  │
│  • Monitors     │   │  │ Extractor   │  │   Chunking    │  │
│    ROOT_DIR     │   │  │             │  │   Module      │  │
│  • Auto-reindex │   │  │ • Text      │  │               │  │
│    on changes   │   │  │ • PDF/OCR   │  │ • Fixed       │  │
│                 │   │  │ • Office    │  │ • Sentence    │  │
│                 │   │  │ • Images    │  │ • Semantic    │  │
│                 │   │  └─────────────┘  │ • Template    │  │
│                 │   │                   └───────────────┘  │
└────────┬────────┘   └──────────────┬───────────────────────┘
         │                           │
         └──────────┬────────────────┘
                    ▼
┌───────────────────────────────────────────────────────────┐
│                    Search Layer                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Hybrid Searcher                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │  │
│  │  │ Vector Search│  │ BM25 Search  │  │ Reranker  │  │  │
│  │  │ (semantic)   │  │ (keyword)    │  │ (optional)│  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘  │  │
│  │         └────────┬────────┘                │        │  │
│  │                  ▼                         │        │  │
│  │         ┌───────────────┐                  │        │  │
│  │         │ Result Fusion │◄─────────────────┘        │  │
│  │         │ (RRF/Weighted)│                           │  │
│  │         └───────────────┘                           │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────┬──────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌──────────────────────┐      ┌──────────────────────┐
│   Vector Database    │      │    BM25 Index        │
│   (Abstraction)      │      │   (bm25_index.json)  │
│                      │      │                      │
│  ┌────────────────┐  │      │  • Inverted index    │
│  │   ChromaDB     │  │      │  • IDF weighting     │
│  │   (default)    │  │      │  • Tokenization      │
│  └────────────────┘  │      │  • Stopword removal  │
│  ┌────────────────┐  │      └──────────────────────┘
│  │    Qdrant      │  │
│  │   (optional)   │  │
│  └────────────────┘  │
└──────────────────────┘
         ▲
         │
┌────────┴───────────┐
│   Embedding Model  │
│ sentence-transformers│
│ all-MiniLM-L6-v2   │
│ (384-dimensional)  │
└────────────────────┘
```

## System Components

### 1. MCP Server (`mcp_server.py`)

**Purpose**: Main entry point and MCP protocol implementation

**Key Responsibilities**:
- Expose RAG capabilities via MCP tools
- Manage vector database client lifecycle
- Coordinate file watching and ingestion
- Handle tool requests from Claude

**MCP Tools Exposed**:
- `rag.search` - Hybrid semantic + keyword search over documents
- `rag.get` - Retrieve specific document excerpts
- `rag.reindex` - Trigger manual reindexing
- `rag.stats` - Get index statistics
- `rag.invalidate` - Remove documents from index

### 2. Chunking Module (`chunking.py`)

**Purpose**: Split documents into searchable chunks using configurable strategies

**Strategies Available**:

| Strategy | Description | Best For |
|----------|-------------|----------|
| `fixed` | Character-based with overlap | Simple documents, code |
| `sentence` | Respects sentence boundaries | Prose, articles |
| `semantic` | Groups by embedding similarity | Research papers |
| `template` | Document-type aware (headers, code blocks) | Markdown, code files |

**Key Classes**:
- `FixedChunker` - Simple character-based chunking
- `SentenceChunker` - Sentence boundary aware
- `SemanticChunker` - Embedding similarity based
- `TemplateChunker` - Document structure aware

**Configuration**:
- `CHUNK_SIZE` (default: 3000) - Maximum characters per chunk
- `CHUNK_OVERLAP` (default: 400) - Overlap between chunks
- `CHUNKING_STRATEGY` (default: template) - Strategy to use

### 3. Ingestion Pipeline (`ingest/`)

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
- Code files (Python, JavaScript, etc.)
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

### 4. Search Module (`search.py`)

**Purpose**: Hybrid search combining vector similarity and keyword matching

**Components**:

#### BM25Index
- Okapi BM25 implementation for keyword search
- Inverted index with IDF weighting
- Stopword removal and tokenization
- Persistence to JSON

#### HybridSearcher
- Combines vector and BM25 search results
- Configurable fusion methods:
  - **RRF** (Reciprocal Rank Fusion) - default
  - **Weighted** - configurable weights per source
  - **Max** - take best score from either
- Optional cross-encoder reranking

**Configuration**:
- `SEARCH_METHOD` - "vector", "bm25", or "hybrid"
- `VECTOR_WEIGHT` (default: 0.7) - Weight for vector results
- `BM25_WEIGHT` (default: 0.3) - Weight for BM25 results
- `USE_RERANKER` (default: false) - Enable cross-encoder

### 5. Vector Store Abstraction (`vectorstore.py`)

**Purpose**: Unified interface for different vector databases

**Supported Backends**:

| Backend | Type | Best For |
|---------|------|----------|
| ChromaDB | Local | Development, personal use |
| Qdrant | Local/Cloud | Scaling, production |

**BaseVectorStore Interface**:
```python
class BaseVectorStore:
    def add_documents(ids, texts, embeddings, metadatas)
    def delete_documents(ids=None, where=None)
    def search(query_embedding, k=10, where=None)
    def get_documents(ids)
    def count()
    def clear()
```

**Configuration**:
- `VECTOR_STORE` - "chroma" or "qdrant"
- `QDRANT_URL` - Qdrant server URL (optional)
- `QDRANT_API_KEY` - Qdrant API key (optional)

### 6. Document Indexer (`indexer.py`)

**Purpose**: Orchestrate document processing and indexing

**Key Features**:
- Configurable chunking strategy
- Vector store backend selection
- BM25 index building
- Incremental updates via file hashing
- State persistence

**CLI Options**:
```bash
python indexer.py ~/Documents --user-data-dir ~/rag-data \
  --strategy template \
  --store chroma \
  --chunk-size 3000 \
  --chunk-overlap 400 \
  --force
```

### 7. Document Searcher (`query.py`)

**Purpose**: Query interface for document retrieval

**Key Features**:
- Hybrid search (vector + BM25)
- Optional cross-encoder reranking
- Metadata filtering
- JSON output format

**CLI Options**:
```bash
python query.py "search query" --user-data-dir ~/rag-data \
  --method hybrid \
  --vector-weight 0.7 \
  --bm25-weight 0.3 \
  --rerank \
  -k 10
```

### 8. Chunk Visualizer (`visualize.py`)

**Purpose**: Debug and compare chunking strategies

**Features**:
- Visual output with colored boundaries
- JSON export for programmatic use
- Statistics (counts, sizes, overlap)
- Strategy comparison mode

**CLI Options**:
```bash
python visualize.py document.md --strategy template --compare
python visualize.py document.md -f json
python visualize.py document.md -f stats
```

### 9. File Watcher

**Purpose**: Automatically detect and reindex changed documents

**Technology**: `watchdog` library

**Behavior**:
- Monitors `ROOT_DIR` recursively
- Triggers on: create, modify, delete events
- Filters by `ALLOWED_EXTS`
- Debounces rapid changes

### 10. Embedding Model

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
4. Chunk text (chunking.py)
   ├─ Fixed: character-based
   ├─ Sentence: boundary-aware
   ├─ Semantic: similarity-based
   └─ Template: structure-aware
   ↓
5. Generate embeddings (batch)
   ↓
6. Upsert to Vector Store (ChromaDB/Qdrant)
   ↓
7. Update BM25 Index (bm25_index.json)
   ↓
8. Update state tracking (ingest_state.json)
```

### Search Flow

```
1. Claude calls rag.search via MCP
   ↓
2. Parse query and parameters
   ↓
3. Parallel retrieval:
   ├─ Vector: Embed query → cosine similarity
   └─ BM25: Tokenize → inverted index lookup
   ↓
4. Fuse results (RRF/Weighted/Max)
   ↓
5. Optional: Cross-encoder reranking
   ↓
6. Format results with metadata
   ↓
7. Return to Claude
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
- **Hybrid search**: ~150ms (vector + BM25 + fusion)
- **With reranking**: ~300ms additional
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
- Full reindex on file change (no incremental chunk updates)
- In-memory embeddings during indexing
- No distributed architecture

### Scaling Strategies

**For larger corpora (>10GB)**:
1. Use Qdrant (via `--store qdrant`)
2. Enable hybrid search for better recall
3. Use template chunking for better precision
4. Increase chunk size for fewer total chunks

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
| `CHUNKING_STRATEGY` | `template` | Chunking strategy |
| `VECTOR_STORE` | `chroma` | Vector database backend |
| `PERSIST_DIR` | `.chromadb` | Vector store path |
| `EMBED_MODEL` | `all-MiniLM-L6-v2` | Embedding model name |
| `SEARCH_METHOD` | `hybrid` | Search method |
| `VECTOR_WEIGHT` | `0.7` | Vector search weight |
| `BM25_WEIGHT` | `0.3` | BM25 search weight |
| `USE_RERANKER` | `false` | Enable cross-encoder |

### Tuning Guidelines

**For better accuracy**:
- Use `template` or `sentence` chunking
- Enable hybrid search
- Enable reranking for top-k
- Decrease `CHUNK_SIZE` (more granular)
- Use larger embedding model

**For better performance**:
- Use `fixed` chunking
- Disable BM25 (vector-only)
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
├─ ChromaDB (local filesystem)
└─ BM25 Index (JSON file)
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
Vector DB (Qdrant Cloud)
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Protocol | MCP | Claude integration |
| Language | Python 3.11+ | Implementation |
| Vector DB | ChromaDB/Qdrant | Storage & search |
| Embeddings | sentence-transformers | Vector generation |
| Keyword Search | BM25 (custom) | Sparse retrieval |
| Reranking | cross-encoder | Result refinement |
| OCR | Surya/PaddleOCR | Image text extraction |
| File Watching | watchdog | Change detection |
| PDF | pypdf, pdfplumber | PDF parsing |
| Office | python-docx, openpyxl | Office formats |

## Design Principles

1. **Local-first**: No cloud dependencies after setup
2. **Privacy**: Documents never leave the machine
3. **Simplicity**: Minimal dependencies, clear code
4. **Performance**: Fast enough for personal use (not enterprise)
5. **Extensibility**: Easy to add new file formats, OCR engines, vector stores
6. **Reliability**: Crash-safe state tracking
7. **Flexibility**: Multiple chunking/search strategies for different use cases

## Future Improvements

See [roadmap.md](roadmap.md) for detailed plans.

**Architecture Evolution**:
- Incremental chunk indexing
- Multi-user support via API
- Distributed architecture
- Real-time collaboration
- Advanced query DSL
- Query expansion and rewriting
- Multi-modal search (images with CLIP)
