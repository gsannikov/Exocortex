"""
Tests for Setup & Maintenance Manager.
"""
import sys
from pathlib import Path

# Add package root to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from setup_manager.discovery import get_skill_details, list_installed_skills
from setup_manager.setup import check_system_requirements


def test_discovery():
    print("Testing Skill Discovery...")
    skills = list_installed_skills()
    print(f"Found {len(skills)} skills.")
    for skill in skills:
        print(f"- {skill['name']} ({skill['id']})")
        
    if skills:
        first_skill = skills[0]['id']
        print(f"\nGetting details for {first_skill}...")
        details = get_skill_details(first_skill)
        if details:
            print("Successfully retrieved details.")
        else:
            print("Failed to retrieve details.")

def test_requirements():
    print("\nTesting System Requirements...")
    reqs = check_system_requirements()
    for tool, installed in reqs.items():
        print(f"{tool}: {'Installed' if installed else 'Missing'}")

if __name__ == "__main__":
    test_discovery()
    test_requirements()
