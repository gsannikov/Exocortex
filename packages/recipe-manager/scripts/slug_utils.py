"""
Slug utilities for recipe-manager skill.
Generates URL-safe slugs with Hebrew transliteration support.
"""

import re

# Hebrew to Latin transliteration map
HEBREW_MAP = {
    'א': '', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h',
    'ו': 'v', 'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'y',
    'כ': 'k', 'ך': 'k', 'ל': 'l', 'מ': 'm', 'ם': 'm',
    'נ': 'n', 'ן': 'n', 'ס': 's', 'ע': '', 'פ': 'p',
    'ף': 'f', 'צ': 'ts', 'ץ': 'ts', 'ק': 'k', 'ר': 'r',
    'ש': 'sh', 'ת': 't',
    # Special marks
    '״': '', '׳': '', 'ּ': '', 'ְ': '', 'ֱ': '', 'ֲ': '',
    'ֳ': '', 'ִ': '', 'ֵ': '', 'ֶ': '', 'ַ': '', 'ָ': '',
    'ֹ': '', 'ֻ': '', 'ׁ': '', 'ׂ': ''
}


def transliterate_hebrew(text: str) -> str:
    """Transliterate Hebrew characters to Latin equivalents."""
    result = []
    for char in text:
        if char in HEBREW_MAP:
            result.append(HEBREW_MAP[char])
        else:
            result.append(char)
    return ''.join(result)


def generate_slug(name: str, max_length: int = 50) -> str:
    """
    Generate a URL-safe slug from a recipe name.
    
    Args:
        name: Recipe name (Hebrew or English)
        max_length: Maximum slug length
        
    Returns:
        URL-safe slug string
        
    Examples:
        >>> generate_slug("Arais Tortilla")
        'arais-tortilla'
        >>> generate_slug("עוף עם תפו״א מדורה")
        'of-im-tpva-mdvrh'
        >>> generate_slug("French Toast 🍞")
        'french-toast'
    """
    # Transliterate Hebrew
    slug = transliterate_hebrew(name)
    
    # Lowercase
    slug = slug.lower()
    
    # Replace spaces and underscores with dashes
    slug = re.sub(r'[\s_]+', '-', slug)
    
    # Remove emojis and special characters (keep only alphanumeric and dashes)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Clean up multiple dashes
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading/trailing dashes
    slug = slug.strip('-')
    
    # Truncate if needed
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    
    return slug


def ensure_unique_slug(slug: str, existing_slugs: list) -> str:
    """
    Ensure slug is unique by appending number if needed.
    
    Args:
        slug: Base slug
        existing_slugs: List of existing slugs to check against
        
    Returns:
        Unique slug (possibly with -2, -3, etc. appended)
    """
    if slug not in existing_slugs:
        return slug
    
    counter = 2
    while f"{slug}-{counter}" in existing_slugs:
        counter += 1
    
    return f"{slug}-{counter}"


if __name__ == "__main__":
    # Test cases
    test_cases = [
        "Arais Tortilla",
        "עוף עם תפו״א מדורה",
        "French Toast 🍞",
        "School Breakfast - Simple",
        "פיתה עם זעתר",
        "Banana Bread!!!",
        "  Extra   Spaces  ",
    ]
    
    print("Slug Generation Tests:")
    print("-" * 50)
    for name in test_cases:
        slug = generate_slug(name)
        print(f"'{name}' → '{slug}'")
