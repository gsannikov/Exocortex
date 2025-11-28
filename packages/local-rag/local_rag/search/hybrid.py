#!/usr/bin/env python3
"""
Hybrid search module for Local RAG.

Combines multiple retrieval methods:
- Vector similarity (semantic search via embeddings)
- BM25 (keyword-based sparse retrieval)
- Fuzzy matching (for typo tolerance)

Supports configurable fusion strategies and reranking.
"""

import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import json


class SearchMethod(str, Enum):
    """Available search methods."""
    VECTOR = "vector"
    BM25 = "bm25"
    HYBRID = "hybrid"


class FusionMethod(str, Enum):
    """Methods for fusing multiple result sets."""
    RRF = "rrf"  # Reciprocal Rank Fusion
    WEIGHTED = "weighted"  # Weighted combination
    MAX = "max"  # Maximum score


@dataclass
class SearchResult:
    """A single search result."""
    doc_id: str
    text: str
    score: float
    metadata: dict = field(default_factory=dict)
    source_scores: dict = field(default_factory=dict)


@dataclass
class SearchConfig:
    """Configuration for hybrid search."""
    method: SearchMethod = SearchMethod.HYBRID
    fusion: FusionMethod = FusionMethod.RRF
    vector_weight: float = 0.7
    bm25_weight: float = 0.3
    rrf_k: int = 60  # RRF parameter
    use_reranker: bool = False
    reranker_top_k: int = 20


class BM25Index:
    """
    BM25 sparse retrieval index.

    Implements Okapi BM25 scoring for keyword-based retrieval.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """
        Initialize BM25 index.

        Args:
            k1: Term frequency saturation parameter (1.2-2.0 typical)
            b: Document length normalization (0.75 typical)
        """
        self.k1 = k1
        self.b = b

        # Index structures
        self.doc_ids: List[str] = []
        self.doc_texts: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.doc_count: int = 0

        # Inverted index: term -> [(doc_idx, term_freq), ...]
        self.inverted_index: Dict[str, List[Tuple[int, int]]] = {}
        # Document frequencies: term -> num_docs_containing_term
        self.doc_freqs: Dict[str, int] = {}

        # Tokenization
        self._tokenize_pattern = re.compile(r'\b\w+\b')
        self._stopwords = self._get_stopwords()

    def _get_stopwords(self) -> set:
        """Get common English stopwords."""
        return {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'over', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
            'have', 'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
        }

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into terms."""
        text = text.lower()
        tokens = self._tokenize_pattern.findall(text)
        # Filter stopwords and short tokens
        return [t for t in tokens if t not in self._stopwords and len(t) > 1]

    def add_documents(self, doc_ids: List[str], texts: List[str]):
        """
        Add documents to the BM25 index.

        Args:
            doc_ids: List of document identifiers
            texts: List of document texts
        """
        for doc_id, text in zip(doc_ids, texts):
            self._add_document(doc_id, text)

        # Update average document length
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)

    def _add_document(self, doc_id: str, text: str):
        """Add a single document to the index."""
        doc_idx = len(self.doc_ids)
        self.doc_ids.append(doc_id)
        self.doc_texts.append(text)

        tokens = self.tokenize(text)
        self.doc_lengths.append(len(tokens))
        self.doc_count += 1

        # Count term frequencies in this document
        term_freqs: Dict[str, int] = {}
        for token in tokens:
            term_freqs[token] = term_freqs.get(token, 0) + 1

        # Update inverted index
        for term, freq in term_freqs.items():
            if term not in self.inverted_index:
                self.inverted_index[term] = []
                self.doc_freqs[term] = 0

            self.inverted_index[term].append((doc_idx, freq))
            self.doc_freqs[term] += 1

    def remove_document(self, doc_id: str):
        """Remove a document from the index."""
        if doc_id not in self.doc_ids:
            return

        doc_idx = self.doc_ids.index(doc_id)

        # Remove from inverted index
        for term, postings in list(self.inverted_index.items()):
            self.inverted_index[term] = [(idx, freq) for idx, freq in postings if idx != doc_idx]
            if not self.inverted_index[term]:
                del self.inverted_index[term]
                del self.doc_freqs[term]
            else:
                # Adjust doc_idx for documents after removed one
                self.inverted_index[term] = [
                    (idx - 1 if idx > doc_idx else idx, freq)
                    for idx, freq in self.inverted_index[term]
                ]

        # Remove from document lists
        del self.doc_ids[doc_idx]
        del self.doc_texts[doc_idx]
        del self.doc_lengths[doc_idx]
        self.doc_count -= 1

        # Recalculate average
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)

    def search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        """
        Search the index using BM25 scoring.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of (doc_id, score) tuples sorted by score descending
        """
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        scores: Dict[int, float] = {}

        for token in query_tokens:
            if token not in self.inverted_index:
                continue

            # IDF calculation
            df = self.doc_freqs[token]
            idf = math.log((self.doc_count - df + 0.5) / (df + 0.5) + 1)

            for doc_idx, tf in self.inverted_index[token]:
                doc_length = self.doc_lengths[doc_idx]

                # BM25 score for this term
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
                term_score = idf * numerator / denominator

                scores[doc_idx] = scores.get(doc_idx, 0) + term_score

        # Sort by score and return top k
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
        return [(self.doc_ids[idx], score) for idx, score in sorted_results]

    def get_document(self, doc_id: str) -> Optional[str]:
        """Get document text by ID."""
        try:
            idx = self.doc_ids.index(doc_id)
            return self.doc_texts[idx]
        except ValueError:
            return None

    def save(self, path: str):
        """Save index to disk."""
        data = {
            'k1': self.k1,
            'b': self.b,
            'doc_ids': self.doc_ids,
            'doc_texts': self.doc_texts,
            'doc_lengths': self.doc_lengths,
            'avg_doc_length': self.avg_doc_length,
            'doc_count': self.doc_count,
            'inverted_index': self.inverted_index,
            'doc_freqs': self.doc_freqs
        }
        with open(path, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, path: str) -> 'BM25Index':
        """Load index from disk."""
        with open(path, 'r') as f:
            data = json.load(f)

        index = cls(k1=data['k1'], b=data['b'])
        index.doc_ids = data['doc_ids']
        index.doc_texts = data['doc_texts']
        index.doc_lengths = data['doc_lengths']
        index.avg_doc_length = data['avg_doc_length']
        index.doc_count = data['doc_count']
        index.inverted_index = {k: [tuple(x) for x in v] for k, v in data['inverted_index'].items()}
        index.doc_freqs = data['doc_freqs']
        return index


class HybridSearcher:
    """
    Hybrid search combining vector and BM25 retrieval.

    Supports multiple fusion strategies for combining results.
    """

    def __init__(
        self,
        config: SearchConfig = None,
        embed_model=None,
        reranker=None
    ):
        """
        Initialize hybrid searcher.

        Args:
            config: Search configuration
            embed_model: Sentence transformer model for embeddings
            reranker: Optional cross-encoder reranker
        """
        self.config = config or SearchConfig()
        self._embed_model = embed_model
        self._reranker = reranker
        self.bm25_index: Optional[BM25Index] = None

    @property
    def embed_model(self):
        """Lazy load embedding model."""
        if self._embed_model is None:
            from sentence_transformers import SentenceTransformer
            self._embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return self._embed_model

    @property
    def reranker(self):
        """Lazy load reranker model."""
        if self._reranker is None and self.config.use_reranker:
            from sentence_transformers import CrossEncoder
            self._reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        return self._reranker

    def build_bm25_index(self, doc_ids: List[str], texts: List[str]):
        """Build BM25 index from documents."""
        self.bm25_index = BM25Index()
        self.bm25_index.add_documents(doc_ids, texts)

    def save_bm25_index(self, path: str):
        """Save BM25 index to disk."""
        if self.bm25_index:
            self.bm25_index.save(path)

    def load_bm25_index(self, path: str):
        """Load BM25 index from disk."""
        self.bm25_index = BM25Index.load(path)

    def search(
        self,
        query: str,
        collection,  # ChromaDB collection
        k: int = 10,
        metadata_filter: dict = None
    ) -> List[SearchResult]:
        """
        Perform hybrid search.

        Args:
            query: Search query
            collection: ChromaDB collection for vector search
            k: Number of results to return
            metadata_filter: Optional metadata filter

        Returns:
            List of SearchResult objects sorted by relevance
        """
        # Fetch more results for fusion
        fetch_k = min(k * 3, 100)

        results = []

        if self.config.method in (SearchMethod.VECTOR, SearchMethod.HYBRID):
            vector_results = self._vector_search(query, collection, fetch_k, metadata_filter)
            results.append(('vector', vector_results))

        if self.config.method in (SearchMethod.BM25, SearchMethod.HYBRID):
            if self.bm25_index:
                bm25_results = self._bm25_search(query, fetch_k)
                results.append(('bm25', bm25_results))

        # Fuse results
        if len(results) == 1:
            fused = results[0][1]
        else:
            fused = self._fuse_results(results, k)

        # Rerank if enabled
        if self.config.use_reranker and self.reranker:
            fused = self._rerank(query, fused[:self.config.reranker_top_k])

        return fused[:k]

    def _vector_search(
        self,
        query: str,
        collection,
        k: int,
        metadata_filter: dict = None
    ) -> List[SearchResult]:
        """Perform vector similarity search."""
        query_embedding = self.embed_model.encode([query], normalize_embeddings=True)[0]

        kwargs = {
            'query_embeddings': [query_embedding.tolist()],
            'n_results': k,
            'include': ['documents', 'metadatas', 'distances']
        }
        if metadata_filter:
            kwargs['where'] = metadata_filter

        res = collection.query(**kwargs)

        results = []
        if res.get('ids') and res['ids'][0]:
            for i in range(len(res['ids'][0])):
                doc_id = res['ids'][0][i]
                text = res['documents'][0][i]
                distance = res['distances'][0][i]
                metadata = res['metadatas'][0][i] if res.get('metadatas') else {}

                # Convert distance to similarity score (cosine distance -> similarity)
                score = 1 - distance

                results.append(SearchResult(
                    doc_id=doc_id,
                    text=text,
                    score=score,
                    metadata=metadata,
                    source_scores={'vector': score}
                ))

        return results

    def _bm25_search(self, query: str, k: int) -> List[SearchResult]:
        """Perform BM25 keyword search."""
        if not self.bm25_index:
            return []

        bm25_results = self.bm25_index.search(query, k)

        # Normalize BM25 scores to [0, 1]
        if bm25_results:
            max_score = bm25_results[0][1] if bm25_results[0][1] > 0 else 1
            min_score = min(r[1] for r in bm25_results)
            score_range = max_score - min_score if max_score > min_score else 1

        results = []
        for doc_id, score in bm25_results:
            normalized_score = (score - min_score) / score_range if score_range > 0 else 0
            text = self.bm25_index.get_document(doc_id) or ""

            results.append(SearchResult(
                doc_id=doc_id,
                text=text,
                score=normalized_score,
                source_scores={'bm25': normalized_score}
            ))

        return results

    def _fuse_results(
        self,
        result_sets: List[Tuple[str, List[SearchResult]]],
        k: int
    ) -> List[SearchResult]:
        """Fuse multiple result sets using configured method."""
        if self.config.fusion == FusionMethod.RRF:
            return self._rrf_fusion(result_sets, k)
        elif self.config.fusion == FusionMethod.WEIGHTED:
            return self._weighted_fusion(result_sets, k)
        else:
            return self._max_fusion(result_sets, k)

    def _rrf_fusion(
        self,
        result_sets: List[Tuple[str, List[SearchResult]]],
        k: int
    ) -> List[SearchResult]:
        """
        Reciprocal Rank Fusion.

        RRF(d) = sum(1 / (k + rank(d))) for each ranking
        """
        rrf_k = self.config.rrf_k
        scores: Dict[str, float] = {}
        doc_map: Dict[str, SearchResult] = {}

        for source, results in result_sets:
            for rank, result in enumerate(results):
                doc_id = result.doc_id
                rrf_score = 1.0 / (rrf_k + rank + 1)
                scores[doc_id] = scores.get(doc_id, 0) + rrf_score

                if doc_id not in doc_map:
                    doc_map[doc_id] = result
                else:
                    # Merge source scores
                    doc_map[doc_id].source_scores.update(result.source_scores)

        # Sort by RRF score
        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in sorted_ids[:k]:
            result = doc_map[doc_id]
            result.score = score
            results.append(result)

        return results

    def _weighted_fusion(
        self,
        result_sets: List[Tuple[str, List[SearchResult]]],
        k: int
    ) -> List[SearchResult]:
        """Weighted linear combination of scores."""
        weights = {
            'vector': self.config.vector_weight,
            'bm25': self.config.bm25_weight
        }

        scores: Dict[str, float] = {}
        doc_map: Dict[str, SearchResult] = {}

        for source, results in result_sets:
            weight = weights.get(source, 0.5)
            for result in results:
                doc_id = result.doc_id
                weighted_score = result.score * weight
                scores[doc_id] = scores.get(doc_id, 0) + weighted_score

                if doc_id not in doc_map:
                    doc_map[doc_id] = result
                else:
                    doc_map[doc_id].source_scores.update(result.source_scores)

        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in sorted_ids[:k]:
            result = doc_map[doc_id]
            result.score = score
            results.append(result)

        return results

    def _max_fusion(
        self,
        result_sets: List[Tuple[str, List[SearchResult]]],
        k: int
    ) -> List[SearchResult]:
        """Take maximum score across all sources."""
        scores: Dict[str, float] = {}
        doc_map: Dict[str, SearchResult] = {}

        for source, results in result_sets:
            for result in results:
                doc_id = result.doc_id
                if doc_id not in scores or result.score > scores[doc_id]:
                    scores[doc_id] = result.score

                if doc_id not in doc_map:
                    doc_map[doc_id] = result
                else:
                    doc_map[doc_id].source_scores.update(result.source_scores)

        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in sorted_ids[:k]:
            result = doc_map[doc_id]
            result.score = score
            results.append(result)

        return results

    def _rerank(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        """Rerank results using cross-encoder."""
        if not results or not self.reranker:
            return results

        # Prepare pairs for cross-encoder
        pairs = [(query, r.text) for r in results]

        # Get reranking scores
        rerank_scores = self.reranker.predict(pairs)

        # Update scores
        for result, new_score in zip(results, rerank_scores):
            result.source_scores['rerank'] = float(new_score)
            result.score = float(new_score)

        # Sort by new scores
        results.sort(key=lambda x: x.score, reverse=True)

        return results


def create_hybrid_searcher(
    method: str = "hybrid",
    vector_weight: float = 0.7,
    bm25_weight: float = 0.3,
    use_reranker: bool = False
) -> HybridSearcher:
    """Factory function to create a hybrid searcher."""
    config = SearchConfig(
        method=SearchMethod(method),
        vector_weight=vector_weight,
        bm25_weight=bm25_weight,
        use_reranker=use_reranker
    )
    return HybridSearcher(config=config)
