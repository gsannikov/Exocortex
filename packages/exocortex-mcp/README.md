# Exocortex MCP Server

Expose Exocortex Claude skills through MCP protocol for use with any LLM platform.

## Features

- **Token Optimization**: Lazy loading of skills and modules
- **Self-Update**: Modules can be updated during conversations
- **Multi-Platform**: Works with Claude, ChatGPT, Cursor, and any MCP-compatible client
- **Backups**: Automatic backup before any modification

## Installation

```bash
cd packages/exocortex-mcp
pip install -e .
```

Or with uv:

```bash
uv pip install -e .
```

## Usage

### Stdio Mode (Local)

```bash
python -m exocortex_mcp.server
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "exocortex": {
      "command": "python",
      "args": ["-m", "exocortex_mcp.server"],
      "cwd": "/Users/gursannikov/Projects/exocortex/packages/exocortex-mcp"
    }
  }
}
```

Or with uv:

```json
{
  "mcpServers": {
    "exocortex": {
      "command": "uv",
      "args": ["run", "python", "-m", "exocortex_mcp.server"],
      "cwd": "/Users/gursannikov/Projects/exocortex/packages/exocortex-mcp"
    }
  }
}
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `exocortex_list_skills` | List all available skills with triggers |
| `exocortex_get_skill` | Load skill overview (SKILL.md) |
| `exocortex_load_module` | Load specific module on-demand |
| `exocortex_load_reference` | Load reference documentation |
| `exocortex_skill_action` | Execute skill command |
| `exocortex_update_module` | Self-update a module |
| `exocortex_get_config` | Get skill configuration |

## Token Optimization

The MCP server implements lazy loading:

1. **list_skills** returns only names + triggers (~100 tokens)
2. **get_skill** loads full SKILL.md (~500-1500 tokens)
3. **load_module** loads specific module when needed (~300-800 tokens)

This mirrors Claude's selective loading behavior.

## Self-Update Loop

Modules can be improved during conversations:

```python
# Example: Update scoring formula based on feedback
await update_module({
    "skill_name": "job-analyzer",
    "module_name": "scoring-formulas",
    "content": "# Updated Scoring...",
    "reason": "Added remote work bonus weight"
})
```

Backups are created at `~/exocortex-data/mcp-backups/`.

## Comparison: MCP vs Claude Skills

| Aspect | Claude Skills (ZIP) | MCP Server |
|--------|---------------------|------------|
| Setup | Manual upload | Config once |
| Updates | Re-upload ZIP | Live edits |
| Platforms | Claude only | Any LLM |
| Token loading | Claude optimizes | Manual lazy load |
| Self-update | No | Yes |
