#!/usr/bin/env python3
"""
Test suite for Meeting Recorder skill validation.
Validates SKILL.md structure, config files, and documentation.
"""

import os
import re
import sys
import yaml
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_pass(msg):
    print(f"  {Colors.GREEN}✓{Colors.RESET} {msg}")

def print_fail(msg):
    print(f"  {Colors.RED}✗{Colors.RESET} {msg}")

def print_warn(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_section(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}")

# Get paths
SCRIPT_DIR = Path(__file__).parent
MEETING_RECORDER_DIR = SCRIPT_DIR.parent
VOICE_MEMOS_DIR = MEETING_RECORDER_DIR.parent
SKILLS_DIR = VOICE_MEMOS_DIR / "skills"

# Test results
passed = 0
failed = 0
warnings = 0


def test_skill_md_exists():
    """Test that meeting-transcription-SKILL.md exists"""
    global passed, failed
    skill_path = SKILLS_DIR / "meeting-transcription-SKILL.md"

    if skill_path.exists():
        print_pass(f"SKILL.md exists at {skill_path.relative_to(VOICE_MEMOS_DIR)}")
        passed += 1
        return True
    else:
        print_fail(f"SKILL.md not found at {skill_path}")
        failed += 1
        return False


def test_skill_md_structure():
    """Test that SKILL.md has required sections"""
    global passed, failed, warnings
    skill_path = SKILLS_DIR / "meeting-transcription-SKILL.md"

    if not skill_path.exists():
        print_fail("Cannot test structure - file missing")
        failed += 1
        return

    content = skill_path.read_text()

    required_sections = [
        ("# Meeting Transcription Skill", "Title"),
        ("## Overview", "Overview section"),
        ("## Trigger Commands", "Trigger commands"),
        ("## Data Locations", "Data locations"),
        ("## Processing Pipeline", "Processing pipeline"),
        ("## Error Handling", "Error handling"),
    ]

    for pattern, name in required_sections:
        if pattern in content:
            print_pass(f"Has {name}")
            passed += 1
        else:
            print_fail(f"Missing {name}")
            failed += 1

    # Check for code blocks
    code_blocks = re.findall(r'```\w*\n', content)
    if len(code_blocks) >= 3:
        print_pass(f"Has {len(code_blocks)} code blocks")
        passed += 1
    else:
        print_warn(f"Only {len(code_blocks)} code blocks (expected >= 3)")
        warnings += 1


def test_skill_md_commands():
    """Test that SKILL.md defines expected commands"""
    global passed, failed
    skill_path = SKILLS_DIR / "meeting-transcription-SKILL.md"

    if not skill_path.exists():
        return

    content = skill_path.read_text()

    expected_commands = [
        "process meeting",
        "transcribe meeting",
    ]

    for cmd in expected_commands:
        if cmd.lower() in content.lower():
            print_pass(f"Documents command: '{cmd}'")
            passed += 1
        else:
            print_fail(f"Missing command documentation: '{cmd}'")
            failed += 1


def test_readme_exists():
    """Test that README.md exists"""
    global passed, failed
    readme_path = MEETING_RECORDER_DIR / "README.md"

    if readme_path.exists():
        print_pass("README.md exists")
        passed += 1
        return True
    else:
        print_fail("README.md not found")
        failed += 1
        return False


def test_readme_content():
    """Test README.md has required sections"""
    global passed, failed, warnings
    readme_path = MEETING_RECORDER_DIR / "README.md"

    if not readme_path.exists():
        return

    content = readme_path.read_text()

    required_sections = [
        ("## Features", "Features section"),
        ("## Requirements", "Requirements section"),
        ("## Quick Install", "Installation instructions"),
        ("## Usage", "Usage instructions"),
        ("## Permissions", "Permissions documentation"),
    ]

    for pattern, name in required_sections:
        if pattern in content:
            print_pass(f"README has {name}")
            passed += 1
        else:
            print_warn(f"README missing {name}")
            warnings += 1


def test_setup_script():
    """Test that setup.sh exists and is executable"""
    global passed, failed
    setup_path = MEETING_RECORDER_DIR / "setup.sh"

    if not setup_path.exists():
        print_fail("setup.sh not found")
        failed += 1
        return

    print_pass("setup.sh exists")
    passed += 1

    # Check if executable (on Unix)
    if os.access(setup_path, os.X_OK):
        print_pass("setup.sh is executable")
        passed += 1
    else:
        print_fail("setup.sh is not executable")
        failed += 1

    # Check shebang
    content = setup_path.read_text()
    if content.startswith("#!/bin/bash"):
        print_pass("setup.sh has bash shebang")
        passed += 1
    else:
        print_fail("setup.sh missing bash shebang")
        failed += 1


def test_config_example():
    """Test that config.yaml.example exists and is valid"""
    global passed, failed, warnings
    config_path = MEETING_RECORDER_DIR / "config.yaml.example"

    if not config_path.exists():
        print_fail("config.yaml.example not found")
        failed += 1
        return

    print_pass("config.yaml.example exists")
    passed += 1

    # Try to parse YAML
    try:
        content = config_path.read_text()
        # Remove comments for parsing
        yaml_content = '\n'.join(
            line for line in content.split('\n')
            if not line.strip().startswith('#')
        )
        if yaml_content.strip():
            data = yaml.safe_load(yaml_content)
            print_pass("config.yaml.example is valid YAML")
            passed += 1
        else:
            print_warn("config.yaml.example has no YAML content (all comments)")
            warnings += 1
    except yaml.YAMLError as e:
        print_fail(f"config.yaml.example has invalid YAML: {e}")
        failed += 1


def test_swift_package():
    """Test that Package.swift exists and has correct structure"""
    global passed, failed
    package_path = MEETING_RECORDER_DIR / "MeetingRecorder" / "Package.swift"

    if not package_path.exists():
        print_fail("Package.swift not found")
        failed += 1
        return

    print_pass("Package.swift exists")
    passed += 1

    content = package_path.read_text()

    # Check for required elements
    checks = [
        ("swift-tools-version", "Swift tools version"),
        (".macOS(.v13)", "macOS 13 platform requirement"),
        ("MeetingRecorder", "Product name"),
        ("testTarget", "Test target"),
    ]

    for pattern, name in checks:
        if pattern in content:
            print_pass(f"Package.swift has {name}")
            passed += 1
        else:
            print_fail(f"Package.swift missing {name}")
            failed += 1


def test_swift_sources():
    """Test that all required Swift source files exist"""
    global passed, failed
    sources_dir = MEETING_RECORDER_DIR / "MeetingRecorder" / "Sources"

    required_files = [
        "main.swift",
        "AppDelegate.swift",
        "AudioCapture.swift",
        "MeetingDetector.swift",
        "Config.swift",
    ]

    for filename in required_files:
        filepath = sources_dir / filename
        if filepath.exists():
            print_pass(f"Source file exists: {filename}")
            passed += 1
        else:
            print_fail(f"Source file missing: {filename}")
            failed += 1


def test_swift_tests():
    """Test that Swift test files exist"""
    global passed, failed, warnings
    tests_dir = MEETING_RECORDER_DIR / "MeetingRecorder" / "Tests"

    if not tests_dir.exists():
        print_fail("Tests directory not found")
        failed += 1
        return

    print_pass("Tests directory exists")
    passed += 1

    expected_tests = [
        "ConfigTests.swift",
        "MeetingDetectorTests.swift",
        "AudioCaptureTests.swift",
        "IntegrationTests.swift",
    ]

    for filename in expected_tests:
        filepath = tests_dir / filename
        if filepath.exists():
            print_pass(f"Test file exists: {filename}")
            passed += 1
        else:
            print_warn(f"Test file missing: {filename}")
            warnings += 1


def test_audio_settings_documented():
    """Test that audio settings are documented"""
    global passed, failed
    readme_path = MEETING_RECORDER_DIR / "README.md"

    if not readme_path.exists():
        return

    content = readme_path.read_text()

    # Check for audio settings documentation
    settings = ["64", "kbps", "16", "kHz", "Mono", "M4A"]

    found = sum(1 for s in settings if s in content)
    if found >= 4:
        print_pass(f"Audio settings documented ({found}/6 keywords found)")
        passed += 1
    else:
        print_fail(f"Audio settings not well documented ({found}/6 keywords)")
        failed += 1


def test_meeting_apps_documented():
    """Test that supported meeting apps are documented"""
    global passed, failed
    readme_path = MEETING_RECORDER_DIR / "README.md"

    if not readme_path.exists():
        return

    content = readme_path.read_text()

    apps = ["Zoom", "Google Meet", "Microsoft Teams", "Slack", "Discord"]
    found = sum(1 for app in apps if app in content)

    if found >= 4:
        print_pass(f"Meeting apps documented ({found}/5)")
        passed += 1
    else:
        print_fail(f"Meeting apps not well documented ({found}/5)")
        failed += 1


def main():
    global passed, failed, warnings

    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  Meeting Recorder - Validation Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

    print_section("SKILL.md Validation")
    test_skill_md_exists()
    test_skill_md_structure()
    test_skill_md_commands()

    print_section("Documentation Validation")
    test_readme_exists()
    test_readme_content()
    test_audio_settings_documented()
    test_meeting_apps_documented()

    print_section("Setup & Configuration")
    test_setup_script()
    test_config_example()

    print_section("Swift Package Validation")
    test_swift_package()
    test_swift_sources()
    test_swift_tests()

    # Summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  Test Results Summary{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

    total = passed + failed
    print(f"\n  {Colors.GREEN}Passed:   {passed}{Colors.RESET}")
    print(f"  {Colors.RED}Failed:   {failed}{Colors.RESET}")
    print(f"  {Colors.YELLOW}Warnings: {warnings}{Colors.RESET}")
    print(f"  Total:    {total}")

    if failed == 0:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.RESET}")
        return 0
    else:
        print(f"\n  {Colors.RED}{Colors.BOLD}{failed} test(s) failed{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
