---
name: recipe-manager
description: Family recipe collection manager. Extracts recipes from URLs (Instagram, YouTube, websites), images, and Apple Notes. Tracks family preferences, cooking status (To try → Perfected), and syncs with Notion. Supports Hebrew and English. Triggers - "add recipe", "save recipe", "extract recipe", "show recipes", "process recipe inbox", "import from Apple Notes", "sync to Notion", "mark recipe tried", "family recipes", "ninja recipes", "oven recipes".
---

# Recipe Manager

## Overview

Manage recipes, plan meals, and generate shopping lists.

## Storage

Path: `~/exocortex-data/recipe-manager/`

```
recipe-manager/
├── config/settings.yaml   # Preferences
├── recipes/               # YAML files by status
│   ├── to-try/
│   ├── tried/
│   └── perfected/
└── exports/
```

## Commands

| Command | Action |
|---------|--------|
| `add recipe from [URL]` | Extract from URL |
| `extract recipe from image` | Parse attached image |
| `process recipe inbox` | Import from Apple Notes |
| `show recipes` | List all |
| `show [type] recipes` | Filter by type |
| `mark [recipe] tried` | Update status |
| `rate [recipe] [1-5]` | Add rating |
| `sync to Notion` | Push to Notion |

## Recipe Types

Oven, Ninja, School Breakfast, Stovetop, Grill, No Cook, Instant Pot

## Status Flow

`To try` → `Try next` → `Tried` → `Perfected`

## Source Support

| Source | Method |
|--------|--------|
| Instagram | Bright Data / Firecrawl |
| YouTube | Video description |
| Websites | Firecrawl scrape |
| Images | Claude vision |
| Apple Notes | Direct parse |

## Notion Sync

- Database ID: `2461eaaa56f680c4a8d7f1df05616964`
- Manual sync via commands
- Bi-directional support

## Modules

| Module | Purpose |
|--------|---------|
| `modules/recipe-extraction.md` | URL/image parsing |
| `modules/notion-sync.md` | Notion operations |
| `modules/apple-notes-import.md` | Notes import |

For data schema and extraction workflow, see `references/workflow.md`.

## Quick Start

1. Add URLs to "Recipe Inbox" Apple Note
2. Say: `"process recipe inbox"`
3. Or: `"add recipe from [URL]"`
4. View: `"show recipes"` or `"show ninja recipes"`
