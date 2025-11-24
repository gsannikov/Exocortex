---
name: local-rag
description: Index local folders and query them using RAG (Retrieval Augmented Generation). Commands - "update rag from [folder]", "query rag [question]".
---

# 🧠 Local RAG

Index and search your local documents.

## 🌟 Capabilities
1. **Index Local Folders**: Scan and embed documents (PDF, TXT, MD, Code).
2. **Semantic Search**: Find relevant snippets based on meaning, not just keywords.
3. **Persistent Index**: Stores embeddings in `user-data/local-rag/chromadb`.

## 🚀 Commands

| Command | Action |
|---------|--------|
| `update rag from [path]` | Index files in the specified folder |
| `query rag [question]` | Search the database |

## 🛠️ Tools

### `update_rag`
Index a directory of documents.

- **path**: Absolute path to the directory to index.

```python
def update_rag(path):
    """
    Index files in the specified directory.
    """
    return run_script("indexer.py", [path, "--user-data-dir", USER_DATA_DIR])
```

### `query_rag`
Search the knowledge base.

- **query**: The question or topic to search for.

```python
def query_rag(query):
    """
    Search for relevant documents.
    """
    return run_script("query.py", [query, "--user-data-dir", USER_DATA_DIR])
```

## ⚙️ Configuration

**User Data Location**: `~/MyDrive/claude-skills-data/local-rag/`
