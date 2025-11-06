# SDK Infrastructure

This folder contains infrastructure for maintaining and developing the Claude Skill Template itself.

**Audience:** SDK developers and template maintainers

## Contents

### `.github/`
GitHub Actions workflows for template validation and testing:
- `comprehensive-tests.yml` - 12 comprehensive tests
- `release.yml` - Release automation
- `validate.yml` - Validation workflow

### `config/`
SDK configuration files:
- `.gitleaks.toml` - Secrets scanning configuration
- `version.yaml` - Template version information

### `scripts/`
SDK maintenance scripts:
- `release.sh` - Create and publish template releases

## For SDK Developers

If you're maintaining the template infrastructure:

1. Read `../SDK_DEVELOPMENT.md` for development guidelines
2. Check `../docs/sdk-developers/` for architecture and design docs
3. Modify workflows in `.github/workflows/`
4. Update version in `config/version.yaml`
5. Use `scripts/release.sh` for releases

## Not an SDK Developer?

If you're building a skill using this template:
- **Go back to the main README.md** - that's for you!
- Use `../developer-tools/` for skill development tools
- Read `../docs/skill-developers/` for skill development guides

---

**Layer:** 1 (SDK Development)
**Purpose:** Template infrastructure maintenance
