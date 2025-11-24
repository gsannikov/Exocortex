#!/usr/bin/env python3
"""
Indexer script for Local RAG.
Scans a directory and indexes supported files into ChromaDB.
"""

import os
import sys
import hashlib
import json
import argparse
from pathlib import Path
from typing import List, Generator, Tuple

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from ingest.extractor import read_text_with_ocr as read_text

# Configuration
ALLOWED_EXTS = {'.pdf', '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml'}
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 400
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_paths(user_data_dir: str):
    """Get persistence paths."""
    base = Path(user_data_dir)
    return {
        'persist_dir': base / "chromadb",
        'state_path': base / "state" / "ingest_state.json"
    }

def fhash(p: Path) -> str:
    """Calculate file hash."""
    h = hashlib.sha1()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def load_state(state_path: Path) -> dict:
    """Load ingestion state."""
    return json.loads(state_path.read_text()) if state_path.exists() else {}

def save_state(state_path: Path, state: dict):
    """Save ingestion state."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2))

def chunk_text(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> Generator[Tuple[int, int, str], None, None]:
    """Split text into chunks."""
    n = len(text)
    i = 0
    while i < n:
        j = min(n, i + size)
        yield i, j, text[i:j]
        if j == n:
            break
        i = j - overlap

def upsert_file(p: Path, collection, model, state: dict):
    """Index a single file."""
    if not p.exists() or not p.is_file():
        return
    if p.suffix.lower() not in ALLOWED_EXTS:
        return
    
    # Skip large files (>10MB)
    if p.stat().st_size > 10 * (1<<20):
        print(f"Skipping large file: {p.name}")
        return

    try:
        txt = read_text(p)
    except Exception as e:
        print(f"Error reading {p.name}: {e}")
        return
        
    if not txt.strip():
        return

    # Remove existing chunks for this file
    collection.delete(where={"path": str(p)})

    ids, docs, metas = [], [], []
    for k, (a, b, seg) in enumerate(chunk_text(txt)):
        ids.append(f"{p}:{a}-{b}")
        docs.append(seg)
        metas.append({
            "path": str(p),
            "filename": p.name,
            "start": a,
            "end": b,
            "mtime": int(p.stat().st_mtime)
        })
    
    if not docs:
        return

    # Embed and add
    vecs = model.encode(docs, normalize_embeddings=True)
    collection.add(ids=ids, embeddings=vecs.tolist(), documents=docs, metadatas=metas)

    # Update state
    state[str(p)] = {"hash": fhash(p), "mtime": int(p.stat().st_mtime)}
    print(f"Indexed: {p.name} ({len(docs)} chunks)")

def index_directory(source_dir: Path, user_data_dir: str):
    """Index all files in directory."""
    paths = get_paths(user_data_dir)
    
    print(f"Initializing ChromaDB at {paths['persist_dir']}...")
    client = chromadb.PersistentClient(
        path=str(paths['persist_dir']), 
        settings=Settings(allow_reset=True)
    )
    collection = client.get_or_create_collection("docs", metadata={"hnsw:space": "cosine"})
    
    print(f"Loading embedding model {EMBED_MODEL}...")
    model = SentenceTransformer(EMBED_MODEL)
    
    state = load_state(paths['state_path'])
    
    print(f"Scanning {source_dir}...")
    count = 0
    for p in source_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in ALLOWED_EXTS:
            # Check if modified
            current_hash = fhash(p)
            stored_hash = state.get(str(p), {}).get("hash")
            
            if current_hash != stored_hash:
                upsert_file(p, collection, model, state)
                count += 1
    
    save_state(paths['state_path'], state)
    print(f"Indexing complete. Processed {count} files.")

def main():
    parser = argparse.ArgumentParser(description="Index files for Local RAG")
    parser.add_argument("source_dir", help="Directory to index")
    parser.add_argument("--user-data-dir", required=True, help="Path to user data directory")
    
    args = parser.parse_args()
    
    source = Path(args.source_dir).resolve()
    if not source.exists():
        print(f"Error: Source directory not found: {source}")
        sys.exit(1)
        
    index_directory(source, args.user_data_dir)

if __name__ == "__main__":
    main()
