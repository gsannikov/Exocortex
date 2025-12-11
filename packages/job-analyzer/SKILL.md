---
name: job-analyzer
description: Israeli tech job analysis and tracking system. Analyzes opportunities with 6-component scoring (Match, Income, Growth, LowPrep, Stress, Location), tracks applications via LinkedIn, manages recruiter contacts, and sends follow-up reminders. Outputs to Excel tracker. Triggers - "analyze job", "add to backlog", "process inbox", "show backlog", "track application", "show contacts", "show reminders", "follow up".
---

# Job Analyzer

## Overview

Find, analyze, and track job opportunities in the Israeli tech market.

## Storage

Path: `~/exocortex-data/career/`

```
career/
├── analyses/           # Job analysis YAML files
├── jobs.xlsx           # Master tracker
├── contacts.yaml       # Recruiter/network contacts
├── reminders.yaml      # Follow-up reminders
└── config.yaml         # Shared config
```

## Commands

### Job Analysis
| Command | Action |
|---------|--------|
| `Analyze: [URL]` | Full 6-point scoring |
| `Add to backlog: [URL]` | Quick save |
| `Process inbox` | Batch from Apple Notes |
| `Show backlog` | List pending |

### Application Tracking
| Command | Action |
|---------|--------|
| `Track LinkedIn: [URL]` | Track application |
| `Update status [job]: [status]` | Change status |
| `Show applications` | List tracked |

### Contacts
| Command | Action |
|---------|--------|
| `Add contact: [name] at [company]` | New contact |
| `Show contacts` | List all |
| `Log interaction: [contact]` | Add note |

### Follow-ups
| Command | Action |
|---------|--------|
| `Show reminders` | Pending reminders |
| `Snooze [reminder] [days]` | Delay |
| `Complete [reminder]` | Mark done |

## Scoring System

| Component | Weight | Description |
|-----------|--------|-------------|
| Match | 35 | Skills alignment |
| Income | 25 | Salary vs requirements |
| Growth | 20 | Career advancement |
| LowPrep | 15 | Interview prep effort |
| Stress | 10 | Work-life balance |
| Location | 5 | Commute + remote |

**Tiers**: First (≥70), Second (≥50), Third (<50)



## Modules

| Module | Purpose | Load When |
|--------|---------|-----------|
| `scoring-formulas` | Score calculations | Every analysis |
| `skills-matching` | CV alignment | Every analysis |
| `job-backlog-manager` | Queue management | Backlog commands |
| `company-research` | Auto research | New company |
| `database-operations-hybrid` | Excel sync | Save/export |
| `linkedin-tracking` | Application tracking | Track commands |
| `recruiter-contacts` | Contact management | Contact commands |
| `follow-up-reminders` | Reminder system | Reminder commands |

## Workflow

1. **Analyze**: Parse job → Research company → Match skills → Score → Save
2. **Track**: After analysis, optionally track LinkedIn application
3. **Follow-up**: Auto-reminders for stale applications, post-interview

For detailed workflows, see `references/analysis-workflow.md`.

## Handoff to Interview Prep

After scheduling interview:
```
"Prepare for [company] interview" → uses interview-prep skill
```

Interview-prep reads from shared `career/` storage for context.
