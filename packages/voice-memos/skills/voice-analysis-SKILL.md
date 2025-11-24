# Voice Analysis Skill

**Version**: 1.0.0  
**Created**: 2025-11-03  
**Purpose**: Extract actionable insights, key points, and organize content from voice memo transcriptions

## Overview

This skill analyzes transcribed voice memos to extract action items, generate summaries, identify key entities, and organize content for easy reference and follow-up.

## When to Use This Skill

Use this skill when:
- User has a voice memo transcription
- User asks to "analyze this voice memo"
- User requests "find action items" or "summarize this"
- Automatically offered after transcription completes
- User wants to extract insights from spoken content

## Capabilities

### Core Analysis Features
- **Action Item Extraction**: Identify tasks, to-dos, and commitments with priorities
- **Multi-Level Summarization**: Brief, standard, or detailed summaries
- **Entity Recognition**: Extract people, dates, locations, organizations, projects
- **Key Points Identification**: Highlight most important insights (3-7 points)
- **Categorization**: Auto-assign categories (meeting, idea, task, journal, etc.)
- **Smart Tagging**: Generate relevant tags for organization

### Advanced Features
- **Question Detection**: Identify unanswered questions
- **Decision Tracking**: Note decisions made during conversation
- **Sentiment Analysis**: Detect overall tone and mood (optional)
- **Priority Scoring**: Rank action items by urgency
- **Related Content**: Link to similar past memos

## Configuration

Load settings from: `~/MyDrive/VoiceMemos/config/settings.json`

Key configuration:
```json
{
  "analysis": {
    "extract_action_items": true,
    "priority_scoring": true,
    "generate_summary": true,
    "summary_length": "standard",
    "identify_entities": true,
    "auto_categorize": true,
    "detect_questions": true,
    "detect_decisions": true
  }
}
```

## Workflow

### Step 1: Load Transcription
```
Receive transcription text
↓
Load configuration settings
↓
Read analysis prompt template
```

### Step 2: Extract Action Items
```
Scan for action item keywords
↓
Identify tasks and commitments
↓
Assign priorities (HIGH/MEDIUM/LOW)
↓
Extract due dates if mentioned
↓
Format as checkboxes
```

### Step 3: Generate Summary
```
Based on summary_length setting:
- Brief: 3 sentences (TL;DR)
- Standard: 5-10 sentences
- Detailed: 15-20 sentences

Include: Main points, context, conclusions
```

### Step 4: Extract Entities & Metadata
```
Identify:
- People mentioned
- Dates and times
- Locations
- Organizations
- Projects
- Key statistics or facts
```

### Step 5: Categorize & Tag
```
Assign 1-3 categories
↓
Generate 5-10 descriptive tags
↓
Detect sentiment/tone
↓
Identify questions and decisions
```

### Step 6: Organize Output
```
Compile all analysis results
↓
Format in structured markdown
↓
Save to processed/ directory
↓
Optionally sync to integrations
```

## Output Template

```markdown
# {Title} - Analysis

**Original**: `{transcript_filename}`
**Analyzed**: {YYYY-MM-DD HH:MM}
**Duration**: {MM:SS}

## Summary
{Generated summary based on configured level}

## Action Items

### HIGH Priority
- [ ] {action item with details} — Due: {date if mentioned}

### MEDIUM Priority
- [ ] {action item}

### LOW Priority
- [ ] {action item}

## Key Points
- {Important insight or decision point 1}
- {Important insight 2}
- {Important insight 3}
- {Continue for 5-7 total points}

## Entities & References

**People**: {names mentioned}
**Dates**: {specific dates, deadlines, appointments}
**Locations**: {places mentioned}
**Organizations**: {companies, departments, teams}
**Projects**: {project names or initiatives}

## Questions & Decisions

**Unanswered Questions**:
- {Question 1}
- {Question 2}

**Decisions Made**:
- {Decision 1}
- {Decision 2}

## Classification

**Categories**: {category1}, {category2}
**Tags**: #{tag1}, #{tag2}, #{tag3}, #{tag4}, #{tag5}
**Tone**: {Professional/Casual/Urgent/Reflective}
**Sentiment**: {Positive/Neutral/Negative/Mixed}

---
*Analysis complete. Ready for export or integration.*
```

## Action Item Detection

### Keywords That Trigger Extraction
```
Primary:
- "todo", "task", "need to", "have to", "must", "should"
- "remember to", "don't forget", "make sure"
- "follow up", "reach out", "contact"
- "schedule", "book", "reserve", "plan"
- "send", "email", "call", "message"

Contextual:
- "by [date]" → deadline indicator
- "urgent", "asap" → high priority
- "eventually", "someday" → low priority
```

### Priority Assignment Logic
```
HIGH Priority if contains:
- "urgent", "asap", "critical", "immediately", "today"
- Specific short deadline ("by tomorrow", "by EOD")

MEDIUM Priority if contains:
- "this week", "soon", "priority"
- Specific near deadline ("by Friday")

LOW Priority:
- "eventually", "someday", "maybe", "consider"
- No deadline specified
- Vague timing ("when I get a chance")
```

## Summary Generation

### Brief Summary (TL;DR)
```
Max 3 sentences, ~100 words
Focus on: Core message, main takeaway
Style: Concise, direct
Example: "Discussion of Q4 marketing strategy. Team agreed to focus 
on digital channels. Budget approved, launch planned for December."
```

### Standard Summary
```
5-10 sentences, ~250-300 words
Include: Main points, key decisions, action items overview, context
Style: Balanced detail
Example: "Team met to finalize Q4 marketing strategy with focus on 
digital transformation. Sarah presented data showing 40% better ROI 
from digital vs. traditional channels. Team agreed to reallocate 30% 
of budget from print to social media and content marketing. John 
raised concerns about timing... [continues]"
```

### Detailed Summary
```
15-20 sentences, ~500-800 words
Include: Comprehensive overview, nuance, examples, full context
Style: Thorough documentation
Use when: Important meetings, complex discussions, detailed planning
```

## Entity Recognition Patterns

### People Detection
```
Look for:
- Proper names (capitalized)
- Titles (Mr., Dr., CEO)
- Role references ("the designer", "our lawyer")
- Possessive forms ("Sarah's report")
```

### Date/Time Extraction
```
Formats:
- Absolute: "November 15th", "Friday", "next week"
- Relative: "tomorrow", "in two days", "by end of month"
- Time: "3pm", "10:30", "morning", "end of day"

Convert relative to absolute using current date
```

### Location Identification
```
Detect:
- City/country names
- Addresses
- Office locations
- Meeting venues
- Geographic references
```

## Categorization Logic

### Auto-Category Assignment
```
"meeting" if contains:
- Multiple speakers
- Agenda items
- Action items assigned to different people
- Decision tracking

"idea" if contains:
- Brainstorming language
- "What if", "maybe we could"
- Creative exploration
- No specific commitments

"task" if contains:
- Multiple action items
- To-do list structure
- Task-oriented language

"journal" if contains:
- First-person reflection
- Personal thoughts
- Single speaker
- Introspective language

"research" if contains:
- Information gathering
- Notes from reading/learning
- References to sources
- Questions for further exploration
```

## Integration Actions

### Apple Notes Sync (if enabled)
```
Create note in configured notebook
↓
Include: Summary, action items, key points
↓
Format for readability
↓
Add link to full transcript
```

### Calendar Events (if enabled)
```
For each detected date/time with action:
- Parse date and time
- Create event suggestion
- Include: Action item, related context
- Request user confirmation
```

### Notion Sync (if enabled)
```
Create database entry with:
- Title (from summary)
- Date, Duration
- Category, Tags
- Action items
- Full analysis
- Link to transcript
```

## Examples

### Example 1: Team Meeting Analysis
**Input**: 15-minute team meeting transcript

**Output**:
```markdown
# Q4 Planning Meeting - Analysis

## Summary
Team discussed Q4 priorities and resource allocation. Key decision: 
Focus on product feature X due to customer demand. Sarah will lead 
development, timeline is 6 weeks. Budget approved at $50K. Concerns 
about testing timeline addressed - QA team will start parallel 
testing in week 3.

## Action Items

### HIGH Priority
- [ ] Sarah: Draft technical spec for feature X — Due: Nov 10
- [ ] John: Secure $50K budget approval from finance — Due: Nov 8

### MEDIUM Priority
- [ ] Team: Review and comment on spec — Due: Nov 15
- [ ] Mike: Coordinate with QA team on testing plan

## Key Points
- Customer demand for feature X is strong (mentioned 3 times in feedback)
- 6-week timeline is aggressive but feasible
- QA parallel testing will reduce overall timeline
- Budget approval needed before work begins

## Entities & References
**People**: Sarah (Lead), John (Finance), Mike (QA Coordinator)
**Dates**: Nov 8 (budget), Nov 10 (spec), Nov 15 (review), Dec 20 (launch)
**Projects**: Feature X, Q4 Roadmap
**Budget**: $50,000

## Questions & Decisions
**Decisions Made**:
- Proceed with Feature X for Q4
- Sarah leads development
- 6-week timeline approved
- $50K budget allocated

**Unanswered Questions**:
- Who will handle customer communications?
- What's the backup plan if timeline slips?

## Classification
**Categories**: meeting, work, planning
**Tags**: #q4, #feature-x, #planning, #team-meeting, #product
**Tone**: Professional, focused
**Sentiment**: Positive, motivated
```

### Example 2: Personal Journal Entry
**Input**: 3-minute personal reflection

**Output**:
```markdown
# Daily Reflection - Analysis

## Summary
Reflecting on career progress and goals. Feeling good about recent 
promotion but uncertain about next steps. Considering whether to 
pursue management track or stay in IC role. Need to discuss with 
mentor.

## Action Items

### MEDIUM Priority
- [ ] Schedule meeting with mentor to discuss career path
- [ ] Research management training programs

## Key Points
- Recent promotion feels like validation of hard work
- Uncertainty about management vs. IC track
- Value both technical depth and team leadership
- Mentor input would be helpful

## Classification
**Categories**: personal, journal, career
**Tags**: #reflection, #career, #decision-making, #growth
**Tone**: Reflective, thoughtful
**Sentiment**: Mixed (positive about past, uncertain about future)
```

### Example 3: Quick Task Capture
**Input**: 1-minute voice memo listing tasks

**Output**:
```markdown
# Task List - Analysis

## Summary
Quick capture of errands and tasks for the week.

## Action Items

### HIGH Priority
- [ ] Buy birthday gift for Mom — Due: Thursday

### MEDIUM Priority
- [ ] Schedule dentist appointment
- [ ] Pick up dry cleaning
- [ ] Reply to David's email about project

### LOW Priority
- [ ] Research new coffee maker
- [ ] Update resume

## Classification
**Categories**: task, personal
**Tags**: #errands, #tasks, #shopping, #appointments
```

## Error Handling

### Empty or Very Short Transcripts
```
If transcript < 50 words:
- Note that analysis may be limited
- Extract what's available
- Skip sections with no content
- Suggest user add more detail
```

### Multiple Languages
```
If transcript contains multiple languages:
- Note primary language
- Extract entities from all languages
- Generate summary in primary language
- Flag for user review
```

### Unclear Action Items
```
If action item ambiguous:
- Extract anyway with [needs clarification] note
- Include surrounding context
- Suggest user review
```

## Quality Metrics

- **Action Item Recall**: >95% of actual tasks identified
- **Summary Quality**: Captures all key points
- **Entity Accuracy**: >90% correct entity extraction
- **Category Accuracy**: >85% appropriate category assignment
- **User Satisfaction**: >80% find analysis helpful

## Performance

- **Processing Time**: <30 seconds for typical memo
- **Output Size**: 0.5-2KB per minute of audio
- **Accuracy**: >90% for clear transcripts

## Next Steps After Analysis

### Automatic
- Save analysis file
- Update search index
- Log in history

### User Options
1. Export to preferred format
2. Sync to integrations
3. Archive or delete
4. Create follow-up items
5. Link to related memos

## File Locations

### Input
- Transcript: `~/MyDrive/VoiceMemos/transcripts/`
- Config: `~/MyDrive/VoiceMemos/config/settings.json`
- Prompt: `~/MyDrive/VoiceMemos/config/prompts/analysis.txt`

### Output
- Analysis: `~/MyDrive/VoiceMemos/processed/YYYY-MM-DD/`
- Action items: Optionally extracted to separate file

---

**Skill Status**: Production Ready  
**Dependencies**: Transcription output, configuration system  
**Related Skills**: voice-transcription (prerequisite)  
**Support**: See CONFIG-GUIDE.md for settings
