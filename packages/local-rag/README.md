# 🧠 Local RAG

Hybrid semantic + keyword search over your local documents using embeddings, BM25, and ChromaDB/Qdrant.

## Features

- **Hybrid Search**: Combines vector similarity and BM25 keyword search for best results
- **Multi-Format Support**: PDF, DOCX, PPTX, XLSX, TXT, MD, code files, images
- **Smart Chunking**: 4 strategies (fixed, sentence, semantic, template)
- **OCR Support**: Extract text from scanned PDFs and images (PaddleOCR with Hebrew support)
- **Multiple Vector Stores**: ChromaDB (default) or Qdrant
- **Cross-Encoder Reranking**: Optional precision boost for top results
- **Persistent Storage**: Local vector database + BM25 index
- **Incremental Updates**: Only re-index changed files

## Quickstart (Docker - Recommended)

```bash
# From repo root
cd packages/local-rag

# Run the wrapper script (builds image automatically)
./run_mcp_docker.sh

# The MCP server is configured in claude.desktop.mcp.json to use this script.
# Just restart Claude Desktop and use the tools!
```

## Quickstart (Local Python)

```bash
# From repo root
python3.11 -m pip install --user ./packages/local-rag

# Add user bin to PATH so console scripts are available
export PATH="$HOME/Library/Python/3.11/bin:$PATH"

# Index a folder
local-rag index ~/Documents/research --user-data-dir ~/rag-data

# Query it
local-rag query "neural network training" --user-data-dir ~/rag-data
```

## Usage

### Index a folder
```bash
local-rag index ~/Documents/research --user-data-dir ~/rag-data
```

Optional flags:
- `--parallel 6` to enable multithreaded ingestion on Apple silicon
- `--include "*.md" "*.pdf"` / `--exclude "archive/**"` to control scope
- `--max-errors 10` to abort early on systemic failures

### Query the database
```bash
local-rag query "neural network training" --user-data-dir ~/rag-data
```

### Hybrid search with options
```bash
local-rag query "machine learning" --user-data-dir ~/rag-data \
  --method hybrid \
  --vector-weight 0.7 \
  --bm25-weight 0.3 \
  -k 10
```

### Visualize chunking
```bash
local-rag visualize document.md --strategy template --compare
```

## Chunking Strategies

| Strategy | Best For | Description |
|----------|----------|-------------|
| `fixed` | Simple documents | Character-based with overlap |
| `sentence` | Prose, articles | Respects sentence boundaries |
| `semantic` | Research papers | Groups by embedding similarity |
| `template` | Markdown, code | Document-structure aware |

## Search Methods

| Method | Description |
|--------|-------------|
| `vector` | Pure semantic similarity search |
| `bm25` | Keyword matching with IDF weighting |
| `hybrid` | RRF fusion of both (default, best recall) |

## Supported File Types

### Documents
- **PDF** (`.pdf`) - Native text extraction + OCR fallback
- **Word** (`.docx`, `.doc`) - Full document text extraction
- **PowerPoint** (`.pptx`) - Slide text extraction
- **Excel** (`.xlsx`) - Cell content extraction

### Text Files
- **Markdown** (`.md`, `.mdx`, `.mdc`)
- **Plain Text** (`.txt`)
- **JSON/YAML** (`.json`, `.jsonc`, `.yaml`, `.yml`)

### Code Files
- **Python** (`.py`)
- **JavaScript/TypeScript** (`.js`, `.ts`, `.tsx`, `.jsx`)
- **Web** (`.html`, `.xhtml`, `.css`, `.scss`)
- **Systems** (`.c`, `.cpp`, `.h`, `.hpp`, `.sh`)
- **Modern** (`.swift`, `.go`, `.rs`, `.java`)

### Images (with OCR)
- PNG, JPEG, TIFF, WebP

### Excluded Directories
The indexer automatically skips:
- `.git`, `.svn`, `.hg` (version control)
- `node_modules`, `__pycache__` (dependencies)
- `.venv`, `venv`, `env` (Python environments)
- `.idea`, `.vscode` (IDE configs)
- `dist`, `build`, `.next` (build outputs)

## Configuration

### Storage Location
```
~/Library/Application Support/local-rag/   # macOS default
~/.local-rag-data                          # other platforms (default)
├── vectordb/              # Vector database (ChromaDB/Qdrant)
└── state/
    ├── ingest_state.json  # File tracking
    └── bm25_index.json    # BM25 inverted index
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHUNK_SIZE` | `3000` | Characters per chunk |
| `CHUNK_OVERLAP` | `400` | Overlap between chunks |
| `CHUNKING_STRATEGY` | `template` | Chunking strategy |
| `VECTOR_STORE` | `chroma` | Vector store backend |
| `SEARCH_METHOD` | `hybrid` | Search method |
| `VECTOR_WEIGHT` | `0.7` | Vector search weight |
| `BM25_WEIGHT` | `0.3` | BM25 search weight |
| `USE_RERANKER` | `false` | Enable cross-encoder |
| `OCR_ENABLED` | `true` | Enable OCR |
| `OCR_ENGINE` | `paddle` | OCR engine (paddle, surya, deepseek) |
| `OCR_LANG` | `en,he` | OCR language(s) |
| `OCR_MAX_PAGES` | `120` | Max pages to OCR |
| `OCR_PAGE_DPI` | `200` | DPI for OCR |
| `CHUNK_MIN_ENTROPY` | `0.0` | Drop chunks with entropy below this |
| `CHUNK_MIN_CHARS` | `40` | Drop chunks shorter than this before embedding |
| `CHUNK_STRIP_CONTROL` | `true` | Remove control characters before embedding |
| `OCR_CACHE_DIR` | `~/.cache/local-rag/ocr_cache` | Cache OCR outputs |
| `LOCAL_RAG_PARALLEL` | `6` | Default worker count for indexing |
| `LOCAL_RAG_MAX_ERRORS` | `20` | Stop indexing after this many errors |

### Embedding Model
Uses `sentence-transformers/all-MiniLM-L6-v2`:
- 384-dimensional embeddings
- Fast CPU inference
- Good semantic similarity
- Small memory footprint (~90MB)

## Installation

### 1. Python Dependencies
```bash
cd packages/local-rag
python3.11 -m pip install --user .

# If you want isolation without managing a venv yourself:
# pipx install .
# or
# uv pip install --user .

# Using pyenv for Python 3.11
# pyenv shell 3.11
# python -m pip install --user .
```

Core packages installed:
- `chromadb` - Vector database
- `sentence-transformers` - Embedding model
- `rapidfuzz` - Fuzzy string matching
- `pypdf`, `pdf2image` - PDF processing
- `python-docx`, `python-pptx`, `openpyxl` - Office documents
- `paddleocr`, `paddlepaddle` - OCR engine (default, multi-language)

### 2. System Dependencies (for PDF/OCR)
```bash
# macOS
brew install poppler antiword

# Ubuntu/Debian
sudo apt install poppler-utils antiword
```

### 3. Optional: Alternative OCR Engines

**Surya** (lighter weight, English-focused):
```bash
pip install surya-ocr
export OCR_ENGINE=surya
```

**DeepSeek-OCR** (highest accuracy, requires API):
```bash
export OCR_ENGINE=deepseek
export DEEPSEEK_OCR_URL=http://localhost:8000/v1/completions
export DEEPSEEK_OCR_MODEL=deepseek-vl
```

### 4. Optional: Qdrant Vector Store
```bash
pip install qdrant-client
export VECTOR_STORE=qdrant
```

### 5. Optional: Legacy .doc Support
```bash
# Requires antiword (see system dependencies above)
pip install textract
```

## Performance

- **Indexing**: ~100 chunks/second
- **Search**: <150ms for hybrid search over 10k documents
- **With reranking**: ~300ms additional
- **Scale**: Tested up to 100k documents

## Limitations

- Files larger than 10MB are skipped
- OCR quality depends on document scan quality
- Initial indexing of large directories may take several minutes
- Embedding model download required on first run (~90MB)

## Documentation

- [SKILL.md](SKILL.md) - Full skill documentation
- [docs/architecture.md](docs/architecture.md) - Technical architecture
- [docs/agent-guide.md](docs/agent-guide.md) - AI assistant guide
