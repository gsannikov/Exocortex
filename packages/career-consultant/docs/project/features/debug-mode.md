# Feature: Debug Mode (Developer Console)

**Status**: Implemented (v1.1.0)
**Priority**: High (Developer Experience)
**Owner**: Engineering

## Overview

Debug Mode provides a "Developer Console" within the chat interface, allowing developers to inspect the skill's internal state, view raw system prompts, and test MCP tools in isolation without running full workflows.

## Problem Statement

Developing and debugging Claude Skills is opaque.
- You can't see the exact prompt the AI is using.
- You can't easily tell if a tool failure is due to the tool or the prompt.
- You can't see the current session state (loaded modules, token usage).

## Solution

A dedicated `debug-mode.md` module that intercepts `/debug` commands.

### Capabilities

1.  **Prompt Inspector**: `/debug prompt [module]`
    - Displays the exact system prompt for a specific module.
    - Useful for verifying prompt engineering changes.

2.  **Tool Tester**: `/debug tool [name] [args]`
    - Runs an MCP tool (Firecrawl, Bright Data) with raw arguments.
    - Bypasses the skill's error handling to show raw failures/successes.

3.  **State Viewer**: `/debug state`
    - Dumps the current session context (config, loaded modules, token usage).

4.  **Verbose Logging**: `/debug on`
    - Enables detailed print statements in the Python execution log.

## Architecture

- **Module**: `skill-package/modules/debug-mode.md`
- **Integration**: `SKILL.md` intercepts `/debug` commands before normal processing.
- **Config**: `debug_mode` flag in `settings.yaml`.

## Usage

```
User: /debug on
Claude: ✅ Debug Mode ENABLED. Verbose logging active.

User: /debug prompt scoring
Claude: ### 📝 System Prompt: scoring ...

User: /debug tool firecrawl https://google.com
Claude: 🧪 Testing tool: firecrawl ...
```
