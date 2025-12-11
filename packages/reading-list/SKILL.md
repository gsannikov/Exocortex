---
name: reading-list
description: Manage reading list via Apple Notes inbox. Auto-scrapes articles, generates AI summaries with key takeaways, categorizes by topic (Tech, AI, Business, Career, Finance), and tracks reading progress. Triggers - "process reading list", "show unread", "summarize articles", "reading inbox", "mark read", "search articles", "show [category] articles", "add article".
---

# Reading List

## Overview

Manage reading list, track progress, and organize books/articles. Auto-scrapes URLs, summarizes content, and tracks status.

## Storage

Path: `~/exocortex-data/reading-list/`

```
reading-list/
├── reading-list.yaml   # Database
├── summaries/          # Full content
└── config.yaml         # Preferences
```

## Commands

| Command | Action |
|---------|--------|
| `process reading list` | Process URLs from inbox |
| `show unread` | List unread items |
| `show reading list` | Full list with status |
| `show [category]` | Filter by category |
| `summarize [topic]` | Get summaries |
| `mark read: [title]` | Update status |
| `search: [query]` | Find by keyword |

## Categories

| Category | Content |
|----------|---------|
| Tech | Programming, tools, engineering |
| AI | AI/ML, LLMs, data science |
| Business | Strategy, management, startups |
| Career | Job search, skills, growth |
| Finance | Investing, markets |
| Science | Research, discoveries |
| Other | Everything else |

## Status Flow

`unread` → `reading` → `done` → `archived`

## Workflow

1. Read "Reading List Inbox" from Apple Notes
2. Extract URLs
3. Scrape via Firecrawl (fallback: web_fetch)
4. AI summarize (150 words) + categorize + extract takeaways
5. Save to `reading-list.yaml` + `summaries/{slug}.md`
6. Mark processed in Apple Notes

For detailed implementation, see `references/workflow.md`.

## Quick Start

1. Open "Reading List Inbox" Apple Note
2. Paste article URLs (one per line)
3. Say: `"process reading list"`
4. View: `"show unread"`
