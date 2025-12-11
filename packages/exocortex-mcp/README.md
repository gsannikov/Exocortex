# Exocortex MCP Server

Expose Exocortex Claude skills through MCP protocol for use with any LLM platform.

## Features

- **Token Optimization**: Lazy loading of skills and modules
- **Self-Update Loop**: Modules evolve during conversations (Phase 2)
- **Multi-Platform**: Works with Claude, ChatGPT, Cursor, and any MCP-compatible client
- **Pattern Learning**: Capture improvements and apply them later
- **Backups & Rollback**: Every change creates a backup

## Installation

```bash
cd packages/exocortex-mcp
pip install -e .
```

## Usage

### Cursor Configuration

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "exocortex": {
      "command": "/Users/gursannikov/Projects/exocortex/.venv/bin/python",
      "args": ["-m", "exocortex_mcp"],
      "cwd": "/Users/gursannikov/Projects/exocortex/packages/exocortex-mcp"
    }
  }
}
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "exocortex": {
      "command": "/Users/gursannikov/Projects/exocortex/.venv/bin/python",
      "args": ["-m", "exocortex_mcp"],
      "cwd": "/Users/gursannikov/Projects/exocortex/packages/exocortex-mcp"
    }
  }
}
```

## Available Tools

### Phase 1: Core Tools

| Tool | Purpose | Tokens |
|------|---------|--------|
| `exocortex_list_skills` | List all skills with triggers | ~100 |
| `exocortex_get_skill` | Load skill overview (SKILL.md) | 500-1500 |
| `exocortex_load_module` | Load specific module on-demand | 300-800 |
| `exocortex_load_reference` | Load reference documentation | 200-500 |
| `exocortex_skill_action` | Execute skill command with guidance | ~50 |
| `exocortex_get_config` | Get skill configuration | ~100 |

### Phase 2: Self-Update Loop

| Tool | Purpose |
|------|---------|
| `exocortex_update_module` | Replace entire module content |
| `exocortex_apply_patch` | Targeted find-replace patch |
| `exocortex_learn_pattern` | Capture improvement/insight |
| `exocortex_list_patterns` | Show learned patterns |
| `exocortex_propose_update` | Generate update proposals from patterns |
| `exocortex_mark_pattern_applied` | Mark pattern as implemented |
| `exocortex_list_backups` | Show available backups |
| `exocortex_rollback_module` | Restore from backup |
| `exocortex_diff_module` | Show diff between current and backup |

## Self-Update Workflow

```
1. During work, notice an improvement opportunity
   → exocortex_learn_pattern(skill, type, description, suggestion)

2. Later, review pending patterns
   → exocortex_list_patterns(skill)

3. Generate proposals
   → exocortex_propose_update(skill)

4. Apply targeted fix
   → exocortex_apply_patch(skill, module, find, replace, reason)

5. Mark as done
   → exocortex_mark_pattern_applied(pattern_id)

6. If something breaks, rollback
   → exocortex_list_backups()
   → exocortex_rollback_module(backup, skill, module)
```

## Storage

```
~/exocortex-data/
├── mcp-backups/           # Module backups (timestamped)
├── mcp-updates.log        # Change log
└── learned-patterns.json  # Pattern database
```

## Token Optimization Strategy

The MCP server mirrors Claude's selective loading:

1. **list_skills** returns only names + triggers (~100 tokens)
2. **get_skill** loads full SKILL.md (~500-1500 tokens)
3. **load_module** loads specific module when needed (~300-800 tokens)

This prevents loading all skill content upfront.

## Comparison: MCP vs Claude Skills

| Aspect | Claude Skills (ZIP) | MCP Server |
|--------|---------------------|------------|
| Setup | Manual upload | Config once |
| Updates | Re-upload ZIP | Live edits |
| Platforms | Claude only | Any LLM |
| Token loading | Claude optimizes | Manual lazy load |
| Self-update | No | Yes |
| Pattern learning | No | Yes |
| Rollback | Manual | Built-in |
