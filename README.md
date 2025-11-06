# Claude Skills SDK Template

**Version:** 1.1.0 | **License:** MIT | **Status:** Production Ready

Build production-grade Claude skills with multi-backend storage, automation, and best practices.

---

## 👋 First Time Here? Get Interactive Onboarding!

### The Easiest Way to Start (Recommended)

1. **Open Claude** at claude.ai
2. **Attach this entire repo** to your conversation
3. **Say:** "hi" or "help me get started"
4. **Follow the guided onboarding** (~10-15 minutes)

Claude will read [CLAUDE_ONBOARDING_GUIDE.md](docs/skill-developers/getting-started/CLAUDE_ONBOARDING_GUIDE.md) and walk you through everything interactively!

**Also see:** [WELCOME.md](docs/skill-developers/getting-started/WELCOME.md) for quick intro

---

## 🎯 What This Template Provides

A **production-ready framework** for building Claude Skills featuring:

### Core Features
- **5 Storage Backends** - Local, GitHub, Checkpoint, Email, Notion
- **Three-Tier Architecture** - skill-package, user-data, docs
- **Automation Tools** - validate, release, setup scripts
- **Token Management** - Progressive disclosure, budget protection
- **Best Practices** - From Anthropic + battle-tested patterns

### Perfect For
- Company-specific skills
- Workflow automation  
- Research & analysis tools
- Knowledge management
- Team collaboration

---

## 📚 Quick Navigation

**New Users:**
- [WELCOME.md](docs/skill-developers/getting-started/WELCOME.md) - Start here!
- [QUICK_SETUP.md](docs/skill-developers/getting-started/QUICK_SETUP.md) - Manual setup guide
- [CLAUDE_ONBOARDING_GUIDE.md](docs/skill-developers/getting-started/CLAUDE_ONBOARDING_GUIDE.md) - For Claude's reference

**Documentation:**
- [Documentation Structure](docs/shared/DOCUMENTATION_STRUCTURE.md) - Complete navigation guide
- [DEPENDENCIES.md](docs/skill-developers/getting-started/DEPENDENCIES.md) - Storage backends & setup
- [User Guide](docs/skill-developers/user-guide/) - User guides and tutorials
- [Developer Guide](docs/skill-developers/guides/) - Development documentation

**Resources:**
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [CHANGELOG.md](docs/shared/CHANGELOG.md) - Version history
- [LICENSE](LICENSE) - MIT license

---

## 🏗️ Architecture Overview

```
claude-skills-sdk/
├── skill-package/              # Upload to Claude (read-only)
│   ├── SKILL.md               # Main skill definition
│   ├── config/                # Configuration
│   ├── scripts/               # Python utilities (storage.py)
│   ├── modules/               # Optional skill modules
│   ├── examples/              # Example skills
│   └── user-data-templates/   # Templates to copy to user-data/
│       ├── config/            # Configuration templates
│       ├── db/                # Database directory
│       └── logs/              # Logs directory
│
├── user-data/                 # Your data (created from templates)
│   ├── config/                # Your configuration
│   ├── db/                    # Your database
│   └── logs/                  # Your logs
│
├── docs/                      # Documentation
│   ├── skill-developers/      # For skill developers
│   │   ├── getting-started/   # New user onboarding
│   │   ├── guides/            # Development guides
│   │   └── user-guide/        # Usage documentation
│   ├── sdk-developers/        # For SDK contributors
│   │   └── architecture/      # Architecture docs
│   ├── shared/                # Shared resources
│   │   ├── CHANGELOG.md       # Version history
│   │   ├── DOCUMENTATION_STRUCTURE.md
│   │   └── resources/         # SDK materials
│   └── archives/              # Historical files
│
├── developer-tools/           # Automation scripts (run from repo root)
│   ├── validate.py            # Validate structure
│   ├── setup.sh               # Initial setup
│   ├── setup-storage.sh       # Setup storage
│   └── integrate-skill-creator.sh  # Integrate skill-creator
│
├── sdk/                       # SDK infrastructure
│   ├── .github/workflows/     # CI/CD workflows
│   ├── config/                # Configuration files
│   └── scripts/
│       └── release.sh         # Create releases
│
└── [Root Documentation]
    ├── README.md (this file)
    ├── CONTRIBUTING.md
    └── LICENSE
```

---

## 🚀 Manual Quick Start

**If you prefer written instructions over interactive onboarding:**

```bash
# 1. Clone the template
git clone https://github.com/yourusername/claude-skills-sdk.git
cd claude-skills-sdk

# 2. Set up user data
cp -r skill-package/user-data-templates user-data
cd user-data/config
cp storage-config-template.yaml storage-config.yaml

# 3. Configure storage backend
# Edit storage-config.yaml:
#   - Choose backend: local, github, checkpoint, email, or notion
#   - Set paths/credentials

# 4. Validate
cd ../..
python developer-tools/validate.py

# 5. (Optional) Integrate skill-creator
chmod +x developer-tools/integrate-skill-creator.sh
./developer-tools/integrate-skill-creator.sh

# 6. Upload skill-package/ to Claude Desktop
```

**Full details:** See [QUICK_SETUP.md](docs/skill-developers/getting-started/QUICK_SETUP.md)

---

## 💾 Storage Backend Options

| Backend | Persistence | Multi-Device | Setup | Best For |
|---------|-------------|--------------|-------|----------|
| **Local** | ✅ | ❌ | Easy | Single device, simplicity |
| **GitHub** | ✅ | ✅ | Medium | Teams, version control |
| **Checkpoint** | ❌ | ❌ | None | Testing, temporary |
| **Email** | ✅ | ✅ | Medium | Email-based workflows |
| **Notion** | ✅ | ✅ | Medium | Structured data, dashboards |

**Complete guide:** [DEPENDENCIES.md](docs/skill-developers/getting-started/DEPENDENCIES.md)

---

## 🛠️ Essential Commands

```bash
# Validate skill structure
python developer-tools/validate.py

# Create a release
./sdk/scripts/release.sh 1.1.0

# Integrate official skill-creator
./developer-tools/integrate-skill-creator.sh

# Setup storage backend
./developer-tools/setup-storage.sh
```

---

## 📖 Key Documentation

### Getting Started
- **[WELCOME.md](docs/skill-developers/getting-started/WELCOME.md)** - Warm welcome & quick overview
- **[QUICK_SETUP.md](docs/skill-developers/getting-started/QUICK_SETUP.md)** - 5-minute setup guide
- **[CLAUDE_ONBOARDING_GUIDE.md](docs/skill-developers/getting-started/CLAUDE_ONBOARDING_GUIDE.md)** - Interactive onboarding (for Claude)
- **[DEPENDENCIES.md](docs/skill-developers/getting-started/DEPENDENCIES.md)** - All 5 storage backends explained

### User Guide
- **[Setup Guide](docs/skill-developers/user-guide/setup.md)** - Detailed configuration
- **[Documentation Hub](docs/shared/DOCUMENTATION_STRUCTURE.md)** - Complete navigation

### Developer Guide
- **[Architecture](docs/skill-developers/guides/architecture.md)** - System design
- **[Storage Selection](docs/skill-developers/guides/storage-selection.md)** - Choose the right backend
- **[Testing Guide](docs/skill-developers/guides/testing-guide.md)** - Comprehensive testing
- **[Setup Scripts](docs/skill-developers/guides/setup-scripts.md)** - Automation tools

### Additional Resources
- **[SDK Design Docs](docs/sdk-developers/architecture/)** - Architecture decisions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines

---

## 🎓 Real-World Foundation

Based on **Israeli Tech Career Consultant** skill:
- 30+ production features
- v9.3.0+ releases
- Comprehensive documentation
- Token-optimized (5-35K per analysis)
- Battle-tested in real use

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Ways to help:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve docs
- 🔧 Submit PRs
- ⭐ Star the repo

---

## 📞 Support

**Questions?** Attach this repo to Claude and ask!

**Resources:**
- 📖 [Documentation](docs/)
- 🐛 [GitHub Issues](https://github.com/yourusername/claude-skills-sdk/issues)
- 💬 [Discussions](https://github.com/yourusername/claude-skills-sdk/discussions)

---

## 🗺️ Roadmap

**v1.1** (Current)
- ✅ Multi-backend storage
- ✅ Interactive onboarding
- ✅ Official skill-creator integration
- ✅ Production automation

**v1.2** (Next)
- [ ] More example skills
- [ ] Video tutorials
- [ ] Advanced testing framework

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

**Ready to build?**

👉 **New users:** See [WELCOME.md](docs/skill-developers/getting-started/WELCOME.md) or say "hi" to Claude with this repo attached!

👉 **Experienced:** Check [QUICK_SETUP.md](docs/skill-developers/getting-started/QUICK_SETUP.md) for fast track

👉 **Full docs:** Visit [Documentation Hub](docs/shared/DOCUMENTATION_STRUCTURE.md) for complete navigation

---

*Built with ❤️ for the Claude developer community*

**Last Updated:** 2025-11-04 | **v1.1.0**
