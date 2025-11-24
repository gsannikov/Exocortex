---
module_name: setup-wizard
version: 1.0.0
description: Interactive setup wizard for personalizing scoring weights and preferences
token_cost: ~3-5K tokens
dependencies: []
status: active
---

# Setup Wizard Module

## Purpose

This module provides an interactive setup experience to help users personalize their Career Consultant configuration, particularly the scoring weights that determine job priority rankings.

## When to Load This Module

Load this module when:
- User is setting up the skill for the first time
- User explicitly requests to customize scoring: "customize my scoring weights"
- User wants to reset preferences: "reset my preferences"
- `settings.yaml` doesn't have `custom_weights_enabled: true`

## Token Budget

- First-time setup: ~3-5K tokens (questionnaire + validation)
- Weight recalculation: ~1-2K tokens

## Core Workflow

### Step 1: Introduction

```markdown
🎯 **Personalization Wizard**

This wizard will help you customize how jobs are scored and ranked.

The Career Consultant uses 6 scoring components:
1. **Match** - How well your skills align with the job
2. **Income** - Salary potential vs. your requirements
3. **Growth** - Career advancement opportunities
4. **LowPrep** - How quickly you can interview (less prep = higher score)
5. **Stress** - Work-life balance and role demands
6. **Location** - Commute and location preferences

By default, these have preset weights (Match: 35%, Income: 25%, Growth: 20%, etc.)

**Would you like to customize these weights based on your priorities?**
- Yes - Continue with questionnaire (5 questions, 2 minutes)
- No - Use default weights
- Learn More - See detailed explanation
```

### Step 2: Priority Questionnaire

Ask the user to rate importance on a scale of 1-10 for each component:

```python
questions = [
    {
        "component": "match",
        "question": "How important is skills match? (Strong alignment with your experience)",
        "scale": "1 = Not important, 10 = Critical",
        "context": "Higher weight → Favor jobs matching your exact skills"
    },
    {
        "component": "income",
        "question": "How important is salary/compensation?",
        "scale": "1 = Not important, 10 = Critical",
        "context": "Higher weight → Prioritize highest-paying opportunities"
    },
    {
        "component": "growth",
        "question": "How important is career growth potential?",
        "scale": "1 = Not important, 10 = Critical",
        "context": "Higher weight → Favor roles with advancement opportunities"
    },
    {
        "component": "lowprep",
        "question": "How important is minimal interview preparation?",
        "scale": "1 = Not important, 10 = Critical",
        "context": "Higher weight → Favor jobs you can interview for quickly"
    },
    {
        "component": "stress",
        "question": "How important is low stress / work-life balance?",
        "scale": "1 = Not important, 10 = Critical",
        "context": "Higher weight → Avoid high-stress roles"
    },
    {
        "component": "location",
        "question": "How important is location/commute?",
        "scale": "1 = Not important, 10 = Critical",
        "context": "Higher weight → Strong preference for remote/close locations"
    }
]
```

### Step 3: Calculate Custom Weights

Convert user priorities to percentage weights that sum to 100:

```python
def calculate_weights(priorities: dict) -> dict:
    """
    Convert 1-10 priorities to percentage weights.
    
    Args:
        priorities: {"match": 8, "income": 9, "growth": 7, "lowprep": 5, "stress": 8, "location": 4}
    
    Returns:
        {"match": 24, "income": 27, "growth": 21, "lowprep": 15, "stress": 24, "location": 12}
    """
    total = sum(priorities.values())
    
    # Convert to percentages (raw)
    raw_weights = {k: (v / total * 100) for k, v in priorities.items()}
    
    # Round to integers while preserving sum = 100
    weights = {k: round(v) for k, v in raw_weights.items()}
    
    # Adjust for rounding errors to ensure sum = 100
    current_sum = sum(weights.values())
    difference = 100 - current_sum
    
    if difference != 0:
        # Add/subtract from largest component
        largest_key = max(weights.keys(), key=lambda k: weights[k])
        weights[largest_key] += difference
    
    return weights

# Example:
priorities = {
    "match": 8,
    "income": 10,
    "growth": 7,
    "lowprep": 3,
    "stress": 9,
    "location": 2
}

weights = calculate_weights(priorities)
# Output: {"match": 21, "income": 26, "growth": 18, "lowprep": 8, "stress": 23, "location": 5}
```

### Step 4: Show Preview and Confirm

Display the calculated weights for user review:

```markdown
📊 **Your Custom Scoring Weights**

Based on your priorities:

Component    | Weight | Impact
-------------|--------|------------------
Match        | 21%    | Moderate priority
Income       | 26%    | ⭐ Highest priority
Growth       | 18%    | Moderate priority
LowPrep      | 8%     | Lower priority
Stress       | 23%    | High priority
Location     | 5%     | Lower priority

**What this means:**
- Jobs will be ranked primarily by: **Income** (26%) and **Stress/WLB** (23%)
- Skills match and career growth are moderately important
- Quick interview prep and location are less critical

**Does this reflect your priorities?**
- Yes - Save and apply these weights
- No - Adjust priorities (re-run questionnaire)
- Reset - Use default weights instead
```

### Step 5: Save to Configuration

Update `user-data/profile/settings.yaml`:

```yaml
# Custom Scoring Weights (Wizard-Generated)
scoring:
  custom_weights_enabled: true
  custom_weights_date: "2025-11-20"
  
  # User priorities (1-10 scale, for reference)
  user_priorities:
    match: 8
    income: 10
    growth: 7
    lowprep: 3
    stress: 9
    location: 2
  
  # Calculated weights (must sum to 100)
  weights:
    match: 21
    income: 26
    growth: 18
    lowprep: 8
    stress: 23
    location: 5
  
  # Thresholds remain the same
  thresholds:
    first_priority: 54
    second_priority: 40
  
  bonuses:
    intel_experience: 0
    startup_experience: 0
```

### Step 6: Confirmation

```markdown
✅ **Configuration Saved**

Your custom scoring weights have been applied!

**Next Steps:**
- Analyze your first job: Share a job URL
- Review settings: "Show my configuration"
- Adjust weights later: "Customize scoring weights"

💡 **Tip:** You can always re-run this wizard to adjust your priorities as your job search evolves.
```

## Advanced Features

### Preset Templates

Offer common templates for quick setup:

```python
presets = {
    "balanced": {
        "match": 25, "income": 20, "growth": 20, 
        "lowprep": 15, "stress": 15, "location": 5
    },
    "money_focused": {
        "match": 20, "income": 35, "growth": 20,
        "lowprep": 10, "stress": 10, "location": 5
    },
    "work_life_balance": {
        "match": 20, "income": 15, "growth": 15,
        "lowprep": 15, "stress": 30, "location": 5
    },
    "career_growth": {
        "match": 25, "income": 15, "growth": 35,
        "lowprep": 10, "stress": 10, "location": 5
    },
    "quick_switch": {
        "match": 30, "income": 20, "growth": 10,
        "lowprep": 30, "stress": 5, "location": 5
    }
}
```

### Configuration Review

Command: "Show my scoring configuration"

```markdown
⚙️ **Your Scoring Configuration**

**Custom Weights:** ✅ Enabled (set on 2025-11-20)

Component | Weight | Default | Difference
----------|--------|---------|------------
Match     | 21%    | 35%     | -14% ⬇️
Income    | 26%    | 25%     | +1% ➡️
Growth    | 18%    | 20%     | -2% ⬇️
LowPrep   | 8%     | 15%     | -7% ⬇️
Stress    | 23%    | 10%     | +13% ⬆️
Location  | 5%     | 5%      | 0% ➡️

**Your Priority Profile:**
You prioritize **income** and **work-life balance** over quick interview prep. You're willing to invest more time in preparation for the right opportunity.

**Commands:**
- "Recustomize weights" - Run wizard again
- "Use default weights" - Switch back to preset values
- "Compare scoring" - See how a job scores with custom vs. default
```

### Weight Validation

Always validate before saving:

```python
def validate_weights(weights: dict) -> tuple[bool, str]:
    """
    Validate custom weights meet requirements.
    
    Returns:
        (is_valid, error_message)
    """
    required_keys = {"match", "income", "growth", "lowprep", "stress", "location"}
    
    # Check all keys present
    if set(weights.keys()) != required_keys:
        return False, f"Missing keys: {required_keys - set(weights.keys())}"
    
    # Check all values are positive integers
    for key, value in weights.items():
        if not isinstance(value, int) or value < 0:
            return False, f"{key} must be a positive integer, got {value}"
    
    # Check sum equals 100
    total = sum(weights.values())
    if total != 100:
        return False, f"Weights must sum to 100, got {total}"
    
    # Check no value exceeds 50 (avoid extreme weights)
    max_weight = max(weights.values())
    if max_weight > 50:
        max_key = max(weights.keys(), key=lambda k: weights[k])
        return False, f"{max_key} weight too high ({max_weight}%). Max recommended: 50%"
    
    # Check no value is zero (all components should have some weight)
    if any(v == 0 for v in weights.values()):
        zero_keys = [k for k, v in weights.items() if v == 0]
        return False, f"Components cannot be 0%: {zero_keys}. Minimum: 1%"
    
    return True, ""

# Example usage:
is_valid, error = validate_weights({"match": 21, "income": 26, ...})
if not is_valid:
    print(f"❌ Invalid weights: {error}")
```

## Integration with Scoring Module

The scoring-formulas module should read weights from config:

```python
# In scoring-formulas.md module:

def load_scoring_weights(user_config: dict) -> dict:
    """
    Load weights from user config, with fallback to defaults.
    """
    if user_config.get('scoring', {}).get('custom_weights_enabled', False):
        weights = user_config['scoring']['weights']
        
        # Validate before using
        is_valid, error = validate_weights(weights)
        if is_valid:
            print("✅ Using custom weights")
            return weights
        else:
            print(f"⚠️ Custom weights invalid: {error}")
            print("Falling back to default weights")
    
    # Default weights
    return {
        "match": 35,
        "income": 25,
        "growth": 20,
        "lowprep": 15,
        "stress": 10,
        "location": 5
    }
```

## Error Handling

Handle edge cases gracefully:

1. **User provides invalid input** → Re-ask with clarification
2. **User quits mid-wizard** → Save partial progress, offer to resume
3. **Weights sum validation fails** → Auto-adjust and show what changed
4. **Config file write fails** → Show manual instructions

## Usage Examples

### Example 1: First-Time User

```
User: "I just installed the skill"

Skill: [Runs first-time setup]
"Would you like to customize scoring weights?" → Yes

Q1: Skills match importance? → 8/10
Q2: Salary importance? → 10/10
Q3: Growth importance? → 6/10
Q4: Low prep importance? → 3/10
Q5: Work-life balance importance? → 9/10
Q6: Location importance? → 2/10

Calculated weights:
- Match: 21%, Income: 26%, Growth: 16%, LowPrep: 8%, Stress: 24%, Location: 5%

User confirms → Weights saved ✅
```

### Example 2: Recustomize Weights

```
User: "I want to recustomize my scoring weights"

Skill: [Loads current weights]
"Your current custom weights: Income (26%), Stress (24%), Match (21%)..."
"Would you like to adjust?" → Yes

[Re-runs questionnaire, saves new weights]
```

### Example 3: Compare Scoring Systems

```
User: "How would this job score with default vs. custom weights?"

Skill: [Loads both weight sets]

Job: Google Israel - EM

Default Weights:
- Match: 32/35, Income: 23/25, Growth: 18/20, LowPrep: 12/15, Stress: -8/10, Location: 0/5
- Total: 77/100 (First Priority)

Custom Weights (Income-focused):
- Match: 19/21, Income: 24/26, Growth: 14/16, LowPrep: 6/8, Stress: -19/24, Location: 0/5
- Total: 44/100 (Second Priority)

Analysis: With custom weights, this job drops from First to Second Priority because it has higher stress, which you weight more heavily (24% vs default 10%).
```

## Implementation Checklist

- [x] Questionnaire design (6 questions)
- [x] Weight calculation algorithm
- [x] Validation rules
- [x] Configuration save format
- [x] Preview/confirmation flow
- [x] Preset templates
- [x] Integration with scoring module
- [x] Error handling
- [x] Usage examples

## Version History

- **v1.0.0** (2025-11-20): Initial release

---

**Module Status**: Active  
**Last Updated**: 2025-11-20  
**Dependencies**: None (standalone module)
