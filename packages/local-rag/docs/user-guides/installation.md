# Installation Guide

Complete guide to installing and setting up Local RAG (no virtualenv needed) on your system.

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
sudo apt install -y poppler-utils libmagic1 python3.11
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
git clone https://github.com/gsannikov/claude-skills.git

# Navigate to directory
cd claude-skills
```

---

### 3. Install Local RAG (no virtualenv needed)

```bash
cd packages/local-rag
python3.11 -m pip install --user .

# If you want isolation without managing a venv yourself:
# pipx install .
# or
# uv pip install --user .
```

---

### 4. Verify installation

```bash
local-rag --version
local-rag index --help
```

**Note**: The first call downloads embedding models (~100MB) on demand.

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

Local RAG now ships as an installable CLI. If you want Claude Desktop to call it directly, point to the `local-rag` binary installed above (or `python -m local_rag.cli`). No embedded `mcp_server.py` is required in this package.

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

### Environment Issues

**Problem**: Old virtual environment is still active or conflicting packages

**Solution**:
```bash
# Deactivate any old venv first
deactivate 2>/dev/null || true

# Reinstall locally without a venv
cd packages/local-rag
python3.11 -m pip install --user .
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
sudo chown -R $USER:$USER /path/to/claude-skills

# Or change ROOT_DIR to a directory you own
```

---

## Optional: OCR Engine Setup

By default, Local RAG uses PaddleOCR (CPU-friendly, multilingual). For better accuracy, you can install additional engines.

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

To completely remove Local RAG:

```bash
# 1. Remove from Claude Desktop config
#    Delete the "local-rag" entry from claude_desktop_config.json

# 2. Uninstall the package (user install)
python3.11 -m pip uninstall -y local-rag

# 3. Remove ChromaDB index and state (optional)
rm -rf ~/MyDrive/claude-skills-data/local-rag

# 4. Delete repository (optional)
cd ..
rm -rf claude-skills
```

---

## Update / Upgrade

To update to a new version:

```bash
# Pull latest changes
git pull origin main

# Reinstall the package
cd packages/local-rag
python3.11 -m pip install --user .

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
2. Search existing [GitHub Issues](https://github.com/gsannikov/claude-skills/issues)
3. Ask in [GitHub Discussions](https://github.com/gsannikov/claude-skills/discussions)
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
