# 💡 Ideas Capture

Capture fleeting ideas via Apple Notes, expand them with AI, score their potential, and organize by type.

## Quick Start

1. Open **💡 Ideas Inbox** in Apple Notes
2. Jot ideas (optionally with type prefix):
   - `🚀 App that tracks coffee consumption`
   - `🔬 Novel battery cooling mechanism`
   - `Just a random thought` (auto-classified)
3. Tell Claude: `"process ideas"`
4. View results: `"show ideas"`

## Commands

| Command | Action |
|---------|--------|
| `process ideas` | Process all from Apple Notes inbox |
| `show ideas` | List all ideas by type |
| `show [type] ideas` | Filter by type (patent/startup/business/project) |
| `expand: [idea]` | Generate detailed expansion |
| `evaluate: [idea]` | Score and analyze potential |
| `link ideas: [A] + [B]` | Connect related ideas |
| `search ideas: [query]` | Find by keyword |

## Idea Types

| Tag | Type | Use For |
|-----|------|---------|
| 🔬 | Patent | Novel inventions, technical innovations |
| 🚀 | Startup | Business ventures, product ideas |
| 💼 | Business | Process improvements, revenue ideas |
| 🛠️ | Project | Personal/side projects, tools |
| 💭 | Other | Misc ideas, thoughts |

## Features

- **Apple Notes Inbox**: Quick mobile-friendly capture
- **AI Expansion**: Turn 1-line ideas into detailed concepts
- **Potential Scoring**: Rate feasibility, impact, effort, uniqueness, timing
- **Type Classification**: Auto-categorize or manual tagging
- **Idea Linking**: Connect related ideas across types
- **Tier System**: Hot (≥7), Warm (5-7), Cold (<5)

## Scoring Dimensions

Ideas are rated 1-10 on:
- **Feasibility**: How realistic to implement
- **Impact**: Potential value/change
- **Effort**: Resources required (inverted)
- **Uniqueness**: How novel/differentiated
- **Timing**: Market/tech readiness
- **Personal Fit**: Alignment with your skills

## Storage

```
~/MyDrive/claude-skills-data/ideas-capture/
├── ideas.yaml            # Main database
├── expanded/             # Full idea documents
│   └── {slug}.md
└── config.yaml           # User preferences
```

## Version

See `version.yaml`

---

Part of [Claude Skills Ecosystem](../../README.md)
