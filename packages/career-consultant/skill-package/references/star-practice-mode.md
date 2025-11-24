# STAR Practice Mode System
**Reference:** star-practice-mode.md  
**Version:** 1.0  
**Purpose:** Interview rehearsal and story practice functionality  
**Phase:** 5 of 6

---

## Overview

The Practice Mode system provides three distinct practice formats to help users rehearse their STAR stories and build interview confidence. It bridges the gap between story creation and actual interview performance.

---

## 📋 Core Components

### 1. Flash Cards - Quick Review
### 2. Timed Practice - Delivery Training
### 3. Mock Interview - Simulation

---

## 1️⃣ Flash Cards - Quick Review

### Purpose
Rapid review system for memorizing story key points and question-to-story mappings.

### Card Structure

```yaml
---
# Flash Card Format
card_id: "flash-card-001"
story_id: "leadership-conflict-resolution-001"
story_title: "Resolving Engineering Team Conflict"
competencies: ["conflict-resolution", "leadership", "decision-making"]
---

# FRONT (Question Side)

**Question:**
"Tell me about a time you resolved a team conflict"

**Competencies Tested:**
• Conflict Resolution
• Leadership
• Decision-Making

**Difficulty:** Medium
**Time Limit:** 2 minutes

---

# BACK (Answer Side)

**Story:** Resolving Engineering Team Conflict

**30-Second Version:**
Two senior engineers had a 3-week deadlock on API design (REST vs GraphQL). I facilitated a decision workshop with evaluation criteria, ran POC experiments, and got unanimous agreement in 2 days. Project stayed on track, team dynamics improved.

**Key Points (S-T-A-R):**
• **S:** 2 senior engineers, 3-week API debate, project deadline at risk
• **T:** Break deadlock in 1 week, maintain relationships
• **A:** Decision matrix, facilitated workshop, POC experiments
• **R:** Decision in 2 days, unanimous, project on track, +35% team collab

**Remember to Mention:**
✓ Data-driven approach (evaluation matrix)
✓ Neutral facilitation (not authority-based)
✓ Relationship preservation
✓ Quantifiable outcome (35% improvement)

**Common Follow-ups:**
→ "How did you remain neutral?"
→ "What if they still disagreed?"
→ "What was the final decision?"
```

### Flash Card Modes

**Mode 1: Sequential Review**
- Go through all cards in order
- Best for comprehensive review
- Progress tracking: X of Y cards

**Mode 2: Shuffle Mode**
- Random card order
- Simulates real interview unpredictability
- Builds quick recall

**Mode 3: Competency Focus**
- Filter by specific competency
- Practice weak areas
- "Show me all leadership cards"

**Mode 4: Interview Prep**
- Cards for specific job/company
- Based on job integration package
- Only relevant competencies

### Display Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📇 FLASH CARD PRACTICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Card 3 of 8 | Competency: Leadership

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 QUESTION (FRONT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Tell me about a time you had to make a difficult decision with limited information"

Competencies: Decision-Making, Risk Management
Time Limit: 2 minutes

[Press Enter to reveal answer]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ ANSWER (BACK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Story:** Emergency Production Hotfix Decision

**30-Second Version:**
Production API failing, affecting 10K users. Had 2 hours to decide: quick patch (risky) or rollback (loses week of features). Analyzed error patterns, consulted 2 engineers, chose targeted patch with monitoring. Zero downtime, features preserved, issue resolved in 90 minutes.

**Key Points (S-T-A-R):**
• S: Production down, 10K users affected, 2-hour window
• T: Choose fix approach, balance risk vs. feature preservation
• A: Error analysis, expert consultation, monitored patch
• R: 90-min resolution, zero downtime, features kept

**Remember:** Emphasize systematic approach under pressure

**Rating:** ⭐⭐⭐ Interview-ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actions:
[N]ext card | [P]revious | [F]ull story | [M]ark for review | [Q]uit

Your choice:
```

### Spaced Repetition (Optional)

For advanced practice, implement spaced repetition:

```python
def calculate_next_review(card, performance):
    """
    Calculate when card should be reviewed again
    
    Performance levels:
    - Easy: 4 days
    - Good: 2 days
    - Hard: 1 day
    - Again: Same session
    """
    intervals = {
        'easy': 4,
        'good': 2,
        'hard': 1,
        'again': 0
    }
    
    next_review = datetime.now() + timedelta(days=intervals[performance])
    return next_review
```

---

## 2️⃣ Timed Practice - Delivery Training

### Purpose
Practice delivering stories within time constraints (30s, 2min, 5min versions).

### Time Formats

**30-Second Elevator Pitch**
- Use case: Quick answer or intro
- Structure: Situation + Result only
- Goal: Hit key points fast

**2-Minute Full Story**
- Use case: Standard interview answer
- Structure: Full S-T-A-R with details
- Goal: Complete, concise, impactful

**5-Minute Deep Dive**
- Use case: "Tell me more" follow-ups
- Structure: S-T-A-R with examples, decisions, learnings
- Goal: Demonstrate deep expertise

### Practice Session Flow

**Step 1: Setup**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ TIMED PRACTICE MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Story: Resolving Engineering Team Conflict
Target Time: 2 minutes

**Your Goal:**
Deliver this story in 2 minutes or less while covering all key S-T-A-R points.

**Timer will show:**
• Green: 0-90 seconds (on track)
• Yellow: 90-120 seconds (target zone)  
• Red: 120+ seconds (overtime)

**Key Points to Cover:**
✓ Situation: 3-week debate between engineers
✓ Task: Break deadlock, maintain relationships
✓ Action: Workshop, decision matrix, POC
✓ Result: 2-day resolution, unanimous agreement

Ready? [Start Timer] [See Full Story First]
```

**Step 2: Practice**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ RECORDING... 00:45
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Timer running...]

"At my previous company, two senior engineers had been 
debating the architecture approach for our new API..."

[User speaks their story]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Progress: ████████░░░░ 65% complete
Time: 1:18 remaining
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Stop] [Pause] [Restart]
```

**Step 3: Feedback**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ PRACTICE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Your Time:** 1:54 ✅ (Target: 2:00)

**Performance:**
• Timing: ✅ Excellent (within target)
• Coverage: ⚠️ Good (3 of 4 sections covered)
• Pacing: ✅ Even delivery

**Key Points Covered:**
✅ Situation: Clear context
✅ Task: Your role defined
✅ Action: Specific steps mentioned
❌ Result: Missing quantifiable outcome

**Suggestions:**
1. Add the "35% improvement in collaboration" metric
2. Mention "unanimous agreement" for stronger impact
3. Consider: Did you mention the 2-day timeline?

**Target for Next Practice:**
• Include all 4 key points
• Keep timing at 1:45-2:00
• Add one more quantifiable result

[Practice Again] [Try 30-sec Version] [Save Performance] [Next Story]
```

### Performance Tracking

```yaml
practice_session:
  session_id: "practice-2025-10-30-001"
  story_id: "leadership-conflict-resolution-001"
  target_time: 120  # seconds
  
  attempts:
    - attempt: 1
      time: 145
      coverage_score: 75  # % of key points covered
      pacing_score: 85
      timestamp: "2025-10-30T14:00:00Z"
      
    - attempt: 2
      time: 114
      coverage_score: 100
      pacing_score: 90
      timestamp: "2025-10-30T14:15:00Z"
      improvement: true
  
  progress:
    initial_time: 145
    best_time: 114
    improvement_pct: 21
    target_achieved: true
```

### Timing Guidelines

**30-Second Version Structure:**
- Situation: 5-8 seconds
- Result: 15-20 seconds (main focus)
- Key metric: 5 seconds
- Total: 25-33 seconds

**2-Minute Version Structure:**
- Situation: 20-25 seconds
- Task: 15-20 seconds
- Action: 50-60 seconds (main focus)
- Result: 20-25 seconds
- Total: 105-130 seconds

**5-Minute Version Structure:**
- Situation: 45-60 seconds (rich context)
- Task: 30-45 seconds (constraints, goals)
- Action: 150-180 seconds (detailed steps, decisions)
- Result: 60-90 seconds (multiple impacts)
- Total: 285-375 seconds

---

## 3️⃣ Mock Interview - Simulation

### Purpose
AI-powered interview simulation with realistic questions and feedback.

### Interview Session Structure

**Phase 1: Setup**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 MOCK INTERVIEW SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Interview Configuration:**

1. **Interview Type:**
   • General Behavioral (10 questions)
   • Job-Specific (Wix Engineering Manager)
   • Competency Focus (Leadership only)
   • Quick Practice (5 questions)

2. **Difficulty:**
   • Standard (straightforward questions)
   • Advanced (follow-ups, edge cases)
   • Stress Test (rapid-fire, interruptions)

3. **Stories Available:**
   • 8 stories in your library
   • 5 recommended for this role
   • 3 backup stories

4. **Duration:** 20-30 minutes

[Start Interview] [Change Settings]
```

**Phase 2: Interview Simulation**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 MOCK INTERVIEW - Question 1 of 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Interviewer (AI):**
"Thank you for joining us today. Let's start with a leadership question. Tell me about a time you had to resolve a conflict between team members."

**Your Response:**
[Type your answer or use voice input]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ Time: 0:00 | Recommended: 2-3 min
💡 Tip: Start with the situation and context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[I'm ready to answer] [Skip question] [End interview]
```

**User delivers their story...**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 REAL-TIME FEEDBACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[User is speaking...]

✅ Good pacing
✅ Clear situation established
⚠️ Consider adding more about your specific role
✅ Action steps are detailed
⏰ Time: 1:35 / Target: 2:00

[Continue]
```

**Phase 3: Follow-up Questions**
```
**Interviewer (AI):**
"That's a good example. Can you tell me more about how you remained neutral when facilitating the discussion?"

**Your Response:**
[Answer follow-up question]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Tip: This is testing your conflict resolution approach
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Phase 4: Question Feedback**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUESTION 1 FEEDBACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall:** ⭐⭐⭐ Strong (8.5/10)

**Strengths:**
✅ Clear situation setup
✅ Specific actions described
✅ Good pacing and timing (1:54)
✅ Quantifiable result mentioned

**Areas to Improve:**
⚠️ Task section could be clearer (your specific role)
⚠️ Follow-up answer was brief (expand on neutrality)

**Competency Demonstrated:**
• Conflict Resolution: ⭐⭐⭐ Strong
• Leadership: ⭐⭐ Good
• Decision-Making: ⭐⭐ Good

**Suggested Practice:**
• Emphasize YOUR role more clearly in Task section
• Practice follow-up on "maintaining neutrality"

[Continue to Question 2] [Review Full Answer] [End Here]
```

**Phase 5: Interview Summary**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 MOCK INTERVIEW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Session Summary:**
Date: 2025-10-30
Duration: 28 minutes
Questions: 5 of 5 completed

**Overall Performance:** ⭐⭐⭐ 8.2/10 (Strong)

**By Question:**
1. Conflict Resolution → 8.5/10 ⭐⭐⭐
2. Technical Challenge → 7.8/10 ⭐⭐
3. Team Leadership → 8.9/10 ⭐⭐⭐
4. Scaling Initiative → 7.5/10 ⭐⭐
5. Innovation Example → 8.4/10 ⭐⭐⭐

**Competency Coverage:**
• Leadership: ⭐⭐⭐ Demonstrated strongly
• Technical: ⭐⭐ Demonstrated well
• Collaboration: ⭐⭐ Demonstrated well
• Innovation: ⭐⭐⭐ Demonstrated strongly

**Timing Performance:**
• Average: 2:05 per answer ✅ (Target: 2-3 min)
• Shortest: 1:35 (Q2)
• Longest: 2:45 (Q3)

**Top Strengths:**
1. Excellent quantification of results
2. Clear, structured S-T-A-R format
3. Good time management
4. Strong storytelling flow

**Key Improvements:**
1. Clarify "your role" in Task section (appeared in 3 answers)
2. Add more decision rationale in Action
3. Prepare deeper follow-up answers

**Story Usage:**
• Architecture Migration: Used 1x ✓
• Conflict Resolution: Used 1x ✓
• Team Scaling: Used 1x ✓
• Process Improvement: Used 1x ✓
• Innovation Initiative: Used 1x ✓

**Ready for Real Interview?**
✅ Strong performance across competencies
✅ Good timing and structure
⚠️ Practice follow-up questions more
⚠️ Polish Task section clarity

**Recommended Next Steps:**
1. Do 1-2 more mock interviews focusing on follow-ups
2. Practice "Task" sections for 5-10 minutes
3. Review Question 4 (lowest score) and refine

[Save Session] [Practice Weak Areas] [Schedule Another Mock] [Exit]
```

### Question Generation

AI interviewer uses context-aware question generation:

```python
def generate_interview_questions(job_context, story_library, num_questions=5):
    """
    Generate interview questions based on job and available stories
    
    Returns: List of questions with metadata
    """
    questions = []
    
    # 1. Extract competencies from job
    job_competencies = extract_job_competencies(job_context)
    
    # 2. Map to question types
    for competency in job_competencies[:num_questions]:
        question = {
            'competency': competency,
            'question_text': select_question_for_competency(competency),
            'difficulty': determine_difficulty(job_context['seniority']),
            'expected_stories': find_matching_stories(competency, story_library),
            'follow_ups': generate_follow_up_questions(competency),
            'evaluation_criteria': get_rubric_for_competency(competency)
        }
        questions.append(question)
    
    return questions
```

### Real-time Feedback Algorithm

```python
def provide_realtime_feedback(user_response, expected_story):
    """
    Analyze user's response in real-time
    
    Returns: Feedback and suggestions
    """
    feedback = {
        'structure_score': check_star_structure(user_response),
        'key_points_covered': count_key_points(user_response, expected_story),
        'timing_assessment': evaluate_timing(user_response),
        'suggestions': []
    }
    
    # Check Situation
    if not has_clear_situation(user_response):
        feedback['suggestions'].append("Add more context about the situation")
    
    # Check Task
    if not has_personal_role_clarity(user_response):
        feedback['suggestions'].append("Clarify YOUR specific role/task")
    
    # Check Action
    if count_actions(user_response) < 3:
        feedback['suggestions'].append("Add more specific action steps")
    
    # Check Result
    if not has_quantifiable_results(user_response):
        feedback['suggestions'].append("Include quantifiable outcomes")
    
    return feedback
```

### Session Recording

```yaml
mock_interview_session:
  session_id: "mock-2025-10-30-001"
  date: "2025-10-30T14:00:00Z"
  duration_minutes: 28
  interview_type: "job_specific"
  job_context:
    company: "Wix"
    role: "Engineering Manager"
  
  questions:
    - question_num: 1
      competency: "conflict_resolution"
      question_text: "Tell me about a time you resolved a conflict..."
      story_used: "leadership-conflict-resolution-001"
      response_time: 114
      score: 8.5
      feedback: "Strong answer, clear structure..."
      
    # ... more questions
  
  overall_performance:
    avg_score: 8.2
    timing_avg: 125
    competencies_covered: 5
    stories_used: 5
    
  improvements_identified:
    - "Clarify Task section role clarity"
    - "Practice follow-up responses"
    - "Add more decision rationale"
```

---

## 📊 Integration Points

### With Story Library
- Load stories from `user-data/interview-prep/star-stories/`
- Filter by competency for targeted practice
- Track which stories are practiced most/least

### With Job Integration
- Use prep package to focus practice
- Practice stories selected for specific interview
- Match mock interview questions to job competencies

### With Quality System
- Use story scores to prioritize practice
- Focus on lower-scored stories
- Track improvement over time

---

## 🎯 User Workflows

### Workflow 1: Quick Review (10 min)
```
User: "Quick review of my stories"
→ Flash card mode
→ Shuffle all stories
→ 30-second versions only
→ 10-minute session
```

### Workflow 2: Pre-Interview Polish (1 hour)
```
User: "Practice for Wix interview tomorrow"
→ Load Wix prep package
→ Flash cards for 5 selected stories (15 min)
→ Timed practice for each story (25 min)
→ Mock interview with job-specific questions (20 min)
```

### Workflow 3: Weak Area Focus (30 min)
```
User: "Practice my leadership stories"
→ Filter stories by "leadership" competency
→ Timed practice for 3 stories
→ Focus on Task section clarity
→ Repeat until improved
```

---

## 📝 Implementation Notes

### File Locations
- Practice sessions: `user-data/interview-prep/practice-sessions/`
- Performance tracking: `user-data/interview-prep/practice-sessions/progress.yaml`

### Performance Optimization
1. Cache story library during practice session
2. Pre-generate flash cards on library changes
3. Store practice history for progress tracking

### User Experience
- Always show progress (X of Y)
- Celebrate improvements
- Provide specific, actionable feedback
- Make it easy to repeat practice

---

## ✅ Implementation Checklist

- [ ] Flash card generation from stories
- [ ] Sequential and shuffle modes
- [ ] Timed practice with timer display
- [ ] Performance feedback algorithm
- [ ] Mock interview question generation
- [ ] Real-time feedback during mock
- [ ] Session summary and tracking
- [ ] Progress visualization
- [ ] Integration with story library
- [ ] Integration with job prep packages

---

## 🎓 Best Practices

**For Users:**
- Practice regularly (2-3 times per week)
- Start with flash cards, progress to mock interviews
- Focus on weak areas identified in feedback
- Time yourself to build confidence
- Record improvement metrics

**For Claude:**
- Keep feedback specific and actionable
- Celebrate progress and improvements
- Adjust difficulty based on performance
- Provide context for why feedback matters
- Make practice feel productive, not punitive

---

**Version:** 1.0  
**Status:** ✅ Reference Complete  
**Phase:** 5 of 6 (Practice Mode)  
**Last Updated:** 2025-10-30
