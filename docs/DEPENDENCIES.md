# Dependencies by Backend

This document lists the required and optional dependencies for the Claude Skills SDK Template based on which storage backend you use.

## Core Requirements (Always Needed)

```bash
# Python version
Python 3.8 or higher

# Essential packages
pip install PyYAML>=6.0
```

**Why PyYAML?** Required for loading storage configuration files (`storage-config.yaml`).

---

## Backend-Specific Dependencies

### 1. Local Filesystem (Recommended)
**No additional dependencies required!**

The Local Filesystem backend uses MCP (Model Context Protocol) tools that are already available in Claude Desktop. This is the simplest option for single-user, single-device setups.

**Configuration:**
```yaml
storage:
  backend: local
  local:
    base_path: /Users/yourname/MyDrive/your-skill/user-data
```

---

### 2. GitHub Repository
**Required package:**
```bash
pip install PyGithub>=2.1.1
```

**Why?** Enables programmatic access to GitHub repositories for storing skill data across multiple devices.

**Configuration:**
```yaml
storage:
  backend: github
  github:
    repo: "username/skill-data"
    token: "ghp_your_token_here"
    branch: "main"
```

**Setup:**
1. Create a private GitHub repository
2. Generate a Personal Access Token (Settings → Developer settings → Personal access tokens)
3. Give token `repo` scope permissions
4. Add token to your configuration

---

### 3. Checkpoint System
**No additional dependencies required!**

Checkpoint backend stores data in memory during the session only. Perfect for testing or temporary use.

**Configuration:**
```yaml
storage:
  backend: checkpoint
```

**Note:** Data is lost when Claude session ends. Use `export_checkpoint()` to save data before closing.

---

### 4. Email Storage
**No additional dependencies required!**

Uses Python's built-in `imaplib` and `smtplib` libraries.

**Configuration:**
```yaml
storage:
  backend: email
  email:
    imap_server: "imap.gmail.com"
    smtp_server: "smtp.gmail.com"
    email: "your.email@gmail.com"
    password: "your_app_password"
    folder: "Claude/SkillData"
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate App Password (Google Account → Security → App passwords)
3. Use App Password in configuration (not your regular password)
4. Create folder in Gmail for organization

---

### 5. Notion Database
**Required package:**
```bash
pip install notion-client>=2.0.0
```

**Why?** Provides API access to Notion databases for structured data storage.

**Configuration:**
```yaml
storage:
  backend: notion
  notion:
    token: "secret_your_token_here"
    database_id: "your_database_id"
```

**Setup:**
1. Create a Notion integration (https://www.notion.so/my-integrations)
2. Create a database with these properties:
   - Name (Title)
   - Content (Text)
   - Updated (Date)
3. Share database with your integration
4. Get database ID from URL: notion.so/workspace/`<database_id>`?v=...

---

## Installation Quick Reference

### Minimal Setup (Local Filesystem)
```bash
pip install PyYAML
```

### Full Features (All Backends)
```bash
pip install PyYAML PyGithub notion-client
```

### Development Setup
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

---

## Dependency Matrix

| Backend | PyYAML | PyGithub | notion-client | Other |
|---------|--------|----------|---------------|-------|
| **Local** | ✅ | ❌ | ❌ | MCP tools |
| **GitHub** | ✅ | ✅ | ❌ | Git token |
| **Checkpoint** | ✅ | ❌ | ❌ | None |
| **Email** | ✅ | ❌ | ❌ | App password |
| **Notion** | ✅ | ❌ | ✅ | API token |

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"
```bash
pip install PyYAML
```

### "ModuleNotFoundError: No module named 'github'"
```bash
pip install PyGithub
```

### "ModuleNotFoundError: No module named 'notion_client'"
```bash
pip install notion-client
```

### Import errors persist after installation
```bash
# Check Python version
python --version  # Should be 3.8+

# Verify installation
pip list | grep -i yaml
pip list | grep -i github
pip list | grep -i notion

# Reinstall if needed
pip uninstall PyYAML PyGithub notion-client
pip install PyYAML PyGithub notion-client
```

### "PyYAML required for config file loading"
You're trying to use a YAML configuration file but PyYAML is not installed. Install it with:
```bash
pip install PyYAML
```

### "PyGithub not installed"
You selected GitHub backend but PyGithub is missing:
```bash
pip install PyGithub
```

### "notion-client not installed"
You selected Notion backend but notion-client is missing:
```bash
pip install notion-client
```

---

## Version Compatibility

| Package | Minimum Version | Tested Version | Notes |
|---------|----------------|----------------|-------|
| Python | 3.8 | 3.11 | Earlier versions not tested |
| PyYAML | 6.0 | 6.0.1 | Required for all backends |
| PyGithub | 2.1.1 | 2.1.1 | Optional - GitHub only |
| notion-client | 2.0.0 | 2.2.1 | Optional - Notion only |

---

## Security Notes

⚠️ **Never commit tokens or passwords to version control!**

- Use `.gitignore` to exclude `storage-config.yaml`
- Use environment variables for sensitive data
- Use `.env` files (excluded from git)
- Rotate tokens periodically

**Example using environment variables:**
```python
import os
github_token = os.getenv('GITHUB_TOKEN')
notion_token = os.getenv('NOTION_TOKEN')
```

---

## Getting Help

If you encounter dependency issues:

1. Check this document first
2. Verify Python version: `python --version`
3. Check installed packages: `pip list`
4. Try reinstalling: `pip install --upgrade PyYAML`
5. Create an issue on GitHub with:
   - Python version
   - Operating system
   - Full error message
   - Backend you're trying to use

---

**Last Updated:** 2025-11-04
**SDK Version:** 1.1.0
