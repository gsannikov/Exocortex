#!/usr/bin/env python3
"""
Interactive release workflow guide.

Guides developers through the release process step-by-step:
- Validates package
- Bumps version
- Commits changes
- Creates git tag
- Pushes to GitHub

GitHub Actions automatically handles creating the release page.

Usage:
    python -m host_scripts release
    python -m host_scripts release --patch
    python -m host_scripts release --dry-run
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional
import zipfile
import os

# Import from other host_scripts modules
from bump_version import load_version, parse_version
import re


def get_github_repo_url() -> Optional[str]:
    """Get the GitHub repository URL from git config."""
    try:
        # Try to get remote origin url
        result = subprocess.run(
            "git remote get-url origin", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            return None
            
        url = result.stdout.strip()
        
        # Convert SSH to HTTPS if needed
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
            
        # Remove .git extension
        if url.endswith(".git"):
            url = url[:-4]
            
        return url
    except:
        return None


def update_latest_release_link(version: str):
    """
    Create a link file to the latest release in the releases folder.
    
    Args:
        version: The version number (e.g., '9.24.1')
    """
    repo_url = get_github_repo_url()
    if not repo_url:
        print("⚠️  Could not determine GitHub URL, skipping link creation")
        return

    release_url = f"{repo_url}/releases/tag/v{version}"
    link_file = Path("releases/LATEST_RELEASE.md")
    
    try:
        # Ensure releases dir exists
        link_file.parent.mkdir(exist_ok=True)
        
        with open(link_file, 'w') as f:
            f.write(f"# Latest Release: v{version}\n\n")
            f.write(f"Download and view release notes here:\n")
            f.write(f"[{release_url}]({release_url})\n")
            
        print(f"  ✓ Created release link: {link_file}")
        print(f"  🔗 URL: {release_url}")
        
    except Exception as e:
        print(f"⚠️  Failed to create release link: {e}")


def build_local_artifact(version: str):
    """
    Build the .skill artifact locally.
    
    Args:
        version: The version number
    """
    artifact_name = f"israeli-tech-career-consultant-{version}.skill"
    output_path = Path("releases") / artifact_name
    source_dir = Path("skill-package")
    
    print(f"  📦 Building {artifact_name}...")
    
    try:
        # Ensure releases dir exists
        output_path.parent.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                # Skip __pycache__ and .DS_Store
                dirs[:] = [d for d in dirs if d != '__pycache__']
                
                for file in files:
                    if file == '.DS_Store':
                        continue
                        
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(source_dir.parent)
                    zipf.write(file_path, arcname)
                    
        print(f"  ✓ Created artifact: {output_path}")
        
    except Exception as e:
        print(f"⚠️  Failed to build artifact: {e}")


def run_command(cmd: str, description: str, capture: bool = True) -> Optional[str]:
    """
    Run a shell command with nice output.
    
    Args:
        cmd: Command to run
        description: Human-readable description
        capture: Whether to capture output
    
    Returns:
        Command output if capture=True, None otherwise
    """
    print(f"  ✓ {description}")
    
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ Failed: {result.stderr}")
            sys.exit(1)
        return result.stdout.strip()
    else:
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"  ✗ Command failed with exit code {result.returncode}")
            sys.exit(1)
        return None


def confirm(prompt: str) -> bool:
    """Ask user for confirmation."""
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ['y', 'yes']


def calculate_new_version(current: str, bump_type: str) -> str:
    """Calculate what the new version will be."""
    major, minor, patch = parse_version(current)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def interactive_release(dry_run: bool = False):
    """Guide user through interactive release process."""
    print("🚀 Release Workflow Guide")
    print("━" * 42)
    
    # Get current version
    data = load_version()
    current = data['version']
    print(f"\nCurrent version: {current}\n")
    
    # Choose bump type
    print("What type of release?")
    patch_new = calculate_new_version(current, 'patch')
    minor_new = calculate_new_version(current, 'minor')
    major_new = calculate_new_version(current, 'major')
    
    print(f"  [1] Patch ({current} → {patch_new}) - Bug fixes")
    print(f"  [2] Minor ({current} → {minor_new}) - New features")
    print(f"  [3] Major ({current} → {major_new}) - Breaking changes")
    
    choice = input("\nChoice: ").strip()
    bump_type = {'1': 'patch', '2': 'minor', '3': 'major'}.get(choice)
    
    if not bump_type:
        print("❌ Invalid choice")
        sys.exit(1)
    
    new_version = calculate_new_version(current, bump_type)
    
    if dry_run:
        print(f"\n[DRY RUN] Would release v{new_version}")
        print("\nSteps that would be executed:")
        print("  1. python -m host_scripts validate all")
        print(f"  2. python -m host_scripts bump-version {bump_type}")
        print("  3. git add .")
        print(f'  4. git commit -m "chore: release v{new_version}"')
        print(f"  5. git tag v{new_version}")
        print("  6. git push origin main")
        print("  7. git push --tags")
        return
    
    # Step 1: Validate
    print("\nStep 1/6: Validating package...")
    run_command("python -m host_scripts validate all", "Running validation", capture=False)
    
    # Step 2: Bump version
    print("\nStep 2/6: Bumping version...")
    run_command(
        f"python -m host_scripts bump-version {bump_type}",
        f"Bumping version to {new_version}",
        capture=False
    )
    
    # Step 3: Review changes
    print("\nStep 3/6: Review changes")
    print("\nModified files:")
    run_command("git status --short", "git status", capture=False)
    
    if not confirm("\n📋 Continue with release?"):
        print("❌ Release aborted")
        sys.exit(0)
    
    # Step 4: Commit
    print("\nStep 4/6: Committing changes...")
    run_command("git add .", "Staging changes")
    run_command(
        f'git commit -m "chore: release v{new_version}"',
        f"Creating commit for v{new_version}"
    )
    
    # Step 5: Create tag
    print("\nStep 5/6: Creating git tag...")
    run_command(f"git tag v{new_version}", f"Creating tag v{new_version}")
    
    # Step 6: Push
    print("\nStep 6/6: Pushing to GitHub...")
    if not confirm("🚀 Push to GitHub?"):
        print("⚠️  Changes committed locally but not pushed")
        print(f"   To push manually: git push origin main --tags")
        sys.exit(0)
    
    run_command("git push origin main", "Pushing commits")
    run_command("git push --tags", "Pushing tags")
    
    # Step 7: Create release link
    print("\nStep 7/8: Updating release link...")
    update_latest_release_link(new_version)

    # Step 8: Build local artifact
    print("\nStep 8/8: Building local artifact...")
    build_local_artifact(new_version)
    
    # Success!
    print(f"\n✅ Release v{new_version} complete!")
    print("\n" + "━" * 42)
    print("GitHub Actions will automatically:")
    print("  • Create GitHub Release page")
    print("  • Upload .skill artifact")
    print("  • Publish release notes")
    print("\nView releases: https://github.com/gsannikov/israeli-tech-career-consultant/releases")


def preset_release(bump_type: str, dry_run: bool = False):
    """Non-interactive release with preset bump type."""
    data = load_version()
    current = data['version']
    new_version = calculate_new_version(current, bump_type)
    
    print(f"🚀 Releasing v{new_version} ({bump_type})")
    
    if dry_run:
        print(f"\n[DRY RUN] Would release {current} → {new_version}")
        return
    
    print("\n1/6 Validating...")
    run_command("python -m host_scripts validate all", "Validation", capture=False)
    
    print("\n2/6 Bumping version...")
    run_command(f"python -m host_scripts bump-version {bump_type}", "Version bump", capture=False)
    
    print("\n3/6 Committing...")
    run_command("git add .", "Staging")
    run_command(f'git commit -m "chore: release v{new_version}"', "Committing")
    
    print("\n4/6 Tagging...")
    run_command(f"git tag v{new_version}", "Creating tag")
    
    print("\n5/6 Pushing...")
    run_command("git push origin main", "Pushing commits")
    run_command("git push --tags", "Pushing tags")
    
    print("\n6/8 Updating link...")
    update_latest_release_link(new_version)

    print("\n7/8 Building artifact...")
    build_local_artifact(new_version)
    
    print(f"\n✅ Release v{new_version} complete!")


def main():
    """Main entry point."""
    # Parse arguments
    dry_run = '--dry-run' in sys.argv
    
    # Check for preset bump type
    if '--patch' in sys.argv:
        preset_release('patch', dry_run)
    elif '--minor' in sys.argv:
        preset_release('minor', dry_run)
    elif '--major' in sys.argv:
        preset_release('major', dry_run)
    else:
        # Interactive mode
        interactive_release(dry_run)


if __name__ == "__main__":
    main()
