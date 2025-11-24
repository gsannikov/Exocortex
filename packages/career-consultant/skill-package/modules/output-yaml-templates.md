---
title: Output YAML Templates Module
summary: Provide reusable YAML/Markdown templates for role analyses and deliverables.
last_updated: "2025-10-29"
---

# Output YAML Templates Module v9.0

## Purpose
Generate professional role analysis documents with YAML frontmatter and rich markdown content.

## When to Load This Module
- **Step 11**: After all scoring complete (Steps 5-10)
- **Prerequisites**: All scores calculated, match analysis done
- **Token Impact**: ~2K tokens

---

## Document Structure

```
---
[YAML Frontmatter - Machine-readable metadata]
---

[Markdown Content - Human-readable analysis]
```

---

## YAML Frontmatter Generation

### Create Role ID

```python
def create_role_id(company_id, position_title, date_analyzed):
    """
    Generate unique role identifier
    
    Format: {company-slug}-{position-slug}-{YYYYMMDD}
    Example: nvidia-engineering-manager-20251028
    
    Args:
        company_id: Company slug
        position_title: Job title
        date_analyzed: Date string YYYY-MM-DD
    
    Returns:
        Role ID string
    """
    
    from slug_utils import normalize_slug
    
    # Normalize position title
    position_slug = normalize_slug(position_title)
    
    # Extract date digits
    date_digits = date_analyzed.replace('-', '')
    
    role_id = f"{company_id}-{position_slug}-{date_digits}"
    
    return role_id
```

### Generate YAML Frontmatter

```python
def generate_role_frontmatter(
    role_id,
    company_data,
    role_data,
    scores,
    match_results,
    prep_strategy
):
    """
    Create YAML frontmatter with all metadata
    
    Args:
        role_id: Generated role ID
        company_data: Company frontmatter
        role_data: Job requirements dict
        scores: All calculated scores
        match_results: Skills matching results
        prep_strategy: Preparation strategy dict
    
    Returns:
        Dict for YAML serialization
    """
    
    from datetime import datetime
    
    frontmatter = {
        # IDs
        'role_id': role_id,
        'company_id': company_data['company_id'],

        # Basic Info
        'company_name': company_data['company_name'],
        'position_title': role_data['position_title'],
        'location': role_data['location'],
        'job_url': role_data['job_url'],

        # Dates & Version
        'date_analyzed': datetime.now().strftime('%Y-%m-%d'),
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'schema_version': '2.0',
        'analysis_depth': role_data.get('analysis_depth', 'basic'),  # basic | in_depth
        'last_basic_analysis': role_data.get('last_basic_analysis', None),
        'last_in_depth_analysis': role_data.get('last_in_depth_analysis', None),

        # Scores (converted to floats for precision)
        'score_match': float(scores['scores']['match']),
        'score_income': float(scores['scores']['income']),
        'score_growth': float(scores['scores']['growth']),
        'score_lowprep': float(scores['scores']['lowprep']),
        'score_stress': float(scores['scores']['stress']),
        'score_location': float(scores['scores']['location']),
        'score_total': float(scores['scores']['total']),

        # Classification
        'priority': scores['details']['priority'],
        'status': 'New',

        # Financial Details (monthly in ILS unless specified)
        'income_estimate': int(scores['details']['income_mid']),  # Monthly
        'income_estimate_annual': int(scores['details']['income_mid']) * 12,  # Annual
        'income_range_low': int(scores['details']['income_range'][0]),  # Monthly
        'income_range_high': int(scores['details']['income_range'][1]),  # Monthly

        # Preparation
        'prep_hours': int(scores['details']['prep_hours']),
        'best_cv': match_results['best_cv'],

        # Skills Matching
        'critical_gaps': match_results['critical_gaps'],
        'high_priority_gaps': match_results.get('high_priority_gaps', match_results.get('high_gaps', [])),
        'nice_to_have_gaps': match_results.get('nice_to_have_gaps', match_results.get('nice_gaps', [])),
        'strong_matches': match_results.get('strong_matches', [])[:10],  # Top 10

        # Role Details (Phase 2)
        'seniority_level': role_data.get('seniority_level', 'unknown'),
        'role_type': role_data.get('role_type', 'individual_contributor'),
        'team_size': role_data.get('team_size', 0),
        'reports_to': role_data.get('reports_to', ''),
        'direct_reports': role_data.get('direct_reports', 0),

        # Work Environment (Phase 2)
        'work_hours_weekly': role_data.get('work_hours_weekly', 40),
        'on_call_required': role_data.get('on_call_required', False),
        'on_call_frequency': role_data.get('on_call_frequency', 'never'),
        'travel_required': role_data.get('travel_required', False),
        'travel_percentage': role_data.get('travel_percentage', 0),

        # Interview Process (Phase 2)
        'interview_rounds_expected': role_data.get('interview_rounds_expected', 4),
        'interview_duration_hours': role_data.get('interview_duration_hours', 6),
        'interview_process_known': role_data.get('interview_process_known', False),
        'technical_interview': role_data.get('technical_interview', True),
        'coding_interview': role_data.get('coding_interview', True),
        'system_design_interview': role_data.get('system_design_interview', False),
        'behavioral_interview': role_data.get('behavioral_interview', True),
        'take_home_assignment': role_data.get('take_home_assignment', False),
        'take_home_hours': role_data.get('take_home_hours', 0),

        # Data Quality & Provenance (Phase 3)
        'score_confidence': scores.get('confidence', 0.75),  # 0-1 scale
        'income_confidence': scores.get('income_confidence', 'medium'),  # low/medium/high
        'data_sources': role_data.get('data_sources', ['company_website']),
        'data_quality': role_data.get('data_quality', 'medium'),  # low/medium/high
        'verified': role_data.get('verified', False),  # Human verified
        'analyzed_by': role_data.get('analyzed_by', 'system'),  # system/human/hybrid
        'analysis_method': role_data.get('analysis_method', 'automated_scoring'),

        # Organization & Metadata (Phase 4)
        'tags': role_data.get('tags', []),  # Custom tags for filtering
        'custom_notes': role_data.get('custom_notes', ''),  # Free-form notes
        'flagged': role_data.get('flagged', False),  # Star/flag important
        'archived': role_data.get('archived', False),  # Archive old roles
        'priority_override': role_data.get('priority_override', None),  # Manual override
        'application_deadline': role_data.get('application_deadline', None),  # YYYY-MM-DD
        'in_depth_requested': role_data.get('in_depth_requested', False),  # Phase 2 requested?
        'views': role_data.get('views', 0),  # View count
        'notes_count': role_data.get('notes_count', 0),  # Number of notes

        # Ranking (will be filled by Excel sync)
        'rank': None,
        'total_jobs': None
    }
    
    return frontmatter
```

---

## Markdown Content Generation

### Document Header

```python
def generate_document_header(frontmatter, scores):
    """
    Create document title and summary section
    """
    
    priority_emoji = scores['details']['priority_emoji']
    priority = scores['details']['priority']
    
    header = f"""# {frontmatter['position_title']} at {frontmatter['company_name']}

## Executive Summary

**Total Score**: {frontmatter['score_total']:.1f}/100 {priority_emoji}  
**Priority**: {priority}  
**Best CV Match**: {frontmatter['best_cv']}  
**Date Analyzed**: {frontmatter['date_analyzed']}

**Quick Stats**:
- Income Estimate: ₪{frontmatter['income_estimate']:,}/month (₪{frontmatter['income_estimate']*12:,}/year)
- Preparation Time: {frontmatter['prep_hours']} hours
- Critical Gaps: {len(frontmatter['critical_gaps'])}
- Location: {frontmatter['location']}

---
"""
    
    return header
```

### Score Breakdown Section

```python
def generate_score_breakdown(frontmatter, scores, match_results, company_data):
    """
    Detailed score breakdown with explanations
    """
    
    section = f"""## Score Breakdown

### Match: {frontmatter['score_match']:.1f}/35

{match_results['analysis_markdown']}

---

### Income: {frontmatter['score_income']:.1f}/25

**Estimated Salary Range**: ₪{frontmatter['income_range_low']:,} - ₪{frontmatter['income_range_high']:,}/month  
**Mid-Point**: ₪{frontmatter['income_estimate']:,}/month (₪{frontmatter['income_estimate']*12:,}/year)

**Calculation Factors**:
- Company Tier: {company_data['tier']} (multiplier: {get_tier_multiplier(company_data['tier'])})
- Role Level: {get_role_level_description(frontmatter['position_title'])}
- Domain: {get_domain_from_title(frontmatter['position_title'])}
- Experience Band: {get_experience_band_description()}

---

### Growth: {frontmatter['score_growth']:.1f}/20

**Assessment**: {assess_growth_level(frontmatter['score_growth'])}

**Company Context**:
- Tier: {company_data['tier']} ({company_data['tier_score']} base points)
- Funding Stage: {company_data['funding_stage']}
- Israeli Team Size: {company_data['employees_israel']} employees
- Glassdoor Rating: {company_data.get('glassdoor_rating', 'N/A')}/5.0 ⭐

**Growth Factors**:
{generate_growth_factors_list(company_data, frontmatter['score_growth'])}

---

### LowPrep: {frontmatter['score_lowprep']:.1f}/15

**Estimated Preparation Time**: {frontmatter['prep_hours']} hours

**Breakdown**:
- Company Research: ~{estimate_company_research_hours(company_data)} hours
- Skills Development: ~{estimate_skills_hours(match_results)} hours
- Interview Preparation: ~{estimate_interview_hours(frontmatter['position_title'])} hours

**Assessment**: {assess_prep_difficulty(frontmatter['prep_hours'])}

---

### Stress: {frontmatter['score_stress']:.1f}/10

**Level**: {assess_stress_level(frontmatter['score_stress'])}

**Stress Factors**:
{generate_stress_factors_list(frontmatter['score_stress'])}

---

### Location: {frontmatter['score_location']:.1f}/5

**Office Location**: {frontmatter['location']}  
**Work Model**: {get_work_model_from_data()}

**Score Calculation**:
- Base Location: {get_location_base_name(frontmatter['location'])}
- Work Model Adjustment: {get_work_model_adjustment()}

---
"""
    
    return section
```

### Overall Assessment

```python
def generate_overall_assessment(frontmatter, scores, company_data, match_results):
    """
    Strategic analysis and fit evaluation
    """
    
    total_score = frontmatter['score_total']
    priority = scores['details']['priority']
    
    section = f"""## Overall Assessment

### Strategic Fit: {get_fit_category(total_score)}

{generate_fit_analysis(total_score, company_data, match_results)}

### Key Strengths

{generate_strengths_list(frontmatter, scores, company_data, match_results)}

### Key Concerns

{generate_concerns_list(frontmatter, scores, match_results)}

### Decision Framework

**If {priority} Priority:**
{generate_decision_guidance(priority, total_score, frontmatter)}

---
"""
    
    return section
```

### Company Context

```python
def generate_company_context(company_data):
    """
    Company profile summary section
    """
    
    section = f"""## Company Profile

**Quick Reference**: [Full Profile](../companies/{company_data['company_id']}.md)

### Key Facts

- **Company**: {company_data['company_name']}
- **Tier**: {company_data['tier']} ({company_data['tier_score']} points)
- **Industry**: {company_data.get('industry', 'Technology')}
- **Employees**: {company_data['employees_global']:,} global, {company_data['employees_israel']} in Israel

### Culture & Ratings

- **Glassdoor**: {company_data.get('glassdoor_rating', 'N/A')}/5.0 ⭐
- **Work-Life Balance**: {company_data.get('work_life_balance', 'N/A')}/5.0

### Technology

**Tech Stack**: {', '.join(company_data.get('tech_stack', ['See profile'])[:8])}

### Links

- **Website**: {company_data.get('website', 'N/A')}
- **Glassdoor**: {company_data.get('glassdoor_url', 'N/A')}
- **LinkedIn**: {company_data.get('linkedin_url', 'N/A')}

---
"""
    
    return section
```

### Preparation Roadmap

```python
def generate_preparation_roadmap(prep_strategy, match_results, company_data):
    """
    Detailed preparation plan with phases
    """
    
    section = f"""## Preparation Roadmap

**Total Estimated Time**: {prep_strategy['total_hours']} hours

### Phase 1: Foundation ({calculate_phase_hours(prep_strategy, 1)} hours)

**Objectives**: Company understanding + Critical gaps

**Tasks**:
1. **Company Deep Dive** (~{prep_strategy['breakdown']['company_research']} hours)
   - Read company website and recent news
   - Study products and technology
   - Review Glassdoor reviews
   - Find employees on LinkedIn

2. **Critical Skills** (~{prep_strategy['breakdown']['critical_skills']} hours)
{generate_critical_skills_tasks(match_results['critical_gaps'])}

3. **CV Optimization** (~2 hours)
   - Update {match_results['best_cv']} CV
   - Highlight relevant projects
   - Add quantifiable achievements

---

### Phase 2: Technical Depth ({calculate_phase_hours(prep_strategy, 2)} hours)

**Objectives**: Technical preparation + Role understanding

**Tasks**:
1. **High Priority Skills** (~{prep_strategy['breakdown'].get('high_priority_skills', 0)} hours)
{generate_high_priority_tasks(match_results.get('high_gaps', []))}

2. **Role Research** (~4 hours)
   - Study similar positions at {company_data['company_name']}
   - Understand team structure and challenges
   - Prepare role-specific scenarios

3. **Technical Brushup** (~4 hours)
   - Review strong match skills for confidence
   - Prepare technical examples
   - Practice explaining complex concepts

---

### Phase 3: Interview Excellence ({calculate_phase_hours(prep_strategy, 3)} hours)

**Objectives**: Interview practice + Final polish

**Tasks**:
1. **Mock Interviews** (~{prep_strategy['breakdown']['interview_prep']} hours)
   - Leadership scenarios
   - Technical problem-solving
   - Behavioral questions (STAR method)
   - Questions for interviewers

2. **Company-Specific Prep** (~4 hours)
   - Understand {company_data['company_name']}'s challenges
   - Prepare relevant examples
   - Research interviewers on LinkedIn

3. **Final Polish** (~2 hours)
   - Review all materials
   - Prepare opening/closing statements
   - Logistics check (location, time, documents)

---
"""
    
    return section
```

### Recommendation Section

```python
def generate_recommendation(frontmatter, scores, company_data, match_results):
    """
    Clear action-oriented recommendation
    """
    
    priority = scores['details']['priority']
    total_score = frontmatter['score_total']
    
    section = f"""## Recommendation

{generate_detailed_recommendation(priority, total_score, frontmatter, match_results, company_data)}

### Immediate Next Steps

{generate_next_steps(priority, frontmatter, match_results)}

### Timeline

{generate_timeline(priority, frontmatter['prep_hours'])}

---
"""
    
    return section
```

### Metadata Footer

```python
def generate_metadata_footer(frontmatter, company_data):
    """
    Document metadata and links
    """
    
    footer = f"""## Document Metadata

**Analysis Information**:
- **Role ID**: `{frontmatter['role_id']}`
- **Company ID**: `{company_data['company_id']}`
- **Analysis Date**: {frontmatter['date_analyzed']}
- **Status**: {frontmatter['status']}
- **Rank**: #{frontmatter['rank'] if frontmatter['rank'] else '?'} of {frontmatter['total_jobs'] if frontmatter['total_jobs'] else '?'}

**File Locations**:
- This Analysis: `jobs/analyzed/{frontmatter['role_id']}.md`
- Company Profile: `companies/{company_data['company_id']}.md`
- Excel Database: `db.xlsx`

**Links**:
- [Job Posting]({frontmatter['job_url']})
- [Company Profile](../companies/{company_data['company_id']}.md)
- [Database View](../db.xlsx)

---

*Generated by Israeli Tech Career Consultant v9.0*  
*YAML + Markdown Architecture*
"""
    
    return footer
```

---

## Complete Document Assembly

### Assemble Full Document

```python
def generate_complete_role_document(
    role_id,
    company_data,
    role_data,
    scores,
    match_results,
    prep_strategy
):
    """
    Generate complete YAML + Markdown document
    
    Args:
        role_id: Generated role ID
        company_data: Company frontmatter
        role_data: Job requirements
        scores: All calculated scores
        match_results: Skills matching results
        prep_strategy: Preparation strategy
    
    Returns:
        (complete_document, frontmatter_dict)
    """
    
    import yaml
    
    # Generate frontmatter
    frontmatter = generate_role_frontmatter(
        role_id=role_id,
        company_data=company_data,
        role_data=role_data,
        scores=scores,
        match_results=match_results,
        prep_strategy=prep_strategy
    )
    
    # Generate markdown sections
    markdown_parts = [
        generate_document_header(frontmatter, scores),
        generate_score_breakdown(frontmatter, scores, match_results, company_data),
        generate_overall_assessment(frontmatter, scores, company_data, match_results),
        generate_company_context(company_data),
        generate_preparation_roadmap(prep_strategy, match_results, company_data),
        generate_recommendation(frontmatter, scores, company_data, match_results),
        generate_metadata_footer(frontmatter, company_data)
    ]
    
    markdown_body = '\n'.join(markdown_parts)
    
    # Combine YAML + Markdown
    yaml_text = yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False
    )
    
    complete_document = f"---\n{yaml_text}---\n\n{markdown_body}"
    
    return complete_document, frontmatter
```

---

## Helper Functions for Content Generation

### Assessment Helpers

```python
def get_fit_category(total_score):
    """Categorize overall fit"""
    if total_score >= 80:
        return "Exceptional Match"
    elif total_score >= 70:
        return "Excellent Match"
    elif total_score >= 60:
        return "Strong Match"
    elif total_score >= 54:
        return "Good Match"
    else:
        return "Consider Carefully"


def assess_growth_level(score):
    """Growth potential description"""
    if score >= 16:
        return "Exceptional growth potential"
    elif score >= 12:
        return "Strong growth opportunities"
    elif score >= 8:
        return "Moderate growth potential"
    else:
        return "Limited growth trajectory"


def assess_stress_level(score):
    """Stress level description"""
    if score >= -5:
        return "Low to Moderate"
    elif score >= -7:
        return "Moderate"
    else:
        return "High Stress Environment"


def assess_prep_difficulty(hours):
    """Preparation difficulty assessment"""
    if hours <= 15:
        return "Light preparation - you're well-positioned"
    elif hours <= 30:
        return "Moderate preparation needed"
    elif hours <= 45:
        return "Substantial preparation required"
    else:
        return "Extensive preparation needed - consider timing carefully"
```

### List Generators

```python
def generate_strengths_list(frontmatter, scores, company_data, match_results):
    """Generate strengths bullet list"""
    
    strengths = []
    
    if frontmatter['score_match'] >= 25:
        strengths.append(f"✅ **Excellent technical fit** ({frontmatter['score_match']:.1f}/35)")
    
    if frontmatter['score_income'] >= 20:
        strengths.append(f"✅ **Strong compensation** (₪{frontmatter['income_estimate']:,}/month)")
    
    if frontmatter['score_growth'] >= 14:
        strengths.append(f"✅ **High growth potential** ({frontmatter['score_growth']:.1f}/20)")
    
    if frontmatter['score_lowprep'] >= 12:
        strengths.append(f"✅ **Quick ramp-up** ({frontmatter['prep_hours']} hours)")
    
    if company_data['tier'] <= 2:
        strengths.append(f"✅ **Top-tier company** (Tier {company_data['tier']})")
    
    if len(frontmatter['critical_gaps']) == 0:
        strengths.append("✅ **No critical skill gaps**")
    
    if not strengths:
        strengths.append("- Review individual components for details")
    
    return '\n'.join(strengths)


def generate_concerns_list(frontmatter, scores, match_results):
    """Generate concerns bullet list"""
    
    concerns = []
    
    if frontmatter['score_match'] < 20:
        concerns.append(f"⚠️ **Skill gaps present** ({len(frontmatter['critical_gaps'])} critical)")
    
    if frontmatter['score_income'] < 15:
        concerns.append("⚠️ **Below target compensation**")
    
    if frontmatter['score_stress'] <= -8:
        concerns.append("⚠️ **High-stress environment**")
    
    if frontmatter['score_location'] <= -5:
        concerns.append(f"⚠️ **Challenging location** ({frontmatter['location']})")
    
    if frontmatter['prep_hours'] >= 40:
        concerns.append(f"⚠️ **Extensive prep required** ({frontmatter['prep_hours']}h)")
    
    if not concerns:
        concerns.append("✅ **No major concerns identified**")
    
    return '\n'.join(concerns)


def generate_critical_skills_tasks(critical_gaps):
    """Generate critical skills prep tasks"""
    
    if not critical_gaps:
        return "   - No critical gaps identified ✅\n"
    
    tasks = []
    for gap in critical_gaps[:5]:  # Top 5
        tasks.append(f"   - Study {gap} (8 hours): online courses, documentation, practice")
    
    return '\n'.join(tasks)


def generate_next_steps(priority, frontmatter, match_results):
    """Generate next steps based on priority"""
    
    if priority == "First":
        steps = f"""
**Immediate Actions** (Within 48 hours):
1. ✅ Update {frontmatter['best_cv']} CV with latest achievements
2. 📧 Submit application through company website
3. 🔍 Research hiring manager on LinkedIn
4. 📚 Begin Phase 1 preparation

**This Week**:
5. Complete company research ({estimate_company_research_hours({'tier': 2})} hours)
6. Start addressing critical gaps
7. Reach out to employees for referral/insights
8. Prepare questions for interviewers
"""
    
    elif priority == "Second":
        steps = f"""
**Consider Carefully**:
1. Review against other opportunities
2. Assess if trade-offs are acceptable
3. If proceeding:
   - Update CV within 1 week
   - Begin company research
   - Allocate {frontmatter['prep_hours']} hours for prep
"""
    
    else:
        steps = """
**Recommended**:
1. ⏭️ Pass on this opportunity
2. Focus energy on higher-scoring positions
3. Note learnings for future searches
"""
    
    return steps
```

---

## Save Document

### Write to Filesystem

```python
def save_role_document(complete_document, role_id, db_paths):
    """
    Save complete document to roles directory
    
    Args:
        complete_document: Full YAML + Markdown string
        role_id: Role identifier
        db_paths: Database paths dict
    
    Returns:
        (success, file_path)
    """
    
    file_path = f"{db_paths['ROLES_DIR']}/{role_id}.md"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(complete_document)
        
        print(f"✅ Saved: jobs/analyzed/{role_id}.md")
        return True, file_path
    
    except Exception as e:
        print(f"❌ Failed to save document: {e}")
        return False, None
```

---

## Module Output

### Return Format

```python
{
    'success': True,
    'role_id': 'nvidia-engineering-manager-20251028',
    'file_path': '/path/to/jobs/analyzed/nvidia-engineering-manager-20251028.md',
    'frontmatter': {
        'role_id': '...',
        'score_total': 71.5,
        # ... all frontmatter fields
    },
    'document': '---\n...\n---\n\n# ...'  # Complete document
}
```

---

## Error Handling

### Safe Document Generation

```python
def safe_document_generation(generation_func, section_name):
    """
    Wrap document generation with error handling
    """
    
    try:
        return generation_func()
    except Exception as e:
        print(f"⚠️ Error generating {section_name}: {e}")
        return f"\n## {section_name}\n\n*Error generating this section - please review manually*\n\n"
```

---

## Module Interface

### Input Requirements

```python
{
    'role_id': str,
    'company_data': dict,      # Company frontmatter
    'role_data': dict,         # Job requirements
    'scores': dict,            # All calculated scores
    'match_results': dict,     # Skills matching results
    'prep_strategy': dict,     # Preparation strategy
    'db_paths': dict          # Database paths
}
```

### Output Format

```python
{
    'success': bool,
    'role_id': str,
    'file_path': str,
    'frontmatter': dict,
    'document': str
}
```

---

## Module Version

**Version**: v1.1.0  
**Architecture**: YAML frontmatter + Rich markdown  
**Dependencies**: pyyaml, user-config.yaml  
**Status**: Production Ready ✅

---

**Last Updated**: January 2025  
**Token Budget**: ~2K tokens  
**Output Quality**: Professional-grade analysis documents
