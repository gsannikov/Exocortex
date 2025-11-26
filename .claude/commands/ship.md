# Ship Command - Full Release Cycle

Automates the full cycle: **Test → Commit → Push → PR**

## Arguments

- `$ARGUMENTS` - Optional: commit message or PR title (will prompt if not provided)

## Step 1: Pre-flight Checks

Run these checks in parallel:

```bash
# Check git status
git status --short

# Check current branch
git branch --show-current

# Check if we're ahead of remote
git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "No upstream"
```

**Stop if**:
- Working directory is clean (nothing to ship)
- On main/master branch (should be on feature branch)

## Step 2: Run Tests

Detect and run appropriate tests based on what changed:

### For Swift packages (MeetingRecorder):
```bash
# Check if Swift files changed
git diff --name-only | grep -q "\.swift$"

# If yes, run Swift tests
cd packages/voice-memos/meeting-recorder/MeetingRecorder
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer swift test --scratch-path /tmp/MeetingRecorder-build
```

### For Python scripts:
```bash
# Check if Python files changed
git diff --name-only | grep -q "\.py$"

# If yes, run pytest (if tests exist)
pytest packages/*/tests/ --tb=short 2>/dev/null || echo "No Python tests found"
```

### For general validation:
```bash
# Validate YAML files
python3 -c "import yaml; [yaml.safe_load(open(f)) for f in __import__('glob').glob('**/*.yaml', recursive=True)]"

# Check dependency status
python3 shared/scripts/dependency_tracker.py status 2>/dev/null || echo "Dependency tracker not available"
```

**Stop if any tests fail.**

## Step 3: Stage and Commit

1. Show the diff summary:
```bash
git diff --stat
git diff --name-only
```

2. Stage all changes:
```bash
git add -A
```

3. Create commit with conventional commit format:
   - If `$ARGUMENTS` provided, use it as commit message
   - Otherwise, analyze changes and generate appropriate message
   - Use format: `type(scope): description`
   - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

```bash
git commit -m "$(cat <<'EOF'
{generated or provided message}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Step 4: Push to Remote

```bash
# Push with upstream tracking
git push -u origin $(git branch --show-current)
```

## Step 5: Create Pull Request

Use GitHub CLI to create PR:

```bash
gh pr create \
  --title "{PR title based on commits}" \
  --body "$(cat <<'EOF'
## Summary
{bullet points summarizing changes}

## Test Plan
- [ ] Tests pass locally
- [ ] Manual verification completed

## Checklist
- [ ] Code follows project conventions
- [ ] Documentation updated if needed
- [ ] No breaking changes (or documented)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## Step 6: Report Results

Provide summary:
- Commit SHA
- Branch name
- PR URL
- Any warnings or notes

---

## Quick Reference

| Stage | Command | On Failure |
|-------|---------|------------|
| Tests | `swift test` / `pytest` | Stop and report |
| Commit | `git commit` | Stop and report |
| Push | `git push -u origin` | Stop and report |
| PR | `gh pr create` | Provide manual URL |

---

## Usage Examples

```
/ship                           # Auto-generate commit message
/ship fix login validation      # Use provided message
/ship "feat: add dark mode"     # Explicit commit message
```

---

Now execute the ship workflow starting with Step 1.
