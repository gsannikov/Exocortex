# SDK Development Guide

**Welcome, SDK Developer!** This guide is for developers maintaining the Claude Skill Template infrastructure.

> ⚠️ **Are you building a skill?** You probably want [README.md](README.md) instead. This guide is for template maintainers only.

---

## What is SDK Development?

**SDK Development (Layer 1)** involves maintaining and improving the template infrastructure itself:

- 🔧 CI/CD workflows and GitHub Actions
- 📦 Release automation and versioning
- 🏗️ Template architecture and design
- 🧪 Validation and testing systems
- 📚 SDK documentation

**This is different from Skill Development (Layer 2)**, which involves using this template to build Claude skills.

---

## Quick Start for SDK Developers

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/gsannikov/claude-skill-template.git
cd claude-skill-template

# Install development dependencies
pip install -r requirements-dev.txt

# Run validation to ensure everything works
python developer-tools/validate.py
```

### 2. Understand the Structure

The repository has three distinct layers:

```
claude-skill-template/
├── sdk/                          # Layer 1: SDK infrastructure (YOU ARE HERE)
│   ├── .github/workflows/        # CI/CD for template validation
│   ├── config/                   # SDK configuration
│   └── scripts/                  # Release automation
│
├── developer-tools/              # Layer 2: Tools for skill developers
│   ├── validate.py
│   ├── setup.sh
│   └── ...
│
├── skill-package/                # Layer 3: The skill itself
│   └── ...
│
└── docs/
    ├── sdk-developers/           # YOUR DOCUMENTATION
    ├── skill-developers/         # For skill developers
    └── shared/                   # Shared resources
```

### 3. Read the Documentation

Start with these docs in `docs/sdk-developers/`:

1. **[architecture/SDK_DESIGN.md](docs/sdk-developers/architecture/SDK_DESIGN.md)** - Overall design philosophy
2. **[architecture/STORAGE_DESIGN.md](docs/sdk-developers/architecture/STORAGE_DESIGN.md)** - Storage system design
3. **[README.md](docs/sdk-developers/README.md)** - SDK developer documentation index

---

## SDK Development Workflow

### Making Changes

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Modify SDK infrastructure in `sdk/`
   - Update workflows in `sdk/.github/workflows/`
   - Add/update documentation in `docs/sdk-developers/`

3. **Test Locally**
   ```bash
   # Run validation
   python developer-tools/validate.py

   # Test specific workflows locally if possible
   # Or create a test PR to run GitHub Actions
   ```

4. **Update Documentation**
   - Update relevant docs in `docs/sdk-developers/`
   - Update `docs/shared/CHANGELOG.md`
   - Add comments to complex code

5. **Create Pull Request**
   - Push branch to GitHub
   - Create PR (CI runs automatically)
   - Address review feedback

### Release Process

When ready to release a new version:

1. **Update Version**
   ```bash
   # Edit sdk/config/version.yaml
   # Follow semantic versioning (MAJOR.MINOR.PATCH)
   ```

2. **Update Changelog**
   ```bash
   # Edit docs/shared/CHANGELOG.md
   # Document all changes, breaking changes, migration notes
   ```

3. **Run Release Script**
   ```bash
   bash sdk/scripts/release.sh
   ```

4. **Create GitHub Release**
   - Tag the commit
   - Write release notes
   - Announce breaking changes

---

## What Can I Work On?

### High-Priority Areas

1. **New Storage Backends**
   - Add support for new storage systems
   - See `skill-package/scripts/storage.py`
   - Update `docs/sdk-developers/architecture/STORAGE_DESIGN.md`

2. **Improved Validation**
   - Enhance `developer-tools/validate.py`
   - Add new checks to `sdk/.github/workflows/comprehensive-tests.yml`
   - Improve error messages

3. **Better Testing**
   - Add more comprehensive tests
   - Improve test coverage
   - Add integration tests

4. **CI/CD Improvements**
   - Optimize workflow performance
   - Add new automation
   - Improve error reporting

5. **Documentation**
   - Improve SDK architecture docs
   - Add tutorials for SDK development
   - Create contribution guides

### Current Issues

Check the GitHub Issues for:
- Bugs in template infrastructure
- Feature requests for the SDK
- Documentation improvements needed

---

## Key Files and Their Purpose

### SDK Infrastructure (`sdk/`)

| File | Purpose |
|------|---------|
| `sdk/.github/workflows/comprehensive-tests.yml` | 12 comprehensive tests for template validation |
| `sdk/.github/workflows/release.yml` | Automated release process |
| `sdk/.github/workflows/validate.yml` | Quick validation workflow |
| `sdk/config/version.yaml` | Template version number |
| `sdk/config/.gitleaks.toml` | Secrets scanning configuration |
| `sdk/scripts/release.sh` | Release automation script |

### Developer Tools (`developer-tools/`)

These tools are shared between SDK development and skill development:

| File | Purpose | Used By |
|------|---------|---------|
| `developer-tools/validate.py` | Validate structure and config | Both SDK & Skill devs |
| `developer-tools/setup.sh` | Initial project setup | Skill developers |
| `developer-tools/setup-storage.sh` | Configure storage backends | Skill developers |
| `developer-tools/integrate-skill-creator.sh` | Integration tools | Skill developers |

### Documentation (`docs/sdk-developers/`)

| File | Purpose |
|------|---------|
| `architecture/SDK_DESIGN.md` | Overall SDK design and philosophy |
| `architecture/STORAGE_DESIGN.md` | Storage system architecture |
| `architecture/GITHUB_STORAGE.md` | GitHub backend implementation |
| `README.md` | SDK developer documentation index |

---

## Architecture Principles

### 1. Three-Layer Separation

**Layer 1 (SDK)** - Template infrastructure
- Who: SDK developers and maintainers
- What: CI/CD, releases, template architecture
- Where: `sdk/`, `docs/sdk-developers/`

**Layer 2 (Skill Development)** - Tools for building skills
- Who: Developers building Claude skills
- What: Validation, setup, testing tools
- Where: `developer-tools/`, `docs/skill-developers/`

**Layer 3 (Skill Package)** - The skill itself
- Who: End users in Claude Desktop
- What: Skill code, storage abstraction
- Where: `skill-package/`

### 2. Self-Documenting Structure

- Every major folder has `README.md`
- Clear ownership through folder names
- Layer annotations in documentation
- Comprehensive inline comments

### 3. Developer Experience First

- Quick setup for skill developers
- Automated validation and testing
- Clear error messages
- Comprehensive documentation

See `docs/sdk-developers/architecture/SDK_DESIGN.md` for full architecture details.

---

## Testing Philosophy

All SDK changes should maintain:

✅ **12 Comprehensive Tests Passing**
- Python syntax and imports
- Shell script validation
- Markdown link checking
- Storage configuration tests
- Documentation completeness
- Security scanning
- Code linting
- And more...

✅ **Backward Compatibility**
- Don't break existing skills
- Provide migration guides for breaking changes
- Use semantic versioning

✅ **Documentation Updated**
- Update relevant SDK docs
- Update changelog
- Add inline comments

✅ **No Breaking Changes Without Version Bump**
- MAJOR version: Breaking changes
- MINOR version: New features, backward compatible
- PATCH version: Bug fixes only

---

## Common SDK Development Tasks

### Adding a New Storage Backend

1. Update `skill-package/scripts/storage.py`
2. Add backend class inheriting from `StorageBackend`
3. Implement required methods: `save()`, `load()`, `delete()`, `list_keys()`
4. Add configuration template to `skill-package/user-data-templates/config/`
5. Update validation in `developer-tools/validate.py`
6. Add tests in `sdk/.github/workflows/comprehensive-tests.yml`
7. Document in `docs/skill-developers/getting-started/DEPENDENCIES.md`
8. Update `docs/sdk-developers/architecture/STORAGE_DESIGN.md`

### Adding a New Test

1. Edit `sdk/.github/workflows/comprehensive-tests.yml`
2. Add new test section following existing pattern
3. Update test summary at the end
4. Document test in comments
5. Test locally or via PR

### Updating Documentation

1. Edit relevant files in `docs/sdk-developers/`
2. Update `docs/shared/CHANGELOG.md` if user-facing
3. Check all links work
4. Update last modified date

### Creating a Release

1. Update `sdk/config/version.yaml`
2. Update `docs/shared/CHANGELOG.md`
3. Run `bash sdk/scripts/release.sh`
4. Create GitHub release
5. Announce if breaking changes

---

## Contributing Guidelines

### Code Standards

- **Follow existing patterns** - Consistency matters
- **Add tests** - All new features need tests
- **Document thoroughly** - Both inline and in docs
- **Maintain compatibility** - Don't break existing skills

### Pull Request Checklist

Before creating a PR:

- [ ] Tests passing locally
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] No breaking changes (or version bump + migration guide)
- [ ] Code follows existing patterns
- [ ] All files have appropriate comments

### Review Process

1. Create PR (CI runs automatically)
2. Address any CI failures
3. Request review from maintainers
4. Address feedback
5. Merge when approved

---

## Getting Help

### Resources

- **Architecture docs:** `docs/sdk-developers/architecture/`
- **Design decisions:** Review past PRs and commits
- **General contributing:** `CONTRIBUTING.md`
- **Ask questions:** Open an issue or discussion

### Contact

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and ideas
- **Pull Requests:** For contributions

---

## Frequently Asked Questions

### Q: How is this different from skill development?

**A:** SDK development maintains the template infrastructure (CI/CD, releases, architecture). Skill development uses the template to build Claude skills. Most people are skill developers.

### Q: Can I modify both SDK and skill code?

**A:** Yes! But understand which layer you're working in. SDK changes affect all users of the template. Skill changes only affect your specific skill.

### Q: How do I test SDK changes?

**A:** Run `python developer-tools/validate.py` locally, then create a test PR to run full GitHub Actions workflows.

### Q: What's the release cadence?

**A:** No fixed schedule. We release when there are meaningful improvements or important bug fixes.

### Q: Can I add new developer tools?

**A:** Yes! Add to `developer-tools/` and document in `docs/skill-developers/`.

---

## Next Steps

1. ✅ Read `docs/sdk-developers/README.md`
2. ✅ Explore `docs/sdk-developers/architecture/`
3. ✅ Check open issues on GitHub
4. ✅ Make your first contribution!

---

**Layer:** 1 (SDK Development)
**Last Updated:** 2025-11-06
**For Skill Developers:** See [README.md](README.md)
