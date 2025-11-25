# Claude Skills Project

Architecture decisions, roadmap, and project management.

## 📊 Current State

**Version**: Monorepo v1.1.0
**Date**: 2025-11-25
**Skills**: 5 (career-consultant, reading-list, ideas-capture, voice-memos, local-rag)

## 🏗️ Architecture Decisions

### ADR-001: Monorepo over Submodules

**Decision**: Use monorepo with `packages/` folder instead of git submodules.

**Rationale**:
- Simpler CI/CD
- Atomic changes across skills
- Shared tooling without duplication
- Easier refactoring
- Submodules add complexity for solo dev

### ADR-002: Centralized User Data

**Decision**: User data in `~/MyDrive/claude-skills-data/` outside repo.

**Rationale**:
- Clear separation of code and data
- Never risk committing personal data
- Easier backup/sync decisions
- Global config for cross-skill settings

### ADR-003: Apple Notes Inbox Pattern

**Decision**: All skills use Apple Notes for mobile-friendly capture.

**Rationale**:
- Mobile capture without app development
- Sync via iCloud
- Simple text-based parsing
- Universal pattern across skills

### ADR-004: YAML for Structured Data

**Decision**: Use YAML over JSON or SQLite.

**Rationale**:
- Human readable/editable
- Git-friendly diffs
- Comment support
- Good balance of structure and flexibility

### ADR-005: Dependency Tracking for Documentation

**Decision**: Use a dependency graph (`dependencies.yaml`) to track relationships between files and ensure documentation stays in sync.

**Rationale**:
- Cascading updates: Code → README → USER_GUIDE → Marketing
- CI integration warns on PRs, blocks releases if out of sync
- Claude commands (`/refactor`, `/deps`) for easy updates
- Prevents documentation drift in monorepo

**Components**:
- `dependencies.yaml` - Dependency manifest
- `shared/scripts/dependency_tracker.py` - CLI tool
- `.claude/commands/refactor.md` - Slash command
- CI jobs in `validate.yml` and `release.yml`

## 🗺️ Roadmap

### Phase 1: Foundation (Complete ✅)
- [x] Monorepo structure
- [x] 4 skills migrated
- [x] Centralized user-data
- [x] Shared scripts (release, generator)
- [x] Root-level documentation
- [x] Full cleanup (nested .git, legacy folders, unified paths)

### Phase 2: Automation (In Progress)
- [x] GitHub Actions for validation
- [x] GitHub Actions for release
- [x] Dependency tracking system
- [ ] Automated changelog generation
- [ ] Cross-skill tests

### Phase 3: Enhancement
- [ ] Notion integration
- [ ] Google Drive backup automation
- [ ] CLI tool for local operations
- [ ] Web dashboard (stretch)

### Phase 4: Sharing
- [ ] Public skill template
- [ ] Documentation site
- [ ] Example skills gallery

## 📈 Metrics

Track per skill:
- Items processed
- Last activity
- Version history
- User satisfaction

## 🔄 Release Process

1. **Validation**: Run tests, lint
2. **Version Bump**: Update version.yaml
3. **Changelog**: Update CHANGELOG.md
4. **Commit**: "Release {skill} v{version}"
5. **Tag**: `{skill}-v{version}`
6. **Push**: `git push origin main --tags`

## 🧩 Skill Patterns

| Pattern | Skills Using |
|---------|-------------|
| inbox | All 5 |
| database | All 5 |
| scoring | career-consultant, ideas-capture |
| scraping | career-consultant, reading-list |
| transcription | voice-memos |
| rag | local-rag |

## 📝 Notes

### Known Issues
- Apple Notes timeout with large updates (>100 items)
- Firecrawl rate limits on bulk scraping

### Workarounds
- Keep processed section as stats only
- Batch scraping with delays
- Fallback to web_fetch when needed

## 📅 Change Log

| Date | Change |
|------|--------|
| 2025-11-25 | Dependency tracking system (ADR-005) |
| 2025-11-25 | CI integration for dependency checks |
| 2025-11-25 | local-rag skill added |
| 2024-11-24 | Monorepo restructure |
| 2024-11-24 | Apple Notes inbox pattern added |
| 2024-11-24 | Centralized user-data |
| 2024-11-24 | Shared scripts created |
| 2024-11-24 | Full cleanup: removed nested .git, legacy folders, unified paths |
