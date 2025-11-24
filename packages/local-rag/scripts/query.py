#!/usr/bin/env python3
"""
Query script for Local RAG.
Searches the ChromaDB index for relevant documents.
"""

import os
import sys
import json
import argparse
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from rapidfuzz import fuzz

# Configuration
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_paths(user_data_dir: str):
    """Get persistence paths."""
    base = Path(user_data_dir)
    return {
        'persist_dir': base / "chromadb"
    }

def search(query: str, user_data_dir: str, k: int = 5):
    """Search the index."""
    paths = get_paths(user_data_dir)
    persist_dir = paths['persist_dir']
    
    if not persist_dir.exists():
        print(json.dumps({"error": "Index not found. Please run indexing first."}))
        return

    client = chromadb.PersistentClient(
        path=str(persist_dir), 
        settings=Settings(allow_reset=True)
    )
    collection = client.get_collection("docs")
    
    model = SentenceTransformer(EMBED_MODEL)
    qvec = model.encode([query])[0].tolist()
    
    res = collection.query(
        query_embeddings=[qvec], 
        n_results=k, 
        include=["documents", "metadatas", "distances"]
    )
    
    items = []
    if res.get("ids"):
        for i in range(len(res["ids"][0])):
            meta = res["metadatas"][0][i]
            doc = res["documents"][0][i]
            dist = res["distances"][0][i]
            
            # Calculate score (cosine distance to similarity)
            # Distance is usually between 0 and 2 for cosine distance
            # We want a score between 0 and 1
            score = 1 - dist
            
            # Boost with fuzzy match on preview
            fuzzy_score = fuzz.partial_ratio(query.lower(), doc[:1000].lower()) / 100
            final_score = (0.7 * score) + (0.3 * fuzzy_score)
            
            items.append({
                "path": meta["path"],
                "filename": meta.get("filename", os.path.basename(meta["path"])),
                "score": round(final_score, 4),
                "preview": doc,
                "metadata": meta
            })
            
    # Sort by score
    items.sort(key=lambda x: x["score"], reverse=True)
    
    print(json.dumps({
        "query": query,
        "results": items
    }, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Query Local RAG")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--user-data-dir", required=True, help="Path to user data directory")
    parser.add_argument("-k", type=int, default=5, help="Number of results")
    
    args = parser.parse_args()
    
    search(args.query, args.user_data_dir, args.k)

if __name__ == "__main__":
    main()
