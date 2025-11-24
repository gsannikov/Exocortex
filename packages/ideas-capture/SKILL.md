---
name: ideas-capture
description: Capture fleeting ideas via Apple Notes inbox. AI expands, evaluates, scores potential, and organizes by type (Patent, Startup, Business, Project). Commands - "process ideas", "show ideas", "expand [idea]", "evaluate [idea]".
---

# 💡 Ideas Capture

Capture → Expand → Evaluate → Track

## 🌟 Key Capabilities
1. **Apple Notes Inbox**: Quick capture to "💡 Ideas Inbox" note
2. **AI Expansion**: Turn 1-line ideas into detailed concepts
3. **Potential Scoring**: Rate feasibility, impact, effort
4. **Type Classification**: Patent, Startup, Business, Project, Other
5. **Idea Linking**: Connect related ideas across types

## ⚙️ Storage Configuration

**User Data Location**: `~/MyDrive/claude-skills-data/ideas-capture/`

```
ideas-capture/
├── ideas.yaml            # Main database
├── expanded/             # Full idea documents
│   └── {slug}.md
└── config.yaml           # User preferences
```

## 🚀 Commands

| Command | Action |
|---------|--------|
| `process ideas` | Process all ideas from Apple Notes inbox |
| `show ideas` | List all ideas by type |
| `show [type] ideas` | Filter by type (patent/startup/business/project) |
| `expand: [idea]` | Generate detailed expansion |
| `evaluate: [idea]` | Score and analyze potential |
| `link ideas: [A] + [B]` | Connect related ideas |
| `search ideas: [query]` | Find by keyword |

## 🏷️ Idea Types

| Tag | Type | Description |
|-----|------|-------------|
| 🔬 | Patent | Novel inventions, technical innovations |
| 🚀 | Startup | Business ventures, product ideas |
| 💼 | Business | Process improvements, revenue ideas |
| 🛠️ | Project | Personal/side projects, tools |
| 💭 | Other | Misc ideas, thoughts |

## 📋 Workflow: Process Ideas

### Step 1: Read Apple Notes Inbox

```python
def process_ideas_inbox():
    """
    Read 💡 Ideas Inbox note, parse ideas with types.
    """
    note_content = Read and Write Apple Notes:get_note_content(
        note_name="💡 Ideas Inbox"
    )
    
    # Parse ideas - format: [TYPE] idea text
    # or just plain text (auto-classify)
    
    ideas = []
    for line in note_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('━') or line.startswith('✅'):
            continue
            
        # Check for type prefix
        idea_type = 'other'
        idea_text = line
        
        if '🔬' in line or '[Patent]' in line.lower():
            idea_type = 'patent'
            idea_text = line.replace('🔬', '').replace('[Patent]', '').strip()
        elif '🚀' in line or '[Startup]' in line.lower():
            idea_type = 'startup'
            idea_text = line.replace('🚀', '').replace('[Startup]', '').strip()
        elif '💼' in line or '[Business]' in line.lower():
            idea_type = 'business'
            idea_text = line.replace('💼', '').replace('[Business]', '').strip()
        elif '🛠️' in line or '[Project]' in line.lower():
            idea_type = 'project'
            idea_text = line.replace('🛠️', '').replace('[Project]', '').strip()
        elif '💭' in line or '[Other]' in line.lower():
            idea_type = 'other'
            idea_text = line.replace('💭', '').replace('[Other]', '').strip()
        
        if idea_text and len(idea_text) > 3:
            ideas.append({
                'raw': idea_text,
                'type': idea_type
            })
    
    return ideas
```

### Step 2: AI Expansion

```python
def expand_idea(idea_raw, idea_type):
    """
    Use AI to expand a brief idea into a detailed concept.
    """
    
    expansion_prompts = {
        'patent': """
            Expand this invention idea:
            - Problem it solves
            - Technical approach
            - Key innovations (what's novel)
            - Prior art considerations
            - Potential claims
        """,
        'startup': """
            Expand this startup idea:
            - Problem & market need
            - Solution overview
            - Target customers
            - Business model
            - Competitive advantage
            - MVP features
        """,
        'business': """
            Expand this business idea:
            - Current pain point
            - Proposed improvement
            - Implementation steps
            - Expected ROI
            - Risks & mitigations
        """,
        'project': """
            Expand this project idea:
            - Goal & purpose
            - Key features
            - Tech stack suggestions
            - Time estimate
            - First steps
        """,
        'other': """
            Expand this idea:
            - Core concept
            - Potential applications
            - Next steps to explore
        """
    }
    
    prompt = expansion_prompts.get(idea_type, expansion_prompts['other'])
    
    # AI generates expansion
    expansion = ai_expand(idea_raw, prompt)
    
    return expansion
```

### Step 3: Potential Scoring

```python
def score_idea(idea, expansion):
    """
    Score idea on multiple dimensions (1-10 scale).
    """
    scores = {
        'feasibility': 0,      # How realistic to implement
        'impact': 0,           # Potential value/change
        'effort': 0,           # Resources required (inverted - low effort = high score)
        'uniqueness': 0,       # How novel/differentiated
        'timing': 0,           # Market/tech readiness
        'personal_fit': 0      # Alignment with your skills/interests
    }
    
    # AI scoring with reasoning
    for dimension in scores:
        score, reason = ai_score(idea, expansion, dimension)
        scores[dimension] = score
    
    # Overall score (weighted average)
    weights = {
        'feasibility': 0.20,
        'impact': 0.25,
        'effort': 0.15,
        'uniqueness': 0.15,
        'timing': 0.15,
        'personal_fit': 0.10
    }
    
    overall = sum(scores[d] * weights[d] for d in scores)
    
    return {
        'scores': scores,
        'overall': round(overall, 1),
        'tier': 'Hot' if overall >= 7 else 'Warm' if overall >= 5 else 'Cold'
    }
```

### Step 4: Save to Database

```python
def save_idea(idea_raw, idea_type, expansion, scoring, user_data_base):
    """
    Save idea to YAML database and create expansion file.
    """
    import yaml
    from datetime import datetime
    
    # Generate slug
    slug = slugify(idea_raw[:50])
    
    # Load database
    db_path = f"{user_data_base}/ideas.yaml"
    db = yaml.safe_load(open(db_path)) or {'ideas': []}
    
    # Create entry
    entry = {
        'slug': slug,
        'raw': idea_raw,
        'type': idea_type,
        'added_date': datetime.now().isoformat(),
        'status': 'new',  # new → exploring → active → parked → done
        'scores': scoring['scores'],
        'overall_score': scoring['overall'],
        'tier': scoring['tier'],
        'tags': [],
        'related_ideas': []
    }
    
    db['ideas'].append(entry)
    
    # Save database
    with open(db_path, 'w') as f:
        yaml.dump(db, f, sort_keys=False, allow_unicode=True)
    
    # Save expansion file
    type_icons = {'patent': '🔬', 'startup': '🚀', 'business': '💼', 'project': '🛠️', 'other': '💭'}
    expansion_path = f"{user_data_base}/expanded/{slug}.md"
    
    expansion_content = f"""# {type_icons[idea_type]} {idea_raw[:80]}

**Type**: {idea_type.title()}
**Added**: {entry['added_date']}
**Status**: {entry['status']}
**Score**: {scoring['overall']}/10 ({scoring['tier']})

## Scores
| Dimension | Score |
|-----------|-------|
| Feasibility | {scoring['scores']['feasibility']}/10 |
| Impact | {scoring['scores']['impact']}/10 |
| Effort (low=good) | {scoring['scores']['effort']}/10 |
| Uniqueness | {scoring['scores']['uniqueness']}/10 |
| Timing | {scoring['scores']['timing']}/10 |
| Personal Fit | {scoring['scores']['personal_fit']}/10 |

## Expansion

{expansion}

## Next Steps
- [ ] Research competitors/prior art
- [ ] Validate problem with potential users
- [ ] Create rough prototype/mockup
- [ ] Estimate resources needed

## Notes
_Add your thoughts here..._
"""
    
    with open(expansion_path, 'w') as f:
        f.write(expansion_content)
    
    return {'status': 'added', 'slug': slug, 'entry': entry}
```

## 📊 Output Templates

### Ideas Dashboard (show ideas)

```markdown
# 💡 Ideas Dashboard

## 🔥 Hot Ideas (Score ≥7)
| Idea | Type | Score | Status |
|------|------|-------|--------|
| AI-powered resume optimizer | 🚀 Startup | 8.2 | exploring |

## 🌡️ Warm Ideas (Score 5-7)
...

## ❄️ Cold Ideas (Score <5)
...

## By Type
- 🔬 Patents: 3
- 🚀 Startups: 8
- 💼 Business: 5
- 🛠️ Projects: 12
- 💭 Other: 4
```

### Single Idea View (expand [idea])

```markdown
# 🚀 AI-powered resume optimizer

**Score**: 8.2/10 (Hot)
**Status**: exploring

## The Idea
An AI tool that analyzes job descriptions and automatically 
tailors resumes for maximum ATS compatibility...

## Expansion
[Full AI-generated expansion]

## Scores
- Feasibility: 8/10 - Tech exists, APIs available
- Impact: 9/10 - Huge pain point for job seekers
- Effort: 6/10 - 2-3 months MVP
...
```

## ⚡ Quick Start

1. Open "💡 Ideas Inbox" Apple Note
2. Jot ideas with optional type prefix:
   - `🚀 App that tracks coffee consumption`
   - `🔬 Novel battery cooling mechanism`
   - `Just a random thought` (auto-classified)
3. Tell Claude: `"process ideas"`
4. View with: `"show ideas"` or `"show startup ideas"`

## 💡 Tips

- **Capture fast**: Don't overthink, just dump ideas
- **Process weekly**: Batch process for efficiency
- **Review monthly**: Revisit cold ideas - timing changes
- **Link related**: Connect ideas that could combine

---

**Version**: 1.0.0
**Last Updated**: 2025-11-24
