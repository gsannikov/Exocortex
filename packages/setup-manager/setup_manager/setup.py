"""
Setup logic for Setup & Maintenance Manager.
"""
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple


def check_system_requirements() -> Dict[str, bool]:
    """
    Check if required system tools are installed.
    
    Returns:
        Dictionary mapping tool names to their installation status (True/False).
    """
    requirements = ["python3", "uv", "npm", "git"]
    status = {}
    
    for tool in requirements:
        status[tool] = shutil.which(tool) is not None
        
    return status

def install_package_dependencies(package_path: Path) -> Tuple[bool, str]:
    """
    Install dependencies for a specific package using uv or pip.
    
    Args:
        package_path: Path to the package directory.
        
    Returns:
        Tuple (success, message).
    """
    if not package_path.exists():
        return False, f"Package path does not exist: {package_path}"
        
    # Check for pyproject.toml
    if (package_path / "pyproject.toml").exists():
        # Prefer uv if available
        if shutil.which("uv"):
            cmd = ["uv", "sync"]
            tool_name = "uv"
        else:
            cmd = [sys.executable, "-m", "pip", "install", "-e", "."]
            tool_name = "pip"
            
        try:
            subprocess.run(cmd, cwd=package_path, check=True, capture_output=True, text=True)
            return True, f"Dependencies installed successfully using {tool_name}."
        except subprocess.CalledProcessError as e:
            return False, f"Failed to install dependencies: {e.stderr}"
            
    # Check for requirements.txt
    elif (package_path / "requirements.txt").exists():
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        try:
            subprocess.run(cmd, cwd=package_path, check=True, capture_output=True, text=True)
            return True, "Dependencies installed successfully using pip."
        except subprocess.CalledProcessError as e:
            return False, f"Failed to install dependencies: {e.stderr}"
            
    return False, "No dependency file (pyproject.toml or requirements.txt) found."
