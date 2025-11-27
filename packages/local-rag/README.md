# 🧠 Local RAG

Hybrid semantic + keyword search over your local documents using embeddings, BM25, and ChromaDB/Qdrant.

## Features

- **Hybrid Search**: Combines vector similarity and BM25 keyword search for best results
- **Multi-Format Support**: PDF, DOCX, PPTX, XLSX, TXT, MD, code files, images
- **Smart Chunking**: 4 strategies (fixed, sentence, semantic, template)
- **OCR Support**: Extract text from scanned PDFs and images
- **Multiple Vector Stores**: ChromaDB (default) or Qdrant
- **Cross-Encoder Reranking**: Optional precision boost for top results
- **Persistent Storage**: Local vector database + BM25 index
- **Incremental Updates**: Only re-index changed files

## Usage

### Index a folder
```bash
python scripts/indexer.py ~/Documents/research --user-data-dir ~/rag-data
```

### Query the database
```bash
python scripts/query.py "neural network training" --user-data-dir ~/rag-data
```

### Hybrid search with options
```bash
python scripts/query.py "machine learning" --user-data-dir ~/rag-data \
  --method hybrid \
  --vector-weight 0.7 \
  --bm25-weight 0.3 \
  -k 10
```

### Visualize chunking
```bash
python scripts/visualize.py document.md --strategy template --compare
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
- **Word** (`.docx`) - Full document text extraction
- **PowerPoint** (`.pptx`) - Slide text extraction
- **Excel** (`.xlsx`) - Cell content extraction

### Text Files
- **Markdown** (`.md`)
- **Plain Text** (`.txt`)
- **JSON/YAML** (`.json`, `.yaml`, `.yml`)

### Code Files
- Python, JavaScript, TypeScript, HTML, CSS, C/C++, Shell

### Images (with OCR)
- PNG, JPEG, TIFF, WebP

## Configuration

### Storage Location
```
~/MyDrive/claude-skills-data/local-rag/
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
| `OCR_MAX_PAGES` | `120` | Max pages to OCR |
| `OCR_PAGE_DPI` | `200` | DPI for OCR |

### Embedding Model
Uses `sentence-transformers/all-MiniLM-L6-v2`:
- 384-dimensional embeddings
- Fast CPU inference
- Good semantic similarity
- Small memory footprint (~90MB)

## Requirements

### Python Dependencies
```
chromadb>=0.4.0
sentence-transformers>=2.2.0
rapidfuzz>=3.0.0
pypdf>=3.0.0
python-docx>=0.8.11
openpyxl>=3.0.0
# Optional: qdrant-client>=1.7.0
```

### System Dependencies (for OCR)
```bash
# macOS
brew install poppler tesseract

# Ubuntu
sudo apt install poppler-utils tesseract-ocr
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
