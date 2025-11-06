# Setup Scripts Guide

This repository contains two different setup scripts with different purposes. This guide clarifies when to use each one.

---

## Scripts Overview

### 1. `developer-tools/setup.sh`

**Purpose:** General skill directory initialization and structure creation

**What it does:**
- Creates all required directory structure (skill-package, user-data, docs, etc.)
- Copies configuration templates
- Checks Python dependencies
- Optionally initializes Git repository
- General-purpose setup for the template structure

**When to use:**
- First time setting up the template from scratch
- Recreating directory structure after corruption
- Setting up a fresh clone of the repository

**Run with:**
```bash
./developer-tools/setup.sh
```

---

### 2. `developer-tools/setup-storage.sh`

**Purpose:** Auto-configuration of local filesystem storage with Claude Desktop MCP integration

**What it does:**
- Detects your OS (macOS/Linux)
- Creates user-data directory from templates
- Configures Claude Desktop's MCP server for filesystem access
- Sets up paths.py with absolute paths
- Specifically configures the filesystem MCP server to access user-data

**When to use:**
- After running developer-tools/setup.sh
- When you want to use Local Filesystem storage backend
- When setting up Claude Desktop MCP integration
- When you need automatic Claude config file updates

**Run with:**
```bash
./developer-tools/setup-storage.sh
```

**Note:** This script requires Claude Desktop to be installed and modifies your Claude Desktop configuration file.

---

## Recommended Workflow for New Users

### Step 1: Initialize Template Structure
```bash
# Run general setup first
./developer-tools/setup.sh
```

### Step 2: Choose Storage Backend

**Option A: Local Filesystem (Easiest)**
```bash
# Run storage-specific setup
./developer-tools/setup-storage.sh
```

**Option B: GitHub/Email/Notion (Multi-device)**
```bash
# Manually configure storage backend
cd user-data/config
cp storage-config-template.yaml storage-config.yaml
# Edit storage-config.yaml with your chosen backend
```

### Step 3: Validate
```bash
python developer-tools/validate.py
```

---

## Quick Reference

| Script | Purpose | Modifies Claude Config | Best For |
|--------|---------|----------------------|----------|
| `developer-tools/setup.sh` | Initialize directories | ❌ No | First-time setup |
| `developer-tools/setup-storage.sh` | Configure local storage + MCP | ✅ Yes | Claude Desktop users |

---

## Need Help?

- For interactive guidance: Attach this repo to Claude and say "hi"
- For manual setup: See [QUICK_SETUP.md](QUICK_SETUP.md)
- For storage backends: See [DEPENDENCIES.md](../DEPENDENCIES.md)

---

**Last Updated:** 2025-11-05 | **v1.1.0**
