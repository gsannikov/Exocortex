"""
Storage Path Resolution Utilities for Career Consultant

Handles both Google Drive and local filesystem storage with automatic detection.

Usage:
    from storage_utils import resolve_storage_paths, verify_storage, init_storage
    
    # Resolve paths based on user config
    paths = resolve_storage_paths(user_config)
    
    # Verify storage is accessible
    is_valid, message = verify_storage(user_config)
    
    # Initialize storage on first run
    init_storage(user_config)

Author: Gur Sannikov
Version: 9.2
"""

import os
from pathlib import Path
from typing import Dict, Tuple, Optional
import yaml


def detect_storage_type() -> str:
    """
    Auto-detect storage type based on current environment
    
    Returns:
        'google_drive' or 'local'
    """
    # Check for common Google Drive mount points
    common_drive_paths = [
        Path.home() / "MyDrive",
        Path.home() / "Google Drive",
        Path.home() / "GoogleDrive"
    ]
    
    for drive_path in common_drive_paths:
        if drive_path.exists():
            print(f"✅ Detected Google Drive at: {drive_path}")
            return "google_drive"
    
    print("ℹ️  Google Drive not detected, using local filesystem")
    return "local"


def resolve_base_path(user_config: Dict) -> Path:
    """
    Resolve the base storage path from user configuration
    
    Args:
        user_config: Loaded user-config.yaml
    
    Returns:
        Path object to base directory
    """
    storage_config = user_config.get('storage', {})
    storage_type = storage_config.get('type', 'google_drive')
    base_path_config = storage_config.get('base_path', 'auto')
    
    # If explicitly set, use that
    if base_path_config != 'auto':
        base_path = Path(base_path_config).expanduser()
        print(f"📍 Using configured base path: {base_path}")
        return base_path
    
    # Auto-detect based on storage type
    if storage_type == 'google_drive':
        # Get Google Drive mount point
        mount_point = storage_config.get('google_drive', {}).get('mount_point', '~/MyDrive')
        mount_path = Path(mount_point).expanduser()
        
        # Career consultant directory
        base_path = mount_path / 'career-consultant.skill'
        print(f"📍 Auto-detected Google Drive path: {base_path}")
        
    else:  # local
        # Get local base directory
        base_dir = storage_config.get('local', {}).get('base_dir', '~/Documents/career-consultant')
        base_path = Path(base_dir).expanduser()
        print(f"📍 Auto-detected local path: {base_path}")
    
    return base_path


def resolve_storage_paths(user_config: Dict) -> Dict[str, str]:
    """
    Resolve all storage paths from user configuration
    
    Args:
        user_config: Loaded user-config.yaml
    
    Returns:
        Dictionary with all resolved paths
    """
    # Get base path
    base_path = resolve_base_path(user_config)
    user_data_base = base_path / 'user-data'
    
    # Get relative paths from config
    paths_config = user_config.get('paths', {})
    
    # Resolve all paths
    resolved_paths = {
        'BASE_PATH': str(base_path),
        'USER_DATA_BASE': str(user_data_base),
        'CV_BASE': str(user_data_base / paths_config.get('cv_base', 'profile/cvs')),
        'PROFILE': str(user_data_base / paths_config.get('profile', 'profile/candidate.md')),
        'SALARY_DATA': str(user_data_base / paths_config.get('salary_data', 'profile/salary-requirements.md')),
        'COMPANIES_DIR': str(user_data_base / paths_config.get('companies_db', 'companies')),
        'REPORTS_DIR': str(user_data_base / 'reports'),
        'EXCEL_PATH': str(user_data_base / paths_config.get('excel_db', 'reports/companies-db.xlsx')),
        'HTML_PATH': str(user_data_base / paths_config.get('html_db', 'reports/companies-db.html')),
        'CONFIG_DIR': str(user_data_base / 'profile'),
        'LOGS_DIR': str(user_data_base / 'logs'),
        'SKILL_PACKAGE': str(base_path / 'skill-package'),
        'TEMPLATES_DIR': str(base_path / 'skill-package/templates')
    }
    
    return resolved_paths


def verify_storage(user_config: Dict) -> Tuple[bool, str]:
    """
    Verify that storage is accessible and properly configured
    
    Args:
        user_config: Loaded user-config.yaml
    
    Returns:
        (is_valid, message)
    """
    storage_config = user_config.get('storage', {})
    storage_type = storage_config.get('type', 'google_drive')
    
    # Resolve base path
    try:
        base_path = resolve_base_path(user_config)
    except Exception as e:
        return False, f"Failed to resolve base path: {e}"
    
    # Check if base path exists
    if not base_path.exists():
        return False, f"Base path does not exist: {base_path}"
    
    # Google Drive specific checks
    if storage_type == 'google_drive':
        verify_mounted = storage_config.get('google_drive', {}).get('verify_mounted', True)
        
        if verify_mounted:
            mount_point = storage_config.get('google_drive', {}).get('mount_point', '~/MyDrive')
            mount_path = Path(mount_point).expanduser()
            
            if not mount_path.exists():
                return False, f"Google Drive not mounted at: {mount_path}. Please start Google Drive for Desktop."
            
            # Check if it's actually a Drive directory (has .tmp.drivedownload or similar)
            # This is a heuristic - Drive folders often have these temp files
            if not any(mount_path.rglob('.tmp.drivedownload*')):
                # Not definitive, but warn
                print(f"⚠️  Warning: {mount_path} exists but may not be a mounted Google Drive")
    
    # Check critical directories
    user_data_base = base_path / 'user-data'
    if not user_data_base.exists():
        return False, f"User data directory not found: {user_data_base}"
    
    # Check for config
    config_path = user_data_base / 'profile' / 'settings.yaml'
    if not config_path.exists():
        return False, f"Configuration file not found: {config_path}"
    
    # Check for database directories
    companies_dir = user_data_base / 'companies'

    if not companies_dir.exists():
        return False, f"Companies directory not found: {companies_dir}"

    return True, f"✅ Storage verified: {storage_type} at {base_path}"


def verify_google_drive_mounted() -> Tuple[bool, Optional[Path]]:
    """
    Check if Google Drive is mounted
    
    Returns:
        (is_mounted, mount_path)
    """
    common_mount_points = [
        Path.home() / "MyDrive",
        Path.home() / "Google Drive",
        Path.home() / "GoogleDrive"
    ]
    
    for mount_point in common_mount_points:
        if mount_point.exists():
            return True, mount_point
    
    return False, None


def init_storage(user_config: Dict, create_structure: bool = False) -> Tuple[bool, str]:
    """
    Initialize storage on first run
    
    Args:
        user_config: Loaded user-config.yaml
        create_structure: If True, create directory structure
    
    Returns:
        (success, message)
    """
    storage_config = user_config.get('storage', {})
    storage_type = storage_config.get('type', 'google_drive')
    
    # Resolve base path
    base_path = resolve_base_path(user_config)
    
    print(f"\n🚀 Initializing storage: {storage_type}")
    print(f"📍 Base path: {base_path}")
    
    # Google Drive specific initialization
    if storage_type == 'google_drive':
        is_mounted, mount_path = verify_google_drive_mounted()
        
        if not is_mounted:
            return False, "❌ Google Drive is not mounted. Please install and start Google Drive for Desktop."
        
        print(f"✅ Google Drive mounted at: {mount_path}")
        
        if not base_path.exists():
            return False, f"❌ Project directory not found: {base_path}\nPlease ensure the career-consultant.skill folder exists in Google Drive."
    
    # Local filesystem initialization
    elif storage_type == 'local':
        auto_create = storage_config.get('local', {}).get('auto_create_dirs', True)
        
        if not base_path.exists():
            if auto_create and create_structure:
                print(f"📁 Creating directory structure at: {base_path}")
                base_path.mkdir(parents=True, exist_ok=True)
            else:
                return False, f"❌ Project directory not found: {base_path}"
    
    # Verify storage is accessible
    is_valid, message = verify_storage(user_config)
    
    if not is_valid:
        return False, f"❌ Storage verification failed: {message}"
    
    print(message)
    return True, "✅ Storage initialized successfully"


def get_storage_info(user_config: Dict) -> Dict:
    """
    Get comprehensive storage information
    
    Args:
        user_config: Loaded user-config.yaml
    
    Returns:
        Dictionary with storage information
    """
    storage_config = user_config.get('storage', {})
    storage_type = storage_config.get('type', 'google_drive')
    base_path = resolve_base_path(user_config)
    
    info = {
        'type': storage_type,
        'base_path': str(base_path),
        'exists': base_path.exists(),
        'is_google_drive': storage_type == 'google_drive',
        'is_local': storage_type == 'local'
    }
    
    if storage_type == 'google_drive':
        is_mounted, mount_path = verify_google_drive_mounted()
        info['drive_mounted'] = is_mounted
        info['drive_mount_point'] = str(mount_path) if mount_path else None
    
    # Get storage size if available
    if base_path.exists():
        try:
            # Calculate total size
            total_size = sum(f.stat().st_size for f in base_path.rglob('*') if f.is_file())
            info['total_size_bytes'] = total_size
            info['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        except (OSError, PermissionError):
            info['total_size_bytes'] = None
            info['total_size_mb'] = None
    
    return info


def load_config_with_storage(config_path: Optional[Path] = None) -> Tuple[Dict, Dict]:
    """
    Load user config and resolve storage paths
    
    Args:
        config_path: Optional path to config file. If None, auto-detect.
    
    Returns:
        (user_config, storage_paths)
    """
    # Auto-detect config if not provided
    if config_path is None:
        # Try to find config in common locations
        possible_configs = [
            Path.cwd() / 'user-data/profile/settings.yaml',
            Path.home() / 'MyDrive/career-consultant.skill/user-data/profile/settings.yaml',
            Path.home() / 'Documents/career-consultant/user-data/profile/settings.yaml'
        ]
        
        for possible_config in possible_configs:
            if possible_config.exists():
                config_path = possible_config
                break
        
        if config_path is None:
            raise FileNotFoundError("Could not find settings.yaml")
    
    # Load config
    with open(config_path, 'r') as f:
        user_config = yaml.safe_load(f)
    
    # Resolve storage paths
    storage_paths = resolve_storage_paths(user_config)
    
    return user_config, storage_paths


# Example usage
if __name__ == "__main__":
    print("🔍 Storage Detection Utility\n")
    
    # Detect storage type
    storage_type = detect_storage_type()
    print(f"Storage Type: {storage_type}\n")
    
    # Check Google Drive status
    is_mounted, mount_path = verify_google_drive_mounted()
    if is_mounted:
        print(f"✅ Google Drive mounted at: {mount_path}\n")
    else:
        print("❌ Google Drive not mounted\n")
    
    # Try to load config and resolve paths
    try:
        user_config, storage_paths = load_config_with_storage()
        print("✅ Configuration loaded successfully\n")
        print("Resolved Paths:")
        for key, value in storage_paths.items():
            print(f"  {key}: {value}")
        
        # Verify storage
        is_valid, message = verify_storage(user_config)
        print(f"\n{message}")
        
        # Get storage info
        info = get_storage_info(user_config)
        print(f"\nStorage Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
