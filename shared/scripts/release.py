#!/usr/bin/env python3
"""
Claude Skills - Unified Release Script

Usage:
    python release.py career-consultant --patch
    python release.py all --minor
    python release.py reading-list --major --dry-run
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

# Skill configurations
SKILL_CONFIG = {
    'career-consultant': {
        'has_host_scripts': True,
        'has_tests': True,
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
    'reading-list': {
        'has_host_scripts': False,
        'has_tests': False,
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
    'ideas-capture': {
        'has_host_scripts': False,
        'has_tests': False,
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
    'voice-memos': {
        'has_host_scripts': False,
        'has_tests': False,
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
    'local-rag': {
        'has_host_scripts': True,
        'has_tests': True,
        'version_file': 'version.yaml',
        'changelog': 'CHANGELOG.md',
    },
}

REPO_ROOT = Path(__file__).parent.parent.parent
PACKAGES_DIR = REPO_ROOT / 'packages'


def get_current_version(skill_name: str) -> str:
    """Read current version from skill's version file."""
    config = SKILL_CONFIG[skill_name]
    version_path = PACKAGES_DIR / skill_name / config['version_file']
    
    if not version_path.exists():
        return '0.0.0'
    
    with open(version_path) as f:
        data = yaml.safe_load(f)
        return data.get('version', '0.0.0')


def bump_version(version: str, bump_type: str) -> str:
    """Bump version according to semver."""
    parts = version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2].split('-')[0])
    
    if bump_type == 'major':
        return f'{major + 1}.0.0'
    elif bump_type == 'minor':
        return f'{major}.{minor + 1}.0'
    else:  # patch
        return f'{major}.{minor}.{patch + 1}'


def update_version_file(skill_name: str, new_version: str, dry_run: bool = False):
    """Update the version file with new version."""
    config = SKILL_CONFIG[skill_name]
    version_path = PACKAGES_DIR / skill_name / config['version_file']
    
    version_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        'version': new_version,
        'updated': datetime.now().strftime('%Y-%m-%d'),
        'skill': skill_name,
    }
    
    if dry_run:
        print(f"[DRY RUN] Would update {version_path}:")
        print(yaml.dump(data))
    else:
        with open(version_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        print(f"✅ Updated {version_path}")


def update_changelog(skill_name: str, new_version: str, dry_run: bool = False):
    """Add new version entry to changelog."""
    config = SKILL_CONFIG[skill_name]
    changelog_path = PACKAGES_DIR / skill_name / config['changelog']
    
    if not changelog_path.exists():
        content = f"# Changelog\n\n## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n- Initial release\n"
        if dry_run:
            print(f"[DRY RUN] Would create {changelog_path}")
        else:
            with open(changelog_path, 'w') as f:
                f.write(content)
        return
    
    with open(changelog_path) as f:
        content = f.read()
    
    # Add new version section after # Changelog
    new_entry = f"\n## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n- Release {new_version}\n"
    content = content.replace('# Changelog\n', f'# Changelog\n{new_entry}', 1)
    
    if dry_run:
        print(f"[DRY RUN] Would update {changelog_path}")
    else:
        with open(changelog_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated {changelog_path}")


def run_tests(skill_name: str) -> bool:
    """Run tests if configured."""
    config = SKILL_CONFIG[skill_name]
    if not config['has_tests']:
        print(f"ℹ️  No tests configured for {skill_name}")
        return True
    
    test_path = PACKAGES_DIR / skill_name / 'tests'
    if not test_path.exists():
        print(f"⚠️  Tests directory not found: {test_path}")
        return True
    
    # Run from REPO_ROOT with absolute path to avoid pytest.ini in subdirs
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', str(test_path.absolute()), '--rootdir', str(REPO_ROOT)],
        capture_output=True,
        cwd=REPO_ROOT
    )
    if result.returncode != 0:
        print(f"❌ Tests failed for {skill_name}")
        print(result.stdout.decode())
        print(result.stderr.decode())
        return False
    
    print(f"✅ Tests passed for {skill_name}")
    return True


def create_git_tag(skill_name: str, version: str, dry_run: bool = False):
    """Create git tag for the release."""
    tag_name = f"{skill_name}-v{version}"
    
    if dry_run:
        print(f"[DRY RUN] Would create tag: {tag_name}")
        return
    
    subprocess.run(['git', 'add', '-A'], cwd=REPO_ROOT)
    subprocess.run(['git', 'commit', '-m', f'Release {skill_name} v{version}'], cwd=REPO_ROOT)
    subprocess.run(['git', 'tag', '-a', tag_name, '-m', f'Release {skill_name} v{version}'], cwd=REPO_ROOT)
    print(f"✅ Created tag: {tag_name}")


import shutil
import glob

def create_package(skill_name: str, version: str, dry_run: bool = False):
    """Create a compressed package for the skill."""
    print(f"\n📦 Packaging {skill_name} v{version}...")
    
    # Ensure releases dir exists
    releases_dir = REPO_ROOT / 'releases'
    if not releases_dir.exists():
        releases_dir.mkdir(exist_ok=True)
    
    # Cleanup old releases for this specific skill/version to avoid stale files
    # We match pattern: skill_name-v*.zip
    # But specifically checking for the current one to be safe, 
    # though usually we want to keep history? 
    # The user asked not to "overhelp repo with historical packages", 
    # but that was about git history. Local releases/ dir is gitignored.
    # To be safe and clean, we'll remove ANY existing file with this exact target name.
    
    target_base = releases_dir / f"{skill_name}-v{version}"
    target_zip = releases_dir / f"{skill_name}-v{version}.zip"
    
    if target_zip.exists():
        if dry_run:
             print(f"[DRY RUN] Would remove existing: {target_zip}")
        else:
             target_zip.unlink()
             print(f"   Removed existing: {target_zip.name}")

    if dry_run:
        print(f"[DRY RUN] Would create zip package: {target_zip}")
        return

    # Create zip
    # We want the zip to contain the CONTENT of the package, 
    # so we set root_dir to packages/{skill} and base_dir to .
    package_dir = PACKAGES_DIR / skill_name
    
    try:
        shutil.make_archive(
            str(target_base), 
            'zip', 
            root_dir=package_dir, 
            base_dir='.'
        )
        print(f"✅ Created package: {target_zip.name}")
        print(f"   Path: {target_zip}")
    except Exception as e:
        print(f"❌ Failed to create package: {e}")
        raise


def release_skill(skill_name: str, bump_type: str, dry_run: bool = False, skip_tests: bool = False) -> tuple[bool, str]:
    """Execute full release process for a skill."""
    print(f"\n{'='*50}")
    print(f"Releasing {skill_name} ({bump_type})")
    print(f"{'='*50}\n")

    # Get current and new version
    current = get_current_version(skill_name)
    new_version = bump_version(current, bump_type)
    print(f"Version: {current} → {new_version}")

    # Run tests
    if not skip_tests and not run_tests(skill_name):
        print("❌ Release aborted due to test failures")
        return False, ''

    # Update version file
    update_version_file(skill_name, new_version, dry_run)

    # Update changelog
    update_changelog(skill_name, new_version, dry_run)

    # Create package
    create_package(skill_name, new_version, dry_run)

    # Create git tag
    if not dry_run:
        create_git_tag(skill_name, new_version, dry_run)

    print(f"\n✅ {'[DRY RUN] ' if dry_run else ''}Released {skill_name} v{new_version}")
    return True, new_version


def main():
    parser = argparse.ArgumentParser(description='Release Claude Skills')
    parser.add_argument('skill', choices=list(SKILL_CONFIG.keys()) + ['all'],
                       help='Skill to release (or "all")')
    parser.add_argument('--patch', action='store_true', help='Patch release')
    parser.add_argument('--minor', action='store_true', help='Minor release')
    parser.add_argument('--major', action='store_true', help='Major release')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--skip-tests', action='store_true', help='Skip running tests')

    args = parser.parse_args()

    # Determine bump type
    if args.major:
        bump_type = 'major'
    elif args.minor:
        bump_type = 'minor'
    else:
        bump_type = 'patch'

    # Release skill(s)
    skills = list(SKILL_CONFIG.keys()) if args.skill == 'all' else [args.skill]
    released_version = ''

    for skill in skills:
        success, version = release_skill(skill, bump_type, args.dry_run, args.skip_tests)
        if not success:
            sys.exit(1)
        released_version = version

    # Output version for GitHub Actions
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output and released_version:
        with open(github_output, 'a') as f:
            f.write(f"version={released_version}\n")

    if not args.dry_run:
        print("\n🎉 Release complete! Don't forget to push:")
        print("   git push origin main --tags")


if __name__ == '__main__':
    main()
