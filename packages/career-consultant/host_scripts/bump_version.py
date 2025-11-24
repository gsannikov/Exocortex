#!/usr/bin/env python3
"""
Version bumping utility with YAML support.
Reads version.yaml, bumps version, writes back, and syncs to all files.

Usage:
    python -m host_scripts bump-version patch    # 1.2.3 -> 1.2.4
    python -m host_scripts bump-version minor    # 1.2.3 -> 1.3.0
    python -m host_scripts bump-version major    # 1.2.3 -> 2.0.0
    python -m host_scripts bump-version show     # Display current version
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
VERSION_FILE = REPO_ROOT / "version.yaml"


def load_version():
    """Load version from version.yaml."""
    if not VERSION_FILE.exists():
        print(f"Error: {VERSION_FILE} not found")
        sys.exit(1)
    
    with open(VERSION_FILE, 'r') as f:
        data = yaml.safe_load(f)
    
    return data


def save_version(data):
    """Save version to version.yaml."""
    with open(VERSION_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def parse_version(version_str):
    """Parse version string into (major, minor, patch)."""
    parts = version_str.lstrip('v').split('.')
    return tuple(int(p) for p in parts)


def bump_version(current, bump_type):
    """Bump version based on type."""
    major, minor, patch = parse_version(current)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m host_scripts bump-version [patch|minor|major|show]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    data = load_version()
    current_version = data.get('version', '0.0.0')
    
    if action == 'show':
        print(current_version)
        return
    
    if action not in ['patch', 'minor', 'major']:
        print(f"Invalid action: {action}")
        print("Usage: python -m host_scripts bump-version [patch|minor|major|show]")
        sys.exit(1)
    
    new_version = bump_version(current_version, action)
    
    # Update version data
    data['version'] = new_version
    data['release_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Save
    save_version(data)
    
    print(f"{current_version} -> {new_version}")
    
    # Auto-sync version to all documentation files
    try:
        from update_version import update_version_references
        print("Syncing version to documentation files...")
        update_version_references(quiet=True)
        print("✅ Version synced to all files")
    except Exception as e:
        print(f"⚠️  Warning: Failed to auto-sync version: {e}", file=sys.stderr)
        print("   Run 'python -m host_scripts update-version' manually", file=sys.stderr)


if __name__ == "__main__":
    main()
