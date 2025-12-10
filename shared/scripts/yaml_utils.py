"""
YAML Utilities for Career Consultant Skill
Handles YAML frontmatter creation and parsing

This script runs in Claude's container.
"""

from typing import Any, Dict, Tuple

import yaml


def create_yaml_document(frontmatter: Dict[str, Any], content: str) -> str:
    """
    Create markdown document with YAML frontmatter.
    
    Args:
        frontmatter: Dictionary to be serialized as YAML
        content: Markdown content to follow the frontmatter
        
    Returns:
        Complete markdown document with YAML frontmatter
        
    Example:
        >>> frontmatter = {'title': 'Test', 'date': '2025-01-01'}
        >>> content = '# Test Document'
        >>> doc = create_yaml_document(frontmatter, content)
        >>> print(doc)
        ---
        title: Test
        date: '2025-01-01'
        ---
        
        # Test Document
    """
    # Serialize frontmatter to YAML
    yaml_text = yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        indent=2
    )
    
    # Combine with content
    return f"---\n{yaml_text}---\n\n{content}\n"


def parse_yaml_frontmatter(markdown: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract YAML frontmatter and content from markdown document.
    
    Args:
        markdown: Markdown document with YAML frontmatter
        
    Returns:
        Tuple of (frontmatter_dict, content_str)
        
    Example:
        >>> doc = "---\\ntitle: Test\\n---\\n\\n# Content"
        >>> frontmatter, content = parse_yaml_frontmatter(doc)
        >>> frontmatter['title']
        'Test'
        >>> '# Content' in content
        True
    """
    # Split on --- delimiters
    parts = markdown.split('---', 2)
    
    # Check if valid frontmatter exists
    if len(parts) < 3:
        return {}, markdown
    
    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(parts[1])
        if frontmatter is None:
            frontmatter = {}
    except yaml.YAMLError as e:
        print(f"Warning: YAML parse error: {e}")
        frontmatter = {}
    
    # Extract content (everything after second ---)
    content = parts[2].strip()
    
    return frontmatter, content


def get_yaml_field(markdown: str, field: str) -> Any:
    """
    Extract a specific field from YAML frontmatter.
    
    Args:
        markdown: Markdown document with YAML frontmatter
        field: Field name to extract
        
    Returns:
        Field value or None if not found
    """
    frontmatter, _ = parse_yaml_frontmatter(markdown)
    return frontmatter.get(field)


def update_yaml_field(markdown: str, field: str, value: Any) -> str:
    """
    Update a specific field in YAML frontmatter.
    
    Args:
        markdown: Markdown document with YAML frontmatter
        field: Field name to update
        value: New value for the field
        
    Returns:
        Updated markdown document
    """
    frontmatter, content = parse_yaml_frontmatter(markdown)
    frontmatter[field] = value
    return create_yaml_document(frontmatter, content)


def merge_yaml_frontmatter(markdown: str, updates: Dict[str, Any]) -> str:
    """
    Merge updates into existing YAML frontmatter.
    
    Args:
        markdown: Markdown document with YAML frontmatter
        updates: Dictionary of fields to update
        
    Returns:
        Updated markdown document
    """
    frontmatter, content = parse_yaml_frontmatter(markdown)
    frontmatter.update(updates)
    return create_yaml_document(frontmatter, content)


def validate_yaml_frontmatter(markdown: str, required_fields: list) -> bool:
    """
    Validate that required fields exist in YAML frontmatter.
    
    Args:
        markdown: Markdown document with YAML frontmatter
        required_fields: List of required field names
        
    Returns:
        True if all required fields exist
        
    Raises:
        ValueError: If required fields are missing
    """
    frontmatter, _ = parse_yaml_frontmatter(markdown)
    
    missing_fields = []
    for field in required_fields:
        if field not in frontmatter:
            missing_fields.append(field)
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return True


def yaml_to_dict(yaml_file_path: str) -> Dict[str, Any]:
    """
    Load YAML file and return as dictionary.
    
    Args:
        yaml_file_path: Path to YAML file
        
    Returns:
        Dictionary representation of YAML
    """
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def dict_to_yaml(data: Dict[str, Any], output_path: str) -> None:
    """
    Save dictionary as YAML file.
    
    Args:
        data: Dictionary to save
        output_path: Path to save YAML file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2
        )


# Example usage
if __name__ == "__main__":
    # Test create_yaml_document
    frontmatter = {
        'title': 'Test Document',
        'date': '2025-01-01',
        'tags': ['test', 'example']
    }
    content = "# Test Document\n\nThis is test content."
    
    doc = create_yaml_document(frontmatter, content)
    print("Created document:")
    print(doc)
    print("\n" + "="*50 + "\n")
    
    # Test parse_yaml_frontmatter
    parsed_frontmatter, parsed_content = parse_yaml_frontmatter(doc)
    print("Parsed frontmatter:")
    print(parsed_frontmatter)
    print("\nParsed content:")
    print(parsed_content)
    print("\n" + "="*50 + "\n")
    
    # Test update_yaml_field
    updated_doc = update_yaml_field(doc, 'updated', True)
    print("Updated document:")
    print(updated_doc)
