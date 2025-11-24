# Contributing to Israeli Tech Career Consultant

Thank you for your interest in contributing! This is a personal career tool, but contributions are welcome.

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 How to Contribute

### Reporting Issues

- Check existing issues first
- Provide clear description and steps to reproduce
- Include version information (from `version.yaml`)

### Suggesting Enhancements

- Open an issue with the enhancement label
- Describe the use case and benefits
- Consider backward compatibility

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Update documentation if needed
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## 📁 Project Structure

```
career-consultant.skill/
├── version.yaml              # Version management
├── LICENSE                   # MIT License
├── README.md                 # Main documentation
├── skill-package/            # Core skill files
│   ├── SKILL.md             # Main orchestrator
│   ├── modules/             # Analysis modules
│   ├── scripts/             # Helper scripts
│   ├── config/              # Configuration
│   └── templates/           # User templates
├── user-data/               # User-specific data (not in repo)
├── host_scripts/            # Host automation package (CLI commands)
└── docs/                    # Additional documentation
```

## 🎯 Development Guidelines

### Code Style

**Python**:
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings for functions
- Keep functions focused and small

**Markdown**:
- Use clear headers
- Include code examples
- Add emoji for visual clarity (optional)
- Keep line length reasonable

### Module Development

If adding new modules:

1. Place in `skill-package/modules/`
2. Follow existing module structure
3. Include YAML frontmatter if needed
4. Document token costs
5. Update SKILL.md to reference the module

### Testing

- Test with different CV configurations
- Verify Excel generation works
- Check token usage is reasonable
- Test error handling

### Documentation

- Update README.md for user-facing changes
- Update SKILL.md for workflow changes
- Add inline comments for complex logic
- Create examples when helpful

## 🔄 Version Management

When making changes:

1. Update `version.yaml` following semantic versioning
2. Run `python -m host_scripts update-version`
3. Commit version changes separately
4. Tag releases properly

See [docs/guides/developers-guide/release-process.md](docs/guides/developers-guide/release-process.md) for details.

## ✅ Pull Request Checklist

- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Version bumped if needed
- [ ] No breaking changes (or clearly documented)
- [ ] Tested with sample data
- [ ] Token usage is reasonable
- [ ] Backward compatible with existing user data

## 🚫 What Not to Contribute

- Personal CVs or job data
- API keys or credentials
- Company-specific modifications
- Breaking changes without discussion
- Large binary files

## 💡 Ideas for Contribution

- Additional scoring algorithms
- New module types
- Improved documentation
- Bug fixes
- Performance optimizations
- Better error handling
- Additional MCP tool integrations
- Excel enhancements
- Testing infrastructure

## 🆘 Getting Help

- Check existing documentation
- Review closed issues
- Open a discussion issue
- Be patient and respectful

## 📞 Contact

For questions or discussions:
- Open an issue
- Start a discussion on GitHub

Thank you for contributing! 🎉
