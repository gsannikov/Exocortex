"""Tests for hybrid search and BM25."""

from local_rag.search import (
    BM25Index,
    FusionMethod,
    HybridSearcher,
    SearchConfig,
    SearchMethod,
    SearchResult,
    create_hybrid_searcher,
)


class TestBM25Index:
    """Tests for BM25Index."""

    def test_empty_index(self):
        """Test empty index behavior."""
        index = BM25Index()
        results = index.search("test query", k=5)
        assert results == []

    def test_add_single_document(self):
        """Test adding a single document."""
        index = BM25Index()
        index.add_documents(["doc1"], ["This is a test document"])

        assert index.doc_count == 1
        assert "doc1" in index.doc_ids

    def test_add_multiple_documents(self):
        """Test adding multiple documents."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2", "doc3"],
            [
                "Machine learning is great",
                "Deep learning neural networks",
                "Natural language processing"
            ]
        )

        assert index.doc_count == 3

    def test_basic_search(self):
        """Test basic keyword search."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2", "doc3"],
            [
                "Python programming language",
                "Java programming language",
                "Machine learning algorithms"
            ]
        )

        results = index.search("Python programming", k=3)

        assert len(results) > 0
        # Python doc should rank first
        assert results[0][0] == "doc1"

    def test_search_with_k(self):
        """Test search respects k parameter."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2", "doc3", "doc4", "doc5"],
            [
                "test document one",
                "test document two",
                "test document three",
                "test document four",
                "test document five"
            ]
        )

        results = index.search("test document", k=2)
        assert len(results) <= 2

    def test_tokenization(self):
        """Test text tokenization."""
        index = BM25Index()

        tokens = index.tokenize("Hello, World! This is a TEST.")

        # Should be lowercase
        assert all(t.islower() for t in tokens)
        # Should remove stopwords
        assert "is" not in tokens
        assert "a" not in tokens
        # Should keep meaningful words
        assert "hello" in tokens
        assert "world" in tokens
        assert "test" in tokens

    def test_stopword_removal(self):
        """Test that stopwords are removed."""
        index = BM25Index()

        tokens = index.tokenize("The quick brown fox jumps over the lazy dog")

        assert "the" not in tokens
        assert "over" not in tokens
        assert "quick" in tokens
        assert "brown" in tokens
        assert "fox" in tokens

    def test_idf_calculation(self):
        """Test IDF weighting (rare terms should score higher)."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2", "doc3"],
            [
                "common common common rare",
                "common common common",
                "common common common"
            ]
        )

        # Document with rare term should rank higher for that term
        results = index.search("rare", k=3)
        assert results[0][0] == "doc1"

    def test_get_document(self):
        """Test document retrieval."""
        index = BM25Index()
        index.add_documents(["doc1"], ["Test content here"])

        doc = index.get_document("doc1")
        assert doc == "Test content here"

        # Non-existent document
        doc = index.get_document("nonexistent")
        assert doc is None

    def test_remove_document(self):
        """Test document removal."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2", "doc3"],
            ["First doc", "Second doc", "Third doc"]
        )

        assert index.doc_count == 3

        index.remove_document("doc2")

        assert index.doc_count == 2
        assert "doc2" not in index.doc_ids
        assert index.get_document("doc2") is None

    def test_save_and_load(self, tmp_path):
        """Test index persistence."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2"],
            ["First document content", "Second document content"]
        )

        # Save
        save_path = tmp_path / "bm25_index.json"
        index.save(str(save_path))

        # Load
        loaded_index = BM25Index.load(str(save_path))

        assert loaded_index.doc_count == 2
        assert "doc1" in loaded_index.doc_ids
        assert loaded_index.get_document("doc1") == "First document content"

        # Search should work
        results = loaded_index.search("first", k=1)
        assert len(results) > 0

    def test_unicode_handling(self):
        """Test handling of unicode text."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2"],
            [
                "Hello 世界 こんにちは",
                "Bonjour le monde café"
            ]
        )

        results = index.search("世界", k=1)
        # Should handle unicode without errors
        assert isinstance(results, list)

    def test_empty_query(self):
        """Test with empty query."""
        index = BM25Index()
        index.add_documents(["doc1"], ["Some content"])

        results = index.search("", k=5)
        assert results == []

    def test_query_with_only_stopwords(self):
        """Test query containing only stopwords."""
        index = BM25Index()
        index.add_documents(["doc1"], ["Some content here"])

        results = index.search("the a an is", k=5)
        assert results == []


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_basic_creation(self):
        """Test basic SearchResult creation."""
        result = SearchResult(
            doc_id="doc1",
            text="Test content",
            score=0.95
        )

        assert result.doc_id == "doc1"
        assert result.text == "Test content"
        assert result.score == 0.95
        assert result.metadata == {}
        assert result.source_scores == {}

    def test_with_metadata(self):
        """Test SearchResult with metadata."""
        result = SearchResult(
            doc_id="doc1",
            text="Test",
            score=0.9,
            metadata={"path": "/test/file.txt"},
            source_scores={"vector": 0.85, "bm25": 0.95}
        )

        assert result.metadata["path"] == "/test/file.txt"
        assert result.source_scores["vector"] == 0.85


class TestSearchConfig:
    """Tests for SearchConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = SearchConfig()

        assert config.method == SearchMethod.HYBRID
        assert config.fusion == FusionMethod.RRF
        assert config.vector_weight == 0.7
        assert config.bm25_weight == 0.3
        assert config.use_reranker is False

    def test_custom_config(self):
        """Test custom configuration."""
        config = SearchConfig(
            method=SearchMethod.VECTOR,
            fusion=FusionMethod.WEIGHTED,
            vector_weight=0.8,
            bm25_weight=0.2,
            use_reranker=True
        )

        assert config.method == SearchMethod.VECTOR
        assert config.fusion == FusionMethod.WEIGHTED
        assert config.vector_weight == 0.8


class TestHybridSearcher:
    """Tests for HybridSearcher."""

    def test_creation(self):
        """Test basic creation."""
        searcher = HybridSearcher()
        assert searcher.config is not None

    def test_with_config(self):
        """Test creation with custom config."""
        config = SearchConfig(method=SearchMethod.BM25)
        searcher = HybridSearcher(config=config)

        assert searcher.config.method == SearchMethod.BM25

    def test_build_bm25_index(self):
        """Test building BM25 index."""
        searcher = HybridSearcher()
        searcher.build_bm25_index(
            ["doc1", "doc2"],
            ["First document", "Second document"]
        )

        assert searcher.bm25_index is not None
        assert searcher.bm25_index.doc_count == 2

    def test_save_and_load_bm25(self, tmp_path):
        """Test BM25 index persistence through searcher."""
        searcher = HybridSearcher()
        searcher.build_bm25_index(
            ["doc1", "doc2"],
            ["First document", "Second document"]
        )

        save_path = tmp_path / "bm25.json"
        searcher.save_bm25_index(str(save_path))

        # Create new searcher and load
        new_searcher = HybridSearcher()
        new_searcher.load_bm25_index(str(save_path))

        assert new_searcher.bm25_index is not None
        assert new_searcher.bm25_index.doc_count == 2


class TestFusionMethods:
    """Tests for result fusion methods."""

    def test_rrf_fusion(self):
        """Test Reciprocal Rank Fusion."""
        config = SearchConfig(fusion=FusionMethod.RRF, rrf_k=60)
        searcher = HybridSearcher(config=config)

        # Create mock result sets
        vector_results = [
            SearchResult("doc1", "text1", 0.9),
            SearchResult("doc2", "text2", 0.8),
            SearchResult("doc3", "text3", 0.7),
        ]
        bm25_results = [
            SearchResult("doc2", "text2", 0.95),
            SearchResult("doc1", "text1", 0.85),
            SearchResult("doc4", "text4", 0.75),
        ]

        result_sets = [
            ("vector", vector_results),
            ("bm25", bm25_results)
        ]

        fused = searcher._rrf_fusion(result_sets, k=5)

        # doc1 and doc2 appear in both, should rank higher
        doc_ids = [r.doc_id for r in fused]
        assert "doc1" in doc_ids[:3]
        assert "doc2" in doc_ids[:3]

    def test_weighted_fusion(self):
        """Test weighted score fusion."""
        config = SearchConfig(
            fusion=FusionMethod.WEIGHTED,
            vector_weight=0.6,
            bm25_weight=0.4
        )
        searcher = HybridSearcher(config=config)

        vector_results = [
            SearchResult("doc1", "text1", 1.0, source_scores={"vector": 1.0}),
            SearchResult("doc2", "text2", 0.5, source_scores={"vector": 0.5}),
        ]
        bm25_results = [
            SearchResult("doc2", "text2", 1.0, source_scores={"bm25": 1.0}),
            SearchResult("doc1", "text1", 0.5, source_scores={"bm25": 0.5}),
        ]

        result_sets = [
            ("vector", vector_results),
            ("bm25", bm25_results)
        ]

        fused = searcher._weighted_fusion(result_sets, k=2)

        # Both docs should be present
        doc_ids = [r.doc_id for r in fused]
        assert len(doc_ids) == 2

    def test_max_fusion(self):
        """Test max score fusion."""
        config = SearchConfig(fusion=FusionMethod.MAX)
        searcher = HybridSearcher(config=config)

        vector_results = [
            SearchResult("doc1", "text1", 0.9),
            SearchResult("doc2", "text2", 0.3),
        ]
        bm25_results = [
            SearchResult("doc2", "text2", 0.95),
            SearchResult("doc1", "text1", 0.4),
        ]

        result_sets = [
            ("vector", vector_results),
            ("bm25", bm25_results)
        ]

        fused = searcher._max_fusion(result_sets, k=2)

        # doc2 should be first (max score 0.95 vs doc1's 0.9)
        assert fused[0].doc_id == "doc2"
        assert fused[0].score == 0.95


class TestCreateHybridSearcher:
    """Tests for create_hybrid_searcher factory function."""

    def test_default_creation(self):
        """Test default searcher creation."""
        searcher = create_hybrid_searcher()

        assert searcher.config.method == SearchMethod.HYBRID

    def test_custom_method(self):
        """Test with custom method."""
        searcher = create_hybrid_searcher(method="vector")

        assert searcher.config.method == SearchMethod.VECTOR

    def test_custom_weights(self):
        """Test with custom weights."""
        searcher = create_hybrid_searcher(
            vector_weight=0.8,
            bm25_weight=0.2
        )

        assert searcher.config.vector_weight == 0.8
        assert searcher.config.bm25_weight == 0.2

    def test_with_reranker(self):
        """Test with reranker enabled."""
        searcher = create_hybrid_searcher(use_reranker=True)

        assert searcher.config.use_reranker is True


class TestBM25EdgeCases:
    """Edge case tests for BM25."""

    def test_duplicate_documents(self):
        """Test handling of duplicate document IDs."""
        index = BM25Index()
        index.add_documents(["doc1"], ["First version"])
        index.add_documents(["doc1"], ["Second version"])

        # Should have both (or last one depending on implementation)
        # At minimum, should not crash
        assert index.doc_count >= 1

    def test_very_long_document(self):
        """Test with very long document."""
        index = BM25Index()
        long_text = "word " * 10000
        index.add_documents(["doc1"], [long_text])

        results = index.search("word", k=1)
        assert len(results) == 1

    def test_special_characters_in_text(self):
        """Test handling of special characters."""
        index = BM25Index()
        index.add_documents(
            ["doc1"],
            ["Hello! @#$%^&*() World... <html>test</html>"]
        )

        results = index.search("hello world", k=1)
        assert len(results) > 0

    def test_numbers_in_text(self):
        """Test handling of numbers."""
        index = BM25Index()
        index.add_documents(
            ["doc1", "doc2"],
            ["Version 2.0 release", "Version 3.0 update"]
        )

        results = index.search("version 2", k=2)
        assert len(results) >= 1

    def test_case_insensitivity(self):
        """Test case insensitive search."""
        index = BM25Index()
        index.add_documents(["doc1"], ["Python Programming LANGUAGE"])

        results_lower = index.search("python programming language", k=1)
        results_upper = index.search("PYTHON PROGRAMMING LANGUAGE", k=1)
        results_mixed = index.search("Python PROGRAMMING Language", k=1)

        # All should find the same document
        assert len(results_lower) == len(results_upper) == len(results_mixed) == 1
