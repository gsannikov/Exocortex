# Changelog

## [1.3.1] - 2025-12-10

- Release 1.3.1

## [1.3.0] - 2025-12-10

- Release 1.3.0

## [1.2.0] - 2025-12-09

- Release 1.2.0

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.0] - 2025-11-21
### Added
- **Debug Mode**: Developer console (`/debug`) for prompt inspection and tool testing.
- **Agent Workflow**: New `.agent/workflows/update_module.md` for automated dependency management.
- **Documentation**: Feature spec for Debug Mode and updated architecture docs.

## [1.0.0] - 2025-11-21

### Added
- **Customizable Scoring System**: Interactive setup wizard for personalized job scoring weights
- **Market Investigation Module**: Company comparison, salary benchmarking, and trend analysis
- **Job Preparation Planner**: Detailed interview prep plans with hour breakdowns and study resources
- **MCP Server Detection**: Automatic detection with blocking for required servers and guided setup
- **Setup Wizard Module**: 6-question questionnaire to customize scoring priorities
- **Weight Validation**: Comprehensive validation ensuring weights sum to 100 and are reasonable

### Changed
- **Generic Examples**: Removed all personal data from examples (paths, compensation data)
- **Enhanced Configuration Flow**: Step-by-step setup with MCP detection before operations
- **Scoring Module**: Now supports both default and custom weights with validation
- **Welcome Message**: Updated to use generic placeholders instead of personal paths

### Fixed
- **Bug #1**: Hardcoded scoring weights - now fully customizable via interactive wizard
- **Bug #2**: Personal data in examples - replaced with `<username>` placeholders


## [9.24.1] - 2025-11-20

### Added
- **Inbox Workflow**: "Capture First, Analyze Later" system for batch job processing
- **Smart Config**: Auto-updating scraper preferences based on success rates

### Fixed
- **Scraper Optimization**: Fixed scraper configuration persistence (Bug 1)
- **Data Structure**: Removed legacy `roles/` directory generation (Bug 2 & 3)
- **Batch Processing**: Resolved context window exhaustion during batch adds (Bug 4)
- **System Prompt**: Updated feature awareness in SKILL.md (Bug 5)
- **Cleanup**: Moved DEV_SESSION_STATE.md to user-data directory


## [9.13.0] - 2025-11-19

### Changed
- **Refactored Documentation**: Ultra-aggressive documentation consolidation reducing file count by 50-60%
- **Simplified Host Scripts**: Consolidated host_scripts to minimal Python + shell scripts
- **Removed Obsolete Files**: Cleaned up obsolete configuration and migration scripts
- **Updated Developer Guide**: Comprehensive updates to reflect new host_scripts structure

### Fixed
- Allow uppercase letters for consolidated guide filenames
- Updated documentation validation for simplified structure

## [9.10.0] - 2025-11-18

### Added
- Configurable scraping tool priorities for flexible data source selection

### Fixed
- Removed hardcoded username and added setup option for better portability
- Added initialization greeting to prevent auto-search behavior

### Changed
- Prioritized MCP_DOCKER for LinkedIn scraping
- Refactored user-data structure to v2

## [9.9.5] - 2025-11-17

### Fixed
- Syntax error in validator script

## [9.9.4] - 2025-11-17

### Changed
- Documentation cleanup and consolidation

---

## Release Notes for v9.13.0

This release focuses on codebase simplification and maintainability:

**Major Improvements:**
- Streamlined documentation structure with 50% fewer files
- Simplified automation tooling with consolidated scripts
- Improved developer experience with updated guides
- Cleaned up legacy code and obsolete configurations

**Breaking Changes:**
- None. All changes are internal refactoring.

**Migration Guide:**
- No migration needed. All changes are backward compatible.

**Known Issues:**
- None reported.

---

[9.13.0]: https://github.com/gsannikov/israeli-tech-career-consultant/compare/v9.10.0...v9.13.0
[9.10.0]: https://github.com/gsannikov/israeli-tech-career-consultant/compare/v9.9.5...v9.10.0
[9.9.5]: https://github.com/gsannikov/israeli-tech-career-consultant/compare/v9.9.4...v9.9.5
[9.9.4]: https://github.com/gsannikov/israeli-tech-career-consultant/releases/tag/v9.9.4
