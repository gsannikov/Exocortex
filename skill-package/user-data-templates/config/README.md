# Configuration Templates

This directory contains configuration templates for the Claude Skills SDK.

## Files

### storage-config-template.yaml
**Purpose:** Storage backend configuration template
**Used for:** Configuring where the skill stores its data

**Usage:**
```bash
cp storage-config-template.yaml storage-config.yaml
# Edit storage-config.yaml with your settings
```

**What it configures:**
- Storage backend type (local, github, checkpoint, email, notion)
- Backend-specific credentials and paths
- Where skill data is persisted

**Location in user setup:**
- Template: `skill-package/user-data-templates/config/storage-config-template.yaml`
- Your config: `user-data/config/storage-config.yaml`

---

## Related Templates

### user-config-template.yaml
**Location:** `user-data/config/user-config-template.yaml`
**Purpose:** Skill-specific user configuration template
**Used for:** Customizing skill behavior, user preferences, and feature settings

**Note:** This is a separate template that lives in the root `user-data/config/` directory (not in `skill-package/user-data-templates/`). It's maintained there for backward compatibility and quick access.

---

## Setup Flow

1. **Copy user-data-templates to user-data:**
   ```bash
   cp -r skill-package/user-data-templates user-data
   ```
   This gives you the basic directory structure with storage-config-template.yaml

2. **Copy user-config-template if needed:**
   ```bash
   cd user-data/config
   cp user-config-template.yaml user-config.yaml
   ```
   (Optional - only if your skill uses user-config)

3. **Configure storage:**
   ```bash
   cd user-data/config
   cp storage-config-template.yaml storage-config.yaml
   # Edit storage-config.yaml
   ```

4. **Customize skill settings:**
   ```bash
   # Edit user-config.yaml if it exists
   ```

---

## Template Purposes Summary

| Template | Location | Purpose | When to Use |
|----------|----------|---------|-------------|
| `storage-config-template.yaml` | `skill-package/user-data-templates/config/` | Storage backend setup | **Always** - Required for all skills |
| `user-config-template.yaml` | `user-data/config/` | Skill customization | **Optional** - Only if skill needs custom config |

---

## Why Two Locations?

**skill-package/user-data-templates/config/storage-config-template.yaml:**
- Part of the portable skill package
- Gets copied when setting up user-data
- Storage configuration is fundamental to all skills

**user-data/config/user-config-template.yaml:**
- Skill-specific configuration
- Maintained in user-data for easy access
- Not all skills need this
- Kept separate for backward compatibility

---

For more information, see:
- [DEPENDENCIES.md](../../../docs/getting-started/DEPENDENCIES.md) - Storage backend details
- [QUICK_SETUP.md](../../../docs/getting-started/QUICK_SETUP.md) - Setup guide
