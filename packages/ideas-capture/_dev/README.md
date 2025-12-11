# 💡 Ideas Capture

Capture, organize, and develop ideas and thoughts from Apple Notes inbox.

## Quick Start

1. Open **💡 Ideas Inbox** in Apple Notes
2. Add ideas (optional type prefix): `[Startup] App idea...`
3. Tell Claude: `"process ideas"`
4. View: `"show ideas"` or `"show startup ideas"`

## Commands

| Command | Action |
|---------|--------|
| `process ideas` | Process Apple Notes inbox |
| `show ideas` | List all by type |
| `show [type] ideas` | Filter by type (patent/startup/business/project) |
| `expand: [idea]` | Generate expansion |
| `evaluate: [idea]` | Score potential |
| `link ideas: [A] + [B]` | Connect related |
| `search ideas: [query]` | Find by keyword |

## Idea Types

- **Patent**: Inventions, technical innovations
- **Startup**: Business ventures, products
- **Business**: Process improvements, revenue
- **Project**: Side projects, personal tools
- **Other**: Misc thoughts

## Features

- **Apple Notes Inbox**: Quick mobile-friendly capture
- **AI Expansion**: Turn 1-line ideas into detailed concepts
- **Potential Scoring**: Rate feasibility, impact, effort, uniqueness, timing
- **Type Classification**: Auto-categorize or manual tagging
- **Idea Linking**: Connect related ideas across types
- **Tier System**: Hot (≥7), Warm (5-7), Cold (<5)

## Scoring Dimensions

- **Feasibility** (20%)
- **Impact** (25%)
- **Effort** (15%) - low=good
- **Uniqueness** (15%)
- **Timing** (15%)
- **Personal Fit** (10%)

## Storage

User data: `~/exocortex-data/ideas-capture/`

```
ideas-capture/
├── ideas.yaml        # Database
├── expanded/         # Full documents
└── config.yaml       # Preferences
```

## Version

See `version.yaml`

---

Part of [Claude Skills Ecosystem](../../README.md)
