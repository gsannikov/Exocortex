#!/usr/bin/env python3
"""
Query script for Local RAG.

Searches the index for relevant documents using hybrid search
(vector similarity + BM25) with optional reranking.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Optional

from sentence_transformers import SentenceTransformer
from rapidfuzz import fuzz

from .vectorstore import VectorStoreType, get_vector_store
from .search import (
    HybridSearcher,
    SearchConfig,
    SearchMethod,
    FusionMethod,
    BM25Index,
    SearchResult
)


# Configuration defaults
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_STORE = os.getenv("VECTOR_STORE", "chroma")
SEARCH_METHOD = os.getenv("SEARCH_METHOD", "hybrid")
VECTOR_WEIGHT = float(os.getenv("VECTOR_WEIGHT", "0.7"))
BM25_WEIGHT = float(os.getenv("BM25_WEIGHT", "0.3"))
USE_RERANKER = os.getenv("USE_RERANKER", "false").lower() == "true"


def get_paths(user_data_dir: str):
    """Get persistence paths."""
    base = Path(user_data_dir)
    return {
        'persist_dir': base / "vectordb",
        'bm25_path': base / "state" / "bm25_index.json"
    }


class DocumentSearcher:
    """
    Enhanced document searcher with hybrid search and reranking.
    """

    def __init__(
        self,
        user_data_dir: str,
        vector_store_type: str = VECTOR_STORE,
        embed_model_name: str = EMBED_MODEL,
        search_method: str = SEARCH_METHOD,
        vector_weight: float = VECTOR_WEIGHT,
        bm25_weight: float = BM25_WEIGHT,
        use_reranker: bool = USE_RERANKER
    ):
        self.user_data_dir = user_data_dir
        self.vector_store_type = vector_store_type
        self.embed_model_name = embed_model_name
        self.search_method = search_method
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight
        self.use_reranker = use_reranker

        self.paths = get_paths(user_data_dir)

        self._embed_model = None
        self._vector_store = None
        self._hybrid_searcher = None

    @property
    def embed_model(self):
        """Lazy load embedding model."""
        if self._embed_model is None:
            self._embed_model = SentenceTransformer(self.embed_model_name)
        return self._embed_model

    @property
    def vector_store(self):
        """Lazy initialize vector store."""
        if self._vector_store is None:
            persist_dir = self.paths['persist_dir']

            if not persist_dir.exists():
                raise FileNotFoundError(
                    f"Index not found at {persist_dir}. Please run indexing first."
                )

            try:
                store_type = VectorStoreType(self.vector_store_type)
            except ValueError:
                store_type = VectorStoreType.CHROMA

            self._vector_store = get_vector_store(
                store_type=store_type,
                collection_name="docs",
                persist_dir=str(persist_dir)
            )

        return self._vector_store

    @property
    def hybrid_searcher(self) -> HybridSearcher:
        """Get or create hybrid searcher."""
        if self._hybrid_searcher is None:
            try:
                method = SearchMethod(self.search_method)
            except ValueError:
                method = SearchMethod.HYBRID

            config = SearchConfig(
                method=method,
                fusion=FusionMethod.RRF,
                vector_weight=self.vector_weight,
                bm25_weight=self.bm25_weight,
                use_reranker=self.use_reranker
            )

            self._hybrid_searcher = HybridSearcher(
                config=config,
                embed_model=self.embed_model
            )

            # Load BM25 index if it exists and hybrid search is enabled
            if method in (SearchMethod.BM25, SearchMethod.HYBRID):
                bm25_path = self.paths['bm25_path']
                if bm25_path.exists():
                    try:
                        self._hybrid_searcher.load_bm25_index(str(bm25_path))
                    except Exception as e:
                        print(f"Warning: Could not load BM25 index: {e}", file=sys.stderr)

        return self._hybrid_searcher

    def search(
        self,
        query: str,
        k: int = 5,
        metadata_filter: dict = None,
        include_scores: bool = True
    ) -> List[dict]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            k: Number of results to return
            metadata_filter: Optional metadata filter
            include_scores: Whether to include detailed scores

        Returns:
            List of search results
        """
        # Use hybrid searcher if BM25 is available
        if self.hybrid_searcher.bm25_index and self.hybrid_searcher.bm25_index.doc_count > 0:
            results = self._hybrid_search(query, k, metadata_filter)
        else:
            # Fallback to vector-only search
            results = self._vector_search(query, k, metadata_filter)

        # Format results
        items = []
        for result in results:
            item = {
                "path": result.metadata.get("path", ""),
                "filename": result.metadata.get("filename", ""),
                "score": round(result.score, 4),
                "preview": result.text,
                "metadata": result.metadata
            }

            if include_scores and result.source_scores:
                item["source_scores"] = {
                    k: round(v, 4) for k, v in result.source_scores.items()
                }

            items.append(item)

        return items

    def _hybrid_search(
        self,
        query: str,
        k: int,
        metadata_filter: dict = None
    ) -> List[SearchResult]:
        """Perform hybrid search using HybridSearcher."""
        # Get raw ChromaDB collection for hybrid searcher
        # Note: This requires access to the underlying collection
        from vectorstore import ChromaVectorStore

        if isinstance(self.vector_store, ChromaVectorStore):
            collection = self.vector_store.collection
            return self.hybrid_searcher.search(
                query=query,
                collection=collection,
                k=k,
                metadata_filter=metadata_filter
            )
        else:
            # For other stores, use vector-only search
            return self._vector_search(query, k, metadata_filter)

    def _vector_search(
        self,
        query: str,
        k: int,
        metadata_filter: dict = None
    ) -> List[SearchResult]:
        """Perform vector-only search."""
        query_embedding = self.embed_model.encode([query], normalize_embeddings=True)[0]

        vs_results = self.vector_store.search(
            query_embedding=query_embedding,
            k=k * 2,  # Fetch more for fuzzy boosting
            where=metadata_filter
        )

        # Add fuzzy matching boost
        results = []
        for vs_result in vs_results:
            fuzzy_score = fuzz.partial_ratio(
                query.lower(),
                vs_result.text[:1000].lower()
            ) / 100

            # Combine scores
            final_score = (0.7 * vs_result.score) + (0.3 * fuzzy_score)

            results.append(SearchResult(
                doc_id=vs_result.id,
                text=vs_result.text,
                score=final_score,
                metadata=vs_result.metadata,
                source_scores={
                    'vector': vs_result.score,
                    'fuzzy': fuzzy_score
                }
            ))

        # Sort by combined score
        results.sort(key=lambda x: x.score, reverse=True)

        return results[:k]

    def get_document(self, doc_id: str) -> Optional[dict]:
        """Get a specific document by ID."""
        docs = self.vector_store.get_documents([doc_id])
        if docs:
            doc = docs[0]
            return {
                "id": doc.id,
                "text": doc.text,
                "metadata": doc.metadata
            }
        return None

    def get_stats(self) -> dict:
        """Get search index statistics."""
        bm25_count = 0
        if self.hybrid_searcher.bm25_index:
            bm25_count = self.hybrid_searcher.bm25_index.doc_count

        return {
            "vector_store": self.vector_store_type,
            "search_method": self.search_method,
            "vector_weight": self.vector_weight,
            "bm25_weight": self.bm25_weight,
            "use_reranker": self.use_reranker,
            "total_documents": self.vector_store.count(),
            "bm25_documents": bm25_count
        }


def search(query: str, user_data_dir: str, k: int = 5, **kwargs):
    """
    Search the index.

    Backward-compatible wrapper around DocumentSearcher.
    """
    searcher = DocumentSearcher(user_data_dir, **kwargs)
    results = searcher.search(query, k)

    output = {
        "query": query,
        "method": searcher.search_method,
        "results": results
    }

    print(json.dumps(output, indent=2))
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Query Local RAG index",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "machine learning" --user-data-dir ~/rag-data
  %(prog)s "neural networks" --user-data-dir ~/rag-data -k 10
  %(prog)s "python functions" --user-data-dir ~/rag-data --method hybrid
  %(prog)s "error handling" --user-data-dir ~/rag-data --rerank
        """
    )

    parser.add_argument("query", help="Search query")
    parser.add_argument("--user-data-dir", required=True, help="Path to user data directory")
    parser.add_argument("-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument(
        "--method",
        choices=["vector", "bm25", "hybrid"],
        default=SEARCH_METHOD,
        help=f"Search method (default: {SEARCH_METHOD})"
    )
    parser.add_argument(
        "--store",
        choices=["chroma", "qdrant"],
        default=VECTOR_STORE,
        help=f"Vector store backend (default: {VECTOR_STORE})"
    )
    parser.add_argument(
        "--vector-weight",
        type=float,
        default=VECTOR_WEIGHT,
        help=f"Weight for vector similarity (default: {VECTOR_WEIGHT})"
    )
    parser.add_argument(
        "--bm25-weight",
        type=float,
        default=BM25_WEIGHT,
        help=f"Weight for BM25 score (default: {BM25_WEIGHT})"
    )
    parser.add_argument(
        "--rerank",
        action="store_true",
        help="Enable cross-encoder reranking"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show index statistics and exit"
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="Metadata filter as JSON (e.g., '{\"filename\": \"doc.pdf\"}')"
    )

    args = parser.parse_args()

    try:
        searcher = DocumentSearcher(
            user_data_dir=args.user_data_dir,
            vector_store_type=args.store,
            search_method=args.method,
            vector_weight=args.vector_weight,
            bm25_weight=args.bm25_weight,
            use_reranker=args.rerank
        )

        if args.stats:
            stats = searcher.get_stats()
            print(json.dumps(stats, indent=2))
            return

        # Parse metadata filter if provided
        metadata_filter = None
        if args.filter:
            try:
                metadata_filter = json.loads(args.filter)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON filter: {e}", file=sys.stderr)
                sys.exit(1)

        results = searcher.search(
            query=args.query,
            k=args.k,
            metadata_filter=metadata_filter
        )

        output = {
            "query": args.query,
            "method": args.method,
            "results": results
        }

        print(json.dumps(output, indent=2))

    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Search failed: {e}"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
