---
name: setup-manager
description: Manages Claude Skills ecosystem setup and maintenance. Checks environment (Python, uv, npm, git), discovers available skills, installs dependencies, and performs routine maintenance. Triggers - "setup skills", "check environment", "list skills", "install dependencies", "skill maintenance", "discover skills", "skill guide".
---

# Setup Manager

## Overview

Manage initial setup, configuration, and health checks for the Exocortex system.

## Commands

| Command | Action |
|---------|--------|
| `check environment` | Verify tools (Python, uv, npm, git) |
| `list skills` | Show available skills |
| `get skill guide [name]` | Detailed skill info |
| `install dependencies` | Install project deps |
| `perform maintenance` | Log rotation, updates |

## Environment Requirements

- Python 3.10+
- uv (Python package manager)
- npm (for MCP servers)
- git

## Skill Discovery

Scans `packages/` directory for skills with valid SKILL.md files. Extracts name, description, and trigger phrases from frontmatter.
