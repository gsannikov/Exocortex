#!/usr/bin/env python3
"""
Claude Skill Validation Script
Validates skill structure, configuration, and integrity
"""

import os
import sys
import yaml
from pathlib import Path
from typing import List, Tuple

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class SkillValidator:
    def __init__(self, skill_root: str):
        self.skill_root = Path(skill_root)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("🔍 Validating Claude Skill Structure...\n")
        
        checks = [
            ("Directory Structure", self.validate_structure),
            ("SKILL.md Format", self.validate_skill_md),
            ("Configuration Files", self.validate_config),
            ("Python Scripts", self.validate_scripts),
            ("Templates", self.validate_templates),
            ("Documentation", self.validate_docs),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            passed = check_func()
            if not passed:
                all_passed = False
                
        # Print summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        if self.warnings:
            print(f"\n{YELLOW}⚠️  Warnings ({len(self.warnings)}):{RESET}")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errors:
            print(f"\n{RED}❌ Errors ({len(self.errors)}):{RESET}")
            for error in self.errors:
                print(f"  • {error}")
        
        if all_passed and not self.errors:
            print(f"\n{GREEN}✅ All validations passed!{RESET}")
            return True
        else:
            print(f"\n{RED}❌ Validation failed{RESET}")
            return False
    
    def validate_structure(self) -> bool:
        """Check directory structure is correct"""
        print("Checking directory structure...")
        
        required_dirs = [
            "skill-package",
            "skill-package/config",
            "skill-package/modules",
            "skill-package/scripts",
            "user-data",
            "user-data/config",
            "user-data/db",
            "user-data/logs",
        ]
        
        optional_dirs = [
            "docs",
            "docs/skill-developers",
            "docs/sdk-developers",
            "developer-tools",
            "sdk/.github",
        ]
        
        all_exist = True
        for dir_path in required_dirs:
            full_path = self.skill_root / dir_path
            if not full_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
                all_exist = False
        
        for dir_path in optional_dirs:
            full_path = self.skill_root / dir_path
            if not full_path.exists():
                self.warnings.append(f"Optional directory not found: {dir_path}")
        
        if all_exist:
            print(f"{GREEN}✅ Directory structure valid{RESET}")
        return all_exist
    
    def validate_skill_md(self) -> bool:
        """Check SKILL.md has required sections"""
        print("Checking SKILL.md...")
        
        skill_md_path = self.skill_root / "skill-package" / "SKILL.md"
        
        if not skill_md_path.exists():
            self.errors.append("SKILL.md not found")
            return False
        
        with open(skill_md_path, 'r') as f:
            content = f.read()
        
        required_sections = [
            "# ",  # Title
            "## Overview",
            "## ⚠️ CRITICAL: Storage Configuration",
        ]
        
        all_present = True
        for section in required_sections:
            if section not in content:
                self.errors.append(f"SKILL.md missing section: {section}")
                all_present = False
        
        if all_present:
            print(f"{GREEN}✅ SKILL.md structure valid{RESET}")
        return all_present
    
    def validate_config(self) -> bool:
        """Check configuration files are valid"""
        print("Checking configuration files...")
        
        # Check paths.py
        paths_py = self.skill_root / "skill-package" / "config" / "paths.py"
        if not paths_py.exists():
            self.errors.append("config/paths.py not found")
            return False
        
        # Check user config template
        user_config_template = self.skill_root / "user-data" / "config" / "user-config-template.yaml"
        if not user_config_template.exists():
            self.warnings.append("user-config-template.yaml not found")
        else:
            # Validate YAML syntax
            try:
                with open(user_config_template, 'r') as f:
                    yaml.safe_load(f)
                print(f"{GREEN}✅ Configuration files valid{RESET}")
            except yaml.YAMLError as e:
                self.errors.append(f"Invalid YAML in user-config-template.yaml: {e}")
                return False
        
        return True
    
    def validate_scripts(self) -> bool:
        """Check Python scripts are present"""
        print("Checking Python scripts...")
        
        required_scripts = [
            "skill-package/scripts/yaml_utils.py",
            "skill-package/scripts/config_loader.py",
        ]
        
        all_exist = True
        for script_path in required_scripts:
            full_path = self.skill_root / script_path
            if not full_path.exists():
                self.errors.append(f"Missing script: {script_path}")
                all_exist = False
        
        if all_exist:
            print(f"{GREEN}✅ Python scripts present{RESET}")
        return all_exist
    
    def validate_templates(self) -> bool:
        """Check templates directory"""
        print("Checking templates...")
        
        templates_dir = self.skill_root / "skill-package" / "templates"
        if not templates_dir.exists():
            self.warnings.append("Templates directory not found")
            return True  # Not critical
        
        print(f"{GREEN}✅ Templates directory exists{RESET}")
        return True
    
    def validate_docs(self) -> bool:
        """Check documentation"""
        print("Checking documentation...")
        
        readme = self.skill_root / "README.md"
        if not readme.exists():
            self.errors.append("README.md not found")
            return False
        
        print(f"{GREEN}✅ Documentation present{RESET}")
        return True


def main():
    # Determine skill root (assume script is in developer-tools/)
    script_dir = Path(__file__).parent
    skill_root = script_dir.parent
    
    print(f"Skill root: {skill_root}\n")
    
    validator = SkillValidator(str(skill_root))
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
