---
title: Skills Matching Module
summary: Match candidate CV data to role requirements with weighted scoring and gap analysis.
last_updated: "2025-10-29"
---

# Skills Matching Module v9.1

## Purpose
Intelligent CV-to-job matching with proficiency weighting, gap analysis, and dynamic multi-CV support.

## When to Load This Module
- **Step 5**: After company context loaded and job requirements parsed
- **Prerequisites**: Job description available, user config loaded
- **Token Impact**: ~2K module + ~8K for CVs = ~10K total

---

## Core Capabilities

- 🎯 **Multi-CV Comparison** - Match 1-N CV variants dynamically
- 📊 **Proficiency Weighting** - 1-10 scale for skill depth
- 🔍 **Gap Analysis** - Critical vs. nice-to-have gaps
- 🏆 **Best Fit Selection** - Automatic optimal CV recommendation
- 🎁 **Config-Driven Bonuses** - Intel bonus and other adjustments

---

## Configuration and Setup

### Load CV Variants from Config

```python
def load_cv_variants(user_config, USER_DATA_BASE):
    """
    Dynamically load CV files based on user configuration
    
    Supports 1 to N CV variants
    
    Args:
        user_config: Loaded user-config.yaml
        USER_DATA_BASE: Base path to user data
    
    Returns:
        Dict of {cv_id: cv_data}
    """
    
    cv_variants = user_config['cv_variants']['variants']
    cv_base = f"{USER_DATA_BASE}/{user_config['paths']['cv_base']}"
    
    print(f"📄 Loading {len(cv_variants)} CV variant(s)...")
    
    cvs = {}
    errors = []
    
    for variant in cv_variants:
        cv_id = variant['id']
        cv_filename = variant['filename']
        cv_path = f"{cv_base}/{cv_filename}"
        
        try:
            with open(cv_path, 'r', encoding='utf-8') as f:
                cv_content = f.read()
            
            cvs[cv_id] = {
                'content': cv_content,
                'focus': variant['focus'],
                'weight': variant.get('weight', 1.0),
                'filename': cv_filename
            }
            
            print(f"  ✅ {cv_id}: {variant['focus']}")
        
        except FileNotFoundError:
            error_msg = f"CV not found: {cv_filename}"
            errors.append(error_msg)
            print(f"  ⚠️ {error_msg}")
        
        except Exception as e:
            error_msg = f"Error loading {cv_filename}: {e}"
            errors.append(error_msg)
            print(f"  ⚠️ {error_msg}")
    
    if not cvs:
        raise ValueError(f"No CVs loaded. Errors: {', '.join(errors)}")
    
    print(f"✅ Loaded {len(cvs)} CV(s) successfully")
    
    return cvs
```

---

## Job Requirements Extraction

### Parse Job Description

```python
def extract_job_requirements(job_content, company_data):
    """
    Parse job description for technical and soft skill requirements
    
    Args:
        job_content: Full job description text
        company_data: Company frontmatter for context
    
    Returns:
        Dict of categorized requirements
    """
    
    requirements = {
        'position_title': extract_position_title(job_content),
        'location': extract_location(job_content),
        'technical_skills': extract_technical_skills(job_content),
        'soft_skills': extract_soft_skills(job_content),
        'experience_years': extract_experience_requirement(job_content),
        'role_level': infer_role_level(job_content),
        'team_size': extract_team_size_mention(job_content),
        'responsibilities': extract_key_responsibilities(job_content),
        'work_arrangement': extract_work_model(job_content),
        'domain': infer_domain(job_content, company_data)
    }
    
    # Categorize skills by importance
    requirements['categorized_skills'] = categorize_skills_by_importance(
        requirements['technical_skills'],
        job_content
    )
    
    return requirements


def categorize_skills_by_importance(skills_list, job_content):
    """
    Categorize skills as critical, high, medium, or low importance
    
    Critical: Must-have, required, mandatory
    High: Preferred, strong plus, desired
    Medium: Nice to have, bonus
    Low: Mentioned but not emphasized
    """
    
    job_lower = job_content.lower()
    
    categorized = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }
    
    # Keywords for importance
    critical_keywords = ['required', 'must have', 'mandatory', 'essential']
    high_keywords = ['preferred', 'strong', 'desired', 'important']
    medium_keywords = ['nice to have', 'bonus', 'plus', 'advantage']
    
    for skill in skills_list:
        skill_lower = skill.lower()
        
        # Find skill context in job description
        skill_context = get_skill_context(skill_lower, job_lower, window=50)
        
        if any(kw in skill_context for kw in critical_keywords):
            importance = 'critical'
            required = True
        elif any(kw in skill_context for kw in high_keywords):
            importance = 'high'
            required = False
        elif any(kw in skill_context for kw in medium_keywords):
            importance = 'medium'
            required = False
        else:
            importance = 'low'
            required = False
        
        categorized[importance].append({
            'skill': skill,
            'importance': importance,
            'required': required,
            'weight': {'critical': 3.0, 'high': 2.0, 'medium': 1.5, 'low': 1.0}[importance]
        })
    
    return categorized
```

---

## Skills Matching Algorithm

### Core Matching Logic

```python
def calculate_cv_match(job_requirements, cv_content, cv_id):
    """
    Match a single CV against job requirements with proficiency weighting
    
    Proficiency Scale (1-10):
    10: Expert - Can teach, architect, lead. 5+ years deep experience
    8-9: Advanced - Complex independent work. 3-5 years
    6-7: Proficient - Daily effective use. 1-3 years
    4-5: Intermediate - Can work with guidance
    2-3: Basic - Learning phase, limited experience
    1: Minimal - Awareness only
    
    Args:
        job_requirements: Parsed job requirements dict
        cv_content: CV text content
        cv_id: CV identifier for logging
    
    Returns:
        Match result dict with scores and analysis
    """
    
    matches = {
        'strong': [],      # Proficiency 8-10
        'good': [],        # Proficiency 6-7
        'adequate': [],    # Proficiency 4-5
        'weak': []         # Proficiency 1-3
    }
    
    gaps = {
        'critical': [],    # Required but missing
        'high': [],        # Important but missing
        'nice_to_have': [] # Optional but missing
    }
    
    total_weight = 0
    matched_weight = 0
    
    # Process all categorized skills
    all_requirements = []
    for importance_level, skills in job_requirements['categorized_skills'].items():
        all_requirements.extend(skills)
    
    for req in all_requirements:
        skill = req['skill']
        importance = req['importance']
        required = req['required']
        weight = req['weight']
        
        total_weight += weight
        
        # Search for skill in CV
        cv_match = find_skill_in_cv(skill, cv_content)
        
        if cv_match:
            # Assess proficiency level
            proficiency = assess_skill_proficiency(
                skill=skill,
                cv_content=cv_content,
                match_context=cv_match
            )
            
            match_entry = {
                'skill': skill,
                'proficiency': proficiency,
                'weight': weight,
                'context': cv_match['context'][:100]  # First 100 chars
            }
            
            # Categorize by proficiency
            if proficiency >= 8:
                matches['strong'].append(match_entry)
                matched_weight += weight * (proficiency / 10)
            elif proficiency >= 6:
                matches['good'].append(match_entry)
                matched_weight += weight * (proficiency / 10)
            elif proficiency >= 4:
                matches['adequate'].append(match_entry)
                matched_weight += weight * (proficiency / 10)
            else:
                matches['weak'].append(match_entry)
                matched_weight += weight * (proficiency / 10)
        
        else:
            # Skill not found - it's a gap
            gap_entry = {
                'skill': skill,
                'importance': importance,
                'required': required,
                'weight': weight
            }
            
            if importance == 'critical':
                gaps['critical'].append(gap_entry)
            elif importance == 'high':
                gaps['high'].append(gap_entry)
            else:
                gaps['nice_to_have'].append(gap_entry)
    
    # Calculate match percentage
    match_percentage = (matched_weight / total_weight * 100) if total_weight > 0 else 0
    
    return {
        'cv_id': cv_id,
        'match_percentage': round(match_percentage, 1),
        'matches': matches,
        'gaps': gaps,
        'total_weight': total_weight,
        'matched_weight': round(matched_weight, 2),
        'match_counts': {
            'strong': len(matches['strong']),
            'good': len(matches['good']),
            'adequate': len(matches['adequate']),
            'weak': len(matches['weak']),
            'critical_gaps': len(gaps['critical']),
            'high_gaps': len(gaps['high']),
            'nice_gaps': len(gaps['nice_to_have'])
        }
    }


def find_skill_in_cv(skill, cv_content):
    """
    Find skill mention in CV with context
    
    Args:
        skill: Skill to search for
        cv_content: CV text
    
    Returns:
        Match dict or None
    """
    
    cv_lower = cv_content.lower()
    skill_lower = skill.lower()
    
    # Direct match
    if skill_lower in cv_lower:
        # Find position and extract context
        pos = cv_lower.index(skill_lower)
        context_start = max(0, pos - 100)
        context_end = min(len(cv_content), pos + len(skill) + 100)
        
        return {
            'found': True,
            'position': pos,
            'context': cv_content[context_start:context_end],
            'exact_match': True
        }
    
    # Fuzzy match for variations
    skill_variations = generate_skill_variations(skill)
    
    for variation in skill_variations:
        if variation.lower() in cv_lower:
            pos = cv_lower.index(variation.lower())
            context_start = max(0, pos - 100)
            context_end = min(len(cv_content), pos + len(variation) + 100)
            
            return {
                'found': True,
                'position': pos,
                'context': cv_content[context_start:context_end],
                'exact_match': False,
                'matched_variation': variation
            }
    
    return None


def assess_skill_proficiency(skill, cv_content, match_context):
    """
    Assess proficiency level (1-10) based on CV evidence
    
    Factors:
    - Years of experience mentioned
    - Leadership/teaching indicators
    - Depth indicators (architected, designed, led)
    - Breadth indicators (projects, companies)
    - Recency (current role vs. past)
    
    Args:
        skill: Skill name
        cv_content: Full CV content
        match_context: Context dict from find_skill_in_cv
    
    Returns:
        Proficiency score 1-10
    """
    
    context_lower = match_context['context'].lower()
    cv_lower = cv_content.lower()
    skill_lower = skill.lower()
    
    proficiency = 5  # Start at intermediate
    
    # Leadership indicators (+3)
    leadership_keywords = ['led', 'architected', 'designed', 'mentored', 'taught', 'established']
    if any(kw in context_lower for kw in leadership_keywords):
        proficiency += 3
    
    # Deep experience indicators (+2)
    depth_keywords = ['expert', 'extensive', 'deep', 'advanced', 'specialist']
    if any(kw in context_lower for kw in depth_keywords):
        proficiency += 2
    
    # Years mentioned (+1 to +3)
    years_match = extract_years_experience(context_lower, skill_lower)
    if years_match:
        if years_match >= 5:
            proficiency += 3
        elif years_match >= 3:
            proficiency += 2
        else:
            proficiency += 1
    
    # Recency (+1 if current role)
    if 'current' in context_lower or 'present' in context_lower:
        proficiency += 1
    
    # Multiple mentions (+1)
    mentions = cv_lower.count(skill_lower)
    if mentions >= 3:
        proficiency += 1
    
    # Cap at 10
    proficiency = min(10, proficiency)
    
    # Lower bound at 1
    proficiency = max(1, proficiency)
    
    return proficiency
```

---

## Multi-CV Comparison

### Compare All CVs

```python
def compare_all_cvs(job_requirements, cvs):
    """
    Match job against all CV variants and rank them
    
    Args:
        job_requirements: Parsed job requirements
        cvs: Dict of loaded CVs
    
    Returns:
        Comparison results with ranking
    """
    
    print(f"🔍 Comparing {len(cvs)} CV variant(s) against job...")
    
    all_results = {}
    
    for cv_id, cv_data in cvs.items():
        print(f"  Analyzing: {cv_id}...")
        
        match_result = calculate_cv_match(
            job_requirements=job_requirements,
            cv_content=cv_data['content'],
            cv_id=cv_id
        )
        
        # Apply CV weight from config
        weighted_percentage = match_result['match_percentage'] * cv_data['weight']
        match_result['weighted_percentage'] = round(weighted_percentage, 1)
        match_result['cv_focus'] = cv_data['focus']
        
        all_results[cv_id] = match_result
        
        print(f"    ✅ {match_result['match_percentage']:.1f}% match ({match_result['match_counts']['strong']} strong)")
    
    # Rank by weighted percentage
    ranked = sorted(
        all_results.items(),
        key=lambda x: x[1]['weighted_percentage'],
        reverse=True
    )
    
    best_cv_id = ranked[0][0]
    best_cv_result = ranked[0][1]
    
    print(f"\n🏆 Best Match: {best_cv_id} ({best_cv_result['match_percentage']:.1f}%)")
    
    return {
        'best_cv': best_cv_id,
        'best_cv_result': best_cv_result,
        'all_results': all_results,
        'ranking': [(cv_id, result['match_percentage']) for cv_id, result in ranked]
    }
```

---

## Bonus Calculations

### Intel Bonus Detection

```python
def check_bonuses(job_description, company_data, user_config):
    """
    Check for configured bonuses
    
    Args:
        job_description: Job description text
        company_data: Company frontmatter
        user_config: User configuration
    
    Returns:
        Dict of applicable bonuses
    """
    
    bonuses = user_config['scoring']['bonuses']
    applicable = {}
    
    # Intel bonus
    intel_bonus = bonuses.get('intel_experience', 0)
    
    if intel_bonus > 0:
        company_lower = company_data['company_name'].lower()
        job_lower = job_description.lower()
        
        intel_indicators = ['intel', 'mobileye', 'habana']
        
        if any(ind in company_lower for ind in intel_indicators) or \
           any(ind in job_lower for ind in intel_indicators):
            applicable['intel'] = intel_bonus
            print(f"🎁 Intel bonus detected: +{intel_bonus} points")
    
    # Could add more bonuses here based on config
    # Example: hardware_bonus, ai_bonus, etc.
    
    return applicable
```

---

## Score Calculation

### Convert Match to Score (0-35)

```python
def calculate_match_score(best_match_result, applicable_bonuses, scoring_weights):
    """
    Convert match percentage to 0-35 point scale with bonuses
    
    Scoring bands:
    - 90-100%: 30-35 points (exceptional match)
    - 80-89%: 25-29 points (excellent match)
    - 70-79%: 20-24 points (strong match)
    - 60-69%: 15-19 points (good match)
    - 50-59%: 10-14 points (adequate match)
    - 40-49%: 5-9 points (weak match)
    - <40%: 0-4 points (poor match)
    
    Args:
        best_match_result: Best CV match result dict
        applicable_bonuses: Dict of bonuses to apply
        scoring_weights: User config scoring weights
    
    Returns:
        Final match score (0-35)
    """
    
    match_pct = best_match_result['match_percentage']
    max_match_score = scoring_weights['match']  # Default: 35
    
    # Calculate base score from percentage
    if match_pct >= 90:
        base = 30 + ((match_pct - 90) / 10) * 5
    elif match_pct >= 80:
        base = 25 + ((match_pct - 80) / 10) * 5
    elif match_pct >= 70:
        base = 20 + ((match_pct - 70) / 10) * 5
    elif match_pct >= 60:
        base = 15 + ((match_pct - 60) / 10) * 5
    elif match_pct >= 50:
        base = 10 + ((match_pct - 50) / 10) * 5
    elif match_pct >= 40:
        base = 5 + ((match_pct - 40) / 10) * 5
    else:
        base = (match_pct / 40) * 5
    
    # Add bonuses
    total_bonus = sum(applicable_bonuses.values())
    final_score = base + total_bonus
    
    # Cap at max_match_score
    final_score = min(max_match_score, final_score)
    
    return round(final_score, 1)
```

---

## Analysis Generation

### Generate Match Analysis Markdown

```python
def generate_match_analysis_markdown(comparison_results, match_score, bonuses):
    """
    Create detailed match analysis in markdown format
    
    Args:
        comparison_results: Results from compare_all_cvs
        match_score: Calculated match score (0-35)
        bonuses: Dict of applicable bonuses
    
    Returns:
        Formatted markdown string
    """
    
    best_cv = comparison_results['best_cv']
    best_result = comparison_results['best_cv_result']
    all_results = comparison_results['all_results']
    
    analysis = f"""### Match Analysis: {match_score}/35 points

**Best CV**: {best_cv} ({best_result['match_percentage']:.1f}% match)  
**Focus**: {best_result['cv_focus']}
"""
    
    # Add bonuses if any
    if bonuses:
        analysis += "\n**Bonuses Applied**:\n"
        for bonus_name, bonus_value in bonuses.items():
            analysis += f"- {bonus_name.replace('_', ' ').title()}: +{bonus_value} points\n"
    
    # Strong matches
    analysis += f"\n#### Strong Matches ({best_result['match_counts']['strong']})\n"
    
    if best_result['matches']['strong']:
        for match in best_result['matches']['strong'][:10]:  # Top 10
            analysis += f"- **{match['skill']}** (proficiency: {match['proficiency']}/10)\n"
    else:
        analysis += "*No strong matches*\n"
    
    # Good matches
    analysis += f"\n#### Good Matches ({best_result['match_counts']['good']})\n"
    
    if best_result['matches']['good']:
        for match in best_result['matches']['good'][:8]:  # Top 8
            analysis += f"- {match['skill']} (proficiency: {match['proficiency']}/10)\n"
    else:
        analysis += "*No good matches*\n"
    
    # Critical gaps
    if best_result['gaps']['critical']:
        analysis += f"\n#### ⚠️ Critical Gaps ({len(best_result['gaps']['critical'])})\n"
        for gap in best_result['gaps']['critical']:
            analysis += f"- **{gap['skill']}** (required)\n"
    
    # High priority gaps
    if best_result['gaps']['high']:
        analysis += f"\n#### High Priority Gaps ({len(best_result['gaps']['high'])})\n"
        for gap in best_result['gaps']['high'][:5]:  # Top 5
            analysis += f"- {gap['skill']}\n"
    
    # CV Rankings
    analysis += "\n#### All CV Rankings\n"
    
    for cv_id, match_pct in comparison_results['ranking']:
        symbol = "🏆" if cv_id == best_cv else "  "
        focus = all_results[cv_id]['cv_focus']
        analysis += f"{symbol} **{cv_id}**: {match_pct:.1f}% ({focus})\n"
    
    return analysis
```

---

## Preparation Strategy

### Generate Prep Recommendations

```python
def generate_prep_strategy(best_result, company_data):
    """
    Create targeted preparation strategy based on gaps
    
    Args:
        best_result: Best CV match result
        company_data: Company frontmatter
    
    Returns:
        Preparation recommendations dict
    """
    
    critical_gaps = best_result['gaps']['critical']
    high_gaps = best_result['gaps']['high']
    
    total_gaps = len(critical_gaps) + len(high_gaps)
    
    # Estimate prep time
    critical_hours = len(critical_gaps) * 8
    high_hours = len(high_gaps) * 4
    company_research_hours = 4 if company_data['tier'] <= 2 else 6
    interview_prep_hours = 12
    
    total_hours = critical_hours + high_hours + company_research_hours + interview_prep_hours
    
    strategy = {
        'total_hours': total_hours,
        'breakdown': {
            'critical_skills': critical_hours,
            'high_priority_skills': high_hours,
            'company_research': company_research_hours,
            'interview_prep': interview_prep_hours
        },
        'priority_order': [],
        'resources': []
    }
    
    # Priority order
    if critical_gaps:
        strategy['priority_order'].append({
            'phase': 'Critical Skills',
            'hours': critical_hours,
            'skills': [g['skill'] for g in critical_gaps]
        })
    
    if high_gaps:
        strategy['priority_order'].append({
            'phase': 'High Priority Skills',
            'hours': high_hours,
            'skills': [g['skill'] for g in high_gaps[:3]]  # Top 3
        })
    
    strategy['priority_order'].extend([
        {'phase': 'Company Research', 'hours': company_research_hours},
        {'phase': 'Interview Preparation', 'hours': interview_prep_hours}
    ])
    
    return strategy
```

---

## Module Output

### Return Format

```python
def format_module_output(comparison_results, match_score, bonuses, prep_strategy):
    """
    Format complete module output
    
    Returns:
        Dict with all match results
    """
    
    best_result = comparison_results['best_cv_result']
    
    return {
        # Score
        'match_score': match_score,
        'match_percentage': best_result['match_percentage'],
        
        # Best CV
        'best_cv': comparison_results['best_cv'],
        'best_cv_focus': best_result['cv_focus'],
        
        # Bonuses
        'bonuses_applied': bonuses,
        'total_bonus': sum(bonuses.values()),
        
        # Gaps
        'critical_gaps': [g['skill'] for g in best_result['gaps']['critical']],
        'high_gaps': [g['skill'] for g in best_result['gaps']['high']],
        'nice_gaps': [g['skill'] for g in best_result['gaps']['nice_to_have']],
        
        # Matches
        'strong_matches': [m['skill'] for m in best_result['matches']['strong']],
        'match_counts': best_result['match_counts'],
        
        # Analysis
        'analysis_markdown': generate_match_analysis_markdown(
            comparison_results, 
            match_score, 
            bonuses
        ),
        
        # Preparation
        'prep_hours': prep_strategy['total_hours'],
        'prep_strategy': prep_strategy,
        
        # Full results
        'all_cv_results': comparison_results['all_results'],
        'cv_ranking': comparison_results['ranking']
    }
```

---

## Helper Functions

> **📚 Helper Functions**: Utility functions for skill matching (generate_skill_variations, 
> extract_years_experience, get_skill_context) are documented in 
> [references/skills-matching-helpers.md](../references/skills-matching-helpers.md)

---

## Error Handling

### Safe Matching Operations

```python
def safe_cv_match(job_requirements, cv_content, cv_id):
    """
    Wrap matching with error handling
    
    Returns partial results on failure
    """
    
    try:
        return calculate_cv_match(job_requirements, cv_content, cv_id)
    
    except Exception as e:
        print(f"⚠️ Error matching {cv_id}: {e}")
        
        # Return minimal result
        return {
            'cv_id': cv_id,
            'match_percentage': 0,
            'error': str(e),
            'matches': {'strong': [], 'good': [], 'adequate': [], 'weak': []},
            'gaps': {'critical': [], 'high': [], 'nice_to_have': []},
            'match_counts': {
                'strong': 0, 'good': 0, 'adequate': 0, 'weak': 0,
                'critical_gaps': 0, 'high_gaps': 0, 'nice_gaps': 0
            }
        }
```

---

## Module Interface

### Input Requirements

```python
{
    'job_requirements': dict,   # From job parsing
    'user_config': dict,        # From user-config.yaml
    'USER_DATA_BASE': str,      # Base path
    'company_data': dict,       # Company frontmatter
    'job_description': str      # Full job text
}
```

### Output Format

```python
{
    'match_score': float,       # 0-35
    'best_cv': str,             # CV ID
    'match_percentage': float,  # 0-100
    'critical_gaps': list,      # Critical missing skills
    'analysis_markdown': str,   # Full analysis
    'prep_hours': int,          # Estimated prep time
    'all_cv_results': dict      # Complete results
}
```

---

## Token Budget

**Module Size**: ~2K tokens  
**CVs Load**: ~8K tokens (varies with CV count)  
**Total Impact**: ~10K tokens  
**Loaded**: Only in Step 5 (skills matching phase)

---

## Module Version

**Version**: v1.1.0  
**Last Updated**: October 28, 2025  
**Architecture**: Dynamic multi-CV with config-driven paths  
**Dependencies**: user-config.yaml, CV files  
**Status**: Production Ready ✅

---  
**Key Feature**: Supports 1-N CV variants dynamically
