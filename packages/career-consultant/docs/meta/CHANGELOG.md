# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- STAR Framework Phase 3: Library Management
- STAR Framework Phase 5: Practice Mode
- STAR Framework Phase 6: Polish & Documentation
- User Minimal Rampup (onboarding wizard)
- Resume Generation feature
- Cover letter generation feature
- GitHub Actions workflows for CI/CD

### In Progress
- STAR Framework Phase 4: Job Integration (current)

## [9.6.0] - 2025-10-30

### Added
- Option to skip version bump during release creation
- Critical bug resolution documentation for Directory Tree Token Exhaustion

### Changed
- Refactored host scripts for improved structure and functionality
- Updated documentation with version 9.6.0 references

### Fixed
- Syntax error in version.yaml
- Critical bugs related to Notion integration and path initialization

## [9.5.0] - 2025-10-30

### Added
- Resume Generation System feature specification
- Enhanced documentation structure

### Changed
- Updated version to 9.5.0 across all modules
- Improved release tooling and automation

## [9.4.0] - 2025-10-30

### Added - STAR Framework Core (Phases 1-2)
- **STAR Framework Module v1.1** (`star-framework.md`)
  - Interactive story builder with guided Q&A
  - 100-point quality scoring system
  - 6-step refinement workflow with priority levels
  - Support for 7 competency categories
- **STAR Scoring System Reference** (`star-scoring-system.md`)
  - Detailed 100-point scoring rubric
  - Section-by-section criteria with examples
  - Improvement suggestion framework
  - Common scoring mistakes guide
- **STAR Templates and Examples**
  - YAML story template with full metadata
  - Question database with 50+ behavioral questions
  - 5 high-quality example stories
- **STAR Storage Infrastructure**
  - `user-data/interview-prep/star-stories/` directory
  - Story library with index.yaml
  - Interview session tracking

### Changed
- Enhanced star-framework.md from v1.0 to v1.1 with refinement workflow

### Fixed
- STAR scoring consistency validated (87/100 test score)

## [9.3.0] - 2025-10-30

### Added - Documentation & Planning
- **STAR Framework Feature Specification** (600+ lines)
  - Complete 5-component system design
  - 6-phase implementation plan
  - Success metrics and KPIs
- **Marketing Content**
  - Product positioning and messaging
  - Target audience definitions
  - Value proposition statements
- **Career Guard Vision Feature**
  - Long-term product vision
  - Integration roadmap

### Changed
- **Roadmap Restructure**
  - Reorganized priorities into clear phases
  - Identified MVP requirements
  - Established pre-launch tasks

## [9.2.0] - 2025-10-30

### Added
- Session state management system
- Archive documentation structure
- GitHub workflow validation

### Changed
- Improved documentation organization
- Enhanced project structure

## [9.1.0] - 2025-10-29

### Added
- **Job Backlog Manager**: Quick capture mode for jobs (~3-5K tokens vs 25-35K)
- Batch processing support for multiple job URLs
- Organized backlog storage (pending/archived folders)
- Smart tool selection based on job platform
- Centralized version management via `version.yaml`
- MIT License and CONTRIBUTING.md
- Enhanced .gitignore with comprehensive rules
- GitHub issue and PR templates
- CODE_OF_CONDUCT.md
- CHANGELOG.md (this file)

### Changed
- Tool selection strategy: Bright Data for LinkedIn, Firecrawl for others
- Updated README with badges and license info
- Improved documentation structure
- Version format to semantic versioning (9.1.0)

### Fixed
- Token usage optimization for quick job capture

## [9.0.0] - 2025-10-28

### Added
- Dynamic configuration via `user-config.yaml`
- Support for 1 to N CV variants
- Configurable scoring weights and thresholds
- User-specific bonuses and preferences
- Complete separation of generic skill from user data

### Changed
- Architecture to hybrid modular design
- All personalization moved to config file
- Made skill fully generic and reusable

### Removed
- Hardcoded user-specific settings

## [8.1.0] - 2025-10-27

### Added
- YAML frontmatter structure for all files
- Automated Excel database sync
- kebab-case naming conventions

### Changed
- Migrated from plain markdown to YAML + markdown
- File naming conventions standardized

## [8.0.0] - 2025-10-26

### Added
- Modular architecture with 6 core modules
- On-demand module loading
- Reference files for code examples
- Token efficiency improvements

### Changed
- Split monolithic skill into focused modules
- Progressive module loading strategy

## [7.0.0] - 2025-10-25

### Added
- Multi-CV support
- Advanced scoring system (6 components)
- Company research caching
- Excel database integration

## [6.0.0] - 2025-10-24

### Added
- Initial public release
- Basic job analysis
- Company profiles
- Scoring system
- Database operations

---

## Version History Summary

| Version | Date | Codename | Key Feature |
|---------|------|----------|-------------|
| 9.6.0 | 2025-10-30 | Backlog Feature | Bug fixes & tooling improvements |
| 9.5.0 | 2025-10-30 | Resume Generation | Resume system specification |
| 9.4.0 | 2025-10-30 | STAR Framework | Interview prep system (Phases 1-2) |
| 9.3.0 | 2025-10-30 | Documentation | Marketing & planning content |
| 9.2.0 | 2025-10-30 | Archive Structure | Session state & GitHub validation |
| 9.1.0 | 2025-10-29 | Backlog Feature | Job backlog manager |
| 9.0.0 | 2025-10-28 | Dynamic Config | user-config.yaml system |
| 8.1.0 | 2025-10-27 | YAML Migration | Frontmatter structure |
| 8.0.0 | 2025-10-26 | Modular | Split into modules |
| 7.0.0 | 2025-10-25 | Multi-CV | Multiple CV support |
| 6.0.0 | 2025-10-24 | Genesis | Initial release |

---

## Notes

- **Breaking changes** are indicated with MAJOR version bumps
- **New features** increment MINOR version
- **Bug fixes** and minor improvements increment PATCH version
- See [version.yaml](version.yaml) for current version
