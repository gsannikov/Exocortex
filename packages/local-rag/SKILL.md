---
name: local-rag
description: Index local folders and query them using RAG (Retrieval Augmented Generation). Supports PDF, DOCX, PPTX, XLSX, images with OCR, and text files.
---

# 🧠 Local RAG

Index and semantically search your local documents using embeddings and ChromaDB.

## 🌟 Capabilities

1. **Index Local Folders**: Scan and embed documents from any directory
2. **Multi-Format Support**: PDF, DOCX, PPTX, XLSX, TXT, MD, code files, images
3. **OCR Support**: Extract text from scanned PDFs and images
4. **Semantic Search**: Find relevant content by meaning, not just keywords
5. **Persistent Index**: Embeddings stored locally in ChromaDB
6. **Incremental Updates**: Only re-index changed files

## 🚀 Commands

| Command | Action |
|---------|--------|
| `update rag from [path]` | Index files in the specified folder |
| `query rag [question]` | Search the indexed documents |
| `search documents [query]` | Alternative search command |

## 📄 Supported File Types

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
- **Python** (`.py`)
- **JavaScript** (`.js`)
- **TypeScript** (`.ts`)
- **HTML/CSS** (`.html`, `.css`)
- **C/C++** (`.c`, `.cpp`, `.h`)
- **Shell** (`.sh`)

### Images (with OCR)
- **PNG** (`.png`)
- **JPEG** (`.jpg`, `.jpeg`)
- **TIFF** (`.tiff`)
- **WebP** (`.webp`)

## 🛠️ Tools

### `update_rag`
Index a directory of documents.

**Parameters:**
- `path`: Absolute path to the directory to index

**Example:**
```
update rag from ~/Documents/research
```

**Behavior:**
- Scans directory recursively
- Skips files larger than 10MB
- Uses file hashing for change detection
- Only re-indexes modified files

### `query_rag`
Search the indexed knowledge base.

**Parameters:**
- `query`: Natural language question or search terms
- `k`: Number of results (default: 5)

**Example:**
```
query rag what are the key findings about climate change?
```

**Output:**
- Ranked list of relevant document chunks
- File paths and names
- Relevance scores (0-1)
- Text previews

## ⚙️ Configuration

### User Data Location
```
~/MyDrive/claude-skills-data/local-rag/
├── chromadb/           # Vector database storage
└── state/
    └── ingest_state.json  # File tracking state
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `OCR_ENABLED` | `true` | Enable OCR for images/scanned PDFs |
| `OCR_MAX_PAGES` | `120` | Max pages to OCR per PDF |
| `OCR_PAGE_DPI` | `200` | DPI for PDF-to-image conversion |

### Embedding Model
Uses `sentence-transformers/all-MiniLM-L6-v2` for:
- Fast embedding generation
- Good semantic similarity
- Small memory footprint (~90MB)

### Chunking Strategy
- **Chunk Size**: 3000 characters
- **Overlap**: 400 characters
- Ensures context preservation across chunk boundaries

## 📊 Example Workflows

### Index a Research Folder
```
User: update rag from ~/Documents/research-papers
Claude: Scanning ~/Documents/research-papers...
        Found 47 PDF files, 12 markdown files
        Indexing complete. Processed 59 files (1,247 chunks).
```

### Search for Information
```
User: query rag neural network training techniques
Claude: Found 5 relevant results:

1. deep-learning-survey.pdf (score: 0.89)
   "...backpropagation remains the primary training algorithm..."

2. optimization-methods.md (score: 0.84)
   "...Adam optimizer combines momentum with adaptive learning..."
```

### Incremental Update
```
User: update rag from ~/Documents/research-papers
Claude: Scanning for changes...
        3 files modified since last index
        Indexing complete. Processed 3 files.
```

## 🔧 Requirements

### Python Dependencies
```
chromadb>=0.4.0
sentence-transformers>=2.2.0
rapidfuzz>=3.0.0
python-dotenv>=1.0.0
pypdf>=3.0.0
pdf2image>=1.16.0
Pillow>=9.0.0
python-docx>=0.8.11
python-pptx>=0.6.21
openpyxl>=3.0.0
```

### System Dependencies (for OCR)
- **poppler-utils**: PDF to image conversion
- **tesseract-ocr**: OCR engine

Install on macOS:
```bash
brew install poppler tesseract
```

Install on Ubuntu:
```bash
sudo apt install poppler-utils tesseract-ocr
```

## 🚨 Limitations

- Files larger than 10MB are skipped
- OCR quality depends on document scan quality
- Initial indexing of large directories may take several minutes
- Embedding model download required on first run (~90MB)

## 📁 Project Structure

```
local-rag/
├── SKILL.md              # This file
├── AI_GUIDE.md           # AI assistant guide
├── README.md             # Quick intro
├── CHANGELOG.md          # Version history
├── version.yaml          # Version info
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── indexer.py        # Document indexing
│   ├── query.py          # Search functionality
│   └── ingest/
│       ├── extractor.py  # File content extraction
│       ├── ocr.py        # OCR processing
│       └── utils.py      # Utilities
├── tests/                # Test suite
└── docs/                 # Additional documentation
```
