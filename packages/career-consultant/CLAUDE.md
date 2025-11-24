# CLAUDE.md - AI Assistant Guide

**Last Updated**: 2025-11-18
**Version**: 1.1.0
**Status**: Stable

This document provides comprehensive guidance for AI assistants (like Claude) working with this codebase. It explains the structure, conventions, workflows, and critical patterns to follow when making changes or analyzing this project.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Codebase Architecture](#codebase-architecture)
3. [Critical Rules & Conventions](#critical-rules--conventions)
4. [Directory Structure](#directory-structure)
5. [Module System](#module-system)
6. [Storage & Data Model](#storage--data-model)
7. [Development Workflows](#development-workflows)
8. [Version Management](#version-management)
9. [Testing & Validation](#testing--validation)
10. [Common Tasks](#common-tasks)
11. [Troubleshooting Guide](#troubleshooting-guide)

---

## Project Overview

### What This Project Is

**Israeli Tech Career Consultant** is an AI-powered job analysis system designed for the Israeli tech market. It helps senior tech professionals make data-driven career decisions through:

- **6-component scoring system**: Match, Income, Growth, LowPrep, Stress, Location (0-100 points)
- **Smart company caching**: Research once, reuse forever (15-20K tokens saved per reuse)
- **Multi-CV matching**: Support for multiple CV variants with weighted relevance
- **Dual workflow modes**: Quick capture (~5K tokens) or full analysis (25-35K tokens)
- **Excel tracking**: Automated generation from YAML database

### Target Users

Senior tech professionals (EM, TPM, AI roles) in Israel targeting ₪450K+ compensation.

### Technology Stack

- **Primary Language**: Python 3.8+
- **Data Formats**: YAML (metadata), Markdown (content), Excel (reporting)
- **AI Platform**: Claude.ai with MCP (Model Context Protocol)
- **Dependencies**: pyyaml, pandas, openpyxl
- **Storage**: Local filesystem only (no cloud/Notion/Google Drive)

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Files | ~280+ |
| Python Scripts | 31 |
| Markdown Docs | 95+ |
| Core Modules | 7 |
| Template Files | 15+ |
| Feature Specs | 13 |

---

## Codebase Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Claude.ai Platform                    │
│              (Uploads skill-package/)                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  SKILL.md (Orchestrator)                │
│         - Loads modules on demand                       │
│         - Manages token budgets                         │
│         - Coordinates workflow phases                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌──────────────┬──────────────┬──────────────┬────────────┐
│   Company    │   Skills     │   Scoring    │  Database  │
│   Research   │   Matching   │   Formulas   │  Operations│
│   (857 L)    │   (880 L)    │   (903 L)    │  (1,117 L) │
└──────────────┴──────────────┴──────────────┴────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              MCP Filesystem Server                      │
│         (@modelcontextprotocol/server-filesystem)       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              User Data (Local Filesystem)               │
│   config/   db/companies/   db/roles/   db.xlsx        │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Request** → Claude.ai with skill uploaded
2. **SKILL.md** → Loads required modules progressively
3. **Modules** → Process request using helper scripts
4. **MCP Filesystem** → Read/write user data (config, CVs, database)
5. **Python Scripts** → Generate Excel, process YAML, create reports
6. **Output** → Markdown analysis + YAML storage + Excel tracking

---

## Critical Rules & Conventions

### 🚨 ABSOLUTE RULES (Never Break These)

#### 1. Storage & File Access

**DO:**
- ✅ Use `filesystem:read_text_file` for ALL user data (CVs, config, companies, roles)
- ✅ Use `file_read()` for skill modules (company-research.md, skills-matching.md, etc.)
- ✅ Use paths from `skill-package/config/paths.py`
- ✅ Store all data locally in `user-data/` directory

**DO NOT:**
- ❌ NEVER use Notion API tools
- ❌ NEVER use Google Drive MCP
- ❌ NEVER use `file_read()` for user data
- ❌ NEVER use `filesystem:read_text_file` for skill modules
- ❌ NEVER search entire filesystem for skill files
- ❌ NEVER create session state files in root (use `user-data/`)

#### 2. Token Budget Protection

**DO:**
- ✅ Track token usage after each major operation
- ✅ Use progressive module loading (load only what's needed)
- ✅ Stop after company research for validation, then restart
- ✅ Start fresh conversations for each job analysis

**DO NOT:**
- ❌ NEVER use `directory_tree` on large directories (>100 files)
- ❌ NEVER perform recursive operations on root directories
- ❌ NEVER load all modules at once

**Typical Token Budgets:**
- Research new company: 15-20K tokens → **STOP**, validate, restart
- Analyze with cached company: 25-35K tokens → Complete in one session
- Quick backlog capture: ~5K tokens per job

#### 3. Version Management

**DO:**
- ✅ `version.yaml` is the **single source of truth**
- ✅ Update version.yaml FIRST, then run `python -m host_scripts update-version`
- ✅ Follow semantic versioning: MAJOR.MINOR.PATCH
- ✅ Update CHANGELOG.md for each release

**DO NOT:**
- ❌ NEVER manually update version numbers in README.md or SKILL.md
- ❌ NEVER create releases without updating version.yaml
- ❌ NEVER skip the version sync script

#### 4. Data Model & File Formats

**DO:**
- ✅ Use YAML frontmatter for structured metadata
- ✅ Use Markdown for human-readable content
- ✅ Use hybrid format: `---\nYAML\n---\n# Markdown`
- ✅ Generate Excel dynamically from YAML
- ✅ Use kebab-case for file names (e.g., `company-research.md`)

**DO NOT:**
- ❌ NEVER store data in formats other than YAML+Markdown
- ❌ NEVER commit binary files except images for docs
- ❌ NEVER commit user-data/ directory (it's .gitignored)

#### 5. Module Development

**DO:**
- ✅ Keep modules self-contained (~900-1,300 lines)
- ✅ Include YAML frontmatter with metadata
- ✅ Document token costs explicitly
- ✅ Provide "When to Load This Module" section
- ✅ Include step-by-step workflow definitions

**DO NOT:**
- ❌ NEVER create circular dependencies between modules
- ❌ NEVER exceed 2,000 lines per module
- ❌ NEVER forget to update SKILL.md when adding modules

---

## Directory Structure

### Root Level Structure

```
israeli-tech-career-consultant/
├── .github/                    # GitHub Actions workflows
│   ├── workflows/
│   │   ├── release.yml         # Automated releases
│   │   ├── validate-skill.yml  # Structure validation
│   │   └── version-check.yml   # Version consistency
│   └── ISSUE_TEMPLATE/
│
├── skill-package/              # CORE - Upload to Claude
│   ├── SKILL.md                # Main orchestrator (27K lines)
│   ├── modules/                # 7 analysis modules (6.8K lines total)
│   ├── scripts/                # 8 Python utilities (3.2K lines)
│   ├── config/                 # Path & scoring config
│   ├── references/             # Reference documentation
│   └── templates/              # User templates (15 files)
│
├── host_scripts/               # Host automation (Python CLI)
│   ├── __main__.py             # CLI entry point
│   ├── commands/               # Command implementations
│   └── domain/                 # Domain models
│
├── docs/                       # Comprehensive documentation
│   ├── guides/
│   │   ├── user-guide/         # End-user docs
│   │   └── developers-guide/   # Developer docs
│   ├── project/                # Project management
│   │   ├── features/           # 13 feature specs
│   │   ├── bugs/               # Issue tracking
│   │   ├── planning/           # Planning docs
│   │   └── roadmap/            # Product roadmap
│   ├── logs/                   # Session logs
│   ├── strategy/               # Strategic docs
│   └── marketing/              # Marketing materials
│
├── project/roadmap/            # Feature roadmap
├── releases/                   # Release artifacts
│
├── version.yaml                # VERSION SINGLE SOURCE OF TRUTH
├── README.md                   # Main project README
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── CLAUDE.md                   # THIS FILE - AI assistant guide
└── .gitignore                  # Git ignore rules
```

### User Data Structure (Not in Repo)

```
user-data/                      # User's local data (gitignored)
├── config/
│   ├── user-config.yaml        # Main configuration
│   ├── candidate-profile.md    # Professional profile
│   ├── salary-data.md          # Salary expectations
│   └── cv-variants/            # Multiple CV files
│       ├── cv-em.md
│       ├── cv-tpm.md
│       └── cv-ai.md
├── db/
│   ├── companies/              # Company research (YAML+MD)
│   │   ├── google-israel.yaml
│   │   └── google-israel.md
│   ├── roles/                  # Job analyses (YAML+MD)
│   │   ├── google-senior-engineer-2025.yaml
│   │   └── google-senior-engineer-2025.md
│   ├── job-backlog/            # Pending jobs
│   │   ├── pending/
│   │   └── archived/
│   └── db.xlsx                 # Excel database (auto-generated)
└── scripts/
    └── dynamic_excel_generator.py
```

### Critical File Locations

| File | Location | Purpose |
|------|----------|---------|
| `version.yaml` | Root | Single source of truth for version |
| `SKILL.md` | skill-package/ | Main orchestrator for AI |
| `paths.py` | skill-package/config/ | Path configuration |
| `user-config.yaml` | user-data/config/ | User settings |
| `db.xlsx` | user-data/db/ | Excel tracking database |

---

## Module System

### Core Modules (skill-package/modules/)

1. **company-research.md** (857 lines)
   - Multi-source company intelligence
   - Smart caching system
   - Research validation workflow
   - Token cost: 15-20K first time, 0K reuse

2. **skills-matching.md** (880 lines)
   - CV-to-job proficiency matching
   - Support for 1-N CV variants
   - Weighted relevance scoring
   - Token cost: 4-6K per analysis

3. **scoring-formulas.md** (903 lines)
   - 6-component scoring algorithm
   - Match (35), Income (25), Growth (20), LowPrep (15), Stress (10), Location (5)
   - Priority tier classification
   - Token cost: 2-3K per calculation

4. **job-backlog-manager.md** (746 lines)
   - Quick job capture workflow
   - Batch processing support
   - Lightweight alternative to full analysis
   - Token cost: ~5K per job

5. **database-operations-hybrid.md** (1,117 lines)
   - YAML + Markdown storage
   - Company profiles management
   - Job role tracking
   - Excel generation coordination

6. **output-yaml-templates.md** (882 lines)
   - Markdown report generation
   - YAML frontmatter standardization
   - Multi-format output support

7. **star-framework.md** (1,330 lines)
   - Behavioral interview story builder
   - 100-point quality scoring
   - 7 competency categories
   - Story library management

8. **debug-mode.md** (Developer Console)
   - Introspection tools (Prompt Inspector, State Viewer)
   - MCP Tool Tester
   - Verbose logging control
   - Token cost: ~1.5K (loaded only on demand)

### Module Loading Pattern

```python
# CORRECT: Progressive loading
if task_requires_company_research:
    module = file_read("modules/company-research.md")
    # Process module...

if task_requires_scoring:
    module = file_read("modules/scoring-formulas.md")
    # Process module...
```

**Never load all modules at once** - this wastes tokens.

### Helper Scripts (skill-package/scripts/)

| Script | Purpose | Lines |
|--------|---------|-------|
| `paths.py` | Path configuration | 122 |
| `yaml_utils.py` | YAML frontmatter helpers | 222 |
| `config_loader.py` | Config parsing | 198 |
| `cv_matcher.py` | CV matching logic | 238 |
| `slug_utils.py` | URL/filename slugification | 279 |
| `token_estimator.py` | Token cost calculation | 262 |
| `html_generator.py` | HTML report generation | 653 |
| `storage_utils.py` | File operations | 380 |

---

## Storage & Data Model

### Storage Philosophy

1. **Local Filesystem Only** - No cloud services
2. **YAML for Structure** - Metadata, scores, configuration
3. **Markdown for Content** - Human-readable narrative
4. **Excel for Reporting** - Auto-generated from YAML

### YAML Frontmatter Pattern

All data files use this pattern:

```markdown
---
# Structured YAML metadata
company_id: google-israel
company_name: Google Israel
tier: 1
tier_score: 25
updated: true
---

# Markdown Content

Human-readable content goes here...
```

### Company Data Model

**File**: `user-data/db/companies/{company-slug}.yaml`

```yaml
---
company_id: google-israel
company_name: Google Israel
tier: 1                    # 1=Top Tier, 2=Mid Tier, 3=Other
tier_score: 25             # 25, 15, or 5 based on tier
employees_global: 150000
employees_israel: 2000
glassdoor_rating: 4.5
revenue_usd: "280B"
funding_stage: "Public"
key_products: ["Search", "Cloud", "Android"]
updated: true
---

# Company Research

## Overview
[Content...]

## Products & Technology
[Content...]
```

### Role Data Model

**File**: `user-data/db/roles/{role-slug}.yaml`

```yaml
---
role_id: google-israel-senior-engineer-20250128
company_id: google-israel
role_title: Senior Software Engineer
application_date: "2025-01-28"

# Scoring
score_total: 78
score_match: 32
score_income: 23
score_growth: 18
score_lowprep: 12
score_stress: 8
score_location: 5

priority: First           # First (≥70), Second (50-69), Third (<50)
best_cv: Backend
cv_scores:
  Backend: 32
  General: 28

# Classification
status: Applied          # Backlog, Applied, Interview, Rejected, Accepted
notes: "Strong team, interesting project"
---

# Job Analysis

[Markdown content...]
```

### Configuration Model

**File**: `user-data/config/user-config.yaml`

```yaml
# Storage Configuration
storage:
  type: local_filesystem
  base_path: /Users/username/career-consultant/user-data
  auto_create_dirs: true

# CV Variants
cv_variants:
  count: 3
  variants:
    - id: "EM"
      filename: "cv-em.md"
      focus: "Engineering Management"
      weight: 1.0
    - id: "TPM"
      filename: "cv-tpm.md"
      focus: "Technical Program Management"
      weight: 0.9
    - id: "AI"
      filename: "cv-ai.md"
      focus: "AI/ML Engineering"
      weight: 0.85

# Scoring Configuration
scoring:
  weights:
    match: 35
    income: 25
    growth: 20
    lowprep: 15
    stress: 10
    location: 5

  thresholds:
    first_priority: 70
    second_priority: 50

  bonuses:
    tech_giant_experience: 5
    startup_experience: 3
    relevant_domain: 2

# Preferences
preferences:
  min_salary_annual_ils: 450000
  preferred_locations:
    - "Tel Aviv"
    - "Remote"
    - "Herzliya"

  avoid_keywords:
    - "relocation required"
    - "on-call 24/7"
```

---

## Development Workflows

### Workflow 1: Creating a New Release

**Location**: Host machine (not Claude)

```bash
# 1. Update version
vim version.yaml  # Update version, date, codename

# 2. Sync all files
python -m host_scripts update-version

# 3. Update changelog
vim CHANGELOG.md  # Add release notes

# 4. Commit and tag
git add .
git commit -m "Release v9.7.0: New Feature Name"
git tag v9.7.0
git push origin main --tags

# 5. GitHub Actions automatically:
#    - Validates version consistency
#    - Creates GitHub release
#    - Packages skill files (.skill)
#    - Uploads artifacts
```

### Workflow 2: Adding a New Module

**Steps:**

1. **Create module file**: `skill-package/modules/new-module.md`
2. **Follow module template**:
   ```markdown
   ---
   module_name: new-module
   version: 1.0.0
   token_cost: ~XK
   ---

   # Module Name

   ## When to Load This Module

   Load when...

   ## Token Budget

   Approximately XK tokens

   ## Workflow Steps

   1. Step one...
   2. Step two...
   ```

3. **Update SKILL.md**: Add module loading logic
4. **Test thoroughly**: Verify token usage and functionality
5. **Document**: Update docs/project/features/ if needed
6. **Commit**: Follow git conventions

### Workflow 3: User Job Analysis

**Location**: Claude.ai with skill uploaded

**Phase 1: Research Company (if new)**
```
User: "Analyze this job: https://linkedin.com/jobs/view/12345"

Claude:
1. Load SKILL.md
2. Extract company name from URL
3. Check if company cached
4. If not cached:
   a. Load company-research.md module
   b. Research company (Bright Data for LinkedIn, Firecrawl for others)
   c. Create company YAML file
   d. STOP - Ask user to validate company research
```

**Phase 2: Analyze Job (company cached)**
```
User: "Company looks good, continue with analysis"

Claude:
1. Load required modules:
   - skills-matching.md
   - scoring-formulas.md
   - database-operations-hybrid.md
2. Load user config and CVs
3. Match job against CV variants
4. Calculate 6-component scores
5. Determine priority tier
6. Create role YAML file
7. Generate Excel via Python script
8. Show summary report
```

### Workflow 4: Contributing Code

**For External Contributors:**

1. **Fork repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow conventions**:
   - Python: PEP 8, type hints, docstrings
   - Markdown: Clear headers, code examples
   - Files: kebab-case naming
4. **Test thoroughly**: Test with sample data
5. **Update docs**: If adding features or changing workflows
6. **Submit PR**: Clear description, link issues
7. **CI/CD checks**: Ensure all workflows pass

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Version Management

### Single Source of Truth

**File**: `version.yaml` (root directory)

```yaml
version: 9.6.0
release_date: '2025-10-30'
status: stable
major: 9
minor: 6
patch: 0
codename: Backlog Feature
```

### Version Sync Process

**ALWAYS follow this order:**

1. Update `version.yaml` manually
2. Run sync script: `python -m host_scripts update-version`
3. Script updates:
   - README.md
   - skill-package/SKILL.md
   - All other version references
4. Review changes with `git diff`
5. Commit all changes together

### Semantic Versioning

- **MAJOR** (X.0.0): Breaking changes, major rewrites
- **MINOR** (9.X.0): New features, backward compatible
- **PATCH** (9.6.X): Bug fixes, small improvements

### Release Status Values

- `stable`: Production-ready
- `beta`: Testing phase
- `alpha`: Early development
- `deprecated`: No longer maintained

---

## Testing & Validation

### GitHub Actions Workflows

Located in `.github/workflows/`:

1. **version-check.yml**
   - Validates version consistency
   - Runs on: Push to main, PRs
   - Checks: version.yaml ↔ README.md ↔ SKILL.md

2. **release.yml**
   - Creates releases automatically
   - Runs on: Push tags (v*)
   - Actions: Package skill, create release, upload artifacts

3. **validate-skill.yml**
   - Validates skill structure
   - Runs on: Push to main, PRs
   - Checks: Required files, module structure, Python syntax, YAML validity

### Manual Testing

**Before committing changes:**

```bash
# Test version consistency
python -c "
import yaml
with open('version.yaml') as f:
    v = yaml.safe_load(f)['version']
with open('README.md') as f:
    assert f'v{v}' in f.read()
print('✅ Version check passed')
"

# Test Python syntax
python -m py_compile skill-package/scripts/*.py

# Test YAML templates
python -c "
import yaml
with open('skill-package/templates/user-config-template.yaml') as f:
    yaml.safe_load(f)
print('✅ Templates valid')
"

# Test paths configuration
python skill-package/config/paths.py
```

### Validation Checklist

Before submitting changes:

- [ ] Version updated in version.yaml
- [ ] Sync script run (`update-version`)
- [ ] CHANGELOG.md updated
- [ ] Python syntax valid
- [ ] YAML files valid
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Git commit message clear
- [ ] All tests pass locally

---

## Common Tasks

### Task 1: Update Documentation

**When**: Documentation is outdated or missing

**Steps**:
1. Identify which doc needs updating:
   - User guides: `docs/guides/user-guide/`
   - Developer guides: `docs/guides/developers-guide/`
   - Feature specs: `docs/project/features/`
2. Edit the relevant .md file
3. Update docs/DOCS_INDEX.yaml if adding new docs
4. Commit with message: `docs: Update [topic] documentation`

**Example**:
```bash
vim docs/guides/user-guide/setup.md
git add docs/guides/user-guide/setup.md
git commit -m "docs: Update MCP server setup instructions"
```

### Task 2: Add Python Helper Script

**When**: Need new utility functionality

**Steps**:
1. Create script in `skill-package/scripts/`
2. Follow template:
   ```python
   """
   Module Name

   Brief description of what this does.
   """

   def main_function(param1: str, param2: int) -> dict:
       """
       Function description.

       Args:
           param1: Description
           param2: Description

       Returns:
           Description of return value

       Example:
           >>> main_function("test", 42)
           {'result': 'success'}
       """
       # Implementation
       pass

   if __name__ == "__main__":
       # Example usage
       pass
   ```
3. Test thoroughly
4. Update module that uses it
5. Add docstring examples
6. Commit with message: `feat: Add [script name] utility`

### Task 3: Fix a Bug

**When**: Issue reported or discovered

**Steps**:
1. Document bug in `docs/project/bugs/` if significant
2. Create branch: `git checkout -b fix/bug-description`
3. Fix the issue
4. Test fix thoroughly
5. Update tests if applicable
6. Commit with message: `fix: [description of fix]`
7. Move bug doc to `resolved/` if created
8. Submit PR or merge

### Task 4: Add Host Automation Command

**When**: Need new CLI command for automation

**Steps**:
1. Create command in `host_scripts/commands/new_command.py`
2. Follow template:
   ```python
   """
   Command Name

   Description of what this command does.
   """

   def run(args):
       """
       Execute the command.

       Args:
           args: Command arguments from argparse
       """
       # Implementation
       pass
   ```
3. Update `host_scripts/cli.py` to add command
4. Update `host_scripts/__main__.py` if needed
5. Test: `python -m host_scripts new-command --help`
6. Document in relevant guide
7. Commit with message: `feat: Add [command] host script`

### Task 5: Create Feature Specification

**When**: Planning new feature

**Steps**:
1. Create file: `docs/project/features/feature-name.md`
2. Use template:
   ```markdown
   # Feature Name

   ## Overview
   Brief description

   ## Use Cases
   - Use case 1
   - Use case 2

   ## Requirements
   - Requirement 1
   - Requirement 2

   ## Implementation Plan
   1. Step 1
   2. Step 2

   ## Token Budget
   Estimated tokens

   ## Testing Strategy
   How to test
   ```
3. Add to `docs/project/features/README.md`
4. Add to roadmap: `docs/project/roadmap/planned.md`
5. Commit with message: `docs: Add [feature] specification`

### Task 6: Migrate Data Structure

**When**: Changing data format or storage

**Steps**:
1. Create migration script in `host_scripts/commands/`
2. Test on sample data first
3. Document migration process
4. Run migration: `python -m host_scripts migrate-to-vX`
5. Validate results
6. Update version (MINOR bump)
7. Document in CHANGELOG.md
8. Commit with message: `feat: Migrate to new data structure`

---

## Troubleshooting Guide

### Issue: "Module not found" when loading skill modules

**Symptom**: Claude reports it cannot find modules like `company-research.md`

**Cause**: Skill package not properly uploaded or wrong file access method

**Solution**:
1. Verify skill-package/ was uploaded to Claude
2. Use `file_read("modules/company-research.md")` not `filesystem:read_text_file`
3. Check relative paths are correct (no leading `/`)

### Issue: "User config not found"

**Symptom**: Cannot load user-config.yaml

**Cause**: Wrong path or file doesn't exist

**Solution**:
1. Check `skill-package/config/paths.py` has correct USER_DATA_BASE
2. Verify `user-data/config/user-config.yaml` exists
3. Ensure MCP Filesystem has access to user-data directory
4. Test: `python skill-package/config/paths.py`

### Issue: "Token budget exhausted"

**Symptom**: Conversation hits token limit

**Cause**: Too many modules loaded or inefficient operations

**Solution**:
1. Start fresh conversation
2. Use progressive loading (load only needed modules)
3. For research: STOP after company creation, validate, then restart
4. Avoid loading all CVs if not needed
5. Never use `directory_tree` on large directories

### Issue: "Version mismatch" in CI/CD

**Symptom**: GitHub Actions version-check.yml fails

**Cause**: Version not synchronized across files

**Solution**:
```bash
# Update version.yaml first
vim version.yaml

# Run sync script
python -m host_scripts update-version

# Verify changes
git diff

# Commit all together
git add .
git commit -m "Bump version to vX.Y.Z"
```

### Issue: "Permission denied" accessing user data

**Symptom**: Cannot read/write files in user-data/

**Cause**: MCP Filesystem doesn't have permission

**Solution**:
1. In Claude settings, grant Filesystem MCP access to user-data directory
2. Check file permissions: `ls -la user-data/`
3. Ensure directory exists and is readable

### Issue: "Invalid YAML frontmatter"

**Symptom**: YAML parsing errors

**Cause**: Malformed YAML in frontmatter

**Solution**:
1. Validate YAML syntax: `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`
2. Check for:
   - Missing closing quotes
   - Incorrect indentation
   - Special characters not escaped
   - Missing colons
3. Use YAML linter if available

### Issue: "Excel generation failed"

**Symptom**: db.xlsx not created

**Cause**: Python dependencies missing or script error

**Solution**:
```bash
# Install dependencies
pip install pyyaml pandas openpyxl

# Test script
python user-data/scripts/dynamic_excel_generator.py

# Check error messages
```

### Issue: "CV not found"

**Symptom**: Cannot load CV variant

**Cause**: File path mismatch or file doesn't exist

**Solution**:
1. Verify CV files exist: `ls -la user-data/config/cv-variants/`
2. Check filenames match user-config.yaml
3. Ensure paths.py has correct CV_BASE
4. Test: `cat user-data/config/cv-variants/cv-general.md`

---

## Additional Resources

### Key Documentation Files

- **README.md**: Main project overview and quick start
- **CONTRIBUTING.md**: Contribution guidelines
- **CHANGELOG.md**: Version history
- **docs/guides/user-guide/setup.md**: Detailed setup instructions
- **docs/guides/developers-guide/architecture.md**: Technical architecture
- **docs/guides/developers-guide/workflows.md**: Development workflows
- **docs/guides/developers-guide/release-process.md**: Release procedures

### External Resources

- **MCP Filesystem**: github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **Bright Data MCP**: Bright Data documentation
- **Firecrawl MCP**: Firecrawl documentation
- **GitHub Repository**: github.com/gsannikov/israeli-tech-career-consultant

### Contact & Support

- **GitHub Issues**: github.com/gsannikov/israeli-tech-career-consultant/issues
- **Documentation**: docs/ directory
- **Discussions**: GitHub Discussions (if enabled)

---

## Appendix: File Naming Conventions

### Python Files
- **Format**: `snake_case.py`
- **Examples**: `config_loader.py`, `yaml_utils.py`

### Markdown Files
- **Format**: `kebab-case.md`
- **Examples**: `company-research.md`, `skills-matching.md`

### YAML Files
- **Format**: `kebab-case.yaml`
- **Examples**: `user-config.yaml`, `version.yaml`

### Data Files (Companies/Roles)
- **Format**: `company-slug.yaml` or `role-slug.yaml`
- **Examples**: `google-israel.yaml`, `google-senior-engineer-2025.yaml`
- **Slug Rules**:
  - Lowercase only
  - Hyphens instead of spaces
  - Remove special characters
  - Keep alphanumeric and hyphens only

---

## Changelog for This Document

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-18 | 1.0.0 | Initial comprehensive CLAUDE.md created |

---

**End of CLAUDE.md**

This document is maintained as part of the Israeli Tech Career Consultant project. For questions or suggestions about this guide, please open an issue on GitHub.
