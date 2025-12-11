# Developer Guide

This guide covers how to create new skills, test them, and release them in the Exocortex monorepo.

## Table of Contents

- [Manual Installation](#manual-installation)
- [Repository Structure](#repository-structure)
- [Creating a New Skill](#creating-a-new-skill)
- [Skill Structure](#skill-structure)
- [Development Patterns](#development-patterns)
- [Testing](#testing)
- [Release Process](#release-process)
- [CI/CD](#cicd)
- [Best Practices](#best-practices)

---

## Manual Installation

If you prefer not to use the one-line installer, you can set up the environment manually.

### Prerequisites
- Python 3.11+
- Git
- `uv` (Python package manager, recommended) or `pip`

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/gsannikov/exocortex.git ~/Projects/exocortex
cd ~/Projects/exocortex

# 2. Run the interactive setup wizard
uv run packages/setup-manager/setup_manager/cli.py
```

### Setup Options

```bash
# Run interactive setup (default)
uv run packages/setup-manager/setup_manager/cli.py

# Check system status without making changes
uv run packages/setup-manager/setup_manager/cli.py --check

# Disable colored output (for logs/CI)
uv run packages/setup-manager/setup_manager/cli.py --no-color
```

---

## Repository Structure

```
exocortex/
├── packages/                      # All skills (9)
│   ├── job-analyzer/              # Job scoring & tracking
│   ├── interview-prep/            # STAR stories & negotiation
│   ├── reading-list/
│   ├── ideas-capture/
│   ├── voice-memos/
│   ├── local-rag/
│   ├── recipe-manager/
│   ├── social-media-post/
│   └── setup-manager/
├── shared/
│   ├── scripts/                   # Release, generator utilities
│   ├── config/                    # paths.py (single source of truth)
│   ├── templates/                 # Patterns, templates
│   └── workflows/                 # Troubleshooting guides
├── .github/workflows/             # CI/CD
├── CLAUDE.md                      # Global instructions
├── docs/project-status.md         # Architecture decisions
└── docs/developer-guide.md        # This file
```

---

## Creating a New Skill

### Option 1: Using the Skill Generator (Recommended)

```bash
cd ~/Projects/exocortex
python shared/scripts/skill_generator.py --name "expense-tracker" --patterns inbox,database
```

**Available Patterns:**
| Pattern | Description |
|---------|-------------|
| `inbox` | Apple Notes inbox integration |
| `database` | YAML database storage |
| `scoring` | Multi-dimensional scoring system |
| `scraping` | Web scraping capabilities |
| `output` | Report generation |

### Option 2: Manual Creation

1. Create the skill directory in `packages/`
2. Create required files: `SKILL.md`, `README.md`, `version.yaml`, `CHANGELOG.md`
3. Update `shared/scripts/release.py`

---

## Skill Structure

### Standard Structure (ADR-006)

All skills follow this structure with SKILL.md as orchestrator (<100 lines):

```
{skill}/
├── SKILL.md              # <100 lines, orchestrator
├── references/           # Detailed workflows
│   └── workflow.md
├── modules/              # Feature modules (loaded on-demand)
├── scripts/              # Python utilities
├── config/               # Configuration
├── README.md             # User guide
├── _dev/                 # Development metadata
│   ├── CHANGELOG.md      # Version history
│   └── version.yaml      # Version metadata
└── tests/                # Unit & integration tests
```

### SKILL.md Best Practices

- Keep under 100 lines
- Focus on commands and when to load modules
- Move detailed implementations to `references/`
- Use tables for command references
- No verbose explanations

### Shared Storage Pattern (ADR-007)

Skills can share storage for handoffs. Example: job-analyzer and interview-prep:

```
~/exocortex-data/career/           # Shared storage
├── analyses/                      # job-analyzer writes
├── contacts.yaml                  # job-analyzer writes, interview-prep reads
└── interview-prep/                # interview-prep writes
```

---

## Development Patterns

### Learned Patterns Reference

See `shared/templates/learned-patterns.yaml` for best practices.

### Key Patterns

| Pattern | Description |
|---------|-------------|
| **Inbox** | Apple Notes with "ADD BELOW" / "PROCESSED" sections |
| **Database** | YAML with id, title, added_at, status |
| **Scoring** | 6 dimensions (feasibility, impact, effort, uniqueness, timing, fit) |
| **Naming** | Skills: kebab-case, Functions: snake_case |

### Shared Utilities

Located in `shared/scripts/`:
- `dependency_tracker.py` - File dependency management
- `yaml_utils.py` - YAML/frontmatter utilities
- `slug_utils.py` - URL-safe slug generation
- `token_estimator.py` - Token budget management

---

## Testing

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests
└── integration/          # Integration tests
```

### Running Tests

We recommend using `uv` to ensure you run tests in the correct environment with all dependencies.

```bash
# Run all tests for the entire monorepo (Recommended)
uv run pytest

# Run all tests for a specific skill
uv run pytest packages/job-analyzer/tests/

# Run with verbose output
uv run pytest -v packages/job-analyzer/tests/

# Run with coverage
uv run pytest --cov=packages/job-analyzer packages/job-analyzer/tests/
```

---

## Release Process

### Option 1: Using Claude Command (Recommended)

```bash
/release                    # Interactive prompts
/release job-analyzer patch # Release specific skill
```

### Option 2: Using the Release Script

```bash
# Release single skill
python shared/scripts/release.py job-analyzer --patch

# Release all skills
python shared/scripts/release.py all --patch

# Dry run
python shared/scripts/release.py job-analyzer --patch --dry-run
```

### Available Skills (9)

| Skill | Description |
|-------|-------------|
| `job-analyzer` | Job scoring, tracking, contacts |
| `interview-prep` | STAR stories, negotiation |
| `reading-list` | Article capture & summaries |
| `ideas-capture` | Idea expansion & scoring |
| `voice-memos` | Transcription & analysis |
| `local-rag` | Semantic document search |
| `social-media-post` | Platform-optimized posts |
| `recipe-manager` | Recipe extraction |
| `setup-manager` | Environment setup |

---

## CI/CD

### Validation Workflow

Runs on every push and PR:
- Validates skill structure
- Validates YAML syntax
- Checks Python syntax
- Runs on matrix of all skills

### Release Workflow

Manual trigger with inputs:
- `skill`: Select skill or "all"
- `bump`: patch/minor/major
- `dry_run`: Preview mode

---

## Dependency Management

### Commands

```bash
# Check status
python shared/scripts/dependency_tracker.py status

# See dependency tree
python shared/scripts/dependency_tracker.py graph

# What depends on a file?
python shared/scripts/dependency_tracker.py affected packages/job-analyzer/SKILL.md
```

### Claude Code Commands

| Command | Purpose |
|---------|---------|
| `/deps` | Quick dependency status check |
| `/refactor` | Full dependency-aware update |
| `/release` | Trigger Cloud Release Workflow |

---

## Best Practices

### Do's

- **Keep SKILL.md under 100 lines** - Use references/ for details
- **Separate user data from code** - Data in `~/exocortex-data/`
- **Use centralized path config** - `shared/config/paths.py`
- **Use YAML for structured data** - Human-readable, git-friendly
- **Load modules on-demand** - Optimize token usage
- **Use slugs as IDs** - URL-safe, unique identifiers

### Don'ts

- **Don't store large content in Apple Notes** - Causes timeout
- **Don't hardcode paths** - Use configuration
- **Don't commit user data** - It's in a separate gitignored folder
- **Don't make SKILL.md verbose** - Keep it concise

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
| `SKILL.md` | Main skill documentation (<100 lines) |
| `references/workflow.md` | Detailed workflows |
| `version.yaml` | Version metadata |
| `shared/config/paths.py` | User data path configuration |

---

**Version**: 1.2.0
**Last Updated**: 2025-12-11
