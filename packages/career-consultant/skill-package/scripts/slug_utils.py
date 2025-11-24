"""
Slug Utilities for Career Consultant Skill
Handles string normalization for file names and IDs

This script runs in Claude's container.
"""

import re
from typing import Optional


def normalize_slug(text: str, max_length: Optional[int] = None) -> str:
    """
    Create URL-safe slug from text.
    
    Args:
        text: Text to convert to slug
        max_length: Maximum length of slug (optional)
        
    Returns:
        Normalized slug string
        
    Examples:
        >>> normalize_slug("Hello World!")
        'hello-world'
        >>> normalize_slug("Test & Demo Company")
        'test-demo-company'
        >>> normalize_slug("Company (Israel) Ltd.")
        'company-israel-ltd'
    """
    if not text:
        return ""
    
    # Convert to lowercase
    slug = str(text).lower().strip()
    
    # Replace special characters with spaces
    slug = re.sub(r'[&()]', ' ', slug)
    
    # Remove non-word characters (except spaces and hyphens)
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace multiple spaces/hyphens with single hyphen
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Limit length if specified
    if max_length and len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    
    return slug


def create_role_id(company_name: str, job_title: str, date_str: str) -> str:
    """
    Create unique role ID from components.
    
    Args:
        company_name: Company name
        job_title: Job title
        date_str: Date string (format: YYYYMMDD)
        
    Returns:
        Role ID string
        
    Example:
        >>> create_role_id("Google", "Senior Engineer", "20250128")
        'google-senior-engineer-20250128'
    """
    company_slug = normalize_slug(company_name)
    title_slug = normalize_slug(job_title)
    
    return f"{company_slug}-{title_slug}-{date_str}"


def create_company_id(company_name: str) -> str:
    """
    Create company ID from company name.
    
    Args:
        company_name: Company name
        
    Returns:
        Company ID string
        
    Example:
        >>> create_company_id("Microsoft Corporation")
        'microsoft-corporation'
    """
    return normalize_slug(company_name)


def extract_company_from_url(url: str) -> str:
    """
    Extract company name from job posting URL.
    
    This is a simplified version. The actual implementation
    should handle various job board URL formats.
    
    Args:
        url: Job posting URL
        
    Returns:
        Extracted company name
        
    Examples:
        >>> extract_company_from_url("https://linkedin.com/jobs/google-engineer")
        'google'
        >>> extract_company_from_url("https://jobs.lever.co/companyname/role-id")
        'companyname'
    """
    # Common patterns
    patterns = [
        r'linkedin\.com/(?:jobs/view|jobs|company)/([^/-]+)',
        r'jobs\.lever\.co/([^/]+)',
        r'greenhouse\.io/([^/]+)',
        r'boards\.greenhouse\.io/([^/]+)',
        r'(?:www\.)?([^/.]+)\.com/careers',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url.lower())
        if match:
            return match.group(1)
    
    # Fallback: extract from domain
    domain_match = re.search(r'https?://(?:www\.)?([^/.]+)', url.lower())
    if domain_match:
        return domain_match.group(1)
    
    return "unknown-company"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to be filesystem-safe.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
        
    Example:
        >>> sanitize_filename("Company: Report (2025).md")
        'company-report-2025.md'
    """
    # Split extension
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
    else:
        name, ext = filename, ''
    
    # Sanitize name part
    safe_name = normalize_slug(name)
    
    # Reassemble
    return f"{safe_name}.{ext}" if ext else safe_name


def is_valid_slug(slug: str) -> bool:
    """
    Check if string is a valid slug format.
    
    Args:
        slug: String to validate
        
    Returns:
        True if valid slug format
        
    Example:
        >>> is_valid_slug("valid-slug-123")
        True
        >>> is_valid_slug("Invalid Slug!")
        False
    """
    if not slug:
        return False
    
    # Check for invalid characters
    if not re.match(r'^[a-z0-9-]+$', slug):
        return False
    
    # Check for leading/trailing hyphens
    if slug.startswith('-') or slug.endswith('-'):
        return False
    
    # Check for consecutive hyphens
    if '--' in slug:
        return False
    
    return True


def truncate_slug(slug: str, max_length: int = 50, preserve_words: bool = True) -> str:
    """
    Truncate slug to maximum length.
    
    Args:
        slug: Slug to truncate
        max_length: Maximum length
        preserve_words: Try to preserve whole words
        
    Returns:
        Truncated slug
        
    Example:
        >>> truncate_slug("very-long-slug-name-that-needs-truncating", 20)
        'very-long-slug-name'
    """
    if len(slug) <= max_length:
        return slug
    
    if preserve_words:
        # Try to break at hyphen
        truncated = slug[:max_length]
        last_hyphen = truncated.rfind('-')
        if last_hyphen > 0:
            return truncated[:last_hyphen]
    
    # Just truncate at max length
    return slug[:max_length].rstrip('-')


# Example usage
if __name__ == "__main__":
    # Test normalize_slug
    test_strings = [
        "Hello World!",
        "Test & Demo Company",
        "Company (Israel) Ltd.",
        "Special@#$Characters",
        "Multiple   Spaces",
    ]
    
    print("Slug Normalization Tests:")
    for text in test_strings:
        slug = normalize_slug(text)
        print(f"  '{text}' -> '{slug}'")
    
    print("\n" + "="*50 + "\n")
    
    # Test role ID creation
    role_id = create_role_id("Google Israel", "Senior Software Engineer", "20250128")
    print(f"Role ID: {role_id}")
    
    print("\n" + "="*50 + "\n")
    
    # Test URL extraction
    test_urls = [
        "https://www.linkedin.com/jobs/google-engineer",
        "https://jobs.lever.co/companyname/role-id",
        "https://example.com/careers/job-123"
    ]
    
    print("Company Extraction Tests:")
    for url in test_urls:
        company = extract_company_from_url(url)
        print(f"  {url}")
        print(f"  -> {company}\n")
    
    print("="*50 + "\n")
    
    # Test slug validation
    test_slugs = [
        "valid-slug-123",
        "Invalid Slug!",
        "-leading-hyphen",
        "trailing-hyphen-",
        "double--hyphen"
    ]
    
    print("Slug Validation Tests:")
    for slug in test_slugs:
        valid = is_valid_slug(slug)
        status = "✅" if valid else "❌"
        print(f"  {status} '{slug}'")
