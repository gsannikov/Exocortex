# Roadmap

## Vision

Transform 2ndBrain_RAG from a personal RAG tool into a robust, cross-platform knowledge assistant that seamlessly integrates with AI tools while maintaining privacy and simplicity.

---

## Release Timeline

### Q4 2024 - Foundation ✅

**Status**: Completed

**Goals**: Establish core functionality and MCP integration

- [x] MCP server with 5 core tools
- [x] ChromaDB vector storage
- [x] Basic document ingestion (PDF, TXT, MD)
- [x] Sentence-transformer embeddings
- [x] Claude Desktop integration
- [x] Configuration via environment variables

---

### Q1 2025 - Enhancement (Current)

**Status**: In Progress

**Theme**: Improve robustness, add OCR, enable auto-indexing

#### Completed
- [x] OCR support (Surya, PaddleOCR, DeepSeek)
- [x] File watcher for auto-reindexing
- [x] State tracking for efficient reindexing
- [x] Refactored ingestion pipeline
- [x] Comprehensive documentation structure

#### In Progress
- [ ] Incremental indexing (avoid full reindex)
- [ ] Error recovery and retry logic
- [ ] Configuration validation
- [ ] Performance monitoring

#### Planned
- [ ] Linux support and testing
- [ ] Intel Mac support
- [ ] Improved logging and debugging
- [ ] Basic health checks

**Target**: v0.3.0 by end of Q1 2025

---

### Q2 2025 - Polish

**Theme**: User experience and reliability

#### Features
- [ ] Configuration UI/TUI for easier setup
- [ ] Better error messages and user feedback
- [ ] Installation script (one-command setup)
- [ ] Improved search relevance (tuning)
- [ ] Windows support (experimental)

#### Quality
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Performance benchmarks
- [ ] Memory leak detection and fixes
- [ ] Crash reporting and recovery

#### Documentation
- [ ] Video tutorials
- [ ] Troubleshooting guide
- [ ] Migration guide for upgrades
- [ ] API documentation

**Target**: v0.4.0 by end of Q2 2025

---

### Q3 2025 - Advanced Features

**Theme**: Enhanced search and multi-modal support

#### Search Improvements
- [ ] Hybrid search (BM25 + semantic)
- [ ] Query expansion and rewriting
- [ ] Temporal search ("when did I work on X?")
- [ ] Fuzzy matching for names and terms
- [ ] Search history and suggestions

#### Multi-Modal
- [ ] Image search (visual similarity)
- [ ] Diagram understanding (OCR + layout)
- [ ] Code snippet extraction and search
- [ ] Table extraction and querying

#### Performance
- [ ] Optimize embedding generation
- [ ] Lazy loading for large documents
- [ ] Caching layer for frequent queries
- [ ] Batch processing improvements

**Target**: v0.5.0 by end of Q3 2025

---

### Q4 2025 - Ecosystem

**Theme**: Extensibility and integration

#### Plugin System
- [ ] Custom document extractors
- [ ] Alternative embedding models
- [ ] Custom chunking strategies
- [ ] Post-processing hooks

#### Integrations
- [ ] Other MCP-enabled tools
- [ ] Obsidian plugin
- [ ] Notion import/export
- [ ] Zotero bibliography sync
- [ ] Git repository indexing

#### Collaboration
- [ ] Multi-device sync protocol (still local)
- [ ] Shared collections (optional)
- [ ] Team knowledge bases
- [ ] Access controls and permissions

**Target**: v0.6.0 by end of Q4 2025

---

### 2026 - Maturity

**Theme**: Production-ready and stable

#### Stability
- [ ] v1.0.0 release (stable API)
- [ ] Long-term support (LTS) version
- [ ] Security audit and hardening
- [ ] Performance optimization
- [ ] Comprehensive monitoring

#### Enterprise Features (Optional)
- [ ] Multi-user support
- [ ] Role-based access control (RBAC)
- [ ] Audit logging
- [ ] Backup and restore
- [ ] High availability setup

#### Community
- [ ] Plugin marketplace
- [ ] Community contributions
- [ ] Documentation translations
- [ ] User forums and support

**Target**: v1.0.0 by mid-2026

---

## Feature Details

### High Priority

#### 1. Incremental Indexing (Q1 2025)

**Problem**: Currently reindexes entire file on any change
**Solution**: Track chunks separately, update only changed sections
**Benefits**: Faster reindexing, less resource usage
**Complexity**: Medium
**Impact**: High

**Implementation**:
- Store chunk-level hashes
- Compare hashes on file change
- Update only modified chunks
- Maintain chunk metadata

**Status**: Planned for v0.3.0

---

#### 2. Hybrid Search (Q3 2025)

**Problem**: Semantic search misses exact keyword matches
**Solution**: Combine BM25 (keyword) + semantic (embedding) scores
**Benefits**: Better accuracy, handles both use cases
**Complexity**: Medium
**Impact**: High

**Implementation**:
- Add BM25 index alongside vectors
- Score fusion algorithm (RRF or linear)
- Configurable weighting
- Benchmarking suite

**Status**: Planned for v0.5.0

---

#### 3. Configuration UI (Q2 2025)

**Problem**: `.env` files are not beginner-friendly
**Solution**: Interactive TUI for configuration
**Benefits**: Easier onboarding, validation, discoverability
**Complexity**: Low
**Impact**: Medium

**Implementation**:
- Use `rich` or `textual` for TUI
- Validate inputs before saving
- Show current config
- Quick setup wizard

**Status**: Planned for v0.4.0

---

### Medium Priority

#### 4. Multi-Modal Search (Q3 2025)

**Problem**: Can't search images or diagrams
**Solution**: Add visual embedding and search
**Benefits**: Complete coverage of document types
**Complexity**: High
**Impact**: Medium

**Dependencies**: CLIP or similar model

---

#### 5. Plugin System (Q4 2025)

**Problem**: Hard to add custom extractors or processors
**Solution**: Plugin API with hooks
**Benefits**: Community extensibility
**Complexity**: High
**Impact**: Medium

**API Design**:
```python
class Plugin:
    def on_extract(self, path: Path) -> Optional[str]:
        """Custom extraction logic."""
        pass

    def on_chunk(self, text: str) -> list[str]:
        """Custom chunking logic."""
        pass
```

---

#### 6. Cross-Platform Support (Q1-Q2 2025)

**Problem**: Currently optimized for Mac M-series
**Solution**: Test and optimize for Linux, Intel Mac, Windows
**Benefits**: Wider adoption
**Complexity**: Medium
**Impact**: Medium

**Tasks**:
- CI testing on multiple platforms
- Platform-specific installation guides
- Handle platform differences (paths, OCR engines)

---

### Low Priority

#### 7. Collaborative Features (Q4 2025)

**Problem**: No multi-user or sync capabilities
**Solution**: Optional sync protocol (still local-first)
**Benefits**: Multi-device workflows
**Complexity**: Very High
**Impact**: Low (niche use case)

---

#### 8. Advanced Analytics (2026)

**Problem**: No insights into usage or corpus
**Solution**: Usage analytics, corpus visualization
**Benefits**: Understanding knowledge graph
**Complexity**: High
**Impact**: Low

---

## Non-Goals

We explicitly will **NOT** pursue:

1. **Cloud/SaaS Version**: Contradicts privacy-first vision
2. **Mobile Apps**: Desktop-focused tool
3. **Real-Time Collaboration**: Out of scope complexity
4. **Web Interface**: MCP integration is primary UX
5. **AI Training**: Not a model training tool
6. **Blockchain/Web3**: No decentralization needs

---

## Versioning Strategy

### Semantic Versioning

- **0.x.x**: Pre-1.0, breaking changes allowed
- **1.0.0**: Stable API, backward compatibility guaranteed
- **1.x.x**: Minor versions, new features
- **1.x.y**: Patch versions, bug fixes only

### Breaking Changes

Before 1.0.0:
- Breaking changes allowed in minor versions (0.x.0)
- Clearly documented in CHANGELOG
- Migration guide provided

After 1.0.0:
- Breaking changes only in major versions (2.0.0)
- Deprecation warnings in prior minor version
- Support for migration from N-1 major version

---

## Community Involvement

### How to Contribute

**Code**:
- Check [backlog.md](backlog.md) for tasks
- See [features-and-bugs.md](features-and-bugs.md) for open issues
- Follow [coding-conventions.md](coding-conventions.md)

**Documentation**:
- Improve existing docs
- Add examples and tutorials
- Translate to other languages

**Testing**:
- Test on different platforms
- Report bugs and edge cases
- Performance benchmarking

**Ideas**:
- Propose features (open issue)
- Discuss architecture (open discussion)
- Share use cases and workflows

---

## Success Metrics

### Quantitative

| Metric | Current | Q2 2025 | Q4 2025 | 2026 |
|--------|---------|---------|---------|------|
| Supported formats | 10+ | 15+ | 20+ | 25+ |
| Index speed (docs/min) | ~100 | ~200 | ~300 | ~500 |
| Search latency (ms) | ~150 | ~100 | ~50 | ~50 |
| Corpus size (docs) | 10k | 50k | 100k | 500k |
| Platforms supported | 1 | 3 | 4 | 4 |
| GitHub stars | - | 100 | 500 | 1000 |
| Active users | - | 50 | 200 | 1000 |

### Qualitative

- [ ] "Just works" for 90% of users (no troubleshooting)
- [ ] Integrates seamlessly with Claude workflow
- [ ] Trusted by privacy-conscious users
- [ ] Active community contributions
- [ ] Referenced in RAG best practices

---

## Dependencies and Risks

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ChromaDB limitations | Medium | High | Evaluate Qdrant, Weaviate as alternatives |
| OCR accuracy issues | High | Medium | Support multiple engines, user feedback |
| Performance degradation | Medium | High | Benchmarking, profiling, optimization |
| MCP protocol changes | Low | High | Stay updated, contribute to spec |
| Platform compatibility | Medium | Medium | CI testing, community feedback |

### Resource Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Maintainer burnout | Medium | High | Community involvement, co-maintainers |
| Lack of contributors | Medium | Medium | Good docs, welcoming community |
| Funding for hosting | Low | Low | No hosting needed (local-first) |
| Legal/licensing | Low | High | Use permissive licenses, legal review |

---

## Milestones

### v0.3.0 - Robust Foundation (Q1 2025)
- Incremental indexing
- Cross-platform support
- Error recovery
- Performance monitoring

### v0.4.0 - User Experience (Q2 2025)
- Configuration UI
- Better error messages
- Installation script
- Test suite and CI

### v0.5.0 - Advanced Search (Q3 2025)
- Hybrid search (BM25 + semantic)
- Multi-modal support
- Query improvements
- Performance optimizations

### v0.6.0 - Extensibility (Q4 2025)
- Plugin system
- Integrations (Obsidian, etc.)
- Advanced features
- Community tools

### v1.0.0 - Stable Release (2026)
- Production-ready
- Stable API
- Security audit
- LTS support

---

## Feedback and Priorities

This roadmap is a living document. Priorities may shift based on:

- User feedback and feature requests
- Technical discoveries and limitations
- Community contributions
- MCP ecosystem evolution

**Your input matters**: Open an issue or discussion to:
- Suggest features
- Report pain points
- Share use cases
- Propose changes to priorities

---

## References

- [problem-and-vision.md](problem-and-vision.md) - Long-term vision
- [features-and-bugs.md](features-and-bugs.md) - Current issues
- [backlog.md](backlog.md) - Detailed task list
- [changelog.md](changelog.md) - Historical changes

---

**Last Updated**: 2025-11-13
**Next Review**: 2025-02-01 (quarterly review)

**Questions?** Open a discussion on GitHub.
