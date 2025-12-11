# Scoring Pattern Module

## Overview

Multi-dimensional evaluation with configurable weights and component scores.

## Score Architecture

### Components

Define scoring components relevant to your domain:

```yaml
# config/scoring.yaml
components:
  component1:
    name: "Component 1 Name"
    weight: 0.25
    description: "What this measures"
    
  component2:
    name: "Component 2 Name"  
    weight: 0.25
    description: "What this measures"
    
  component3:
    name: "Component 3 Name"
    weight: 0.25
    description: "What this measures"
    
  component4:
    name: "Component 4 Name"
    weight: 0.25
    description: "What this measures"

# Weights must sum to 1.0
```

### Score Calculation

```python
def calculate_score(item: dict, config: dict) -> dict:
    """
    Calculate weighted score from component scores.
    Each component score is 0-100.
    """
    scores = {}
    total = 0
    
    for component, settings in config['components'].items():
        # Get raw score (0-100)
        raw_score = evaluate_component(item, component)
        scores[component] = raw_score
        
        # Apply weight
        weighted = raw_score * settings['weight']
        total += weighted
    
    return {
        'total': round(total, 1),
        'components': scores,
        'calculated_at': datetime.now().isoformat()
    }
```

### Component Evaluation

Each component needs its own evaluation logic:

```python
def evaluate_component(item: dict, component: str) -> float:
    """
    Return score 0-100 for specific component.
    """
    if component == 'component1':
        # Your evaluation logic
        return calculate_component1_score(item)
    elif component == 'component2':
        return calculate_component2_score(item)
    # ... etc
```

## Score Storage

```yaml
# Item with scores
- id: item-001
  title: "Item Title"
  data:
    field1: value
    field2: value
  scores:
    total: 78.5
    components:
      component1: 85
      component2: 70
      component3: 80
      component4: 79
    calculated_at: 2025-12-11T10:00:00Z
```

## Ranking

```python
def rank_items(items: list, min_score: float = 0) -> list:
    """
    Return items sorted by total score, filtered by minimum.
    """
    filtered = [i for i in items if i['scores']['total'] >= min_score]
    return sorted(filtered, key=lambda x: x['scores']['total'], reverse=True)
```

## Display Format

```
┌────────────────────────────────────────────────────────┐
│ ITEM: {title}                           SCORE: {total} │
├────────────────────────────────────────────────────────┤
│ Component 1: ████████░░ 85                             │
│ Component 2: ███████░░░ 70                             │
│ Component 3: ████████░░ 80                             │
│ Component 4: ████████░░ 79                             │
└────────────────────────────────────────────────────────┘
```

## Customization

Users can override weights:
```
"Prioritize component1 heavily"
→ Adjust weights: component1=0.5, others=0.167 each
→ Recalculate all scores
```
