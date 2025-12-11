# 🏭 Next Skill - Skill Factory

AI-assisted skill creation with GitHub discovery, adaptation, or fresh scaffolding.

## Commands

| Command | Action |
|---------|--------|
| `create skill: [description]` | Full workflow: discover → adapt/create → scaffold |
| `search skills: [query]` | Discovery only - show existing solutions |
| `scaffold: [name]` | Skip discovery, create from scratch |
| `adapt: [github-url]` | Refactor specific repo to our architecture |
| `validate skill: [name]` | Check existing skill compliance |

## Workflow

### Phase 1: Discovery
When user describes a skill need:
1. Search GitHub for similar implementations → `modules/github-search.md`
2. Search MCP registries → `modules/mcp-registry.md`
3. Present findings with match percentages
4. Recommend: adapt existing OR create fresh

### Phase 2: Build
**If adapting**: Load `modules/refactor-engine.md`
- Clone/analyze external code
- Map to Exocortex architecture
- Preserve useful logic, restructure layout

**If creating fresh**: Load `modules/scaffold-generator.md`
- Select patterns (inbox, database, scoring, scraping)
- Generate from templates

### Phase 3: Scaffold
Generate compliant structure:
```
{skill-name}/
├── SKILL.md              # <100 lines
├── references/workflow.md
├── modules/
├── _dev/                 # Design docs, TODOs
├── scripts/
├── config/
├── version.yaml
└── CHANGELOG.md
```

### Phase 4: Integrate
1. Create `~/exocortex-data/{skill}/` directory
2. Add to `shared/scripts/release.py`
3. Update `dependencies.yaml`
4. Validate with `modules/structure-validator.md`

## Module Loading

| Trigger | Load |
|---------|------|
| `create skill`, `search skills` | `modules/github-search.md` |
| MCP-related query | `modules/mcp-registry.md` |
| `adapt:` command | `modules/refactor-engine.md` |
| `scaffold:` command | `modules/scaffold-generator.md` |
| `validate skill` | `modules/structure-validator.md` |
| Architecture questions | `modules/architecture-analyzer.md` |

## Templates

- `templates/skill-skeleton/` - Full skill structure
- `templates/patterns/` - Reusable pattern modules

## Config

- `config/sources.yaml` - GitHub repos and search queries

## Storage

No persistent storage - generates into `packages/`

---
**Version**: 0.1.0 | **Patterns**: scaffold, search
