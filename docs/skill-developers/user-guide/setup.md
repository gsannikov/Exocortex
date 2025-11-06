# Setup Guide

Complete guide to setting up your skill for the first time.

## Prerequisites

**Required:**
- macOS 14+ or Linux
- Claude Desktop with MCP support  
- Python 3.8+
- Git

**Optional:**
- GitHub account (for version control)
- Text editor (VS Code recommended)

---

## Installation Steps

### 1. Get the Skill

**Option A: Clone from GitHub**
```bash
git clone https://github.com/yourusername/your-skill.git
cd your-skill
```

**Option B: Download Release ZIP**
1. Download from GitHub Releases
2. Extract to your preferred location
3. Open terminal in that directory

### 2. Configure File Paths

Edit `skill-package/config/paths.py`:

```python
# Before (template):
USER_DATA_BASE = "/path/to/user-data"

# After (your system):
USER_DATA_BASE = "/Users/yourusername/your-skill/user-data"
```

**Important:** Use absolute paths, not relative paths.

### 3. Configure MCP Servers

Add to Claude Desktop config:

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourusername/your-skill/user-data"
      ]
    }
  }
}
```

**Important:** Replace `/Users/yourusername/your-skill/user-data` with your actual path.

### 4. Restart Claude Desktop

**Mac:** Cmd+Q, then reopen  
**Linux:** Close and reopen

Verify MCP connection in Claude Desktop settings.

### 5. Upload Skill to Claude

1. Open Claude Desktop
2. Start a new conversation  
3. Click attachment icon or drag-and-drop
4. Upload the entire `skill-package/` directory

**All files in skill-package will be uploaded:**
- SKILL.md
- config/
- modules/
- scripts/

### 6. Initialize User Configuration

```bash
# Copy template to active config
cp user-data/config/user-config-template.yaml user-data/config/user-config.yaml

# Edit with your settings
nano user-data/config/user-config.yaml
# or use your preferred editor
```

Fill in your personal settings.

---

## Verification

Test that everything works:

```
You: "Test the skill setup"
Claude: [Should load skill and respond with success message]
```

If you see errors, proceed to troubleshooting.

---

## Troubleshooting

### Skill won't load
- Check all files are in skill-package/
- Verify SKILL.md has no syntax errors
- Try uploading files individually

### MCP connection fails
- Verify config path is correct
- Check file permissions on user-data/
- Restart Claude Desktop
- Check Claude Desktop logs

### Path errors
- Use absolute paths, not relative
- Check for typos in paths
- Verify directories exist

---

## Next Steps

1. Read [usage.md](usage.md) to learn how to use the skill
2. Customize user-config.yaml for your needs
3. Start using the features!

---

*Setup time: ~5-10 minutes*  
*Need help? See [troubleshooting.md](troubleshooting.md)*
