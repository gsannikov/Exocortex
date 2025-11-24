# Reading List Capture Skill

**Version**: 1.0.0  
**Created**: 2025-11-03  
**Purpose**: Capture, extract, and analyze web articles with AI-powered summarization and organization

## Overview

This skill enables Claude to capture web articles, extract clean content, generate multi-level summaries, and organize content into a searchable knowledge base. It handles URLs, PDFs, and batch processing with intelligent categorization.

## When to Use This Skill

Use this skill when:
- User provides a URL to capture
- User says "save this article" or "add to reading list"
- User uploads a list of URLs (batch processing)
- User mentions "capture this content" or "process this webpage"
- User wants to build a personal knowledge base

## Capabilities

### Content Capture
- **Web Scraping**: Clean extraction from any website (Firecrawl + Bright Data)
- **Batch Processing**: Handle multiple URLs simultaneously (up to 50)
- **PDF Extraction**: Process PDF articles and documents
- **Video Transcripts**: Extract YouTube/Vimeo transcripts
- **Metadata Capture**: Author, date, source, reading time

### Analysis & Organization
- **Multi-Level Summaries**: Brief (TL;DR), Standard, Detailed
- **Key Points Extraction**: 5-7 main insights
- **Notable Quotes**: Memorable excerpts with attribution
- **Topic Classification**: Auto-assign to topic taxonomy
- **Smart Tagging**: Generate 5-10 relevant tags
- **Priority Scoring**: Relevance to user interests
- **Related Articles**: Suggest connections to existing content

### NotebookLM Integration
- **Complexity Detection**: Auto-suggest for >5,000 word articles
- **Export Preparation**: Format for deep analysis
- **Collection Bundling**: Group related articles
- **Research Questions**: Generate suggested questions

## Configuration

Load settings from:
- Main: `~/MyDrive/ReadingList/config/settings.json`
- Sources: `~/MyDrive/ReadingList/config/sources.json`
- Prompt: `~/MyDrive/ReadingList/config/prompts/article-analysis.txt`

Key config sections:
```json
{
  "capture": {
    "default_scraper": "firecrawl",
    "fallback_scraper": "bright_data"
  },
  "analysis": {
    "generate_summary": true,
    "summary_levels": ["brief", "standard"],
    "extract_key_points": true,
    "extract_quotes": true
  },
  "notebooklm": {
    "enabled": true,
    "auto_suggest_threshold": {
      "word_count": 5000,
      "technical_score": 0.7
    }
  }
}
```

## Workflow

### Step 1: Receive URL(s)
```
User provides URL or list
↓
Validate URL format
↓
Check if already captured
↓
Load configuration
```

### Step 2: Scrape Content
```
Try Firecrawl first (primary)
↓
If fails: Use Bright Data (fallback)
↓
Extract clean HTML/markdown
↓
Remove ads, navigation, popups
↓
Preserve formatting and links
```

### Step 3: Extract Metadata
```
Capture:
- Title, Author, Published Date
- Site name, Domain
- Word count, Reading time
- Language, Content type
- Description, Keywords
```

### Step 4: Analyze Content
```
Generate summaries (Brief + Standard)
↓
Extract 5-7 key points
↓
Find 3-5 notable quotes
↓
Identify entities (people, orgs, stats)
↓
Assess difficulty level
↓
Estimate reading time
```

### Step 5: Classify & Organize
```
Assign 2-4 topics from taxonomy
↓
Generate 5-10 tags
↓
Calculate priority score
↓
Find related articles
↓
Assess NotebookLM need
```

### Step 6: Save & Output
```
Save to: ~/MyDrive/ReadingList/articles/YYYY-MM/
↓
Update search index
↓
Sync to integrations (if enabled)
↓
Provide user with summary
```

## Output Template

```markdown
# {Article Title}

## Metadata
**Author**: {author}
**Source**: {source/domain}
**Published**: {date}
**URL**: {url}
**Word Count**: {count}
**Reading Time**: {minutes} minutes
**Language**: {language}
**Content Type**: {type}
**Difficulty**: {Beginner/Intermediate/Advanced/Academic}

## Brief Summary
{2-3 sentence TL;DR capturing core message}

## Standard Summary
{Comprehensive 250-300 word summary with main arguments, 
evidence, conclusions, and context. Why does this matter?}

## Key Points
- {Specific insight or finding with data if available}
- {Main argument or perspective}
- {Notable conclusion or recommendation}
- {Supporting evidence or example}
- {Unique perspective or novel idea}
- {Practical implication or application}
- {Future direction or open question}

## Notable Quotes
> "{Impactful quote that captures essence}"
> — {Author/Source}

> "{Quote providing unique insight}"
> — {Attribution}

> "{Memorable excerpt}"
> — {Source}

## Entities & Facts
**People**: {experts, subjects mentioned}
**Organizations**: {companies, institutions}
**Key Statistics**: {numbers, percentages, data}
**Technologies**: {tools, platforms, methods}

## Classification
**Topics**: {topic1}, {topic2}, {topic3}
**Tags**: #{tag1}, #{tag2}, #{tag3}, #{tag4}, #{tag5}
**Tone**: {Professional/Academic/Casual/Technical/Balanced}

## Priority Assessment
**Relevance Score**: {score}/10
**Overall Priority**: {HIGH/MEDIUM/LOW}
**Reasoning**: {Brief explanation based on user interests}

## Related Concepts
- {Related topic or concept for follow-up}
- {Connected theme or area}
- {Complementary perspective}

## NotebookLM Recommendation
**Export to NotebookLM**: {YES/NO/MAYBE}
**Reason**: {Word count >5,000 / Highly technical / Part of research project / etc.}
{If YES: Provide export button/link}

## Full Article
{Clean article content in markdown}

---
*Captured on {date} via Reading List Automation*
*File: ~/MyDrive/ReadingList/articles/{YYYY-MM}/{slug}.md*
```

## Scraping Strategy

### Primary: Firecrawl
```
Best for: Most websites, clean extraction
Advantages:
- Fast processing
- Clean markdown output
- Good ad removal
- Preserves formatting
- Reliable for 95% of sites

Use for: Standard articles, blogs, news sites
```

### Fallback: Bright Data
```
Best for: Complex sites, paywalled content, LinkedIn
Advantages:
- Handles JavaScript-heavy sites
- Bypasses paywalls
- Works with LinkedIn
- More robust

Use for:
- When Firecrawl fails
- Paywalled articles (if configured)
- LinkedIn posts
- Complex dynamic sites
```

### Decision Logic
```
1. Try Firecrawl first
2. If status != 200 or content_length < 500:
   → Try Bright Data
3. If both fail:
   → Save URL to failed queue
   → Notify user
   → Suggest manual copy/paste
```

## Priority Scoring Algorithm

```
Factors (weighted):
1. Relevance to user interests (40%)
   - Match against user.interests in config
   - Match against historical reading patterns
   - Match against recent searches

2. Recency (20%)
   - Published in last week: +8 points
   - Published in last month: +6 points
   - Published in last 3 months: +4 points
   - Published in last year: +2 points
   - Older: +0 points

3. Source authority (20%)
   - Match against preferred_sources in config
   - Check quality_score of source
   - High-quality sources (0.85+): +8 points
   - Medium quality (0.70-0.84): +5 points
   - Unknown/low quality: +2 points

4. Depth/comprehensiveness (10%)
   - Word count >3,000: +10 points
   - Word count 1,500-3,000: +7 points
   - Word count 800-1,500: +5 points
   - Word count <800: +3 points

5. Actionability (10%)
   - How-to/tutorial: +10 points
   - Case study with examples: +8 points
   - Analysis with insights: +6 points
   - Pure news/announcement: +3 points

Final score: Sum of weighted factors (0-100)
Priority:
- HIGH: Score >70
- MEDIUM: Score 40-70
- LOW: Score <40
```

## Topic Classification

Load taxonomy from `sources.json`:
```json
{
  "topic_taxonomy": {
    "technology": ["ai", "ml", "blockchain", "cloud", "saas"],
    "business": ["strategy", "management", "leadership"],
    "career": ["job-search", "interview", "promotion"],
    "startups": ["funding", "growth", "product-market-fit"],
    "ai-ml": ["llm", "deep-learning", "computer-vision"],
    "israeli-tech": ["tel-aviv", "startup-nation", "exit"]
  }
}
```

### Classification Logic
```
1. Extract keywords from title + first 3 paragraphs
2. Match against taxonomy keywords
3. Calculate confidence scores
4. Assign top 2-4 topics (confidence >0.7)
5. If no match: Assign "general" or ask user
```

## Tag Generation

### Smart Tagging Rules
```
Sources:
1. Keywords from title (highest weight)
2. Technical terms in content
3. Entity names (people, orgs)
4. Domain-specific vocabulary
5. Author-provided keywords

Filters:
- Remove common words (blacklist)
- Remove very rare words (<2 occurrences)
- Prefer nouns and noun phrases
- Maximum 10 tags
- Minimum confidence: 0.65

Format: Lowercase, hyphenated, descriptive
Examples: #ai-transformation, #israeli-startups, #product-management
```

## NotebookLM Assessment

### Auto-Suggest Criteria
```
Suggest NotebookLM if ANY:
1. Word count >5,000
2. Technical/academic difficulty level
3. Part of collection with 5+ articles
4. Complex topic (multiple subtopics)
5. Contains dense data/statistics
6. Research paper or academic content
7. User manually marks "deep study"
```

### Export Format
```
If recommended:
1. Format article for NotebookLM
2. Include metadata and summary
3. Add to exports/notebooklm/ folder
4. Provide one-click export button
5. Generate research questions

File name: {date}-{slug}-notebooklm.md
```

## Batch Processing

### When User Provides Multiple URLs
```
If URL count 2-10:
- Process each sequentially
- Show progress indicator
- Provide summary at end

If URL count 11-50:
- Enable parallel processing (if configured)
- Batch into groups of 10
- Show live progress
- Report failures separately

If URL count >50:
- Warn about processing time
- Offer to process first 50
- Suggest breaking into multiple sessions
```

### CSV Import
```
User provides CSV with columns:
- url (required)
- title (optional)
- priority (optional)
- collection (optional)

Process:
1. Validate CSV format
2. Preview first 5 entries
3. Confirm with user
4. Process batch
5. Save to specified collection
```

## Integration Actions

### Notion Sync (if enabled)
```
Create database entry:
- Title, URL, Author, Date
- Status: "To Read"
- Priority: from calculation
- Topics: as multi-select
- Tags: as multi-select
- Summary: text field
- Key Points: text field
- File Path: link to markdown
```

### Apple Notes (if enabled)
```
Create note in configured notebook:
- Title from article
- Brief summary
- Link to full markdown
- Tags for organization
```

### Email Digest (if enabled)
```
If configured for weekly digest:
- Add to digest queue
- Include: Title, source, brief summary
- Sort by priority
- Send on configured day/time
```

## Error Handling

### URL Errors
```
Invalid URL:
→ Suggest correct format
→ Try to auto-correct common mistakes

Dead link (404):
→ Notify user
→ Suggest Internet Archive lookup
→ Save URL to failed queue

Paywall (no Bright Data):
→ Extract preview/excerpt
→ Note paywall encountered
→ Suggest: Subscribe or enable Bright Data
```

### Content Extraction Failures
```
If extracted content <500 chars:
→ Retry with fallback scraper
→ If still fails: Ask user to copy/paste
→ Save URL for manual processing

If content is garbled:
→ Check encoding
→ Try alternate extraction method
→ Report issue to user
```

### API Failures
```
Firecrawl API down:
→ Switch to Bright Data immediately
→ Log for later analysis

Bright Data API down:
→ Queue for retry later
→ Notify user of delay
→ Offer manual copy/paste option
```

## Examples

### Example 1: Tech Article
**Input**: https://techcrunch.com/ai-startup-raises-50m

**Output**:
```markdown
# AI Startup Raises $50M Series B for Enterprise Platform

## Metadata
**Author**: Sarah Mitchell
**Source**: TechCrunch
**Published**: 2025-11-01
**Word Count**: 1,247
**Reading Time**: 5 minutes
**Difficulty**: Intermediate

## Brief Summary
Acme AI raised $50M Series B led by Sequoia to expand its enterprise 
AI platform. The funding will support product development and go-to-market 
expansion. Company has 200+ enterprise customers and $20M ARR.

## Key Points
- $50M Series B funding led by Sequoia Capital
- Post-money valuation: $250M (2.5x from Series A)
- 200+ enterprise customers including Fortune 500 companies
- Current ARR: $20M, growing 300% YoY
- Plans to double engineering team from 50 to 100
- Focus on expanding into European market
- New product features for data privacy and compliance

## Classification
**Topics**: ai-ml, startups, funding
**Tags**: #series-b, #enterprise-ai, #sequoia, #funding, #saas
**Priority**: HIGH (Score: 85/100)

## NotebookLM Recommendation
**Export to NotebookLM**: NO
**Reason**: Standard news article, appropriate length, straightforward content
```

### Example 2: Academic Paper
**Input**: https://arxiv.org/paper123 (8,000 words)

**Output**:
```markdown
# Novel Approach to Transformer Architecture Optimization

## Metadata
**Authors**: Chen et al.
**Source**: arXiv
**Published**: 2025-10-28
**Word Count**: 8,247
**Reading Time**: 33 minutes
**Difficulty**: Academic

## Brief Summary
Researchers propose new method for optimizing transformer architectures, 
achieving 40% reduction in training time while maintaining accuracy. 
Technique involves dynamic layer pruning and adaptive attention mechanisms.

[... full analysis ...]

## NotebookLM Recommendation
**Export to NotebookLM**: YES
**Reason**: Academic paper (8,247 words), highly technical, dense with 
mathematical concepts and experimental results. NotebookLM can help with:
- Q&A about methodology
- Study guide generation
- Concept clarification
- Connection to related papers

[Export to NotebookLM] ← button/link
```

### Example 3: Batch Processing
**Input**: CSV with 25 URLs

**Process**:
```
Processing 25 articles...

Progress: [████████░░] 20/25 complete

✓ 18 successfully captured
✗ 2 failed (paywalled)
⏸ 5 queued (rate limiting)

Summary:
- Average reading time: 8.5 minutes
- Topics: ai-ml (8), business (6), career (4), tech (7)
- Priority: 6 HIGH, 12 MEDIUM, 2 LOW
- 3 recommended for NotebookLM export

View captured articles: ~/MyDrive/ReadingList/articles/2025-11/
```

## Performance Benchmarks

- **Single article**: 15-30 seconds
- **Batch (10 articles)**: 2-5 minutes
- **Success rate**: 95%+ with fallback
- **Accuracy**: 90%+ topic classification

## Quality Checks

```
Before saving, verify:
✓ Title extracted (not URL)
✓ Content >500 words
✓ At least 1 topic assigned
✓ At least 3 tags generated
✓ Summary is coherent
✓ Quotes properly attributed

If any fail: Flag for manual review
```

## File Organization

```
~/MyDrive/ReadingList/
├── articles/
│   └── 2025-11/
│       ├── ai-startup-funding.md
│       ├── transformer-optimization.md
│       └── ...
├── collections/
│   └── ai-research.md (links to related articles)
├── exports/
│   └── notebooklm/
│       └── transformer-optimization-notebooklm.md
└── config/
    ├── settings.json
    └── sources.json
```

---

**Skill Status**: Production Ready  
**Dependencies**: Firecrawl API, Bright Data API (optional), filesystem access  
**Related Skills**: reading-list-research (for multi-article analysis)  
**Support**: See CONFIG-GUIDE.md for API setup and configuration
