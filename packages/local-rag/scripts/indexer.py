#!/usr/bin/env python3
"""
Indexer script for Local RAG.

Scans a directory and indexes supported files into vector store.
Supports multiple chunking strategies, vector stores, and BM25 indexing.
"""

import os
import sys
import hashlib
import json
import argparse
from pathlib import Path
from typing import List, Generator, Tuple, Optional

from sentence_transformers import SentenceTransformer

from ingest.extractor import read_text_with_ocr as read_text
from chunking import ChunkingStrategy, get_chunker, chunk_text, Chunk
from vectorstore import VectorStoreType, get_vector_store, get_vector_store_from_env
from search import BM25Index


# Configuration defaults
ALLOWED_EXTS = {'.pdf', '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml',
                '.docx', '.pptx', '.xlsx', '.ts', '.c', '.cpp', '.h', '.sh'}
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "3000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "400"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "template")
VECTOR_STORE = os.getenv("VECTOR_STORE", "chroma")


def get_paths(user_data_dir: str):
    """Get persistence paths."""
    base = Path(user_data_dir)
    return {
        'persist_dir': base / "vectordb",
        'state_path': base / "state" / "ingest_state.json",
        'bm25_path': base / "state" / "bm25_index.json"
    }


def fhash(p: Path) -> str:
    """Calculate file hash."""
    h = hashlib.sha1()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state(state_path: Path) -> dict:
    """Load ingestion state."""
    return json.loads(state_path.read_text()) if state_path.exists() else {}


def save_state(state_path: Path, state: dict):
    """Save ingestion state."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2))


class DocumentIndexer:
    """
    Enhanced document indexer with configurable chunking and storage.
    """

    def __init__(
        self,
        user_data_dir: str,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        chunking_strategy: str = CHUNKING_STRATEGY,
        vector_store_type: str = VECTOR_STORE,
        embed_model_name: str = EMBED_MODEL,
        build_bm25: bool = True
    ):
        self.user_data_dir = user_data_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunking_strategy = chunking_strategy
        self.vector_store_type = vector_store_type
        self.embed_model_name = embed_model_name
        self.build_bm25 = build_bm25

        self.paths = get_paths(user_data_dir)
        self.state = load_state(self.paths['state_path'])

        self._embed_model = None
        self._vector_store = None
        self._chunker = None
        self._bm25_index = None

    @property
    def embed_model(self):
        """Lazy load embedding model."""
        if self._embed_model is None:
            print(f"Loading embedding model {self.embed_model_name}...")
            self._embed_model = SentenceTransformer(self.embed_model_name)
        return self._embed_model

    @property
    def vector_store(self):
        """Lazy initialize vector store."""
        if self._vector_store is None:
            print(f"Initializing {self.vector_store_type} vector store...")
            try:
                store_type = VectorStoreType(self.vector_store_type)
            except ValueError:
                store_type = VectorStoreType.CHROMA

            self._vector_store = get_vector_store(
                store_type=store_type,
                collection_name="docs",
                persist_dir=str(self.paths['persist_dir'])
            )
        return self._vector_store

    @property
    def chunker(self):
        """Get chunker based on strategy."""
        if self._chunker is None:
            try:
                strategy = ChunkingStrategy(self.chunking_strategy)
            except ValueError:
                strategy = ChunkingStrategy.TEMPLATE

            self._chunker = get_chunker(
                strategy=strategy,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        return self._chunker

    @property
    def bm25_index(self) -> Optional[BM25Index]:
        """Get or create BM25 index."""
        if not self.build_bm25:
            return None

        if self._bm25_index is None:
            bm25_path = self.paths['bm25_path']
            if bm25_path.exists():
                try:
                    self._bm25_index = BM25Index.load(str(bm25_path))
                except Exception as e:
                    print(f"Warning: Could not load BM25 index: {e}")
                    self._bm25_index = BM25Index()
            else:
                self._bm25_index = BM25Index()

        return self._bm25_index

    def should_index_file(self, path: Path) -> bool:
        """Check if file should be indexed."""
        if not path.exists() or not path.is_file():
            return False

        if path.suffix.lower() not in ALLOWED_EXTS:
            return False

        # Skip large files (>10MB)
        if path.stat().st_size > 10 * (1 << 20):
            return False

        return True

    def is_file_changed(self, path: Path) -> bool:
        """Check if file has changed since last indexing."""
        current_hash = fhash(path)
        stored_hash = self.state.get(str(path), {}).get("hash")
        return current_hash != stored_hash

    def index_file(self, path: Path) -> int:
        """
        Index a single file.

        Returns:
            Number of chunks indexed
        """
        if not self.should_index_file(path):
            return 0

        try:
            text = read_text(path)
        except Exception as e:
            print(f"Error reading {path.name}: {e}")
            return 0

        if not text.strip():
            return 0

        # Delete existing chunks for this file
        self.vector_store.delete_documents(where={"path": str(path)})

        # Also remove from BM25 index
        if self.bm25_index:
            # Remove old entries (by prefix matching on doc_id)
            old_ids = [doc_id for doc_id in self.bm25_index.doc_ids if doc_id.startswith(str(path))]
            for old_id in old_ids:
                self.bm25_index.remove_document(old_id)

        # Chunk the text
        chunks = list(self.chunker.chunk(text, file_path=str(path)))

        if not chunks:
            return 0

        # Prepare data for indexing
        ids = []
        texts = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{path}:{chunk.start}-{chunk.end}"
            ids.append(chunk_id)
            texts.append(chunk.text)
            metadatas.append({
                "path": str(path),
                "filename": path.name,
                "start": chunk.start,
                "end": chunk.end,
                "chunk_index": i,
                "mtime": int(path.stat().st_mtime),
                "strategy": chunk.metadata.get("strategy", self.chunking_strategy),
                **{k: v for k, v in chunk.metadata.items() if k != "strategy"}
            })

        # Generate embeddings
        embeddings = self.embed_model.encode(texts, normalize_embeddings=True)

        # Add to vector store
        self.vector_store.add_documents(
            ids=ids,
            texts=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        # Add to BM25 index
        if self.bm25_index:
            self.bm25_index.add_documents(ids, texts)

        # Update state
        self.state[str(path)] = {
            "hash": fhash(path),
            "mtime": int(path.stat().st_mtime),
            "chunks": len(chunks)
        }

        return len(chunks)

    def index_directory(self, source_dir: Path, force: bool = False) -> dict:
        """
        Index all files in a directory.

        Args:
            source_dir: Directory to index
            force: Force re-indexing of all files

        Returns:
            Statistics about indexing
        """
        stats = {
            "files_processed": 0,
            "files_skipped": 0,
            "chunks_created": 0,
            "errors": 0
        }

        print(f"Scanning {source_dir}...")

        for path in source_dir.rglob("*"):
            if not self.should_index_file(path):
                continue

            # Check if file changed (unless forcing)
            if not force and not self.is_file_changed(path):
                stats["files_skipped"] += 1
                continue

            try:
                num_chunks = self.index_file(path)
                if num_chunks > 0:
                    stats["files_processed"] += 1
                    stats["chunks_created"] += num_chunks
                    print(f"Indexed: {path.name} ({num_chunks} chunks)")
                else:
                    stats["files_skipped"] += 1
            except Exception as e:
                print(f"Error indexing {path.name}: {e}")
                stats["errors"] += 1

        # Save state and BM25 index
        save_state(self.paths['state_path'], self.state)

        if self.bm25_index:
            self.bm25_index.save(str(self.paths['bm25_path']))

        return stats

    def get_stats(self) -> dict:
        """Get indexing statistics."""
        return {
            "vector_store": self.vector_store_type,
            "chunking_strategy": self.chunking_strategy,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "total_documents": self.vector_store.count(),
            "indexed_files": len(self.state),
            "bm25_enabled": self.build_bm25 and self.bm25_index is not None,
            "bm25_documents": self.bm25_index.doc_count if self.bm25_index else 0
        }


def index_directory(source_dir: Path, user_data_dir: str, **kwargs):
    """
    Index all files in directory.

    Backward-compatible wrapper around DocumentIndexer.
    """
    indexer = DocumentIndexer(user_data_dir, **kwargs)
    stats = indexer.index_directory(source_dir)

    print(f"\nIndexing complete:")
    print(f"  Files processed: {stats['files_processed']}")
    print(f"  Files skipped:   {stats['files_skipped']}")
    print(f"  Chunks created:  {stats['chunks_created']}")
    if stats['errors']:
        print(f"  Errors:          {stats['errors']}")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Index files for Local RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Documents --user-data-dir ~/rag-data
  %(prog)s ~/Documents --user-data-dir ~/rag-data --strategy sentence
  %(prog)s ~/Documents --user-data-dir ~/rag-data --store qdrant
  %(prog)s ~/Documents --user-data-dir ~/rag-data --force
        """
    )

    parser.add_argument("source_dir", help="Directory to index")
    parser.add_argument("--user-data-dir", required=True, help="Path to user data directory")
    parser.add_argument(
        "--strategy",
        choices=["fixed", "sentence", "semantic", "template"],
        default=CHUNKING_STRATEGY,
        help=f"Chunking strategy (default: {CHUNKING_STRATEGY})"
    )
    parser.add_argument(
        "--store",
        choices=["chroma", "qdrant"],
        default=VECTOR_STORE,
        help=f"Vector store backend (default: {VECTOR_STORE})"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help=f"Chunk size in characters (default: {CHUNK_SIZE})"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=CHUNK_OVERLAP,
        help=f"Chunk overlap in characters (default: {CHUNK_OVERLAP})"
    )
    parser.add_argument(
        "--no-bm25",
        action="store_true",
        help="Disable BM25 index building"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-indexing of all files"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show index statistics and exit"
    )

    args = parser.parse_args()

    source = Path(args.source_dir).resolve()
    if not source.exists() and not args.stats:
        print(f"Error: Source directory not found: {source}")
        sys.exit(1)

    indexer = DocumentIndexer(
        user_data_dir=args.user_data_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        chunking_strategy=args.strategy,
        vector_store_type=args.store,
        build_bm25=not args.no_bm25
    )

    if args.stats:
        stats = indexer.get_stats()
        print(json.dumps(stats, indent=2))
        return

    stats = indexer.index_directory(source, force=args.force)

    print(f"\nIndexing complete:")
    print(f"  Files processed: {stats['files_processed']}")
    print(f"  Files skipped:   {stats['files_skipped']}")
    print(f"  Chunks created:  {stats['chunks_created']}")
    if stats['errors']:
        print(f"  Errors:          {stats['errors']}")


if __name__ == "__main__":
    main()
