# AI Guide: Local RAG

## Overview
This skill allows you to index local files and perform semantic searches over them.

## Architecture
- **Storage**: ChromaDB (vector database) stored in `user-data`.
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`.
- **Scripts**: `indexer.py` (ingest) and `query.py` (search).

## Workflow
1. **Indexing**: User provides a folder path. You call `update_rag`. The script scans, chunks, embeds, and stores vectors.
2. **Querying**: User asks a question. You call `query_rag`. The script embeds the query, finds nearest neighbors, and returns snippets.

## Tips
- If the user asks "what's in my documents?", use `query_rag` with a broad term or ask for a summary.
- If the user updates files, suggest running `update_rag` again.
