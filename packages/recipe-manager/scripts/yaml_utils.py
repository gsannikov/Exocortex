"""
YAML utilities for recipe-manager skill.
Load, save, and validate recipe YAML files.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# Configure YAML to preserve Unicode and ordering
yaml.SafeDumper.add_representer(
    str,
    lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style=None)
)


def load_recipe(file_path: str) -> Optional[Dict]:
    """
    Load a recipe from a YAML file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Recipe dict or None if file not found
    """
    path = Path(file_path)
    if not path.exists():
        return None
    
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_recipe(recipe: Dict, file_path: str) -> bool:
    """
    Save a recipe to a YAML file.
    
    Args:
        recipe: Recipe dictionary
        file_path: Path to save the YAML file
        
    Returns:
        True if successful
    """
    path = Path(file_path)
    
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Update timestamp
    recipe['updated_at'] = datetime.now().isoformat()
    
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(
            recipe, 
            f, 
            allow_unicode=True, 
            default_flow_style=False,
            sort_keys=False,
            width=120
        )
    
    return True


def list_recipes(base_path: str, status: Optional[str] = None) -> List[Dict]:
    """
    List all recipes, optionally filtered by status.
    
    Args:
        base_path: Base path to recipes directory
        status: Optional status filter ('to-try', 'tried', 'perfected')
        
    Returns:
        List of recipe dictionaries
    """
    recipes = []
    base = Path(base_path) / 'recipes'
    
    folders = [status] if status else ['to-try', 'tried', 'perfected']
    
    for folder in folders:
        folder_path = base / folder
        if folder_path.exists():
            for yaml_file in folder_path.glob('*.yaml'):
                recipe = load_recipe(str(yaml_file))
                if recipe:
                    recipe['_path'] = str(yaml_file)
                    recipes.append(recipe)
    
    return recipes


def find_recipe_by_id(base_path: str, recipe_id: str) -> Optional[Dict]:
    """
    Find a recipe by its ID.
    
    Args:
        base_path: Base path to recipes directory
        recipe_id: Recipe ID (slug)
        
    Returns:
        Recipe dict or None
    """
    for recipe in list_recipes(base_path):
        if recipe.get('id') == recipe_id:
            return recipe
    return None


def find_recipe_by_name(base_path: str, name: str) -> Optional[Dict]:
    """
    Find a recipe by its name (case-insensitive partial match).
    
    Args:
        base_path: Base path to recipes directory
        name: Recipe name to search for
        
    Returns:
        Recipe dict or None
    """
    name_lower = name.lower()
    for recipe in list_recipes(base_path):
        if name_lower in recipe.get('name', '').lower():
            return recipe
    return None


def validate_recipe(recipe: Dict) -> List[str]:
    """
    Validate a recipe dictionary.
    
    Args:
        recipe: Recipe dictionary to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Required fields
    required = ['id', 'name', 'status']
    for field in required:
        if not recipe.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Status validation
    valid_statuses = ['To try', 'Try next', 'Tried', 'Perfected']
    if recipe.get('status') and recipe['status'] not in valid_statuses:
        errors.append(f"Invalid status: {recipe['status']}")
    
    # Rating validation
    rating = recipe.get('rating')
    if rating is not None and (not isinstance(rating, (int, float)) or rating < 1 or rating > 5):
        errors.append(f"Invalid rating: {rating} (must be 1-5)")
    
    # Ingredients should be a list
    if 'ingredients' in recipe and not isinstance(recipe['ingredients'], list):
        errors.append("Ingredients must be a list")
    
    # Instructions should be a list
    if 'instructions' in recipe and not isinstance(recipe['instructions'], list):
        errors.append("Instructions must be a list")
    
    return errors


def create_recipe_template(
    name: str,
    slug: str,
    source_url: str = "",
    source_type: str = "text",
    platform: str = "Manual"
) -> Dict:
    """
    Create a new recipe with default template.
    
    Args:
        name: Recipe name
        slug: URL-safe ID
        source_url: Optional source URL
        source_type: text, image, or video
        platform: Source platform
        
    Returns:
        Recipe dictionary with defaults
    """
    now = datetime.now()
    
    return {
        'id': slug,
        'name': name,
        'icon': '🍽️',
        
        'type': '',
        'status': 'To try',
        'rating': None,
        
        'relevant': [],
        
        'source': {
            'url': source_url,
            'type': source_type,
            'platform': platform,
            'author': '',
            'date_added': now.strftime('%Y-%m-%d')
        },
        
        'prep_time': '',
        'cook_time': '',
        'servings': None,
        'difficulty': '',
        
        'ingredients': [],
        'instructions': [],
        
        'notes': [],
        'tags': [],
        
        'created_at': now.isoformat(),
        'updated_at': now.isoformat(),
        'notion_page_id': None
    }


def move_recipe(
    base_path: str,
    recipe_id: str,
    new_status: str
) -> Optional[str]:
    """
    Move a recipe to a different status folder.
    
    Args:
        base_path: Base path to recipes directory
        recipe_id: Recipe ID to move
        new_status: Target status
        
    Returns:
        New file path or None if not found
    """
    # Find current recipe
    recipe = find_recipe_by_id(base_path, recipe_id)
    if not recipe or '_path' not in recipe:
        return None
    
    old_path = Path(recipe['_path'])
    
    # Determine new folder
    status_folder = {
        'To try': 'to-try',
        'Try next': 'to-try',
        'Tried': 'tried',
        'Perfected': 'perfected'
    }.get(new_status, 'to-try')
    
    new_path = Path(base_path) / 'recipes' / status_folder / old_path.name
    
    # Update and save
    recipe['status'] = new_status
    del recipe['_path']  # Remove internal field
    
    save_recipe(recipe, str(new_path))
    
    # Remove old file if different location
    if old_path != new_path and old_path.exists():
        old_path.unlink()
    
    return str(new_path)


if __name__ == "__main__":
    # Test validation
    test_recipe = {
        'id': 'test-recipe',
        'name': 'Test Recipe',
        'status': 'To try',
        'rating': 4,
        'ingredients': ['item 1', 'item 2'],
        'instructions': ['step 1', 'step 2']
    }
    
    errors = validate_recipe(test_recipe)
    if errors:
        print("Validation errors:", errors)
    else:
        print("Recipe is valid!")
