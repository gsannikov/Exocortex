#!/usr/bin/env python3
"""
Version Synchronization Script

Reads version from version.yaml and updates all version references
across the repository to maintain consistency.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


# Repository root is parent of host_scripts
REPO_ROOT = Path(__file__).parent.parent
VERSION_FILE = REPO_ROOT / "version.yaml"


# Files and their version patterns to update
VERSION_PATTERNS: List[Tuple[Path, str, str]] = [
    # (file_path, regex_pattern, replacement_template)
    (
        REPO_ROOT / "CLAUDE.md",
        r"\*\*Version\*\*:\s*\d+\.\d+\.\d+",
        "**Version**: {version}"
    ),
    (
        REPO_ROOT / "README.md",
        r"\*\*Version\*\*:\s*\d+\.\d+\.\d+",
        "**Version**: {version}"
    ),
    (
        REPO_ROOT / "docs/project/STATUS.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
    (
        REPO_ROOT / "skill-package/SKILL.md",
        r"\*\*Version\*\*:\s*\d+\.\d+\.\d+",
        "**Version**: {version}"
    ),
    (
        REPO_ROOT / "skill-package/modules/scoring-formulas.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
    (
        REPO_ROOT / "skill-package/modules/skills-matching.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
    (
        REPO_ROOT / "skill-package/modules/job-backlog-manager.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
    (
        REPO_ROOT / "skill-package/modules/output-yaml-templates.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
    (
        REPO_ROOT / "skill-package/modules/database-operations-hybrid.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
    (
        REPO_ROOT / "skill-package/modules/company-research.md",
        r"\*\*Version\*\*:\s*v?\d+\.\d+\.\d+",
        "**Version**: v{version}"
    ),
]


def load_version() -> Dict:
    """Load version data from version.yaml."""
    if not VERSION_FILE.exists():
        raise FileNotFoundError(f"Version file not found: {VERSION_FILE}")
    
    with open(VERSION_FILE, 'r') as f:
        data = yaml.safe_load(f)
    
    if 'version' not in data:
        raise ValueError("version.yaml missing 'version' key")
    
    return data


def update_file_version(file_path: Path, pattern: str, replacement: str, version: str, quiet: bool = False) -> bool:
    """
    Update version in a single file.
    
    Args:
        file_path: Path to file to update
        pattern: Regex pattern to match
        replacement: Replacement template with {version} placeholder
        version: Version string to insert
        quiet: Suppress output
    
    Returns:
        True if file was modified, False otherwise
    """
    if not file_path.exists():
        if not quiet:
            print(f"⚠️  Skipping (not found): {file_path.relative_to(REPO_ROOT)}")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Perform replacement
    new_content = re.sub(
        pattern,
        replacement.format(version=version),
        content,
        count=1  # Only replace first occurrence
    )
    
    # Check if anything changed
    if new_content == content:
        if not quiet:
            print(f"✓ Already synced: {file_path.relative_to(REPO_ROOT)}")
        return False
    
    # Write updated content
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    if not quiet:
        print(f"✓ Updated: {file_path.relative_to(REPO_ROOT)}")
    
    return True


def update_version_references(quiet: bool = False) -> None:
    """
    Update all version references across the repository.
    
    Args:
        quiet: If True, suppress all output except errors
    """
    # Load current version
    version_data = load_version()
    version = version_data['version']
    
    if not quiet:
        print(f"Syncing version references to: {version}")
        print("=" * 50)
    
    # Update all files
    updated_count = 0
    for file_path, pattern, replacement in VERSION_PATTERNS:
        if update_file_version(file_path, pattern, replacement, version, quiet):
            updated_count += 1
    
    if not quiet:
        print("=" * 50)
        print(f"✅ Sync complete: {updated_count} file(s) updated")


if __name__ == "__main__":
    # Allow running directly for testing
    update_version_references(quiet=False)
