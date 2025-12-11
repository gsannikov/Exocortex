# Changelog

All notable changes to the Claude Skills Ecosystem will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Monorepo v1.0.0] - 2025-11-25

### Added
- **Root README.md** - Comprehensive monorepo documentation
- **CONTRIBUTING.md** - Contribution guidelines
- **Root CHANGELOG.md** - This file
- **GitHub Actions** - Automated validation and release workflows
- **Git tags** - Version tags for all skills

### Skills Included

| Skill | Version | Status |
|-------|---------|--------|
| career-consultant | v1.1.1 | Stable |
| reading-list | v1.0.0 | Stable |
| ideas-capture | v1.0.0 | Stable |
| voice-memos | v1.0.0 | Stable |
| local-rag | v1.0.0 | Stable |

---

## [Initial Restructure] - 2024-11-24

### Added
- Monorepo structure with `packages/` directory
- Centralized user-data pattern (`~/MyDrive/claude-skills-data/`)
- Shared scripts for release and skill generation
- Apple Notes inbox pattern across all skills
- Unified path configuration

### Changed
- Migrated from separate repositories to monorepo
- Standardized skill structure (SKILL.md, README.md, version.yaml)
- Unified documentation patterns

### Fixed
- Removed nested `.git` directories
- Cleaned up legacy folder structures
- Unified path references

---

## Skill-Specific Changelogs

For detailed changes to individual skills, see:

- [career-consultant/CHANGELOG.md](packages/career-consultant/CHANGELOG.md)
- [reading-list/CHANGELOG.md](packages/reading-list/CHANGELOG.md)
- [ideas-capture/CHANGELOG.md](packages/ideas-capture/CHANGELOG.md)
- [voice-memos/CHANGELOG.md](packages/voice-memos/CHANGELOG.md)
- [local-rag/CHANGELOG.md](packages/local-rag/CHANGELOG.md)

---

## Versioning Strategy

### Monorepo Version
The monorepo has its own version tracking major infrastructure changes.

### Skill Versions
Each skill is versioned independently:
- Tags: `{skill}-v{version}` (e.g., `career-consultant-v1.1.1`)
- Version file: `packages/{skill}/version.yaml`

### Version Bumping
- **patch**: Bug fixes, documentation updates
- **minor**: New features, non-breaking changes
- **major**: Breaking changes, major restructuring

---

## Release Process

### Automated (Recommended)
```bash
# Via GitHub Actions
# Go to Actions → Release Skill → Select skill and bump type
```

### Manual
```bash
# Release a specific skill
python shared/scripts/release.py career-consultant --patch

# Release all skills
python shared/scripts/release.py all --patch
```

---

## Links

- [Full Roadmap](docs/project-status.md)
- [Contributing Guide](CONTRIBUTING.md)
- [GitHub Releases](https://github.com/gsannikov/claude-skills/releases)
