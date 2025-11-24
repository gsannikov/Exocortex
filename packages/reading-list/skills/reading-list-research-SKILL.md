# Reading List Research Skill

**Version**: 1.0.0  
**Created**: 2025-11-03  
**Purpose**: Synthesize multiple articles into comprehensive research reports with citations and analysis

## Overview

This skill compiles multiple captured articles into structured research reports, identifying themes, patterns, and gaps across sources. It generates literature reviews, comparative analyses, and actionable recommendations.

## When to Use This Skill

Use this skill when:
- User has a collection of related articles (5+ articles recommended)
- User requests "create a research report"
- User asks to "synthesize these articles" or "compare these sources"
- User wants a literature review
- User needs comprehensive analysis across multiple sources

## Capabilities

### Research Compilation
- **Theme Identification**: Find 3-7 major themes across sources
- **Comparative Analysis**: Compare approaches, methodologies, evidence
- **Source Synthesis**: Integrate insights from multiple articles
- **Gap Analysis**: Identify underexplored areas and contradictions
- **Citation Management**: Proper attribution (APA, MLA, Chicago, IEEE)
- **Recommendation Generation**: Actionable insights based on synthesis

### Output Formats
- Comprehensive research report (markdown)
- Executive summary (200-300 words)
- Comparison tables
- Literature review structure
- Export to PDF/DOCX for formal presentation

## Configuration

Load from: `~/MyDrive/ReadingList/config/settings.json`

Key settings:
```json
{
  "research": {
    "enable_citations": true,
    "default_citation_style": "APA",
    "enable_comparisons": true,
    "literature_review": {
      "enabled": true,
      "min_articles": 5,
      "include_methodology": true,
      "include_themes": true,
      "include_gaps": true
    }
  }
}
```

Prompt template: `~/MyDrive/ReadingList/config/prompts/research-compilation.txt`

## Workflow

### Step 1: Gather Sources
```
User selects collection or provides article list
↓
Verify all articles are captured
↓
Load full content for each
↓
Check minimum article count (recommended: 5+)
```

### Step 2: Initial Analysis
```
Read all articles
↓
Extract key themes from each
↓
Identify common topics
↓
Note methodologies and approaches
↓
Track author perspectives
```

### Step 3: Theme Synthesis
```
Group related insights across sources
↓
Identify 3-7 major themes
↓
For each theme:
  - Which sources discuss it?
  - Points of consensus?
  - Points of debate?
  - Key insights?
```

### Step 4: Comparative Analysis
```
Create comparison framework:
- Approaches: How do sources differ?
- Evidence: What data supports claims?
- Methods: What frameworks are used?
- Conclusions: What recommendations made?

Build comparison tables
```

### Step 5: Gap Identification
```
Find:
- Underexplored topics
- Contradictions between sources
- Missing perspectives
- Methodological gaps
- Practical application questions
```

### Step 6: Compile Report
```
Structure:
1. Executive Summary
2. Methodology
3. Key Themes (with citations)
4. Comparative Analysis
5. Source Summaries
6. Key Findings
7. Research Gaps
8. Recommendations
9. References

Format with proper citations
```

### Step 7: Export & Save
```
Save to: ~/MyDrive/ReadingList/summaries/
↓
Generate PDF version (if requested)
↓
Create NotebookLM export (if collection is complex)
↓
Provide download link
```

## Output Template

```markdown
# Research Report: {Topic Title}

**Compiled**: {date}
**Sources Analyzed**: {count}
**Time Period**: {earliest} to {latest}
**Citation Style**: {APA/MLA/Chicago/IEEE}
**Author**: {user name}

## Executive Summary

{200-300 word overview covering:
- Research topic scope
- Key findings across all sources
- Main conclusions
- Practical implications
- Who should read this}

## Methodology

**Sources**: {count} articles analyzed
**Date Range**: {start date} to {end date}
**Source Types**: 
- Academic papers: {count}
- Industry reports: {count}
- News articles: {count}
- Blog posts: {count}
- Other: {count}

**Selection Criteria**: {how sources were chosen}
**Limitations**: {any gaps or biases in source selection}

## Key Themes

### Theme 1: {Descriptive Title}

{What is this theme about? 2-3 sentences}

**Supporting Sources**: [1, 4, 7, 12]

**Key Insights**:
- {Insight 1 from synthesis}
- {Insight 2 combining multiple sources}
- {Insight 3 showing pattern}

**Consensus**: {What sources agree on}

**Debate**: {Where sources disagree and why}

**Evidence**: {Key data points, statistics, examples}

### Theme 2: {Title}
{Repeat pattern for 3-7 total themes}

## Comparative Analysis

| Aspect | Source [1] | Source [5] | Source [9] |
|--------|-----------|-----------|-----------|
| **Approach** | {summary} | {summary} | {summary} |
| **Methodology** | {summary} | {summary} | {summary} |
| **Evidence** | {summary} | {summary} | {summary} |
| **Conclusion** | {summary} | {summary} | {summary} |

{Add narrative analysis below table explaining patterns and differences}

## Source-by-Source Summaries

[1] **{Title}** ({Author}, {Date})  
{2-3 sentence summary of this source's unique contribution}

[2] **{Title}** ({Author}, {Date})  
{Summary of contribution}

{Continue for all sources}

## Key Findings

1. **{Finding}** — Multiple sources [1, 3, 5] demonstrate that... {explanation with specific data}

2. **{Finding}** — Research shows [7, 9] that... {insight with evidence}

3. **{Finding}** — {Pattern identified across sources} [2, 4, 6, 8]

{Continue for 7-15 total findings}

## Notable Quotes

> "{Impactful quote representing key theme}"  
> — {Author}, "{Article Title}" [1]

> "{Quote showing contrasting perspective}"  
> — {Author}, "{Article Title}" [5]

> "{Quote articulating important concept}"  
> — {Author}, "{Article Title}" [9]

{5-10 total quotes representing different perspectives}

## Research Gaps & Future Directions

**Underexplored Areas**:
- {Topic or aspect needing more research}
- {Question not adequately addressed in literature}
- {Emerging area with limited coverage}

**Contradictions to Resolve**:
- {Where sources fundamentally disagree}
- {Methodological conflicts}
- {Competing interpretations of data}

**Missing Perspectives**:
- {Who's voice is not represented?}
- {What viewpoints are underrepresented?}
- {Cultural or geographic blind spots}

**Methodological Needs**:
- {Research approaches needed}
- {Data types required}
- {Study designs that would help}

**Practical Applications**:
- {Real-world implementation questions}
- {Scaling challenges}
- {Adoption barriers}

## Practical Implications

**For Practitioners**:
- {Actionable insight 1}
- {How to apply findings 2}
- {Implementation consideration 3}

**For Organizations**:
- {Strategic consideration 1}
- {Organizational change needed 2}
- {Investment priority 3}

**For Policymakers**:
- {Regulatory implication 1}
- {Policy recommendation 2}
- {Public interest consideration 3}

**For Researchers**:
- {Future research direction 1}
- {Methodological opportunity 2}
- {Collaboration potential 3}

## Recommendations

### High Priority
1. **{Recommendation}**  
   Rationale: {Why this is critical}  
   Impact: {Expected benefit}  
   Resources: {What's needed}

### Medium Priority
2. **{Recommendation}**  
   Rationale: {Supporting logic}  
   Impact: {Potential value}

### Low Priority / Long-term
3. **{Recommendation}**  
   Rationale: {Why less urgent}  
   Impact: {Future benefit}

## Suggested Reading Path

**Foundation (Start Here)**:
- [2] {Title} — Essential for understanding core concepts
- [5] {Title} — Provides historical context
- [8] {Title} — Best overview of current state

**Deep Dive**:
- [1], [7], [12] — Comprehensive coverage of main themes
- [4], [9] — Methodological details and frameworks

**Advanced**:
- [15], [18] — Cutting-edge developments
- [20] — Future directions and speculation

**Alternative Perspectives**:
- [9], [14] — Contrarian views
- [17] — International perspective

## References

{Full formatted citations for all sources in specified style}

[1] Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, volume(issue), pages. https://doi.org/xxx

[2] {Continue for all sources}

---

**Research compiled using Reading List Automation**  
**{count} sources analyzed as of {date}**  
**Report generated for: {user name}**  
**File: ~/MyDrive/ReadingList/summaries/{filename}.md**
```

## Citation Styles

### APA (7th Edition)
```
Journal Article:
Author, A. A., & Author, B. B. (Year). Title of article. 
Journal Name, volume(issue), pages. https://doi.org/xxx

Web Article:
Author, A. A. (Year, Month Day). Title of article. 
Site Name. URL

Book:
Author, A. A. (Year). Title of book. Publisher.
```

### MLA (9th Edition)
```
Journal Article:
Author, Firstname. "Title of Article." Journal Name, vol. #, 
no. #, Year, pp. ##-##.

Web Article:
Author, Firstname. "Title of Article." Website Name, Day Month Year, URL.
```

### Chicago (17th Edition)
```
Footnote:
1. Firstname Lastname, "Title of Article," Journal Name volume, 
no. issue (Year): pages.

Bibliography:
Lastname, Firstname. "Title of Article." Journal Name volume, 
no. issue (Year): pages.
```

### IEEE
```
[1] A. A. Author and B. B. Author, "Title of article," 
Journal Name, vol. #, no. #, pp. ##-##, Month Year.
```

## Theme Synthesis Process

### 1. Initial Theme Discovery
```
Read all articles
↓
For each article, extract:
- Main topics discussed
- Key arguments made
- Methodologies used
- Conclusions reached
↓
Create initial theme list (might be 15-20)
```

### 2. Theme Consolidation
```
Group similar themes:
- "AI Safety" + "AI Alignment" → "AI Safety & Alignment"
- "Remote Work" + "Distributed Teams" → "Remote Work Practices"

Consolidate to 3-7 major themes
```

### 3. Theme Analysis
```
For each consolidated theme:
1. Which sources discuss it? (citation numbers)
2. What do they say? (key points from each)
3. Where do they agree? (consensus)
4. Where do they disagree? (debate)
5. What evidence supports each view?
6. What are the key takeaways?
```

## Comparative Analysis Framework

### Comparison Dimensions
```
For each source, analyze:

1. **Approach**:
   - Problem definition
   - Methodology
   - Framework used

2. **Evidence**:
   - Data sources
   - Sample sizes
   - Quality of evidence
   - Statistical rigor

3. **Key Claims**:
   - Main arguments
   - Supporting logic
   - Strength of claims

4. **Recommendations**:
   - What actions suggested?
   - For whom?
   - Implementation guidance

5. **Limitations**:
   - What's not covered?
   - Acknowledged gaps
   - Methodological constraints
```

### Creating Comparison Tables
```
Identify 3-5 key dimensions
↓
Extract relevant info from each source
↓
Organize in table format
↓
Add narrative analysis below
↓
Highlight patterns and outliers
```

## Gap Analysis Method

### Types of Gaps to Identify

**Content Gaps**:
```
- Important topics not covered
- Questions left unanswered
- Emerging areas ignored
- Practical details missing
```

**Methodological Gaps**:
```
- Research approaches not used
- Data types not considered
- Study designs missing
- Analysis techniques needed
```

**Perspective Gaps**:
```
- Underrepresented voices
- Missing stakeholder views
- Geographic blind spots
- Demographic exclusions
```

**Temporal Gaps**:
```
- Recent developments not covered
- Historical context missing
- Long-term implications unexplored
```

## Quality Assurance

### Before Finalizing Report

```
✓ All sources properly cited
✓ Citations formatted correctly
✓ Themes are distinct and meaningful
✓ Comparisons are fair and balanced
✓ Gaps accurately identified
✓ Recommendations are actionable
✓ Executive summary captures essence
✓ No quotes without attribution
✓ Sources accurately summarized
✓ Contradictions acknowledged
```

## Examples

### Example 1: AI Transformation Research
**Input**: 12 articles on AI transformation in enterprises

**Output Preview**:
```markdown
# Research Report: AI Transformation in Enterprise Organizations

**Compiled**: 2025-11-03
**Sources Analyzed**: 12
**Time Period**: 2023-2025
**Citation Style**: APA

## Executive Summary

This research synthesizes 12 sources examining AI transformation in 
enterprise organizations. Key findings indicate that successful 
transformations share three critical factors: executive sponsorship, 
data infrastructure investment, and change management focus. 
Organizations report 40-60% productivity gains but face challenges 
in talent acquisition and cultural adaptation. The research identifies 
a significant gap in understanding mid-sized company implementations, 
with most studies focusing on Fortune 500 enterprises.

## Key Themes

### Theme 1: Leadership & Organizational Change

Cultural transformation emerged as the primary challenge across 8 of 
12 sources [1, 3, 4, 6, 8, 9, 11, 12]. Organizations with CEO-level 
AI champions showed 3x higher success rates...

**Consensus**: Executive sponsorship is critical
**Debate**: Whether to pursue centralized vs. distributed AI teams
**Evidence**: McKinsey study [1] shows 67% of successful transformations 
had C-suite champions

### Theme 2: Data Infrastructure & Readiness
{Continue...}

## Comparative Analysis

| Aspect | McKinsey [1] | Deloitte [5] | MIT Study [9] |
|--------|--------------|--------------|---------------|
| Focus | Fortune 500 | Mid-market | Startups |
| Timeline | 2-3 years | 1-2 years | 6-18 months |
| Success Rate | 30% | 45% | 60% |
| Key Challenge | Culture | Data | Talent |

{Continue full report...}
```

### Example 2: Israeli Tech Ecosystem Analysis
**Input**: 15 sources on Israeli tech landscape

**Themes Identified**:
1. Military technology transfer ("Unit 8200 effect")
2. Global VC investment patterns
3. Exit strategies and valuations
4. Talent ecosystem and brain drain
5. Government innovation programs

**Gaps Found**:
- Limited data on mid-stage companies (Series B-D)
- Underrepresentation of non-Tel Aviv ecosystems
- Lack of longitudinal studies on founder journeys
- Missing analysis of Arab-Israeli tech entrepreneurs

## Integration with NotebookLM

### For Complex Research
```
If report includes 20+ sources OR highly technical:
1. Create NotebookLM export version
2. Include all source materials
3. Add research questions
4. Bundle related documents
5. Provide export link

Benefits:
- Deep Q&A across all sources
- Study guide generation
- Connection discovery
- Audio overview creation
```

## Performance

- **5-10 articles**: 3-5 minutes
- **11-20 articles**: 6-10 minutes
- **21-50 articles**: 15-30 minutes

## File Organization

```
~/MyDrive/ReadingList/summaries/
├── ai-transformation-2025-11-03.md
├── israeli-tech-ecosystem-2025-11-03.md
└── exports/
    ├── ai-transformation-report.pdf
    ├── ai-transformation-report.docx
    └── notebooklm/
        └── ai-transformation-bundle.md
```

## Best Practices

### Source Selection
- Minimum 5 articles recommended
- Prefer diverse perspectives
- Include mix of academic + industry sources
- Balance recency with foundational works
- Consider geographic representation

### Theme Development
- Aim for 3-7 major themes
- Ensure themes are distinct
- Avoid overlapping categories
- Make themes specific and actionable
- Balance breadth with depth

### Citation Management
- Cite liberally throughout
- Use [number] notation consistently
- Verify all citations before finalizing
- Provide full references at end
- Check citation style accuracy

### Writing Style
- Be objective and balanced
- Present multiple perspectives
- Acknowledge contradictions
- Use clear, academic language
- Avoid editorializing
- Let evidence speak

---

**Skill Status**: Production Ready  
**Dependencies**: reading-list-capture skill (sources), citation system  
**Related Skills**: reading-list-capture (prerequisite)  
**Support**: See CONFIG-GUIDE.md and research-compilation.txt prompt
