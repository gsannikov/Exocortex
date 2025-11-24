# Changelog

All notable changes to the 2ndBrain_RAG project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation structure
  - `architecture.md` - System architecture and design
  - `problem-and-vision.md` - Project goals and philosophy
  - `agent-guide.md` - Guide for AI assistants
  - `changelog.md` - This file
  - `coding-conventions.md` - Code style guidelines
  - `roadmap.md` - Future plans
  - `features-and-bugs.md` - Known issues and planned features
  - `backlog.md` - Development backlog
  - `user-guides/` - User documentation

### Changed
- Documentation reorganized into `docs/` directory

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

---

## [0.2.0] - 2025-11-13

### Added
- OCR support with multiple engines:
  - Surya OCR (default, CPU-optimized)
  - PaddleOCR (optional)
  - DeepSeek-OCR (optional, high accuracy)
- File ingestion pipeline in `ingest/` directory
  - `extractor.py` - Text extraction from multiple formats
  - `ocr.py` - OCR engine integrations
  - `utils.py` - Helper utilities
- Automatic file watching with watchdog
- State tracking for indexed files (`state/ingest_state.json`)
- Hash-based change detection for efficient reindexing

### Changed
- Refactored document processing into separate modules
- Improved error handling for unsupported file types
- Enhanced chunking strategy with configurable overlap

### Fixed
- Fixed encoding issues with non-UTF8 documents
- Improved PDF text extraction reliability
- Better handling of empty or corrupted files

---

## [0.1.0] - 2025-10-22

### Added
- Initial project structure
- MCP server implementation with 5 core tools:
  - `rag.search` - Semantic search over documents
  - `rag.get` - Retrieve document excerpts
  - `rag.reindex` - Manual reindexing trigger
  - `rag.stats` - Index statistics
  - `rag.invalidate` - Remove documents from index
- ChromaDB integration for vector storage
- sentence-transformers for embeddings (`all-MiniLM-L6-v2`)
- Basic document loading (PDF, TXT, MD)
- Configuration via environment variables
- Claude Desktop integration guide
- Basic README with setup instructions

### Core Features
- Local-first architecture (no cloud dependencies)
- Privacy-preserving (documents never leave machine)
- Automatic persistent storage
- Cosine similarity search
- Configurable chunking (size and overlap)

---

## Version History

### Version Numbering

We use Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes or major feature rewrites
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

### Release Process

1. Update this CHANGELOG.md with changes
2. Update version in relevant files
3. Tag release: `git tag v0.x.x`
4. Push tags: `git push --tags`

---

## Categories

### Added
New features or capabilities added to the project.

### Changed
Changes to existing functionality.

### Deprecated
Features that will be removed in upcoming releases.

### Removed
Features or functionality that have been removed.

### Fixed
Bug fixes.

### Security
Security-related changes or fixes (vulnerabilities, security updates).

---

## Migration Guides

### Migrating from 0.1.x to 0.2.x

**Breaking Changes**: None

**New Features**:
- OCR support - automatically enabled for scanned PDFs
- File watcher - automatically reindexes on changes
- State tracking - faster reindexing by detecting changes

**Configuration Changes**:
```bash
# New environment variables (optional)
ROOT_DIR=/path/to/docs              # Replaces manual folder config
ALLOWED_EXTS=.pdf,.txt,.md          # Filter file types
CHUNK_SIZE=3000                     # Tune chunking
CHUNK_OVERLAP=400                   # Tune overlap
```

**Action Required**: None (backward compatible)

**Recommended**:
1. Copy `.env.example` to `.env`
2. Set `ROOT_DIR` to your documents folder
3. Restart MCP server
4. Trigger reindex for OCR benefits

---

## Upcoming Changes

See [roadmap.md](roadmap.md) for detailed future plans.

### Next Release (0.3.0) - Planned Q1 2025

**Focus**: Incremental indexing and cross-platform support

- Incremental reindexing (avoid full reindex on file change)
- Linux support and testing
- Intel Mac support
- Configuration validation and better error messages
- Performance monitoring and metrics

### Future Releases

- 0.4.0: Enhanced search (hybrid BM25 + semantic)
- 0.5.0: Multi-modal search (images, diagrams)
- 1.0.0: Stable API, production-ready features

---

## Contributing

When contributing changes:

1. **Update this file** under `[Unreleased]` section
2. **Choose correct category** (Added, Changed, Fixed, etc.)
3. **Write clear descriptions** (what changed and why)
4. **Reference issues** where applicable (#123)
5. **Note breaking changes** prominently

**Example entry**:
```markdown
### Added
- New search filter by date range (#123)
  - Allows users to limit search to specific time periods
  - Configurable via `date_from` and `date_to` parameters
```

---

## Links

- [Releases](https://github.com/yourusername/2ndBrain_RAG/releases)
- [Issues](https://github.com/yourusername/2ndBrain_RAG/issues)
- [Pull Requests](https://github.com/yourusername/2ndBrain_RAG/pulls)
- [Roadmap](roadmap.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

**Note**: This changelog is manually maintained. Each release should update the version number and move items from `[Unreleased]` to the new version section.

**Last Updated**: 2025-11-13
