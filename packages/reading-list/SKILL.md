---
name: reading-list
description: Capture articles via Apple Notes inbox. Auto-scrape, summarize, categorize, and track reading progress. Commands - "process reading list", "show unread", "summarize [topic]".
---

# 📚 Reading List Automation

Capture → Scrape → Summarize → Organize

## 🌟 Key Capabilities
1. **Apple Notes Inbox**: Paste URLs to "📚 Reading List Inbox" note
2. **Auto-Scraping**: Firecrawl/web_fetch for full content
3. **AI Summarization**: 150-word summaries with key takeaways
4. **Smart Categorization**: Tech, AI, Business, Career, Finance, Science, Other
5. **Progress Tracking**: unread → reading → done → archived

## ⚙️ Storage Configuration

**User Data Location**: `~/MyDrive/claude-skills-data/reading-list/`

```
reading-list/
├── reading-list.yaml     # Main database
├── summaries/            # Full scraped content
│   └── {slug}.md
└── config.yaml           # Local overrides
```

## 🚀 Commands

| Command | Action |
|---------|--------|
| `process reading list` | Process all URLs from inbox |
| `show unread` | List unread items |
| `show reading list` | Full list with status |
| `summarize [topic]` | Get summaries by topic/category |
| `mark read: [title]` | Update status |
| `search: [query]` | Find by keyword |

## 📋 Workflow: Process Reading List

### Step 1: Read Apple Notes Inbox

```python
def process_reading_inbox():
    """
    Read 📚 Reading List Inbox note, extract URLs.
    """
    note_content = get_note_content("📚 Reading List Inbox")
    
    # Split by processed marker
    if "✅ PROCESSED" in note_content:
        pending = note_content.split("✅ PROCESSED")[0]
    else:
        pending = note_content
    
    # Extract URLs
    import re
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, pending)
    
    return normalize_urls(urls)
```

### Step 2: Scrape Content

```python
def scrape_article(url):
    """
    Use Firecrawl for reliable scraping.
    """
    result = firecrawl_scrape(
        url=url,
        formats=["markdown"],
        onlyMainContent=True
    )
    
    return {
        'title': result.get('title', extract_title(url)),
        'content': result.get('markdown', ''),
        'url': url,
        'scraped_at': datetime.now().isoformat()
    }
```

### Step 3: Summarize & Categorize

```python
def analyze_article(scraped):
    """
    Generate summary, category, takeaways.
    """
    content = scraped['content']
    
    # AI analysis
    analysis = {
        'summary': generate_summary(content, max_words=150),
        'category': categorize(content),  # Tech, AI, Business, etc.
        'key_takeaways': extract_takeaways(content, max_items=5),
        'estimated_read_time': estimate_read_time(content),
        'tags': generate_tags(content, max_tags=5)
    }
    
    return analysis
```

### Step 4: Save to Database

```python
def save_article(url, scraped, analysis, db_path):
    """
    Add to reading-list.yaml
    """
    import yaml
    from datetime import datetime
    
    slug = slugify(scraped['title'])
    
    entry = {
        'id': slug,
        'title': scraped['title'],
        'url': url,
        'status': 'unread',
        'category': analysis['category'],
        'summary': analysis['summary'],
        'key_takeaways': analysis['key_takeaways'],
        'read_time_mins': analysis['estimated_read_time'],
        'tags': analysis['tags'],
        'added_at': datetime.now().isoformat(),
        'read_at': None
    }
    
    # Load existing
    with open(db_path) as f:
        db = yaml.safe_load(f) or {'stats': {}, 'items': []}
    
    # Add and update stats
    db['items'].append(entry)
    db['stats']['total'] = len(db['items'])
    db['stats']['unread'] = len([i for i in db['items'] if i['status'] == 'unread'])
    
    # Save
    with open(db_path, 'w') as f:
        yaml.dump(db, f, allow_unicode=True)
    
    # Save full content
    summary_path = f"summaries/{slug}.md"
    save_full_content(summary_path, scraped, analysis)
    
    return entry
```

## 📊 Database Schema

```yaml
# reading-list.yaml
stats:
  total: 42
  unread: 12
  reading: 3
  done: 25
  archived: 2
  by_category:
    tech: 15
    ai: 10
    business: 8
    career: 5
    other: 4

items:
  - id: building-llm-applications
    title: "Building LLM Applications in 2024"
    url: https://example.com/llm-apps
    status: unread
    category: ai
    summary: |
      Comprehensive guide to building production LLM apps.
      Covers RAG, fine-tuning, and deployment strategies.
    key_takeaways:
      - Start with RAG before fine-tuning
      - Use structured outputs for reliability
      - Monitor token costs from day one
    read_time_mins: 12
    tags: [llm, ai, development, rag]
    added_at: 2024-11-24T10:30:00Z
    read_at: null
```

## 🏷️ Categories

| Category | Description |
|----------|-------------|
| tech | Programming, tools, engineering |
| ai | AI/ML, LLMs, data science |
| business | Strategy, management, startups |
| career | Job search, skills, growth |
| finance | Investing, markets, economics |
| science | Research, discoveries |
| other | Everything else |

## 📝 Output Examples

### Unread List

```
📚 Reading List - 12 Unread

🔥 AI (5)
• Building LLM Applications (12 min)
• RAG Best Practices (8 min)
• Claude 4 Features (6 min)

💼 Career (3)
• Tech Interview Guide 2024 (15 min)
• Salary Negotiation Tips (10 min)
```

### Article Summary

```
📖 Building LLM Applications in 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category: AI | Read time: 12 min
Added: Nov 24, 2024

Summary:
Comprehensive guide covering RAG implementation,
fine-tuning decisions, and production deployment...

Key Takeaways:
• Start with RAG before considering fine-tuning
• Use structured outputs for reliability
• Monitor token costs from day one
• Implement proper error handling
• Cache aggressively

Tags: llm, ai, development, rag
URL: https://example.com/llm-apps
```

## ⚡ Quick Start

1. Open "📚 Reading List Inbox" in Apple Notes
2. Paste article URLs (one per line)
3. Tell Claude: `"process reading list"`
4. View with: `"show unread"`

---

**Version**: 1.0.0
**Last Updated**: 2024-11-24
**Patterns**: inbox, database, scraping
