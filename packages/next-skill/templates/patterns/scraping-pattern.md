# Scraping Pattern Module

## Overview

Web content extraction using available tools (Firecrawl, Bright Data, web_fetch).

## Tool Selection

| Tool | Best For | Limitations |
|------|----------|-------------|
| `firecrawl_scrape` | General pages, JS-rendered | Rate limits |
| `firecrawl_search` | Finding URLs first | Query-based |
| `Bright Data:scrape_as_markdown` | Bot-protected sites | |
| `web_fetch` | Simple static pages | No JS rendering |

## Workflow

### Step 1: URL Acquisition

Either:
- User provides URL directly
- Search for URL: `firecrawl_search` or `web_search`
- Extract from data (e.g., LinkedIn URL from job posting)

### Step 2: Content Extraction

```python
# Primary method
result = firecrawl_scrape(
    url=target_url,
    formats=["markdown"],
    onlyMainContent=True
)

# Fallback for protected sites
if result.error:
    result = bright_data_scrape_as_markdown(url=target_url)
```

### Step 3: Content Parsing

Extract structured data from markdown:

```python
def parse_content(markdown: str, extraction_rules: dict) -> dict:
    """
    Extract specific fields from scraped content.
    
    extraction_rules = {
        'title': {'pattern': r'^# (.+)$', 'required': True},
        'date': {'pattern': r'Published: (.+)', 'required': False},
        'body': {'selector': 'main content after title'}
    }
    """
    extracted = {}
    for field, rules in extraction_rules.items():
        # Apply extraction logic
        extracted[field] = extract_field(markdown, rules)
    return extracted
```

### Step 4: Storage

Store both raw and extracted:

```yaml
scraped_content:
  url: "https://example.com/page"
  scraped_at: 2025-12-11T10:00:00Z
  raw_markdown: |
    # Title
    Content...
  extracted:
    title: "Title"
    date: "2025-12-10"
    summary: "..."
```

## Error Handling

| Error | Fallback |
|-------|----------|
| Rate limited | Wait and retry, or switch tool |
| 404 | Report to user, skip |
| Bot protection | Try Bright Data |
| Timeout | Reduce content scope |

## Caching

Avoid re-scraping recently fetched content:

```python
def get_cached_or_scrape(url: str, max_age_hours: int = 24) -> dict:
    cached = get_cached(url)
    if cached and cached['scraped_at'] > (now - hours(max_age_hours)):
        return cached
    return scrape_and_cache(url)
```

## Batch Scraping

For multiple URLs:

```python
# Firecrawl batch (up to 10)
results = firecrawl_batch_scrape(urls=url_list)

# Or sequential with rate limiting
for url in urls:
    result = scrape(url)
    time.sleep(1)  # Rate limit courtesy
```

## Best Practices

1. **Respect rate limits** - Don't hammer sites
2. **Cache aggressively** - Avoid redundant scrapes
3. **Extract only what's needed** - Don't store entire pages
4. **Handle failures gracefully** - Log and continue
5. **Validate extracted data** - Check required fields exist
