# Architecture Analyzer Module

## Overview

Analyzes external repository structure to determine adaptation strategy.

## Analysis Process

### Step 1: Detect Repository Type

| Type | Indicators | Adaptation Strategy |
|------|------------|---------------------|
| MCP Server | `mcp`, `@modelcontextprotocol` | Light wrapper |
| Python Package | `setup.py`, `pyproject.toml` | Extract core |
| Node Package | `package.json` | Convert to Python or wrap |
| CLI Tool | `argparse`, `click` | Extract logic |
| Monorepo | Multiple packages | Extract relevant part |

### Step 2: Map Structure

```
External Structure          →    Exocortex Mapping
─────────────────────────────────────────────────────
README.md                   →    SKILL.md (condensed)
docs/                       →    references/
src/                        →    scripts/
lib/                        →    scripts/
config.json, .env           →    config/paths.py
tests/                      →    tests/ (keep)
examples/                   →    references/examples.md
.github/                    →    (remove)
Dockerfile                  →    (remove)
```

### Step 3: Identify Core Logic

Look for:
- Main entry point (`main.py`, `index.js`, `cli.py`)
- Core business logic (not boilerplate)
- Utility functions worth keeping
- Configuration patterns

### Step 4: Dependency Assessment

```python
@dataclass
class DependencyAnalysis:
    required: List[str]      # Must have for functionality
    optional: List[str]      # Enhance but not essential
    replaceable: List[str]   # Can substitute with our patterns
    incompatible: List[str]  # Won't work, need alternative
```

**Common Replacements**:

| External | Exocortex Equivalent |
|----------|---------------------|
| SQLite/Postgres | YAML files |
| Redis | In-memory or file |
| REST API server | MCP tools |
| Web scraping (selenium) | Firecrawl/Bright Data |
| Config files | shared/config/paths.py |

### Step 5: Effort Estimation

| Factor | Low (1-2h) | Medium (2-4h) | High (4-8h) |
|--------|------------|---------------|-------------|
| Structure match | Already similar | Some mapping | Full restructure |
| Dependencies | All compatible | Some replace | Many incompatible |
| Code complexity | Simple functions | Moderate classes | Complex system |
| Documentation | Good README | Partial docs | No docs |

## Output Report

```markdown
## Architecture Analysis: {repo-name}

### Repository Type
**Type**: Python CLI Tool
**Entry Point**: src/cli.py
**License**: MIT ✅

### Structure Mapping

| External | Exocortex | Action |
|----------|-----------|--------|
| README.md | SKILL.md | Condense |
| src/main.py | scripts/main.py | Copy + update imports |
| src/utils/ | scripts/utils/ | Copy |
| config.yaml | config/paths.py | Convert |
| tests/ | tests/ | Keep |
| docs/ | references/ | Move |
| .github/ | - | Remove |

### Dependencies

**Required** (keep):
- requests==2.28.0
- pyyaml==6.0

**Replaceable**:
- sqlite3 → YAML storage
- argparse → Remove (not CLI)

**Incompatible**:
- None

### Core Logic Location
- Main functionality: `src/main.py` (200 lines)
- Utilities: `src/utils/helpers.py` (100 lines)
- Total useful code: ~300 lines

### Effort Estimate
**Level**: Medium (2-3 hours)

**Breakdown**:
- Structure setup: 30 min
- Code migration: 1 hour
- Path updates: 30 min
- Documentation: 30 min
- Testing: 30 min

### Recommendation
✅ **Proceed with adaptation**

Code quality is good, structure maps well, minimal incompatibilities.
```
