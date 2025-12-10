"""
MCP Configuration Manager for Setup & Maintenance Manager.
Handles reading, writing, and updating the Claude Desktop configuration file.
Supports macOS and Windows.
"""
import difflib
import json
import os
import platform
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def get_config_path() -> Path:
    """
    Get the path to the Claude Desktop configuration file based on the OS.
    
    Returns:
        Path to claude_desktop_config.json
    """
    system = platform.system()
    
    if system == "Windows":
        app_data = os.environ.get("APPDATA")
        if not app_data:
            # Fallback if APPDATA is not set (unlikely on Windows)
            app_data = str(Path.home() / "AppData" / "Roaming")
        return Path(app_data) / "Claude" / "claude_desktop_config.json"
        
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        
    else:
        # Linux or other (fallback to XDG or similar if needed, but user asked for Mac/Windows)
        # Assuming standard XDG for Linux for completeness, though not explicitly requested
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            return Path(xdg_config) / "Claude" / "claude_desktop_config.json"
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"

def read_config() -> Dict[str, Any]:
    """
    Read the existing configuration file.
    Returns an empty dict structure if file doesn't exist.
    """
    path = get_config_path()
    if not path.exists():
        return {"mcpServers": {}}
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"mcpServers": {}}
    except Exception:
        return {"mcpServers": {}}

def generate_config_diff(current_config: Dict[str, Any], new_config: Dict[str, Any]) -> str:
    """
    Generate a readable diff between current and new configuration.
    """
    current_str = json.dumps(current_config, indent=2, sort_keys=True)
    new_str = json.dumps(new_config, indent=2, sort_keys=True)
    
    diff = difflib.unified_diff(
        current_str.splitlines(),
        new_str.splitlines(),
        fromfile='Current Config',
        tofile='Proposed Config',
        lineterm=''
    )
    return '\n'.join(diff)

def add_mcp_server(
    name: str, 
    command: str, 
    args: List[str], 
    env: Optional[Dict[str, str]] = None,
    preview_only: bool = True
) -> Tuple[bool, str]:
    """
    Add or update an MCP server in the configuration.
    
    Args:
        name: Server name (key in mcpServers)
        command: Executable command
        args: List of arguments
        env: Environment variables (optional)
        preview_only: If True, only returns the diff without saving.
        
    Returns:
        Tuple (success, message/diff)
    """
    path = get_config_path()
    current_config = read_config()
    
    # Create a deep copy to modify
    new_config = json.loads(json.dumps(current_config))
    
    if "mcpServers" not in new_config:
        new_config["mcpServers"] = {}
        
    server_config = {
        "command": command,
        "args": args
    }
    
    if env:
        server_config["env"] = env
        
    new_config["mcpServers"][name] = server_config
    
    # Generate diff
    diff = generate_config_diff(current_config, new_config)
    
    if preview_only:
        if not diff:
            return True, "No changes detected (configuration is already up to date)."
        
        return True, f"Proposed changes to {path}:\n\n```diff\n{diff}\n```\n\nTo apply these changes, set `confirm` to true."
        
    # Apply changes
    try:
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=2, sort_keys=True)
            
        return True, f"Successfully updated configuration at {path}."
        
    except Exception as e:
        return False, f"Failed to write configuration: {str(e)}"
