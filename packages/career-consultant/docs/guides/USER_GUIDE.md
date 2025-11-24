# User Guide

Complete guide for using the Israeli Tech Career Consultant skill.

## Table of Contents
1. [Quick Reference](#quick-reference)
2. [Getting Started](#getting-started)
3. [MCP Server Setup](#mcp-server-setup)
4. [Usage Examples](#usage-examples)
5. [Troubleshooting](#troubleshooting)

---

## Quick Reference

| Command | Purpose | Token Cost |
|---------|---------|------------|
| `Add to backlog: [URL]` | Quick save job | ~5K |
| `Batch add: [URLs]` | Save multiple jobs | ~5K each |
| `Show backlog` | View saved jobs | Minimal |
| `Analyze: [URL]` | Full job analysis | ~25-35K |
| `Analyze job [id]` | Analyze from backlog | ~25-35K |

---

## Getting Started

### First Time Setup

1. **Initialize Configuration**:
```
Load my configuration from: /Users/yourname/career-consultant/user-data
```

Claude will verify:
- ✅ Configuration file loaded
- ✅ CV variants found
- ✅ Directories accessible

2. **Test with a Job**:
```
Add to backlog: https://linkedin.com/jobs/view/12345
```

3. **Review and Analyze**:
```
Show my backlog
Analyze job [job-id]
```

---

## MCP Server Setup

### Required MCP Servers

#### 1. Filesystem MCP ⚡ REQUIRED

**Purpose**: Access your local file system for reading/writing job analyses.

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Configuration** in `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/user-data"]
    }
  }
}
```

#### 2. Firecrawl MCP ⭐ RECOMMENDED

**Purpose**: Web scraping for company research and job postings.

**Installation**:
```bash
npm install -g @mendable/firecrawl-mcp
```

**Get API key**: https://firecrawl.dev

#### 3. MCP_DOCKER (for LinkedIn) 🔧 OPTIONAL

**Purpose**: LinkedIn company page scraping.

**Setup**: See [MCP_DOCKER documentation](https://github.com/example/mcp-docker)

#### 4. Bright Data MCP 💰 PREMIUM

**Purpose**: Alternative for LinkedIn scraping (paid).

**Setup**: Requires Bright Data subscription.

---

## Usage Examples

### Backlog Mode (Quick Capture)

**Single job**:
```
Add to backlog: https://linkedin.com/jobs/view/12345
```

**With priority**:
```
Add high priority: https://linkedin.com/jobs/view/12345
```

**Batch processing**:
```
Batch add these jobs:
- https://linkedin.com/jobs/view/12345
- https://linkedin.com/jobs/view/67890
- https://www.google.com/careers/job/123
```

### Analysis Mode

**Basic analysis**:
```
Analyze this job: https://linkedin.com/jobs/view/12345
```

**From backlog**:
```
Analyze job nvidia-senior-tpm-20251029
```

**Batch analyze**:
```
Analyze top 5 jobs from backlog
```

### Company Research

**Manual research**:
```
Research: Microsoft Israel
```

**Update profile**:
```
Update Google Israel profile
```

### Results Management

**View rankings**:
```
Show my top 10 ranked jobs
List all First Priority jobs
```

**Filter by company**:
```
Show all Google jobs I've analyzed
```

### Best Practices

1. **Use Backlog First**: Save 50-100 jobs before analyzing (token efficient)
2. **Research Companies Strategically**: Research once per company, start new conversation
3. **Analyze in Batches**: Process 5-7 jobs per conversation
4. **Monitor Tokens**: Start new conversation at >60% usage

---

## Troubleshooting

### Configuration Issues

#### "User config not found"

**Solutions**:
- Check file exists: `ls user-data/profile/settings.yaml`
- Verify path in `paths.py`
- Recreate from template if needed

#### "CV not found"

**Solutions**:
- Check CVs exist: `ls user-data/profile/cvs/`
- Verify filenames match config
- Check file permissions: `chmod 644 user-data/profile/cvs/*.md`

### MCP Server Issues

#### "Filesystem tool not available"

**Solutions**:
1. Install: `npm install -g @modelcontextprotocol/server-filesystem`
2. Configure in Claude Desktop settings
3. Grant directory access
4. Restart Claude Desktop

#### "Firecrawl tool not available"

**Solutions**:
1. Install: `npm install -g @mendable/firecrawl-mcp`
2. Set API key: `export FIRECRAWL_API_KEY=your_key`
3. Check rate limits in dashboard
4. Use `web_fetch` as fallback

### Analysis Issues

#### "Company research hangs"

**Solutions**:
- Retry with different tool: `Research [Company] using web_fetch`
- Provide manual info
- Use shorter timeout

#### "Score calculation wrong"

**Solutions**:
- Verify weights sum to 100 in `settings.yaml`
- Check thresholds (first_priority, second_priority)
- Debug: `Show detailed scoring breakdown for role-id-123`

#### "Excel not syncing"

**Solutions**:
- Close Excel first
- Fix permissions: `chmod 644 user-data/db/db.xlsx`
- Rebuild: `Rebuild Excel database from all role files`

### Token Issues

#### "Token budget exceeded"

**Solutions**:
- Start new conversation after company research
- Use backlog mode for quick saves
- Reduce CV count temporarily

### Platform-Specific

**LinkedIn Jobs**: Use Bright Data or MCP_DOCKER

**Company Career Pages**: Use Firecrawl for better parsing

**Glassdoor**: Search manually if scraping fails

### Recovery Procedures

**Corrupted database**:
```bash
cp -r user-data/db user-data/db.backup
python user-data/scripts/dynamic_excel_generator.py
```

**Lost configuration**:
```bash
cp skill-package/templates/user-config-template.yaml user-data/profile/settings.yaml
```

**Missing files**:
```bash
mkdir -p user-data/{profile/cvs,companies,jobs,interviews,reports}
```

### Getting Help

**Before asking**:
1. Check this guide
2. Review documentation
3. Verify file structure
4. Test with minimal config

**Include when reporting issues**:
- Version from `version.yaml`
- Full error messages
- Steps to reproduce
- System info (OS, Python version)

**Resources**:
- [GitHub Issues](https://github.com/gsannikov/israeli-tech-career-consultant/issues)
- [Documentation](../../README.md)
