# Testing Guide

This guide explains the comprehensive testing strategy for the Claude Skills SDK Template.

---

## Test Suite Overview

The project includes two GitHub workflows:

1. **`validate.yml`** - Basic validation (runs on every push/PR)
2. **`comprehensive-tests.yml`** - Full test suite (11 comprehensive tests)

---

## The 11 Comprehensive Tests

### 1. 🐍 Python Syntax & Import Validation

**What it does**: Validates Python syntax and import statements

**Why it matters**: Catches syntax errors and missing imports before deployment

**Checks**:
- All `.py` files compile without errors
- All imports resolve correctly
- No circular dependencies

**How to run locally**:
```bash
python -m py_compile skill-package/scripts/*.py
python -m py_compile host_scripts/*.py
```

---

### 2. 🐚 Shell Script Validation (ShellCheck)

**What it does**: Validates bash scripts for common errors

**Why it matters**: Prevents bash pitfalls like unquoted variables, missing error handling

**Checks**:
- Proper quoting
- Error handling (set -e)
- Variable usage
- Common bash antipatterns

**How to run locally**:
```bash
# Install ShellCheck
brew install shellcheck  # macOS
sudo apt-get install shellcheck  # Linux

# Run checks
shellcheck *.sh host_scripts/*.sh
```

---

### 3. 🔗 Markdown Link Validation

**What it does**: Checks all markdown files for broken links

**Why it matters**: Ensures documentation is accessible and complete

**Checks**:
- Internal links (to other files)
- External links (to websites)
- Anchor links (to sections)

**How to run locally**:
```bash
npm install -g markdown-link-check
markdown-link-check README.md
```

---

### 4. 💾 Storage Configuration Tests

**What it does**: Validates storage configuration templates

**Why it matters**: Ensures users get valid configuration templates

**Checks**:
- YAML syntax is valid
- Required fields present (`storage`, `backend`)
- Backend values are valid
- Backend-specific config exists

**How to run locally**:
```bash
python -c "import yaml; yaml.safe_load(open('user-data-templates/config/storage-config-template.yaml'))"
```

---

### 5. 🧪 Storage Backend Unit Tests

**What it does**: Tests storage.py functionality

**Why it matters**: Ensures storage backends work correctly

**Checks**:
- CheckpointBackend save/load/delete
- Storage interface compliance
- Error handling

**How to run locally**:
```bash
pip install pytest
python tests/test_storage_basic.py
```

**Extending tests**: Add tests for other backends in `tests/` directory

---

### 6. 📚 Documentation Completeness Check

**What it does**: Verifies required documentation sections exist

**Why it matters**: Ensures consistent, complete documentation

**Checks**:
- README.md has: Quick Start, Documentation, License
- SKILL.md has: Overview, Storage Configuration
- DEPENDENCIES.md has: Storage, Backend sections
- CONTRIBUTING.md exists

**How to run locally**:
```bash
# Check for required sections
grep -i "## Quick Start" README.md
grep -i "## Overview" skill-package/SKILL.md
```

---

### 7. 🔒 Security Scanning (Bandit)

**What it does**: Scans Python code for security vulnerabilities

**Why it matters**: Identifies security issues before they reach production

**Checks**:
- Hardcoded passwords/secrets
- SQL injection vulnerabilities
- Shell injection risks
- Weak cryptography usage
- Unsafe deserialization

**How to run locally**:
```bash
pip install bandit
bandit -r skill-package/scripts/ host_scripts/ -ll
```

**Report**: Generates `bandit-report.json` artifact

---

### 8. 🛡️ Dependency Vulnerability Check

**What it does**: Checks dependencies for known CVEs

**Why it matters**: Prevents using packages with security vulnerabilities

**Checks**:
- All packages in requirements.txt
- Known vulnerabilities (CVE database)
- Severity levels

**How to run locally**:
```bash
pip install safety
safety check
```

**Report**: Generates `safety-report.json` artifact

---

### 9. ✨ Code Style & Linting (Flake8)

**What it does**: Enforces consistent code style

**Why it matters**: Maintains readable, maintainable code

**Checks**:
- PEP 8 compliance
- Line length (max 100 chars)
- Unused imports
- Undefined variables
- Complexity metrics

**How to run locally**:
```bash
pip install flake8
flake8 skill-package/scripts/ host_scripts/ --max-line-length=100
```

**Configuration**: Customize in `.flake8` or `setup.cfg`

---

### 10. 🔐 Secrets & Private Data Detection (Gitleaks)

**What it does**: Scans all files for secrets, credentials, and private data

**Why it matters**: Prevents accidental exposure of sensitive information

**Checks**:
- API keys and tokens (GitHub, AWS, Google, Slack, Stripe, etc.)
- Passwords and secrets in code
- Private keys (RSA, SSH, OpenSSH)
- Database connection strings
- OAuth tokens and JWTs
- Email addresses (potential PII)
- Phone numbers (potential PII)
- Social Security Numbers
- Credit card numbers
- High-entropy strings (likely secrets)

**How to run locally**:
```bash
# Install Gitleaks
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.1/gitleaks_8.18.1_linux_x64.tar.gz
tar -xzf gitleaks_8.18.1_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# Run scan
gitleaks detect --config .gitleaks.toml --verbose
```

**Configuration**: `.gitleaks.toml` in repository root

**What to do if secrets are found**:
1. **Remove the secret immediately** from code
2. **Rotate/revoke the exposed credential** (change password, regenerate API key)
3. **Use environment variables** for credentials instead
4. **Add to .gitignore** if in user-data files
5. **Rewrite git history** if secret was committed (use `git filter-branch` or BFG Repo-Cleaner)

**False positives**: Add to allowlist in `.gitleaks.toml`:
```toml
[allowlist]
regexes = [
  '''your-pattern-here''',
]
```

**Common secrets to avoid**:
```python
# ❌ BAD - Hardcoded secret
api_key = "my-secret-api-key-12345"  # Never hardcode!

# ✅ GOOD - Use environment variable
api_key = os.environ.get("API_KEY")

# ✅ BETTER - Use secrets management
from secretmanager import get_secret
api_key = get_secret("api-key-name")
```

**Report**: Generates `gitleaks-secrets-report.txt` artifact

---

### 11. 🎯 End-to-End Template Test

**What it does**: Tests complete workflow from setup to validation

**Why it matters**: Ensures the entire template works as designed

**Tests**:
1. `host_scripts/setup.sh` runs successfully
2. Storage configuration can be created
3. `validate.py` passes
4. `integrate-skill-creator.sh` works
5. Template structure is complete

**How to run locally**:
```bash
# Manual E2E test
bash host_scripts/setup.sh
cp -r user-data-templates user-data-test
python host_scripts/validate.py
bash integrate-skill-creator.sh
```

---

## Running Tests Locally

### Run all tests:
```bash
# Python tests
python -m py_compile skill-package/scripts/*.py
python tests/test_storage_basic.py

# Shell tests
shellcheck *.sh host_scripts/*.sh

# Security
bandit -r skill-package/scripts/
safety check

# Style
flake8 skill-package/scripts/ host_scripts/

# Validation
python host_scripts/validate.py
```

### Quick test:
```bash
# Just run validation and basic checks
python host_scripts/validate.py
python -m py_compile skill-package/scripts/*.py
```

---

## Adding New Tests

### 1. Unit Tests

Create test files in `tests/` directory:

```python
# tests/test_config_loader.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "skill-package" / "scripts"))

def test_config_loader():
    from config_loader import load_config
    # Your test here
    assert True
```

### 2. Integration Tests

Add to the E2E test in `comprehensive-tests.yml`:

```yaml
- name: My Integration Test
  run: |
    echo "Testing my feature..."
    # Your test commands
    echo "✅ Test passed"
```

### 3. GitHub Workflow Jobs

Add new job to workflow:

```yaml
jobs:
  my-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run my test
        run: ./my-test-script.sh
```

---

## Test Reports

After each workflow run, the following reports are available:

1. **Bandit Security Report** (`bandit-report.json`)
   - Download from Actions > Artifacts
   - Shows security issues by severity

2. **Safety Vulnerability Report** (`safety-report.json`)
   - Download from Actions > Artifacts
   - Shows vulnerable dependencies

3. **Workflow Logs**
   - All test output in GitHub Actions logs
   - Color-coded pass/fail indicators

---

## Continuous Integration Strategy

### On Every Push/PR:
- Basic validation (`validate.yml`)
- YAML syntax checking

### On Main/Develop Branches:
- Full comprehensive test suite
- Security scanning
- Dependency checks

### On Release Tags (v*):
- All tests pass
- Release package creation
- GitHub release published

---

## Test Coverage Goals

| Component | Current Coverage | Goal |
|-----------|------------------|------|
| Storage Backends | Basic | 80%+ |
| Config Loader | None | 70%+ |
| YAML Utils | None | 70%+ |
| Shell Scripts | Syntax only | Logic tests |
| Documentation | Completeness | Link validation |

---

## Troubleshooting

### Test failing locally but passing in CI?
- Check Python version (CI uses 3.10)
- Check environment variables
- Ensure dependencies installed

### Test passing locally but failing in CI?
- Check file paths (absolute vs relative)
- Check git ignored files
- Review CI logs for differences

### Security scan false positives?
- Add exclusions to Bandit config
- Document why issue is not a concern
- Use `# nosec` comments (sparingly)

---

## Best Practices

1. **Run tests before committing**
   ```bash
   python host_scripts/validate.py
   flake8 .
   ```

2. **Fix issues immediately**
   - Don't let test failures accumulate
   - Address security findings promptly

3. **Keep tests fast**
   - Unit tests should run in seconds
   - E2E tests under 5 minutes

4. **Test what matters**
   - Focus on user-facing functionality
   - Test failure scenarios
   - Validate security boundaries

5. **Document test failures**
   - Known issues in GitHub Issues
   - Workarounds in this guide

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [ShellCheck Wiki](https://www.shellcheck.net/wiki/)
- [Flake8 Documentation](https://flake8.pycqa.org/)

---

**Last Updated**: 2025-11-05 | **v1.1.0**
