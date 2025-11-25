# Quick Dependency Check

Run a quick dependency status check:

```bash
python shared/scripts/dependency_tracker.py status
```

This shows:
- All tracked files grouped by type (source, derived, documentation, marketing)
- Which files need updating
- Summary of how many files need attention

For a full refactor workflow, use `/refactor` instead.
