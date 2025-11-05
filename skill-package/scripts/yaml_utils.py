"""
Utilities for YAML file operations.

Provides safe and consistent YAML reading, writing, and manipulation
with proper error handling and validation.
"""

import yaml
import os
from datetime import datetime
from pathlib import Path


# =============================================================================
# CORE OPERATIONS
# =============================================================================

def read_yaml(filepath):
    """
    Read and parse a YAML file.
    
    Args:
        filepath (str): Path to YAML file
    
    Returns:
        dict: Parsed YAML data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"YAML file not found: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data if data is not None else {}
    
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in {filepath}: {e}")


def write_yaml(data, filepath, **kwargs):
    """
    Write data to a YAML file.
    
    Args:
        data (dict): Data to write
        filepath (str): Path to output file
        **kwargs: Additional arguments for yaml.dump()
            - default_flow_style (bool): Use flow style (default: False)
            - allow_unicode (bool): Allow unicode characters (default: True)
            - sort_keys (bool): Sort dictionary keys (default: False)
            - indent (int): Indentation spaces (default: 2)
    
    Returns:
        bool: True if successful
    """
    # Default YAML formatting options
    options = {
        'default_flow_style': False,
        'allow_unicode': True,
        'sort_keys': False,
        'indent': 2,
        'width': 120,
    }
    options.update(kwargs)

    # Ensure directory exists (only if filepath has a directory component)
    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, **options)
        return True
    
    except Exception as e:
        raise IOError(f"Failed to write YAML to {filepath}: {e}")


def read_yaml_safe(filepath, default=None):
    """
    Read YAML file with fallback to default value on error.
    
    Args:
        filepath (str): Path to YAML file
        default (any): Default value if file doesn't exist or is invalid
    
    Returns:
        dict: Parsed YAML data or default value
    """
    try:
        return read_yaml(filepath)
    except (FileNotFoundError, yaml.YAMLError):
        return default if default is not None else {}


# =============================================================================
# UPDATE OPERATIONS
# =============================================================================

def update_yaml(filepath, updates, create_if_missing=True):
    """
    Update existing YAML file with new values.
    
    Args:
        filepath (str): Path to YAML file
        updates (dict): Dictionary of updates to apply
        create_if_missing (bool): Create file if it doesn't exist
    
    Returns:
        dict: Updated data
    """
    if os.path.exists(filepath):
        data = read_yaml(filepath)
    elif create_if_missing:
        data = {}
    else:
        raise FileNotFoundError(f"YAML file not found: {filepath}")
    
    # Deep update
    data = deep_update(data, updates)
    
    # Write back
    write_yaml(data, filepath)
    
    return data


def deep_update(base_dict, update_dict):
    """
    Recursively update nested dictionaries.
    
    Args:
        base_dict (dict): Base dictionary
        update_dict (dict): Updates to apply
    
    Returns:
        dict: Updated dictionary
    """
    result = base_dict.copy()
    
    for key, value in update_dict.items():
        if (
            key in result and
            isinstance(result[key], dict) and
            isinstance(value, dict)
        ):
            result[key] = deep_update(result[key], value)
        else:
            result[key] = value
    
    return result


def merge_yaml_files(file1, file2, output_file=None):
    """
    Merge two YAML files.
    
    Args:
        file1 (str): Path to first YAML file (base)
        file2 (str): Path to second YAML file (updates)
        output_file (str, optional): Path to output file (defaults to file1)
    
    Returns:
        dict: Merged data
    """
    data1 = read_yaml(file1)
    data2 = read_yaml(file2)
    
    merged = deep_update(data1, data2)
    
    if output_file is None:
        output_file = file1
    
    write_yaml(merged, output_file)
    
    return merged


# =============================================================================
# VALIDATION
# =============================================================================

def validate_yaml(filepath):
    """
    Validate YAML file syntax.
    
    Args:
        filepath (str): Path to YAML file
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        read_yaml(filepath)
        return (True, None)
    except FileNotFoundError as e:
        return (False, f"File not found: {e}")
    except yaml.YAMLError as e:
        return (False, f"Invalid YAML: {e}")


def validate_yaml_schema(data, required_keys):
    """
    Validate that YAML data contains required keys.
    
    Args:
        data (dict): YAML data to validate
        required_keys (list): List of required key paths (e.g., ['key1', 'key2.nested'])
    
    Returns:
        tuple: (is_valid, missing_keys)
    """
    missing = []
    
    for key_path in required_keys:
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                missing.append(key_path)
                break
            current = current[key]
    
    return (len(missing) == 0, missing)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def add_metadata(data, **metadata):
    """
    Add metadata fields to YAML data.
    
    Args:
        data (dict): YAML data
        **metadata: Metadata fields to add
    
    Returns:
        dict: Data with metadata
    """
    if 'metadata' not in data:
        data['metadata'] = {}
    
    # Add timestamp if not provided
    if 'updated_at' not in metadata:
        metadata['updated_at'] = datetime.utcnow().isoformat() + 'Z'
    
    data['metadata'].update(metadata)
    
    return data


def get_nested_value(data, key_path, default=None):
    """
    Get nested value from dictionary using dot notation.
    
    Args:
        data (dict): YAML data
        key_path (str): Path to key (e.g., 'level1.level2.key')
        default (any): Default value if key not found
    
    Returns:
        any: Value at key path or default
    """
    keys = key_path.split('.')
    current = data
    
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    
    return current


def set_nested_value(data, key_path, value):
    """
    Set nested value in dictionary using dot notation.
    
    Args:
        data (dict): YAML data
        key_path (str): Path to key (e.g., 'level1.level2.key')
        value (any): Value to set
    
    Returns:
        dict: Updated data
    """
    keys = key_path.split('.')
    current = data
    
    # Navigate to parent of target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the value
    current[keys[-1]] = value
    
    return data


def list_yaml_files(directory):
    """
    List all YAML files in a directory.
    
    Args:
        directory (str): Directory path
    
    Returns:
        list: List of YAML file paths
    """
    yaml_extensions = ['.yaml', '.yml']
    yaml_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in yaml_extensions):
                yaml_files.append(os.path.join(root, file))
    
    return sorted(yaml_files)


def backup_yaml(filepath):
    """
    Create a backup of a YAML file.
    
    Args:
        filepath (str): Path to YAML file
    
    Returns:
        str: Path to backup file
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Cannot backup non-existent file: {filepath}")
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = f"{filepath}.backup-{timestamp}"
    
    # Copy file
    with open(filepath, 'r') as src:
        with open(backup_path, 'w') as dst:
            dst.write(src.read())
    
    return backup_path


# =============================================================================
# BATCH OPERATIONS
# =============================================================================

def batch_read_yaml(filepaths):
    """
    Read multiple YAML files.
    
    Args:
        filepaths (list): List of file paths
    
    Returns:
        dict: Dictionary mapping filepath to parsed data
    """
    results = {}
    
    for filepath in filepaths:
        try:
            results[filepath] = read_yaml(filepath)
        except Exception as e:
            results[filepath] = {'error': str(e)}
    
    return results


def batch_validate_yaml(directory):
    """
    Validate all YAML files in a directory.
    
    Args:
        directory (str): Directory path
    
    Returns:
        dict: Dictionary mapping filepath to validation result
    """
    yaml_files = list_yaml_files(directory)
    results = {}
    
    for filepath in yaml_files:
        is_valid, error = validate_yaml(filepath)
        results[filepath] = {
            'valid': is_valid,
            'error': error
        }
    
    return results


# =============================================================================
# FORMATTING
# =============================================================================

def format_yaml_file(filepath, **options):
    """
    Reformat a YAML file with consistent style.
    
    Args:
        filepath (str): Path to YAML file
        **options: Formatting options for yaml.dump()
    
    Returns:
        bool: True if successful
    """
    data = read_yaml(filepath)
    write_yaml(data, filepath, **options)
    return True


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    # Test basic operations
    test_data = {
        'version': '1.0',
        'settings': {
            'enabled': True,
            'options': {
                'option1': 'value1',
                'option2': 42
            }
        }
    }
    
    print("Testing YAML utilities...")
    
    # Test write
    test_file = '/tmp/test.yaml'
    write_yaml(test_data, test_file)
    print(f"✅ Write test passed")
    
    # Test read
    read_data = read_yaml(test_file)
    assert read_data == test_data
    print(f"✅ Read test passed")
    
    # Test nested value access
    value = get_nested_value(test_data, 'settings.options.option1')
    assert value == 'value1'
    print(f"✅ Nested access test passed")
    
    # Test validation
    is_valid, error = validate_yaml(test_file)
    assert is_valid
    print(f"✅ Validation test passed")
    
    # Cleanup
    os.remove(test_file)
    print("\n✅ All tests passed!")
