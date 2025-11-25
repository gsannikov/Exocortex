# User Guide

This guide covers how to use each skill in the Claude Skills ecosystem with detailed command examples.

## Table of Contents

- [Quick Start](#quick-start)
- [Skills Overview](#skills-overview)
- [Career Consultant](#-career-consultant)
- [Reading List](#-reading-list)
- [Ideas Capture](#-ideas-capture)
- [Voice Memos](#-voice-memos)
- [Local RAG](#-local-rag)
- [Apple Notes Setup](#apple-notes-setup)
- [Data Storage](#data-storage)

---

## Quick Start

| Skill | Command | Apple Note |
|-------|---------|------------|
| Career Consultant | `process inbox` | Job Links Inbox |
| Reading List | `process reading list` | Reading List Inbox |
| Ideas Capture | `process ideas` | Ideas Inbox |
| Voice Memos | `process voice memos` | Voice Memos Inbox |
| Local RAG | `search documents` | N/A (local files) |

---

## Skills Overview

All skills follow the same pattern:
1. **Capture** - Add items to Apple Notes or directly
2. **Process** - Claude processes and enriches data
3. **Store** - Data saved to YAML database
4. **Query** - Search and retrieve information

**User Data Location**: `~/MyDrive/claude-skills-data/{skill}/`

---

## Career Consultant

**Purpose**: Analyze tech job opportunities with 6-component scoring system.

### Commands

#### Inbox Processing
```
process inbox
```
Processes job URLs from the Apple Notes inbox.

#### Add to Backlog (Quick Capture)
```
Add to backlog: https://linkedin.com/jobs/view/12345
```
Saves job for later analysis without full processing.

```
Save this job: https://company.com/careers/senior-engineer
```
Alternative phrasing for backlog capture.

```
Add high priority: https://linkedin.com/jobs/view/67890
```
Sets priority to high when saving.

#### Batch Add Jobs
```
Add jobs: https://url1.com, https://url2.com, https://url3.com
```
Save multiple jobs at once.

```
Batch add:
- https://linkedin.com/jobs/view/111
- https://linkedin.com/jobs/view/222
- https://linkedin.com/jobs/view/333
```
Multi-line batch add.

#### View Backlog
```
Show my backlog
```
Display all saved jobs with status.

```
View backlog
```
Alternative command.

```
List pending jobs
```
Show only unanalyzed jobs.

#### Full Analysis
```
Analyze: https://linkedin.com/jobs/view/12345
```
Complete job analysis with scoring.

```
Analyze job nvidia-senior-tpm-backlog-20251029
```
Analyze a specific job from backlog by ID.

```
Analyze top 5 jobs from backlog
```
Analyze highest priority jobs.

#### Statistics & Reports
```
Show me my job statistics
```
Display analysis statistics and trends.

```
Mark nvidia-tpm-123 as Applied
```
Update job status.

```
Rebuild Excel from all roles
```
Regenerate the Excel database.

### Scoring Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Match | 35 | Skills alignment + role fit |
| Income | 25 | Salary vs. requirements |
| Growth | 20 | Career advancement |
| LowPrep | 15 | Interview readiness |
| Stress | 10 | Work-life balance |
| Location | 5 | Commute + hybrid policy |

### Example Session

```
User: Add to backlog: https://linkedin.com/jobs/view/3847592847

Claude: Saved to backlog:
        Company: NVIDIA
        Title: Senior TPM
        Added: 2025-11-25
        ID: nvidia-senior-tpm-backlog-20251125

User: Analyze job nvidia-senior-tpm-backlog-20251125

Claude: ANALYSIS COMPLETE

        Company: NVIDIA (Tier 1)
        Position: Senior Technical Program Manager
        Location: Santa Clara, Hybrid

        SCORE: 82/100 (First Priority)
        RANK: #3 of 47 analyzed jobs

        Scores:
        - Match: 31/35
        - Income: 22/25
        - Growth: 18/20
        - LowPrep: 12/15
        - Stress: 7/10
        - Location: 3/5

        NEXT STEPS:
        1. Update cv-tpm.md CV
        2. Start prep (8 hours estimated)
        3. Research hiring manager
```

---

## Reading List

**Purpose**: Capture articles via Apple Notes, auto-scrape, summarize, and organize.

### Commands

#### Process Inbox
```
process reading list
```
Process all URLs from the Apple Notes inbox.

#### View Articles
```
show unread
```
List all unread articles.

```
show reading list
```
Full list with status.

```
show ai articles
```
Filter by category.

#### Search
```
search: machine learning
```
Find articles by keyword.

```
summarize ai
```
Get summaries by topic/category.

#### Update Status
```
mark read: Building LLM Applications
```
Mark article as read.

```
archive: Old Article Title
```
Move to archived status.

### Categories

| Category | Description |
|----------|-------------|
| tech | Programming, tools, engineering |
| ai | AI/ML, LLMs, data science |
| business | Strategy, management, startups |
| career | Job search, skills, growth |
| finance | Investing, markets, economics |
| science | Research, discoveries |
| other | Everything else |

### Example Session

```
User: process reading list

Claude: Processing Reading List Inbox...
        Found 5 new URLs

        Processing: https://example.com/llm-apps-2024
        - Title: Building LLM Applications in 2024
        - Category: ai
        - Read time: 12 min
        - Summary: Comprehensive guide covering RAG implementation...

        [Processing 4 more...]

        Processed 5 articles:
        - 3 AI articles
        - 1 Career article
        - 1 Tech article

User: show unread

Claude: Reading List - 12 Unread

        AI (5)
        - Building LLM Applications (12 min)
        - RAG Best Practices (8 min)
        - Claude 4 Features (6 min)

        Career (3)
        - Tech Interview Guide 2024 (15 min)
        - Salary Negotiation Tips (10 min)
```

---

## Ideas Capture

**Purpose**: Capture fleeting ideas, expand with AI, evaluate potential, and organize.

### Commands

#### Process Inbox
```
process ideas
```
Process all ideas from Apple Notes inbox.

#### View Ideas
```
show ideas
```
List all ideas by type.

```
show startup ideas
```
Filter by type (patent/startup/business/project).

```
show hot ideas
```
Show high-scoring ideas (7+).

#### Expand & Evaluate
```
expand: AI resume optimizer
```
Generate detailed expansion of an idea.

```
evaluate: AI resume optimizer
```
Score and analyze potential.

#### Link Related Ideas
```
link ideas: Resume AI + Job Matching
```
Connect related ideas.

#### Search
```
search ideas: automation
```
Find ideas by keyword.

### Idea Types

| Type | Tag | Description |
|------|-----|-------------|
| Patent | [Patent] | Novel inventions, technical innovations |
| Startup | [Startup] | Business ventures, product ideas |
| Business | [Business] | Process improvements, revenue ideas |
| Project | [Project] | Personal/side projects, tools |
| Other | [Other] | Miscellaneous ideas |

### Scoring Dimensions

| Dimension | Description |
|-----------|-------------|
| Feasibility | How realistic to implement |
| Impact | Potential value/change |
| Effort | Resources required (low=good) |
| Uniqueness | How novel/differentiated |
| Timing | Market/tech readiness |
| Personal Fit | Alignment with skills |

### Example Session

```
User: process ideas

Claude: Processing Ideas Inbox...
        Found 3 new ideas

        [Startup] AI-powered resume optimizer
        - Expanded: Full concept with market analysis
        - Score: 8.2/10 (Hot)
        - Tier: Hot

        [Project] CLI tool for note organization
        - Expanded: Features and tech stack
        - Score: 6.5/10 (Warm)
        - Tier: Warm

        Processed 3 ideas (1 Hot, 1 Warm, 1 Cold)

User: expand: AI resume optimizer

Claude: AI-powered Resume Optimizer

        Score: 8.2/10 (Hot)

        Problem & Market Need:
        Job seekers struggle to tailor resumes for ATS systems...

        Solution Overview:
        AI tool that analyzes job descriptions and automatically
        customizes resumes for maximum compatibility...

        Target Customers:
        - Active job seekers
        - Career changers
        - Recruiting agencies

        MVP Features:
        1. Job description parser
        2. Resume analyzer
        3. Auto-tailor engine
        4. ATS score predictor
```

---

## Voice Memos

**Purpose**: Process voice memos - transcribe, extract action items, and organize.

### Commands

#### Process Inbox
```
process voice memos
```
Process all memos from Apple Notes inbox.

#### Direct Transcription
```
transcribe [file]
```
Transcribe a single uploaded file.

```
transcribe and analyze this
```
Full transcription with analysis (for uploaded files).

#### View Transcripts
```
show transcripts
```
List all transcripts.

```
show pending memos
```
List unprocessed memos.

#### Search
```
search memos: project deadline
```
Find by keyword in transcripts.

### Supported Formats

- `.m4a` (Voice Memos default)
- `.mp3`
- `.wav`
- `.aac`
- `.opus`
- `.flac`

### Analysis Output

Each memo is analyzed for:
- **Summary**: Brief overview
- **Key Points**: Main topics (up to 7)
- **Action Items**: Tasks with priorities (HIGH/MEDIUM/LOW)
- **People Mentioned**: Names extracted
- **Dates Mentioned**: Deadlines, events
- **Category**: meeting, journal, task-list, brainstorm, etc.

### Example Session

```
User: process voice memos

Claude: Processing Voice Memos Inbox...
        Found 2 memos to process

        Processing: team-standup-2024-11-24.m4a
        - Duration: 5:32
        - Language: English
        - Speakers: 3 detected

        Summary:
        Daily standup covering sprint progress. Team discussed
        blockers on authentication feature.

        Action Items:
        - [HIGH] Fix auth API integration (@Dan) - Due: Nov 25
        - [MEDIUM] Prepare onboarding for new designer (@Sarah)
        - [LOW] Update sprint board (@Team)

        Saved to: transcripts/2024-11-24-team-standup.md

User: search memos: authentication

Claude: Found 3 results:

        1. team-standup-2024-11-24.m4a
           "...authentication feature blocked by API changes..."

        2. planning-session-2024-11-20.m4a
           "...need to implement OAuth authentication..."
```

---

## Local RAG

**Purpose**: Index local folders and query them using semantic search.

### Commands

#### Index Documents
```
update rag from ~/Documents/research
```
Index files in the specified folder.

```
update rag from ~/Downloads/papers
```
Index a different folder.

#### Search Documents
```
query rag what are the key findings about climate change?
```
Search indexed documents semantically.

```
search documents neural network training
```
Alternative search command.

### Supported File Types

**Documents:**
- PDF (`.pdf`)
- Word (`.docx`)
- PowerPoint (`.pptx`)
- Excel (`.xlsx`)

**Text Files:**
- Markdown (`.md`)
- Plain text (`.txt`)
- JSON/YAML (`.json`, `.yaml`)

**Code Files:**
- Python, JavaScript, TypeScript
- HTML, CSS
- C, C++, Shell

**Images (with OCR):**
- PNG, JPEG, TIFF, WebP

### Example Session

```
User: update rag from ~/Documents/research-papers

Claude: Scanning ~/Documents/research-papers...
        Found 47 PDF files, 12 markdown files
        Indexing complete. Processed 59 files (1,247 chunks).

User: query rag neural network training techniques

Claude: Found 5 relevant results:

        1. deep-learning-survey.pdf (score: 0.89)
           "...backpropagation remains the primary training
           algorithm for neural networks..."

        2. optimization-methods.md (score: 0.84)
           "...Adam optimizer combines momentum with
           adaptive learning rates..."

        3. transformer-architecture.pdf (score: 0.78)
           "...attention mechanisms enable parallel training..."

User: update rag from ~/Documents/research-papers

Claude: Scanning for changes...
        3 files modified since last index
        Indexing complete. Processed 3 files.
```

---

## Apple Notes Setup

### Creating Inbox Notes

For each skill that uses Apple Notes, create a note with this structure:

```
{Emoji} {Skill Name} Inbox

ADD BELOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Your items here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCESSED

[Stats will appear here]
```

### Required Notes

| Skill | Note Name |
|-------|-----------|
| Career Consultant | Job Links Inbox |
| Reading List | Reading List Inbox |
| Ideas Capture | Ideas Inbox |
| Voice Memos | Voice Memos Inbox |

### Adding Items

**Job Links:**
```
https://linkedin.com/jobs/view/12345
https://company.com/careers/position
```

**Reading List:**
```
https://example.com/article-1
https://blog.com/interesting-post
```

**Ideas (with optional type tags):**
```
[Startup] App that tracks coffee consumption
[Patent] Novel battery cooling mechanism
Just a random thought (auto-classified)
```

**Voice Memos:**
```
meeting-2024-11-24.m4a
brainstorm-session.mp3
```

---

## Data Storage

### Location

All user data is stored separately from skill code:

```
~/MyDrive/claude-skills-data/
├── career-consultant/
│   ├── profile/
│   │   └── settings.yaml
│   ├── companies/
│   ├── jobs/
│   │   ├── backlog.yaml
│   │   └── analyzed/
│   └── reports/
├── reading-list/
│   ├── reading-list.yaml
│   └── summaries/
├── ideas-capture/
│   ├── ideas.yaml
│   └── expanded/
├── voice-memos/
│   ├── transcripts/
│   └── analyzed/
└── local-rag/
    └── chromadb/
```

### Database Format

All databases use YAML format:

```yaml
# reading-list.yaml example
stats:
  total: 42
  unread: 12

items:
  - id: building-llm-applications
    title: "Building LLM Applications in 2024"
    url: https://example.com/llm-apps
    status: unread
    category: ai
    added_at: 2024-11-24T10:30:00Z
```

---

## Tips

### General

- **Process regularly**: Batch process weekly for efficiency
- **Use mobile**: Apple Notes syncs across devices for on-the-go capture
- **Search often**: Find patterns in your data
- **Review periodically**: Revisit old items - priorities change

### Per Skill

**Career Consultant:**
- Start fresh conversation for each job analysis (token efficiency)
- Use backlog mode for quick capture during job hunting
- Review company research before full analysis

**Reading List:**
- One URL per line in inbox
- Process once you have 5-10 articles
- Use categories to find related content

**Ideas Capture:**
- Capture first, evaluate later
- Use type tags for better organization
- Link related ideas to find patterns

**Voice Memos:**
- Add speaker hints: "Speakers: John, Sarah"
- Works with mixed languages (English + Hebrew)
- Batch process weekly

**Local RAG:**
- Index important folders once
- Incremental updates are fast
- Semantic search finds related content

---

**Version**: 1.0.0
**Last Updated**: 2025-11-25
