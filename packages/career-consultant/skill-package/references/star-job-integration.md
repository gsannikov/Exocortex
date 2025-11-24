# STAR Job Integration System
**Reference:** star-job-integration.md  
**Version:** 1.0  
**Purpose:** Match STAR stories to job requirements and generate interview prep packages  
**Phase:** 4 of 6

---

## Overview

This system analyzes job postings to extract competencies, matches them against the user's STAR story library, and generates comprehensive interview preparation packages. It bridges the gap between offline story building and interview-specific preparation.

---

## 📋 Core Components

### 1. Competency Extraction Engine
### 2. Story Matching Algorithm  
### 3. Prep Package Generator
### 4. Gap Analysis System

---

## 1️⃣ Competency Extraction Engine

### Purpose
Parse job descriptions to identify required competencies, skills, and behavioral expectations.

### Competency Categories

**Leadership (L)**
- Team management
- Conflict resolution
- Change management
- Decision-making
- Vision & strategy
- Performance management
- Delegation
- Motivation

**Technical (T)**
- System design & architecture
- Problem-solving & debugging
- Performance optimization
- Code quality & review
- Technical debt management
- Tool/technology expertise
- Best practices & standards

**Collaboration (C)**
- Cross-functional teamwork
- Stakeholder management
- Influence without authority
- Communication (written/verbal)
- Mentorship & coaching
- Knowledge sharing
- Relationship building

**Innovation (I)**
- Process improvement
- New initiatives
- Creative problem-solving
- Risk-taking & experimentation
- Product thinking
- Customer focus

**Delivery (D)**
- Project planning & execution
- Priority management
- Meeting deadlines
- Resource allocation
- Risk management
- Quality assurance

**Domain Expertise (X)**
- Industry knowledge
- Domain-specific skills
- Regulatory/compliance
- Market understanding

### Extraction Algorithm

**Input:** Job description text or job analysis results

**Process:**
```python
# Pseudo-code for competency extraction

def extract_competencies(job_text, job_analysis=None):
    """
    Extract competencies from job description
    
    Returns: List of competencies with priority levels
    """
    competencies = []
    
    # Step 1: Use job analysis results if available
    if job_analysis and 'key_responsibilities' in job_analysis:
        competencies.extend(extract_from_responsibilities(job_analysis))
    
    # Step 2: Keyword matching
    keywords = {
        'leadership': ['lead', 'manage', 'mentor', 'coach', 'team'],
        'technical': ['design', 'architect', 'build', 'optimize', 'debug'],
        'collaboration': ['cross-functional', 'stakeholder', 'communicate'],
        'innovation': ['innovate', 'improve', 'create', 'initiative'],
        'delivery': ['deliver', 'execute', 'ship', 'launch', 'deadline']
    }
    
    for category, words in keywords.items():
        matches = count_keyword_matches(job_text, words)
        if matches > 0:
            competencies.append({
                'category': category,
                'strength': calculate_strength(matches),
                'priority': determine_priority(matches, context)
            })
    
    # Step 3: Phrase pattern matching
    patterns = {
        'conflict_resolution': ['resolve conflict', 'difficult conversation', 'disagreement'],
        'system_design': ['design system', 'architecture', 'scalable'],
        'mentorship': ['mentor', 'coach', 'develop team members'],
        # ... more patterns
    }
    
    # Step 4: Seniority-based inference
    if is_senior_role(job_text):
        add_senior_competencies(competencies)
    
    # Step 5: Industry-based inference
    industry = detect_industry(job_text)
    add_industry_competencies(competencies, industry)
    
    # Step 6: Priority ranking
    competencies = rank_by_priority(competencies)
    
    return competencies
```

**Output Format:**
```yaml
competencies:
  - id: "leadership-team-management"
    category: "leadership"
    name: "Team Management"
    priority: "critical"  # critical, high, medium, low
    confidence: 0.92
    evidence:
      - "lead team of 8-12 engineers"
      - "manage performance and growth"
      - "build high-performing teams"
    
  - id: "technical-system-design"
    category: "technical"
    name: "System Design & Architecture"
    priority: "critical"
    confidence: 0.88
    evidence:
      - "design scalable systems"
      - "architecture decisions"
      - "technical strategy"
    
  # ... 10-20 total competencies
```

### Priority Classification

**Critical** (Must-have, 5-7 competencies)
- Mentioned 3+ times in job description
- In job title or top 3 requirements
- Explicitly labeled "required" or "must have"

**High** (Important, 5-8 competencies)
- Mentioned 2 times
- In "key responsibilities" section
- Aligned with role seniority

**Medium** (Nice-to-have, 3-5 competencies)
- Mentioned once
- In "preferred qualifications"
- Industry-standard for role

**Low** (Bonus, 0-3 competencies)
- Implicit requirements
- Inferred from role/industry
- Growth opportunities

---

## 2️⃣ Story Matching Algorithm

### Purpose
Match user's STAR stories against job competencies with relevance scoring.

### Matching Process

**Step 1: Load Story Library**
```python
def load_story_library(user_path):
    """Load user's STAR stories and index"""
    index_path = f"{user_path}/interview-prep/star-stories/index.yaml"
    index = read_yaml(index_path)
    
    stories = []
    for story_ref in index['stories']:
        story_path = f"{user_path}/interview-prep/star-stories/{story_ref['file']}"
        story = read_yaml(story_path)
        stories.append(story)
    
    return stories, index
```

**Step 2: Calculate Match Scores**
```python
def calculate_match_score(story, job_competencies, job_context):
    """
    Calculate how well a story matches job requirements
    
    Scoring breakdown:
    - Competency overlap: 40%
    - Role/seniority alignment: 20%
    - Industry/context relevance: 15%
    - Story quality score: 15%
    - Recency and completeness: 10%
    
    Returns: Score 0-100
    """
    
    # 1. Competency Overlap (40 points)
    competency_score = 0
    story_competencies = set(story['competencies'])
    job_competency_ids = set([c['id'] for c in job_competencies])
    
    overlap = story_competencies.intersection(job_competency_ids)
    overlap_ratio = len(overlap) / len(job_competency_ids)
    
    # Weight by priority
    priority_weight = 0
    for comp_id in overlap:
        job_comp = find_competency(job_competencies, comp_id)
        if job_comp['priority'] == 'critical':
            priority_weight += 4
        elif job_comp['priority'] == 'high':
            priority_weight += 2
        elif job_comp['priority'] == 'medium':
            priority_weight += 1
    
    competency_score = min(40, (overlap_ratio * 20) + (priority_weight * 2))
    
    # 2. Role/Seniority Alignment (20 points)
    role_score = 0
    if job_context['role'] in story['roles_applicable']:
        role_score += 15
    
    seniority_match = compare_seniority(
        story['seniority_level'],
        job_context['seniority']
    )
    role_score += seniority_match * 5  # 0-5 points
    
    # 3. Industry/Context Relevance (15 points)
    context_score = 0
    
    if job_context['company_size'] in story.get('company_sizes', []):
        context_score += 5
    
    if job_context['industry'] in story.get('industries', []):
        context_score += 5
    
    # Similar technologies, methodologies
    tech_overlap = len(set(story.get('technologies', [])).intersection(
        set(job_context.get('technologies', []))
    ))
    context_score += min(5, tech_overlap)
    
    # 4. Story Quality Score (15 points)
    quality_score = (story['quality_score'] / 100) * 15
    
    # 5. Recency and Completeness (10 points)
    recency_score = calculate_recency_score(story['last_updated'])  # 0-5
    completeness_score = (story['completeness_score'] / 100) * 5  # 0-5
    
    # Total Score
    total_score = (
        competency_score +
        role_score +
        context_score +
        quality_score +
        recency_score +
        completeness_score
    )
    
    return {
        'total_score': round(total_score, 1),
        'breakdown': {
            'competency': round(competency_score, 1),
            'role_alignment': round(role_score, 1),
            'context': round(context_score, 1),
            'quality': round(quality_score, 1),
            'recency_completeness': round(recency_score + completeness_score, 1)
        },
        'matched_competencies': list(overlap),
        'missing_competencies': list(job_competency_ids - story_competencies)
    }
```

**Step 3: Rank and Select Stories**
```python
def select_top_stories(stories, job_competencies, job_context, num_stories=5):
    """
    Select best-matching stories for interview prep
    
    Returns: Top N stories with match scores
    """
    scored_stories = []
    
    for story in stories:
        match_score = calculate_match_score(story, job_competencies, job_context)
        scored_stories.append({
            'story': story,
            'match_score': match_score
        })
    
    # Sort by total score
    scored_stories.sort(key=lambda x: x['match_score']['total_score'], reverse=True)
    
    # Select top N, ensuring competency diversity
    selected = select_with_diversity(scored_stories, num_stories)
    
    return selected
```

### Match Score Interpretation

**90-100** - Perfect Match ⭐⭐⭐
- Directly addresses 3+ critical competencies
- Role and context perfectly aligned
- High quality story (90+/100)
- Ready to use as-is

**75-89** - Strong Match ⭐⭐
- Covers 2+ critical competencies
- Good role alignment
- Minor refinement suggested

**60-74** - Moderate Match ⭐
- Covers 1 critical or 2+ high competencies
- Some alignment
- Needs refinement before use

**<60** - Weak Match
- Limited competency overlap
- Poor alignment
- Consider building new story instead

---

## 3️⃣ Prep Package Generator

### Purpose
Create comprehensive interview preparation package with stories, talking points, and coverage report.

### Package Structure

```yaml
---
# Interview Prep Package
package_id: "wix-eng-manager-2025-10-30"
created: "2025-10-30T14:00:00Z"
company: "Wix"
role: "Engineering Manager"
interview_date: "2025-11-15"
status: "in_progress"  # in_progress, ready, completed
---

# Interview Preparation Package

## Job Overview
**Company:** Wix  
**Role:** Engineering Manager - Platform Team  
**Location:** Tel Aviv  
**Team Size:** 12-15 engineers  
**Seniority:** Senior/Staff level  
**Interview Date:** November 15, 2025

## Competency Requirements

### Critical (Must Demonstrate)
1. ✅ **Team Leadership** - Have 2 strong stories
2. ✅ **System Design** - Have 1 strong story
3. ⚠️ **Conflict Resolution** - Have 1 moderate story (needs refinement)
4. ❌ **Scaling Teams** - Missing (build new story)
5. ❌ **Technical Strategy** - Missing (build new story)

### High Priority
6. ✅ **Cross-functional Collaboration** - Have 1 story
7. ⚠️ **Performance Management** - Have 1 weak story (consider rebuild)
8. ❌ **Process Improvement** - Missing (build new story)

**Coverage:** 5/8 critical competencies (62.5%)  
**Recommendation:** Build 3 new stories + refine 2 existing
```

*(See full package example in YAML structure above)*

### Display Format - Quick View

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 INTERVIEW PREP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Company: Wix
Role: Engineering Manager
Interview Date: Nov 15, 2025

COMPETENCY COVERAGE:
Critical:  ████████░░ 80% (4/5)
High:      ██████░░░░ 60% (3/5)
Overall:   ██████░░░░ 62%

STATUS: ⚠️  Needs Work (Target: 85%+)

MATCHED STORIES FROM LIBRARY:
✅ Architecture Migration     [94% match] ⭐⭐⭐
✅ Conflict Resolution         [92% match] ⭐⭐⭐
✅ Team Culture Building       [86% match] ⭐⭐
✅ Product Launch              [81% match] ⭐⭐
✅ Mentorship Journey          [78% match] ⭐⭐

RECOMMENDED NEW STORIES:
🔴 Scaling Engineering Team    [Critical]  20 min
🔴 Technical Strategy          [Critical]  25 min
🟡 Process Improvement         [High]      15 min

Total prep time: ~3 hours
```

---

## 4️⃣ Gap Analysis System

### Purpose
Identify missing competencies and recommend stories to build.

### Gap Identification Process

1. Map all job competencies to matched stories
2. Identify competencies not covered
3. Prioritize gaps by job priority (critical > high > medium)
4. Generate specific story recommendations for each gap
5. Estimate time to build each story

### Story Recommendation Format

```yaml
gap:
  competency_id: "leadership-team-scaling"
  competency_name: "Scaling Engineering Teams"
  priority: "critical"
  impact: 9.5/10
  estimated_time: "20 minutes"
  
  prompts:
    - "Have you grown a team from X to Y people?"
    - "What challenges did you face during team growth?"
    - "How did you maintain velocity and quality while scaling?"
    - "What structures or processes did you establish?"
  
  example_questions:
    - "Tell me about a time you scaled a team"
    - "How do you approach building high-performing teams?"
    - "Describe your experience with hiring and team growth"
  
  tips:
    - "Focus on specific metrics (team size X→Y, time period)"
    - "Include both process and culture aspects"
    - "Mention hiring, onboarding, and retention"
    - "Discuss challenges overcome"
    - "Highlight business impact of scaling"
```

### Coverage Targets

**Minimum Viable Coverage (Ready for Interview):**
- Critical competencies: 80%+ (4 of 5)
- High priority: 60%+ (3 of 5)
- Overall: 70%+

**Interview-Ready Coverage (Confident):**
- Critical competencies: 100% (all covered)
- High priority: 80%+ (4 of 5)
- Overall: 85%+

**Exceptional Coverage (Highly Prepared):**
- All competencies: 90%+
- Multiple stories per critical competency
- Deep demonstration across all categories

---

## 5️⃣ Integration with Job Analysis

### Trigger Points

**Automatic:**
When user completes job analysis via main Career Guard system.

**Manual:**
User explicitly requests interview prep:
- "Prepare for [Company] interview"
- "Match my stories to this job"
- "Interview prep for this role"

### Workflow Integration

```
User runs job analysis
    ↓
Job Analysis Complete
    ↓
[Automatic] STAR module offers prep
    ↓
User accepts → Generate prep package
    ↓
Display matched stories + gaps
    ↓
User builds missing stories
    ↓
Practice mode
```

---

## 📊 Implementation Checklist

Phase 4 Implementation Tasks:

**Core Functions:**
- [ ] Competency extraction from job descriptions
- [ ] Story matching algorithm with scoring
- [ ] Prep package generation
- [ ] Gap analysis with recommendations
- [ ] Coverage calculation and display

**Integration:**
- [ ] Hook into job analysis completion
- [ ] Load story library and index
- [ ] Generate job context from analysis
- [ ] Offer interview prep automatically

**Display:**
- [ ] CLI-style summary view
- [ ] Detailed prep package format
- [ ] Coverage matrix visualization
- [ ] Story recommendations with prompts

**Testing:**
- [ ] Test with real job descriptions
- [ ] Validate scoring accuracy
- [ ] Check coverage calculations
- [ ] Verify gap identification

---

## 🎯 Success Criteria

Phase 4 is complete when:
- [ ] Job competencies extracted correctly
- [ ] Stories matched with accurate scores
- [ ] Gaps identified with priority ranking
- [ ] Prep packages generated with all sections
- [ ] Coverage displayed clearly
- [ ] Integration with job analysis works
- [ ] User can take action on recommendations

---

**Version:** 1.0  
**Status:** ✅ Reference Complete  
**Phase:** 4 of 6 (Job Integration)  
**Last Updated:** 2025-10-30
