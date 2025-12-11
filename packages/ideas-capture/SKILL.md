---
name: ideas-capture
description: Capture and develop fleeting ideas via Apple Notes inbox. AI expands rough concepts into detailed plans, evaluates potential with scoring (feasibility, impact, effort), and organizes by type (Patent, Startup, Business, Project). Triggers - "process ideas", "show ideas", "expand idea", "evaluate idea", "new idea", "brainstorm", "idea inbox", "show patents", "show startups", "link ideas", "search ideas".
---

# Ideas Capture

## Overview

Capture, organize, and develop ideas and thoughts from Apple Notes inbox.

## Storage

Path: `~/exocortex-data/ideas-capture/`

```
ideas-capture/
├── ideas.yaml        # Database
├── expanded/         # Full documents
└── config.yaml       # Preferences
```

## Commands

| Command | Action |
|---------|--------|
| `process ideas` | Process Apple Notes inbox |
| `show ideas` | List all by type |
| `show [type] ideas` | Filter by type |
| `expand: [idea]` | Generate expansion |
| `evaluate: [idea]` | Score potential |
| `link ideas: [A] + [B]` | Connect related |
| `search ideas: [query]` | Find by keyword |

## Idea Types

| Type | Use For |
|------|---------|
| Patent | Inventions, technical innovations |
| Startup | Business ventures, products |
| Business | Process improvements, revenue |
| Project | Side projects, personal tools |
| Other | Misc thoughts |

## Scoring Dimensions

| Dimension | Weight |
|-----------|--------|
| Feasibility | 20% |
| Impact | 25% |
| Effort (low=good) | 15% |
| Uniqueness | 15% |
| Timing | 15% |
| Personal Fit | 10% |

**Tiers**: Hot (≥7), Warm (5-7), Cold (<5)

## Workflow

1. Read "Ideas Inbox" from Apple Notes
2. Parse type prefix (or auto-classify)
3. AI-expand based on type
4. Score on 6 dimensions
5. Save to `ideas.yaml` + `expanded/{slug}.md`
6. Mark processed in Apple Notes

For detailed implementation, see `references/workflow.md`.

## Quick Start

1. Open "Ideas Inbox" Apple Note
2. Add ideas (optional type prefix): `[Startup] App idea...`
3. Say: `"process ideas"`
4. View: `"show ideas"` or `"show startup ideas"`
