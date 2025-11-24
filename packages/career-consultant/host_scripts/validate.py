#!/usr/bin/env python3
"""
Validation script for skill package and documentation structure.
Consolidates validation logic from multiple Python modules.

Usage:
    ./validate docs       - Validate documentation structure
    ./validate package    - Validate skill package structure
    ./validate all        - Run all validations
"""

import sys
import yaml
from pathlib import Path
from typing import List, Tuple, Optional
import re
import compileall

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent
DOCS_ROOT = REPO_ROOT / "docs"
SKILL_PACKAGE_DIR = REPO_ROOT / "skill-package"

# =============================================================================
# Documentation Structure Validation
# =============================================================================


def validate_docs_structure() -> bool:
    """Validate documentation structure and naming conventions."""
    print("\n" + "=" * 70)
    print("Documentation Structure Validation")
    print("=" * 70)
    print(f"  Project Root: {REPO_ROOT}")
    print(f"  Docs Root: {DOCS_ROOT}")

    all_passed = True

    # Check required directories
    print("\n" + "=" * 70)
    print("Checking Required Directories")
    print("=" * 70)
    
    required_dirs = [
        "guides",
        "project",
        "project/bugs",
        "meta",
    ]
    
    missing = []
    for dir_path in required_dirs:
        full_path = DOCS_ROOT / dir_path
        if not full_path.exists() or not full_path.is_dir():
            missing.append(dir_path)
    
    if missing:
        print(f"✗ Missing {len(missing)} required directories:")
        for d in missing:
            print(f"    - {d}")
        all_passed = False
    else:
        print(f"✓ All {len(required_dirs)} required directories exist")

    # Check naming conventions
    print("\n" + "=" * 70)
    print("Checking Naming Conventions")
    print("=" * 70)
    
    allowed_special_cases = [
        "README", "INDEX", "PROJECT_PLAN", "MASTER_FIX_GUIDE",
        "FEATURES", "ROADMAP", "STRATEGY", "MARKETING", "STATUS",
        "USER_GUIDE", "DEVELOPER_GUIDE", "CREDITS",
    ]
    
    issues = []
    for md_file in DOCS_ROOT.rglob("*.md"):
        if md_file.name.startswith("_") or md_file.name.startswith("."):
            continue
        if "meta" in md_file.parts:
            continue
        
        file_name = md_file.stem
        
        # Check if allowed
        if file_name.upper() in allowed_special_cases:
            continue
        if file_name.startswith("BUG_") or file_name.startswith("CRITICAL_"):
            continue
        
        # Check for uppercase
        if any(c.isupper() for c in file_name):
            issues.append((str(md_file.relative_to(DOCS_ROOT)), "Contains uppercase letters"))
        
        # Check for underscores
        if "_" in file_name:
            issues.append((str(md_file.relative_to(DOCS_ROOT)), "Uses underscores instead of hyphens"))
    
    if issues:
        print(f"⚠ Found {len(issues)} naming convention issues:")
        for path, issue in issues:
            print(f"    - {path}: {issue}")
        print("  \nRecommendation: Use kebab-case for all markdown files")
    else:
        print("✓ All files follow naming conventions")

    # Check required files
    print("\n" + "=" * 70)
    print("Checking Required Files")
    print("=" * 70)
    
    required_files = [
        "README.md",
        "DOCS_INDEX.yaml",
        "quick-reference.md",
        "guides/USER_GUIDE.md",
        "guides/DEVELOPER_GUIDE.md",
        "project/FEATURES.md",
        "project/ROADMAP.md",
        "project/STRATEGY.md",
        "project/MARKETING.md",
        "project/STATUS.md",
        "meta/CHANGELOG.md",
        "meta/CONTRIBUTING.md",
        "meta/CODE_OF_CONDUCT.md",
        "meta/CREDITS.md",
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = DOCS_ROOT / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"✗ Missing {len(missing_files)} required files:")
        for f in missing_files:
            print(f"    - {f}")
        all_passed = False
    else:
        print(f"✓ All {len(required_files)} required files exist")

    # Summary
    print("\n" + "=" * 70)
    print("Validation Summary")
    print("=" * 70)
    
    if all_passed and not issues:
        print("✓ Validation PASSED - Structure is correct!")
    elif all_passed:
        print("⚠ Validation PASSED with warnings")
    else:
        print("✗ Validation FAILED - Errors found that need fixing")
    
    return all_passed and not issues


# =============================================================================
# Skill Package Validation
# =============================================================================


def validate_skill_package() -> bool:
    """Validate skill package structure."""
    print("\n" + "=" * 70)
    print("Skill Package Validation")
    print("=" * 70)
    print(f"  Skill Package: {SKILL_PACKAGE_DIR}")

    all_passed = True

    # Check required directories
    required_dirs = ["modules", "scripts", "templates", "config"]
    missing = []
    
    for dir_name in required_dirs:
        dir_path = SKILL_PACKAGE_DIR / dir_name
        if not dir_path.exists():
            missing.append(dir_name)
    
    if missing:
        print(f"✗ Missing required directories: {', '.join(missing)}")
        all_passed = False
    else:
        print(f"✓ All required directories exist")

    # Check SKILL.md exists
    skill_md = SKILL_PACKAGE_DIR / "SKILL.md"
    if not skill_md.exists():
        print("✗ SKILL.md not found")
        all_passed = False
    else:
        print("✓ SKILL.md exists")

    # Compile Python scripts
    scripts_dir = SKILL_PACKAGE_DIR / "scripts"
    if scripts_dir.exists():
        print("\nCompiling Python scripts...")
        success = compileall.compile_dir(str(scripts_dir), quiet=1)
        if not success:
            print("✗ Python syntax errors detected in scripts")
            all_passed = False
        else:
            print("✓ All Python scripts compiled successfully")

    # Check module frontmatter
    modules_dir = SKILL_PACKAGE_DIR / "modules"
    if modules_dir.exists():
        print("\nChecking module frontmatter...")
        errors = []
        
        for module_path in sorted(modules_dir.glob("*.md")):
            content = module_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            
            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append(f"{module_path.name}: Invalid frontmatter structure")
                continue
            
            try:
                yaml.safe_load(parts[1])
                print(f"  ✓ {module_path.name} frontmatter valid")
            except yaml.YAMLError as exc:
                errors.append(f"{module_path.name}: {exc}")
        
        if errors:
            print("\n✗ YAML frontmatter errors:")
            for error in errors:
                print(f"  - {error}")
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ Skill package validation PASSED")
    else:
        print("✗ Skill package validation FAILED")
    print("=" * 70)
    
    return all_passed


# =============================================================================
# Main
# =============================================================================


def main():
    if len(sys.argv) < 2:
        print("Usage: ./validate [docs|package|all]")
        sys.exit(1)
    
    target = sys.argv[1].lower()
    
    if target == "docs":
        success = validate_docs_structure()
    elif target == "package":
        success = validate_skill_package()
    elif target == "all":
        docs_ok = validate_docs_structure()
        pkg_ok = validate_skill_package()
        success = docs_ok and pkg_ok
    else:
        print(f"Unknown target: {target}")
        print("Usage: ./validate [docs|package|all]")
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
