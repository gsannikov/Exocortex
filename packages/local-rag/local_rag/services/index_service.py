#!/usr/bin/env python3
"""
Indexer script for Local RAG.

Scans a directory and indexes supported files into vector store.
Supports multiple chunking strategies, vector stores, and BM25 indexing.
"""

import sys
import hashlib
import json
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Generator, Tuple, Optional
import threading
from datetime import datetime

from sentence_transformers import SentenceTransformer

from ..utils.logger import setup_logging, get_logger

from ..settings import LocalRagSettings, get_settings
from ..ingestion.extractors import read_text_with_ocr as read_text
from ..ingestion.discover import discover_files
from ..ingestion.filters import filter_chunks
from ..ingestion.chunking import ChunkingStrategy, get_chunker, chunk_text, Chunk
from ..search.hybrid import BM25Index
from ..storage import create_repository, VectorStoreRepository
from ..adapters.vectorstore import get_vector_store

# Load defaults once
DEFAULT_SETTINGS = get_settings()


# Configuration defaults
ALLOWED_EXTS = {
    # Documents
    '.pdf', '.txt', '.md', '.mdx', '.mdc',
    '.docx', '.pptx', '.xlsx', '.doc',
    # Code
    '.py', '.js', '.ts', '.tsx', '.jsx',
    '.html', '.xhtml', '.css', '.scss',
    '.json', '.jsonc', '.yaml', '.yml',
    '.c', '.cpp', '.h', '.hpp', '.sh',
    '.swift', '.go', '.rs', '.java',
    # Images (OCR)
    '.png', '.jpg', '.jpeg', '.tiff', '.webp',
}

# Directories to exclude from indexing
EXCLUDE_DIRS = {
    '.git', '.svn', '.hg',           # Version control
    'node_modules', '__pycache__',    # Dependencies/cache
    '.venv', 'venv', 'env',           # Python environments
    '.idea', '.vscode',               # IDE configs
    'dist', 'build', '.next',         # Build outputs
    '.cache', '.tmp', 'tmp', 'temp',  # Cache/temp
    'vectordb', 'chromadb', 'chroma', # Vector databases (avoid indexing ourselves)
    'claude-skills-data',             # Our own data folder
    '.DS_Store',                      # macOS
    'Thumbs.db',                      # Windows
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
        user_data_dir: Optional[str] = None,
        ocr_enabled: Optional[bool] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        chunking_strategy: Optional[str] = None,
        vector_store_type: Optional[str] = None,
        embed_model_name: Optional[str] = None,
        embed_batch_size: Optional[int] = None,
        build_bm25: bool = True,
        include_globs: Optional[List[str]] = None,
        exclude_globs: Optional[List[str]] = None,
        parallel_workers: Optional[int] = None,
        max_errors: Optional[int] = None,
        settings: Optional[LocalRagSettings] = None
    ):
        overrides = {}
        if user_data_dir is not None:
            overrides["user_data_dir"] = user_data_dir
        if ocr_enabled is not None:
            overrides["ocr_enabled"] = ocr_enabled
        if chunk_size is not None:
            overrides["chunk_size"] = chunk_size
        if chunk_overlap is not None:
            overrides["chunk_overlap"] = chunk_overlap
        if chunking_strategy is not None:
            overrides["chunking_strategy"] = chunking_strategy
        if vector_store_type is not None:
            overrides["vector_store"] = vector_store_type
        if embed_model_name is not None:
            overrides["embed_model"] = embed_model_name
        if embed_batch_size is not None:
            overrides["embed_batch_size"] = embed_batch_size
        if include_globs is not None:
            overrides["include_globs"] = tuple(include_globs)
        if exclude_globs is not None:
            overrides["exclude_globs"] = tuple(exclude_globs)
        if parallel_workers is not None:
            overrides["parallel_workers"] = parallel_workers
        if max_errors is not None:
            overrides["max_errors"] = max_errors

        self.settings = settings or get_settings(**overrides)
        self.settings.apply_runtime_env()
        
        # Initialize logging
        if self.settings.log_to_file:
            log_dir = self.settings.paths["log_dir"]
            setup_logging(
                log_dir,
                self.settings.log_level,
                self.settings.log_rotation_mb,
                self.settings.log_backup_count
            )
        
        self.logger = get_logger(__name__)

        self.user_data_dir = str(self.settings.user_data_dir)
        self.chunk_size = self.settings.chunk_size
        self.chunk_overlap = self.settings.chunk_overlap
        self.chunking_strategy = self.settings.chunking_strategy
        self.vector_store_type = self.settings.vector_store
        self.embed_model_name = self.settings.embed_model
        self.embed_batch_size = self.settings.embed_batch_size
        self.build_bm25 = build_bm25
        self.include_globs = list(self.settings.include_globs or [])
        self.exclude_globs = list(self.settings.exclude_globs or [])
        self.parallel_workers = self.settings.parallel_workers
        self.max_errors = self.settings.max_errors
        self.min_chunk_chars = self.settings.chunk_min_chars
        self.strip_control_chars = self.settings.chunk_strip_control
        self.min_chunk_entropy = self.settings.chunk_min_entropy

        self.paths = self.settings.paths
        self.state = load_state(self.paths["state_path"])

        self._embed_model = None
        self._vector_store = None
        self._chunker = None
        self._bm25_index = None
        self._repository: Optional[VectorStoreRepository] = None
        self._write_lock = threading.Lock()

    @property
    def embed_model(self):
        """Lazy load embedding model."""
        if self._embed_model is None:
            self.logger.info(f"Loading embedding model {self.embed_model_name}...")
            self._embed_model = SentenceTransformer(self.embed_model_name)
        return self._embed_model

    @property
    def vector_store(self):
        """Lazy initialize vector store."""
        if self._vector_store is None:
            # Ensure repository is initialized so we reuse the same store instance
            self._vector_store = self.repository.store
        return self._vector_store

    @property
    def repository(self) -> VectorStoreRepository:
        """Vector store wrapped in repository for idempotent upserts."""
        if self._repository is None:
            self._repository = create_repository(self.settings, factory=get_vector_store)
            if self._vector_store is None:
                self._vector_store = self._repository.store
        return self._repository

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
                    self.logger.warning(f"Could not load BM25 index: {e}")
                    self._bm25_index = BM25Index()
            else:
                self._bm25_index = BM25Index()

        return self._bm25_index

    def should_index_file(self, path: Path) -> bool:
        """Check if file should be indexed."""
        if not path.exists() or not path.is_file():
            return False

        # Note: Parent directory exclusion is handled by discover_files()
        # to avoid false positives with system paths like /tmp

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

    def index_file(self, path: Path) -> Tuple[int, int]:
        """
        Index a single file.

        Returns:
            (Number of chunks indexed, chunks dropped)
        """
        if not self.should_index_file(path):
            return 0, 0

        try:
            text = read_text(path, settings=self.settings)
        except Exception as e:
            self.logger.error(f"Error reading {path.name}: {e}")
            return 0, 0

        if not text.strip():
            return 0, 0

        # Chunk the text
        chunks = list(self.chunker.chunk(text, file_path=str(path)))

        if not chunks:
            return 0, 0

        # Quality filter
        filtered_chunks, dropped = filter_chunks(
            chunks,
            min_chars=self.min_chunk_chars,
            min_entropy=self.min_chunk_entropy,
            strip_control=self.strip_control_chars,
        )

        if not filtered_chunks:
            return 0, dropped

        # Prepare data for indexing
        ids = []
        texts = []
        metadatas = []

        for i, chunk in enumerate(filtered_chunks):
            chunk_id = f"{path}:{chunk.start}-{chunk.end}"
            ids.append(chunk_id)
            texts.append(chunk.text)

            # Build metadata, filtering out None values (ChromaDB doesn't accept None)
            meta = {
                "path": str(path),
                "filename": path.name,
                "start": chunk.start,
                "end": chunk.end,
                "chunk_index": i,
                "mtime": int(path.stat().st_mtime),
                "strategy": chunk.metadata.get("strategy", self.chunking_strategy),
            }
            # Add extra metadata from chunk, excluding None values
            for k, v in chunk.metadata.items():
                if k != "strategy" and v is not None:
                    meta[k] = v
            metadatas.append(meta)

        # Generate embeddings
        embeddings = self.embed_model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=self.embed_batch_size
        )

        with self._write_lock:
            # Delete existing chunks for this file
            self.repository.delete_documents(where={"path": str(path)})

            # Also remove from BM25 index
            if self.bm25_index:
                # Remove old entries (by prefix matching on doc_id)
                old_ids = [doc_id for doc_id in self.bm25_index.doc_ids if doc_id.startswith(str(path))]
                for old_id in old_ids:
                    self.bm25_index.remove_document(old_id)

            # Add to vector store
            self.repository.upsert_documents(
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
                "chunks": len(filtered_chunks)
            }

        return len(filtered_chunks), dropped

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
            "chunks_filtered": 0,
            "errors": 0,
            "error_details": [],  # List of {path, error, timestamp}
            "skipped_large": [],  # Files > max_file_size_mb
            "skipped_unchanged": 0,  # Files not changed since last index
        }

        self.logger.info(f"Starting indexing: {source_dir}")
        self.logger.info(f"Scanning {source_dir}...")

        candidates = discover_files(
            source_dir,
            allowed_exts=ALLOWED_EXTS,
            exclude_dirs=EXCLUDE_DIRS,
            include_globs=self.include_globs,
            exclude_globs=self.exclude_globs,
        )
        
        paths = list(candidates)
        self.logger.info(f"Found {len(paths)} candidate files")

        def process_path(path: Path):
            # Check file size before processing
            try:
                file_size_mb = path.stat().st_size / (1024 * 1024)
                if file_size_mb > self.settings.max_file_size_mb:
                    self.logger.warning(f"Skipping large file: {path} ({file_size_mb:.1f}MB > {self.settings.max_file_size_mb}MB)")
                    stats["skipped_large"].append({"path": str(path), "size_mb": round(file_size_mb, 1)})
                    return ("skip_large", path, 0, 0, None)
            except (OSError, FileNotFoundError) as e:
                self.logger.error(f"Cannot access file {path}: {e}")
                return ("error", path, 0, 0, e)
                
            if not self.should_index_file(path):
                return ("skip", path, 0, 0, None)
            if not force and not self.is_file_changed(path):
                stats["skipped_unchanged"] += 1
                return ("skip_unchanged", path, 0, 0, None)
            try:
                num_chunks, dropped = self.index_file(path)
                return ("ok", path, num_chunks, dropped, None)
            except Exception as e:
                self.logger.error(f"Failed to index {path}: {e}", exc_info=True)
                return ("error", path, 0, 0, e)



        # Decide execution strategy
        if self.parallel_workers and self.parallel_workers > 1:
            self.logger.info(f"Indexing with {self.parallel_workers} workers")
            with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
                futures = {executor.submit(process_path, p): p for p in paths}
                for future in as_completed(futures):
                    status, path, num_chunks, dropped, err = future.result()
                    if status == "error":
                        error_detail = {"path": str(path), "error": str(err), "timestamp": datetime.now().isoformat()}
                        stats["error_details"].append(error_detail)
                        self.logger.error(f"Error indexing {path.name}: {err}")
                        stats["errors"] += 1
                        if self.max_errors and stats["errors"] >= self.max_errors:
                            self.logger.warning(f"Max errors reached ({self.max_errors}); aborting")
                            break
                    elif status == "skip_large":
                        stats["files_skipped"] += 1
                    elif status == "skip_unchanged":
                        pass  # Already counted
                    elif num_chunks > 0:
                        stats["files_processed"] += 1
                        stats["chunks_created"] += num_chunks
                        stats["chunks_filtered"] += dropped
                        self.logger.info(f"Indexed: {path.name} ({num_chunks} chunks, dropped {dropped})")
                    else:
                        stats["files_skipped"] += 1
        else:
            self.logger.info("Indexing sequentially (single-threaded)")
            for path in paths:
                status, path, num_chunks, dropped, err = process_path(path)
                if status == "error":
                    error_detail = {"path": str(path), "error": str(err), "timestamp": datetime.now().isoformat()}
                    stats["error_details"].append(error_detail)
                    self.logger.error(f"Error indexing {path.name}: {err}")
                    stats["errors"] += 1
                    if self.max_errors and stats["errors"] >= self.max_errors:
                        self.logger.warning(f"Max errors reached ({self.max_errors}); aborting")
                        break
                elif status == "skip_large":
                    stats["files_skipped"] += 1
                elif status == "skip_unchanged":
                    pass  # Already counted
                elif num_chunks > 0:
                    stats["files_processed"] += 1
                    stats["chunks_created"] += num_chunks
                    stats["chunks_filtered"] += dropped
                    self.logger.info(f"Indexed: {path.name} ({num_chunks} chunks, dropped {dropped})")
                else:
                    stats["files_skipped"] += 1

        # Save state and BM25 index
        save_state(self.paths['state_path'], self.state)

        if self.bm25_index:
            self.bm25_index.save(str(self.paths['bm25_path']))
        
        
        # Log comprehensive summary
        self.logger.info(f"Indexing complete: {stats['files_processed']} processed, "
                        f"{stats['chunks_created']} chunks created, "
                        f"{stats['skipped_unchanged']} unchanged, "
                        f"{len(stats['skipped_large'])} too large, "
                        f"{stats['errors']} errors")
        
        if stats["skipped_large"]:
            self.logger.warning(f"Skipped {len(stats['skipped_large'])} large files (>{self.settings.max_file_size_mb}MB)")
            for item in stats["skipped_large"][:5]:  # Log first 5
                self.logger.warning(f"  - {item['path']} ({item['size_mb']}MB)")
            if len(stats["skipped_large"]) > 5:
                self.logger.warning(f"  ... and {len(stats['skipped_large']) - 5} more")
        
        if stats["error_details"]:
            self.logger.error(f"{len(stats['error_details'])} files failed to index:")
            for error in stats["error_details"][:5]:  # Log first 5
                self.logger.error(f"  - {error['path']}: {error['error']}")
            if len(stats["error_details"]) > 5:
                self.logger.error(f"  ... and {len(stats['error_details']) - 5} more (see full log)")
        
        self.logger.info(f"\nIndexing complete:")
        self.logger.info(f"  Files processed: {stats['files_processed']}")
        self.logger.info(f"  Chunks created: {stats['chunks_created']}")
        self.logger.info(f"  Files skipped (unchanged): {stats['skipped_unchanged']}")
        self.logger.info(f"  Files skipped (too large): {len(stats['skipped_large'])}")
        self.logger.info(f"  Errors: {stats['errors']}")

        if self.settings.log_to_file:
            log_path = self.settings.paths["log_dir"] / "indexing.log"
            self.logger.info(f"\nFull logs: {log_path}")

        return stats

    def get_stats(self) -> dict:
        """Get indexing statistics."""
        return {
            "vector_store": self.vector_store_type,
            "chunking_strategy": self.chunking_strategy,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "total_documents": self.repository.count(),
            "indexed_files": len(self.state),
            "bm25_enabled": self.build_bm25 and self.bm25_index is not None,
            "bm25_documents": self.bm25_index.doc_count if self.bm25_index else 0
        }


def index_directory(
    source_dir: Path,
    user_data_dir: Optional[str] = None,
    settings: Optional[LocalRagSettings] = None,
    include_globs: Optional[List[str]] = None,
    exclude_globs: Optional[List[str]] = None,
    parallel_workers: Optional[int] = None,
    max_errors: Optional[int] = None,
    **kwargs
):
    """
    Index all files in directory.

    Backward-compatible wrapper around DocumentIndexer.
    """
    indexer = DocumentIndexer(
        user_data_dir=user_data_dir,
        settings=settings,
        include_globs=include_globs,
        exclude_globs=exclude_globs,
        parallel_workers=parallel_workers,
        max_errors=max_errors,
        **kwargs
    )
    stats = indexer.index_directory(source_dir)

    print(f"\nIndexing complete:")
    print(f"  Files processed: {stats['files_processed']}")
    print(f"  Files skipped:   {stats['files_skipped']}")
    print(f"  Chunks created:  {stats['chunks_created']}")
    if stats.get("chunks_filtered"):
        print(f"  Chunks dropped:  {stats['chunks_filtered']}")
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
    parser.add_argument(
        "--user-data-dir",
        default=str(DEFAULT_SETTINGS.user_data_dir),
        help="Path to user data directory (default: %(default)s)"
    )
    parser.add_argument(
        "--strategy",
        choices=["fixed", "sentence", "semantic", "template"],
        default=DEFAULT_SETTINGS.chunking_strategy,
        help="Chunking strategy"
    )
    parser.add_argument(
        "--store",
        choices=["chroma", "qdrant"],
        default=DEFAULT_SETTINGS.vector_store,
        help="Vector store backend"
    )
    parser.add_argument(
        "--embed-batch-size",
        type=int,
        default=DEFAULT_SETTINGS.embed_batch_size,
        help="Batch size for embedding model encode() calls"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_SETTINGS.chunk_size,
        help="Chunk size in characters"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=DEFAULT_SETTINGS.chunk_overlap,
        help="Chunk overlap in characters"
    )
    parser.add_argument(
        "--no-bm25",
        action="store_true",
        help="Disable BM25 index building"
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Disable OCR (images and scanned PDFs will be skipped)"
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=DEFAULT_SETTINGS.parallel_workers,
        help="Worker count for indexing (defaults to %(default)s)"
    )
    parser.add_argument(
        "--include",
        nargs="*",
        default=DEFAULT_SETTINGS.include_globs or None,
        help="Glob patterns to include (relative to source dir)"
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=DEFAULT_SETTINGS.exclude_globs or None,
        help="Glob patterns to exclude (relative to source dir)"
    )
    parser.add_argument(
        "--max-errors",
        type=int,
        default=DEFAULT_SETTINGS.max_errors,
        help="Abort after this many errors (defaults to %(default)s)"
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
        ocr_enabled=not args.no_ocr,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        chunking_strategy=args.strategy,
        vector_store_type=args.store,
        embed_batch_size=args.embed_batch_size,
        build_bm25=not args.no_bm25,
        include_globs=args.include,
        exclude_globs=args.exclude,
        parallel_workers=args.parallel,
        max_errors=args.max_errors,
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
    if stats.get("chunks_filtered"):
        print(f"  Chunks dropped:  {stats['chunks_filtered']}")
    if stats['errors']:
        print(f"  Errors:          {stats['errors']}")


if __name__ == "__main__":
    main()
