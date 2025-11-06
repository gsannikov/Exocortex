# Architecture Guide

System design and implementation patterns for developers.

## Overview

This skill uses a **three-tier architecture** for clean separation of concerns, optimal token usage, and maintainability.

---

## Three-Tier Design

### Tier 1: skill-package/ (Skill Logic)

**Purpose:** The "brain" - all logic uploaded to Claude

**Structure:**
```
skill-package/
├── SKILL.md           # Main instructions for Claude
├── config/            # Static configuration
│   └── paths.py       # File system paths
├── modules/           # Feature modules (load on-demand)
│   └── feature-a.md
├── scripts/           # Python utilities
│   ├── config_loader.py
│   └── yaml_utils.py
└── templates/         # Output formatting (optional)
```

**Characteristics:**
- ✅ Read-only for Claude
- ✅ Version controlled in Git
- ✅ Portable across users
- ✅ Token-optimized (progressive loading)
- ❌ No user-specific data
- ❌ No secrets or API keys

---

### Tier 2: user-data/ (User Storage)

**Purpose:** User-specific data and state

**Structure:**
```
user-data/
├── config/           # User settings
│   └── user-config.yaml
├── db/               # Dynamic data (YAML files)
│   └── entities.yaml
└── logs/             # Operation logs
    └── operations.log
```

**Characteristics:**
- ✅ Read-write via MCP Filesystem
- ✅ User-specific data
- ✅ Gitignored (.gitignore)
- ✅ Private and local
- ❌ Never version controlled
- ❌ Never uploaded to Claude

**Access Pattern:**
```python
# Read config
config = load_user_config()

# Write data
save_to_yaml("user-data/db/data.yaml", data)

# Log operation
log_operation("Feature X executed successfully")
```

---

### Tier 3: docs/ (Documentation)

**Purpose:** Project knowledge base

**Structure:**
```
docs/
├── guides/
│   ├── user-guide/      # For end users
│   │   ├── setup.md
│   │   ├── usage.md
│   │   └── troubleshooting.md
│   └── developer-guide/ # For developers
│       ├── architecture.md (this file)
│       ├── module-guide.md
│       └── testing.md
└── project/
    ├── features/        # Feature specifications
    ├── roadmap.md       # Release planning
    └── session-archives/ # Archived session states
```

**Characteristics:**
- ✅ Version controlled
- ✅ Comprehensive
- ✅ Always up-to-date
- ✅ Supports collaboration

---

## Token Budget System

### The Problem
Claude has a 190K token context window. Loading everything exhausts tokens mid-conversation.

### The Solution: Progressive Loading

**Stage 1: Bootstrap (Always)**
```
Load:
- SKILL.md (~2K tokens)
- paths.py (~1K tokens)
Total: ~3K tokens
```

**Stage 2: On-Demand (As Needed)**
```
User: "Use Feature A"
Load:
- modules/feature-a.md (~8K tokens)
Execute and respond
Total so far: ~11K tokens
```

**Stage 3: Archive (At 50% threshold)**
```
When tokens reach 95K/190K:
1. Save current state to DEV_SESSION_STATE.md
2. Inform user
3. Start new conversation
4. Load saved state
5. Continue seamlessly
```

### Token Budget Rules
- **Core loading:** <5K tokens
- **Module size:** 5-15K tokens each
- **Warning threshold:** 50% (95K tokens)
- **Archive threshold:** Never reached (archived first)

---

## Data Flow

### Standard Request Flow
```
1. User sends request
   ↓
2. SKILL.md routes to appropriate module
   ↓
3. Module loads on-demand
   ↓
4. Module executes via MCP Filesystem
   ↓
5. Reads/writes user-data/
   ↓
6. Formats output
   ↓
7. Returns result to user
```

### Cross-Module Flow
```
Module A needs Module B:
1. Check if Module B already loaded
2. If not, load Module B
3. Execute Module B logic
4. Return to Module A
5. Continue Module A logic
```

---

## Module Pattern

### Anatomy of a Module
```markdown
# Module: Feature Name
**Token Estimate:** ~8K tokens  
**Dependencies:** None | Module X, Module Y  
**Load Strategy:** On-demand

## Purpose
Single-sentence description.

## Usage
\`\`\`
User: "Command"
Claude: "Response"
\`\`\`

## Implementation
[Core logic here]

## Error Handling
[How errors are handled]
```

### Module Guidelines
1. **Single Responsibility:** One feature per module
2. **Token Aware:** Keep under 15K tokens
3. **Self-Contained:** Minimal dependencies
4. **Well-Documented:** Clear purpose and usage
5. **Error Handling:** Graceful failures

---

## MCP Integration

### Filesystem Operations
```python
# Read
content = read_file("user-data/config/settings.yaml")

# Write  
write_file("user-data/db/data.yaml", data)

# List
files = list_directory("user-data/db/")

# Search
results = search_files("user-data/", "*.yaml")
```

### Best Practices
- Always use absolute paths from paths.py
- Handle file not found gracefully
- Validate YAML before writing
- Log all file operations
- Never write to skill-package/

---

## State Management

### Session State (DEV_SESSION_STATE.md)
**Purpose:** Maintain context across conversations

**Contains:**
- Current work in progress
- Token usage tracking
- Recent completions
- Known issues
- Next steps

**Usage:**
```
At 50% tokens:
1. Update DEV_SESSION_STATE.md
2. Save all work
3. Start new conversation
4. Load DEV_SESSION_STATE.md
5. Resume work
```

### Persistent State (user-data/db/)
**Purpose:** Long-term data storage

**Examples:**
- User preferences
- Historical data
- Cached results
- Entity databases

---

## Error Handling Strategy

### Graceful Degradation
1. Try primary approach
2. If fails, try fallback
3. If all fail, inform user clearly
4. Log error for debugging
5. Provide recovery suggestions

### Error Categories
- **P0 (Critical):** Skill cannot function
- **P1 (High):** Major feature broken
- **P2 (Medium):** Minor feature issue
- **P3 (Low):** Cosmetic or enhancement

---

## Security Principles

### Never Store in skill-package/
- ❌ API keys
- ❌ Passwords
- ❌ Personal data
- ❌ Secrets

### Always Store in user-data/config/
- ✅ User settings
- ✅ API keys (gitignored)
- ✅ Private configuration

### .gitignore Protection
```
user-data/config/*.yaml
user-data/db/*.yaml
user-data/logs/*.log
*.secret
*.key
```

---

## Performance Optimization

### Token Efficiency
- Load modules lazily
- Cache expensive computations
- Archive proactively
- Use references instead of duplicating

### Execution Speed
- Minimize file I/O
- Batch operations
- Use efficient data structures
- Profile and optimize hot paths

---

## Testing Architecture

### Unit Tests
Test individual functions in scripts/

### Integration Tests
Test complete workflows end-to-end

### Token Budget Tests
Verify progressive loading works

### Manual Tests
User acceptance testing

---

## Deployment Pattern

### Development
1. Edit in skill-package/
2. Test in Claude
3. Iterate until working
4. Document changes

### Release
1. Run validation: `python host_scripts/validate.py`
2. Update version: `version.yaml`, `SKILL.md`
3. Create release: `./host_scripts/release.sh X.Y.Z`
4. Push to GitHub with tags
5. Create GitHub release with ZIP

---

## Future Considerations

### Scaling
- Module lazy loading
- Distributed state
- Multi-user support

### Enhancement
- Real-time updates
- Plugin architecture
- Visual builder

---

*This architecture has been battle-tested in production skills handling 30+ features and 5-35K tokens per operation.*
