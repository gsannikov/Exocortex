"""
Path Configuration for Recipe Manager Skill

This file contains path configurations for the skill package.
Users should update USER_DATA_BASE to point to their user-data folder.
"""

# ============================================
# User Configuration
# ============================================
# CONFIGURE THIS: Set your user-data directory path
USER_DATA_BASE = "/Users/gursannikov/MyDrive/claude-skills-data/recipe-manager"

# ============================================
# Derived Paths (Auto-configured)
# ============================================

# Main directories
CONFIG_DIR = f"{USER_DATA_BASE}/config"
RECIPES_DIR = f"{USER_DATA_BASE}/recipes"
EXPORTS_DIR = f"{USER_DATA_BASE}/exports"

# Recipe status directories
RECIPES_TO_TRY = f"{RECIPES_DIR}/to-try"
RECIPES_TRIED = f"{RECIPES_DIR}/tried"
RECIPES_PERFECTED = f"{RECIPES_DIR}/perfected"

# Configuration files
SETTINGS_PATH = f"{CONFIG_DIR}/settings.yaml"

# Export files
EXPORT_EXCEL = f"{EXPORTS_DIR}/recipes.xlsx"
EXPORT_HTML = f"{EXPORTS_DIR}/recipes.html"

# Skill package paths (relative to skill location)
SKILL_BASE = "."
MODULES_BASE = f"{SKILL_BASE}/modules"
TEMPLATES_BASE = f"{SKILL_BASE}/templates"
SCRIPTS_BASE = f"{SKILL_BASE}/scripts"

# ============================================
# Notion Integration
# ============================================
NOTION_DATABASE_ID = "2461eaaa56f680c4a8d7f1df05616964"
NOTION_DATA_SOURCE_ID = "2461eaaa-56f6-81cd-8003-000bfe08e51f"

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
        CONFIG_DIR,
        RECIPES_DIR,
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
        'config_dir': CONFIG_DIR,
        'recipes_dir': RECIPES_DIR,
        'exports_dir': EXPORTS_DIR,
        'recipes_to_try': RECIPES_TO_TRY,
        'recipes_tried': RECIPES_TRIED,
        'recipes_perfected': RECIPES_PERFECTED,
        'settings_path': SETTINGS_PATH,
        'notion_database_id': NOTION_DATABASE_ID,
        'notion_data_source_id': NOTION_DATA_SOURCE_ID,
    }


if __name__ == "__main__":
    print("Recipe Manager - Path Configuration\n")
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
