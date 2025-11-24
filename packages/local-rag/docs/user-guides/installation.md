# Installation Guide

Complete guide to installing and setting up 2ndBrain_RAG on your system.

---

## System Requirements

### Minimum Requirements

- **Operating System**: macOS 12+ (Apple Silicon), Linux (Ubuntu 20.04+), or Windows 11
- **CPU**: Multi-core processor (Apple M1/M2/M3 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for software + storage for documents
- **Python**: 3.11 or higher

### Recommended Setup

- **OS**: macOS 13+ on Apple Silicon (M1/M2/M3)
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Disk**: SSD with 10GB+ free space
- **Python**: 3.11 or 3.12

---

## Installation Steps

### 1. Prerequisites

#### Install Homebrew (macOS/Linux)

```bash
# Check if already installed
brew --version

# If not, install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install System Dependencies

**macOS**:
```bash
brew install poppler libmagic
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install -y poppler-utils libmagic1 python3.11 python3.11-venv
```

**Windows**:
- Download and install [Python 3.11+](https://www.python.org/downloads/)
- Download [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
- Add poppler to PATH

#### Verify Python Version

```bash
python3 --version
# Should show 3.11.0 or higher
```

---

### 2. Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/2ndBrain_RAG.git

# Navigate to directory
cd 2ndBrain_RAG
```

---

### 3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Verify activation (should show (.venv) in prompt)
```

---

### 4. Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# This will install:
# - MCP SDK
# - ChromaDB
# - sentence-transformers
# - watchdog
# - OCR libraries (Surya, optionally PaddleOCR)
# - Document processing libraries (pypdf, python-docx, etc.)
```

**Note**: Initial installation downloads embedding models (~100MB). This is a one-time download.

---

### 5. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

**Required Configuration**:

```bash
# Path to your documents folder
ROOT_DIR=/path/to/your/documents

# File extensions to index (comma-separated)
ALLOWED_EXTS=.pdf,.txt,.md,.docx

# Chunking parameters
CHUNK_SIZE=3000
CHUNK_OVERLAP=400

# ChromaDB storage path
PERSIST_DIR=.chromadb

# Embedding model
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Example Configuration**:

```bash
# Index all documents in your Documents folder
ROOT_DIR=/Users/yourname/Documents/MyKnowledgeBase

# Support common document types
ALLOWED_EXTS=.pdf,.txt,.md,.docx,.pptx,.xlsx

# Default chunking (good for most use cases)
CHUNK_SIZE=3000
CHUNK_OVERLAP=400
```

---

### 6. Test Installation

```bash
# Test basic functionality
python -c "import mcp; import chromadb; import sentence_transformers; print('All dependencies OK')"

# Should print: "All dependencies OK"
```

---

### 7. Configure Claude Desktop

#### Find Claude Desktop Config File

**macOS**:
```bash
~/.config/claude/claude_desktop_config.json
```

**Linux**:
```bash
~/.config/claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### Add MCP Server Configuration

Edit the config file and add:

```json
{
  "mcpServers": {
    "local-rag": {
      "command": "python",
      "args": ["-u", "/absolute/path/to/2ndBrain_RAG/mcp_server.py"],
      "cwd": "/absolute/path/to/2ndBrain_RAG",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/2ndBrain_RAG` with your actual path.

**Example**:
```json
{
  "mcpServers": {
    "local-rag": {
      "command": "python",
      "args": ["-u", "/Users/john/projects/2ndBrain_RAG/mcp_server.py"],
      "cwd": "/Users/john/projects/2ndBrain_RAG",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

---

### 8. Restart Claude Desktop

1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Verify MCP server is connected (should see no errors)

---

### 9. Verify Installation in Claude

Open Claude Desktop and try:

```
Can you check the status of my RAG index?
```

Claude should use the `rag.stats` tool and show index statistics.

---

## Troubleshooting Installation

### Python Version Issues

**Problem**: `command not found: python3.11`

**Solution**:
```bash
# macOS with Homebrew
brew install python@3.11

# Linux
sudo apt install python3.11

# Verify
python3.11 --version
```

---

### Virtual Environment Issues

**Problem**: Cannot activate virtual environment

**Solution**:
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
```

---

### Dependency Installation Failures

**Problem**: `pip install` fails with errors

**Solution**:
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Try installing again
pip install -r requirements.txt

# If specific package fails, try individually
pip install chromadb
pip install sentence-transformers
# etc.
```

---

### poppler Not Found

**Problem**: `pdf2image requires poppler`

**Solution**:
```bash
# macOS
brew install poppler

# Linux
sudo apt install poppler-utils

# Windows: Download and add to PATH
# https://github.com/oschwartz10612/poppler-windows/releases/
```

---

### Claude Desktop Not Finding MCP Server

**Problem**: MCP server doesn't appear in Claude

**Checklist**:
1. Is path absolute (not relative)?
2. Does `mcp_server.py` exist at that path?
3. Is `.env` file configured?
4. Did you restart Claude Desktop?
5. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Linux: `~/.local/share/Claude/logs/`
   - Windows: `%LOCALAPPDATA%\Claude\logs\`

---

### Permission Errors

**Problem**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Make sure you own the directory
sudo chown -R $USER:$USER /path/to/2ndBrain_RAG

# Or change ROOT_DIR to a directory you own
```

---

## Optional: OCR Engine Setup

By default, 2ndBrain_RAG uses Surya OCR (CPU-friendly). For better accuracy, you can install additional engines.

### PaddleOCR (Balanced)

```bash
pip install paddlepaddle paddleocr
```

### DeepSeek-OCR (High Accuracy)

See [OCR guide](ocr-setup.md) for detailed instructions.

---

## Next Steps

After successful installation:

1. **Add documents**: Copy documents to your `ROOT_DIR`
2. **Initial indexing**: See [Usage Guide](usage.md)
3. **Test search**: Try searching in Claude
4. **Configure**: Tune settings in `.env` if needed

---

## Uninstallation

To completely remove 2ndBrain_RAG:

```bash
# 1. Remove from Claude Desktop config
#    Delete the "local-rag" entry from claude_desktop_config.json

# 2. Remove virtual environment
cd /path/to/2ndBrain_RAG
rm -rf .venv

# 3. Remove ChromaDB index (optional)
rm -rf .chromadb

# 4. Remove state files (optional)
rm -rf state/

# 5. Delete repository (optional)
cd ..
rm -rf 2ndBrain_RAG
```

---

## Update / Upgrade

To update to a new version:

```bash
# Pull latest changes
git pull origin main

# Activate virtual environment
source .venv/bin/activate

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart Claude Desktop
```

**Note**: Check [changelog.md](../changelog.md) for breaking changes and migration steps.

---

## Platform-Specific Notes

### macOS (Apple Silicon)

- **Best performance**: Optimized for M1/M2/M3 chips
- **MPS acceleration**: Automatic for compatible operations
- **Rosetta**: Not needed, runs natively on ARM64

### Linux

- **Tested on**: Ubuntu 22.04, Debian 11
- **Other distros**: Should work but untested
- **Wayland**: Fully supported

### Windows

- **Status**: Experimental support
- **Known issues**: Path handling, some dependencies
- **Recommendation**: Use WSL2 for best experience

---

## Getting Help

If you're stuck:

1. Check [Troubleshooting Guide](troubleshooting.md)
2. Search existing [GitHub Issues](https://github.com/yourusername/2ndBrain_RAG/issues)
3. Ask in [GitHub Discussions](https://github.com/yourusername/2ndBrain_RAG/discussions)
4. Open a new issue with:
   - Your OS and Python version
   - Error messages (full text)
   - Steps you've already tried

---

## FAQ

**Q: Do I need a GPU?**
A: No, everything runs on CPU. GPU can speed up embeddings but is optional.

**Q: How much disk space do I need?**
A: ~2GB for software + ~1MB per 1000 document chunks indexed.

**Q: Can I use this without Claude Desktop?**
A: Not currently. The MCP protocol requires a compatible client.

**Q: Does this work offline?**
A: Yes, after initial model downloads, everything runs offline.

**Q: How do I change the documents folder after setup?**
A: Edit `ROOT_DIR` in `.env`, then restart the MCP server (restart Claude Desktop).

---

**Installation complete!**

Next: Read the [Usage Guide](usage.md) to start searching your documents.

---

**Last Updated**: 2025-11-13
**Applies to**: v0.2.0+
