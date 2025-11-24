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
│   └── voice-memos/
├── shared/
│   ├── scripts/                   # Release, generator
│   └── templates/                 # Patterns, templates
├── .github/workflows/             # CI/CD
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
career_skill = "/packages/career-consultant/skill-package/SKILL.md"
reading_skill = "/packages/reading-list/skill-package/SKILL.md"
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

## 🔗 Related Files

- [PROJECT.md](PROJECT.md) - Architecture decisions, roadmap
- [shared/templates/learned-patterns.yaml](shared/templates/learned-patterns.yaml) - Best practices
