"""
Verification script for Data Management features.
Tests backup and reset functionality.
"""
import shutil
import sys
from pathlib import Path

# Add package root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from setup_manager.maintenance import backup_skill_data, reset_skill_data


def test_data_management():
    print("\nTesting Data Management...")
    
    # Setup test data
    test_dir = Path("/tmp/claude-skills-test-data")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    skill_id = "test-skill"
    skill_dir = test_dir / skill_id
    skill_dir.mkdir()
    
    # Create some dummy files
    (skill_dir / "data.txt").write_text("Important Data")
    (skill_dir / "config.json").write_text("{}")
    
    print(f"Created test data at {skill_dir}")
    
    # 1. Test Backup
    print("\n1. Testing Backup...")
    success, msg = backup_skill_data(skill_id, test_dir)
    print(f"Backup Result: {msg}")
    
    if success:
        print("✅ Backup successful")
        # Verify zip exists
        backups_dir = test_dir / "backups"
        zips = list(backups_dir.glob("*.zip"))
        if zips:
            print(f"   Found backup: {zips[0]}")
        else:
            print("❌ No zip file found!")
    else:
        print("❌ Backup failed")
        
    # 2. Test Reset (with backup)
    print("\n2. Testing Reset...")
    # Add a new file to verify it gets deleted
    (skill_dir / "new_data.txt").write_text("New Data")
    
    success, msg = reset_skill_data(skill_id, test_dir, backup=True)
    print(f"Reset Result: {msg}")
    
    if success:
        print("✅ Reset successful")
        # Verify directory is empty but exists
        if skill_dir.exists():
            files = list(skill_dir.iterdir())
            if not files:
                print("   Directory is empty (correct)")
            else:
                print(f"❌ Directory not empty: {files}")
        else:
            print("❌ Directory was deleted completely (should exist but be empty)")
            
        # Verify second backup was created
        zips = list(backups_dir.glob("*.zip"))
        if len(zips) >= 2:
            print(f"   Found {len(zips)} backups (correct)")
        else:
            print(f"❌ Expected 2 backups, found {len(zips)}")
    else:
        print("❌ Reset failed")

if __name__ == "__main__":
    test_data_management()
