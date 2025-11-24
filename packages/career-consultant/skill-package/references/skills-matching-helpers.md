# Skills Matching - Helper Functions

## Utility Functions for Skill Matching

These helper functions are referenced in skills-matching.md and provide supporting functionality for the core matching algorithm.

### Generate Skill Variations

```python
def generate_skill_variations(skill):
    """
    Generate common variations of a skill name
    
    Handles:
    - Hyphen vs space variations (e.g., "machine-learning" vs "machine learning")
    - Hyphen vs concatenated (e.g., "machine-learning" vs "machinelearning")
    - Acronyms (e.g., "ML" for "Machine Learning")
    
    Args:
        skill: Original skill name
    
    Returns:
        List of skill variations to check
    """
    
    variations = [skill]
    
    # Add common variations
    if '-' in skill:
        variations.append(skill.replace('-', ' '))
        variations.append(skill.replace('-', ''))
    
    if ' ' in skill:
        variations.append(skill.replace(' ', '-'))
        variations.append(skill.replace(' ', ''))
    
    # Add acronyms if applicable
    words = skill.split()
    if len(words) > 1:
        acronym = ''.join([w[0].upper() for w in words])
        variations.append(acronym)
    
    # Add lowercase acronym
    if len(words) > 1:
        acronym_lower = ''.join([w[0].lower() for w in words])
        variations.append(acronym_lower)
    
    return variations


# Example usage:
# generate_skill_variations("Machine Learning")
# Returns: ["Machine Learning", "Machine-Learning", "MachineLearning", "ML", "ml"]
```

### Extract Years of Experience

```python
def extract_years_experience(context, skill):
    """
    Extract years of experience from context string
    
    Patterns matched:
    - "X years of [skill]"
    - "[skill] for X years"
    - "X+ years [skill]"
    - "X years' [skill] experience"
    
    Args:
        context: Text context around the skill mention
        skill: Skill name to search for
    
    Returns:
        int: Number of years, or None if not found
    """
    
    import re
    
    # Pattern: "X years of [skill]" or "[skill] for X years"
    patterns = [
        rf'(\d+)\+?\s*years?\s+(?:of\s+)?{re.escape(skill)}',
        rf'{re.escape(skill)}\s+for\s+(\d+)\+?\s*years?',
        rf'(\d+)\+?\s*years?\s+{re.escape(skill)}',
        rf'{re.escape(skill)}\s+(?:experience\s+)?(?:of\s+)?(\d+)\+?\s*years?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, context, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None


# Example usage:
# extract_years_experience("5+ years of Python experience", "Python")
# Returns: 5
```

### Get Skill Context

```python
def get_skill_context(skill, text, window=50):
    """
    Get context around skill mention for proficiency assessment
    
    Args:
        skill: Skill name to find
        text: Full text to search in
        window: Number of characters before/after to include
    
    Returns:
        str: Context string, or empty if skill not found
    """
    
    skill_lower = skill.lower()
    text_lower = text.lower()
    
    pos = text_lower.find(skill_lower)
    if pos == -1:
        return ""
    
    start = max(0, pos - window)
    end = min(len(text), pos + len(skill) + window)
    
    return text[start:end]


# Example usage:
# get_skill_context("Python", "Led team using Python for backend...", window=20)
# Returns: "Led team using Python for backend"
```

## Advanced Matching Utilities

### Fuzzy Skill Matching

```python
def fuzzy_match_skill(skill, text, threshold=0.8):
    """
    Fuzzy matching for skills with typos or variations
    
    Uses similarity ratio to find close matches
    
    Args:
        skill: Skill to search for
        text: Text to search in
        threshold: Minimum similarity (0.0 to 1.0)
    
    Returns:
        tuple: (found, matched_text, similarity_score)
    """
    
    from difflib import SequenceMatcher
    
    skill_lower = skill.lower()
    text_lower = text.lower()
    
    # Check for exact match first
    if skill_lower in text_lower:
        return (True, skill, 1.0)
    
    # Split text into words and check similarity
    words = text_lower.split()
    best_match = None
    best_score = 0.0
    
    for word in words:
        score = SequenceMatcher(None, skill_lower, word).ratio()
        if score > best_score and score >= threshold:
            best_score = score
            best_match = word
    
    if best_match:
        return (True, best_match, best_score)
    
    return (False, None, 0.0)
```

### Skill Category Detection

```python
def categorize_skill_domain(skill):
    """
    Categorize skill into domain (programming, cloud, database, etc.)
    
    Helps with weighting and proficiency assessment
    
    Args:
        skill: Skill name
    
    Returns:
        str: Domain category
    """
    
    skill_lower = skill.lower()
    
    # Programming languages
    programming = ['python', 'java', 'javascript', 'c++', 'go', 'rust', 'typescript']
    if any(lang in skill_lower for lang in programming):
        return 'programming_language'
    
    # Cloud platforms
    cloud = ['aws', 'azure', 'gcp', 'google cloud', 'cloud']
    if any(c in skill_lower for c in cloud):
        return 'cloud_platform'
    
    # Databases
    databases = ['sql', 'postgres', 'mysql', 'mongodb', 'redis', 'database']
    if any(db in skill_lower for db in databases):
        return 'database'
    
    # Frameworks
    frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring']
    if any(fw in skill_lower for fw in frameworks):
        return 'framework'
    
    # DevOps/Tools
    devops = ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform']
    if any(tool in skill_lower for tool in devops):
        return 'devops'
    
    # Default
    return 'general'
```

## Proficiency Assessment Helpers

### Context Analysis Keywords

```python
# Keywords for proficiency levels
PROFICIENCY_KEYWORDS = {
    'expert': ['expert', 'architected', 'designed', 'led', 'taught', 'mentored', 'established'],
    'advanced': ['extensive', 'deep', 'advanced', 'specialist', 'senior'],
    'proficient': ['proficient', 'experienced', 'skilled', 'competent'],
    'intermediate': ['familiar', 'working knowledge', 'some experience'],
    'basic': ['basic', 'learning', 'beginner', 'introduction']
}

def assess_proficiency_from_keywords(context):
    """
    Quick proficiency assessment from keyword analysis
    """
    
    context_lower = context.lower()
    
    for level, keywords in PROFICIENCY_KEYWORDS.items():
        if any(kw in context_lower for kw in keywords):
            return level
    
    return 'intermediate'  # Default
```

---

**Purpose**: Helper functions for skills-matching.md  
**Usage**: Reference when implementing skill matching features  
**Last Updated**: October 28, 2025
