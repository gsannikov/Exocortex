---
title: Scoring Formulas Module
summary: Define weighted scoring logic for evaluating opportunities across multiple dimensions.
last_updated: "2025-10-29"
---

# Scoring Formulas Module v9.1

## Purpose
Calculate Income, Growth, LowPrep, Stress, and Location scores using config-driven formulas and Israeli market data.

## When to Load This Module
- **Step 6-10**: After skills matching (Step 5) completes
- **Prerequisites**: Match score calculated, company data loaded, user config available
- **Token Impact**: ~3K tokens

---

## Scoring Components Overview

| Component | Range | Weight | Based On |
|-----------|-------|--------|----------|
| Match | 0-35 | 35% | Skills fit (from Step 5) |
| Income | 0-25 | 25% | Israeli salary estimates |
| Growth | 0-20 | 20% | Company + role trajectory |
| LowPrep | 0-15 | 15% | Preparation time (inverse) |
| Stress | -10 to 0 | 10% | Role demands (penalty) |
| Location | -8 to +5 | 5% | Office + remote flexibility |
| **TOTAL** | **0-100** | **100%** | Sum of components |

**Threshold-Based Priority**:
- First Priority: ≥ config threshold (default: 54)
- Second Priority: < config threshold

---

## Configuration Integration

### Load Scoring Config

```python
def load_scoring_config(user_config):
    """
    Extract scoring parameters from user configuration
    
    Args:
        user_config: Loaded user-config.yaml
    
    Returns:
        Scoring config dict
    """
    
    scoring = user_config['scoring']
    background = user_config['background']
    preferences = user_config['preferences']
    
    # Load weights (custom if enabled, otherwise defaults)
    weights = load_scoring_weights(scoring)
    
    return {
        # Weights (custom or default)
        'weights': weights,
        'custom_weights_enabled': scoring.get('custom_weights_enabled', False),
        
        # Thresholds
        'first_priority_threshold': scoring['thresholds']['first_priority'],
        'second_priority_threshold': scoring['thresholds']['second_priority'],
        
        # Income targets
        'min_salary_annual': preferences['min_salary_annual'],
        'target_salary_annual': preferences['target_salary_annual'],
        
        # Experience
        'years_experience': background.get('years_experience', 5),
        'has_big_tech': background.get('has_big_tech_experience', False),
        
        # Location preferences
        'preferred_locations': preferences.get('preferred_locations', []),
        'work_model_preference': preferences.get('work_model_preference', 'hybrid'),
        
        # Bonuses
        'bonuses': scoring.get('bonuses', {}),
        
        # Tier preferences
        'tier_preferences': preferences.get('company_tier_preference', {})
    }


def load_scoring_weights(scoring_config: dict) -> dict:
    """
    Load weights from config with validation and fallback.
    
    Supports custom weights from setup wizard or default weights.
    
    Args:
        scoring_config: scoring section from user-config.yaml
    
    Returns:
        Validated weights dict {match: X, income: Y, ...}
    """
    # Check if custom weights are enabled
    if scoring_config.get('custom_weights_enabled', False):
        custom_weights = scoring_config.get('weights', {})
        
        # Validate custom weights
        is_valid, error_msg = validate_weights(custom_weights)
        
        if is_valid:
            print("✅ Using custom scoring weights")
            return custom_weights
        else:
            print(f"⚠️  Custom weights invalid: {error_msg}")
            print("📊 Falling back to default weights")
    
    # Default weights
    default_weights = {
        "match": 35,
        "income": 25,
        "growth": 20,
        "lowprep": 15,
        "stress": 10,
        "location": 5
    }
    
    return default_weights


def validate_weights(weights: dict) -> tuple[bool, str]:
    """
    Validate custom weights meet all requirements.
    
    Returns:
        (is_valid, error_message)
    """
    required_keys = {"match", "income", "growth", "lowprep", "stress", "location"}
    
    # Check all keys present
    if set(weights.keys()) != required_keys:
        missing = required_keys - set(weights.keys())
        return False, f"Missing keys: {missing}"
    
    # Check all values are positive numbers
    for key, value in weights.items():
        if not isinstance(value, (int, float)) or value < 0:
            return False, f"{key} must be positive number, got {value}"
    
    # Check sum equals 100
    total = sum(weights.values())
    if abs(total - 100) > 0.1:  # Allow tiny floating point errors
        return False, f"Weights must sum to 100, got {total}"
    
    # Check no extreme values (>60%)
    max_weight = max(weights.values())
    if max_weight > 60:
        max_key = max(weights.keys(), key=lambda k: weights[k])
        return False, f"{max_key} weight too high ({max_weight}%). Max: 60%"
    
    # All checks passed
    return True, ""
```

---

## Step 6: Income Estimation (0-25 points)

### Israeli Market Salary Data

```python
# Base salary ranges in NIS (monthly gross)
# Updated for 2025 Israeli tech market

ISRAELI_SALARY_RANGES = {
    'Engineering Manager': {
        'junior': (35000, 45000),      # 1-3 years management
        'mid': (45000, 60000),         # 4-7 years
        'senior': (60000, 80000),      # 8-12 years
        'principal': (80000, 100000)   # 12+ years
    },
    'Technical Program Manager': {
        'junior': (30000, 40000),
        'mid': (40000, 55000),
        'senior': (55000, 75000),
        'principal': (75000, 95000)
    },
    'AI/ML Engineering Manager': {
        'junior': (40000, 50000),
        'mid': (50000, 65000),
        'senior': (65000, 85000),
        'principal': (85000, 110000)
    },
    'Product Manager': {
        'junior': (28000, 38000),
        'mid': (38000, 50000),
        'senior': (50000, 70000),
        'principal': (70000, 90000)
    },
    'Senior Software Engineer': {
        'junior': (25000, 35000),
        'mid': (35000, 45000),
        'senior': (45000, 60000),
        'principal': (60000, 75000)
    },
    'Director': {
        'mid': (70000, 90000),
        'senior': (90000, 120000),
        'principal': (120000, 150000)
    },
    'VP Engineering': {
        'senior': (100000, 130000),
        'principal': (130000, 180000)
    }
}


# Company tier multipliers
TIER_MULTIPLIERS = {
    1: 1.25,  # Top tier (NVIDIA, Google, etc.)
    2: 1.15,  # Strong established
    3: 1.05,  # Growth stage
    4: 0.95   # Early stage
}


# Domain/technology premiums
DOMAIN_PREMIUMS = {
    'AI/ML': 1.20,              # +20%
    'Hardware': 1.15,           # +15%
    'Security': 1.15,           # +15%
    'Cloud Infrastructure': 1.12,
    'Autonomous Vehicles': 1.18,
    'Fintech': 1.10,
    'Enterprise SaaS': 1.08,
    'Standard Software': 1.0
}
```

### Map Experience to Salary Band

```python
def map_experience_to_band(years_experience, role_level_title):
    """
    Determine salary band based on experience and role
    
    Args:
        years_experience: Total years of experience
        role_level_title: Job title (to infer level)
    
    Returns:
        Band: 'junior', 'mid', 'senior', or 'principal'
    """
    
    title_lower = role_level_title.lower()
    
    # Check title for explicit level
    if any(keyword in title_lower for keyword in ['vp', 'director', 'head of']):
        if years_experience >= 15:
            return 'principal'
        else:
            return 'senior'
    
    if 'principal' in title_lower or 'staff' in title_lower:
        return 'principal'
    
    if 'senior' in title_lower or 'lead' in title_lower:
        if years_experience >= 12:
            return 'principal'
        else:
            return 'senior'
    
    # Default to experience-based
    if years_experience >= 12:
        return 'principal'
    elif years_experience >= 8:
        return 'senior'
    elif years_experience >= 4:
        return 'mid'
    else:
        return 'junior'
```

### Calculate Income Estimate

```python
def calculate_income_estimate(role_type, company_tier, domain, candidate_experience, role_title):
    """
    Estimate Israeli market salary with all factors
    
    Args:
        role_type: Job category (e.g., 'Engineering Manager')
        company_tier: 1-4 tier
        domain: Technology domain
        candidate_experience: Years of experience
        role_title: Full job title
    
    Returns:
        (low_estimate, high_estimate, monthly_mid) in NIS
    """
    
    # Normalize role type
    if role_type not in ISRAELI_SALARY_RANGES:
        # Try to match
        if 'engineer' in role_type.lower() and 'manager' in role_type.lower():
            role_type = 'Engineering Manager'
        elif 'program' in role_type.lower() or 'project' in role_type.lower():
            role_type = 'Technical Program Manager'
        elif 'product' in role_type.lower():
            role_type = 'Product Manager'
        elif 'director' in role_type.lower():
            role_type = 'Director'
        else:
            role_type = 'Senior Software Engineer'  # Default
    
    # Get experience band
    band = map_experience_to_band(candidate_experience, role_title)
    
    # Base range
    try:
        base_low, base_high = ISRAELI_SALARY_RANGES[role_type][band]
    except KeyError:
        # Fallback to mid band
        base_low, base_high = ISRAELI_SALARY_RANGES[role_type].get('mid', (40000, 60000))
    
    # Apply tier multiplier
    tier_mult = TIER_MULTIPLIERS.get(company_tier, 1.0)
    base_low *= tier_mult
    base_high *= tier_mult
    
    # Apply domain premium
    domain_mult = DOMAIN_PREMIUMS.get(domain, 1.0)
    base_low *= domain_mult
    base_high *= domain_mult
    
    # Round to nearest 1K
    low_estimate = round(base_low / 1000) * 1000
    high_estimate = round(base_high / 1000) * 1000
    mid_estimate = (low_estimate + high_estimate) / 2
    
    return (
        int(low_estimate),
        int(high_estimate),
        int(mid_estimate)
    )
```

### Convert Income to Score

```python
def income_to_score(monthly_estimate, scoring_config):
    """
    Convert monthly income estimate to 0-25 point scale
    
    Uses target salary from config for scoring curve
    
    Args:
        monthly_estimate: Monthly gross salary estimate (NIS)
        scoring_config: Config dict with salary targets
    
    Returns:
        Score 0-25
    """
    
    # Get targets from config
    min_annual = scoring_config['min_salary_annual']
    target_annual = scoring_config['target_salary_annual']
    
    min_monthly = min_annual / 12
    target_monthly = target_annual / 12
    
    # Scoring bands
    # 25 points: >= 1.5x target
    # 20 points: >= target
    # 15 points: >= 0.85x target
    # 10 points: >= min_monthly (minimum acceptable)
    # 5 points: >= 0.75x min_monthly
    # 0 points: < 0.75x min_monthly
    
    if monthly_estimate >= target_monthly * 1.5:
        score = 25
    
    elif monthly_estimate >= target_monthly:
        # Linear interpolation: target to 1.5x target = 20 to 25
        ratio = (monthly_estimate - target_monthly) / (target_monthly * 0.5)
        score = 20 + (ratio * 5)
    
    elif monthly_estimate >= target_monthly * 0.85:
        # Linear: 0.85x target to target = 15 to 20
        ratio = (monthly_estimate - target_monthly * 0.85) / (target_monthly * 0.15)
        score = 15 + (ratio * 5)
    
    elif monthly_estimate >= min_monthly:
        # Linear: min to 0.85x target = 10 to 15
        ratio = (monthly_estimate - min_monthly) / (target_monthly * 0.85 - min_monthly)
        score = 10 + (ratio * 5)
    
    elif monthly_estimate >= min_monthly * 0.75:
        # Linear: 0.75x min to min = 5 to 10
        ratio = (monthly_estimate - min_monthly * 0.75) / (min_monthly * 0.25)
        score = 5 + (ratio * 5)
    
    else:
        # Below 75% of minimum: 0-5 based on how close
        ratio = monthly_estimate / (min_monthly * 0.75)
        score = ratio * 5
    
    return round(score, 1)
```

---

## Step 7: Growth Assessment (0-20 points)

### Growth Evaluation

```python
def assess_growth_potential(company_data, role_data, scoring_config):
    """
    Calculate growth score across multiple dimensions
    
    Components:
    - Company trajectory (0-8)
    - Role scope (0-7)
    - Learning opportunities (0-5)
    - Tier bonus from config
    
    Args:
        company_data: Company frontmatter
        role_data: Job requirements dict
        scoring_config: Config with tier bonuses
    
    Returns:
        Growth score (0-20)
    """
    
    growth_score = 0
    
    # 1. Company Trajectory (0-8)
    growth_score += assess_company_trajectory(company_data)
    
    # 2. Role Scope (0-7)
    growth_score += assess_role_scope(role_data)
    
    # 3. Learning Opportunities (0-5)
    growth_score += assess_learning_opportunities(company_data, role_data)
    
    # 4. Apply tier bonus from config
    tier_bonus = scoring_config['tier_preferences'].get(f'tier_{company_data["tier"]}_bonus', 0)
    growth_score += tier_bonus
    
    # Cap at 20
    return min(20, round(growth_score, 1))


def assess_company_trajectory(company_data):
    """
    Company growth indicators (0-8 points)
    """
    
    score = 0
    
    # Funding stage (0-3)
    funding = company_data.get('funding_stage', '').lower()
    if any(stage in funding for stage in ['series d', 'series e', 'ipo', 'public']):
        score += 3
    elif any(stage in funding for stage in ['series b', 'series c']):
        score += 2
    elif 'series a' in funding:
        score += 1
    
    # Recent growth (0-2)
    if company_data.get('recent_funding', False):
        score += 1
    if company_data.get('expanding_israel', False):
        score += 1
    
    # Market position (0-2)
    tier = company_data.get('tier', 4)
    if tier == 1:
        score += 2
    elif tier == 2:
        score += 1
    
    # Glassdoor rating (0-1)
    rating = company_data.get('glassdoor_rating', 0)
    if rating and rating >= 4.0:
        score += 1
    
    return min(8, score)


def assess_role_scope(role_data):
    """
    Role growth potential (0-7 points)
    """
    
    score = 0
    
    # Team size (0-3)
    team_size = role_data.get('team_size', 0)
    if team_size >= 50:
        score += 3
    elif team_size >= 20:
        score += 2
    elif team_size >= 5:
        score += 1
    
    # Seniority level (0-2)
    title = role_data.get('position_title', '').lower()
    if any(kw in title for kw in ['director', 'vp', 'head', 'chief']):
        score += 2
    elif any(kw in title for kw in ['senior', 'lead', 'principal', 'staff']):
        score += 1
    
    # Cross-functional scope (0-2)
    responsibilities = role_data.get('responsibilities', [])
    cross_func_keywords = ['cross-functional', 'collaborate', 'stakeholders', 'multiple teams']
    
    if any(any(kw in resp.lower() for kw in cross_func_keywords) for resp in responsibilities):
        score += 2
    
    return min(7, score)


def assess_learning_opportunities(company_data, role_data):
    """
    Learning and skill development (0-5 points)
    """
    
    score = 0
    
    # Cutting-edge tech (0-2)
    tech_stack = company_data.get('tech_stack', [])
    cutting_edge = ['ai', 'ml', 'quantum', 'autonomous', 'robotics', 'blockchain']
    
    if any(any(tech in str(stack).lower() for tech in cutting_edge) for stack in tech_stack):
        score += 2
    
    # Domain complexity (0-2)
    domain = role_data.get('domain', '')
    complex_domains = ['AI/ML', 'Hardware', 'Autonomous Vehicles', 'Security']
    
    if domain in complex_domains:
        score += 2
    
    # Company tier (high visibility) (0-1)
    if company_data.get('tier', 4) <= 2:
        score += 1
    
    return min(5, score)
```

---

## Step 8: LowPrep Score (0-15 points)

### Preparation Time Calculation

```python
def calculate_prep_hours(skills_gaps, company_data, role_data):
    """
    Conservative preparation time estimate
    
    Components:
    - Company research (2-8 hours)
    - Critical skills gaps (8 hours each)
    - High priority gaps (4 hours each)
    - Nice-to-have gaps (2 hours each)
    - Interview prep (8-20 hours)
    
    Args:
        skills_gaps: Gaps dict from skills matching
        company_data: Company frontmatter
        role_data: Job requirements
    
    Returns:
        Total prep hours
    """
    
    hours = 0
    
    # Company research (varies by tier and complexity)
    tier = company_data.get('tier', 3)
    if tier == 1:
        hours += 8  # Deep research for top companies
    elif tier == 2:
        hours += 6
    else:
        hours += 4
    
    # Skills gaps
    critical_gaps = len(skills_gaps.get('critical', []))
    high_gaps = len(skills_gaps.get('high', []))
    nice_gaps = len(skills_gaps.get('nice_to_have', []))
    
    hours += critical_gaps * 8   # 8 hours per critical skill
    hours += high_gaps * 4       # 4 hours per high priority
    hours += nice_gaps * 2       # 2 hours per nice-to-have
    
    # Interview preparation
    title = role_data.get('position_title', '').lower()
    
    if any(kw in title for kw in ['director', 'vp', 'head']):
        hours += 20  # Executive-level prep
    elif any(kw in title for kw in ['senior', 'lead', 'principal']):
        hours += 15  # Senior-level prep
    else:
        hours += 12  # Standard prep
    
    return hours


def prep_time_to_score(total_hours, max_score=15):
    """
    Convert prep hours to score (inverse: less time = better)
    
    Scoring bands:
    - 0-10 hours: 15 points (minimal prep)
    - 11-20 hours: 12-14 points (light prep)
    - 21-30 hours: 9-11 points (moderate prep)
    - 31-40 hours: 6-8 points (substantial prep)
    - 41-50 hours: 3-5 points (heavy prep)
    - 51+ hours: 0-2 points (extensive prep)
    
    Args:
        total_hours: Estimated prep time
        max_score: Maximum points (default 15)
    
    Returns:
        Score 0-15
    """
    
    if total_hours <= 10:
        score = max_score
    elif total_hours <= 20:
        # Linear: 10-20 hours = 15-12
        ratio = (20 - total_hours) / 10
        score = 12 + (ratio * 3)
    elif total_hours <= 30:
        # Linear: 20-30 hours = 12-9
        ratio = (30 - total_hours) / 10
        score = 9 + (ratio * 3)
    elif total_hours <= 40:
        # Linear: 30-40 hours = 9-6
        ratio = (40 - total_hours) / 10
        score = 6 + (ratio * 3)
    elif total_hours <= 50:
        # Linear: 40-50 hours = 6-3
        ratio = (50 - total_hours) / 10
        score = 3 + (ratio * 3)
    else:
        # 50+ hours: 0-3 based on how far over
        score = max(0, 3 - ((total_hours - 50) / 25))
    
    return round(score, 1)
```

---

## Step 9: Stress Assessment (-10 to 0 points)

### Stress Calculation

```python
def calculate_stress_score(role_data, company_data):
    """
    Assess role stress level (penalty system: all negative)
    
    Factors:
    - Team size pressure
    - On-call requirements
    - Startup pressure
    - High-stakes environment
    - Travel requirements
    
    Returns:
        Score -10 to 0
    """
    
    stress_factors = 0
    
    # Team size pressure (0-2)
    team_size = role_data.get('team_size', 0)
    if team_size >= 50:
        stress_factors += 2
    elif team_size >= 20:
        stress_factors += 1
    
    # On-call/24-7 (0-2)
    responsibilities = ' '.join(role_data.get('responsibilities', [])).lower()
    if any(kw in responsibilities for kw in ['on-call', '24/7', '24-7', 'on call']):
        stress_factors += 2
    
    # Startup pressure (0-1)
    tier = company_data.get('tier', 3)
    if tier >= 3:
        stress_factors += 1
    
    # High-stakes indicators (0-2)
    high_stakes_keywords = ['critical', 'mission-critical', 'high-pressure', 'fast-paced', 'demanding']
    if any(kw in responsibilities for kw in high_stakes_keywords):
        stress_factors += 1
    
    # Travel requirements (0-1)
    if 'travel' in responsibilities:
        stress_factors += 1
    
    # Multiple products/platforms (0-1)
    if team_size >= 30:
        stress_factors += 1
    
    # Map to score (negative)
    if stress_factors == 0:
        return 0  # No stress indicators
    elif stress_factors <= 2:
        return -5  # Low stress
    elif stress_factors <= 4:
        return -7  # Medium stress
    else:
        return -10  # High stress
```

---

## Step 10: Location Score (-8 to +5 points)

### Location Scoring

```python
def calculate_location_score(office_location, work_model, scoring_config):
    """
    Score based on location and work flexibility
    
    Base scores by location (from config preferences)
    Modifiers for work model
    
    Args:
        office_location: Office city/area
        work_model: Work arrangement (remote/hybrid/office)
        scoring_config: Config with location preferences
    
    Returns:
        Score -8 to +5
    """
    
    # Base location scores
    LOCATION_BASE_SCORES = {
        'remote': 5,
        'tel aviv': 0,
        'ramat gan': 0,
        'herzliya': -4,
        'petah tikva': -4,
        'haifa': -6,
        'jerusalem': -8,
        'beer sheva': -8,
        'netanya': -5,
        'rehovot': -5
    }
    
    # Work model modifiers
    WORK_MODEL_MODIFIERS = {
        'full remote': +1,
        'remote': +1,
        'hybrid (2-3 days)': +1,
        'hybrid': 0,
        'hybrid (4 days)': -1,
        'full office': -1,
        'office': -1
    }
    
    # Normalize location
    location_lower = office_location.lower()
    
    # Get base score
    base_score = LOCATION_BASE_SCORES.get(location_lower, -4)  # Default -4
    
    # Check against preferred locations
    preferred = scoring_config.get('preferred_locations', [])
    if any(pref.lower() in location_lower for pref in preferred):
        base_score = max(base_score, 0)  # Boost to at least 0
    
    # Apply work model modifier
    work_model_lower = work_model.lower()
    modifier = 0
    
    for key, mod_value in WORK_MODEL_MODIFIERS.items():
        if key in work_model_lower:
            modifier = mod_value
            break
    
    final_score = base_score + modifier
    
    # Clamp to range
    final_score = max(-8, min(5, final_score))
    
    return final_score
```

---

## Complete Scoring Pipeline

### Generate All Scores

```python
def calculate_all_scores(match_score, company_data, role_data, skills_gaps, scoring_config):
    """
    Calculate complete score breakdown
    
    Args:
        match_score: Score from skills matching (0-35)
        company_data: Company frontmatter
        role_data: Job requirements
        skills_gaps: Skills gaps dict
        scoring_config: Loaded scoring config
    
    Returns:
        Complete scores dict
    """
    
    # Income (0-25)
    income_low, income_high, income_mid = calculate_income_estimate(
        role_type=role_data.get('role_type', 'Engineering Manager'),
        company_tier=company_data['tier'],
        domain=role_data.get('domain', 'Standard Software'),
        candidate_experience=scoring_config['years_experience'],
        role_title=role_data['position_title']
    )
    
    income_score = income_to_score(income_mid, scoring_config)
    
    # Growth (0-20)
    growth_score = assess_growth_potential(company_data, role_data, scoring_config)
    
    # LowPrep (0-15)
    prep_hours = calculate_prep_hours(skills_gaps, company_data, role_data)
    lowprep_score = prep_time_to_score(prep_hours)
    
    # Stress (-10 to 0)
    stress_score = calculate_stress_score(role_data, company_data)
    
    # Location (-8 to +5)
    location_score = calculate_location_score(
        office_location=role_data.get('location', 'Tel Aviv'),
        work_model=role_data.get('work_arrangement', 'Full Office'),
        scoring_config=scoring_config
    )
    
    # Total
    total_score = (
        match_score +
        income_score +
        growth_score +
        lowprep_score +
        stress_score +
        location_score
    )
    
    # Determine priority
    if total_score >= scoring_config['first_priority_threshold']:
        priority = "First"
        priority_emoji = "🟢"
    elif total_score >= scoring_config['second_priority_threshold']:
        priority = "Second"
        priority_emoji = "🟡"
    else:
        priority = "Third"
        priority_emoji = "🔴"
    
    return {
        'scores': {
            'match': round(match_score, 1),
            'income': round(income_score, 1),
            'growth': round(growth_score, 1),
            'lowprep': round(lowprep_score, 1),
            'stress': round(stress_score, 1),
            'location': round(location_score, 1),
            'total': round(total_score, 1)
        },
        'details': {
            'income_range': (income_low, income_high),
            'income_mid': income_mid,
            'prep_hours': prep_hours,
            'priority': priority,
            'priority_emoji': priority_emoji
        }
    }
```

---

## Module Output

### Return Format

```python
{
    'scores': {
        'match': 28.5,
        'income': 22.0,
        'growth': 16.0,
        'lowprep': 12.0,
        'stress': -7,
        'location': 0,
        'total': 71.5
    },
    'details': {
        'income_range': (55000, 75000),
        'income_mid': 65000,
        'prep_hours': 18,
        'priority': 'First',
        'priority_emoji': '🟢'
    }
}
```

---

## Helper Functions

### Utility Functions

```python
def infer_domain(job_content, company_data):
    """Infer technology domain from job and company"""
    
    content_lower = job_content.lower()
    
    # Check keywords
    if any(kw in content_lower for kw in ['ai', 'ml', 'machine learning', 'deep learning']):
        return 'AI/ML'
    
    if any(kw in content_lower for kw in ['hardware', 'chip', 'silicon', 'asic']):
        return 'Hardware'
    
    if any(kw in content_lower for kw in ['autonomous', 'self-driving', 'robotics']):
        return 'Autonomous Vehicles'
    
    if any(kw in content_lower for kw in ['security', 'cyber', 'infosec']):
        return 'Security'
    
    if any(kw in content_lower for kw in ['cloud', 'infrastructure', 'devops']):
        return 'Cloud Infrastructure'
    
    if any(kw in content_lower for kw in ['fintech', 'payment', 'banking']):
        return 'Fintech'
    
    return 'Standard Software'


def format_score_breakdown(scores_dict):
    """Format scores for display"""
    
    scores = scores_dict['scores']
    details = scores_dict['details']
    
    return f"""
Component          Score   Max    Details
───────────────────────────────────────────────
Match              {scores['match']:5.1f}    35    From skills matching
Income             {scores['income']:5.1f}    25    ₪{details['income_mid']:,}/month
Growth             {scores['growth']:5.1f}    20    Company + role potential
LowPrep            {scores['lowprep']:5.1f}    15    {details['prep_hours']} hours prep
Stress             {scores['stress']:5.1f}    10    Role demands
Location           {scores['location']:5.1f}     5    Office + work model
───────────────────────────────────────────────
TOTAL              {scores['total']:5.1f}   100    {details['priority_emoji']} {details['priority']} Priority
"""
```

---

## Module Version

**Version**: v1.1.0  
**Last Updated**: October 28, 2025  
**Architecture**: Config-driven with Israeli market data  
**Dependencies**: user-config.yaml  
**Status**: Production Ready ✅

---  
**Token Budget**: ~3K tokens
