# Next Skill - Design Document

## Purpose

Meta-skill that creates other skills by:
1. Searching for existing implementations (GitHub, MCP registries)
2. Adapting found solutions to Exocortex architecture
3. Scaffolding from templates when nothing suitable exists

## User Stories

1. As a user, I want to quickly create new skills that follow consistent architecture
2. As a user, I want to leverage existing implementations rather than reinvent
3. As a user, I want proper structure including _dev metadata from the start

## Design Philosophy

### Discovery First
Before building anything, search for existing solutions. The best code is code you don't have to write.

### Adapt Over Create
When a good implementation exists, adapt it rather than starting fresh. This preserves battle-tested logic.

### Templates as Guardrails
Templates enforce architectural consistency and ensure all skills have proper structure from day one.

## Key Design Decisions

### Decision 1: No Persistent Storage
**Context**: Should next-skill maintain a database of created skills?
**Decision**: No - generates into packages/, relies on file system
**Rationale**: Simpler, avoids sync issues, skill metadata lives with skill

### Decision 2: Modular Search
**Context**: How to handle different search sources?
**Decision**: Separate modules for GitHub, MCP, etc.
**Rationale**: Easy to add new sources, each can evolve independently

### Decision 3: Pattern Library
**Context**: How to handle common skill patterns?
**Decision**: Template patterns that can be combined
**Rationale**: Reusable components, consistent implementations

### Decision 4: _dev Folder Convention
**Context**: Where to store skill development metadata?
**Decision**: Every skill gets _dev/ with design.md, todos.md
**Rationale**: Keeps development context with the skill, aids future maintenance

## Workflow Architecture

```
User Request
     │
     ▼
┌─────────────┐
│  Discovery  │ ── Search GitHub, MCP registries
└─────────────┘
     │
     ▼
┌─────────────┐
│   Decide    │ ── Adapt existing OR create fresh?
└─────────────┘
     │
     ├──────────────────┐
     ▼                  ▼
┌─────────────┐   ┌─────────────┐
│   Adapt     │   │  Scaffold   │
└─────────────┘   └─────────────┘
     │                  │
     └──────────────────┘
     │
     ▼
┌─────────────┐
│  Validate   │ ── Check compliance
└─────────────┘
     │
     ▼
┌─────────────┐
│  Integrate  │ ── Register in release.py, etc.
└─────────────┘
```

## Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| github-search | Search GitHub repos and code |
| mcp-registry | Search MCP server registries |
| architecture-analyzer | Analyze external repo structure |
| refactor-engine | Adapt external code |
| scaffold-generator | Create from templates |
| structure-validator | Verify compliance |

## Template System

### Skeleton Templates
Full skill structure with all files as templates.

### Pattern Templates
Reusable modules for common functionality:
- inbox: Apple Notes integration
- database: YAML storage
- scoring: Multi-dimensional evaluation
- scraping: Web content extraction
- output: Report/file generation

## Future Enhancements

- [ ] Interactive skill creation wizard
- [ ] Automatic dependency detection
- [ ] Skill marketplace integration
- [ ] Version upgrade assistance
- [ ] Cross-skill dependency management

## Created

- **Date**: 2025-12-11
- **Author**: Exocortex team
- **Version**: 0.1.0
