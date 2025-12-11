---
name: interview-prep
description: Interview preparation system with STAR story management, company deep-dives, and salary negotiation. Build and practice behavioral stories, research companies thoroughly, and prepare for offer negotiations. Triggers - "prepare for interview", "practice STAR", "show my stories", "deep dive company", "prep negotiation", "compare offers", "interview prep", "behavioral questions".
---

# Interview Prep

## Overview

Prepare for interviews with STAR stories, company research, and negotiation planning.

## Storage

Path: `~/exocortex-data/career/` (shared with job-analyzer)

```
career/
├── interview-prep/
│   ├── star-stories.yaml    # STAR story library
│   ├── practice-log.yaml    # Practice sessions
│   └── negotiations/        # Per-company negotiation files
├── contacts.yaml            # Shared with job-analyzer
└── config.yaml              # Shared config
```

## Commands

### STAR Stories
| Command | Action |
|---------|--------|
| `Show my stories` | List STAR library |
| `Add story: [title]` | Create new STAR |
| `Practice STAR` | Random story prompt |
| `Match stories for [company]` | Relevant stories |

### Company Research
| Command | Action |
|---------|--------|
| `Deep dive: [company]` | Full research report |
| `Quick brief: [company]` | 5-minute overview |
| `Who will I meet at [company]` | Interview panel research |

### Negotiation
| Command | Action |
|---------|--------|
| `Prep negotiation for [company]` | Full prep package |
| `Compare offers` | Side-by-side matrix |
| `Draft counter for [company]` | Counter-offer script |

## STAR Framework

| Element | Question |
|---------|----------|
| **S**ituation | What was the context? |
| **T**ask | What was your responsibility? |
| **A**ction | What did you do? |
| **R**esult | What was the outcome? (quantify!) |

### Story Categories
- Leadership & influence
- Technical problem-solving
- Conflict resolution
- Failure & learning
- Cross-functional collaboration
- Delivering under pressure

## Modules

| Module | Purpose | Load When |
|--------|---------|-----------|
| `star-framework` | Story structure & practice | STAR commands |
| `job-prep-planner` | Interview prep checklist | Prep commands |
| `company-deep-dive` | Research automation | Research commands |
| `salary-negotiation` | Offer negotiation | Negotiation commands |

## Workflow

### Pre-Interview (2-3 days before)
1. `Deep dive: [company]` - Research
2. `Match stories for [company]` - Select relevant STAR stories
3. `Practice STAR` - Run through key stories

### Post-Interview
1. Log interview notes
2. `Prep negotiation for [company]` - If expecting offer

### Offer Stage
1. `Compare offers` - If multiple
2. `Draft counter for [company]` - Prepare response

## Integration with Job Analyzer

Reads from shared storage:
- Job analysis for role requirements
- Company research from initial analysis
- Recruiter contacts for interview panel

```
job-analyzer: "Analyze: [URL]" → saves analysis
interview-prep: "Prepare for [company]" → reads analysis
```
