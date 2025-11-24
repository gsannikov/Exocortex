# Israeli Tech Career Consultant v9.25.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-9.25.0-blue.svg)](version.yaml)

**AI-powered job analysis for Israeli tech market with 6-component scoring, CV matching, and smart company caching.**

---

## 🎯 What It Does

Your AI career advisor for data-driven job decisions in Israel's tech market:

- **📋 Quick Backlog** - Capture 50-100 jobs in minutes (~5K tokens each)
- **📝 Apple Notes Inbox** - Paste URLs into "Job Links Inbox" note, process with one command
- **📊 Deep Analysis** - 6-component scoring system (Match, Income, Growth, LowPrep, Stress, Location)
- **🏢 Smart Caching** - Research companies once, reuse forever (saves 15-20K tokens per job)
- **📈 Auto-Tracking** - Excel database with priority rankings and trends
- **🎨 Multi-CV Engine** - Match jobs against multiple CV variants (EM, TPM, AI, etc.)
- **🎤 Interview Prep** - STAR framework story builder with 100-point quality scoring
- **⚡ Token Efficient** - Progressive module loading, optimized for long job searches

**Scoring System**: Jobs rated 0-100 across 6 weighted dimensions:
- Match (35 pts), Income (25 pts), Growth (20 pts), LowPrep (15 pts), Stress (10 pts), Location (5 pts)

**Priority Tiers**:
- First Priority (≥70) - Apply immediately
- Second Priority (50-69) - Strong consideration
- Third Priority (<50) - Keep on radar

---

## 💡 Why Use This?

### The Problem
You find 50-100 job postings. Which 5-10 should you actually spend time applying to?

### The Old Way (Spreadsheet Hell)
- Copy-paste job details into Excel
- Try to remember company info
- Guess at match quality
- Waste hours on low-probability jobs
- Miss great opportunities buried in the list

### The New Way (This Tool)
1. **Capture** - Save 100 jobs in 30 minutes
2. **Research** - AI researches 20 unique companies once
3. **Analyze** - Get ranked list with objective scores
4. **Focus** - Apply only to your top 10 First Priority jobs
5. **Prepare** - Build STAR stories for interviews

**Result**: 5-10x better ROI on your time. Focus on quality over quantity.

### Perfect For
- 🎯 **Senior+ Tech Roles** - EM, Staff Engineer, TPM, Principal, Director
- 🇮🇱 **Israeli Market Focus** - Optimized for local companies and culture
- 💰 **High Comp Roles** - ₪450K+ annual packages
- 🔄 **Career Switchers** - Multiple CV variants for different positioning
- ⏱️ **Time-Constrained** - Full-time workers doing parallel job search

### At a Glance

| Manual Spreadsheet | This Tool |
|-------------------|-----------|
| 2-3 hours per job | 5 min capture + 15 min analysis |
| Remember company details | Cached, validated research |
| Gut feeling ranking | Objective 6-component scoring |
| Single CV positioning | Multi-variant matching |
| Hope for the best | Data-driven decisions |
| No interview prep | STAR story builder included |

---

## 🚀 How It Works

### The 3-Phase System

**Phase 1: Capture** (5K tokens/job)
- Save 50-100 job URLs to your backlog in minutes
- Lightweight metadata extraction
- No deep analysis yet - just building your pipeline

**Phase 2: Intelligence** (One-time, 15-20K tokens/company)
- Research each unique company once
- Smart caching means instant reuse
- Validate research before continuing

**Phase 3: Decision** (10-15K tokens/job)
- Deep analysis with 6-component scoring
- Match against all your CV variants
- Get priority rankings (First/Second/Third)
- Auto-generate Excel tracking

**Bonus: Interview Prep** (5-8K tokens/story)
- Build STAR stories for top opportunities
- Get quality scores and improvement tips
- Build your story library

---

## ⚡ Quick Start

### 1. Download & Upload (2 minutes)

1. **Download**: [Get latest release](https://github.com/gsannikov/israeli-tech-career-consultant/releases/latest) (.skill file)
2. **Upload**: Drag the `skill-package/` folder into Claude.ai
3. **Start**: Type "Hi, let's set up my career consultant"

That's it! No complex installation, no config files, no manual setup.

### 2. Interactive Setup (5-10 minutes)

Claude guides you through:
- ✅ Where to store your data
- ✅ Your CV variants (EM/TPM/AI etc.)
- ✅ Scoring preferences and weights
- ✅ Salary expectations
- ✅ Location preferences
- ✅ Installing Python packages

Everything happens **in the chat**. Just answer questions!

### 3. Start Analyzing

Once setup is done, you're ready:

```
Add to backlog: https://linkedin.com/jobs/view/12345
Batch add: [paste 10 URLs]
Analyze this job: https://linkedin.com/jobs/view/12345
Show my top 10 jobs
Research: Google Israel
Build STAR story: Led AWS migration for 50-person team
```

---

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| [🔧 MCP Setup](docs/guides/USER_GUIDE.md) | Install and configure required MCP servers |
| [📦 Complete Setup](docs/guides/USER_GUIDE.md) | Full installation and configuration guide |
| [📖 Usage Examples](docs/guides/USER_GUIDE.md) | Detailed workflows and commands |
| [🔍 Troubleshooting](docs/guides/USER_GUIDE.md) | Common issues and solutions |
| [🤝 Contributing Guide](docs/meta/CONTRIBUTING.md) | How to contribute to the project |
| [📜 Code of Conduct](docs/meta/CODE_OF_CONDUCT.md) | Guidelines for community interaction |
| [📋 Changelog](docs/meta/CHANGELOG.md) | Version history and release notes |

---

## 🎨 Key Features

### 7 Integrated Modules

1. **🏢 Company Research** - Multi-source intelligence gathering with smart caching
2. **🎯 Skills Matching** - CV-to-job proficiency analysis across multiple variants
3. **📊 Scoring Engine** - 6-component algorithmic ranking (0-100 points)
4. **📋 Job Backlog** - Lightning-fast capture system for pipeline building
5. **💾 Database Operations** - Hybrid YAML+Markdown storage with Excel export
6. **📝 Output Templates** - Structured reports and tracking documents
7. **🎤 STAR Framework** - Interview story builder with quality scoring

### Dual Workflow Modes

**Backlog Mode** (Week 1-2):
- Capture 50-100 jobs in hours (~5K tokens each)
- Lightweight metadata extraction
- Build your pipeline fast

**Analysis Mode** (Week 3-4):
- Deep 6-component scoring per job
- Multi-CV variant matching
- Company research integration
- Excel tracking generation

### Smart Company Caching

**First Analysis**:
- Research: 15-20K tokens
- Requires validation
- Deep company intelligence

**Subsequent Jobs**:
- Reuse cached data: 0K tokens
- Instant analysis
- Consistent scoring

### Multi-CV Strategy

Support for multiple CV variants:
- **Engineering Manager** - Leadership focus
- **Technical Program Manager** - Cross-functional skills
- **AI/ML Engineer** - Technical depth
- **Custom variants** - Your unique positioning

Each job gets matched against ALL variants to find your best angle.

### Interview Preparation

**STAR Story Builder**:
- Structured Situation-Task-Action-Result format
- 100-point quality scoring system
- 7 competency categories (Leadership, Technical, Communication, etc.)
- Story library management
- Interview-ready presentation

### Intelligent Tool Selection

Auto-routes tasks to optimal tools:
- **Bright Data**: LinkedIn scraping (handles authentication)
- **Firecrawl**: Company research and job postings
- **MCP Filesystem**: Local data storage
- **Python Scripts**: Excel generation, YAML processing

---

## 📊 Complete Job Search Workflow

### Week 1-2: Build Your Pipeline
**Goal**: Capture 50-100 opportunities fast
```
process inbox                              # Process URLs from Apple Notes "Job Links Inbox"
Batch add these 10 jobs: [paste URLs]
Add to backlog: https://linkedin.com/jobs/view/12345
Show my backlog status
```
**Token cost**: ~5K per job = 250-500K total

### Week 3: Company Intelligence
**Goal**: Research unique companies once
```
Research: Google Israel
Research: Microsoft Development Center
Update company: Nvidia - add recent layoff news
```
**Token cost**: ~15-20K per company (one-time)

### Week 4: Deep Analysis
**Goal**: Score and rank all opportunities
```
Analyze all jobs from backlog
Show my First Priority jobs
Generate Excel report
```
**Token cost**: ~10-15K per job (company data cached)

### Week 5: Interview Prep
**Goal**: Prepare STAR stories for top jobs
```
Build STAR story: Led team through AWS migration
Score my story about scaling system to 1M users
Show all my leadership stories
```
**Token cost**: ~5-8K per story

### Week 6: Apply & Track
**Goal**: Submit applications strategically
```
Mark job nvidia-senior-tpm as "Applied"
Show application pipeline
Update job status: Interview scheduled
```

📖 **More examples**: [docs/guides/USER_GUIDE.md](docs/guides/USER_GUIDE.md)

---

## 🛠️ Requirements

### Minimal Setup
- **Claude.ai account** (free or paid)
- **Python 3.8+** (for Excel tracking)
- **MCP Filesystem** (installed during setup)

### Optional MCP Servers
These enhance the experience but aren't required:
- **Firecrawl** - Better web scraping
- **Bright Data** - LinkedIn access
- **MCP Docker** - Advanced scraping

### Python Packages
Installed automatically during setup:
```bash
pip install pyyaml pandas openpyxl
```

All other setup happens **in the Claude chat** - no complex configuration files!

---

## 📁 Project Structure

```
career-consultant.skill/
├── skill-package/           # Core skill (upload to Claude)
│   ├── SKILL.md            # Main orchestrator
│   ├── modules/            # Analysis modules
│   ├── scripts/            # Helper utilities
│   ├── config/             # Configuration
│   └── templates/          # User templates
├── docs/                   # Documentation
├── host_scripts/           # Host automation package (`python -m host_scripts …`)
└── user-data/             # Your data (not in repo)
```

---

## 🆕 What's New in v9.25

### Latest Features
- 📝 **Apple Notes Inbox** - Paste job URLs into "Job Links Inbox" note, say "process inbox" to batch-add
- 🎤 **STAR Framework Module** - Build interview stories with 100-point quality scoring
- 💬 **Interactive Setup** - Complete configuration happens in Claude chat
- 📦 **One-Click Install** - Just download and upload, no manual config needed
- 🏢 **Enhanced Company Research** - Multi-source intelligence with smart validation
- 📊 **7 Integrated Modules** - Complete job search system from capture to interview

### Recent Improvements (v9.13-9.24)
- ✨ **Simplified Documentation** - 50% fewer files, better organization
- 🔧 **Streamlined Host Scripts** - Easier maintenance and development
- ⚡ **Better Token Management** - Optimized module loading
- 🎯 **Configurable Tool Priority** - Choose your preferred scraping tools
- 📝 **Enhanced Validation** - Better error messages and guidance

Full changelog: [CHANGELOG.md](CHANGELOG.md)

---

## 🛠 For Developers

### Host Automation

If you're contributing or maintaining this project:

```bash
# Quick release workflow
python -m host_scripts release

# Other commands
python -m host_scripts bump-version --minor
python -m host_scripts update-version
python -m host_scripts validate
```

📖 **Full developer guide**: [docs/guides/DEVELOPER_GUIDE.md](docs/guides/DEVELOPER_GUIDE.md)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/meta/CONTRIBUTING.md) for guidelines.

**Ideas for contribution**:
- Additional scoring algorithms
- New analysis modules
- Documentation improvements
- MCP tool integrations
- Country-specific adaptations

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

Copyright (c) 2025 Gur Sannikov

---

## 🆘 Support

**Need help?**

1. Check [Troubleshooting Guide](docs/guides/USER_GUIDE.md)
2. Review [documentation](docs/)
3. Search [GitHub issues](https://github.com/gsannikov/israeli-tech-career-consultant/issues)
4. Open a new issue with details

---

## 🔗 Quick Links

- **Repository**: https://github.com/gsannikov/israeli-tech-career-consultant
- **Latest Release**: https://github.com/gsannikov/israeli-tech-career-consultant/releases/latest
- **Report Issue**: https://github.com/gsannikov/israeli-tech-career-consultant/issues/new

---

**Version**: 1.1.1 | **Status**: Stable | **Last Updated**: 2025-11-24

> Version managed via `version.yaml` - Single source of truth
