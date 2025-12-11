# Changelog

## [0.1.2] - 2025-12-11

- Release 0.1.2

## [0.1.1] - 2025-12-11

- Release 0.1.1

All notable changes to Next Skill will be documented in this file.

## [0.1.0] - 2025-12-11

### Added
- Initial skill structure
- SKILL.md orchestrator (<100 lines)
- Discovery modules:
  - github-search.md - GitHub repository search
  - mcp-registry.md - MCP server registry search
- Analysis modules:
  - architecture-analyzer.md - External repo analysis
- Build modules:
  - refactor-engine.md - Adapt external code
  - scaffold-generator.md - Create from templates
- Validation:
  - structure-validator.md - Compliance checking
- Templates:
  - skill-skeleton/ - Full skill template
  - patterns/ - Reusable pattern modules (inbox, database, scoring, scraping, output)
- Configuration:
  - sources.yaml - GitHub repos and MCP registries

### Commands
- `create skill: [description]` - Full workflow
- `search skills: [query]` - Discovery only
- `scaffold: [name]` - Create from scratch
- `adapt: [github-url]` - Refactor external repo
- `validate skill: [name]` - Check compliance

### Patterns
- scaffold
- search
