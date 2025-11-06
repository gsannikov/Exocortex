# Repository Restructuring Proposal

## Executive Summary

Restructure the repository to clearly separate three distinct layers of development:

1. **SDK Developers** (Layer 1) - Maintain the template/SDK itself
2. **Skill Developers** (Layer 2) - Use this template to build skills
3. **Skill Package** (Layer 3) - The actual code uploaded to Claude

**Goal:** Make it crystal clear which files are for which audience, reduce confusion, and improve developer experience.

---

## Current Problems

### Confusion of Concerns
- SDK development files (`.github/workflows/`, `config/.gitleaks.toml`) mixed with skill developer files
- Documentation not clearly separated by audience
- `host_scripts/` serves both template maintenance AND skill development
- Unclear what a skill developer should modify vs. what's template infrastructure

### Navigation Challenges
- New skill developers don't know where to start
- SDK developers can't easily find template infrastructure
- Documentation scattered across multiple folders without clear audience targeting

### Onboarding Friction
- README tries to serve too many audiences
- Getting started is buried in docs/getting-started/
- No clear "template vs. your skill" boundary

---

## Proposed Structure

```
claude-skill-template/
│
├── README.md                           # [Layer 2] Main entry for skill developers
├── SDK_DEVELOPMENT.md                  # [Layer 1] Guide for SDK contributors
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
│
├── skill-package/                      # [Layer 3] THE SKILL (uploaded to Claude)
│   ├── SKILL.md                        # Skill definition
│   ├── README.md                       # Skill package documentation
│   ├── scripts/                        # Runtime Python scripts
│   │   ├── storage.py
│   │   ├── config_loader.py
│   │   └── yaml_utils.py
│   ├── config/                         # Skill configuration
│   │   └── paths.py
│   ├── modules/                        # Skill modules
│   │   └── module-template.md
│   ├── templates/                      # Skill templates
│   └── user-data-templates/            # Templates for user data
│       ├── config/
│       ├── db/
│       └── logs/
│
├── developer-tools/                    # [Layer 2] Tools for skill developers
│   ├── README.md                       # Guide to using these tools
│   ├── validate.py                     # Validate skill structure
│   ├── setup.sh                        # Setup new skill project
│   ├── setup-storage.sh                # Configure storage backend
│   ├── integrate-skill-creator.sh      # Integrate official tools
│   └── examples/                       # Example usage scripts
│
├── docs/                               # Documentation (by audience)
│   ├── README.md                       # Documentation navigation
│   │
│   ├── skill-developers/               # [Layer 2] For building skills
│   │   ├── README.md                   # Start here!
│   │   ├── getting-started/
│   │   │   ├── WELCOME.md
│   │   │   ├── QUICK_SETUP.md
│   │   │   ├── CLAUDE_ONBOARDING_GUIDE.md
│   │   │   └── DEPENDENCIES.md
│   │   ├── guides/
│   │   │   ├── storage-selection.md
│   │   │   ├── testing-guide.md
│   │   │   ├── setup-scripts.md
│   │   │   └── testing-quick-reference.md
│   │   ├── tutorials/
│   │   │   └── (future tutorial content)
│   │   └── reference/
│   │       ├── storage-api.md
│   │       └── configuration.md
│   │
│   ├── sdk-developers/                 # [Layer 1] For template maintainers
│   │   ├── README.md                   # Start here!
│   │   ├── architecture/
│   │   │   ├── overview.md
│   │   │   ├── SDK_DESIGN.md
│   │   │   └── STORAGE_DESIGN.md
│   │   ├── design-decisions/
│   │   │   └── GITHUB_STORAGE.md
│   │   ├── contributing/
│   │   │   ├── development-workflow.md
│   │   │   └── release-process.md
│   │   └── testing/
│   │       └── test-suite-guide.md
│   │
│   ├── shared/                         # [Both] Shared resources
│   │   ├── CHANGELOG.md
│   │   ├── DOCUMENTATION_STRUCTURE.md
│   │   └── resources/
│   │       ├── SDK-DOCS-SUMMARY.md
│   │       ├── SDK-PRESENTATION.md
│   │       └── SDK-BLOG-POST.md
│   │
│   └── archives/                       # Historical documentation
│       ├── README.md
│       ├── INCONSISTENCY_REPORT.md
│       ├── FIXES_SUMMARY.md
│       └── WORKFLOW_IMPROVEMENTS.md
│
├── sdk/                                # [Layer 1] SDK development infrastructure
│   ├── README.md                       # SDK infrastructure guide
│   ├── .github/                        # CI/CD for template validation
│   │   ├── workflows/
│   │   │   ├── comprehensive-tests.yml
│   │   │   ├── release.yml
│   │   │   └── validate.yml
│   │   ├── PULL_REQUEST_TEMPLATE.md
│   │   └── ISSUE_TEMPLATE/
│   ├── config/                         # SDK configuration
│   │   ├── .gitleaks.toml
│   │   └── version.yaml
│   ├── scripts/                        # SDK maintenance scripts
│   │   └── release.sh
│   └── tests/                          # Template validation tests
│       └── (test files from workflows)
│
├── user-data/                          # [Layer 3] Runtime data (gitignored)
│   ├── config/
│   ├── db/
│   └── logs/
│
├── releases/                           # Release artifacts
│   └── CHECKSUMS-1.0.0.txt
│
├── requirements.txt                    # [Layer 3] Skill runtime dependencies
├── requirements-dev.txt                # [Layer 1] SDK dev dependencies
├── .gitignore
└── .gitattributes
```

---

## Key Principles

### 1. Clear Audience Targeting
- **README.md** → Skill developers (Layer 2) - main audience
- **SDK_DEVELOPMENT.md** → SDK maintainers (Layer 1)
- **skill-package/README.md** → Documentation of the skill package itself

### 2. Logical Grouping
- **developer-tools/** → All tools for building skills (previously `host_scripts/`)
- **sdk/** → All template infrastructure (CI/CD, config, release scripts)
- **docs/** → Split by audience (skill-developers/, sdk-developers/, shared/)

### 3. Minimal Root Clutter
- Only essential files in root
- README.md immediately guides developers to right place
- SDK_DEVELOPMENT.md clearly marked for maintainers

### 4. Self-Documenting Structure
- Folder names indicate purpose and audience
- Each major folder has its own README.md
- Layer annotations in comments/docs

---

## Migration Plan

### Phase 1: Create New Structure (No Breaking Changes)
```bash
# Create new directories
mkdir -p developer-tools
mkdir -p sdk/.github/workflows
mkdir -p sdk/config
mkdir -p sdk/scripts
mkdir -p docs/skill-developers
mkdir -p docs/sdk-developers
mkdir -p docs/shared

# Move files (preserve git history)
git mv host_scripts/* developer-tools/
git mv .github sdk/
git mv config/* sdk/config/
git mv host_scripts/release.sh sdk/scripts/

# Reorganize docs
git mv docs/getting-started docs/skill-developers/
git mv docs/user-guide docs/skill-developers/guides
git mv docs/developer-guide docs/skill-developers/guides
git mv docs/design docs/sdk-developers/architecture
git mv docs/features docs/shared/
git mv docs/resources docs/shared/
git mv docs/CHANGELOG.md docs/shared/
```

### Phase 2: Update Documentation
- Create SDK_DEVELOPMENT.md
- Update README.md to focus on skill developers
- Add README.md to each major folder
- Update all path references in documentation

### Phase 3: Update Tooling & Scripts
- Update all script paths in workflows
- Update validation script paths
- Update setup script references
- Add deprecation notices where needed

### Phase 4: Update GitHub Actions
- Move workflows to sdk/.github/workflows/
- Update workflow file references
- Test all CI/CD pipelines

### Phase 5: Release & Communication
- Create migration guide for existing users
- Update all external documentation
- Release as v2.0.0 (breaking change)
- Add backward compatibility shims if needed

---

## Benefits

### For Skill Developers (Layer 2)
✅ **Clear starting point** - README.md is immediately relevant
✅ **Easy to find tools** - All in developer-tools/
✅ **Focused documentation** - Only docs/skill-developers/ is relevant
✅ **Less confusion** - SDK infrastructure hidden in sdk/
✅ **Better onboarding** - Obvious path from README → getting-started → building

### For SDK Developers (Layer 1)
✅ **Clear ownership** - SDK infrastructure in sdk/
✅ **Easier maintenance** - Related files grouped together
✅ **Better testing** - Test infrastructure separate from skill code
✅ **Clearer CI/CD** - Workflows clearly for template validation
✅ **Reduced noise** - Skill developer docs don't clutter SDK work

### For Both
✅ **Better mental model** - Clear layer separation
✅ **Easier navigation** - Logical folder structure
✅ **Reduced conflicts** - Less overlap between concerns
✅ **Scalability** - Easy to add new features to right layer
✅ **Professionalism** - Clean, enterprise-grade organization

---

## Alternative Approaches Considered

### Option A: Keep Current Structure + Add Documentation
**Pros:** No migration needed
**Cons:** Doesn't solve fundamental confusion, band-aid solution

### Option B: Monorepo with Workspaces
**Pros:** Complete separation, could publish SDK separately
**Cons:** Over-engineering, adds complexity, requires build tools

### Option C: Separate Repositories
**Pros:** Ultimate separation
**Cons:** Harder to maintain, version sync issues, template distribution problems

**Decision:** Proposed structure (single repo, clear folder organization) strikes the best balance.

---

## Risks & Mitigations

### Risk: Breaking Changes for Existing Users
**Mitigation:**
- Provide detailed migration guide
- Create automated migration script
- Version as 2.0.0 to signal breaking change
- Maintain 1.x branch for 6 months

### Risk: Path Updates Everywhere
**Mitigation:**
- Comprehensive search/replace
- Add path validation tests
- Update all docs in single PR
- Test all scripts and workflows

### Risk: GitHub Actions May Break
**Mitigation:**
- Test workflows before merging
- Keep old workflow files as backup
- Deploy gradually (test on branch first)

### Risk: Documentation Duplication
**Mitigation:**
- Use symlinks where appropriate
- Create "shared" folder for common docs
- Regular audits for duplicate content

---

## Success Metrics

- **Reduced onboarding time** - New skill developers can start in < 5 minutes
- **Fewer support questions** - "Where do I start?" questions drop 80%
- **Clearer contributions** - PRs target correct layer
- **Better discoverability** - Documentation findability improves
- **Higher adoption** - More developers successfully build skills

---

## Next Steps

1. **Review & Feedback** - Get team/community input on proposal
2. **Create Migration Script** - Automate as much as possible
3. **Update Documentation** - Write new READMEs, update guides
4. **Test Migration** - Run on clean branch
5. **Create Migration Guide** - Help existing users upgrade
6. **Execute Migration** - Merge restructuring PR
7. **Update External Docs** - Website, tutorials, videos
8. **Release v2.0.0** - Announce breaking changes

---

## Questions for Discussion

1. Should `developer-tools/` be named something else? (`tools/`, `bin/`, `scripts/`?)
2. Should `sdk/` be at root or nested? (e.g., `.sdk/`, `_sdk/`)
3. Should we keep backward compatibility shims? For how long?
4. Should we split requirements.txt into skill vs. SDK requirements?
5. Do we want a "quick start" script that guides developers to right place?

---

## Appendix: File Mapping

### Current → Proposed

| Current Path | New Path | Layer |
|-------------|----------|-------|
| `host_scripts/validate.py` | `developer-tools/validate.py` | 2 |
| `host_scripts/setup.sh` | `developer-tools/setup.sh` | 2 |
| `host_scripts/release.sh` | `sdk/scripts/release.sh` | 1 |
| `.github/workflows/` | `sdk/.github/workflows/` | 1 |
| `config/.gitleaks.toml` | `sdk/config/.gitleaks.toml` | 1 |
| `config/version.yaml` | `sdk/config/version.yaml` | 1 |
| `docs/getting-started/` | `docs/skill-developers/getting-started/` | 2 |
| `docs/developer-guide/` | `docs/skill-developers/guides/` | 2 |
| `docs/design/` | `docs/sdk-developers/architecture/` | 1 |
| `docs/CHANGELOG.md` | `docs/shared/CHANGELOG.md` | Both |
| `skill-package/` | `skill-package/` (unchanged) | 3 |

---

**Document Version:** 1.0
**Date:** 2025-11-06
**Status:** PROPOSAL - Awaiting Review
