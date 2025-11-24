# Quick Reference Guide

**Last Updated:** November 19, 2025  
**Purpose:** Single-page reference for common paths, commands, and workflows  
**Token Usage:** ~400 tokens

---

## 📂 Most Common File Paths

### For End Users
```
docs/guides/USER_GUIDE.md              # Complete user guide (setup, usage, MCP, troubleshooting)
```

### For Developers
```
docs/guides/DEVELOPER_GUIDE.md         # Complete developer guide (architecture, releases, testing)
docs/project/STATUS.md                 # Current project status
```

### For Product/Project Management
```
docs/project/FEATURES.md               # Core capabilities
docs/project/ROADMAP.md                # Development plan
docs/project/STRATEGY.md               # Business strategy
docs/project/MARKETING.md              # Marketing & distribution
docs/project/STATUS.md                 # Current health
```

### Configuration & Core Files
```
skill-package/config/paths.py          # Path configuration
skill-package/SKILL.md                 # Main skill file
version.yaml                           # Version info
```

---

## 🚀 Common Commands

### Release Management
```bash
# Create release
./host_scripts/release.sh

# Dry run
./host_scripts/release.sh --dry-run
```

### Development
```bash
# Run tests
pytest

# Validate structure
python host_scripts/validate_docs_structure.py
```

---

## 🗺️ Navigation Shortcuts

### I want to...

**Get started as a user:**
→ Read `docs/guides/USER_GUIDE.md`

**Start developing:**
→ Read `docs/guides/DEVELOPER_GUIDE.md`

**See current status:**
→ Read `docs/project/STATUS.md`

**Understand features:**
→ Read `docs/project/FEATURES.md`

**See the roadmap:**
→ Read `docs/project/ROADMAP.md`

**Contribute:**
→ Read `docs/meta/CONTRIBUTING.md`

---

## 📊 Token Usage Quick Reference

| Load This | Tokens | Use When |
|-----------|--------|----------|
| DOCS_INDEX.yaml | ~300 | Need navigation |
| quick-reference.md | ~400 | Common paths |
| USER_GUIDE.md | ~8K | User documentation |
| DEVELOPER_GUIDE.md | ~9K | Developer docs |
| One project file | ~1-2K | Specific info |
| All project files | ~6K | Full product context |
| Full documentation | ~28K | Comprehensive review |

---

## 🏗️ Directory Structure Overview

```
docs/
├── README.md
├── DOCS_INDEX.yaml
├── quick-reference.md
├── guides/
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
├── project/
│   ├── FEATURES.md
│   ├── ROADMAP.md
│   ├── STRATEGY.md
│   ├── MARKETING.md
│   ├── STATUS.md
│   └── bugs/
└── meta/
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    ├── CODE_OF_CONDUCT.md
    └── CREDITS.md
```

---

## 💡 Pro Tips

1. **Token Efficiency**: Start with `DOCS_INDEX.yaml` or this quick reference
2. **User questions?**: Load `USER_GUIDE.md` - it's comprehensive
3. **Developer work?**: Load `DEVELOPER_GUIDE.md` - covers everything
4. **Project info?**: Project files are ~1-2K each, safe to load multiple
5. **Version check**: `cat version.yaml`
6. **Lost?**: Load `docs/DOCS_INDEX.yaml` (~300 tokens)

---

## 🆘 Emergency Quick Access

### Something's broken
→ `docs/guides/USER_GUIDE.md` (Troubleshooting section)

### Need to release NOW
→ `docs/guides/DEVELOPER_GUIDE.md` (Release Process section)

### Completely lost
→ `docs/README.md` or `docs/DOCS_INDEX.yaml`

### Need project context fast
→ `docs/project/STATUS.md`

---

**Pro Tip:** Bookmark this file - it's designed to be your go-to reference! 🔖

**Structure Version:** 4.0 (Ultra-consolidated)  
**Total Files:** 13 markdown files  
**Total Size:** ~180KB
