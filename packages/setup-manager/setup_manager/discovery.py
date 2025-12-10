import json
from pathlib import Path
from typing import Dict, List, Optional

PACKAGE_ROOT = Path(__file__).parent.parent
MARKETPLACE_FILE = PACKAGE_ROOT / "data" / "marketplace.json"
PACKAGES_DIR = PACKAGE_ROOT.parent

def list_installed_skills() -> List[Dict[str, str]]:
    """
    List skills defined in marketplace.json that are present in the packages directory.
    
    Returns:
        List of dictionaries containing skill details.
    """
    skills = []
    
    if not MARKETPLACE_FILE.exists():
        return []

    try:
        with open(MARKETPLACE_FILE, "r") as f:
            data = json.load(f)
            plugins = data.get("plugins", [])
            
        for plugin in plugins:
            # Verify the package actually exists
            source_path = plugin.get("source", "").lstrip("./")
            full_path = PACKAGES_DIR.parent / source_path
            
            if full_path.exists():
                skills.append({
                    "id": plugin.get("name"),
                    "name": plugin.get("name"), # Marketplace uses name as ID often
                    "description": plugin.get("description", "No description available."),
                    "path": str(full_path),
                    "version": plugin.get("version", "0.0.0"),
                    "author": plugin.get("author", "Unknown")
                })
                
    except Exception as e:
        print(f"Error reading marketplace data: {e}")
        
    return skills

def get_skill_details(skill_id: str) -> Optional[Dict[str, str]]:
    """
    Get detailed information about a specific skill.
    
    Args:
        skill_id: The directory name of the skill.
        
    Returns:
        Dictionary with skill details or None if not found.
    """
    skill_path = PACKAGES_DIR / skill_id
    if not skill_path.exists():
        return None
        
    details = {
        "id": skill_id,
        "path": str(skill_path),
        "readme": "",
        "skill_def": ""
    }
    
    readme_path = skill_path / "README.md"
    if readme_path.exists():
        details["readme"] = readme_path.read_text()
        
    skill_def_path = skill_path / "SKILL.md"
    if skill_def_path.exists():
        details["skill_def"] = skill_def_path.read_text()
        
    return details
