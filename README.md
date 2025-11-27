# Claude Skills Ecosystem

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-6-blue.svg)](packages/)
[![Version](https://img.shields.io/badge/monorepo-v1.1.0-green.svg)](PROJECT.md)

**A collection of AI-powered Claude skills for automating personal productivity workflows.**

---

## What Is This?

This monorepo contains a suite of Claude skills that help automate common personal productivity tasks. Each skill is designed to work with Apple Notes for mobile-friendly capture and local filesystem for data storage.

### The Problem

You have scattered workflows across different apps:
- Job links saved in random browser tabs
- Reading list spread across Pocket, bookmarks, and notes
- Ideas lost in voice memos and sticky notes
- Documents you can never find when you need them

### The Solution

One ecosystem of AI skills that:
1. **Capture** - Use Apple Notes as universal inbox (mobile-friendly)
2. **Process** - Claude analyzes, scores, and organizes automatically
3. **Store** - Local YAML/Markdown files (git-friendly, portable)
4. **Act** - Get prioritized recommendations and actionable insights

---

## Available Skills

| Skill | Description | Apple Note Inbox | Command |
|-------|-------------|------------------|---------|
| [Career Consultant](packages/career-consultant/) | AI-powered job analysis with 6-component scoring | Job Links Inbox | `process inbox` |
| [Reading List](packages/reading-list/) | Article capture, summarization, and tracking | Reading List Inbox | `process reading list` |
| [Ideas Capture](packages/ideas-capture/) | Idea expansion, scoring, and categorization | Ideas Inbox | `process ideas` |
| [Voice Memos](packages/voice-memos/) | Transcription, analysis, and action extraction | Voice Memos Inbox | `process voice memos` |
| [Local RAG](packages/local-rag/) | Semantic search across local documents | N/A | `query rag [question]` |
| [Social Media Post](packages/social-media-post/) | Platform-optimized post generation with algorithm insights | N/A | `create [platform] post` |

---

## Quick Start

### Option 1: One-Line Installer (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/gsannikov/claude-skills/main/install.sh | bash
```

This will:
1. Check prerequisites (git, python3)
2. Clone the repository to `~/MyDrive/claude-skills`
3. Run the interactive setup wizard
4. Configure Claude Desktop with MCP servers
5. Create data directories

### Option 2: Manual Installation

```bash
# Clone the repo
git clone https://github.com/gsannikov/claude-skills.git ~/MyDrive/claude-skills
cd ~/MyDrive/claude-skills

# Run setup wizard
python setup.py
```

### Setup Options

```bash
python setup.py              # Interactive setup (recommended)
python setup.py --check      # Check installation status
python setup.py --uninstall  # Remove skills and configs
```

### After Installation

The setup wizard will:
- Create data directories at `~/MyDrive/claude-skills-data/`
- Configure MCP servers in Claude Desktop
- Show you all available commands
- Guide you through Apple Notes inbox setup

### Daily Usage

**Mobile Capture**:
1. Open Apple Notes on your phone
2. Add items to the appropriate inbox note
3. Items sync via iCloud

**Processing**:
1. Open Claude with the skill loaded
2. Say the skill's command (e.g., `process inbox`)
3. Get processed results with AI analysis

---

## Architecture

```
claude-skills/
├── packages/                      # Individual skills
│   ├── career-consultant/         # Job analysis & scoring
│   ├── reading-list/              # Article management
│   ├── ideas-capture/             # Idea tracking
│   ├── voice-memos/               # Audio transcription
│   ├── local-rag/                 # Document search
│   └── social-media-post/         # Social media post generator
├── shared/
│   ├── scripts/                   # Release, generator utilities
│   ├── templates/                 # Patterns and templates
│   ├── marketing/                 # Blog posts, articles
│   └── workflows/                 # Troubleshooting guides
├── .github/workflows/             # CI/CD automation
├── CLAUDE.md                      # Global Claude instructions
├── PROJECT.md                     # Architecture & roadmap
├── CONTRIBUTING.md                # Contribution guidelines
└── README.md                      # This file
```

### User Data Location

All user data is stored separately from the codebase:

```
~/MyDrive/claude-skills-data/
├── career-consultant/             # Job analyses, company profiles
├── reading-list/                  # Articles, summaries
├── ideas-capture/                 # Ideas database
├── voice-memos/                   # Transcripts
├── local-rag/                     # Vector database
└── social-media-post/             # Generated posts, analytics
```

**Key Principle**: Code and data are completely separated. User data is never committed to git.

---

## Key Features

### Universal Patterns

All skills share common patterns:

| Pattern | Description |
|---------|-------------|
| **Apple Notes Inbox** | Mobile-friendly capture via iCloud sync |
| **YAML Storage** | Human-readable, git-friendly data format |
| **AI Processing** | Claude-powered analysis and recommendations |
| **Deduplication** | Automatic duplicate detection |
| **Stats Tracking** | Processing history and metrics |

### Token Efficiency

Skills are designed for optimal token usage:
- On-demand module loading
- Smart caching (company research, etc.)
- Progressive processing (backlog → analysis)

### MCP Integration

Optional MCP servers enhance functionality:
- **Filesystem MCP** - Local file access
- **Firecrawl MCP** - Web scraping
- **Bright Data MCP** - LinkedIn parsing
- **Apple Notes MCP** - Direct note access

---

## Skill Highlights

### Career Consultant (v1.1.1)

**For**: Tech professionals job searching in Israel

- 6-component scoring (Match, Income, Growth, LowPrep, Stress, Location)
- Smart company caching (research once, reuse forever)
- Multi-CV variant matching
- STAR interview story builder
- Excel tracking with auto-ranking

[Full Documentation](packages/career-consultant/README.md)

### Reading List (v1.0.0)

**For**: Anyone drowning in "read later" articles

- AI summarization (150 words + key takeaways)
- Auto-categorization (Tech, AI, Business, etc.)
- Read time estimates
- Progress tracking (unread → done)

[Full Documentation](packages/reading-list/README.md)

### Ideas Capture (v1.0.0)

**For**: Inventors, entrepreneurs, thinkers

- 6-dimension scoring (Feasibility, Impact, Effort, etc.)
- Type classification (Patent, Startup, Business, Project)
- AI expansion of brief ideas
- Idea linking across categories

[Full Documentation](packages/ideas-capture/README.md)

### Voice Memos (v1.0.0)

**For**: People who think out loud

- Multi-language transcription
- Speaker identification (up to 10)
- Action item extraction with priorities
- Auto-categorization (Meeting, Journal, Task-list)

[Full Documentation](packages/voice-memos/README.md)

### Local RAG (v1.0.0)

**For**: Knowledge workers with large document collections

- Semantic search (meaning, not keywords)
- Multiple file formats (PDF, MD, code files)
- Persistent ChromaDB storage
- Incremental indexing

[Full Documentation](packages/local-rag/README.md)

### Social Media Post (v1.0.0)

**For**: Content creators and marketers

- Platform optimization (Threads, X, LinkedIn)
- 2025 algorithm insights
- Multiple post variants (short, medium, long)
- Engagement scoring and best posting times
- Character count validation

[Full Documentation](packages/social-media-post/README.md)

---

## Requirements

### Minimal
- **Claude.ai account** (free or paid)
- **Apple Notes** (for mobile capture)
- **Python 3.8+** (for some scripts)

### Recommended
- **MCP Filesystem server** - Local file operations
- **MCP Firecrawl** - Web scraping capabilities

---

## Release Process

Each skill is versioned independently:

```bash
# Release a specific skill
python shared/scripts/release.py career-consultant --patch

# Or use GitHub Actions
# Go to Actions → Release Skill → Select skill and bump type
```

Tags follow the pattern: `{skill}-v{version}` (e.g., `career-consultant-v1.1.1`)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ideas for contribution**:
- New skills
- Skill improvements
- Documentation
- Bug fixes
- Testing

---

## License

MIT License - see [LICENSE](LICENSE) for details.

Copyright (c) 2025 Gur Sannikov

---

## Links

- **Repository**: https://github.com/gsannikov/claude-skills
- **Issues**: https://github.com/gsannikov/claude-skills/issues
- **Project Roadmap**: [PROJECT.md](PROJECT.md)
- **Author**: [@gsannikov](https://github.com/gsannikov)

---

**Version**: Monorepo v1.1.0 | **Status**: Active Development | **Last Updated**: 2025-11-26

> Built with Claude Skills SDK
