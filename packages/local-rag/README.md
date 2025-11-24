# 🧠 Local RAG

Index and search your local documents using semantic search.

## Features
- **Index Local Folders**: Automatically scan and embed documents (PDF, TXT, MD, code files)
- **Semantic Search**: Find relevant content based on meaning, not just keywords
- **Persistent Storage**: ChromaDB vector database stored in user-data

## Usage

### Index a folder
```
update rag from /path/to/your/documents
```

### Query the database
```
query rag how do I implement authentication?
```

## Supported File Types
- PDF, TXT, MD
- Python, JavaScript, HTML, CSS, JSON, YAML

## Storage
Data is stored in `~/MyDrive/claude-skills-data/local-rag/`

## Requirements
See `requirements.txt` for dependencies.
