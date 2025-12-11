# MCP Registry Module

## Overview

Search MCP (Model Context Protocol) server registries and repositories for existing implementations.

## Primary Sources

### 1. Official MCP Servers Repository

```
Repository: modelcontextprotocol/servers
URL: https://github.com/modelcontextprotocol/servers
```

Categories to search:
- `src/` - Official implementations
- Community contributions
- Reference implementations

### 2. MCP Server Directories

| Source | URL | Type |
|--------|-----|------|
| MCP Hub | mcp.so | Directory |
| Awesome MCP | github.com/punkpeye/awesome-mcp-servers | Curated list |
| Smithery | smithery.ai | Registry |

### 3. NPM/PyPI Search

```bash
# NPM
npm search mcp-server-{topic}

# PyPI  
pip search mcp {topic}
```

## Search Strategy

### Query Construction

For user request: "email management"

```python
search_terms = [
    "email mcp server",
    "gmail mcp",
    "imap mcp server",
    "mail automation mcp"
]
```

### Result Evaluation

| Criterion | Weight | Check |
|-----------|--------|-------|
| Official/verified | 30% | Is it in official repo? |
| Maintenance | 25% | Last update < 3 months? |
| Documentation | 20% | Has clear README? |
| Stars/usage | 15% | Community adoption |
| License | 10% | Compatible license? |

## Output Format

```markdown
## MCP Server Search Results

### 1. @modelcontextprotocol/server-gmail ✓ Official
**Source**: modelcontextprotocol/servers
**Match**: 90%
**Status**: Maintained

**Capabilities**:
- ✅ Read emails
- ✅ Send emails
- ✅ Search
- ❌ Labels management

**Integration**: Can use directly via MCP, or adapt logic

---

### 2. mcp-email-client (Community)
**Source**: github.com/user/mcp-email-client
**Match**: 70%
**Status**: Last update 2 months ago
...
```

## Integration Recommendations

| Scenario | Recommendation |
|----------|----------------|
| Official MCP exists | Use directly, create skill wrapper |
| Community MCP exists | Evaluate quality, adapt or use |
| No MCP exists | Create fresh skill |

### MCP Wrapper Pattern

If good MCP server exists, skill becomes thin wrapper:

```markdown
# SKILL.md for MCP wrapper

## Overview
Wrapper for {mcp-server-name} with Exocortex patterns.

## MCP Server
Server: {mcp-server-name}
Config: Add to claude_desktop_config.json

## Added Value
- Inbox integration
- YAML storage
- Reporting
```
