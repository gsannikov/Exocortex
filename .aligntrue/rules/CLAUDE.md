---
title: Claude
content_hash: updated-2025-12-11
---
# Exocortex Skills Ecosystem

Global instructions for Claude when working with this skills monorepo.

## 🎯 Quick Reference

### Available Skills (10)

| Skill | Command | Apple Note |
|-------|---------|------------|
| 💼 job-analyzer | `analyze: [URL]` | 📋 Job Links Inbox |
| 🎯 interview-prep | `prepare for [company]` | N/A (uses shared career data) |
| 📚 reading-list | `process reading list` | 📚 Reading List Inbox |
| 💡 ideas-capture | `process ideas` | 💡 Ideas Inbox |
| 🎙️ voice-memos | `process voice memos` | 🎙️ Voice Memos Inbox |
| 🔍 local-rag | `search documents` | N/A (local files) |
| 📱 social-media-post | `create [platform] post` | N/A (generates posts) |
| 🍳 recipe-manager | `process recipe inbox` | 🍳 Recipe Inbox |
| 🔧 setup-manager | `check setup` | N/A (system config) |
| 🏭 next-skill | `create skill`, `search skills` | N/A (skill factory) |

### Key Paths

```
~/Projects/exocortex/              # This repo (code)
~/exocortex-data/                  # User data (gitignored)
```

**⚠️ Important**: User data path is configured in `shared/config/paths.py`. 
This is the **SINGLE SOURCE OF TRUTH** for all user data paths.

## 📁 Repo Structure

```
exocortex/
├── packages/                      # All skills (10)
│   ├── job-analyzer/              # Job scoring, tracking, contacts
│   ├── interview-prep/            # STAR stories, negotiation
│   ├── reading-list/
│   ├── ideas-capture/
│   ├── voice-memos/
│   ├── local-rag/
│   ├── social-media-post/
│   ├── recipe-manager/
│   ├── setup-manager/
│   └── next-skill/                # Skill factory
├── shared/
│   ├── scripts/                   # Release, generator, dependency tracker
│   ├── config/                    # paths.py (single source of truth)
│   ├── templates/                 # Patterns, templates
│   └── workflows/                 # Troubleshooting guides
├── .claude/
│   └── commands/                  # Slash commands (/refactor, /deps, /release)
├── .github/workflows/             # CI/CD
├── dependencies.yaml              # File dependency graph
├── CLAUDE.md                      # This file
└── PROJECT.md                     # Roadmap & decisions
```

## 🔧 Global Rules

1. **User Data**: Configured in `shared/config/paths.py` (default: `~/exocortex-data/{skill}/`)
2. **Storage Format**: YAML for structured data, Markdown for content
3. **Skill Structure**: SKILL.md <100 lines, details in `references/`
4. **Deduplication**: Always dedupe before adding items
5. **Stats Tracking**: Update stats after operations
6. **Apple Notes**: Keep processed section minimal (stats only)

## 📋 Skill Loading

Load skill-specific SKILL.md only when needed:

```python
# Example paths
job_analyzer = "packages/job-analyzer/SKILL.md"
interview_prep = "packages/interview-prep/SKILL.md"
reading_skill = "packages/reading-list/SKILL.md"
local_rag_skill = "packages/local-rag/SKILL.md"
```

### Skill Structure Best Practice

All skills follow this structure:
```
skill-name/
├── SKILL.md              # <100 lines, orchestrator
├── references/           # Detailed workflows
│   └── workflow.md
├── modules/              # Feature modules (on-demand)
├── scripts/              # Python utilities
└── config/               # Configuration
```

## 🔄 Career Workflow (Shared Storage)

job-analyzer and interview-prep share `~/exocortex-data/career/`:

```
User: "Analyze: [URL]"           → job-analyzer
User: "Prepare for [company]"   → interview-prep (reads shared data)
```

## 🔄 Common Workflows

### Processing Inbox (Any Skill)

1. Read Apple Note inbox
2. Parse items from pending section
3. Dedupe against existing database
4. Process each new item
5. Save to YAML database
6. Update Apple Note (processed count only)

### Release Process

```bash
cd ~/Projects/exocortex
python shared/scripts/release.py job-analyzer --patch
```

Or use `/release` command.

### Create New Skill

```bash
python shared/scripts/skill_generator.py --name "expense-tracker" --patterns inbox,database
```

## ⚠️ Important Notes

- **Never skip failing tests** - tests must pass before releasing
- **Never commit user data** - it's in a separate gitignored folder
- **Keep SKILL.md under 100 lines** - use references/ for details
- **URL normalization** - strip trailing slashes, decode HTML entities
- **Apple Notes timeout** - keep note updates small, use stats summary

## 🔄 Dependency Tracking

This repo uses a dependency graph to track relationships between files.

### Quick Commands

| Command | Description |
|---------|-------------|
| `/refactor` | Full dependency-aware refactor workflow |
| `/deps` | Quick dependency status check |
| `/release` | Trigger release workflow |

### Key Files

- `dependencies.yaml` - The dependency manifest
- `shared/scripts/dependency_tracker.py` - The tracker script

## 🔗 Related Files

- [PROJECT.md](PROJECT.md) - Architecture decisions, roadmap
- [USER_GUIDE.md](USER_GUIDE.md) - User documentation
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Developer documentation

## 🔄 Cross-Platform Compatibility (AlignTrue)

This repository uses AlignTrue to maintain platform-agnostic AI instructions.

**Source of Truth**: `.aligntrue/rules/CLAUDE.md`

**⚠️ Important**: 
- DO NOT edit `CLAUDE.md` directly - changes will be overwritten
- Edit `.aligntrue/rules/CLAUDE.md` instead
- Run `aligntrue sync` to propagate changes
