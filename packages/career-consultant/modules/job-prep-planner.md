---
module_name: job-prep-planner
version: 1.0.0
description: Detailed interview preparation planning with hour breakdowns, study plans, and timelines
token_cost: ~4-6K tokens per plan
dependencies: [scoring-formulas.md]
status: active
---

# Job Preparation Planner Module

## Purpose

This module creates detailed, actionable preparation plans for specific job opportunities. It breaks down the estimated preparation hours into specific activities, provides study resources, suggests a timeline, and helps candidates track their progress.

## When to Load This Module

Load this module when user requests:
- "Create prep plan for [job_id]"
- "How should I prepare for [company] interview?"
- "Generate study plan for [role]"
- "Show me preparation timeline for [job]"

## Token Budget

- Basic prep plan: ~3-4K tokens
- Detailed prep plan with resources: ~5-6K tokens
- Multiple job plans: ~3K per additional job

## Core Workflow

### Step 1: Load Job Data

```python
def generate_prep_plan(job_id: str, user_data_base: str):
    """
    Generate detailed preparation plan for a specific job.
    
    Args:
        job_id: Job identifier (e.g., "nvidia-senior-tpm-20251120")
        user_data_base: Path to user-data directory
    
    Returns:
        Structured preparation plan with timeline
    """
    # Load job analysis
    job_file = f"{user_data_base}/jobs/analyzed/{job_id}.md"
    
    try:
        content = filesystem:read_text_file(path=job_file)
        job_data = parse_yaml_frontmatter(content)
    except FileNotFoundError:
        print(f"❌ Job {job_id} not found. Analyze the job first.")
        return
    
    # Load company data
    company_file = f"{user_data_base}/companies/{job_data['company_id']}.md"
    company_content = filesystem:read_text_file(path=company_file)
    company_data = parse_yaml_frontmatter(company_content)
    
    # Generate plan
    plan = create_preparation_plan(job_data, company_data)
    
    # Save plan
    plan_file = f"{user_data_base}/jobs/analyzed/{job_id}-prep-plan.md"
    filesystem:write_file(path=plan_file, content=plan)
    
    print(f"✅ Preparation plan saved: {plan_file}")
    display_prep_plan_summary(plan)
```

### Step 2: Calculate Hour Breakdown

```python
def calculate_prep_hours(job_data: dict, company_data: dict) -> dict:
    """
    Break down preparation hours by category.
    
    Returns:
        {
            'company_research': hours,
            'skills_gap': hours,
            'behavioral': hours,
            'technical': hours,
            'mock_interviews': hours,
            'total': hours
        }
    """
    hours = {}
    
    # 1. Company Research (8-20 hours based on tier and familiarity)
    tier = company_data.get('tier', 3)
    if tier == 1:
        # Well-documented companies
        hours['company_research'] = 8
    elif tier == 2:
        hours['company_research'] = 12
    else:
        hours['company_research'] = 16
    
    # 2. Skills Gap (10-50 hours based on match score)
    match_score = job_data.get('score_match', 0)
    max_match = 35  # From scoring system
    
    if match_score >= 30:
        hours['skills_gap'] = 10  # Minor gaps
    elif match_score >= 25:
        hours['skills_gap'] = 20  # Moderate gaps
    elif match_score >= 20:
        hours['skills_gap'] = 35  # Significant gaps
    else:
        hours['skills_gap'] = 50  # Major gaps
    
    # 3. Behavioral Prep (15-25 hours based on role level)
    role_title = job_data.get('position_title', '').lower()
    if 'director' in role_title or 'vp' in role_title:
        hours['behavioral'] = 25
    elif 'manager' in role_title or 'lead' in role_title:
        hours['behavioral'] = 20
    else:
        hours['behavioral'] = 15
    
    # 4. Technical Prep (20-40 hours based on role type)
    if 'tpm' in role_title or 'program manager' in role_title:
        hours['technical'] = 25
    elif 'engineering manager' in role_title:
        hours['technical'] = 30
    elif 'product manager' in role_title:
        hours['technical'] = 20
    else:
        hours['technical'] = 35
    
    # 5. Mock Interviews (10-15 hours)
    hours['mock_interviews'] = 12
    
    # 6. Company-Specific Prep (5-15 hours based on interview difficulty)
    glassdoor_rating = company_data.get('glassdoor_rating', 3.5)
    if glassdoor_rating >= 4.0:
        hours['company_specific'] = 8
    else:
        hours['company_specific'] = 12
    
    hours['total'] = sum(hours.values())
    
    return hours
```

### Step 3: Generate Study Plan

```python
def generate_study_plan(job_data: dict, company_data: dict, hours: dict) -> str:
    """
    Create week-by-week study plan.
    """
    company_name = company_data['company_name']
    role_title = job_data['position_title']
    total_hours = hours['total']
    
    # Assume 15-20 hours/week commitment
    weekly_hours = 18
    total_weeks = (total_hours // weekly_hours) + 1
    
    plan = f"""
# Interview Preparation Plan

**Company:** {company_name}  
**Role:** {role_title}  
**Total Estimated Hours:** {total_hours} hours  
**Timeline:** {total_weeks} weeks ({weekly_hours} hrs/week)  
**Target Interview Date:** [Set based on application timeline]

---

## 📊 Hour Breakdown

| Category | Hours | Percentage |
|----------|-------|------------|
| Company Research | {hours['company_research']} | {hours['company_research']/total_hours*100:.0f}% |
| Skills Gap Study | {hours['skills_gap']} | {hours['skills_gap']/total_hours*100:.0f}% |
| Behavioral Prep | {hours['behavioral']} | {hours['behavioral']/total_hours*100:.0f}% |
| Technical Prep | {hours['technical']} | {hours['technical']/total_hours*100:.0f}% |
| Mock Interviews | {hours['mock_interviews']} | {hours['mock_interviews']/total_hours*100:.0f}% |
| Company-Specific | {hours['company_specific']} | {hours['company_specific']/total_hours*100:.0f}% |
| **Total** | **{total_hours}** | **100%** |

---

## 📅 Week-by-Week Plan

"""
    
    # Generate weekly breakdown
    plan += generate_weekly_schedule(hours, total_weeks, weekly_hours, job_data, company_data)
    
    # Add resources
    plan += generate_study_resources(job_data, company_data)
    
    # Add milestones
    plan += generate_milestones(total_weeks)
    
    return plan

def generate_weekly_schedule(hours: dict, total_weeks: int, weekly_hours: int, 
                             job_data: dict, company_data: dict) -> str:
    """Generate week-by-week schedule."""
    
    schedule = ""
    
    # Week 1: Foundation
    schedule += f"""
### Week 1: Foundation ({weekly_hours} hours)

**Focus:** Company understanding + behavioral framework

- **Company Research ({hours['company_research']//2} hrs)**
  - Read company website, blog, recent news
  - Study products/services in detail
  - Review Glassdoor interviews ({company_data.get('glassdoor_rating', 'N/A')}/5.0)
  - Understand business model and revenue streams
  - Research company culture and values

- **Behavioral Prep ({hours['behavioral']//2} hrs)**
  - Review STAR framework
  - Identify 8-10 key stories from experience
  - Map stories to common competencies:
    - Leadership & Influence
    - Problem Solving & Decision Making
    - Communication & Collaboration
    - Dealing with Ambiguity
    - Innovation & Ownership

- **Role Research ({weekly_hours - (hours['company_research']//2) - (hours['behavioral']//2)} hrs)**
  - Deep dive into job description
  - Identify must-have vs nice-to-have skills
  - Research similar roles at company
  - Connect with employees on LinkedIn

**Milestone:** Complete company overview, 5 polished STAR stories

---
"""
    
    # Week 2: Skills Development
    schedule += f"""
### Week 2: Skills Deep Dive ({weekly_hours} hours)

**Focus:** Close skills gaps + technical preparation

- **Skills Gap Study ({hours['skills_gap']//3} hrs)**
  - Identify top 3-5 skill gaps from job requirements
  - Create focused study plan for each gap
  - Complete online courses/tutorials
  - Build small project/demo if applicable

- **Technical Prep ({hours['technical']//2} hrs)**
  - System design review (if applicable)
  - Architecture patterns
  - Technologies used by company
  - Review technical concepts in job description

- **Behavioral Refinement ({hours['behavioral']//3} hrs)**
  - Refine STAR stories
  - Practice delivery
  - Get feedback from peers/mentors

**Milestone:** Close 2-3 major skill gaps, 8 polished stories ready

---
"""
    
    # Week 3: Practice & Polish
    if total_weeks >= 3:
        schedule += f"""
### Week 3: Practice & Polish ({weekly_hours} hours)

**Focus:** Mock interviews + company-specific prep

- **Mock Interviews ({hours['mock_interviews']//2} hrs)**
  - Schedule 2 mock interviews with peers/mentors
  - Practice behavioral questions
  - Practice technical/case questions
  - Record and review performance

- **Company-Specific Prep ({hours['company_specific']} hrs)**
  - Study {company_data['company_name']}-specific topics
  - Review technical blog posts
  - Understand company's tech stack
  - Research recent projects/launches

- **Skills Gap Continued ({hours['skills_gap']//3} hrs)**
  - Continue closing remaining gaps
  - Build depth in key areas

**Milestone:** Complete 2 full mock interviews, ready for real interviews

---
"""
    
    # Week 4+: Final Push
    if total_weeks >= 4:
        schedule += f"""
### Week 4{'+' if total_weeks > 4 else ''}: Final Preparation ({weekly_hours} hours)

**Focus:** Final reviews + confidence building

- **Final Mock Interviews ({hours['mock_interviews']//2} hrs)**
  - 1-2 more mock interviews
  - Focus on weak areas identified
  - Simulate full interview loop

- **Review & Consolidation ({weekly_hours//2} hrs)**
  - Review all prepared materials
  - Refresh company research
  - Practice elevator pitch
  - Prepare questions for interviewers

- **Stress Management & Mindset (2-3 hrs)**
  - Visualization exercises
  - Stress reduction techniques
  - Positive mindset preparation

**Milestone:** Interview-ready, confident, all materials polished

---
"""
    
    return schedule

def generate_study_resources(job_data: dict, company_data: dict) -> str:
    """Generate study resources section."""
    
    role_title = job_data.get('position_title', '').lower()
    company_name = company_data['company_name']
    
    resources = """
## 📚 Study Resources

### Company-Specific
"""
    
    resources += f"""
- **{company_name} Website:** [company website]
- **{company_name} Engineering Blog:** [blog if available]
- **{company_name} GitHub:** [if applicable]
- **Glassdoor Reviews:** Research interview experiences
- **LinkedIn:** Connect with employees, review backgrounds
- **Recent News:** Google News alerts for {company_name}

"""
    
    # Role-specific resources
    if 'tpm' in role_title or 'program manager' in role_title:
        resources += """
### TPM-Specific Resources
- **Books:**
  - "The TPM Playbook" (Focus on program management frameworks)
  - "Cracking the PM Interview" (TPM sections)
  
- **Online:**
  - Exponent.io TPM Interview Course
  - IGotAnOffer TPM Guide
  - YouTube: TPM interview walkthroughs

- **Technical Topics:**
  - System design fundamentals
  - Software development lifecycle
  - Project management methodologies
  - Risk management frameworks
"""
    
    elif 'engineering manager' in role_title or 'manager' in role_title:
        resources += """
### Engineering Manager Resources
- **Books:**
  - "The Manager's Path" by Camille Fournier
  - "An Elegant Puzzle" by Will Larson
  - "High Output Management" by Andy Grove

- **Online:**
  - Exponent.io EM Interview Course
  - LeadDev resources
  - Manager Tools podcast

- **Key Topics:**
  - People management & coaching
  - Technical depth in relevant areas
  - Strategic planning & roadmapping
  - Hiring & team building
"""
    
    elif 'product manager' in role_title:
        resources += """
### Product Manager Resources
- **Books:**
  - "Cracking the PM Interview"
  - "Inspired" by Marty Cagan
  - "The Lean Product Playbook"

- **Online:**
  - Exponent.io PM Interview Course
  - Product School resources
  - Case interview practice platforms

- **Key Topics:**
  - Product sense & strategy
  - Analytics & metrics
  - Technical fundamentals
  - Go-to-market strategy
"""
    
    resources += """
### Behavioral Interview
- **STAR Framework Guide:**
  - Situation: Context setting (10%)
  - Task: Your responsibility (15%)
  - Action: What YOU did (60%)
  - Result: Outcome + learnings (15%)

- **Common Question Categories:**
  - Leadership & influence
  - Conflict resolution
  - Failure & learning
  - Ambiguity & change
  - Innovation & impact

### General
- **Mock Interview Platforms:**
  - Pramp (free peer practice)
  - Exponent.io (paid, high quality)
  - interviewing.io (anonymous practice)

- **Company Research:**
  - Crunchbase (funding, financials)
  - LinkedIn Sales Navigator (org structure)
  - Glassdoor (culture, interviews)

"""
    
    return resources

def generate_milestones(total_weeks: int) -> str:
    """Generate milestone tracking section."""
    
    milestones = """
## 🎯 Milestones & Checkpoints

### Week 1
- [ ] Complete company overview document
- [ ] Identify 10 STAR stories
- [ ] Polish 5 best stories
- [ ] Create skills gap assessment

### Week 2
- [ ] Close 2-3 major skill gaps
- [ ] Complete technical concepts review
- [ ] Refine all 10 STAR stories
- [ ] Prepare 10 questions for interviewers

### Week 3
- [ ] Complete 2 mock behavioral interviews
- [ ] Complete 1 mock technical interview
- [ ] Review feedback and improve
- [ ] Finalize company-specific knowledge

"""
    
    if total_weeks >= 4:
        milestones += """
### Week 4
- [ ] Final mock interview (full loop)
- [ ] Review all materials
- [ ] Prepare day-of checklist
- [ ] Mental preparation & confidence building

"""
    
    milestones += """
### Pre-Interview (Day Before)
- [ ] Review company recent news
- [ ] Review job description one more time
- [ ] Prepare questions for each interviewer
- [ ] Get good sleep, manage stress

### Interview Day
- [ ] Arrive 10 min early (or test video setup)
- [ ] Have notepad ready
- [ ] Water/coffee prepared
- [ ] Positive mindset, confident

"""
    
    milestones += """
---

## 📝 Notes & Adjustments

Use this space to track your progress and adjust the plan:

- **Week 1 Notes:** [Your notes]
- **Week 2 Notes:** [Your notes]
- **Challenges Encountered:** [Any roadblocks]
- **Adjustments Made:** [Plan modifications]

---

## ✅ Completion Checklist

Before scheduling interview:
- [ ] Company research comprehensive
- [ ] 8-10 polished STAR stories
- [ ] Skills gaps addressed
- [ ] 2+ mock interviews completed
- [ ] Company-specific prep done
- [ ] Questions for interviewers prepared
- [ ] Confident and ready

**Good luck! 🚀**
"""
    
    return milestones
```

---

## Example Output

```markdown
# Interview Preparation Plan

**Company:** NVIDIA  
**Role:** Senior Software TPM  
**Total Estimated Hours:** 85 hours  
**Timeline:** 5 weeks (17 hrs/week)  
**Target Interview Date:** [Set based on application timeline]

---

## 📊 Hour Breakdown

| Category | Hours | Percentage |
|----------|-------|------------|
| Company Research | 8 | 9% |
| Skills Gap Study | 20 | 24% |
| Behavioral Prep | 20 | 24% |
| Technical Prep | 25 | 29% |
| Mock Interviews | 12 | 14% |
| Company-Specific | 8 | 9% |
| **Total** | **93** | **100%** |

---

## 📅 Week-by-Week Plan

[Full weekly breakdown as shown above]

---

## 📚 Study Resources

[Full resources list as shown above]

---

## 🎯 Milestones & Checkpoints

[Full milestones list as shown above]
```

---

## Integration with SKILL.md

Add command detection in main workflow:

```python
# In SKILL.md initialization or command detection

if 'prep plan' in user_message.lower() or 'preparation plan' in user_message.lower():
    # Load prep planner module
    prep_module = file_read("modules/job-prep-planner.md")
    
    # Extract job_id
    job_id = extract_job_id_from_message(user_message)
    
    if not job_id:
        print("Please specify which job: 'Create prep plan for [job-id]'")
        STOP
    
    # Generate plan
    generate_prep_plan(job_id, USER_DATA_BASE)
```

---

## Version History

- **v1.0.0** (2025-11-20): Initial release

---

**Module Status**: Active  
**Last Updated**: 2025-11-20  
**Dependencies**: scoring-formulas.md
