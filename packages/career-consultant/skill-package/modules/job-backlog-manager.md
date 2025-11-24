---
title: Job Backlog Manager Module
summary: Capture and triage job postings before full analysis within the skill workflow.
last_updated: "2025-11-19"
---

# Job Backlog Manager Module v9.2

## Purpose
Lightweight job capture system for building a backlog of jobs to analyze. Enables users to quickly save job postings before committing to full analysis.

## When to Load This Module
- **Trigger**: User provides job URL(s) without requesting full analysis
- **Commands**: "Add to backlog", "Save job", "Batch add jobs"
- **Prerequisites**: 
  - USER_DATA_BASE path loaded
  - Minimal token budget (< 5K per job)
- **After completion**: Ask user if they want to analyze now or later

---

## Critical Requirements

### Token Efficiency

**Module Load**: ~2K tokens  
**Per Job Processing**: ~3-5K tokens  
**Batch (5 jobs)**: ~15-20K tokens

This is significantly lighter than full analysis (~25-35K tokens).

### Tool Selection by Platform

**Configuration-Driven Selection**: Tools are selected from `user_config['scraping_tools']['job_scraping']`.

```python
def select_scraping_tool_for_job(job_url, user_config):
    """
    Choose optimal tool based on user config and URL platform.
    
    Falls back to platform-specific if configured tool unavailable.
    """
    # Get user's preferred tool order for job scraping
    tool_order = user_config.get('scraping_tools', {}).get('job_scraping', [])
    
    # Default if not configured
    if not tool_order:
        # Platform-specific defaults
        if 'linkedin.com' in job_url:
            tool_order = ['bright_data', 'web_fetch']
        else:
            tool_order = ['firecrawl', 'web_fetch']
    
    return tool_order

# Try each tool in order
for tool in tool_order:
    try:
        if tool == 'firecrawl':
            content = firecrawl_scrape(url=job_url)
        elif tool == 'bright_data':
            content = Bright Data:scrape_as_markdown(url=job_url)
        elif tool == 'web_fetch':
            content = web_fetch(url=job_url)
        
        return content
    except:
        continue
```

---

## Workflow Steps

### Step 1: Check if Job Already Exists

```python
from slug_utils import normalize_slug, extract_company_from_url
import yaml
import os

def check_job_exists(job_url, backlog_dir):
    """
    Check if job already in backlog.yaml or analyzed roles
    
    Returns: (exists, file_path, status)
    """
    
    # Load backlog.yaml
    backlog_path = f"{backlog_dir}/backlog.yaml"
    
    if not os.path.exists(backlog_path):
        return False, None, None
        
    try:
        content = Filesystem:read_file(path=backlog_path)
        backlog_data = yaml.safe_load(content) or {}
        
        # Check pending jobs
        for job in backlog_data.get('jobs', {}).get('pending', []):
            if job.get('job_url') == job_url:
                print(f"""
                ✅ JOB ALREADY IN BACKLOG
                
                Job: {job['position_title']}
                Company: {job['company_name']}
                Status: {job['status']}
                Added: {job['scraped_date']}
                Priority: {job['priority']}
                """)
                return True, backlog_path, job
                
        # Check analyzed jobs (in backlog list)
        for job in backlog_data.get('jobs', {}).get('analyzed', []):
             if job.get('job_url') == job_url:
                print(f"""
                ✅ JOB ALREADY ANALYZED
                
                Job: {job['position_title']}
                Company: {job['company_name']}
                Score: {job.get('score_total', 'N/A')}/100
                Priority: {job.get('priority', 'N/A')}
                """)
                return True, backlog_path, job

    except Exception as e:
        print(f"⚠️ Error reading backlog: {e}")
    
    print(f"🆕 New job - not in backlog")
    return False, None, None
    print(f"🆕 New job - not in backlog")
    return False, None, None

### Step 1.5: Add to Inbox (Raw Capture)

```python
def add_to_inbox(job_urls, backlog_dir):
    """
    Save raw URLs to inbox.yaml for later processing.
    Zero scraping, minimal token usage.
    """
    import yaml
    from datetime import datetime
    
    inbox_path = f"{backlog_dir}/inbox.yaml"
    
    try:
        # Read existing or create new
        if os.path.exists(inbox_path):
            content = Filesystem:read_file(path=inbox_path)
            data = yaml.safe_load(content) or {'inbox': []}
        else:
            data = {'inbox': []}
            
        if 'inbox' not in data:
            data['inbox'] = []
            
        added_count = 0
        for url in job_urls:
            # Check if already in inbox
            if any(item['url'] == url for item in data['inbox']):
                continue
                
            data['inbox'].append({
                'url': url,
                'added_date': datetime.now().isoformat(),
                'status': 'pending'
            })
            added_count += 1
            
        # Save
        Filesystem:write_file(path=inbox_path, content=yaml.dump(data, sort_keys=False))
        
        print(f"""
        ✅ Added {added_count} jobs to Inbox
        📂 File: {inbox_path}
        
        💡 Next: "Process inbox" to scrape and organize these jobs.
        """)
        return True
        
    except Exception as e:
        print(f"❌ Error saving to inbox: {e}")
        return False

def get_inbox_count(backlog_dir):
    """Get number of pending items in inbox"""
    try:
        inbox_path = f"{backlog_dir}/inbox.yaml"
        if not os.path.exists(inbox_path):
            return 0
        content = Filesystem:read_file(path=inbox_path)
        data = yaml.safe_load(content) or {}
        return len([i for i in data.get('inbox', []) if i['status'] == 'pending'])
    except:
        return 0

def fetch_from_apple_notes(backlog_dir):
    """
    Sync URLs from Apple Notes 'Job Links Inbox' to inbox.yaml
    """
    import yaml
    import re
    from datetime import datetime
    
    print("🔄 Checking Apple Notes for new jobs...")
    
    try:
        # Try to read the note
        # Note: This assumes the tool is available as 'apple_notes:read_note'
        # We use a try/except block to handle missing MCP or tool name mismatch gracefully
        try:
            # We attempt to find a note with "Inbox" in the title
            note_content = apple_notes:read_note(name="Job Links Inbox")
        except:
            print("⚠️ Could not access Apple Notes. Ensure 'apple-notes-mcp' is installed and a note named 'Job Links Inbox' exists.")
            return 0
            
        if not note_content:
            print("ℹ️ Note 'Job Links Inbox' is empty or not found.")
            return 0
            
        # Extract URLs
        urls = re.findall(r'https?://[^\s]+', note_content)
        
        if not urls:
            print("ℹ️ No URLs found in 'Job Links Inbox'.")
            return 0
            
        print(f"found {len(urls)} URLs in Apple Notes.")
        
        # Add to inbox (using existing function)
        add_to_inbox(urls, backlog_dir)
        
        return len(urls)
        
    except Exception as e:
        print(f"❌ Error syncing with Apple Notes: {e}")
        return 0

def sync_and_process_inbox(backlog_dir):
    """
    Sync from Apple Notes then process next item
    """
    # 1. Sync
    fetch_from_apple_notes(backlog_dir)
    
    # 2. Process next
    return process_next_inbox_item(backlog_dir)
```

### Step 2: Scrape Job Posting

```python
def scrape_job_posting(job_url, scraping_tool='auto'):
    """
    Scrape job posting using optimal tool
    
    Returns: (success, job_content, metadata)
    """
    from config_loader import load_user_config, update_scraping_preference
    from paths import USER_DATA_BASE
    
    # Load config for tool selection
    try:
        user_config = load_user_config(USER_DATA_BASE)
    except:
        user_config = {}

    # Determine tool order
    if scraping_tool == 'auto':
        tool_order = select_scraping_tool_for_job(job_url, user_config)
    elif isinstance(scraping_tool, str):
        tool_order = [scraping_tool]
    else:
        tool_order = scraping_tool
    
    print(f"🔍 Scraping job from {job_url}")
    print(f"📋 Tool order: {' -> '.join(tool_order)}")
    
    for tool in tool_order:
        try:
            print(f"   Trying: {tool}...")
            if tool == 'bright_data':
                # LinkedIn scraping
                job_content = Bright Data:scrape_as_markdown(url=job_url)
                
            elif tool == 'firecrawl':
                # Other platforms
                job_content = firecrawl_scrape(
                    url=job_url,
                    formats=["markdown"],
                    onlyMainContent=True
                )
                
            elif tool == 'web_fetch':
                job_content = web_fetch(url=job_url)
            
            else:
                continue

            print(f"✅ Job scraped successfully via {tool}")
            
            # Update preference if successful (and was auto-selected)
            if scraping_tool == 'auto':
                if 'linkedin.com' in job_url:
                    update_scraping_preference(USER_DATA_BASE, 'linkedin', tool)
                else:
                    update_scraping_preference(USER_DATA_BASE, 'job_scraping', tool)
            
            # Extract basic metadata from content
            metadata = extract_job_metadata(job_content, job_url)
            
            return True, job_content, metadata
            
        except Exception as e:
            print(f"❌ {tool} failed: {e}")
            continue
            
    print("❌ All scraping tools failed")
    return False, None, None
```

### Step 3: Extract Job Metadata

```python
def extract_job_metadata(job_content, job_url):
    """
    Parse scraped content to extract key fields
    
    Smart extraction using pattern matching and AI
    """
    
    from datetime import datetime
    
    # Extract company name
    company_name = extract_company_from_url(job_url)
    
    # Try to extract from content
    if 'linkedin.com' in job_url:
        # LinkedIn pattern: "Company Name\nLocation"
        company_from_content = extract_linkedin_company(job_content)
        if company_from_content:
            company_name = company_from_content
    
    # Extract position title
    position_title = extract_position_title(job_content, job_url)
    
    # Extract location
    location = extract_location(job_content)
    
    # Extract applicants count (LinkedIn specific)
    applicants_count = None
    if 'linkedin.com' in job_url:
        applicants_count = extract_applicants_count(job_content)
    
    # Extract experience level
    experience_level = extract_experience_level(job_content, position_title)
    
    # Extract posting age
    posting_age = extract_posting_age(job_content)
    
    # Check company database for company_id
    from slug_utils import normalize_slug
    company_slug = normalize_slug(company_name)
    company_id = f"{company_slug}"  # Will be validated against db
    
    # Determine source platform
    if 'linkedin.com' in job_url:
        source_platform = 'linkedin'
    elif 'greenhouse.io' in job_url:
        source_platform = 'greenhouse'
    elif 'lever.co' in job_url:
        source_platform = 'lever'
    else:
        source_platform = 'company-site'
    
    # Quick keyword match estimate (optional)
    quick_match = estimate_quick_match(job_content, position_title)
    
    metadata = {
        'company_name': company_name,
        'company_id': company_id,
        'position_title': position_title,
        'location': location,
        'applicants_count': applicants_count,
        'experience_level': experience_level,
        'posting_age_days': posting_age,
        'source_platform': source_platform,
        'job_url': job_url,
        'scraped_date': datetime.now().strftime('%Y-%m-%d'),
        'quick_match_estimate': quick_match
    }
    
    print(f"""
    📊 Extracted Metadata:
    • Position: {position_title}
    • Company: {company_name}
    • Location: {location}
    • Applicants: {applicants_count or 'N/A'}
    • Level: {experience_level}
    • Quick Match: {quick_match}% (estimate)
    """)
    
    return metadata
```

### Step 4: Create Backlog Entry

```python
def create_backlog_entry(job_content, metadata, backlog_dir, user_priority='medium'):
    """
    Save job to backlog.yaml
    
    Args:
        job_content: Raw job description (markdown) - NOT SAVED in YAML, only metadata
        metadata: Extracted metadata dict
        backlog_dir: Path to jobs directory
        user_priority: high/medium/low
    """
    
    from datetime import datetime
    import yaml
    
    # Generate unique job_id
    company_slug = normalize_slug(metadata['company_name'])
    position_slug = normalize_slug(metadata['position_title'])
    date_suffix = datetime.now().strftime('%Y%m%d')
    
    job_id = f"{company_slug}-{position_slug}-backlog-{date_suffix}"
    
    # Build Job Object
    job_entry = {
        # Core Identifiers
        'job_id': job_id,
        'company_name': metadata['company_name'],
        'company_id': metadata['company_id'],
        'position_title': metadata['position_title'],
        'role_category': categorize_role(metadata['position_title']),
        
        # Job Source
        'job_url': metadata['job_url'],
        'source_platform': metadata['source_platform'],
        'scraped_date': metadata['scraped_date'],
        
        # Location & Basics
        'location': metadata['location'],
        'remote_option': detect_remote(job_content),
        
        # Quick Metrics
        'applicants_count': metadata.get('applicants_count'),
        'posting_age_days': metadata.get('posting_age_days'),
        'experience_level': metadata.get('experience_level', 'senior'),
        
        # User Backlog Management
        'priority': user_priority,
        'status': 'pending',
        'analyzed': False,
        'quick_match_estimate': metadata.get('quick_match_estimate'),
        'user_notes': ''
    }
    
    # Update backlog.yaml
    backlog_path = f"{backlog_dir}/backlog.yaml"
    
    try:
        # Read existing
        if os.path.exists(backlog_path):
            content = Filesystem:read_file(path=backlog_path)
            data = yaml.safe_load(content) or {}
        else:
            data = {'stats': {'total': 0, 'new': 0, 'pending': 0, 'analyzed': 0}, 'jobs': {'new': [], 'pending': [], 'analyzed': [], 'archived': []}}
            
        # Append to pending
        if 'jobs' not in data: data['jobs'] = {}
        if 'pending' not in data['jobs']: data['jobs']['pending'] = []
        
        data['jobs']['pending'].append(job_entry)
        
        # Update stats
        data['stats']['pending'] = len(data['jobs']['pending'])
        data['stats']['total'] = data['stats']['pending'] + len(data['jobs'].get('analyzed', [])) + len(data['jobs'].get('new', []))
        
        # Write back
        Filesystem:write_file(path=backlog_path, content=yaml.dump(data, sort_keys=False, allow_unicode=True))
        
        print(f"✅ Saved to backlog: {job_id}")
        
        return job_id, backlog_path
        
    except Exception as e:
        print(f"❌ Error saving to backlog: {e}")
        return None, None
```

### Step 5: Batch Processing

```python
def process_job_batch(job_urls, backlog_dir, default_priority='medium'):
    """
    Process multiple jobs at once
    """
    
    print(f"""
    🔄 BATCH PROCESSING {len(job_urls)} JOBS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    results = {
        'added': [],
        'skipped': [],
        'failed': []
    }
    
    for idx, job_url in enumerate(job_urls, 1):
        print(f"\n[{idx}/{len(job_urls)}] Processing: {job_url}")
        
        # Check if exists
        exists, filepath, metadata = check_job_exists(job_url, backlog_dir)
        
        if exists:
            print("⏭️  Skipping (already in system)")
            results['skipped'].append({
                'url': job_url,
                'reason': 'Already exists',
                'file': filepath
            })
            continue
        
        # Scrape job
        success, content, job_metadata = scrape_job_posting(job_url)
        
        if not success:
            print("❌ Failed to scrape")
            results['failed'].append({
                'url': job_url,
                'reason': 'Scraping failed'
            })
            continue
        
        # Create backlog entry
        job_id, saved_path = create_backlog_entry(
            content, 
            job_metadata, 
            backlog_dir,
            default_priority
        )
        
        if job_id:
            results['added'].append({
                'job_id': job_id,
                'url': job_url,
                'file': saved_path,
                'company': job_metadata['company_name'],
                'position': job_metadata['position_title']
            })
            print("✅ Added to backlog")
        else:
            results['failed'].append({'url': job_url, 'reason': 'Save failed'})
    
    # Print summary
    print(f"""
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 BATCH PROCESSING COMPLETE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    ✅ Added: {len(results['added'])}
    ⏭️  Skipped: {len(results['skipped'])}
    ❌ Failed: {len(results['failed'])}
    
    Total processed: {len(job_urls)}
    """)
    
    return results
```

---

## User Commands

### Command: "Add to backlog"

```python
def handle_add_to_backlog(user_message, backlog_dir):
    """
    Parse user message and add job(s) to backlog
    """
    
    # Extract URLs from message
    import re
    urls = re.findall(r'https?://[^\s]+', user_message)
    
    if not urls:
        print("❌ No valid URLs found in message")
        return
    
    # Extract priority if specified
    priority = 'medium'  # default
    if 'high priority' in user_message.lower():
        priority = 'high'
    elif 'low priority' in user_message.lower():
        priority = 'low'
    
    # Single job or batch?
    if len(urls) == 1:
        # Single job processing
        job_url = urls[0]
        
        # Check if exists
        exists, filepath, metadata = check_job_exists(job_url, backlog_dir)
        
        if exists:
            print("""
            🔄 Job already exists in backlog.
            """)
            return
        
        # Scrape and add
        success, content, job_metadata = scrape_job_posting(job_url)
        
        if success:
            job_id, filepath = create_backlog_entry(
                content, 
                job_metadata, 
                backlog_dir,
                priority
            )
            
            print(f"""
            ✅ JOB ADDED TO BACKLOG
            
            Job ID: {job_id}
            Position: {job_metadata['position_title']}
            Company: {job_metadata['company_name']}
            Priority: {priority.upper()}
            
            💡 NEXT STEPS:
            1. Add more jobs to backlog
            2. Analyze this job now
            3. Analyze all backlog jobs
            """)
    
    else:
        # Batch processing
        results = process_job_batch(urls, backlog_dir, priority)
```

### Command: "Show backlog"

```python
def show_backlog_summary(backlog_dir):
    """
    Display summary of all jobs in backlog.yaml
    """
    import yaml
    
    backlog_path = f"{backlog_dir}/backlog.yaml"
    if not os.path.exists(backlog_path):
        print("Backlog is empty.")
        return

    content = Filesystem:read_file(path=backlog_path)
    data = yaml.safe_load(content) or {}
    jobs = data.get('jobs', {}).get('pending', [])
    
    # Sort by priority and match estimate
    priority_order = {'high': 3, 'medium': 2, 'low': 1}
    jobs.sort(
        key=lambda x: (
            priority_order.get(x.get('priority', 'medium'), 2),
            x.get('quick_match_estimate', 0)
        ),
        reverse=True
    )
    
    print(f"""
    📋 JOB BACKLOG SUMMARY
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Total Jobs: {len(jobs)}
    """)
    
    # Group by priority
    high_priority = [j for j in jobs if j.get('priority') == 'high']
    medium_priority = [j for j in jobs if j.get('priority') == 'medium']
    low_priority = [j for j in jobs if j.get('priority') == 'low']
    
    if high_priority:
        print(f"\n🔴 HIGH PRIORITY ({len(high_priority)} jobs):")
        for job in high_priority[:10]:  # Show top 10
            match = job.get('quick_match_estimate', 'N/A')
            print(f"  • {job['position_title']} at {job['company_name']}")
            print(f"    Match: {match}% | Applicants: {job.get('applicants_count', 'N/A')} | {job['location']}")
    
    if medium_priority:
        print(f"\n🟡 MEDIUM PRIORITY ({len(medium_priority)} jobs):")
        for job in medium_priority[:5]:
            match = job.get('quick_match_estimate', 'N/A')
            print(f"  • {job['position_title']} at {job['company_name']}")
            print(f"    Match: {match}% | {job['location']}")
    
    if low_priority:
        print(f"\n⚪ LOW PRIORITY ({len(low_priority)} jobs)")
    
    print(f"""
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💡 ACTIONS:
    - Analyze job: "Analyze job [job_id]"
    - Analyze top 5: "Analyze top 5 jobs"
    - Change priority: "Set [job_id] to high priority"
    - Remove job: "Remove [job_id] from backlog"
    """)
```

---

## Integration with Full Analysis

When user requests analysis of backlog job:

```python
def analyze_from_backlog(job_id, backlog_dir):
    """
    Load job from backlog and trigger full analysis
    """
    import yaml
    
    backlog_path = f"{backlog_dir}/backlog.yaml"
    if not os.path.exists(backlog_path):
        print("Backlog not found.")
        return False, None

    content = Filesystem:read_file(path=backlog_path)
    data = yaml.safe_load(content) or {}
    
    # Find job
    found_job = None
    for job in data.get('jobs', {}).get('pending', []):
        if job['job_id'] == job_id:
            found_job = job
            break
            
    if not found_job:
        print(f"❌ Job not found: {job_id}")
        return False, None
    
    print(f"""
    🔄 LOADING JOB FROM BACKLOG
    
    Job: {found_job['position_title']}
    Company: {found_job['company_name']}
    Priority: {found_job['priority']}
    Quick Match: {found_job.get('quick_match_estimate', 'N/A')}%
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Starting full analysis...
    """)
    
    # Update status to analyzing
    found_job['status'] = 'analyzing'
    Filesystem:write_file(path=backlog_path, content=yaml.dump(data, sort_keys=False, allow_unicode=True))
    
    # Return job_url to main workflow
    return found_job['job_url'], found_job
    # Return job_url to main workflow
    return found_job['job_url'], found_job

def process_next_inbox_item(backlog_dir):
    """
    Take one item from inbox, scrape it, and move to backlog
    """
    import yaml
    
    inbox_path = f"{backlog_dir}/inbox.yaml"
    if not os.path.exists(inbox_path):
        print("Inbox empty.")
        return False
        
    try:
        content = Filesystem:read_file(path=inbox_path)
        data = yaml.safe_load(content) or {}
        inbox_items = data.get('inbox', [])
        
        # Find first pending
        pending_item = next((i for i in inbox_items if i['status'] == 'pending'), None)
        
        if not pending_item:
            print("No pending items in inbox.")
            return False
            
        url = pending_item['url']
        print(f"🔄 Processing Inbox Item: {url}")
        
        # Scrape
        success, content, metadata = scrape_job_posting(url)
        
        if success:
            # Add to backlog
            job_id, _ = create_backlog_entry(content, metadata, backlog_dir)
            
            if job_id:
                # Mark as processed in inbox (or remove)
                pending_item['status'] = 'processed'
                pending_item['job_id'] = job_id
                Filesystem:write_file(path=inbox_path, content=yaml.dump(data, sort_keys=False))
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error processing inbox: {e}")
        return False
```

---

## Module Output

### Success Response

```python
{
    'success': True,
    'job_id': 'nvidia-senior-tpm-backlog-20251029',
    'job_url': 'https://...',
    'action': 'added',  # added/updated/skipped
    'next_step': 'analyze_prompt'  # analyze_prompt/wait/batch_complete
}
```

---

## Token Budget Impact

**Single Job**: ~5K tokens  
**Batch (5 jobs)**: ~20K tokens  
**Module Load**: ~2K tokens

**Total for 5-job batch**: ~22K tokens (vs. 125-175K for full analysis)

---

**Version**: v1.1.0  
**Last Updated**: 2025-11-19  
**Architecture**: YAML-based backlog system  
**Status**: Production Ready ✅
