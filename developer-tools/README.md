# Developer Tools

Automation scripts for managing your Claude skill.

## Available Scripts

### `validate.py`
Validates skill structure, configuration, and integrity.

**Usage:**
```bash
python3 validate.py
```

**Checks:**
- Directory structure
- SKILL.md format
- Configuration files
- Python scripts
- Templates
- Documentation

**Exit codes:**
- 0: All validations passed
- 1: Validation failed

---

### `setup.sh`
Initializes directory structure and configuration.

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

**Actions:**
- Creates directory structure
- Copies configuration templates
- Checks Python dependencies
- Optionally initializes Git

---

### `release.sh`
Automates version updates and release package creation.

**Usage:**
```bash
chmod +x release.sh
./release.sh 1.0.0
```

**Actions:**
- Updates version in configuration files
- Creates release package (ZIP)
- Creates Git commit and tag
- Prepares for GitHub release

**Requirements:**
- Git repository initialized
- Semantic versioning format (MAJOR.MINOR.PATCH)

---

## Making Scripts Executable

On macOS/Linux, make scripts executable:
```bash
chmod +x setup.sh release.sh
```

For Python scripts, use:
```bash
python3 validate.py
```

---

## Dependencies

**Python 3.8+** with:
- PyYAML: `pip3 install pyyaml`

**Git** (for release.sh)

---

## Workflow Example

1. **Initial setup:**
   ```bash
   ./setup.sh
   ```

2. **After making changes:**
   ```bash
   python3 validate.py
   ```

3. **Create release:**
   ```bash
   ./release.sh 1.0.0
   git push origin main --tags
   ```
