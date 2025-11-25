# Dependency-Aware Refactor Command

You are about to perform a dependency-aware refactor of the Claude Skills monorepo.

## Step 1: Check Dependency Status

First, run the dependency tracker to see what files need updating:

```bash
python shared/scripts/dependency_tracker.py status
```

Review the output to understand:
- Which files are out of date
- What dependencies have changed
- The rebuild order

## Step 2: Analyze Changes

For each file that needs updating:
1. Read the source file(s) it depends on
2. Understand what changed
3. Read the target file that needs updating
4. Determine what updates are needed

## Step 3: Rebuild in Order

Use `python shared/scripts/dependency_tracker.py rebuild-order` to get the correct order.

**IMPORTANT**: Always rebuild in dependency order (sources → derived → documentation → marketing)

For each file:
1. Read the `rebuild_instructions` from `dependencies.yaml`
2. Read the current file content
3. Read the dependency files that changed
4. Make the necessary updates to sync content
5. Verify the changes are consistent

## Step 4: Update Versions

After updating files, don't forget to:
- Update `version.yaml` for affected skills
- Update `CHANGELOG.md` with what changed
- Update the `updated` date in `dependencies.yaml`

## Step 5: Summary

After completing all updates, provide a summary:
- List all files updated
- Describe what changed in each
- Note any issues or items needing manual review

---

## Quick Commands

| Command | Description |
|---------|-------------|
| `python shared/scripts/dependency_tracker.py status` | Show all file statuses |
| `python shared/scripts/dependency_tracker.py graph` | Show dependency tree |
| `python shared/scripts/dependency_tracker.py rebuild-order` | Show rebuild order |
| `python shared/scripts/dependency_tracker.py affected <file>` | Show dependents of a file |
| `python shared/scripts/dependency_tracker.py prompt` | Generate rebuild prompt |

---

Now execute Step 1 to check the current dependency status.
