# GitHub Search Module

## Search Strategy

### API Endpoints

```python
# GitHub Search API
BASE_URL = "https://api.github.com/search"

# Code search
f"{BASE_URL}/code?q={query}+language:python"

# Repository search  
f"{BASE_URL}/repositories?q={query}+topic:mcp+topic:claude"
```

### Query Construction

For user request: "track expenses and generate reports"

```python
queries = [
    # MCP-specific
    "expense tracker MCP server",
    "expense MCP",
    "finance MCP server",
    
    # Claude-specific
    "expense claude skill",
    "expense tracking claude",
    
    # General automation
    "expense tracker automation python",
    "expense CLI tool",
    "budget tracker python"
]
```

### Priority Repositories

Search these first (known quality):

| Repository | Type | Focus |
|------------|------|-------|
| modelcontextprotocol/servers | MCP | Official MCP servers |
| anthropics/anthropic-cookbook | Examples | Claude patterns |
| n8n-io/n8n | Automation | Workflow templates |
| activepieces/activepieces | Automation | Connectors |

### Result Parsing

Extract from each result:
- Repository name and URL
- Description
- Stars count
- Last commit date
- License
- Primary language
- README content (for feature extraction)

### Feature Matching

Compare user requirements vs found repos:

```python
def calculate_match(user_features: list, repo_features: list) -> float:
    """
    Calculate feature overlap percentage.
    
    user_features: ["expense tracking", "reports", "categories"]
    repo_features: extracted from README/code
    """
    matches = set(user_features) & set(repo_features)
    return len(matches) / len(user_features) * 100
```

### Output Format

```markdown
## GitHub Search Results

### 1. expense-tracker-mcp (⭐ 234)
**URL**: https://github.com/user/expense-tracker-mcp
**Match**: 75%
**Last Updated**: 2 weeks ago
**License**: MIT

**Features Found**:
- ✅ Expense tracking
- ✅ Category management
- ❌ Report generation
- ✅ Receipt OCR

**Adaptation Effort**: Medium (2-3 hours)

---

### 2. budget-cli (⭐ 1.2k)
**URL**: https://github.com/user/budget-cli
**Match**: 60%
...
```

### Rate Limiting

- GitHub API: 60 requests/hour (unauthenticated)
- Use web_search as fallback
- Cache results in session

### Fallback: Web Search

If GitHub API unavailable:
```
site:github.com {query} MCP OR claude OR automation
```
