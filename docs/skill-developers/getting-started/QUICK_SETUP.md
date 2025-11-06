# Quick Setup Guide
**Get running in 2 minutes with automatic setup**

---

## 🚀 Automated Setup (Recommended)

### One-Time Setup
```bash
# 1. Extract the downloaded package
unzip skill-package-vX.Y.Z.zip
cd skill-package-vX.Y.Z

# 2. Run auto-setup
chmod +x developer-tools/setup-storage.sh
./developer-tools/setup-storage.sh

# 3. Restart Claude Desktop
# macOS: Cmd+Q, then reopen
# Linux: Close completely, then reopen

# 4. Upload skill-package/ to Claude
# Done! ✅
```

**Time:** 2 minutes  
**What it does:**
- ✅ Creates user-data/ from templates
- ✅ Updates paths.py automatically
- ✅ Configures MCP Filesystem
- ✅ Ready to use

---

## 📝 Manual Setup (If script doesn't work)

### Step 1: Create User Data
```bash
cp -r skill-package/user-data-templates user-data
```

### Step 2: Update Paths
Edit `skill-package/config/paths.py`:
```python
USER_DATA_BASE = "/full/path/to/your/user-data"
```

### Step 3: Configure MCP
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/full/path/to/your/user-data"
      ]
    }
  }
}
```

### Step 4: Restart Claude
Completely quit and reopen Claude Desktop

### Step 5: Upload Skill
Upload the `skill-package/` directory to Claude

---

## ⚠️ Why Local Filesystem?

**For skills using markdown/YAML/CSV, local filesystem is the ONLY good option:**

✅ Native file format support  
✅ Fast read/write  
✅ Git-friendly  
✅ Text editors work  
✅ No conversion issues  
✅ Works offline  

**Other options DON'T work well:**
- ❌ Session-only: Data lost after conversation
- ❌ Google Drive: Poor support for raw text files, converts formats

---

## 🔍 Verify Setup

```
You: "Test the skill setup"

Claude: [Should access user-data/ and confirm working]
```

If errors, check:
1. MCP Filesystem is in Claude settings
2. Path in paths.py matches actual location
3. Claude was restarted after config change

---

## 📊 What Gets Stored

```
user-data/
├── config/
│   └── user-config.yaml    # Your settings
├── db/
│   └── *.yaml              # Skill data
└── logs/
    └── *.log               # Operation logs
```

All data stays on your machine - private and local.

---

**Setup issues?** See [user guide](../user-guide/setup.md) or ask Claude for help!
