# Job Analyzer

Find, analyze, and track job opportunities in the Israeli tech market.

## Features
- **Job Analysis**: 6-component scoring system (Match, Income, Growth, LowPrep, Stress, Location)
- **Application Tracking**: Track status via LinkedIn
- **Contact Management**: Keep track of recruiters and network contacts
- **Follow-ups**: Automated reminders for stale applications

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

### Contacts & Follow-ups
| Command | Action |
|---------|--------|
| `Add contact: [name] at [company]` | New contact |
| `Show contacts` | List all |
| `Show reminders` | Pending reminders |

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

## Quick Start
1. `Analyze: [URL]` - Analyze a job posting
2. `Track LinkedIn: [URL]` - Track your application
