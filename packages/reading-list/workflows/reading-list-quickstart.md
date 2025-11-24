# Reading List Automation - Quick Start Guide

**Goal**: Capture and analyze your first article in 30 seconds  
**Prerequisites**: Configuration files + API keys

## Setup (One-Time - 5 minutes)

### Step 1: Create Directory Structure
```bash
mkdir -p ~/MyDrive/ReadingList/{config/prompts,articles,collections,summaries,exports/notebooklm}
```

### Step 2: Copy Configuration Files
```bash
cp ~/reading-list-config/settings.json ~/MyDrive/ReadingList/config/
cp ~/reading-list-config/sources.json ~/MyDrive/ReadingList/config/
cp ~/reading-list-config/prompts/* ~/MyDrive/ReadingList/config/prompts/
```

### Step 3: Add API Keys

**Edit**: `~/MyDrive/ReadingList/config/settings.json`

```json
{
  "integrations": {
    "firecrawl": {
      "enabled": true,
      "api_key": "YOUR_FIRECRAWL_KEY_HERE"
    },
    "bright_data": {
      "enabled": false,
      "api_key": "YOUR_BRIGHT_DATA_KEY"  // Optional
    }
  }
}
```

**Get API Keys**:
- Firecrawl: https://firecrawl.dev (required)
- Bright Data: https://brightdata.com (optional, for complex sites)

✅ **Setup Complete!**

---

## Your First Article (30 seconds)

### Example: Tech News Article

**You say to Claude:**
> "Can you capture this article for me?  
> https://techcrunch.com/2025/11/03/ai-startup-funding"

### What Happens:

**1. Scraping** (10 seconds)
- Firecrawl extracts clean content
- Removes ads, navigation, popups
- Preserves formatting and links

**2. Analysis** (15 seconds)
```markdown
# AI Startup Raises $50M Series B

**Author**: Sarah Mitchell  
**Source**: TechCrunch  
**Published**: 2025-11-01  
**Reading Time**: 5 minutes  
**Difficulty**: Intermediate

## Brief Summary (TL;DR)
Acme AI raised $50M Series B led by Sequoia to expand enterprise 
platform. 200+ customers, $20M ARR, 300% YoY growth.

## Key Points
- $50M Series B, Sequoia led, $250M valuation
- 200+ enterprise customers, $20M ARR
- Plans to double engineering (50→100)
- European market expansion focus
- New features for data privacy compliance

## Classification
**Topics**: ai-ml, startups, funding  
**Tags**: #series-b #enterprise-ai #sequoia #funding  
**Priority**: HIGH (Score: 85/100)  
**Relevance**: Strong match to your AI & startup interests

## NotebookLM
**Export**: NO  
**Reason**: Standard news article, appropriate length
```

**3. Saved**
```
~/MyDrive/ReadingList/articles/2025-11/ai-startup-funding.md
```

✅ **Article captured in 30 seconds!**

---

## Common Workflows

### 1. Single Article Capture
```
Provide URL → Scrape → Analyze → Save organized
```

### 2. Batch Processing (10 articles)
```
Provide CSV/list → Process all → Show summary → Organize by topic
Time: 2-5 minutes
```

### 3. Research Project
```
Capture 15+ articles → Create collection → Generate research report
Time: 10-15 minutes for capture + 5 minutes for report
```

### 4. Complex Article (>5,000 words)
```
Capture → Detect complexity → Suggest NotebookLM export
→ Format for deep analysis → Export bundle
```

---

## Real Examples

### Example 1: Israeli Tech Article
```
You: "https://calcalist.co.il/tech/article-123"

Claude: [Detects Hebrew]
        [Extracts content]
        [Analyzes]
        
Output:
- Topics: israeli-tech, startups
- Tags: #tel-aviv #israeli-startups #exit
- Priority: HIGH (matches your interests)
```

### Example 2: Academic Paper
```
You: "https://arxiv.org/paper/12345" (8,000 words)

Claude: [Processes]
        "This paper is 8,000 words and highly technical.
        
        📚 Export to NotebookLM?
        Benefits: Q&A, study guide, concept clarification
        
        [Export to NotebookLM]"
```

### Example 3: Batch Import
```
You: "Here are 25 URLs about AI transformation"
     [Upload CSV]

Claude: "Processing 25 articles..."
        
        Progress: [████████░░] 20/25
        
        ✓ 18 captured
        ✗ 2 paywalled (need Bright Data)
        ⏸ 5 queued
        
        Summary:
        - Topics: ai-ml (12), business (8), tech (5)
        - Priority: 6 HIGH, 12 MEDIUM, 2 LOW
        - 3 recommended for NotebookLM
```

---

## Research Report (Multiple Articles)

### When You Have 5+ Related Articles

**You say:**
> "Create a research report from my 'AI Transformation' collection"

**Claude generates**:
```markdown
# Research Report: AI Transformation in Enterprises

**Sources**: 12 articles analyzed  
**Citation Style**: APA

## Executive Summary
[200-word overview of findings across all sources]

## Key Themes
1. Leadership & Organizational Change [sources 1,3,4,6]
2. Data Infrastructure Requirements [sources 2,5,7]
3. Talent & Skills Development [sources 8,9,11]

## Comparative Analysis
[Table comparing approaches across sources]

## Key Findings
1. Executive sponsorship critical (67% success rate) [1,4,6]
2. Average transformation: 2-3 years [1,5,9]
3. 40-60% productivity gains reported [3,7,12]

## Research Gaps
- Limited mid-sized company data
- Lack of longitudinal studies
- Missing failure case analyses

## Recommendations
[Actionable insights with priorities]

## References
[Full APA citations]
```

**Time**: 5-10 minutes for 10-15 articles

---

## Customization

### Adjust Summary Detail
```json
{"analysis": {"summary_levels": ["brief", "standard", "detailed"]}}
```

### Change Priority Scoring
```json
{"organization": {
  "priority_scoring": {
    "factors": {
      "relevance": 0.5,     // Increase weight
      "recency": 0.3
    }
  }
}}
```

### Add Preferred Sources
Edit `~/MyDrive/ReadingList/config/sources.json`:
```json
{
  "preferred_sources": [
    {
      "name": "Your Favorite Blog",
      "domain": "example.com",
      "priority": "high",
      "auto_tag": ["your-tag"]
    }
  ]
}
```

---

## NotebookLM Workflow

### For Deep Analysis

**1. Capture Article(s)**
```
Claude: "📚 This 8,000-word paper is complex.
        Export to NotebookLM for:
        - Interactive Q&A
        - Study guide generation
        - Audio overview
        
        [Export Now]"
```

**2. Export Format**
```markdown
# Article Title

**Source**: URL  
**Summary**: Brief overview  
**Key Points**: Main insights  

## Full Content
[Clean article text]

## Suggested Research Questions
1. What are the main challenges discussed?
2. How does this compare to other approaches?
3. What are the practical implications?
```

**3. Use in NotebookLM**
- Upload exported file to notebooklm.google.com
- Ask questions, get audio overviews
- Generate study guides
- Find connections across sources

---

## Integration Setup

### Notion Database

**1. Create Database** (in Notion)
- Create new database
- Copy database ID from URL

**2. Configure**
```json
{
  "integrations": {
    "notion": {
      "enabled": true,
      "database_id": "your-database-id",
      "sync_frequency": "immediate"
    }
  }
}
```

**3. Use**
```
Claude automatically syncs each captured article to Notion
with: Title, URL, Summary, Topics, Tags, Priority
```

### Apple Notes

```json
{"integrations": {"apple_notes": {"enabled": true, "notebook": "Reading List"}}}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Scraping failed | Enable Bright Data fallback |
| Paywall blocking | Use Bright Data or copy/paste content |
| Wrong topics | Customize taxonomy in sources.json |
| Too many tags | Adjust max_tags in settings |
| Low priority score | Update user interests in config |

---

## Success Tips

### 🌐 Choosing Sources
- Mix academic + industry + news
- Include diverse perspectives
- Check quality_score in sources.json
- Add your favorite sites to preferred_sources

### 📊 Building Collections
- Group by theme, not just topic
- Aim for 5-15 articles per collection
- Include foundational + recent sources
- Mix difficulty levels (beginner to advanced)

### 🎯 Priority Management
- Review HIGH priority articles first
- Batch process MEDIUM priority weekly
- Archive or delete LOW priority
- Refine interests in config over time

### 📝 Research Reports
- Minimum 5 sources for solid report
- Include diverse viewpoints
- Choose citation style (APA recommended)
- Export to PDF for formal presentation

---

## Quick Commands

```
"Capture this article: [URL]"
"Process these 10 URLs: [list]"
"Create research report from AI collection"
"Export this to NotebookLM"
"Show my HIGH priority articles"
"What topics am I reading most?"
```

---

## Next Steps

✅ **You've captured your first article!**

**What to try next:**
1. **Batch Process**: Try 10 URLs at once
2. **Build Collection**: Gather 5+ articles on a topic
3. **Research Report**: Synthesize your collection
4. **NotebookLM**: Deep-dive a complex article
5. **Integrations**: Connect Notion or Apple Notes

**Resources:**
- Full guide: `~/reading-list-config/CONFIG-GUIDE.md`
- Skill docs: `~/skills/reading-list-capture/SKILL.md`
- Research skill: `~/skills/reading-list-research/SKILL.md`

---

**Time to First Article**: 30 seconds  
**Setup**: 5 minutes (one-time)  
**Batch (10 articles)**: 2-5 minutes  
**Research Report**: 5-10 minutes

🎉 **Happy reading and researching!**
