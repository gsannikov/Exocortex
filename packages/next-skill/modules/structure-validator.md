# Structure Validator Module

## Overview

Validates skill compliance with Exocortex architecture standards.

## Validation Checks

### Required Structure

| Item | Required | Check |
|------|----------|-------|
| SKILL.md | ✅ Yes | File exists |
| SKILL.md < 100 lines | ✅ Yes | Line count |
| version.yaml | ✅ Yes | File exists, valid YAML |

### Recommended Structure

| Item | Recommended | Check |
|------|-------------|-------|
| references/ | Yes | Directory exists |
| references/workflow.md | Yes | File exists |
| _dev/ | Yes | Directory exists |
| _dev/design.md | Yes | File exists |
| modules/ | If complex | Directory exists |
| config/paths.py | If has storage | File exists |
| CHANGELOG.md | Yes | File exists |

### Quality Checks

| Check | Method | Severity |
|-------|--------|----------|
| No hardcoded paths | Grep for `/Users/`, `~/` | Error |
| YAML syntax | Parse all .yaml | Error |
| Python syntax | py_compile | Error |
| Markdown links | Check relative links | Warning |
| Line lengths | SKILL.md < 100 | Error |

## Validation Script

```python
def validate_skill(skill_path: Path) -> ValidationResult:
    """
    Validate skill structure and quality.
    """
    errors = []
    warnings = []
    
    # Required files
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    else:
        lines = skill_md.read_text().splitlines()
        if len(lines) > 100:
            errors.append(f"SKILL.md has {len(lines)} lines (max 100)")
    
    version_yaml = skill_path / "version.yaml"
    if not version_yaml.exists():
        errors.append("Missing version.yaml")
    
    # Recommended
    if not (skill_path / "references").exists():
        warnings.append("Missing references/ directory")
    
    if not (skill_path / "_dev").exists():
        warnings.append("Missing _dev/ directory")
    
    # Quality checks
    for py_file in skill_path.rglob("*.py"):
        # Check for hardcoded paths
        content = py_file.read_text()
        if "/Users/" in content or re.search(r'~/', content):
            errors.append(f"Hardcoded path in {py_file.name}")
    
    return ValidationResult(errors=errors, warnings=warnings)
```

## Output Report

```
╔══════════════════════════════════════════════════════════════╗
║           SKILL VALIDATION: {skill-name}                     ║
╠══════════════════════════════════════════════════════════════╣
║ STRUCTURE                                                    ║
║   ✅ SKILL.md exists (87 lines)                              ║
║   ✅ version.yaml valid                                      ║
║   ✅ references/workflow.md                                  ║
║   ✅ _dev/design.md                                          ║
║   ⚠️  No tests/ directory                                    ║
╠══════════════════════════════════════════════════════════════╣
║ QUALITY                                                      ║
║   ✅ No hardcoded paths                                      ║
║   ✅ All YAML files valid                                    ║
║   ✅ All Python files syntax OK                              ║
║   ✅ Internal links resolve                                  ║
╠══════════════════════════════════════════════════════════════╣
║ INTEGRATION                                                  ║
║   ✅ Registered in release.py                                ║
║   ✅ Listed in dependencies.yaml                             ║
║   ✅ Data directory exists                                   ║
╠══════════════════════════════════════════════════════════════╣
║ RESULT: PASS (1 warning)                                     ║
╚══════════════════════════════════════════════════════════════╝
```

## Fix Suggestions

For each error/warning, provide actionable fix:

| Issue | Fix |
|-------|-----|
| SKILL.md > 100 lines | Move details to references/workflow.md |
| Missing version.yaml | Create with `scaffold: version` |
| Hardcoded path | Use config/paths.py |
| Missing _dev/ | Create with design.md template |
