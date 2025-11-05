# Claude Skills SDK Template

**Version:** 1.1.0
**Type:** Development Framework
**License:** MIT

---

## Overview

The Claude Skills SDK Template is a production-ready framework for building Claude Skills with multi-backend storage, automation tools, and best practices. This template provides a complete architecture for creating skills that persist data, manage token budgets, and follow Anthropic's recommended patterns.

**Key Features:**
- 5 storage backend options (Local, GitHub, Checkpoint, Email, Notion)
- Three-tier architecture (skill-package, user-data, docs)
- Automated validation and release scripts
- Token budget management patterns
- Interactive onboarding for new developers

---

## ⚠️ CRITICAL: Storage Configuration

**Before using this skill**, you must configure a storage backend. The skill will not function properly without storage configuration.

### Quick Setup (Recommended: Local Filesystem)

1. **Copy user data templates:**
   ```bash
   cp -r user-data-templates user-data
   cd user-data/config
   cp storage-config-template.yaml storage-config.yaml
   ```

2. **Edit storage-config.yaml:**
   ```yaml
   storage:
     backend: local
     local:
       base_path: /absolute/path/to/user-data
   ```

3. **Validate setup:**
   ```bash
   python host_scripts/validate.py
   ```

### Alternative Backends

For multi-device sync or team collaboration, see [DEPENDENCIES.md](../../DEPENDENCIES.md) for:
- **GitHub** - Version-controlled storage with multi-device sync
- **Email** - Email-based persistence
- **Notion** - Structured database storage
- **Checkpoint** - Session-only (testing)

**IMPORTANT:** Without proper storage configuration, data operations will fail. Always validate your setup before uploading to Claude.

---

## 👋 New Here? Start With Onboarding!

**If you just cloned this repo and want to get started**, Claude has a comprehensive onboarding guide ready for you.

### Quick Start for New Developers

1. **Attach this GitHub repo** to your Claude conversation
2. **Say "hi" or "help me get started"**
3. **Follow Claude's interactive onboarding**

Claude will read the [CLAUDE_ONBOARDING_GUIDE.md](../../CLAUDE_ONBOARDING_GUIDE.md) and guide you through:
- Understanding what this template does
- Choosing and configuring a storage backend
- Creating your first skill
- Using the automation tools

**Estimated time:** 10-15 minutes to full setup

### Manual Setup (If You Prefer)

See [QUICK_SETUP.md](../../QUICK_SETUP.md) for step-by-step written instructions.

---

## What This Template Provides

A production-ready framework for building Claude Skills with:

1. **Multi-Backend Storage** (5 options)
   - Local Filesystem, GitHub, Checkpoint, Email, Notion
2. **Complete Architecture** 
   - Three-tier: skill-package, user-data, docs
3. **Automation Tools**
   - Validation, release, setup scripts
4. **Best Practices**
   - Official Anthropic patterns included

---

## Storage Backend System

### Supported Backends

| Backend | Setup | Persist | Multi-Device | Best For |
|---------|-------|---------|--------------|----------|
| **Local** | Easy | ✅ | ❌ | Single device |
| **GitHub** | Medium | ✅ | ✅ | Multi-device, teams |
| **Checkpoint** | None | ❌ | ❌ | Testing |
| **Email** | Medium | ✅ | ✅ | Email workflows |
| **Notion** | Medium | ✅ | ✅ | Structured data |

### Quick Configuration

```yaml
# user-data/config/storage-config.yaml
storage:
  backend: local  # Choose: local, github, checkpoint, email, notion
  local:
    base_path: /path/to/user-data
```

### Usage

```python
from scripts.storage import init_storage, save_data, load_data

init_storage("user-data/config/storage-config.yaml")

# Save/load data
save_data("db/item.yaml", data)
item = load_data("db/item.yaml")
```

**Full storage docs:** See [DEPENDENCIES.md](../../DEPENDENCIES.md)

---

## Directory Structure

```
skill-package/          # Upload to Claude
├── SKILL.md           # This file
├── config/            # Skill configuration
├── scripts/           # Python utilities
│   └── storage.py     # Multi-backend storage
├── modules/           # Optional skill modules
└── examples/          # Example skills

user-data/             # Your data (not uploaded)
├── config/            # Your settings
├── db/                # Your database
└── logs/              # Your logs

docs/                  # Documentation
host_scripts/          # Automation
```

---

## Essential Commands

```bash
# Validate skill structure
python host_scripts/validate.py

# Create release package
./host_scripts/release.sh 1.1.0

# Integrate skill-creator (optional)
./integrate-skill-creator.sh
```

---

## Token Budget Management

Follow progressive disclosure:
1. Load core modules first (~10K tokens)
2. Load detailed references only when needed
3. Monitor usage with status checks
4. Archive/restart if approaching limits

---

## File Access Rules

**Skill Files (Read-Only):**
```python
# Use file_read tool
content = file_read("modules/analysis.md")
```

**User Data (Read-Write):**
```python
# Use storage backend
save_data("db/item.yaml", data)
data = load_data("db/item.yaml")
```

**Never mix these!** Storage backend works across all backend types.

---

## Documentation

- **README.md** - Main documentation
- **QUICK_SETUP.md** - Fast setup guide
- **DEPENDENCIES.md** - Storage backend details
- **CLAUDE_ONBOARDING_GUIDE.md** - Interactive onboarding
- **docs/** - Complete documentation

---

## Support & Resources

**Getting Help:**
- Attach repo to Claude and ask questions
- Check documentation in docs/
- See troubleshooting in DEPENDENCIES.md

**Learning:**
- Follow onboarding guide (10-15 mins)
- Try skill-creator examples
- Read Anthropic's official patterns

---

## Next Steps

1. **New users:** Say "hi" with repo attached for onboarding
2. **Experienced:** Copy user-data-templates, configure storage
3. **Developers:** Read CONTRIBUTING.md, explore examples

---

**Ready to build?** Attach this repo to Claude and say "help me get started" 🚀

---

*SDK Template v1.1.0 | MIT License*
