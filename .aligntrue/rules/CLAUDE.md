---
title: Claude
content_hash: cb0bc89011bff2524d7c22954273a792e60647ea322351b5830d156a0c481d63
---
# Claude Skills Ecosystem

Global instructions for Claude when working with this skills monorepo.

## 🎯 Quick Reference

### Available Skills

| Skill | Command | Apple Note |
|-------|---------|------------|
| 📋 career-consultant | `process inbox` | 📋 Job Links Inbox |
| 📚 reading-list | `process reading list` | 📚 Reading List Inbox |
| 💡 ideas-capture | `process ideas` | 💡 Ideas Inbox |
| 🎙️ voice-memos | `process voice memos` | 🎙️ Voice Memos Inbox |
| 🔍 local-rag | `search documents` | N/A (local files) |
| 📱 social-media-post | `create [platform] post` | N/A (generates posts) |

### Key Paths

```
~/Projects/claude-skills/          # This repo (code) - can be anywhere
~/Documents/claude-skills-data/     # User data (gitignored) - configured in shared/config/paths.py
```

**⚠️ Important**: User data path is configured in `shared/config/paths.py`. 
This is the **SINGLE SOURCE OF TRUTH** for all user data paths.
To change your user data location, edit `USER_DATA_BASE` in that file.

## 📁 Repo Structure

```
claude-skills/
├── packages/                      # All skills
│   ├── career-consultant/
│   ├── reading-list/
│   ├── ideas-capture/
│   ├── voice-memos/
│   ├── local-rag/
│   └── social-media-post/
├── shared/
│   ├── scripts/                   # Release, generator, dependency tracker
│   ├── templates/                 # Patterns, templates
│   ├── marketing/                 # Blog posts, images
│   └── workflows/                 # Troubleshooting guides
├── .claude/
│   └── commands/                  # Slash commands (/refactor, /deps)
├── .github/workflows/             # CI/CD
├── dependencies.yaml              # File dependency graph
├── CLAUDE.md                      # This file
└── PROJECT.md                     # Roadmap & decisions
```

## 🔧 Global Rules

1. **User Data**: Configured in `shared/config/paths.py` (default: `~/Documents/claude-skills-data/{skill}/`)
2. **Storage Format**: YAML for structured data, Markdown for content
3. **Deduplication**: Always dedupe before adding items
4. **Stats Tracking**: Update stats after operations
5. **Apple Notes**: Keep processed section minimal (stats only)
6. **Path Configuration**: All paths use centralized config - never hardcode user data paths

## 📋 Skill Loading

Load skill-specific SKILL.md only when needed:

```python
# Example paths
career_skill = "packages/career-consultant/SKILL.md"
reading_skill = "packages/reading-list/SKILL.md"
local_rag_skill = "packages/local-rag/SKILL.md"
social_media_skill = "packages/social-media-post/SKILL.md"
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
cd ~/Projects/claude-skills  # or wherever the repo is located
python shared/scripts/release.py career-consultant --patch
```

### Create New Skill

```bash
python shared/scripts/skill_generator.py --name "expense-tracker" --patterns inbox,database
```

## ⚠️ Important Notes

- **Never skip failing tests** - tests must pass before releasing or merging
- **Never commit user data** - it's in a separate gitignored folder
- **URL normalization** - strip trailing slashes, decode HTML entities
- **Apple Notes timeout** - keep note updates small, use stats summary
- **Config precedence**: global → skill-specific → runtime overrides

## 🔄 Dependency Tracking

This repo uses a dependency graph to track relationships between files. When a source file changes, all dependent files need to be updated.

### Dependency Chain Example

```
Skill Code (SKILL.md)
    ↓ triggers update to
Skill README
    ↓ triggers update to
USER_GUIDE.md
    ↓ triggers update to
Marketing Articles
```

### Quick Commands

| Command | Description |
|---------|-------------|
| `/refactor` | Full dependency-aware refactor workflow |
| `/deps` | Quick dependency status check |
| `python shared/scripts/dependency_tracker.py status` | Show all file statuses |
| `python shared/scripts/dependency_tracker.py graph` | Show dependency tree |
| `python shared/scripts/dependency_tracker.py affected <file>` | What depends on this file? |

### When to Use

- **After modifying skill code**: Run `/refactor` to update README, USER_GUIDE, etc.
- **Before releasing**: Check `/deps` to ensure all docs are in sync
- **When asked to "refactor"**: Use `/refactor` to traverse the dependency tree

### Key Files

- `dependencies.yaml` - The dependency manifest (defines all relationships)
- `shared/scripts/dependency_tracker.py` - The tracker script

### File Types

| Type | Description | Example |
|------|-------------|---------|
| `source` | Primary files, no dependencies | `SKILL.md`, `PROJECT.md` |
| `derived` | Generated from sources | Skill READMEs |
| `documentation` | User-facing docs | `USER_GUIDE.md` |
| `marketing` | Blog/promotional content | `article-*.md` |

## 🔗 Related Files

- [PROJECT.md](PROJECT.md) - Architecture decisions, roadmap
- [dependencies.yaml](dependencies.yaml) - File dependency graph
- [shared/templates/learned-patterns.yaml](shared/templates/learned-patterns.yaml) - Best practices

## 🔄 Cross-Platform Compatibility (AlignTrue)

This repository uses [AlignTrue](https://github.com/aligntrue/aligntrue) to maintain platform-agnostic AI instructions.

**How It Works:**
- **Source of Truth**: `.aligntrue/rules/CLAUDE.md` contains the canonical instructions
- **Auto-Generated Files**: Platform-specific instruction files are auto-generated:
  - `CLAUDE.md` → Claude Desktop
  - `AGENTS.md` → OpenAI Codex
  - `.cursorrules` → Cursor IDE
  - Works with Google Antigravity (you're using it now!)
- **Sync Command**: Run `aligntrue sync` after editing `.aligntrue/rules/CLAUDE.md`

**For SDK Developers & Contributors:**
Whether you use Claude, OpenAI Codex, Cursor, Google Antigravity, or other AI coding assistants, AlignTrue ensures you have the same context and capabilities. Clone the repo and use your preferred AI tool—the instructions are platform-agnostic.

**⚠️ Important**: 
- DO NOT edit `CLAUDE.md` directly - changes will be overwritten
- Edit `.aligntrue/rules/CLAUDE.md` instead
- Run `aligntrue sync` to propagate changes to all platforms
- All generated files are tracked in git for immediate availability
