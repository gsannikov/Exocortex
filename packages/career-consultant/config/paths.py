"""
Path Configuration for Career Consultant Skill

This file contains path configurations for the skill package.
Users should update USER_DATA_BASE to point to their user-data folder.
"""

# ============================================
# User Configuration
# ============================================
# CONFIGURE THIS: Set your user-data directory path
# Example: "/Users/<username>/Documents/career-consultant/user-data"
# Example: "/Users/<username>/MyDrive/career-consultant/user-data"
USER_DATA_BASE = "/Users/gursannikov/MyDrive/claude-skills-data/career-consultant"

# Example paths:
# macOS: "/Users/username/Documents/career-consultant/user-data"
# Windows: "C:/Users/username/Documents/career-consultant/user-data"
# Linux: "/home/username/career-consultant/user-data"

# ============================================
# Derived Paths (Auto-configured)
# ============================================
# These paths are automatically derived from USER_DATA_BASE
# You typically don't need to modify these

# Main directories
# Main directories
PROFILE_BASE = f"{USER_DATA_BASE}/profile"
COMPANIES_DIR = f"{USER_DATA_BASE}/companies"
JOBS_BASE = f"{USER_DATA_BASE}/jobs"
INTERVIEWS_BASE = f"{USER_DATA_BASE}/interviews"
REPORTS_BASE = f"{USER_DATA_BASE}/reports"
SCRIPTS_BASE = f"{USER_DATA_BASE}/scripts"

# Legacy paths (deprecated)
DB_BASE = f"{USER_DATA_BASE}/db"  # Deprecated - use COMPANIES_DIR
ROLES_DIR = f"{DB_BASE}/roles"  # Deprecated
EXCEL_PATH = f"{DB_BASE}/db.xlsx" # Kept for now, but relies on deprecated DB_BASE

# Profile/configuration file paths
USER_CONFIG_PATH = f"{PROFILE_BASE}/settings.yaml"  # Renamed from user-config.yaml
CV_BASE = f"{PROFILE_BASE}/cvs"  # Renamed from cv-variants
CANDIDATE_PROFILE_PATH = f"{PROFILE_BASE}/candidate.md"  # Renamed from candidate-profile.md
SALARY_DATA_PATH = f"{PROFILE_BASE}/salary-requirements.md"  # Renamed from salary-data.md

# Jobs paths
BACKLOG_PATH = f"{JOBS_BASE}/BACKLOG.md"  # Renamed from MASTER-BACKLOG.md
NEW_URLS_PATH = f"{JOBS_BASE}/new-urls.txt"

# Reports paths
COMPANIES_DB_HTML = f"{REPORTS_BASE}/companies-db.html"
COMPANIES_DB_XLSX = f"{REPORTS_BASE}/companies-db.xlsx"

# Skill package paths (relative to skill location)
SKILL_BASE = "."  # Current skill directory (auto-detected by Claude)
MODULES_BASE = f"{SKILL_BASE}/modules"
SKILL_SCRIPTS_BASE = f"{SKILL_BASE}/scripts"
SKILL_TEMPLATES_BASE = f"{SKILL_BASE}/templates"

# Scoring system (part of skill package)
SCORING_SYSTEM_PATH = f"{SKILL_BASE}/config/scoring-system.md"

# ============================================
# Path Validation
# ============================================

def validate_paths():
    """
    Validate that required directories exist.
    Call this at skill initialization.
    """
    import os
    
    required_paths = [
        USER_DATA_BASE,
        PROFILE_BASE,
        COMPANIES_DIR,
        JOBS_BASE,
        USER_CONFIG_PATH
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        error_msg = "Missing required paths:\n"
        for path in missing_paths:
            error_msg += f"  - {path}\n"
        error_msg += "\nPlease set up your user-data directory structure."
        raise FileNotFoundError(error_msg)
    
    return True


def get_all_paths():
    """
    Get dictionary of all configured paths.
    Useful for debugging.
    """
    return {
        'user_data_base': USER_DATA_BASE,
        'profile_base': PROFILE_BASE,
        'companies_dir': COMPANIES_DIR,
        'jobs_base': JOBS_BASE,
        'interviews_base': INTERVIEWS_BASE,
        'reports_base': REPORTS_BASE,
        'scripts_base': SCRIPTS_BASE,
        'user_config_path': USER_CONFIG_PATH,
        'cv_base': CV_BASE,
        'candidate_profile_path': CANDIDATE_PROFILE_PATH,
        'salary_data_path': SALARY_DATA_PATH,
        'backlog_path': BACKLOG_PATH,
        'new_urls_path': NEW_URLS_PATH,
        'companies_db_html': COMPANIES_DB_HTML,
        'companies_db_xlsx': COMPANIES_DB_XLSX,
        'skill_base': SKILL_BASE,
        'modules_base': MODULES_BASE,
        'scoring_system_path': SCORING_SYSTEM_PATH
    }


# Example usage
if __name__ == "__main__":
    print("Career Consultant - Path Configuration\n")
    print("="*50)
    
    try:
        validate_paths()
        print("✅ All required paths exist\n")
    except FileNotFoundError as e:
        print(f"❌ Path validation failed:\n{e}\n")
    
    print("Configured Paths:")
    print("="*50)
    all_paths = get_all_paths()
    for name, path in all_paths.items():
        print(f"{name:.<30} {path}")
