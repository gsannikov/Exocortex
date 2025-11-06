# Contributing to Claude Skills SDK

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. **Check existing issues** to avoid duplicates
2. **Verify** the bug exists in the latest version
3. **Collect information** about your environment

Use the **Bug Report** issue template and provide:
- Clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- Error messages and logs
- Environment details (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Use the **Feature Request** issue template and include:
- Clear description of the feature
- Use cases and benefits
- Implementation ideas (optional)
- Willingness to contribute

### Submitting Pull Requests

1. **Fork** the repository
2. **Create a branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit** with clear messages
   ```bash
   git commit -m "feat: add amazing feature"
   ```
6. **Push** to your fork
7. **Submit a pull request** using the PR template

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Claude Desktop (for testing)

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/claude-skill-template.git
   cd claude-skill-template
   ```

2. Run setup:
   ```bash
   ./developer-tools/setup.sh
   ```

3. Install Python dependencies:
   ```bash
   pip3 install pyyaml
   ```

4. Configure paths:
   - Edit `skill-package/config/paths.py`
   - Set your local directories

## Development Workflow

### Testing Your Changes

1. **Run validation**:
   ```bash
   python3 developer-tools/validate.py
   ```

2. **Test in Claude**:
   - Upload `skill-package/` to Claude Desktop
   - Test your changes interactively
   - Document any issues

3. **Check YAML syntax**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"
   ```

### Code Style

- **Python**: Follow PEP 8
- **Markdown**: Use consistent formatting
- **YAML**: 2-space indentation
- **Comments**: Clear and concise

### Commit Messages

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions/updates
- `chore:` - Maintenance tasks

Examples:
```
feat: add validation for user config
fix: resolve path handling on Windows
docs: update setup instructions
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Validation passes (`validate.py`)
- [ ] No new warnings

### Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, maintainer will merge
4. Your contribution will be credited in release notes

### Merging Criteria

- All tests pass
- Code review approved
- Documentation complete
- No merge conflicts
- Follows contribution guidelines

## Documentation

### What to Document

- New features
- API changes
- Configuration options
- Breaking changes
- Migration guides

### Where to Document

- **README.md**: Overview and quick start
- **docs/skill-developers/guides/**: Detailed guides
- **Code comments**: Complex logic
- **docs/shared/CHANGELOG.md**: Version history

## Testing Guidelines

### Test Coverage

- Test happy path
- Test edge cases
- Test error conditions
- Test different configurations

### Manual Testing

1. Test in Claude Desktop
2. Try different user scenarios
3. Verify documentation accuracy
4. Check all file paths work

## Release Process

Maintainers handle releases:

1. Update version in `version.yaml`
2. Update `docs/shared/CHANGELOG.md`
3. Run `./sdk/scripts/release.sh <version>`
4. Push changes and tags
5. GitHub Actions creates release

## Community

### Getting Help

- **GitHub Issues**: For bugs and features
- **GitHub Discussions**: For questions and ideas
- **Documentation**: Check docs/ first

### Recognition

Contributors are recognized in:
- Release notes
- CHANGELOG.md
- GitHub contributors page

Thank you for contributing! 🙏

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label

---

*Last updated: 2025-11-03*
