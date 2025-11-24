"""
Configuration Loader for Career Consultant Skill
Loads and validates user configuration from user-config.yaml

This script runs in Claude's container and accesses user data via MCP Filesystem.
"""

import yaml
from typing import Dict, Any, List


def load_user_config(user_data_base: str) -> Dict[str, Any]:
    """
    Load user configuration from YAML file.
    
    Args:
        user_data_base: Path to user-data directory
        
    Returns:
        Dictionary containing user configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If required fields are missing
    """
    config_path = f"{user_data_base}/profile/settings.yaml"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"User config not found: {config_path}\n"
            f"Please create settings.yaml from template"
        )
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {e}")
    
    # Validate required fields
    required_fields = ['cv_variants', 'scoring', 'preferences', 'paths']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")
    
    return config


def get_cv_variants(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract CV variants from configuration.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        List of CV variant configurations
    """
    if not config.get('cv_variants', {}).get('enabled', False):
        raise ValueError("CV variants not enabled in configuration")
    
    variants = config['cv_variants'].get('variants', [])
    if not variants:
        raise ValueError("No CV variants defined in configuration")
    
    return variants


def get_scoring_weights(config: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract scoring weights from configuration.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        Dictionary of scoring weights
    """
    weights = config['scoring'].get('weights', {})
    
    # Validate weights sum to 100
    total = sum(weights.values())
    if total != 100:
        print(f"Warning: Scoring weights sum to {total}, expected 100")
    
    return weights


def get_scoring_thresholds(config: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract scoring thresholds from configuration.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        Dictionary of scoring thresholds
    """
    return config['scoring'].get('thresholds', {})


def get_scoring_bonuses(config: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract scoring bonuses from configuration.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        Dictionary of scoring bonuses
    """
    return config['scoring'].get('bonuses', {})


def get_preferences(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract user preferences from configuration.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        Dictionary of user preferences
    """
    return config.get('preferences', {})


def get_paths(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract path configurations.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        Dictionary of paths (relative to user-data/)
    """
    return config.get('paths', {})


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure and values.
    
    Args:
        config: User configuration dictionary
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    # Check CV variants
    cv_variants = get_cv_variants(config)
    if not cv_variants:
        raise ValueError("No CV variants configured")
    
    # Check each variant has required fields
    for variant in cv_variants:
        required = ['id', 'filename', 'focus']
        for field in required:
            if field not in variant:
                raise ValueError(f"CV variant missing field: {field}")
    
    # Check scoring weights
    weights = get_scoring_weights(config)
    required_weights = ['match', 'income', 'growth', 'lowprep', 'stress', 'location']
    for weight in required_weights:
        if weight not in weights:
            raise ValueError(f"Missing scoring weight: {weight}")
    
    # Check thresholds
    thresholds = get_scoring_thresholds(config)
    if 'first_priority' not in thresholds:
        raise ValueError("Missing threshold: first_priority")
    
    return True


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python config_loader.py <user_data_base>")
        sys.exit(1)
    
    user_data_base = sys.argv[1]
    
    try:
        config = load_user_config(user_data_base)
        validate_config(config)
        
        print("✅ Configuration valid")
        print(f"CV Variants: {len(get_cv_variants(config))}")
        print(f"Scoring Weights: {get_scoring_weights(config)}")
        print(f"Thresholds: {get_scoring_thresholds(config)}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)


def update_scraping_preference(user_data_base: str, use_case: str, successful_tool: str) -> bool:
    """
    Update user-config.yaml to prioritize the successful tool.
    
    Args:
        user_data_base: Path to user-data directory
        use_case: 'company_research', 'linkedin', or 'job_scraping'
        successful_tool: The tool that succeeded (e.g., 'bright_data')
        
    Returns:
        True if updated, False otherwise
    """
    config_path = f"{user_data_base}/profile/settings.yaml"
    
    try:
        # 1. Load current config
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
            
        # 2. Get current preferences
        scraping_tools = config.get('scraping_tools', {})
        current_order = scraping_tools.get(use_case, [])
        
        # 3. Check if update needed
        if not current_order:
            # No preference set, maybe don't create one automatically to avoid overriding defaults unexpectedly?
            # Or create it with successful tool first.
            new_order = [successful_tool]
        elif current_order[0] == successful_tool:
            # Already top preference
            return False
        else:
            # Reorder: successful tool first, keep others unique
            new_order = [successful_tool] + [t for t in current_order if t != successful_tool]
            
        # 4. Update config object
        if 'scraping_tools' not in config:
            config['scraping_tools'] = {}
        config['scraping_tools'][use_case] = new_order
        
        # 5. Save back (Note: This uses PyYAML so comments might be lost. 
        # We prioritize functionality as requested.)
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
        print(f"⚙️  Auto-updated config: Set '{successful_tool}' as top preference for '{use_case}'")
        return True
        
    except Exception as e:
        print(f"⚠️ Failed to update config preference: {e}")
        return False
