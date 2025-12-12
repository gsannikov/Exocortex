# User Guide

This guide covers how to use each skill in the Exocortex ecosystem with detailed command examples.

## Table of Contents

- [Skills Overview](#skills-overview)
- [Job Analyzer](#-job-analyzer)
- [Interview Prep](#-interview-prep)
- [Reading List](#-reading-list)
- [Ideas Capture](#-ideas-capture)
- [Voice Memos](#-voice-memos)
- [Local RAG](#-local-rag)
- [Social Media Post](#-social-media-post)
- [Recipe Manager](#-recipe-manager)
- [Apple Notes Setup](#apple-notes-setup)
- [Data Storage](#data-storage)

---

## Skills Overview

All skills follow the same pattern:
1. **Capture** - Add items to Apple Notes or directly
2. **Process** - Claude processes and enriches data
3. **Store** - Data saved to YAML database
4. **Query** - Search and retrieve information

**User Data Location**: `~/exocortex-data/{skill}/`

---

## 💼 Job Analyzer

**Purpose**: Find, analyze, and track job opportunities in the Israeli tech market with 6-component scoring.

### Command Categories

| Category | Example Commands |
|----------|------------------|
| Analysis | `analyze: [URL]`, `analyze job [id]` |
| Backlog | `add to backlog`, `process inbox`, `show backlog` |
| Tracking | `track LinkedIn`, `update status`, `show applications` |
| Contacts | `add contact`, `show contacts`, `log interaction` |
| Follow-ups | `show reminders`, `snooze`, `complete` |

---

### Job Analysis

#### Full Analysis
```
Analyze: https://linkedin.com/jobs/view/12345
```
Complete job analysis with 6-component scoring.

#### Analyze from Backlog
```
Analyze job nvidia-senior-tpm-backlog-20251029
```

### Backlog Management

#### Add Single Job
```
Add to backlog: https://linkedin.com/jobs/view/12345
```

#### Batch Add Jobs
```
Add jobs: https://url1.com, https://url2.com, https://url3.com
```

#### Process Inbox
```
process inbox
```
Syncs from Apple Notes and processes jobs.

#### View Backlog
```
show backlog
```

### LinkedIn Application Tracking

#### Track Application
```
Track LinkedIn: https://linkedin.com/jobs/view/12345
```

#### Update Status
```
Update status nvidia-job: interviewed
```
Statuses: applied → viewed → in-review → interview → offer/rejected

#### View Applications
```
Show applications
```
```
Show pending applications
```

### Recruiter & Contact Management

#### Add Contact
```
Add contact: Sarah Cohen at NVIDIA
```

#### Log Interaction
```
Log interaction: Sarah Cohen - discussed EM role via email
```

#### View Contacts
```
Show contacts
```
```
Show contacts at NVIDIA
```

### Follow-up Reminders

#### View Reminders
```
Show reminders
```
```
Show reminders today
```

#### Manage Reminders
```
Snooze nvidia-followup 3 days
```
```
Complete nvidia-followup
```

#### Create Manual Reminder
```
Create reminder: Follow up with AWS recruiter in 5 days
```

### Scoring Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Match | 35% | Skills alignment + role fit |
| Income | 25% | Salary vs. requirements |
| Growth | 20% | Career advancement opportunities |
| LowPrep | 15% | Interview readiness (less prep = higher) |
| Stress | 10% | Work-life balance, on-call, complexity |
| Location | 5% | Commute + hybrid/remote policy |

**Priority Thresholds:**
- First Priority: 70+
- Second Priority: 50-69
- Third Priority: <50

---

## 🎯 Interview Prep

**Purpose**: Prepare for interviews with STAR stories, company research, and salary negotiation.

### Command Categories

| Category | Example Commands |
|----------|------------------|
| STAR | `show my stories`, `add story`, `practice STAR` |
| Research | `deep dive`, `quick brief`, `who will I meet` |
| Negotiation | `prep negotiation`, `compare offers`, `draft counter` |

---

### STAR Story Management

#### View Stories
```
Show my stories
```

#### Add New Story
```
Add story: Led migration of 50 microservices
```

#### Practice
```
Practice STAR
```
Options: Flash cards, Timed practice, Mock interview

#### Match to Job
```
Match stories for NVIDIA
```

### Company Research

#### Deep Dive
```
Deep dive: NVIDIA
```
Full research report with tech stack, culture, leadership, talking points.

#### Quick Brief
```
Quick brief: AWS
```
5-minute overview before interview.

#### Interview Panel
```
Who will I meet at Microsoft
```

### Salary Negotiation

#### Prepare
```
Prep negotiation for NVIDIA
```
Research-backed strategy with market data.

#### Compare Offers
```
Compare offers
```
Side-by-side matrix of all active offers.

#### Counter-Offer
```
Draft counter for NVIDIA
```
Script for negotiation conversation.

### STAR Framework

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

---

## 📚 Reading List

**Purpose**: Manage reading list, track progress, and organize books/articles. Auto-scrapes URLs, summarizes content, and tracks status.

### Commands

| Command | Action |
|---------|--------|
| `process reading list` | Process URLs from inbox |
| `show unread` | List unread items |
| `show reading list` | Full list with status |
| `show [category]` | Filter by category |
| `summarize [topic]` | Get summaries |
| `mark read: [title]` | Update status |
| `search: [query]` | Find by keyword |

### Categories

- **Tech**: Programming, tools, engineering
- **AI**: AI/ML, LLMs, data science
- **Business**: Strategy, management, startups
- **Career**: Job search, skills, growth
- **Finance**: Investing, markets
- **Science**: Research, discoveries

### Example Session

```
User: process reading list

Claude: Processing Reading List Inbox...
        Found 5 new URLs
        Processed 5 articles (3 AI, 1 Career, 1 Tech)

User: show unread

Claude: Reading List - 12 Unread

        AI (5)
        - Building LLM Applications (12 min)
        - RAG Best Practices (8 min)

        Career (3)
        - Tech Interview Guide 2024 (15 min)
```

---

## 💡 Ideas Capture

**Purpose**: Capture, organize, and develop ideas and thoughts from Apple Notes inbox.

### Commands

| Command | Action |
|---------|--------|
| `process ideas` | Process Apple Notes inbox |
| `show ideas` | List all by type |
| `show [type] ideas` | Filter by type (patent/startup/business/project) |
| `expand: [idea]` | Generate expansion |
| `evaluate: [idea]` | Score potential |
| `link ideas: [A] + [B]` | Connect related |
| `search ideas: [query]` | Find by keyword |

### Idea Types

- **Patent**: Inventions, technical innovations
- **Startup**: Business ventures, products
- **Business**: Process improvements, revenue
- **Project**: Side projects, personal tools
- **Other**: Misc thoughts

### Scoring Dimensions

- **Feasibility** (20%)
- **Impact** (25%)
- **Effort** (15%) - low=good
- **Uniqueness** (15%)
- **Timing** (15%)
- **Personal Fit** (10%)

**Tiers**: Hot (≥7), Warm (5-7), Cold (<5)

---

## 🎙️ Voice Memos

**Purpose**: Process, transcribe, and analyze voice memos and audio notes.

### Commands

| Command | Action |
|---------|--------|
| `process voice memos` | Process inbox |
| `transcribe [file]` | Transcribe uploaded file |
| `analyze memo` | Analyze last transcript |
| `show pending memos` | List unprocessed |
| `show transcripts` | List all transcripts |
| `search memos: [query]` | Find by keyword |

### Supported Formats
m4a, mp3, wav, aac, opus, flac

### Analysis Output
- Summary (50-300 words)
- Action Items with priorities
- Key Points (up to 7)
- Entities (People, dates, locations)
- Auto-categorization (Meeting, Journal, etc.)

---

## 🔍 Local RAG

**Purpose**: Index local folders and query them using semantic search.

### Commands

| Command | Action |
|---------|--------|
| `update rag from [path]` | Index folder |
| `query rag [question]` | Search documents |

### Supported Files
- Documents: PDF, DOCX, PPTX, XLSX
- Text: MD, TXT, JSON, YAML
- Code: PY, JS, TS, HTML, CSS
- Images (OCR): PNG, JPEG, TIFF

### Example
```
User: update rag from ~/Documents/research

Claude: Found 47 PDF files, 12 markdown files
        Processed 59 files (1,247 chunks)

User: query rag neural network training

Claude: Found 5 relevant results:
        1. deep-learning-survey.pdf (0.89)
        2. optimization-methods.md (0.84)
```

---

## 📱 Social Media Post

**Purpose**: Generate platform-optimized social media posts.

### Commands

| Command | Action |
|---------|--------|
| `Create Threads post about [topic]` | Threads post |
| `Write X post for [topic]` | Twitter post |
| `Create LinkedIn post about [topic]` | LinkedIn post |

### Platforms

| Platform | Char Limit | Best For |
|----------|------------|----------|
| Threads | 500 | Conversational |
| X | 280 | Concise |
| LinkedIn | 3,000 | Professional |

---

## 🍳 Recipe Manager

**Purpose**: Manage recipes, plan meals, and generate shopping lists.

### Commands

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

### Recipe Types
Oven, Ninja, School Breakfast, Stovetop, Grill, No Cook, Instant Pot

### Status Flow
`To try` → `Try next` → `Tried` → `Perfected`

---

## 🏭 Next Skill (Skill Factory)

**Purpose**: AI-assisted skill creation with GitHub discovery, adaptation, or fresh scaffolding.

### Commands

| Command | Action |
|---------|--------|
| `create skill: [description]` | Full workflow: discover → adapt/create → scaffold |
| `search skills: [query]` | Discovery only - show existing solutions |
| `scaffold: [name]` | Skip discovery, create from scratch |
| `adapt: [github-url]` | Refactor specific repo to our architecture |
| `validate skill: [name]` | Check existing skill compliance |

### Workflow

1. **Discovery**: Search GitHub/MCP registries for similar implementations
2. **Decision**: Recommend adapting existing OR creating fresh
3. **Build**: Clone and adapt, or generate from templates
4. **Scaffold**: Generate compliant skill structure
5. **Integrate**: Add to release scripts and dependencies

---

## Apple Notes Setup

### Creating Inbox Notes

For each skill that uses Apple Notes, create a note:

```
{Skill Name} Inbox

ADD BELOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Your items here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCESSED
```

### Required Notes

| Skill | Note Name |
|-------|-----------|
| Job Analyzer | Job Links Inbox |
| Reading List | Reading List Inbox |
| Ideas Capture | Ideas Inbox |
| Voice Memos | Voice Memos Inbox |
| Recipe Manager | Recipe Inbox |

---

## Data Storage

### Location

All user data is stored separately from skill code:

```
~/exocortex-data/
├── career/                    # Shared by job-analyzer & interview-prep
│   ├── analyses/              # Job analysis YAML files
│   ├── jobs.xlsx              # Master tracker
│   ├── contacts.yaml          # Recruiter/network contacts
│   ├── reminders.yaml         # Follow-up reminders
│   ├── interview-prep/
│   │   ├── star-stories.yaml
│   │   └── negotiations/
│   └── config.yaml
├── reading-list/
│   ├── reading-list.yaml
│   └── summaries/
├── ideas-capture/
│   ├── ideas.yaml
│   └── expanded/
├── voice-memos/
│   ├── index.yaml
│   ├── transcripts/
│   └── analyzed/
├── local-rag/
│   └── vectordb/
├── recipe-manager/
│   └── recipes/
└── social-media-post/
    └── posts/
```

### Database Format

All databases use YAML format for human readability.

---

## Tips

### General
- **Process regularly**: Batch process weekly
- **Use mobile**: Apple Notes syncs for on-the-go capture
- **Search often**: Find patterns in your data

### Job Search Workflow
1. Use **Job Analyzer** to find and score opportunities
2. Track applications with LinkedIn tracking
3. When interview scheduled, switch to **Interview Prep**
4. Use STAR stories and company deep-dive for prep
5. Use salary negotiation module for offer stage

---

**Version**: 1.2.0
**Last Updated**: 2025-12-11
