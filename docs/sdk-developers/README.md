# SDK Developer Documentation

This documentation is for developers maintaining the Claude Skill Template infrastructure.

**Audience:** Template maintainers and core contributors (Layer 1)

## Quick Start for SDK Developers

1. Read `../../SDK_DEVELOPMENT.md` for development guidelines
2. Explore the architecture in `architecture/`
3. Check CI/CD workflows in `../../sdk/.github/workflows/`
4. Review design decisions in this folder

## Documentation Structure

### `architecture/`
System architecture and design documents:
- **SDK_DESIGN.md** - Overall SDK design philosophy
- **STORAGE_DESIGN.md** - Storage system architecture
- **GITHUB_STORAGE.md** - GitHub storage backend implementation details

### Coming Soon
- `contributing/` - Contribution guidelines for SDK development
- `design-decisions/` - Architecture Decision Records (ADRs)
- `testing/` - Test suite documentation

## SDK Development Workflow

### 1. Setup Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run validation
python developer-tools/validate.py
```

### 2. Make Changes
- Modify SDK infrastructure in `sdk/`
- Update documentation in `docs/sdk-developers/`
- Add tests in `sdk/.github/workflows/`

### 3. Test Changes
```bash
# Run local validation
python developer-tools/validate.py

# Test workflows locally (if using act or similar)
# Or create a test PR to run GitHub Actions
```

### 4. Update Version
```bash
# Update version in sdk/config/version.yaml
# Follow semantic versioning
```

### 5. Create Release
```bash
# Use release script
bash sdk/scripts/release.sh
```

## Key Files to Know

### CI/CD Workflows
- `../../sdk/.github/workflows/comprehensive-tests.yml` - 12 comprehensive tests
- `../../sdk/.github/workflows/release.yml` - Release automation
- `../../sdk/.github/workflows/validate.yml` - Validation workflow

### Configuration
- `../../sdk/config/version.yaml` - Template version
- `../../sdk/config/.gitleaks.toml` - Secrets scanning rules

### Scripts
- `../../sdk/scripts/release.sh` - Release automation
- `../../developer-tools/validate.py` - Validation script (shared with skill devs)

## Architecture Overview

The template follows a **three-layer architecture**:

1. **Layer 1 (SDK)** - Template infrastructure (you're here!)
   - Location: `sdk/`, `docs/sdk-developers/`
   - Purpose: Maintain template, CI/CD, releases

2. **Layer 2 (Skill Development)** - Tools for building skills
   - Location: `developer-tools/`, `docs/skill-developers/`
   - Purpose: Provide tools for skill developers

3. **Layer 3 (Skill Package)** - The skill itself
   - Location: `skill-package/`
   - Purpose: Code that runs in Claude Desktop

See `architecture/SDK_DESIGN.md` for detailed architecture.

## Testing Philosophy

All changes should maintain:
- ✅ 12 comprehensive tests passing
- ✅ Backward compatibility (or clear migration path)
- ✅ Documentation updated
- ✅ No breaking changes without version bump

## Release Process

1. Update `sdk/config/version.yaml`
2. Update `docs/shared/CHANGELOG.md`
3. Run `bash sdk/scripts/release.sh`
4. Create GitHub release with notes
5. Announce breaking changes if any

See `sdk/scripts/release.sh` for automation.

## Design Principles

### 1. Clear Layer Separation
- SDK infrastructure in `sdk/`
- Skill development tools in `developer-tools/`
- Skill package in `skill-package/`

### 2. Self-Documenting
- Every major folder has README.md
- Layer annotations in docs
- Clear ownership in folder names

### 3. Developer Experience
- Quick setup for skill developers
- Comprehensive docs for all audiences
- Automated validation and testing

See `architecture/SDK_DESIGN.md` for full design philosophy.

## Contributing to SDK

### Code Standards
- Follow existing patterns
- Add tests for new features
- Update documentation
- Maintain backward compatibility

### Pull Request Process
1. Create feature branch
2. Make changes
3. Update tests and docs
4. Create PR (CI runs automatically)
5. Address review feedback
6. Merge to main

### Areas for Contribution
- New storage backends
- Improved validation scripts
- Better testing tools
- Enhanced CI/CD workflows
- Documentation improvements

## Need Help?

- **Architecture questions?** See `architecture/SDK_DESIGN.md`
- **Storage design?** See `architecture/STORAGE_DESIGN.md`
- **General questions?** Check `../../CONTRIBUTING.md`

## Other Documentation

- **Skill Developers:** See `../skill-developers/` for skill development guides
- **Shared Resources:** See `../shared/` for changelog and general docs

---

**Layer:** 1 (SDK Development)
**Last Updated:** 2025-11-06
