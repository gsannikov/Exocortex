# STAR Library Management Reference

**Document:** star-library-management.md  
**Version:** 1.0  
**Purpose:** Detailed reference for STAR story library management, search, filtering, and bulk operations  
**Parent Module:** star-framework.md

---

## 📚 Overview

This reference document provides comprehensive implementation details for managing a STAR story library, including:

1. **Library Dashboard** - Overview and statistics
2. **Story Catalog** - Detailed listing with quality breakdowns
3. **Search & Filter** - Finding stories by multiple criteria
4. **Statistics Dashboard** - Analytics and progress tracking
5. **Bulk Operations** - Managing multiple stories efficiently
6. **Index Management** - Library index structure and operations

---

## 🏠 Library Dashboard (Main View)

**Trigger Commands:**
- "Show my STAR library"
- "Review my stories"
- "Library dashboard"

**Display Format:**
```
📚 STAR Story Library Dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 LIBRARY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Progress:**
- Total Stories: [N] / Target: 50
- Interview-Ready (90+): [N] ([X]%)
- Average Quality Score: [X.X]/100
- Last Updated: [X] days ago

**Quality Distribution:**
⭐⭐⭐ Excellent (90-100): [N] stories ([X]%)
⭐⭐ Good (75-89): [N] stories ([X]%)
⭐ Fair (60-74): [N] stories ([X]%)
❌ Incomplete (<60): [N] stories ([X]%)

**Competency Coverage:**
✅ Leadership: [N] stories (Strong)
✅ Technical: [N] stories (Strong)
⚠️ Problem-solving: [N] stories (Need 2 more)
⚠️ Collaboration: [N] stories (Need 3 more)
⚠️ Innovation: [N] stories (Need 4 more)
❌ Conflict Resolution: 0 stories (Missing!)

**Recent Activity:**
- Stories created this week: [N]
- Stories improved this week: [N]
- Stories used in interviews: [N]

**Quick Actions:**
1. 📋 View all stories (catalog view)
2. 🔍 Search & filter stories
3. 📊 Detailed statistics
4. ⚡ Improve low-scoring stories
5. 📤 Export library
6. 🎯 Find gaps in coverage
```

---

## 📋 Story Catalog View

**Trigger Commands:**
- "Show all stories"
- "List my stories"
- "View story catalog"

**Display Format:**
```
📋 Story Catalog ([N] total stories)

**Filters Active:** [None] | [Quality: Excellent] | [Competency: Leadership]
**Sort:** [By Date ↓] | [By Score] | [By Usage] | [Alphabetical]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐⭐⭐ EXCELLENT (90-100) - [N] Stories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **[Story Title]** | 94/100 ⭐⭐⭐
   - ID: [story-id]
   - Competencies: Leadership, Conflict Resolution, Decision-Making
   - Created: Oct 25, 2025 | Updated: Oct 28, 2025
   - Used: 3 times (last: Wix interview, Oct 20)
   - 📝 [View] | ✏️ [Edit] | 🔄 [Refine] | 🎭 [Practice]

2. **[Story Title]** | 92/100 ⭐⭐⭐
   - ID: [story-id]
   - Competencies: Technical Leadership, System Architecture
   - Created: Oct 22, 2025 | Updated: Oct 22, 2025
   - Used: 2 times (last: Meta interview, Oct 15)
   - 📝 [View] | ✏️ [Edit] | 🔄 [Refine] | 🎭 [Practice]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐⭐ GOOD (75-89) - [N] Stories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. **[Story Title]** | 87/100 ⭐⭐
   - ID: [story-id]
   - Competencies: Problem-Solving, Crisis Management
   - Created: Oct 18, 2025 | Not yet improved
   - Used: 1 time (last: Google interview, Oct 10)
   - 📝 [View] | ✏️ [Edit] | 🔄 [Refine] (+8 pts potential!) | 🎭 [Practice]

[Continue for all stories...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**View Options:**
- Show only [Excellent/Good/Fair/Incomplete]
- Filter by competency: [Choose]
- Filter by date range: [Choose]
- Show unused stories only
- Show recently used

**Bulk Actions:**
- Export all stories (Markdown/PDF/JSON)
- Export selected quality tier
- Batch improve (focus on Good → Excellent)
- Organize by folder/competency

Choose an action or story number to work with.
```

**Pagination:**
- Show 10-20 stories per view
- Offer "Show more" if >20 stories
- Group by quality tier for better organization

---

## 🔍 Search & Filter System

### Search Command Formats

```
"Search stories about [keyword/competency]"
"Find stories with [criteria]"
"Show me [filtered set]"
"Filter by [attribute]"
```

### Search Types

#### 1. Keyword Search
Search across: Title, competencies, tags, story content

**Examples:**
```
"Search stories about API"
→ Find all stories mentioning APIs in title/content/tags

"Find conflict resolution stories"
→ Match competency

"Search migration"
→ Match keyword in content
```

**Implementation:**
```python
# Search algorithm
1. Load index.yaml
2. For keyword search:
   - Check title (exact & partial match)
   - Check competencies (exact match)
   - Check tags (exact match)
   - If needed: Load full stories and check content
3. Return matched story IDs with relevance score
4. Load full stories for top matches
```

#### 2. Competency Filter
Filter by specific competency or multiple competencies

**Examples:**
```
"Show leadership stories"
→ Filter where competency includes "leadership"

"Filter by technical competency"
→ Filter where competency includes "technical"

"Show all problem-solving stories"
→ Filter where competency includes "problem-solving"
```

**Competency Categories:**
- Leadership
- Technical/Technical Leadership
- Problem-Solving
- Collaboration/Cross-functional
- Innovation
- Conflict Resolution
- Decision-Making
- Crisis Management
- Communication
- Mentorship/Coaching
- Customer Focus
- Strategic Thinking

#### 3. Quality Filter
Filter by score range or rating tier

**Examples:**
```
"Show excellent stories only"
→ Filter where score >= 90

"Find stories that need improvement"
→ Filter where score < 75

"Show interview-ready stories"
→ Filter where score >= 90 AND status = "interview-ready"
```

**Quality Tiers:**
- Excellent: 90-100 ⭐⭐⭐
- Good: 75-89 ⭐⭐
- Fair: 60-74 ⭐
- Incomplete: <60 ❌

#### 4. Date Filter
Filter by creation or update date

**Examples:**
```
"Show stories created this month"
→ Filter where created >= first_day_of_month

"Find recently updated stories"
→ Filter where last_updated >= 7_days_ago

"Show oldest stories"
→ Sort by created ascending
```

#### 5. Usage Filter
Filter by interview usage history

**Examples:**
```
"Show unused stories"
→ Filter where times_used = 0

"Find most-used stories"
→ Sort by times_used descending

"Show stories used at Google"
→ Filter where last_used_company = "Google"
```

#### 6. Combined Filters
Stack multiple filters for precise results

**Examples:**
```
"Show excellent leadership stories created this month"
→ Filter:
   - quality_score >= 90
   - "leadership" in competencies
   - created >= first_day_of_month

"Find technical stories that need improvement"
→ Filter:
   - "technical" in competencies
   - 60 <= quality_score < 75

"Show unused stories with score > 85"
→ Filter:
   - times_used = 0
   - quality_score > 85
```

### Search Result Display

```
🔍 Search Results: "[search query]"

Found [N] matching stories:

1. **[Story Title]** | 94/100 ⭐⭐⭐
   - Matches: [Keyword in title/content]
   - Competencies: [list]
   - Relevance: High
   - 📝 [View Full Story]

2. **[Story Title]** | 87/100 ⭐⭐
   - Matches: [Competency match]
   - Competencies: [list]
   - Relevance: Medium
   - 📝 [View Full Story]

[...]

**Refine search:**
- Add filters
- Sort by [Score/Date/Relevance]
- Clear filters
```

---

## 📊 Detailed Statistics Dashboard

**Trigger Commands:**
- "Show library statistics"
- "Library analytics"
- "Story analytics"

**Display Format:**
```
📊 STAR Library Analytics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 QUALITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Quality:**
- Average Score: [X.X]/100
- Median Score: [X]/100
- Highest Score: [X]/100 ([Story Title])
- Lowest Score: [X]/100 ([Story Title])

**Quality Distribution:**
[Visual bar chart using characters]
⭐⭐⭐ Excellent (90-100): ████████░░ [N] stories (X%)
⭐⭐ Good (75-89):       ██████████ [N] stories (X%)
⭐ Fair (60-74):        ████░░░░░░ [N] stories (X%)
❌ Incomplete (<60):    ██░░░░░░░░ [N] stories (X%)

**Section Scores (Average):**
- Situation: [X.X]/20 ([X]%)
- Task: [X.X]/15 ([X]%)
- Action: [X.X]/35 ([X]%) ← Strongest
- Result: [X.X]/25 ([X]%) ← Needs work
- Overall: [X.X]/5 ([X]%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 COMPETENCY COVERAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Coverage by Competency:**
✅ Leadership:         [N] stories | Avg: [X.X]/100 | Status: Strong
✅ Technical:          [N] stories | Avg: [X.X]/100 | Status: Strong  
✅ Problem-Solving:    [N] stories | Avg: [X.X]/100 | Status: Good
⚠️ Collaboration:      [N] stories | Avg: [X.X]/100 | Status: Need 2 more
⚠️ Innovation:         [N] stories | Avg: [X.X]/100 | Status: Need 3 more
❌ Conflict Resolution: 0 stories | Avg: N/A | Status: Missing!
❌ Customer Focus:      0 stories | Avg: N/A | Status: Missing!

**Target Competencies for Next Stories:**
1. 🎯 Conflict Resolution (0 → Target: 3)
2. 🎯 Customer Focus (0 → Target: 2)
3. 🎯 Innovation (2 → Target: 5)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 TIMELINE & ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Creation Timeline:**
- First story: [Date]
- Most recent: [Date]
- Stories created this week: [N]
- Stories created this month: [N]
- Average creation rate: [X] stories/week

**Improvement Activity:**
- Stories improved this week: [N]
- Stories improved this month: [N]
- Average improvement gain: +[X] points
- Biggest improvement: [Story] (+[X] points)

**Interview Usage:**
- Total interviews prepared: [N]
- Stories used in interviews: [N] ([X]% of library)
- Most-used story: [Title] ([N] times)
- Unused stories: [N] ([X]% of library)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 PROGRESS TO GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Story Library Goal: 50 stories**
[Progress bar] ████████░░░░░░░░░░░░ [N]/50 (X%)
- Stories remaining: [50-N]
- At current rate: ~[X] weeks to goal

**Interview-Ready Goal: 80% at 90+**
[Progress bar] ██████░░░░░░░░░░░░░░ [N]/[Target] (X%)
- Need [X] more excellent stories
- [N] good stories can be improved

**Competency Coverage Goal: 5+ per competency**
[Progress bar] ████████░░░░░░░░░░░░ [N]/[Target] (X%)
- Missing competencies: [N]
- Underrepresented: [N]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Suggested Next Actions:**
1. 🎯 Build [N] stories for missing competencies
2. ⚡ Improve [N] good stories to excellent (+[X] points total)
3. 🔄 Update [N] old stories (>3 months since update)
4. 🎭 Practice [N] unused stories

**Quick Wins:**
- [Story Title] is at 88/100 - quick polish to 90+ (+2 pts)
- [Story Title] is at 89/100 - add metrics (+1 pt to 90)
- [N] stories need only minor improvements

What would you like to focus on?
```

### Statistics Calculations

#### Quality Metrics
```python
# Average quality score
average_score = sum(story.quality_score for story in stories) / len(stories)

# Quality distribution
excellent_count = len([s for s in stories if s.quality_score >= 90])
good_count = len([s for s in stories if 75 <= s.quality_score < 90])
fair_count = len([s for s in stories if 60 <= s.quality_score < 75])
incomplete_count = len([s for s in stories if s.quality_score < 60])

# Section averages
avg_situation = sum(s.situation_score for s in stories) / len(stories)
avg_task = sum(s.task_score for s in stories) / len(stories)
avg_action = sum(s.action_score for s in stories) / len(stories)
avg_result = sum(s.result_score for s in stories) / len(stories)
```

#### Competency Coverage
```python
# Count stories per competency
competency_counts = {}
for story in stories:
    for competency in story.competencies:
        competency_counts[competency] = competency_counts.get(competency, 0) + 1

# Determine status
for competency, count in competency_counts.items():
    if count >= 5:
        status = "Strong"
    elif count >= 3:
        status = "Good"
    elif count >= 1:
        status = f"Need {5-count} more"
    else:
        status = "Missing!"
```

#### Activity Metrics
```python
# Stories created this week
week_ago = now - timedelta(days=7)
created_this_week = len([s for s in stories if s.created >= week_ago])

# Stories improved this week
improved_this_week = len([s for s in stories if s.last_updated >= week_ago and s.created < week_ago])

# Average improvement
improvements = [s.quality_score - s.initial_score for s in stories if hasattr(s, 'initial_score')]
avg_improvement = sum(improvements) / len(improvements) if improvements else 0
```

---

## ⚙️ Bulk Operations

### 1. Batch Export

**Command:** `"Export [all/selected] stories"`

#### Export Options

##### A. Markdown Export
```
**Export Format: Markdown**

Creating single markdown file with all stories...

**Configuration:**
- Include: [N] stories
- Organized by: [Competency/Quality/Date]
- Include scores: Yes
- Include metadata: Yes

Exporting...
✅ Exported to: /Users/.../star-stories/exports/my-star-library-2025-10-30.md

File size: [X] KB
Open file? [Yes] [No]
```

**Markdown Structure:**
```markdown
# My STAR Story Library
*Exported: 2025-10-30*
*Total Stories: 23*

## Table of Contents
1. Leadership Stories (8)
2. Technical Stories (7)
3. Problem-Solving Stories (6)
...

## Leadership Stories

### Story 1: Resolving Architecture Disagreement
**Quality: 94/100 ⭐⭐⭐**
**Competencies:** Leadership, Conflict Resolution, Decision-Making
**Created:** Oct 25, 2025

#### Situation
[Full situation text...]

#### Task
[Full task text...]

#### Action
[Full action text...]

#### Result
[Full result text...]

---

### Story 2: Leading Team Through Change
...

```

##### B. PDF Export
```
**Export Format: PDF**

Creating formatted PDF document...

**Configuration:**
- Include: [N] stories
- Layout: Professional
- Table of contents: Yes
- Page breaks: Between stories
- Include quality indicators: Yes

Generating PDF...
✅ Exported to: /Users/.../star-stories/exports/my-star-library-2025-10-30.pdf

Pages: [X]
File size: [X] MB
Open file? [Yes] [No]
```

##### C. JSON Export
```
**Export Format: JSON**

Creating machine-readable JSON file...

**Configuration:**
- Include: [N] stories
- Include all metadata: Yes
- Pretty-printed: Yes
- Backup-ready: Yes

Exporting...
✅ Exported to: /Users/.../star-stories/exports/my-star-library-2025-10-30.json

File size: [X] KB
```

**JSON Structure:**
```json
{
  "export_metadata": {
    "export_date": "2025-10-30T15:45:00Z",
    "total_stories": 23,
    "format_version": "1.0"
  },
  "stories": [
    {
      "story_id": "leadership-conflict-resolution-001",
      "title": "Resolving Architecture Disagreement",
      "created": "2025-10-25T10:30:00Z",
      "quality_score": 94,
      "competencies": ["leadership", "conflict-resolution"],
      "situation": "...",
      "task": "...",
      "action": "...",
      "result": "..."
    }
  ]
}
```

##### D. Quick Reference Cards
```
**Export Format: Quick Reference Cards**

Creating printable flashcards...

**Configuration:**
- Format: One page per story
- Layout: 3x5 card style
- Include: Key points only
- Ready for: Printing/Practice

Generating...
✅ Exported to: /Users/.../star-stories/exports/flashcards-2025-10-30.pdf

Cards: [N]
Print settings: 3x5 index cards, landscape
Open file? [Yes] [No]
```

---

### 2. Batch Improvement

**Command:** `"Improve all good stories"` or `"Batch improve"`

```
🔄 Batch Improvement Mode

I found [N] stories that could reach Excellent (90+) with minor improvements:

1. **[Story Title]** - 87/100
   - Quick fix: Add decision rationale (+3 pts)
   - Est. time: 5 min
   - New score: 90/100 ⭐⭐⭐

2. **[Story Title]** - 88/100  
   - Quick fix: Add quantifiable metric (+2 pts)
   - Est. time: 3 min
   - New score: 90/100 ⭐⭐⭐

3. **[Story Title]** - 89/100
   - Quick fix: Add organizational context (+1 pt)
   - Est. time: 2 min
   - New score: 90/100 ⭐⭐⭐

**Total estimated time:** 10 minutes for all 3
**Impact:** +3 interview-ready stories!

Would you like to:
1. Improve all 3 stories now (interactive)
2. Show me the fixes (I'll apply myself)
3. Pick specific stories to improve
4. Export improvement checklist
```

**Interactive Mode:**
```
Starting batch improvement...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Story 1 of 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Story Title]** - Current: 87/100

**Missing:** Decision rationale in Action section
**Current Action section has:**
- Created decision matrix
- Facilitated workshop
- Got consensus in 2 days

**Question:** Why did you choose the workshop approach over alternatives like 1-on-1s or management decision?

[User responds...]

Great! Adding this to your story...
✅ Story improved: 87 → 90 (+3 points!)

Continue to story 2? [Yes] [Skip] [Stop]
```

---

### 3. Organize by Category

**Command:** `"Organize stories by [competency/role/company]"`

```
**Organization Options:**

1. **By Competency**
   - Create competency-based views
   - Stories can appear in multiple categories
   - Maintains single source of truth

2. **By Role Type**
   - Engineering Manager stories
   - Technical Lead stories
   - Senior IC stories
   - General/Applicable to all

3. **By Company Size**
   - Startup (0-50)
   - Small (50-200)  
   - Medium (200-1000)
   - Large (1000+)

4. **By Interview Company**
   - Used at Google
   - Used at Meta
   - Used at Amazon
   - Never used

Choose organization scheme: [1-4]
```

**After Organization:**
```
Organizing [N] stories by [Competency]...

✅ Organization complete!

**New Structure:**
📁 Leadership (8 stories)
  - Conflict Resolution (2)
  - Team Management (3)
  - Change Management (3)

📁 Technical (7 stories)
  - System Design (3)
  - Problem-Solving (2)
  - Architecture (2)

📁 Collaboration (4 stories)
  - Cross-functional (2)
  - Stakeholder Management (2)

Would you like to:
- View organized catalog
- Export by category
- Return to main library
```

---

### 4. Batch Quality Check

**Command:** `"Check all stories for quality"` or `"Validate library"`

```
**Running quality check on [N] stories...**

Progress: ████████████████████ 100%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUALITY AUDIT RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Summary:**
✅ Interview-Ready: [N] stories (90-100)
⚠️ Minor Issues: [N] stories (75-89)
⚡ Major Issues: [N] stories (60-74)
❌ Critical Issues: [N] stories (<60)

**Common Issues Found:**
1. Missing quantifiable results: [N] stories
2. Weak action section: [N] stories  
3. Missing organizational context: [N] stories
4. Unclear personal role: [N] stories

**Stories Needing Attention:**

⚡ Priority 1 - Critical Issues:
- [Story Title] (55/100) - Incomplete result section
- [Story Title] (58/100) - Actions too vague

⚠️ Priority 2 - Quick Improvements:
- [Story Title] (87/100) - Add 1 metric (+3 pts)
- [Story Title] (88/100) - Clarify role (+2 pts)  
- [Story Title] (89/100) - Add context (+1 pt)

**Recommended Actions:**
1. Fix [N] critical stories (30-45 min)
2. Improve [N] stories to excellent (15 min)
3. Re-audit in 1 week

Would you like to start with Priority 1?
```

---

### 5. Update Old Stories

**Command:** `"Update old stories"` or `"Refresh library"`

```
**Stories Last Updated >3 Months Ago:**

I found [N] stories that might need updating:

1. **[Story Title]** - Last updated: 6 months ago
   - Score: 85/100
   - Suggestion: Add recent learnings/updates
   - Verify metrics are still accurate

2. **[Story Title]** - Last updated: 4 months ago
   - Score: 78/100
   - Suggestion: Re-score with current rubric
   - May need quantification improvements

**Batch Update Options:**
1. Re-score all old stories with current rubric
2. Review and refresh each story  
3. Mark as "reviewed - no changes needed"
4. Archive outdated stories

Choose an option or select specific stories.
```

---

## 📇 Library Index Structure

**File:** `user-data/interview-prep/star-stories/index.yaml`

### Index Schema

```yaml
---
# STAR Story Library Index
# Auto-updated when stories are created/modified

library_metadata:
  total_stories: 23
  last_updated: "2025-10-30T15:45:00Z"
  average_quality_score: 84.2
  interview_ready_count: 15  # 90+ score
  version: "1.0"

stories:
  - story_id: "leadership-conflict-resolution-001"
    title: "Resolving Architecture Disagreement"
    file: "leadership-conflict-resolution-001.yaml"
    created: "2025-10-25T10:30:00Z"
    last_updated: "2025-10-28T14:20:00Z"
    quality_score: 94
    situation_score: 19
    task_score: 14
    action_score: 33
    result_score: 23
    overall_score: 5
    rating: "excellent"
    competencies:
      - leadership
      - conflict-resolution  
      - decision-making
    tags:
      - architecture
      - team-dynamics
      - technical-decision
    question_types:
      - behavioral
      - leadership
    roles_applicable:
      - Engineering Manager
      - Technical Lead
      - Staff Engineer
    company_sizes:
      - medium
      - large
    impact_level: "high"
    status: "interview-ready"
    times_used: 3
    last_used_date: "2025-10-20"
    last_used_company: "Wix"
    last_used_role: "Engineering Manager"
    interview_outcomes:
      - company: "Wix"
        role: "Engineering Manager"
        outcome: "offer"
        date: "2025-10-20"
    
  # ... more stories

competency_coverage:
  leadership: 8
  technical: 7
  problem_solving: 6
  collaboration: 4
  innovation: 3
  conflict_resolution: 2
  customer_focus: 1
  decision_making: 5
  crisis_management: 3
  communication: 6
  mentorship: 2

quality_distribution:
  excellent: 15  # 90-100
  good: 6        # 75-89
  fair: 2        # 60-74
  incomplete: 0  # <60

section_scores_average:
  situation: 17.8
  task: 13.5
  action: 29.2
  result: 21.7
  overall: 4.8

recent_activity:
  stories_created_this_week: 2
  stories_improved_this_week: 3
  stories_used_this_week: 1
  last_interview_prep: "2025-10-20"
  last_interview_company: "Wix"

milestones:
  next_milestone: "30_stories"
  stories_to_milestone: 7
  target_date: "2025-11-15"
  on_track: true

tags:
  - architecture: 5
  - api: 3
  - migration: 2
  - team-dynamics: 7
  - production-issue: 4
  - [...]
```

### Index Operations

#### Reading Index
```python
# Always start with index for library operations
index = Filesystem:read_file("/Users/.../star-stories/index.yaml")
parsed_index = yaml.load(index)

# Use index for:
# - Quick statistics
# - Filtering stories
# - Finding story files
# - Tracking progress
```

#### Updating Index
```python
# After creating/modifying stories
# 1. Load current index
# 2. Update relevant fields
# 3. Recalculate statistics
# 4. Write updated index

# Update after story creation
parsed_index['library_metadata']['total_stories'] += 1
parsed_index['stories'].append(new_story_metadata)

# Update after story improvement
story_entry = find_story_in_index(story_id)
story_entry['quality_score'] = new_score
story_entry['last_updated'] = timestamp

# Recalculate statistics
recalculate_averages(parsed_index)
recalculate_competency_coverage(parsed_index)
recalculate_quality_distribution(parsed_index)

# Write back
Filesystem:write_file(path="index.yaml", content=yaml.dump(parsed_index))
```

#### Search Using Index
```python
# Fast filtering without loading all stories

# Filter by competency
leadership_stories = [
    s for s in parsed_index['stories'] 
    if 'leadership' in s['competencies']
]

# Filter by quality
excellent_stories = [
    s for s in parsed_index['stories']
    if s['quality_score'] >= 90
]

# Filter by date
recent_stories = [
    s for s in parsed_index['stories']
    if parse_date(s['created']) >= month_ago
]

# Combined filters
filtered = [
    s for s in parsed_index['stories']
    if 'leadership' in s['competencies']
    and s['quality_score'] >= 90
    and s['times_used'] == 0
]

# Load only filtered stories
for story_meta in filtered:
    story = load_story(story_meta['file'])
    # Work with story...
```

---

## 🎯 Implementation Guidelines

### Performance Best Practices

1. **Always use index first**
   - Index contains summary data
   - Faster than loading all story files
   - Use for filtering before loading

2. **Lazy load full stories**
   - Only load when needed for display/editing
   - Load in batches for bulk operations
   - Cache during session

3. **Update index incrementally**
   - Update immediately after story changes
   - Don't wait until next library view
   - Keeps index always accurate

4. **Batch operations efficiently**
   - Load multiple stories at once
   - Process in memory
   - Write back in single transaction

### File Operation Patterns

#### Reading Library Overview
```python
# GOOD: Use index
index = read_index()
display_statistics(index)

# BAD: Load all stories
all_stories = load_all_stories()  # Slow!
calculate_statistics(all_stories)
```

#### Searching Stories
```python
# GOOD: Filter index first
matches = filter_index_by_competency(index, "leadership")
stories = load_stories(matches)  # Load only 8 stories

# BAD: Load all then filter
all_stories = load_all_stories()  # Load all 23 stories
leadership = [s for s in all_stories if "leadership" in s.competencies]
```

#### Updating Statistics
```python
# GOOD: Incremental update
update_index_for_story(story_id, new_score)
recalculate_affected_stats(index)

# BAD: Rebuild everything
all_stories = load_all_stories()
rebuild_entire_index()
```

### Error Handling

1. **Index corruption**
   - Validate index structure on load
   - Rebuild from stories if corrupted
   - Backup index before major changes

2. **Missing stories**
   - Handle missing file gracefully
   - Offer to remove from index
   - Log inconsistencies

3. **Concurrent updates**
   - Lock index during updates
   - Reload before writing
   - Merge conflicts if needed

---

## 📚 Usage Examples

### Example 1: User wants library overview
```
User: "Show my STAR library"

Claude:
1. Read index.yaml
2. Display dashboard with statistics from index
3. No need to load individual story files
```

### Example 2: User searches for leadership stories
```
User: "Find my leadership stories"

Claude:
1. Read index.yaml
2. Filter stories where 'leadership' in competencies
3. Load only matching story files (e.g., 8 stories)
4. Display filtered catalog
```

### Example 3: User wants detailed analytics
```
User: "Show library statistics"

Claude:
1. Read index.yaml
2. Calculate additional metrics from index data
3. Display comprehensive statistics dashboard
4. No need to load story files (all data in index)
```

### Example 4: User improves a story
```
User: "Improve the API bug story"

Claude:
1. Load specific story file
2. Run refinement workflow
3. Save updated story
4. Update index.yaml with new score
5. Recalculate relevant statistics in index
```

### Example 5: User wants to export
```
User: "Export all my stories to PDF"

Claude:
1. Read index.yaml for story list
2. Load all story files
3. Generate PDF with all stories
4. Save to exports folder
5. No index update needed
```

---

## 🔧 Maintenance Operations

### Weekly Maintenance
```python
# Auto-run or prompt user weekly
def weekly_maintenance(index):
    # Check for old stories needing update
    old_stories = find_stories_older_than(index, months=3)
    
    # Check for unused stories
    unused = find_stories_with_usage(index, times=0)
    
    # Validate index consistency
    validate_index_against_files(index)
    
    # Generate weekly report
    return {
        'old_stories': old_stories,
        'unused_stories': unused,
        'inconsistencies': inconsistencies,
        'recommendations': generate_recommendations(index)
    }
```

### Index Rebuild
```python
# When index corrupted or major changes
def rebuild_index():
    # Scan story directory
    story_files = scan_directory("star-stories/")
    
    # Load and process each story
    stories = []
    for file in story_files:
        story = load_story(file)
        stories.append(extract_metadata(story))
    
    # Calculate statistics
    stats = calculate_all_statistics(stories)
    
    # Build new index
    new_index = {
        'library_metadata': stats,
        'stories': stories,
        # ...
    }
    
    # Write index
    write_index(new_index)
    
    return new_index
```

---

## ✅ Quality Checklist

### For Index Management
- [ ] Index updated after every story change
- [ ] Statistics recalculated correctly
- [ ] Competency coverage accurate
- [ ] Quality distribution accurate
- [ ] Usage tracking working
- [ ] Timestamps in ISO format

### For Search & Filter
- [ ] Keyword search works across title/tags
- [ ] Competency filter accurate
- [ ] Quality filter uses correct thresholds
- [ ] Date filter handles timezones
- [ ] Combined filters work correctly
- [ ] Results sorted by relevance

### For Statistics
- [ ] All averages calculated correctly
- [ ] Distribution percentages add to 100%
- [ ] Progress bars accurate
- [ ] Milestones tracked correctly
- [ ] Recommendations relevant
- [ ] Charts/bars display properly

### For Bulk Operations
- [ ] Export includes all selected stories
- [ ] Export formatting professional
- [ ] Batch improvement preserves data
- [ ] Organization maintains links
- [ ] Quality check comprehensive
- [ ] Old story detection accurate

---

**Version:** 1.0  
**Last Updated:** 2025-10-30  
**Status:** ✅ Complete  
**Parent:** star-framework.md
