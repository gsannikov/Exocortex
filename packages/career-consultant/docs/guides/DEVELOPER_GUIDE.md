# Developer Guide

Complete guide for contributing to and maintaining the Israeli Tech Career Consultant.

## Table of Contents
1. [Architecture](#architecture)
2. [Release Process](#release-process)
3. [Testing](#testing)

---

## Architecture

### System Overview

**Hybrid architecture**: Generic skill logic + user-specific data

**Components**:
- `skill-package/`: Claude skill code (modules, scripts, templates)
- `user-data/`: Personal job search data (local, not versioned)
- `host_scripts/`: Release, validation, migration tools

### Directory Structure

```
career-consultant.skill/
├── skill-package/
│   ├── SKILL.md (orchestrator)
│   ├── modules/ (job analysis, company research)
│   ├── scripts/ (Python helpers)
│   ├── templates/ (YAML/MD templates)
│   └── config/ (paths configuration)
├── user-data/ (gitignored)
│   ├── profile/ (settings, CVs, candidate info)
│   ├── companies/ (cached research)
│   ├── jobs/ (backlog, analyzed roles)
│   └── reports/ (Excel, HTML outputs)
└── host_scripts/
    ├── release/ (packaging, validation)
    └── migrations/ (data structure updates)
```

### Key Modules

- `SKILL.md`: Main orchestrator, loaded first by Claude
- `company-research.md`: Company investigation workflow
- `job-backlog-manager.md`: Quick job capture system
- `config/paths.py`: Single source of truth for paths

### Data Flow

1. User provides job URL
2. SKILL.md loads appropriate module
3. Module uses Python scripts for complex operations
4. Data saved to user-data/ in YAML+MD format
5. Reports generated (Excel/HTML)

---

## Release Process

### Interactive Release (Recommended)

```bash
python -m host_scripts release
```

This interactive guide walks you through:
1. Choose release type (patch/minor/major)
2. Validate package
3. Bump version (auto-syncs to all docs)
4. Review changes
5. Commit and create tag
6. Push to GitHub

GitHub Actions automatically creates the release page.

### Quick Release (Non-Interactive)

```bash
# Patch release (9.23.0 → 9.23.1)
python -m host_scripts release --patch

# Minor release (9.23.0 → 9.24.0)  
python -m host_scripts release --minor

# Major release (9.23.0 → 10.0.0)
python -m host_scripts release --major

# Dry run
python -m host_scripts release --minor --dry-run
```

### Manual Release (Step-by-Step)

If you prefer explicit control:

```bash
# 1. Validate
python -m host_scripts validate all

# 2. Bump version
python -m host_scripts bump-version minor

# 3. Commit
git add .
git commit -m "chore: release v9.24.0"

# 4. Tag and push
git tag v9.24.0
git push origin main --tags
```

### What GitHub Actions Does

After you push the tag, the `release.yml` workflow automatically:
- Creates GitHub Release page
- Uploads `.skill` artifact
- Publishes release notes from `releases/RELEASE_NOTES_vX.md`

### Host Scripts

The `host_scripts/` directory contains utilities:

**1. `validate` - Validation tool**
```bash
python -m host_scripts validate docs     # Validate documentation structure
python -m host_scripts validate package  # Validate skill package
python -m host_scripts validate all      # Run all validations
```

**2. `bump-version` - Version management**
```bash
python -m host_scripts bump-version show   # Display current version
python -m host_scripts bump-version patch  # 9.23.0 -> 9.23.1 (auto-syncs)
python -m host_scripts bump-version minor  # 9.23.0 -> 9.24.0 (auto-syncs)
python -m host_scripts bump-version major  # 9.23.0 -> 10.0.0 (auto-syncs)
```
*Note: Bumping automatically syncs the version to all documentation files.*

**3. `release` - Interactive release guide**
```bash
python -m host_scripts release            # Interactive mode
python -m host_scripts release --minor    # Direct minor release
```
```

### Rollback

```bash
# Delete tag
git tag -d v9.10.0
git push origin :refs/tags/v9.10.0

# Revert commit
git revert HEAD
git push
```

---

## Testing

### Test Structure

```
tests/
├── unit/ (fast, isolated)
│   ├── test_paths.py
│   ├── test_utils.py
│   └── test_scoring.py
└── integration/ (slower, end-to-end)
    └── test_workflow.py
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=skill-package/scripts --cov-report=html

# Specific test
pytest tests/unit/test_paths.py::test_user_data_base
```

### Writing Tests

**Unit test example**:
```python
def test_normalize_slug():
    from slug_utils import normalize_slug
    assert normalize_slug("Google Israel") == "google-israel"
    assert normalize_slug("Meta (Facebook)") == "meta-facebook"
```

**Integration test example**:
```python
@pytest.fixture
def temp_user_data(tmp_path):
    # Setup temporary user-data structure
    (tmp_path / "profile").mkdir()
    return tmp_path

def test_full_analysis(temp_user_data):
    # Test complete job analysis workflow
    pass
```

### Validation Scripts

```bash
# Documentation structure
python -m host_scripts validate docs

# Skill package structure
python -m host_scripts validate package

# All validations (CI)
python -m host_scripts validate all
```

### CI/CD

**GitHub Actions workflows**:
- `test.yml`: Runs on every push (Python 3.8-3.11)
- `validate-skill.yml`: Validates structure
- `version-check.yml`: Ensures version consistency
- `release.yml`: Auto-publishes releases

**Badges**:
- Test status
- Coverage percentage
- Latest release version

---

## Contributing

### Development Setup

```bash
# 1. Clone repository
git clone https://github.com/gsannikov/israeli-tech-career-consultant.git
cd israeli-tech-career-consultant

# 2. Install dev dependencies
pip install -r requirements-dev.txt

# 3. Run tests
pytest

# 4. Create branch
git checkout -b feature/my-feature
```

### Code Style

- **Python**: Black formatter, flake8 linter
- **Markdown**: Standard markdown, kebab-case filenames
- **YAML**: 2-space indentation

```bash
# Format code
black skill-package/scripts/ host_scripts/

# Lint
flake8 skill-package/scripts/ host_scripts/
```

### Pull Request Process

1. Create feature branch
2. Write tests
3. Update documentation
4. Run full test suite
5. Create PR with description
6. Address review feedback
7. Squash and merge

### Commit Messages

Follow conventional commits:
```
feat: add LinkedIn MCP support
fix: correct scoring calculation
docs: update setup guide
chore: bump version to 9.11.0
refactor: simplify company research flow
```
