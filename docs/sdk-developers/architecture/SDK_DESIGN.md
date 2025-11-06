# Claude Skills SDK - Design Document

**Version:** 1.0.0  
**Date:** 2025-11-03  
**Author:** Gur Sannikov  
**Based on:** Israeli Tech Career Consultant v9.3.0  

---

## 🎯 Purpose

Create a comprehensive SDK template for building production-ready Claude skills with:
- ✅ Clear project structure and separation of concerns
- ✅ Token budget management and optimization
- ✅ Context management across conversations
- ✅ MCP server integration patterns
- ✅ Documentation-driven development
- ✅ Version control and release management
- ✅ Modular architecture for scale

---

## 🏗️ Architecture Patterns Extracted

### 1. **Three-Tier Storage Architecture**

```
skill-project/
├── skill-package/          # Logic uploaded to Claude (read-only)
│   ├── SKILL.md           # Main skill definition
│   ├── config/            # Static configuration
│   ├── modules/           # Core skill logic (markdown)
│   ├── references/        # Reference documentation
│   ├── scripts/           # Python utilities
│   └── templates/         # Output templates
│
├── user-data/             # Local user storage (read-write)
│   ├── config/           # User configuration
│   ├── db/               # Dynamic data (YAML)
│   └── logs/             # Operation logs
│
└── docs/                 # Project documentation
    ├── guides/           # User & developer guides
    ├── project/          # Project management
    └── marketing/        # Marketing materials
```

**Key Insight**: Clean separation enables:
- Skill to work for any user (portable logic)
- User data remains private (local storage)
- Documentation separate from runtime code

---

### 2. **Token Budget Management System**

**Problem Solved**: Claude conversations have token limits (~190K). Skills that load large modules or process extensive data can exhaust budget before completing tasks.

**Solution Pattern**:

```markdown
## Token Budget Protection

### Discovery Pattern (Safe)
1. Use `list_allowed_directories` to find MCP roots
2. Navigate incrementally with `list_directory` (non-recursive)
3. Build mental map progressively
4. Reserve `directory_tree` for small, confirmed directories

### Forbidden Operations
❌ NEVER use `directory_tree` on allowed directory roots
❌ NEVER perform recursive operations on large directories
❌ NEVER search entire filesystem

### Budget Checkpoints
- After initialization: < 10% used
- After research phase: < 50% used
- Before analysis: < 40% used
- Stop and restart if exceeded
```

**Implementation**:
- Modular loading (load only what's needed)
- Progressive disclosure (incremental data access)
- Smart caching (research once, reuse)
- Checkpoint monitoring (warn before overrun)

---

### 3. **Context Management Across Conversations**

**Problem Solved**: Claude has no memory between conversations. Complex skills need state continuity.

**Solution Pattern**:

```
DEV_SESSION_STATE.md - Session state tracker
├── Quick Stats (overview)
├── Current Sprint/Focus (active work)
├── Recent Completions (archive when > 50% file)
├── Architecture Overview (structure reference)
├── Known Issues (bug tracking)
├── Technical Debt (future work)
├── Testing Status (validation)
├── Documentation Status (docs tracking)
├── Version History (releases)
├── Ideas/Future (roadmap)
├── Important Links (resources)
├── Session Notes (context)
└── Next Steps/Handoff (continuity)
```

**Key Features**:
- **Structured format**: Consistent sections for quick navigation
- **Archive policy**: Move old content when file grows (>500 lines)
- **Health check**: Self-assessment at end of file
- **Token monitoring**: Track usage in session notes
- **Handoff clarity**: Next steps always documented

---

### 4. **MCP Server Integration Pattern**

**MCP Servers Required**:
1. **Filesystem** (required): Local file operations
2. **Firecrawl** (recommended): Web scraping
3. **Bright Data** (optional): LinkedIn scraping

**Configuration Pattern**:

```python
# skill-package/config/paths.py
"""
Centralized path configuration for filesystem operations.
Update USER_DATA_BASE to match your local setup.
"""

import os

# User data location (EDIT THIS)
USER_DATA_BASE = "/Users/username/MyDrive/skill-project/user-data"

# Derived paths (DO NOT EDIT)
CONFIG_DIR = os.path.join(USER_DATA_BASE, "config")
DB_DIR = os.path.join(USER_DATA_BASE, "db")
LOGS_DIR = os.path.join(USER_DATA_BASE, "logs")

# Auto-create structure on first import
def init_directories():
    """Create directory structure if missing."""
    for dir_path in [CONFIG_DIR, DB_DIR, LOGS_DIR]:
        os.makedirs(dir_path, exist_ok=True)
```

**SKILL.md MCP Guidelines**:

```markdown
## ⚠️ CRITICAL: Storage Configuration

**DO NOT USE**:
- ❌ Notion API
- ❌ Google Drive MCP
- ❌ Any external storage APIs

**ALWAYS USE**:
- ✅ MCP Filesystem tools for user data
- ✅ Paths from paths.py configuration
- ✅ Local YAML/JSON for data storage

**File Access Rules**:
1. **Skill modules**: Use `file_read("modules/name.md")`
2. **User data**: Use `filesystem:read_text_file(absolute_path)`
3. **NEVER mix these access methods**
```

---

### 5. **Modular Documentation System**

**Pattern**: "Core + References" for large modules

**Problem**: Large modules (1000+ lines) consume tokens even when not needed.

**Solution**:

```
skill-package/
├── modules/
│   └── core-feature.md          # 200-300 lines (core logic)
│
└── references/
    ├── core-feature-detailed.md # 800+ lines (implementation)
    ├── core-feature-examples.md # 500+ lines (examples)
    └── core-feature-api.md      # 400+ lines (API reference)
```

**Module Structure**:

```markdown
# Core Feature Module v1.0

## Quick Reference
[Link to full documentation: references/core-feature-detailed.md]

## Overview
Brief description (2-3 paragraphs)

## When to Use
- Use case 1
- Use case 2
- Use case 3

## Quick Start
Minimal example to get started

## Core Functions

### Function 1: Primary Operation
Brief description
**Example**: Minimal code
**See**: references/core-feature-detailed.md#function-1

### Function 2: Secondary Operation
Brief description
**Example**: Minimal code
**See**: references/core-feature-examples.md#example-2

## Integration
How this module connects to others

## Token Budget
Expected token usage: ~XK tokens

## Further Reading
- Full spec: references/core-feature-detailed.md
- Examples: references/core-feature-examples.md
- API: references/core-feature-api.md
```

**Benefits**:
- Load only what's needed (token savings)
- Easy navigation (quick reference first)
- Detailed when required (progressive disclosure)
- Maintainable (separate concerns)

---

### 6. **YAML-Based Configuration**

**Pattern**: YAML for structured data, Markdown for documentation

**Configuration Structure**:

```yaml
# user-data/config/user-config.yaml
skill_metadata:
  version: "1.0.0"
  user_name: "John Doe"
  configured_at: "2025-11-03"

feature_settings:
  feature_1:
    enabled: true
    parameters:
      setting_a: "value"
      setting_b: 42
  feature_2:
    enabled: false

data_sources:
  primary: "/Users/username/data"
  cache: "/Users/username/.cache"
  
scoring_weights:
  dimension_1: 35
  dimension_2: 25
  dimension_3: 20
```

**Python YAML Utilities**:

```python
# skill-package/scripts/yaml_utils.py
"""Utilities for YAML file operations."""

import yaml
from pathlib import Path

def read_yaml(filepath):
    """Read and parse YAML file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def write_yaml(data, filepath):
    """Write data to YAML file."""
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, 
                  allow_unicode=True, sort_keys=False)

def update_yaml(filepath, updates):
    """Update YAML file with new values."""
    data = read_yaml(filepath)
    data.update(updates)
    write_yaml(data, filepath)
```

---

### 7. **Version Management System**

**Files**:
```
version.yaml              # Single source of truth
CHANGELOG.md             # Human-readable history
skill-package/SKILL.md   # Auto-updated from version.yaml
```

**version.yaml**:
```yaml
version: "1.0.0"
release_date: "2025-11-03"
status: "stable"
codename: "Initial Release"

changelog:
  - version: "1.0.0"
    date: "2025-11-03"
    changes:
      - "Initial release"
      - "Core features implemented"
```

**Release Script Pattern**:

```bash
#!/bin/bash
# host_scripts/release.sh

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh <version>"
    exit 1
fi

# Update version.yaml
python -c "
import yaml
with open('version.yaml', 'r') as f:
    data = yaml.safe_load(f)
data['version'] = '$VERSION'
with open('version.yaml', 'w') as f:
    yaml.dump(data, f)
"

# Update SKILL.md header
sed -i '' "s/version: .*/version: $VERSION/" skill-package/SKILL.md

# Git operations
git add .
git commit -m "Release v$VERSION"
git tag "v$VERSION"
git push origin main --tags

echo "✅ Released v$VERSION"
```

---

### 8. **Documentation-Driven Development**

**Pattern**: Write specification before implementation

**Document Hierarchy**:

```
docs/
├── project/
│   ├── features/           # Feature specifications
│   │   ├── TEMPLATE.md    # Spec template
│   │   └── feature-x.md   # Individual specs
│   ├── roadmap/           # Planning documents
│   ├── current-status.md  # Overview
│   └── technical-debt.md  # Known issues
│
├── guides/
│   ├── developer-guide/   # For contributors
│   │   ├── architecture.md
│   │   ├── contributing.md
│   │   └── testing.md
│   └── user-guide/        # For end users
│       ├── setup.md
│       ├── usage.md
│       └── troubleshooting.md
│
└── marketing/             # Public-facing content
    ├── README.md          # Project overview
    ├── pitch.md           # Value proposition
    └── demo-script.md     # Demonstration guide
```

**Feature Specification Template**:

```markdown
# Feature Name

**Status**: [Draft/In Progress/Complete]  
**Priority**: [P0/P1/P2/P3]  
**Owner**: [Name]  
**Estimated Effort**: [hours/days]

## Overview
What the feature does (2-3 paragraphs)

## User Stories
- As a [role], I want [feature] so that [benefit]
- As a [role], I want [feature] so that [benefit]

## Requirements

### Must Have
- [ ] Requirement 1
- [ ] Requirement 2

### Should Have
- [ ] Requirement 3

### Nice to Have
- [ ] Requirement 4

## Technical Design

### Architecture
How it fits into existing system

### Data Model
What data structures are needed

### Integration Points
How it connects to other features

## Implementation Plan

### Phase 1: Foundation (X hours)
- [ ] Task 1
- [ ] Task 2

### Phase 2: Core Features (X hours)
- [ ] Task 3
- [ ] Task 4

### Phase 3: Polish (X hours)
- [ ] Task 5
- [ ] Task 6

## Testing Strategy
- Unit tests
- Integration tests
- Manual validation

## Token Budget
Expected token usage: ~XK tokens

## Documentation Updates
- [ ] Update user guide
- [ ] Update API reference
- [ ] Add examples

## Success Metrics
- Metric 1: Target value
- Metric 2: Target value

## Risks & Mitigations
- Risk 1: Mitigation strategy
- Risk 2: Mitigation strategy

## Open Questions
- Question 1?
- Question 2?
```

---

### 9. **Testing & Validation Pattern**

**Validation Scripts**:

```python
# host_scripts/validate.py
"""Validation script for skill integrity."""

import os
import yaml
from pathlib import Path

def validate_structure():
    """Check directory structure is correct."""
    required_dirs = [
        "skill-package/modules",
        "skill-package/config",
        "user-data/config",
        "docs/guides"
    ]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Missing: {dir_path}")
            return False
    print("✅ Directory structure valid")
    return True

def validate_config():
    """Check configuration files are valid."""
    config_path = "user-data/config/user-config.yaml"
    try:
        with open(config_path) as f:
            yaml.safe_load(f)
        print("✅ Configuration valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def validate_skill_md():
    """Check SKILL.md has required sections."""
    required_sections = [
        "# ",  # Title
        "## Overview",
        "## ⚠️ CRITICAL: Storage Configuration"
    ]
    
    with open("skill-package/SKILL.md") as f:
        content = f.read()
    
    for section in required_sections:
        if section not in content:
            print(f"❌ Missing section: {section}")
            return False
    
    print("✅ SKILL.md structure valid")
    return True

if __name__ == "__main__":
    all_valid = all([
        validate_structure(),
        validate_config(),
        validate_skill_md()
    ])
    
    if all_valid:
        print("\n✅ All validations passed!")
    else:
        print("\n❌ Validation failed")
        exit(1)
```

---

### 10. **GitHub & Release Management**

**Repository Structure**:

```
.github/
├── workflows/
│   ├── validate.yml      # CI validation
│   └── release.yml       # Auto-release
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
└── PULL_REQUEST_TEMPLATE.md

.gitignore                # What not to commit
CODE_OF_CONDUCT.md        # Community guidelines
CONTRIBUTING.md           # How to contribute
LICENSE                   # MIT/Apache 2.0
README.md                 # Project overview
```

**Critical .gitignore**:

```gitignore
# User data (NEVER commit personal info)
user-data/config/user-config.yaml
user-data/config/cv-variants/
user-data/config/candidate-profile.md
user-data/db/
user-data/logs/

# Keep templates only
!user-data/config/user-config-template.yaml
!skill-package/templates/

# Python
__pycache__/
*.pyc
.pytest_cache/

# System
.DS_Store
*.swp
*.swo

# IDE
.vscode/
.idea/
```

**Auto-Release GitHub Action**:

```yaml
# .github/workflows/release.yml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Release Package
        run: |
          mkdir release-package
          cp -r skill-package release-package/
          cp -r docs release-package/
          cp README.md LICENSE release-package/
          zip -r skill-package-${{ github.ref_name }}.zip release-package/
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: skill-package-${{ github.ref_name }}.zip
          generate_release_notes: true
```

---

## 🎯 SDK Template Structure

Based on extracted patterns, the SDK template will provide:

```
claude-skill-template/
├── skill-package/              # Upload to Claude
│   ├── SKILL.md               # ⭐ Main skill definition
│   ├── config/
│   │   ├── paths.py           # ⭐ Path configuration
│   │   └── config.yaml        # Static configuration
│   ├── modules/
│   │   ├── core-module.md     # ⭐ Core logic template
│   │   └── module-template.md # Module structure guide
│   ├── references/
│   │   └── reference-template.md
│   ├── scripts/
│   │   ├── yaml_utils.py      # ⭐ YAML helpers
│   │   └── config_loader.py   # ⭐ Config loader
│   └── templates/
│       └── output-template.yaml
│
├── user-data/                 # Local storage
│   ├── config/
│   │   └── user-config-template.yaml
│   ├── db/                    # Created at runtime
│   └── logs/                  # Created at runtime
│
├── docs/
│   ├── guides/
│   │   ├── developer-guide/
│   │   │   ├── architecture.md    # ⭐ Architecture guide
│   │   │   ├── module-guide.md    # ⭐ How to create modules
│   │   │   └── testing.md
│   │   └── user-guide/
│   │       ├── setup.md           # ⭐ Setup instructions
│   │       ├── mcp-servers.md     # ⭐ MCP configuration
│   │       └── troubleshooting.md
│   └── project/
│       ├── features/
│       │   └── TEMPLATE.md        # ⭐ Feature spec template
│       └── current-status.md
│
├── host_scripts/              # Automation
│   ├── validate.py            # ⭐ Validation script
│   ├── release.sh             # ⭐ Release automation
│   └── setup.sh               # ⭐ Initial setup
│
├── .github/
│   ├── workflows/
│   │   ├── validate.yml
│   │   └── release.yml
│   └── ISSUE_TEMPLATE/
│
├── .gitignore                 # ⭐ What not to commit
├── README.md                  # ⭐ Project overview
├── CONTRIBUTING.md
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── version.yaml               # ⭐ Version tracking
└── DEV_SESSION_STATE.md       # ⭐ Session state template

⭐ = Essential files that must be customized
```

---

## 📋 Implementation Checklist

### Phase 1: Core Structure ✅
- [x] Design document
- [ ] Create directory structure
- [ ] Essential templates
- [ ] Configuration system

### Phase 2: Documentation
- [ ] README with setup guide
- [ ] Architecture guide
- [ ] Module creation guide
- [ ] MCP server guide

### Phase 3: Automation
- [ ] Validation scripts
- [ ] Release automation
- [ ] Setup script
- [ ] GitHub Actions

### Phase 4: Examples
- [ ] Example skill module
- [ ] Example configuration
- [ ] Example feature spec
- [ ] Example tests

---

## 🚀 Next Steps

1. **Create directory structure** in filesystem
2. **Generate template files** with placeholders
3. **Write comprehensive README**
4. **Create blog post** explaining:
   - Why Claude skills matter
   - How this SDK helps
   - How to use it
   - Real-world example (career consultant)
5. **Push to GitHub** with proper release

---

**Status**: Design complete, ready for implementation  
**Token Budget**: ~62K used, 128K remaining - plenty of room for implementation  
**Next Action**: Create directory structure and template files
