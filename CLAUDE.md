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

### Key Paths

```
~/MyDrive/claude-skills/           # This repo (code)
~/MyDrive/claude-skills-data/      # User data (gitignored)
```

## 📁 Repo Structure

```
claude-skills/
├── packages/                      # All skills
│   ├── career-consultant/
│   ├── reading-list/
│   ├── ideas-capture/
│   ├── voice-memos/
│   └── local-rag/
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

1. **User Data**: Always in `~/MyDrive/claude-skills-data/{skill}/`
2. **Storage Format**: YAML for structured data, Markdown for content
3. **Deduplication**: Always dedupe before adding items
4. **Stats Tracking**: Update stats after operations
5. **Apple Notes**: Keep processed section minimal (stats only)

## 📋 Skill Loading

Load skill-specific SKILL.md only when needed:

```python
# Example paths
career_skill = "packages/career-consultant/SKILL.md"
reading_skill = "packages/reading-list/SKILL.md"
local_rag_skill = "packages/local-rag/SKILL.md"
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
cd ~/MyDrive/claude-skills
python shared/scripts/release.py career-consultant --patch
```

### Create New Skill

```bash
python shared/scripts/skill_generator.py --name "expense-tracker" --patterns inbox,database
```

## ⚠️ Important Notes

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
