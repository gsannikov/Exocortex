# Developer Guide

This guide covers how to create new skills, test them, and release them in the Claude Skills monorepo.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Creating a New Skill](#creating-a-new-skill)
- [Skill Structure](#skill-structure)
- [Development Patterns](#development-patterns)
- [Testing](#testing)
- [Release Process](#release-process)
- [CI/CD](#cicd)
- [Best Practices](#best-practices)

---

## Repository Structure

```
claude-skills/
├── packages/                      # All skills
│   ├── career-consultant/
│   ├── reading-list/
│   ├── ideas-capture/
│   ├── voice-memos/
│   └── local-rag/
├── shared/
│   ├── scripts/                   # Release, generator utilities
│   │   ├── release.py
│   │   ├── skill_generator.py
│   │   ├── dependency_tracker.py
│   │   ├── yaml_utils.py
│   │   ├── slug_utils.py
│   │   └── token_estimator.py
│   ├── templates/                 # Patterns, templates
│   │   └── learned-patterns.yaml
│   ├── marketing/                 # Blog posts, images
│   └── workflows/                 # Troubleshooting guides
├── .github/workflows/             # CI/CD
│   ├── validate.yml
│   └── release.yml
├── CLAUDE.md                      # Global instructions
├── PROJECT.md                     # Architecture decisions
└── DEVELOPER_GUIDE.md             # This file
```

---

## Creating a New Skill

### Option 1: Using the Skill Generator (Recommended)

```bash
cd ~/MyDrive/claude-skills
python shared/scripts/skill_generator.py --name "expense-tracker" --patterns inbox,database
```

**Parameters:**
- `--name`: Skill name in kebab-case (required)
- `--patterns`: Comma-separated patterns to include (default: `inbox,database`)
- `--description`: Skill description (optional)

**Available Patterns:**
| Pattern | Description |
|---------|-------------|
| `inbox` | Apple Notes inbox integration |
| `database` | YAML database storage |
| `scoring` | Multi-dimensional scoring system |
| `scraping` | Web scraping capabilities |
| `output` | Report generation |

**What Gets Created:**
```
packages/{skill-name}/
├── skill-package/
│   ├── SKILL.md              # Main skill documentation
│   ├── version.yaml          # Version metadata
│   └── modules/              # Module directory
├── README.md                 # User-facing overview
└── CHANGELOG.md              # Version history
```

The generator also creates the user data directory:
```
~/MyDrive/claude-skills-data/{skill-name}/
```

### Option 2: Manual Creation

1. Create the skill directory:
   ```bash
   mkdir -p packages/{skill-name}
   ```

2. Create required files:
   - `SKILL.md` - Main skill documentation
   - `README.md` - User overview
   - `version.yaml` - Version info
   - `CHANGELOG.md` - Version history

3. Update `shared/scripts/release.py` to add the skill configuration.

---

## Skill Structure

### Minimal Skill (e.g., ideas-capture)

```
{skill}/
├── SKILL.md              # Complete workflow documentation
├── README.md             # Quick start guide
├── AI_GUIDE.md           # AI-specific instructions
├── CHANGELOG.md          # Version history
└── version.yaml          # Version metadata
```

### Complex Skill (e.g., career-consultant)

```
{skill}/
├── SKILL.md              # Orchestrator with workflow
├── README.md             # User guide
├── AI_GUIDE.md           # AI instructions
├── CHANGELOG.md          # Version history
├── version.yaml          # Version metadata
├── config/               # Configuration files
│   ├── paths.py
│   └── settings.json
├── modules/              # On-demand loaded modules
│   ├── company-research.md
│   ├── scoring-formulas.md
│   └── database-operations.md
├── scripts/              # Python utilities
│   ├── storage_utils.py
│   └── config_loader.py
├── templates/            # User templates
│   └── user-config-template.yaml
└── tests/                # Test suite
    ├── conftest.py
    └── unit/
```

### Required Files

#### version.yaml
```yaml
version: 1.0.0
updated: 2025-11-25
skill: skill-name
codename: "Initial Release"
status: stable
```

#### SKILL.md Structure
```markdown
---
name: skill-name
description: One-line description of the skill
---

# {Emoji} {Display Name}

Brief description of what the skill does.

## Key Capabilities
1. **Feature 1**: Description
2. **Feature 2**: Description

## Storage Configuration

**User Data Location**: `~/MyDrive/claude-skills-data/{skill}/`

## Commands

| Command | Action |
|---------|--------|
| `command` | Description |

## Workflow: [Name]

### Step 1: ...
### Step 2: ...

---

**Version**: X.Y.Z
**Patterns**: inbox, database
```

---

## Development Patterns

### Learned Patterns Reference

See `shared/templates/learned-patterns.yaml` for best practices:

#### Inbox Pattern
- Apple Note format: `{emoji} {Name} Inbox`
- Sections: "ADD BELOW", separator, "PROCESSED"
- Keep processed section minimal (stats only)

#### Database Pattern
- Format: YAML
- Required fields: `id`, `title`, `added_at`, `status`
- Use slugs as unique identifiers

#### Scoring Pattern (6 dimensions)
```yaml
dimensions:
  - feasibility
  - impact
  - effort
  - uniqueness
  - timing
  - personal_fit
tiers:
  hot: 7+
  warm: 5-6
  cold: 0-4
```

#### Naming Conventions
- Skills: `kebab-case`
- Files: `kebab-case.{yaml,md}`
- Functions: `snake_case`
- Constants: `UPPER_CASE`

### Shared Utilities

Located in `shared/scripts/`:

**dependency_tracker.py**
```python
# CLI tool for managing file dependencies
python shared/scripts/dependency_tracker.py status        # Show all file statuses
python shared/scripts/dependency_tracker.py graph         # Display dependency tree
python shared/scripts/dependency_tracker.py rebuild-order # Get rebuild order
python shared/scripts/dependency_tracker.py affected FILE # Show dependents of a file
```

**yaml_utils.py**
```python
from yaml_utils import (
    create_yaml_document,      # Create markdown with YAML frontmatter
    parse_yaml_frontmatter,    # Extract YAML + content from markdown
    validate_yaml_frontmatter  # Validate required fields
)
```

**slug_utils.py**
```python
from slug_utils import (
    normalize_slug,           # Create URL-safe slugs
    create_role_id,           # Composite IDs
    extract_company_from_url, # Parse URLs
    sanitize_filename         # Filesystem-safe names
)
```

**token_estimator.py**
```python
from token_estimator import (
    estimate_tokens,          # ~4 chars per token
    check_token_budget,       # Budget status
    can_fit_in_budget         # Check if operation fits
)
```

---

## Testing

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests
│   ├── test_storage.py
│   └── test_utils.py
└── integration/          # Integration tests
```

### Writing Tests

1. **Create conftest.py with fixtures:**
```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_user_data_dir(tmp_path):
    """Create temporary user data structure."""
    dirs = ['companies', 'jobs', 'profile']
    for d in dirs:
        (tmp_path / d).mkdir()
    return tmp_path

@pytest.fixture
def sample_config():
    """Sample user configuration."""
    return {
        'cv_variants': {'variants': []},
        'scoring': {'weights': {'match': 35, 'income': 25}},
        'preferences': {'min_salary': 450000}
    }
```

2. **Write unit tests:**
```python
# tests/unit/test_utils.py
import pytest
from scripts.slug_utils import normalize_slug

def test_normalize_slug():
    assert normalize_slug("Hello World") == "hello-world"
    assert normalize_slug("Test@#$String") == "test-string"
    assert normalize_slug("Multiple   Spaces") == "multiple-spaces"

def test_normalize_slug_max_length():
    long_text = "a" * 100
    result = normalize_slug(long_text, max_length=50)
    assert len(result) == 50
```

### Running Tests

```bash
# Run all tests for a skill
pytest packages/career-consultant/tests/

# Run specific test file
pytest packages/career-consultant/tests/unit/test_storage.py

# Run with verbose output
pytest -v packages/career-consultant/tests/

# Run with coverage
pytest --cov=packages/career-consultant packages/career-consultant/tests/
```

### Test Requirements

Create `requirements-test.txt` in skills with tests:
```
pytest>=7.0.0
pytest-cov>=4.0.0
```

---

## Release Process

### Using the Release Script

```bash
cd ~/MyDrive/claude-skills

# Release a single skill with patch bump (1.0.0 → 1.0.1)
python shared/scripts/release.py career-consultant --patch

# Release with minor bump (1.0.0 → 1.1.0)
python shared/scripts/release.py reading-list --minor

# Release with major bump (1.0.0 → 2.0.0)
python shared/scripts/release.py local-rag --major

# Release all skills
python shared/scripts/release.py all --patch

# Dry run (preview without making changes)
python shared/scripts/release.py career-consultant --patch --dry-run
```

### What the Release Script Does

1. **Gets current version** from `version.yaml`
2. **Bumps version** according to semver (major/minor/patch)
3. **Runs tests** if configured for the skill
4. **Updates version.yaml** with new version and date
5. **Updates CHANGELOG.md** with new version entry
6. **Creates git tag** `{skill}-v{version}`
7. **Commits changes** with message "Release {skill} v{version}"

### Manual Steps After Release

```bash
# Push changes and tags to remote
git push origin main --tags
```

### Adding a New Skill to Release Script

Edit `shared/scripts/release.py`:

```python
SKILL_CONFIG = {
    # ... existing skills ...
    'new-skill': {
        'has_host_scripts': False,  # True if skill has Python scripts to test
        'has_tests': False,          # True if skill has pytest tests
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
}
```

---

## CI/CD

### Validation Workflow (.github/workflows/validate.yml)

Runs on every push and PR:
- Validates skill structure (SKILL.md, README.md required)
- Validates YAML syntax
- Validates version.yaml exists
- Checks Python syntax for scripts
- Runs on matrix of all skills

### Release Workflow (.github/workflows/release.yml)

Manual trigger (workflow_dispatch):

**Inputs:**
- `skill`: Select skill or "all"
- `bump`: patch/minor/major
- `dry_run`: Preview mode

**Process:**
1. Checkout with full history
2. Set up Python
3. Run release script
4. Push changes and tags (unless dry-run)
5. Create GitHub Release

### Running CI Locally

```bash
# Validate YAML files
python -c "import yaml; yaml.safe_load(open('packages/skill/version.yaml'))"

# Check Python syntax
python -m py_compile packages/skill/scripts/*.py

# Run tests
pytest packages/skill/tests/
```

---

## Dependency Management

The repo uses a dependency tracking system to ensure documentation stays in sync with code.

### Dependency Workflow

| Stage | What Happens | Blocks? |
|-------|--------------|---------|
| **During Development** | Modify source files freely | No |
| **PR Created** | CI checks dependencies, comments if out of sync | ⚠️ Warning |
| **Pre-Merge** | Run `/refactor` if CI flagged issues | Manual |
| **Release** | CI verifies all docs in sync | ❌ Blocks |

### Commands

```bash
# Check status
python shared/scripts/dependency_tracker.py status

# See dependency tree
python shared/scripts/dependency_tracker.py graph

# Get rebuild order
python shared/scripts/dependency_tracker.py rebuild-order

# What depends on a file?
python shared/scripts/dependency_tracker.py affected packages/voice-memos/SKILL.md
```

### Claude Code Commands

| Command | Purpose |
|---------|---------|
| `/deps` | Quick dependency status check |
| `/refactor` | Full dependency-aware update workflow |

### Adding New Dependencies

Edit `dependencies.yaml` to add new files:

```yaml
nodes:
  - path: packages/new-skill/README.md
    type: derived
    description: User documentation
    depends_on:
      - packages/new-skill/SKILL.md
    rebuild_instructions: |
      Sync commands and features from SKILL.md
```

### File Types

| Type | Updates Triggered By | Example |
|------|---------------------|---------|
| `source` | Manual changes | `SKILL.md`, `PROJECT.md` |
| `derived` | Source changes | Skill READMEs |
| `documentation` | Multiple sources | `USER_GUIDE.md` |
| `marketing` | Documentation changes | Blog articles |

---

## Best Practices

### Do's

- **Separate user data from code**: User data in `~/MyDrive/claude-skills-data/`
- **Use YAML for structured data**: Human-readable, git-friendly
- **Deduplicate before adding**: Always check for existing items
- **Track stats**: Update statistics after operations
- **Use slugs as IDs**: URL-safe, unique identifiers
- **Load modules on-demand**: Optimize token usage
- **Write comprehensive SKILL.md**: Include full workflow documentation

### Don'ts

- **Don't store large content in Apple Notes**: Causes timeout
- **Don't duplicate data**: Between skill-package and user-data
- **Don't hardcode paths**: Use configuration
- **Don't skip deduplication**: Prevents duplicates
- **Don't ignore URL normalization**: Strip trailing slashes
- **Don't commit user data**: It's in a separate gitignored folder

### Anti-patterns to Avoid

```yaml
# BAD: Storing full content in database
items:
  - id: article-1
    full_content: "10000 words of content..."  # DON'T

# GOOD: Store reference only
items:
  - id: article-1
    content_path: "summaries/article-1.md"     # DO
```

---

## Quick Reference

### Create New Skill
```bash
python shared/scripts/skill_generator.py --name "my-skill" --patterns inbox,database
```

### Run Tests
```bash
pytest packages/{skill}/tests/
```

### Release Skill
```bash
python shared/scripts/release.py {skill} --patch
git push origin main --tags
```

### Key Files
| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill documentation |
| `version.yaml` | Version metadata |
| `CHANGELOG.md` | Version history |
| `conftest.py` | Test fixtures |
| `release.py` | Release automation |
| `skill_generator.py` | Skill scaffolding |
| `dependency_tracker.py` | File dependency management |
| `dependencies.yaml` | Dependency graph definition |

---

**Version**: 1.0.0
**Last Updated**: 2025-11-25
