# Exocortex Infrastructure

Architecture decisions, roadmap, and project management.

## 📊 Current State

**Version**: Monorepo v1.2.0
**Date**: 2025-12-11
**Skills**: 10 (job-analyzer, interview-prep, reading-list, ideas-capture, voice-memos, local-rag, recipe-manager, social-media-post, setup-manager, next-skill)

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

**Decision**: User data in configurable location outside repo (default: `~/exocortex-data/`).
Path configured in `shared/config/paths.py` - single source of truth.

**Rationale**:
- Clear separation of code and data
- Never risk committing personal data
- Easier backup/sync decisions
- Global config for cross-skill settings
- Configurable location (no hardcoded paths)
- Easy to move project/data folders without breaking paths

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

### ADR-006: Skill Structure Best Practices

**Decision**: All skills follow a standardized structure with SKILL.md as orchestrator (<100 lines) and detailed workflows in `references/`.

**Rationale**:
- Reduces context loading overhead
- Clear separation of concerns
- Consistent developer experience
- Easier maintenance and updates

**Structure**:
```
skill-name/
├── SKILL.md              # <100 lines, orchestrator
├── references/           # Detailed workflows
│   └── workflow.md
├── modules/              # Feature modules
├── scripts/              # Python utilities
└── config/               # Configuration
```

### ADR-007: Career Skill Split

**Decision**: Split career-consultant into two focused skills: job-analyzer and interview-prep.

**Rationale**:
- Natural workflow boundary (find jobs vs prepare for interviews)
- Reduced context per skill
- Clear handoff pattern via shared storage
- Better single responsibility

**Implementation**:
- Both skills share `~/exocortex-data/career/`
- job-analyzer writes analyses and tracking data
- interview-prep reads from shared storage, writes prep materials

## 🗺️ Roadmap

### Phase 1: Foundation (Complete ✅)
- [x] Monorepo structure
- [x] 4 skills migrated
- [x] Centralized user-data
- [x] Shared scripts (release, generator)
- [x] Root-level documentation
- [x] Full cleanup (nested .git, legacy folders, unified paths)

### Phase 2: Automation & Stability (Complete ✅)
- [x] GitHub Actions for validation
- [x] GitHub Actions for release
- [x] Dependency tracking system
- [x] Comprehensive Documentation Suite (Vision, FAQ, Contributing)
- [x] CI Fixes (Local RAG stability)
- [x] Skills refactoring (SKILL.md <100 lines)
- [x] Career skill split (job-analyzer + interview-prep)
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
| inbox | 9 (all except next-skill) |
| database | 9 (all except next-skill) |
| templates | next-skill |
| scoring | job-analyzer, ideas-capture |
| scraping | job-analyzer, reading-list |
| transcription | voice-memos |
| rag | local-rag |
| shared-storage | job-analyzer, interview-prep |

## 📁 Data Structure

```
~/exocortex-data/
├── career/                    # Shared by job-analyzer & interview-prep
│   ├── analyses/              # Job analysis YAML files
│   ├── jobs.xlsx              # Master tracker
│   ├── contacts.yaml          # Recruiter contacts
│   ├── reminders.yaml         # Follow-up reminders
│   ├── interview-prep/        # STAR stories, negotiations
│   └── config.yaml            # Shared config
├── reading-list/
├── ideas-capture/
├── voice-memos/
├── local-rag/
├── recipe-manager/
└── social-media-post/
```

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
| 2025-12-11 | New skill: next-skill (skill factory with GitHub discovery, MCP registry search, adaptation, scaffolding) |
| 2025-12-11 | Skills refactoring: All SKILL.md files <100 lines |
| 2025-12-11 | Career split: job-analyzer + interview-prep |
| 2025-12-11 | New modules: LinkedIn tracking, recruiter contacts, follow-up reminders, salary negotiation |
| 2025-12-11 | Path standardization: ~/exocortex-data/ |
| 2025-12-01 | CI Fixes: Local RAG stability & test coverage |
| 2025-12-01 | Documentation Suite: Vision, FAQ, Issue Templates |
| 2025-11-30 | Recipe Manager & Social Media Post skills added |
| 2025-11-25 | Dependency tracking system (ADR-005) |
| 2025-11-25 | CI integration for dependency checks |
| 2025-11-25 | local-rag skill added |
| 2024-11-24 | Monorepo restructure |
| 2024-11-24 | Apple Notes inbox pattern added |
| 2024-11-24 | Centralized user-data |
| 2024-11-24 | Shared scripts created |
| 2024-11-24 | Full cleanup: removed nested .git, legacy folders, unified paths |
