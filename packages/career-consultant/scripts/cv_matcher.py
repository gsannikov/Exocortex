"""
CV Matcher for Career Consultant Skill
Dynamically loads and matches CVs based on user configuration

This script runs in Claude's container and accesses CVs via MCP Filesystem.
"""

from typing import Dict, List, Tuple, Any
import re


def load_user_cvs(user_data_base: str, cv_variants: List[Dict]) -> Dict[str, Dict]:
    """
    Dynamically load CVs based on user configuration.
    
    Args:
        user_data_base: Path to user-data directory
        cv_variants: List of CV variant configurations
        
    Returns:
        Dictionary mapping CV IDs to CV data
    """
    cvs = {}
    
    for variant in cv_variants:
        cv_id = variant['id']
        cv_filename = variant['filename']
        cv_path = f"{user_data_base}/config/cv-variants/{cv_filename}"
        
        try:
            with open(cv_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cvs[cv_id] = {
                'content': content,
                'focus': variant['focus'],
                'weight': variant.get('weight', 1.0),
                'filename': cv_filename
            }
            
        except FileNotFoundError:
            print(f"⚠️ Warning: CV not found: {cv_path}")
            continue
        except Exception as e:
            print(f"⚠️ Error loading CV {cv_filename}: {e}")
            continue
    
    if not cvs:
        raise ValueError("No CVs could be loaded. Check your CV files exist.")
    
    return cvs


def extract_skills_from_cv(cv_content: str) -> List[str]:
    """
    Extract skills from CV content.
    
    Args:
        cv_content: Full CV content
        
    Returns:
        List of identified skills
    """
    skills = []
    
    # Common skill patterns
    skill_patterns = [
        r'(?i)python',
        r'(?i)java(?!script)',
        r'(?i)javascript',
        r'(?i)react',
        r'(?i)aws',
        r'(?i)kubernetes',
        r'(?i)docker',
        r'(?i)machine learning',
        r'(?i)ai',
        r'(?i)data science',
        r'(?i)sql',
        r'(?i)leadership',
        r'(?i)management',
        r'(?i)agile',
        r'(?i)scrum'
    ]
    
    for pattern in skill_patterns:
        if re.search(pattern, cv_content):
            skill_name = pattern.replace('(?i)', '').replace('(?!script)', '')
            skills.append(skill_name)
    
    return skills


def calculate_match_score(
    job_requirements: str,
    cv_content: str,
    focus_area: str
) -> int:
    """
    Calculate match score between job requirements and CV.
    
    This is a simplified scoring function. The actual implementation
    should be more sophisticated based on the skills-matching module.
    
    Args:
        job_requirements: Job requirements text
        cv_content: CV content
        focus_area: CV focus area
        
    Returns:
        Match score (0-35)
    """
    score = 0
    
    # Extract keywords from job requirements
    job_keywords = set(re.findall(r'\b\w+\b', job_requirements.lower()))
    cv_keywords = set(re.findall(r'\b\w+\b', cv_content.lower()))
    
    # Calculate keyword overlap
    common_keywords = job_keywords.intersection(cv_keywords)
    keyword_match_ratio = len(common_keywords) / len(job_keywords) if job_keywords else 0
    
    # Base score from keyword matching
    score += int(keyword_match_ratio * 25)
    
    # Bonus for focus area match
    if focus_area.lower() in job_requirements.lower():
        score += 5
    
    # Check for senior/leadership terms
    leadership_terms = ['senior', 'lead', 'manager', 'director', 'principal']
    if any(term in job_requirements.lower() for term in leadership_terms):
        if any(term in cv_content.lower() for term in leadership_terms):
            score += 5
    
    return min(score, 35)


def find_best_cv_match(
    job_requirements: str,
    cvs: Dict[str, Dict],
    scoring_weights: Dict[str, int]
) -> Tuple[str, int, Dict[str, int]]:
    """
    Find best CV match for job requirements.
    
    Args:
        job_requirements: Job requirements text
        cvs: Dictionary of loaded CVs
        scoring_weights: Scoring weight configuration
        
    Returns:
        Tuple of (best_cv_id, best_score, all_scores)
    """
    match_scores = {}
    
    for cv_id, cv_data in cvs.items():
        score = calculate_match_score(
            job_requirements,
            cv_data['content'],
            cv_data['focus']
        )
        
        # Apply weight if specified
        weight = cv_data.get('weight', 1.0)
        adjusted_score = int(score * weight)
        
        match_scores[cv_id] = adjusted_score
    
    # Find best match
    best_cv_id = max(match_scores, key=match_scores.get)
    best_score = match_scores[best_cv_id]
    
    # Cap at max allowed by scoring weights
    max_score = scoring_weights.get('match', 35)
    best_score = min(best_score, max_score)
    
    return best_cv_id, best_score, match_scores


def identify_skill_gaps(
    job_requirements: str,
    cv_content: str
) -> Dict[str, List[str]]:
    """
    Identify skill gaps between job requirements and CV.
    
    Args:
        job_requirements: Job requirements text
        cv_content: CV content
        
    Returns:
        Dictionary with 'critical' and 'nice_to_have' gaps
    """
    gaps = {
        'critical': [],
        'nice_to_have': []
    }
    
    # Common critical skills
    critical_skills = [
        'python', 'java', 'aws', 'kubernetes', 
        'leadership', 'management', 'agile'
    ]
    
    for skill in critical_skills:
        if skill in job_requirements.lower() and skill not in cv_content.lower():
            gaps['critical'].append(skill.title())
    
    return gaps


# Example usage
if __name__ == "__main__":
    import sys
    from config_loader import load_user_config, get_cv_variants, get_scoring_weights
    
    if len(sys.argv) < 2:
        print("Usage: python cv_matcher.py <user_data_base>")
        sys.exit(1)
    
    user_data_base = sys.argv[1]
    
    try:
        # Load config
        config = load_user_config(user_data_base)
        cv_variants = get_cv_variants(config)
        scoring_weights = get_scoring_weights(config)
        
        # Load CVs
        cvs = load_user_cvs(user_data_base, cv_variants)
        
        print(f"✅ Loaded {len(cvs)} CV variant(s):")
        for cv_id, cv_data in cvs.items():
            print(f"  - {cv_id}: {cv_data['focus']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
