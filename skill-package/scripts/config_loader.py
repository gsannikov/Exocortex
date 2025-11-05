"""Configuration Loader for Claude Skills"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import paths
from scripts import yaml_utils

def load_user_config():
    """Load user configuration from YAML file."""
    try:
        # Validate user data base path
        paths.get_user_data_base()
        # Load user config from standard location
        user_config_path = paths.get_config_path('user-config.yaml')
        config = yaml_utils.read_yaml(user_config_path)
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def get_config_value(key, default=None):
    """Get specific config value with default."""
    config = load_user_config()
    return config.get(key, default) if config else default
