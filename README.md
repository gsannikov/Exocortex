# Exocortex
> **Infrastructure for Augmenting the Human Mind**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://github.com/gsannikov/exocortex/actions/workflows/validate.yml/badge.svg)](https://github.com/gsannikov/exocortex/actions/workflows/validate.yml)
[![Skills](https://img.shields.io/badge/skills-10-blue.svg)](packages/)
[![Version](https://img.shields.io/badge/monorepo-v1.2.0-green.svg)](docs/project-status.md)
[![AlignTrue](https://img.shields.io/badge/AlignTrue-enabled-purple.svg)](.aligntrue/)
[![Platform](https://img.shields.io/badge/AI-agnostic-orange.svg)](docs/developer-guide.md#aligntrue-workflow)

**Exocortex** is a local-first system that extends your biological mind with AI, memory, and automated agency.
It integrates deeply with your environment—**Apple Notes**, **Filesystem**, and **Voice**—to create a seamless loop of capture, processing, and recall.
All data is stored in `~/exocortex-data`: Human-readable, human-owned, and forever capable.

---

## 🚀 One-Command Install

Copy and paste this into your terminal. That's it.

```bash
curl -fsSL https://raw.githubusercontent.com/gsannikov/exocortex/main/install.sh | bash
```

**What this does:**
1.  Sets up your **Exocortex** (default: `~/Projects/exocortex`)
2.  Installs all capabilities (Memory, RAG, Analysis)
3.  Configures Claude Desktop automatically
4.  Sets up your sovereign data vault (default: `~/exocortex-data`)

**Note**: User data path is configured in `shared/config/paths.py` - edit this file to change the location.

---

## ⚡️ What You Get

| Skill | What It Does |
|-------|--------------|
| **💼 Job Analyzer** | Analyzes job posts with 6-point scoring (Match/Income/Growth), tracks LinkedIn applications, manages recruiter contacts, and sends follow-up reminders. |
| **🎯 Interview Prep** | STAR story builder, company deep-dives, practice mode, and salary negotiation preparation. |
| **📚 Reading List** | Captures articles from your inbox, summarizes them, and tracks reading progress. |
| **💡 Ideas Capture** | Turns fleeting thoughts into expanded project plans with feasibility scoring. |
| **🎙️ Voice Memos** | Transcribes audio, extracts action items, and identifies speakers. |
| **🔍 Local RAG** | Searches your local documents (PDF, Docx, Code) using semantic understanding. |
| **📱 Social Media** | Generates optimized posts for LinkedIn, X, and Threads with algorithm insights. |
| **🍳 Recipe Manager** | Extracts recipes from web/images to local YAML files. Tracks family preferences. |
| **🔧 Setup Manager** | Automates the environment setup, dependency management, and system health checks. |
| **🏭 Next-Skill** | Skill factory - AI-assisted skill creation with GitHub discovery, MCP registry search, code adaptation, or fresh scaffolding. |

---

## 🆚 Exocortex vs. Standard Claude Skills

| Feature | Exocortex | Standard Claude Skills |
|---------|-----------|------------------------|
| **Execution Environment** | Local-First (Runs on your machine) | Remote / Cloud (API dependent) |
| **Data Storage** | Open Filesystem (Markdown/JSON in `~/exocortex-data`) | Opaque / Database (Hidden or Siloed) |
| **Agent IDE Support** | Multi-Agent / Polyglot (AlignTrue support) | Single Platform (Claude Desktop only) |
| **Architecture** | Decoupled (MCP Server exposed locally) | Tightly Coupled (SDK dependent) |
| **Evolution** | Self-Learning (Grows with usage) | Static (Fixed capabilities) |
| **Latency** | Instant (Local IO, no git sync req) | Network Latency (API calls / Sync) |
| **Cloud Strategy** | Flexible Bridge (BYO Cloud: GDrive, Dropbox, iCloud) | Fixed / Vendor Lock-in |
| **Knowledge Retrieval** | Built-in Local RAG | External Service / None |
| **Testing Framework** | Included (pytest, validation suite) | None / DIY |
| **Security** | Built-in (input validation, safe defaults) | Manual / Varies |
| **CI/CD** | GitHub Actions included | None / External |

**Key Differentiators:**
- **🔑 Ownership**: You own the pipe and the data — not renting the capability
- **🛠️ Customizability**: Code is yours to modify — not a black box

---

## 📱 How It Works

1.  **Capture**: Save links, ideas, or voice memos to your **Inbox** (e.g., Apple Notes, Email, or File).
2.  **Process**: Open Claude and say a command (e.g., `"process inbox"`).
3.  **Done**: Claude analyzes, organizes, and saves everything to your local files.

---

## 🔄 Skill Workflow

### Job Search Flow
```
Job Analyzer                    Interview Prep
───────────────────────────────────────────────
Analyze: [URL]          →       Prepare for [company]
Track LinkedIn app      →       Practice STAR stories
Show reminders          →       Prep negotiation
```

Both skills share data in `~/exocortex-data/career/` for seamless handoff.

---

## 📚 Documentation

- **[User Guide](docs/user-guide.md)**: Detailed commands and workflows.
- **[Developer Guide](docs/developer-guide.md)**: Architecture and manual setup.
- **[AlignTrue Setup](.aligntrue/README.md)**: Cross-platform AI instruction sync.
- **[Vision & Roadmap](docs/vision.md)**: Why we built this and where we're going.
- **[FAQ](docs/faq.md)**: Common questions and troubleshooting.
- **[Contributing](CONTRIBUTING.md)**: How to build new skills.
- **[Project Status](docs/project-status.md)**: Current roadmap and ADRs.

---

## 🔗 Links

- **Repository**: https://github.com/gsannikov/exocortex
- **Issues**: https://github.com/gsannikov/exocortex/issues
- **Author**: [@gsannikov](https://github.com/gsannikov)

> Built with Claude Skills SDK
 
