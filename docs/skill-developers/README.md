# Skill Developer Documentation

Welcome! This documentation is for developers building Claude skills using this template.

**Audience:** Skill developers (Layer 2)

## Quick Start

New to the template? Start here:

1. **[WELCOME.md](getting-started/WELCOME.md)** - Warm welcome and overview
2. **[QUICK_SETUP.md](getting-started/QUICK_SETUP.md)** - Get started in 5 minutes
3. **[CLAUDE_ONBOARDING_GUIDE.md](getting-started/CLAUDE_ONBOARDING_GUIDE.md)** - Interactive guide for Claude

## Documentation Structure

### `getting-started/`
Onboarding guides for new developers:
- **WELCOME.md** - Introduction and overview
- **QUICK_SETUP.md** - Quick setup guide
- **CLAUDE_ONBOARDING_GUIDE.md** - Step-by-step interactive guide
- **DEPENDENCIES.md** - Storage backends and dependencies

### `guides/`
How-to guides and references:
- **architecture.md** - System architecture overview
- **storage-selection.md** - Choosing the right storage backend
- **testing-guide.md** - Comprehensive testing strategies
- **testing-quick-reference.md** - Quick testing reference
- **setup-scripts.md** - Guide to automation scripts

### `user-guide/`
End-user documentation:
- **setup.md** - Setup instructions

## Common Tasks

### Setting Up Your Development Environment
```bash
# Run setup script
./developer-tools/setup.sh

# Configure storage
./developer-tools/setup-storage.sh
```

### Validating Your Skill
```bash
python developer-tools/validate.py
```

### Testing Your Skill
See [testing-guide.md](guides/testing-guide.md) for comprehensive testing strategies.

### Choosing a Storage Backend
See [storage-selection.md](guides/storage-selection.md) for a decision guide.

## Need Help?

- **Questions about the template?** Check [WELCOME.md](getting-started/WELCOME.md)
- **Setup issues?** See [QUICK_SETUP.md](getting-started/QUICK_SETUP.md)
- **Storage backend questions?** Read [DEPENDENCIES.md](getting-started/DEPENDENCIES.md)
- **Architecture questions?** See [guides/architecture.md](guides/architecture.md)

## Contributing

Found a bug or want to improve the template? See `../../CONTRIBUTING.md`

## Other Documentation

- **SDK Developers:** See `../sdk-developers/` if you're maintaining the template itself
- **Shared Resources:** See `../shared/` for changelog, resources, and general docs

---

**Layer:** 2 (Skill Development)
**Last Updated:** 2025-11-06
