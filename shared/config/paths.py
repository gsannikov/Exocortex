"""
Centralized Path Configuration for Claude Skills

This is the SINGLE SOURCE OF TRUTH for user data paths.
All skills and scripts should import from this module.

To change the user data location, update USER_DATA_BASE below.
"""

import os
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# USER CONFIGURATION - CHANGE THIS TO SET YOUR USER DATA LOCATION
# ═══════════════════════════════════════════════════════════════════════════════

# Set this to your user data directory path
# Examples:
#   "/Users/username/Documents/claude-skills-data"
#   "/Users/username/MyDrive/claude-skills-data"
#   "~/Documents/claude-skills-data"  # Will be expanded to full path
USER_DATA_BASE: Optional[str] = None

# If None, will try to auto-detect from common locations
# Set to None to enable auto-detection
# USER_DATA_BASE = None

# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-DETECTION (if USER_DATA_BASE is None)
# ═══════════════════════════════════════════════════════════════════════════════

def _auto_detect_user_data_base() -> Path:
    """
    Auto-detect user data directory from common locations.
    Checks in order:
    1. ~/Documents/claude-skills-data
    2. ~/MyDrive/claude-skills-data
    3. ~/claude-skills-data
    """
    home = Path.home()
    candidates = [
        home / "exocortex-data",
        home / "Documents" / "exocortex-data",
        home / "Documents" / "claude-skills-data",
        home / "MyDrive" / "claude-skills-data",
        home / "claude-skills-data",
    ]
    
    # Return first existing directory, or first candidate if none exist
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]  # Default to Documents if none exist

# ═══════════════════════════════════════════════════════════════════════════════
# PATH RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_user_data_base() -> Path:
    """
    Get the base directory for user data.
    
    Returns:
        Path object to the user data base directory
    """
    if USER_DATA_BASE is None:
        return _auto_detect_user_data_base()
    
    # Expand user home directory if path starts with ~
    path_str = USER_DATA_BASE
    if path_str.startswith("~"):
        path_str = os.path.expanduser(path_str)
    
    return Path(path_str).expanduser().resolve()


def get_skill_data_dir(skill_name: str) -> Path:
    """
    Get the data directory for a specific skill.
    
    Args:
        skill_name: Name of the skill (e.g., "career-consultant")
    
    Returns:
        Path object to the skill's data directory
    """
    return get_user_data_base() / skill_name


def get_project_root() -> Path:
    """
    Get the project root directory (where this repo is located).
    This is auto-detected from the location of this file.
    
    Returns:
        Path object to the project root
    """
    # This file is at: shared/config/paths.py
    # So project root is: shared/config/paths.py -> shared/config -> shared -> root
    return Path(__file__).parent.parent.parent


# ═══════════════════════════════════════════════════════════════════════════════
# LEGACY SUPPORT - For backward compatibility
# ═══════════════════════════════════════════════════════════════════════════════

# Export as string for legacy code that expects strings
def get_user_data_base_str() -> str:
    """Get user data base as string (for legacy code)."""
    return str(get_user_data_base())


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_paths() -> bool:
    """
    Validate that the user data directory exists or can be created.
    
    Returns:
        True if valid, raises exception if not
    """
    base = get_user_data_base()
    if not base.exists():
        # Try to create it
        try:
            base.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise FileNotFoundError(
                f"User data directory does not exist and cannot be created: {base}\n"
                f"Error: {e}\n"
                f"Please update USER_DATA_BASE in {__file__} or create the directory manually."
            )
    return True


if __name__ == "__main__":
    """Test the path configuration."""
    print("Claude Skills - Path Configuration")
    print("=" * 50)
    print(f"User Data Base: {get_user_data_base()}")
    print(f"Project Root: {get_project_root()}")
    print()
    print("Skill Data Directories:")
    for skill in ["career-consultant", "reading-list", "ideas-capture", 
                  "voice-memos", "local-rag", "social-media-post"]:
        print(f"  {skill}: {get_skill_data_dir(skill)}")
    print()
    try:
        validate_paths()
        print("✅ Path configuration is valid")
    except Exception as e:
        print(f"❌ Path validation failed: {e}")

