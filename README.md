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

Claude will read [CLAUDE_ONBOARDING_GUIDE.md](docs/getting-started/CLAUDE_ONBOARDING_GUIDE.md) and walk you through everything interactively!

**Also see:** [WELCOME.md](docs/getting-started/WELCOME.md) for quick intro

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
- [WELCOME.md](docs/getting-started/WELCOME.md) - Start here!
- [QUICK_SETUP.md](docs/getting-started/QUICK_SETUP.md) - Manual setup guide
- [CLAUDE_ONBOARDING_GUIDE.md](docs/getting-started/CLAUDE_ONBOARDING_GUIDE.md) - For Claude's reference

**Documentation:**
- [Documentation Hub](docs/README.md) - Complete navigation guide
- [DEPENDENCIES.md](docs/getting-started/DEPENDENCIES.md) - Storage backends & setup
- [User Guide](docs/user-guide/) - User guides and tutorials
- [Developer Guide](docs/developer-guide/) - Development documentation

**Resources:**
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [CHANGELOG.md](docs/CHANGELOG.md) - Version history
- [LICENSE](LICENSE) - MIT license

---

## 🏗️ Architecture Overview

```
claude-skills-sdk/
├── skill-package/          # Upload to Claude (read-only)
│   ├── SKILL.md           # Main skill definition
│   ├── config/            # Configuration
│   ├── scripts/           # Python utilities (storage.py)
│   ├── modules/           # Optional skill modules
│   └── examples/          # Example skills
│
├── user-data-templates/   # Copy to user-data/
│   ├── config/            # Configuration templates
│   ├── db/                # Database directory
│   └── logs/              # Logs directory
│
├── docs/                  # Documentation (see docs/README.md)
│   ├── getting-started/   # New user onboarding
│   ├── user-guide/        # Usage documentation
│   ├── developer-guide/   # Development docs
│   ├── design/            # Architecture decisions
│   ├── features/          # Feature planning
│   ├── resources/         # SDK materials
│   └── archives/          # Historical files
│
├── host_scripts/          # Automation scripts
│   ├── validate.py        # Validate structure
│   ├── release.sh         # Create releases
│   └── setup-storage.sh   # Setup storage
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
cp -r user-data-templates user-data
cd user-data/config
cp storage-config-template.yaml storage-config.yaml

# 3. Configure storage backend
# Edit storage-config.yaml:
#   - Choose backend: local, github, checkpoint, email, or notion
#   - Set paths/credentials

# 4. Validate
cd ../..
python host_scripts/validate.py

# 5. (Optional) Integrate skill-creator
chmod +x scripts/integrate-skill-creator.sh
./scripts/integrate-skill-creator.sh

# 6. Upload skill-package/ to Claude Desktop
```

**Full details:** See [QUICK_SETUP.md](docs/getting-started/QUICK_SETUP.md)

---

## 💾 Storage Backend Options

| Backend | Persistence | Multi-Device | Setup | Best For |
|---------|-------------|--------------|-------|----------|
| **Local** | ✅ | ❌ | Easy | Single device, simplicity |
| **GitHub** | ✅ | ✅ | Medium | Teams, version control |
| **Checkpoint** | ❌ | ❌ | None | Testing, temporary |
| **Email** | ✅ | ✅ | Medium | Email-based workflows |
| **Notion** | ✅ | ✅ | Medium | Structured data, dashboards |

**Complete guide:** [DEPENDENCIES.md](docs/getting-started/DEPENDENCIES.md)

---

## 🛠️ Essential Commands

```bash
# Validate skill structure
python host_scripts/validate.py

# Create a release
./host_scripts/release.sh 1.1.0

# Integrate official skill-creator
./scripts/integrate-skill-creator.sh

# Setup storage backend
./scripts/setup-storage.sh
```

---

## 📖 Key Documentation

### Getting Started
- **[WELCOME.md](docs/getting-started/WELCOME.md)** - Warm welcome & quick overview
- **[QUICK_SETUP.md](docs/getting-started/QUICK_SETUP.md)** - 5-minute setup guide
- **[CLAUDE_ONBOARDING_GUIDE.md](docs/getting-started/CLAUDE_ONBOARDING_GUIDE.md)** - Interactive onboarding (for Claude)
- **[DEPENDENCIES.md](docs/getting-started/DEPENDENCIES.md)** - All 5 storage backends explained

### User Guide
- **[Setup Guide](docs/user-guide/setup.md)** - Detailed configuration
- **[Documentation Hub](docs/README.md)** - Complete navigation

### Developer Guide
- **[Architecture](docs/developer-guide/architecture.md)** - System design
- **[Storage Selection](docs/developer-guide/storage-selection.md)** - Choose the right backend
- **[Testing Guide](docs/developer-guide/testing-guide.md)** - Comprehensive testing
- **[Setup Scripts](docs/developer-guide/setup-scripts.md)** - Automation tools

### Additional Resources
- **[Design Docs](docs/design/)** - Architecture decisions
- **[Features & Roadmap](docs/features/)** - Planning and future direction
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

👉 **New users:** See [WELCOME.md](docs/getting-started/WELCOME.md) or say "hi" to Claude with this repo attached!

👉 **Experienced:** Check [QUICK_SETUP.md](docs/getting-started/QUICK_SETUP.md) for fast track

👉 **Full docs:** Visit [Documentation Hub](docs/README.md) for complete navigation

---

*Built with ❤️ for the Claude developer community*

**Last Updated:** 2025-11-04 | **v1.1.0**
