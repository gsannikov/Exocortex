# SDK Configuration

This directory contains centralized configuration management for the Claude Skill Template.

## Files

### `template-config.yaml`
**Single source of truth** for all repository constants, settings, and metadata.

**Contains:**
- Version information
- Repository details (name, owner, URLs)
- Directory paths
- Python/Node.js versions
- Dependencies and their versions
- Storage backends list
- Testing configuration
- GitHub Actions settings
- File conventions
- External references

**Usage:** All configuration values should be read from this file, not hardcoded elsewhere.

### `version.yaml`
**Legacy version file** - Will be deprecated in favor of `template-config.yaml`.

Currently used by release scripts. Future versions will use `template-config.yaml` exclusively.

### `config_loader.py`
**Python library** for loading and accessing configuration values.

**Usage in Python:**
```python
from sdk.config.config_loader import get_config

config = get_config()

# Access via properties
print(config.version)              # "1.1.0"
print(config.repo_owner)           # "gsannikov"
print(config.python_min_version)   # "3.8"

# Access via dot notation
print(config.get('version.template'))           # "1.1.0"
print(config.get('repository.owner'))           # "gsannikov"
print(config.get('storage_backends.available')) # ["local", "github", ...]

# URL helpers
print(config.get_url('base'))     # Full GitHub URL
print(config.get_clone_url('ssh')) # SSH clone URL

# Path helpers
print(config.get_path('skill_package'))  # "skill-package"
print(config.get_full_path('skill_package')) # Full Path object

# Dependency helpers
print(config.get_dependency_version('pyyaml'))  # "6.0"
print(config.get_pip_install_command('pyyaml')) # "PyYAML>=6.0"

# Storage backend helpers
print(config.get_storage_backend_display_name('local')) # "Local Filesystem"

# Validation helpers
print(config.get_root_allowed_files())    # List of allowed root files
print(config.get_session_patterns())      # List of session file patterns
```

**CLI Usage:**
```bash
# Show summary
python sdk/config/config_loader.py

# Get specific value
python sdk/config/config_loader.py get version.template
python sdk/config/config_loader.py get repository.owner

# Access shortcut properties
python sdk/config/config_loader.py version
python sdk/config/config_loader.py repo_name
```

### `get-config.py`
**Shell script helper** for extracting config values in non-Python environments (e.g., GitHub Actions, Bash scripts).

**Usage:**
```bash
# Get single value
python sdk/config/get-config.py version.template
# Output: 1.1.0

# Get comma-separated list
python sdk/config/get-config.py --list storage_backends.available
# Output: local,github,checkpoint,email,notion

# Get multiple values as JSON
python sdk/config/get-config.py --json version.template repository.owner
# Output: {"template": "1.1.0", "owner": "gsannikov"}

# GitHub Actions environment variables format
python sdk/config/get-config.py --github-env version.template python.tested_version
# Output:
# VERSION_TEMPLATE=1.1.0
# PYTHON_TESTED_VERSION=3.10
```

**In GitHub Actions Workflows:**
```yaml
- name: Load config
  id: config
  run: |
    VERSION=$(python sdk/config/get-config.py version.template)
    PYTHON_VERSION=$(python sdk/config/get-config.py python.tested_version)
    echo "version=$VERSION" >> $GITHUB_OUTPUT
    echo "python_version=$PYTHON_VERSION" >> $GITHUB_OUTPUT

- name: Use config
  run: |
    echo "Template version: ${{ steps.config.outputs.version }}"
    echo "Python version: ${{ steps.config.outputs.python_version }}"
```

### `.gitleaks.toml`
**Secrets scanning configuration** for Gitleaks tool.

Defines patterns for detecting secrets, credentials, and private data in code.

## Configuration Management Best Practices

### 1. Single Source of Truth
All configuration values should be defined in `template-config.yaml`. Never hardcode values that might change.

### 2. Update Process
When updating configuration:
1. Update `template-config.yaml`
2. If it's a version change, also update `docs/shared/CHANGELOG.md`
3. Run validation to ensure no syntax errors
4. Commit with clear message about what was changed

### 3. Adding New Configuration
When adding a new configurable value:
1. Add it to `template-config.yaml` in the appropriate section
2. Add helper methods to `config_loader.py` if frequently used
3. Document it in this README
4. Update any scripts that use the value to read from config

### 4. Usage Patterns

**DO:**
```python
# Good - uses centralized config
from sdk.config.config_loader import get_config
config = get_config()
version = config.version
```

**DON'T:**
```python
# Bad - hardcoded value
version = "1.1.0"
```

**DO:**
```bash
# Good - reads from config
VERSION=$(python sdk/config/get-config.py version.template)
echo "Version: $VERSION"
```

**DON'T:**
```bash
# Bad - hardcoded value
VERSION="1.1.0"
echo "Version: $VERSION"
```

## Configuration Sections

### Version Information
- Template version, release date, status
- Used for: release automation, badges, documentation

### Repository Information
- Repository name, owner, description
- Used for: clone commands, URLs, documentation

### URLs
- GitHub URLs (base, issues, discussions, releases)
- External references (Anthropic, source skill)
- Used for: documentation links, examples

### Paths
- All directory paths in the repository
- Used for: scripts, validation, documentation
- Ensures consistency across all references

### Python/Node.js Configuration
- Minimum and tested versions
- Used for: workflows, documentation, validation

### Dependencies
- Package names, minimum versions, install commands
- Used for: requirements files, documentation, setup scripts

### Storage Backends
- Available backends, display names, descriptions
- Used for: validation, documentation, setup

### Testing
- Test count, test names, disabled tests
- Used for: documentation, workflows, validation

### GitHub Actions
- Tool versions, timeout settings, configuration
- Used for: workflows, ensuring consistency

### File Conventions
- Allowed root files, forbidden extensions, patterns
- Used for: TEST 12 validation, cleanup scripts

### Release Configuration
- Package includes, checksum algorithm
- Used for: release automation

## Centralization Statistics

Before centralization:
- **200+ instances** of duplicated configuration values
- **3 inconsistencies** found (Python version, backend names, etc.)
- Manual updates required across 40+ files

After centralization:
- **1 source** of truth (`template-config.yaml`)
- **Automatic consistency** through shared access
- **Easy updates** - change once, update everywhere

## Migration Status

### ✅ Centralized
- Version information (✅ Complete)
- Repository details (✅ Complete)
- URLs (✅ Complete)
- Paths (✅ Complete)
- Dependencies (✅ Complete)
- Storage backends (✅ Complete)
- Testing configuration (✅ Complete)
- GitHub Actions settings (✅ Complete)
- File conventions (✅ Complete)

### 🔄 Partially Migrated
- Workflows (can now use get-config.py, but not yet updated)
- Documentation (some still has hardcoded values)
- Scripts (some still have hardcoded paths)

### 📋 Future Work
- Update all workflows to use centralized config
- Update all documentation to pull from config
- Add config validation to TEST suite
- Create automated config update checks

## Contributing

When adding new configuration:
1. Add to appropriate section in `template-config.yaml`
2. Follow existing structure and naming conventions
3. Add comments explaining purpose
4. Update this README
5. Add accessor methods to `config_loader.py` if needed
6. Update any affected documentation

## Questions?

- **Where should I add a new config value?** → `template-config.yaml`
- **How do I access config in Python?** → Use `config_loader.py`
- **How do I access config in workflows?** → Use `get-config.py`
- **How do I update a version?** → Update `template-config.yaml`, then `CHANGELOG.md`
- **Why two config files?** → `version.yaml` is legacy, will be deprecated

---

**Last Updated:** 2025-11-06
**Config Version:** 1.0.0
