# Next Skill - Detailed Workflow

## Discovery Phase

### GitHub Search Strategy

```python
# Search queries to try (in order)
queries = [
    f"{topic} MCP server",
    f"{topic} claude skill", 
    f"{topic} AI agent automation",
    f"{topic} workflow automation",
    f"{topic} CLI tool python"
]

# Priority repositories to search first
priority_repos = [
    "modelcontextprotocol/servers",
    "anthropics/anthropic-cookbook",
    "anthropics/claude-code-skills"
]
```

### Match Scoring

| Factor | Weight | Description |
|--------|--------|-------------|
| Feature overlap | 40% | How many requested features exist |
| Code quality | 20% | Tests, docs, maintenance |
| Architecture fit | 25% | How easy to adapt |
| Recency | 15% | Last commit date |

### Decision Matrix

| Match Score | Recommendation |
|-------------|----------------|
| 80%+ | Strong adapt - minimal changes |
| 60-79% | Adapt with enhancements |
| 40-59% | Partial adapt - use components |
| <40% | Create fresh, reference for ideas |

---

## Adaptation Phase

### Structure Mapping

| External Pattern | Exocortex Equivalent |
|------------------|---------------------|
| README.md | SKILL.md (condensed) |
| docs/ | references/ |
| src/ | scripts/ |
| config.json | config/settings.yaml |
| .env | config/paths.py |
| tests/ | Keep as-is |

### Refactoring Checklist

- [ ] Extract core logic from external structure
- [ ] Create SKILL.md (<100 lines) as orchestrator
- [ ] Move detailed docs to references/
- [ ] Convert config to YAML format
- [ ] Integrate with shared/config/paths.py
- [ ] Add _dev/ folder with adaptation notes
- [ ] Update imports/paths for new structure
- [ ] Test functionality

### Preserving Attribution

Create `_dev/research/adapted-from.md`:
```markdown
# Adaptation Source

**Original**: {github-url}
**License**: {license}
**Author**: {author}
**Adapted**: {date}

## What We Kept
- {feature 1}
- {feature 2}

## What We Changed
- {change 1}
- {change 2}

## What We Added
- {addition 1}
```

---

## Scaffolding Phase

### Pattern Selection

| Pattern | Use When |
|---------|----------|
| inbox | Skill processes items from Apple Notes |
| database | Skill stores structured YAML data |
| scoring | Skill evaluates/ranks items |
| scraping | Skill fetches web content |
| output | Skill generates reports/files |

### File Generation Order

1. `version.yaml` - Version metadata
2. `SKILL.md` - Main orchestrator
3. `references/workflow.md` - Detailed workflow
4. `config/paths.py` - Path configuration
5. `_dev/design.md` - Design decisions
6. `_dev/todos.md` - Development tasks
7. `modules/` - Based on selected patterns
8. `CHANGELOG.md` - Version history

### SKILL.md Template Structure

```markdown
# {emoji} {Name}

{One-line description}

## Commands

| Command | Action |
|---------|--------|
| `command` | Description |

## Workflow

### Step 1: {Name}
{Brief description}
→ Load `modules/{module}.md` if needed

### Step 2: {Name}
{Brief description}

## Module Loading

| Trigger | Load |
|---------|------|
| {trigger} | `modules/{module}.md` |

## Storage

**Location**: `~/exocortex-data/{skill}/`

---
**Version**: 0.1.0 | **Patterns**: {patterns}
```

---

## Integration Phase

### Release.py Registration

Add to `shared/scripts/release.py`:

```python
SKILL_CONFIG = {
    # ... existing skills ...
    '{skill-name}': {
        'has_host_scripts': {True/False},
        'has_tests': {True/False},
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
}
```

### Dependencies.yaml Update

Add nodes for new skill:

```yaml
nodes:
  - path: packages/{skill-name}/SKILL.md
    type: source
    description: {Skill} orchestrator
    
  - path: packages/{skill-name}/README.md
    type: derived
    depends_on:
      - packages/{skill-name}/SKILL.md
```

### Data Directory Creation

```bash
mkdir -p ~/exocortex-data/{skill-name}
```

---

## Validation Phase

### Structure Compliance Checks

| Check | Requirement |
|-------|-------------|
| SKILL.md exists | Required |
| SKILL.md < 100 lines | Required |
| version.yaml exists | Required |
| references/ exists | Recommended |
| _dev/ exists | Recommended |
| paths.py integration | If has storage |

### Quality Checks

| Check | Validation |
|-------|------------|
| No hardcoded paths | Grep for `/Users/`, `~/` outside config |
| YAML valid | Parse all .yaml files |
| Python syntax | py_compile on all .py |
| Markdown links | Check internal links resolve |

### Output Report

```
Skill Validation: {skill-name}
================================
Structure:  ✅ SKILL.md (87 lines)
            ✅ version.yaml
            ✅ references/workflow.md
            ✅ _dev/design.md
            ⚠️  No tests/ directory

Quality:    ✅ No hardcoded paths
            ✅ YAML valid
            ✅ Python syntax OK

Integration: ✅ release.py registered
             ✅ dependencies.yaml updated
             ✅ Data directory exists

Overall: PASS (1 warning)
```
