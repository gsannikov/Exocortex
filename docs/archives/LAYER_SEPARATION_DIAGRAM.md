# Layer Separation Visual Guide

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     CLAUDE SKILL TEMPLATE REPOSITORY                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  LAYER 1: SDK DEVELOPERS (Template Maintainers)                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
│                                                                          │
│  👥 Audience: Core maintainers, contributors to the template            │
│  🎯 Goal: Maintain and improve the template infrastructure              │
│                                                                          │
│  📁 Key Folders:                                                         │
│     sdk/                       ← CI/CD, config, release scripts         │
│     ├── .github/workflows/     ← Template validation tests              │
│     ├── config/                ← SDK configuration                      │
│     ├── scripts/               ← Release automation                     │
│     └── tests/                 ← Template tests                         │
│                                                                          │
│     docs/sdk-developers/       ← Architecture, design docs              │
│     ├── architecture/          ← System design                          │
│     ├── design-decisions/      ← ADRs, technical decisions              │
│     ├── contributing/          ← How to contribute                      │
│     └── testing/               ← Test suite documentation               │
│                                                                          │
│     requirements-dev.txt       ← Development dependencies               │
│     SDK_DEVELOPMENT.md         ← SDK development guide                  │
│                                                                          │
│  🔧 Activities:                                                          │
│     • Improve template infrastructure                                   │
│     • Add new storage backends                                          │
│     • Fix bugs in validation scripts                                    │
│     • Enhance CI/CD pipelines                                           │
│     • Release new template versions                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

                                     │
                                     │ uses template
                                     ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  LAYER 2: SKILL DEVELOPERS (Your Primary Audience)                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                │
│                                                                          │
│  👥 Audience: Developers building Claude skills                         │
│  🎯 Goal: Create, test, and deploy a new skill                          │
│                                                                          │
│  📁 Key Folders:                                                         │
│     README.md                  ← Main entry point (START HERE!)         │
│                                                                          │
│     developer-tools/           ← Tools for skill development            │
│     ├── validate.py            ← Validate your skill                    │
│     ├── setup.sh               ← Setup new skill project                │
│     ├── setup-storage.sh       ← Configure storage                      │
│     └── integrate-skill-creator.sh  ← Integration tools                 │
│                                                                          │
│     docs/skill-developers/     ← Your documentation                     │
│     ├── getting-started/       ← Onboarding (WELCOME, QUICK_SETUP)     │
│     ├── guides/                ← How-to guides                          │
│     ├── tutorials/             ← Step-by-step tutorials                 │
│     └── reference/             ← API reference                          │
│                                                                          │
│     skill-package/             ← Your skill code (modify this!)         │
│                                                                          │
│  🔧 Activities:                                                          │
│     • Clone the template                                                │
│     • Modify skill-package/ to build your skill                         │
│     • Use developer-tools/ to validate and test                         │
│     • Configure storage backend                                         │
│     • Deploy skill to Claude Desktop                                    │
│                                                                          │
│  ⚠️ What NOT to touch:                                                  │
│     • sdk/ folder (template infrastructure)                             │
│     • docs/sdk-developers/ (not relevant to you)                        │
│     • Template CI/CD in sdk/.github/                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

                                     │
                                     │ builds & deploys
                                     ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  LAYER 3: SKILL PACKAGE (What Runs in Claude)                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                │
│                                                                          │
│  👥 Audience: End users (Claude Desktop)                                │
│  🎯 Goal: Provide functionality to Claude users                         │
│                                                                          │
│  📁 Key Folders:                                                         │
│     skill-package/             ← The actual skill code                  │
│     ├── SKILL.md               ← Skill definition (required)            │
│     ├── scripts/               ← Runtime Python code                    │
│     │   ├── storage.py         ← Storage abstraction                    │
│     │   ├── config_loader.py   ← Configuration loading                  │
│     │   └── yaml_utils.py      ← YAML utilities                         │
│     ├── config/                ← Skill configuration                    │
│     ├── modules/               ← Skill modules                          │
│     ├── templates/             ← Skill templates                        │
│     └── user-data-templates/   ← User data structure                    │
│                                                                          │
│     user-data/                 ← Runtime data (created at setup)        │
│     ├── config/                ← User configuration                     │
│     ├── db/                    ← Persistent data                        │
│     └── logs/                  ← Application logs                       │
│                                                                          │
│     requirements.txt           ← Runtime dependencies                   │
│                                                                          │
│  🔧 Runtime Features:                                                    │
│     • Storage abstraction (5 backends)                                  │
│     • Configuration management                                          │
│     • Module system                                                     │
│     • User data persistence                                             │
│                                                                          │
│  📤 Deployment:                                                          │
│     This folder gets uploaded to Claude Desktop and executed            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Information Flow

```
┌────────────┐                ┌────────────┐                ┌────────────┐
│   Layer 1  │                │   Layer 2  │                │   Layer 3  │
│            │  provides      │            │  builds        │            │
│    SDK     │───────────────▶│   Skill    │───────────────▶│   Skill    │
│ Developers │   template     │ Developers │   package      │  Package   │
│            │                │            │                │            │
└────────────┘                └────────────┘                └────────────┘
      │                             │                             │
      │ maintains                   │ uses                        │ runs in
      ▼                             ▼                             ▼
┌────────────┐                ┌────────────┐                ┌────────────┐
│ Template   │                │ Developer  │                │   Claude   │
│ Infrastr.  │                │   Tools    │                │  Desktop   │
└────────────┘                └────────────┘                └────────────┘
```

---

## Folder Ownership Matrix

| Folder | Layer 1 (SDK Dev) | Layer 2 (Skill Dev) | Layer 3 (Runtime) |
|--------|:-----------------:|:-------------------:|:-----------------:|
| `sdk/` | ✅ Owns | ❌ Don't touch | ❌ Not used |
| `developer-tools/` | ✅ Maintains | ✅ Uses | ❌ Not used |
| `skill-package/` | ✅ Provides template | ✅ Modifies | ✅ Executes |
| `user-data/` | ❌ Not used | ✅ Configures | ✅ Reads/writes |
| `docs/sdk-developers/` | ✅ Reads/writes | ❌ Not relevant | ❌ Not used |
| `docs/skill-developers/` | ✅ Maintains | ✅ Reads | ❌ Not used |
| `docs/shared/` | ✅ Reads | ✅ Reads | ❌ Not used |

---

## Typical Workflows

### SDK Developer Workflow (Layer 1)

```
1. Clone template repo
2. Create feature branch
3. Modify sdk/ infrastructure
4. Update docs/sdk-developers/
5. Run SDK tests in sdk/tests/
6. Create PR (CI runs from sdk/.github/workflows/)
7. Merge & release new template version
```

**Files touched:** `sdk/`, `docs/sdk-developers/`, `requirements-dev.txt`

### Skill Developer Workflow (Layer 2)

```
1. Clone/fork template repo
2. Read README.md → docs/skill-developers/getting-started/
3. Run developer-tools/setup.sh
4. Modify skill-package/ (add your skill logic)
5. Run developer-tools/validate.py
6. Configure storage with developer-tools/setup-storage.sh
7. Test locally with skill-package/
8. Deploy to Claude Desktop
```

**Files touched:** `skill-package/`, `user-data/`, possibly `developer-tools/` config

### End User Experience (Layer 3)

```
1. Install skill in Claude Desktop
2. Claude runs skill-package/SKILL.md
3. Skill accesses user-data/ for persistence
4. Skill uses skill-package/scripts/ utilities
5. Storage backend handles data persistence
```

**Files used:** `skill-package/`, `user-data/`, `requirements.txt`

---

## Decision Tree: Which Layer Am I?

```
START
  │
  ├─ Are you improving the template infrastructure itself?
  │  └─ YES → You are Layer 1 (SDK Developer)
  │           • Work in sdk/
  │           • Update docs/sdk-developers/
  │           • Test in sdk/.github/workflows/
  │
  ├─ Are you building a new skill using this template?
  │  └─ YES → You are Layer 2 (Skill Developer)
  │           • Start with README.md
  │           • Use developer-tools/
  │           • Modify skill-package/
  │           • Read docs/skill-developers/
  │
  └─ Are you just using a skill in Claude Desktop?
     └─ YES → You are Layer 3 (End User)
              • You don't need this repo
              • Just install the skill in Claude
```

---

## Color-Coded Reference

### 🔵 SDK Development (Layer 1)
Infrastructure, CI/CD, releases, architecture

### 🟢 Skill Development (Layer 2)
Building skills, using tools, reading docs

### 🟡 Skill Runtime (Layer 3)
Code that runs in Claude Desktop

---

## File Path Quick Reference

### "Where do I find...?"

| What you need | Current location | Proposed location | Layer |
|--------------|------------------|-------------------|-------|
| **Getting started guide** | `docs/getting-started/QUICK_SETUP.md` | `docs/skill-developers/getting-started/QUICK_SETUP.md` | 🟢 2 |
| **Validation script** | `host_scripts/validate.py` | `developer-tools/validate.py` | 🟢 2 |
| **Setup script** | `host_scripts/setup.sh` | `developer-tools/setup.sh` | 🟢 2 |
| **CI/CD workflows** | `.github/workflows/` | `sdk/.github/workflows/` | 🔵 1 |
| **Release script** | `host_scripts/release.sh` | `sdk/scripts/release.sh` | 🔵 1 |
| **Architecture docs** | `docs/design/` | `docs/sdk-developers/architecture/` | 🔵 1 |
| **Storage design** | `docs/design/STORAGE_DESIGN.md` | `docs/sdk-developers/architecture/STORAGE_DESIGN.md` | 🔵 1 |
| **Storage guide** | `docs/developer-guide/storage-selection.md` | `docs/skill-developers/guides/storage-selection.md` | 🟢 2 |
| **Testing guide** | `docs/developer-guide/testing-guide.md` | `docs/skill-developers/guides/testing-guide.md` | 🟢 2 |
| **Skill code** | `skill-package/` | `skill-package/` (unchanged) | 🟡 3 |
| **Storage backend** | `skill-package/scripts/storage.py` | `skill-package/scripts/storage.py` (unchanged) | 🟡 3 |
| **Secrets config** | `config/.gitleaks.toml` | `sdk/config/.gitleaks.toml` | 🔵 1 |
| **Version file** | `config/version.yaml` | `sdk/config/version.yaml` | 🔵 1 |

---

## README.md Strategy

### Current Problem
One README trying to serve everyone (confusing)

### Proposed Solution
Multiple READMEs, each focused on specific audience:

```
README.md                           [Layer 2] Skill developers (main audience)
SDK_DEVELOPMENT.md                  [Layer 1] SDK maintainers
skill-package/README.md             [Layer 3] Skill package documentation
developer-tools/README.md           [Layer 2] Tools guide
sdk/README.md                       [Layer 1] SDK infrastructure guide
docs/README.md                      [Both] Documentation navigation
docs/skill-developers/README.md     [Layer 2] Start here for skill dev
docs/sdk-developers/README.md       [Layer 1] Start here for SDK dev
```

---

## Implementation Checklist

### Phase 1: Structure
- [ ] Create new directories
- [ ] Move files with git mv (preserve history)
- [ ] Update .gitignore paths

### Phase 2: Documentation
- [ ] Create SDK_DEVELOPMENT.md
- [ ] Rewrite README.md for skill developers
- [ ] Create folder-level README.md files
- [ ] Update all internal path references

### Phase 3: Scripts & Tools
- [ ] Update all script paths
- [ ] Update validation script references
- [ ] Update CI/CD workflow paths
- [ ] Test all automation

### Phase 4: Testing
- [ ] Run all tests to verify nothing broke
- [ ] Test on clean clone
- [ ] Validate all documentation links
- [ ] Test setup scripts

### Phase 5: Migration
- [ ] Create migration guide
- [ ] Create automated migration script
- [ ] Tag as v2.0.0
- [ ] Announce breaking changes

---

**Visual Guide Version:** 1.0
**Date:** 2025-11-06
**Companion to:** RESTRUCTURING_PROPOSAL.md
