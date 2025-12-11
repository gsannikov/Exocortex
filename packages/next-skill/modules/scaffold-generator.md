# Scaffold Generator Module

## Overview

Generates new skill structure from templates based on selected patterns.

## Pattern Selection

### Available Patterns

| Pattern | Files Generated | Use Case |
|---------|----------------|----------|
| `inbox` | inbox-pattern module | Apple Notes integration |
| `database` | database module, index.yaml | YAML data storage |
| `scoring` | scoring module | Multi-dimensional evaluation |
| `scraping` | scraping module | Web content fetching |
| `output` | output module | Report/file generation |

### Pattern Combinations

| Skill Type | Recommended Patterns |
|------------|---------------------|
| Tracker | inbox, database |
| Analyzer | database, scoring |
| Collector | inbox, database, scraping |
| Reporter | database, output |
| Full workflow | inbox, database, scoring, output |

## Generation Process

### Step 1: Create Directory Structure

```bash
packages/{skill-name}/
├── SKILL.md
├── references/
│   └── workflow.md
├── modules/
├── _dev/
│   ├── design.md
│   └── todos.md
├── scripts/
├── config/
│   └── paths.py
├── version.yaml
└── CHANGELOG.md
```

### Step 2: Generate version.yaml

```yaml
version: 0.1.0
updated: {today}
skill: {skill-name}
codename: "Initial Release"
status: development
```

### Step 3: Generate SKILL.md

Template variables:
- `{name}` - Skill name (kebab-case)
- `{display_name}` - Display name (Title Case)
- `{emoji}` - Selected emoji
- `{description}` - One-line description
- `{patterns}` - Selected patterns list

Line budget:
- Header: 5 lines
- Commands table: 10-15 lines
- Workflow: 30-40 lines
- Module loading: 10-15 lines
- Storage: 5 lines
- Footer: 5 lines
- **Total: <100 lines**

### Step 4: Generate Pattern Modules

For each selected pattern, copy from `templates/patterns/`:

**inbox-pattern.md** → `modules/inbox.md`
**database-pattern.md** → `modules/database.md`
**scoring-pattern.md** → `modules/scoring.md`
**scraping-pattern.md** → `modules/scraping.md`
**output-pattern.md** → `modules/output.md`

### Step 5: Generate _dev Files

**design.md**:
```markdown
# {Display Name} Design

## Purpose
{description}

## Patterns Used
{patterns list}

## Key Decisions
- Decision 1: {rationale}

## Created
- Date: {today}
- Method: next-skill scaffold
```

**todos.md**:
```markdown
# {Display Name} TODOs

## Phase 1: Core
- [ ] Implement main workflow
- [ ] Test with sample data
- [ ] Write user documentation

## Phase 2: Polish
- [ ] Add error handling
- [ ] Optimize performance
- [ ] Add advanced features

## Phase 3: Release
- [ ] Full testing
- [ ] Update collaterals
- [ ] Release v1.0.0
```

### Step 6: Generate config/paths.py

```python
"""
Path configuration for {skill-name}.
Integrates with shared/config/paths.py
"""
import sys
from pathlib import Path

# Add shared config to path
REPO_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "shared" / "config"))

from paths import get_skill_data_path

SKILL_NAME = "{skill-name}"
DATA_DIR = get_skill_data_path(SKILL_NAME)

# Skill-specific paths
INDEX_FILE = DATA_DIR / "index.yaml"
```

### Step 7: Create Data Directory

```bash
mkdir -p ~/exocortex-data/{skill-name}
```

## Output Summary

```
Created: packages/{skill-name}/

Files:
  ✅ SKILL.md (92 lines)
  ✅ references/workflow.md
  ✅ modules/inbox.md
  ✅ modules/database.md
  ✅ _dev/design.md
  ✅ _dev/todos.md
  ✅ config/paths.py
  ✅ version.yaml
  ✅ CHANGELOG.md

Data Directory:
  ✅ ~/exocortex-data/{skill-name}/

Next Steps:
  1. Review and customize SKILL.md
  2. Implement workflow in modules
  3. Test with sample data
  4. Register in release.py
```
