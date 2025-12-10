"""
Maintenance logic for Setup & Maintenance Manager.
"""
import shutil
from pathlib import Path
from typing import List, Tuple


def clean_logs(log_dir: Path, max_age_days: int = 7) -> Tuple[int, int]:
    """
    Clean up old log files.
    
    Args:
        log_dir: Directory containing logs.
        max_age_days: Maximum age of logs in days (not implemented yet, just clearing for now).
        
    Returns:
        Tuple (files_removed, bytes_freed).
    """
    if not log_dir.exists():
        return 0, 0
        
    files_removed = 0
    bytes_freed = 0
    
    # Simple implementation: remove rotated logs (*.1, *.2, etc)
    # or just report for now to be safe
    
    # For this iteration, let's just look for standard log rotation patterns
    for item in log_dir.glob("**/*.log.*"):
        if item.is_file():
            try:
                size = item.stat().st_size
                item.unlink()
                files_removed += 1
                bytes_freed += size
            except OSError:
                pass
                
    return files_removed, bytes_freed

def update_all_dependencies(packages_dir: Path) -> List[str]:
    """
    Attempt to update dependencies for all packages.
    
    Args:
        packages_dir: Root packages directory.
        
    Returns:
        List of messages describing the outcome for each package.
    """
    from .setup import install_package_dependencies
    
    results = []
    if not packages_dir.exists():
        return ["Packages directory not found."]
        
    for item in packages_dir.iterdir():
        if item.is_dir() and ((item / "pyproject.toml").exists() or (item / "requirements.txt").exists()):
            success, msg = install_package_dependencies(item)
            status = "Success" if success else "Failed"
            results.append(f"[{status}] {item.name}: {msg}")
            
    return results

def backup_skill_data(skill_id: str, data_dir: Path) -> Tuple[bool, str]:
    """
    Create a zip backup of the skill's data directory.
    
    Args:
        skill_id: The ID of the skill (e.g., 'local-rag').
        data_dir: The root data directory (e.g., ~/MyDrive/claude-skills-data).
        
    Returns:
        Tuple (success, message).
    """
    import datetime
    import shutil
    
    skill_data_path = data_dir / skill_id
    if not skill_data_path.exists():
        return False, f"No data found for {skill_id} at {skill_data_path}"
        
    backups_dir = data_dir / "backups"
    backups_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_filename = f"{skill_id}_{timestamp}"
    backup_path = backups_dir / backup_filename
    
    try:
        # shutil.make_archive expects base_name (without extension) and root_dir
        archive_path = shutil.make_archive(str(backup_path), 'zip', str(skill_data_path))
        return True, f"Backup created at {archive_path}"
    except Exception as e:
        return False, f"Backup failed: {e}"

def reset_skill_data(skill_id: str, data_dir: Path, backup: bool = True) -> Tuple[bool, str]:
    """
    Reset (delete and recreate) the skill's data directory.
    
    Args:
        skill_id: The ID of the skill.
        data_dir: The root data directory.
        backup: Whether to create a backup before resetting.
        
    Returns:
        Tuple (success, message).
    """
    skill_data_path = data_dir / skill_id
    if not skill_data_path.exists():
        return False, f"No data found for {skill_id} at {skill_data_path}"
        
    if backup:
        success, msg = backup_skill_data(skill_id, data_dir)
        if not success:
            return False, f"Reset aborted. Backup failed: {msg}"
            
    try:
        # Remove the directory
        shutil.rmtree(skill_data_path)
        # Recreate it empty
        skill_data_path.mkdir(parents=True, exist_ok=True)
        return True, f"Data for {skill_id} has been reset."
    except Exception as e:
        return False, f"Reset failed: {e}"
