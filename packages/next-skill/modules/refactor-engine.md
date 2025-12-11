# Refactor Engine Module

## Overview

Adapts external code repositories to Exocortex architecture while preserving useful functionality.

## Analysis Phase

### Structure Detection

Identify common patterns in source repo:

| Pattern | Indicators | Map To |
|---------|------------|--------|
| Flat structure | All files in root | Create proper hierarchy |
| src/ layout | `src/`, `lib/` folders | → `scripts/` |
| docs/ | `docs/`, `documentation/` | → `references/` |
| config | `.env`, `config.json` | → `config/paths.py` |
| tests | `tests/`, `__tests__/` | Keep, update imports |

### Dependency Analysis

```python
# Extract from requirements.txt, package.json, etc.
dependencies = {
    "required": [],      # Must have
    "optional": [],      # Nice to have
    "dev": [],          # Development only
    "incompatible": []  # Won't work in our env
}
```

### Feature Extraction

Parse README and code for capabilities:
- Main functionality
- Configuration options
- Input/output formats
- Integration points

## Refactoring Steps

### Step 1: Clone/Download Source

```bash
# Clone to temporary location
git clone {repo-url} /tmp/next-skill-adapt/{repo-name}
```

### Step 2: Create Target Structure

```bash
packages/{new-skill-name}/
├── SKILL.md              # New - condensed
├── references/
│   └── workflow.md       # New - from docs
├── modules/              # New - extracted features
├── _dev/
│   ├── design.md
│   └── research/
│       └── adapted-from.md
├── scripts/              # From src/
├── config/
│   └── paths.py          # New - from .env/config
├── version.yaml          # New
└── CHANGELOG.md          # New
```

### Step 3: Code Migration

#### Python Files

```python
# Update imports
OLD: from src.utils import helper
NEW: from scripts.utils import helper

# Update paths
OLD: CONFIG_FILE = "config.json"
NEW: from config.paths import CONFIG_FILE

# Update data locations
OLD: DATA_DIR = Path("./data")
NEW: from config.paths import DATA_DIR
```

#### Configuration

```python
# Original .env
API_KEY=xxx
DATA_PATH=/some/path

# New config/paths.py
from shared.config.paths import get_skill_data_path

SKILL_NAME = "{skill-name}"
DATA_DIR = get_skill_data_path(SKILL_NAME)

# API keys should be in environment or user config
```

### Step 4: Documentation Condensation

Original README (500 lines) → SKILL.md (<100 lines)

**Extract**:
- Core purpose (1-2 sentences)
- Main commands (table)
- Workflow overview (brief)
- Module references

**Move to references/**:
- Detailed explanations
- Examples
- Configuration guide
- Troubleshooting

### Step 5: Create Attribution

`_dev/research/adapted-from.md`:
```markdown
# Adaptation Source

**Original Repository**: {url}
**Original Author**: {author}
**Original License**: {license}
**Adaptation Date**: {date}

## Preserved Components
| Component | Original Location | New Location |
|-----------|------------------|--------------|
| Core logic | src/main.py | scripts/main.py |
| Utils | src/utils/ | scripts/utils/ |
| Tests | tests/ | tests/ |

## Modified Components
| Component | Changes Made |
|-----------|--------------|
| Config | Converted to paths.py |
| Docs | Condensed to SKILL.md |

## Added Components
| Component | Purpose |
|-----------|---------|
| _dev/ | Development metadata |
| references/ | Detailed documentation |

## Removed Components
| Component | Reason |
|-----------|--------|
| CI/CD | Use our workflows |
| Docker | Not needed |
```

## Validation

After refactoring, verify:

- [ ] All imports resolve
- [ ] Paths use config/paths.py
- [ ] SKILL.md < 100 lines
- [ ] Tests pass (if any)
- [ ] No hardcoded paths
- [ ] License compliance documented

## Output

```
Adaptation Complete: {skill-name}
==================================

Source: {original-repo}
Target: packages/{skill-name}/

Files Migrated:
  scripts/main.py ← src/main.py
  scripts/utils.py ← src/utils.py
  references/workflow.md ← docs/guide.md

Files Created:
  SKILL.md (87 lines)
  config/paths.py
  _dev/research/adapted-from.md
  version.yaml
  CHANGELOG.md

Preserved:
  tests/ (updated imports)

Removed:
  .github/workflows/
  Dockerfile
  .env.example

Next: Review SKILL.md and test functionality
```
