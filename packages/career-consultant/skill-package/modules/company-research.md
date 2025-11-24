---
title: Company Research Module
summary: Gather and normalize target company intelligence for downstream evaluation.
last_updated: "2025-10-29"
---

# Company Research Module v9.1

## Purpose
Execute comprehensive company research using Firecrawl MCP or internal fetch_web when company is not cached or validated.

## When to Load This Module
- **Trigger**: Step 3 determines company doesn't exist OR exists but `updated: false`
- **Prerequisites**: 
  - Token budget < 50% used (research needs ~15K tokens)
  - Bright Data MCP available
  - USER_DATA_BASE path loaded
- **After completion**: STOP conversation (user must validate and start new)

---

## Critical Requirements

### Token Budget Check

```python
from token_estimator import check_token_budget, estimate_tokens
from config_loader import update_scraping_preference
from paths import USER_DATA_BASE

budget = check_token_budget(TOKENS_USED)

if budget['percentage_used'] > 50:
    print("""
    ⚠️ INSUFFICIENT TOKEN BUDGET
    
    Current: {budget['percentage_used']:.1f}% used
    Research needs: ~15K tokens (additional 8-10%)
    
    Recommendation: Start NEW conversation for research
    
    Why: Research is token-intensive and stopping here
    allows optimal performance for subsequent job analysis.
    """)
    STOP_HERE
```

### Tool Selection Strategy

**⚠️ CONFIGURATION-DRIVEN TOOLS**

This module uses tools based on `user_config['scraping_tools']` configuration:

```python
def select_scraping_tool(user_config, use_case='company_research'):
    """
    Select scraping tool based on user configuration.
    
    Args:
        user_config: Loaded settings.yaml
        use_case: 'company_research', 'linkedin', or 'job_scraping'
    
    Returns:
        list: Ordered list of tools to try
    """
    # Get configured tool priorities
    tool_priorities = user_config.get('scraping_tools', {}).get(use_case, [])
    
    # Default fallback if not configured
    if not tool_priorities:
        defaults = {
            'company_research': ['firecrawl', 'web_fetch'],
            'linkedin': ['mcp_docker', 'bright_data', 'web_fetch'],
            'job_scraping': ['firecrawl', 'bright_data', 'web_fetch']
        }
        tool_priorities = defaults.get(use_case, ['web_fetch'])
    
    print(f"📋 Tool order for {use_case}: {' → '.join(tool_priorities)}")
    return tool_priorities

def scrape_with_fallback(url, tool_order, context="", use_case=None):
    """
    Try each tool in order until one succeeds.
    
    Args:
        url: Target URL
        tool_order: List of tools from select_scraping_tool()
        context: Description for logging
        use_case: Optional use case for config update (e.g., 'linkedin')
    
    Returns:
        Scraped content or None
    """
    for tool in tool_order:
        try:
            if tool == 'firecrawl':
                content = firecrawl_scrape(url=url, formats=["markdown"])
                print(f"✅ {context} via Firecrawl")
                if use_case: update_scraping_preference(USER_DATA_BASE, use_case, 'firecrawl')
                return content
                
            elif tool == 'bright_data':
                content = Bright Data:scrape_as_markdown(url=url)
                print(f"✅ {context} via Bright Data")
                if use_case: update_scraping_preference(USER_DATA_BASE, use_case, 'bright_data')
                return content
                
            elif tool == 'mcp_docker':
                content = MCP_DOCKER.scrape(url=url)
                print(f"✅ {context} via MCP_DOCKER")
                if use_case: update_scraping_preference(USER_DATA_BASE, use_case, 'mcp_docker')
                return content
                
            elif tool == 'web_fetch':
                content = web_fetch(url=url)
                print(f"✅ {context} via web_fetch")
                if use_case: update_scraping_preference(USER_DATA_BASE, use_case, 'web_fetch')
                return content
                
        except Exception as e:
            print(f"⚠️  {tool} failed: {e}")
            continue  # Try next tool
    
    print(f"❌ All tools failed for: {url}")
    return None
```

**Usage in Company Research**:
```python
# Load user config
user_config = load_user_config()

# Get tool order for company research
company_tools = select_scraping_tool(user_config, 'company_research')

# Get tool order for LinkedIn
linkedin_tools = select_scraping_tool(user_config, 'linkedin')

# Use with fallback
website_content = scrape_with_fallback(
    url=company_website_url,
    tool_order=company_tools,
    context="Company website",
    use_case='company_research'
)
```

---

## Research Protocol

### Step 3.1: Company Overview Search

```python
def search_company_overview(company_name):
    """
    Initial search for company basics
    """
    
    print(f"🔍 Searching: {company_name}")
    
    # Primary search using Firecrawl
    search_result = firecrawl_search(
        query=f"{company_name} company Israel technology overview",
        limit=5
    )
    
    # Extract from results:
    overview_data = {
        'company_name': company_name,
        'employees_global': extract_employee_count(search_result, 'global'),
        'employees_israel': extract_employee_count(search_result, 'israel'),
        'funding_stage': extract_funding_stage(search_result),
        'industry': extract_industry(search_result),
        'founded': extract_founded_year(search_result),
        'official_website': extract_official_url(search_result)
    }
    
    print(f"✅ Overview gathered: {overview_data['employees_israel']} Israeli employees")
    
    return overview_data
```

### Step 3.2: Website Deep Dive

```python
def scrape_company_website(website_url):
    """
    Extract detailed company information from official website
    """
    
    print(f"🌐 Scraping website: {website_url}")
    
    try:
        # Use Firecrawl for company website scraping
        website_content = firecrawl_scrape(
            url=website_url,
            formats=["markdown"]
        )
        
        # Parse website content
        website_data = {
            'mission': extract_mission(website_content),
            'products': extract_products(website_content),
            'tech_stack': extract_tech_stack(website_content),
            'culture_keywords': extract_culture_keywords(website_content),
            'israel_offices': extract_israel_locations(website_content)
        }
        
        print("✅ Website data extracted")
        
        return website_data
        
    except Exception as e:
        print(f"⚠️ Website scraping failed: {e}")
        print("Continuing with search data...")
        return {
            'mission': 'Not available',
            'products': [],
            'tech_stack': [],
            'culture_keywords': [],
            'israel_offices': []
        }
```

### Step 3.3: Recent News & Developments

```python
def search_recent_news(company_name):
    """
    Find recent company news and developments
    """
    
    print(f"📰 Searching news: {company_name}")
    
    from datetime import datetime
    current_year = datetime.now().year
    
    # Use Firecrawl for news search
    news_result = firecrawl_search(
        query=f"{company_name} Israel news {current_year} {current_year-1}",
        limit=5
    )
    
    news_data = {
        'recent_funding': check_recent_funding(news_result),
        'product_launches': extract_product_news(news_result),
        'hiring_announcements': check_hiring_news(news_result),
        'office_expansions': check_expansion_news(news_result),
        'leadership_changes': extract_leadership_news(news_result),
        'news_summary': summarize_top_news(news_result, top_n=3)
    }
    
    print("✅ News analyzed")
    
    return news_data
```

### Step 3.4: Glassdoor Culture Research

```python
def research_glassdoor_data(company_name):
    """
    Gather employee reviews and culture insights
    """
    
    print(f"⭐ Searching Glassdoor: {company_name}")
    
    # Find Glassdoor page using Firecrawl
    glassdoor_search = firecrawl_search(
        query=f"{company_name} glassdoor reviews Israel",
        limit=3
    )
    
    glassdoor_url = extract_glassdoor_url(glassdoor_search)
    
    if not glassdoor_url:
        print("⚠️ Glassdoor page not found")
        return {
            'glassdoor_rating': None,
            'work_life_balance': None,
            'culture_rating': None,
            'pros': [],
            'cons': [],
            'ceo_approval': None
        }
    
    try:
        # Scrape Glassdoor page using Firecrawl
        glassdoor_content = firecrawl_scrape(
            url=glassdoor_url,
            formats=["markdown"]
        )
        
        glassdoor_data = {
            'glassdoor_rating': extract_overall_rating(glassdoor_content),
            'work_life_balance': extract_work_life_score(glassdoor_content),
            'culture_rating': extract_culture_score(glassdoor_content),
            'pros': extract_top_pros(glassdoor_content, top_n=3),
            'cons': extract_top_cons(glassdoor_content, top_n=3),
            'ceo_approval': extract_ceo_approval(glassdoor_content),
            'glassdoor_url': glassdoor_url
        }
        
        print(f"✅ Glassdoor: {glassdoor_data['glassdoor_rating']}/5.0 ⭐")
        
        return glassdoor_data
        
    except Exception as e:
        print(f"⚠️ Glassdoor scraping failed: {e}")
        return {'glassdoor_rating': None, 'glassdoor_url': glassdoor_url}
```

### Step 3.5: LinkedIn Validation

```python
def validate_linkedin_presence(company_name):
    """
    Verify company LinkedIn and employee count
    
    ⚠️ LinkedIn Priority: MCP_DOCKER (user-tested) → Bright Data fallback
    """
    
    print(f"💼 Searching LinkedIn: {company_name}")
    
    # First find LinkedIn URL using Firecrawl
    linkedin_search = firecrawl_search(
        query=f"{company_name} linkedin company page",
        limit=3
    )
    
    linkedin_url = extract_linkedin_url(linkedin_search)
    
    if not linkedin_url:
        print("⚠️ LinkedIn URL not found")
        return {
            'linkedin_url': None,
            'employee_count_linkedin': None,
            'growth_trends': None
        }
    
    # Try MCP_DOCKER first (user-tested, reliable, cost-effective)
    try:
        print(f"🐳 Attempting MCP_DOCKER for LinkedIn: {linkedin_url}")
        linkedin_content = MCP_DOCKER.scrape(url=linkedin_url)
        
        linkedin_data = {
            'linkedin_url': linkedin_url,
            'employee_count_linkedin': extract_linkedin_employee_count(linkedin_content),
            'growth_trends': assess_growth_trends(linkedin_content)
        }
        
        print("✅ LinkedIn validated via MCP_DOCKER")
        return linkedin_data
        
    except Exception as docker_error:
        print(f"⚠️  MCP_DOCKER failed: {docker_error}")
        print("Falling back to Bright Data...")
        
        # Fallback to Bright Data
        try:
            print(f"💼 Scraping LinkedIn via Bright Data: {linkedin_url}")
            linkedin_content = Bright Data:scrape_as_markdown(url=linkedin_url)
            
            linkedin_data = {
                'linkedin_url': linkedin_url,
                'employee_count_linkedin': extract_linkedin_employee_count(linkedin_content),
                'growth_trends': assess_growth_trends(linkedin_content)
            }
            
            print("✅ LinkedIn validated via Bright Data (fallback)")
            return linkedin_data
            
        except Exception as bright_error:
            print(f"⚠️ Bright Data also failed: {bright_error}")
            return {
                'linkedin_url': linkedin_url,
                'employee_count_linkedin': None,
                'growth_trends': None
            }
```

---

## Tier Assessment Logic

```python
def assess_company_tier(company_data, user_config):
    """
    Assign tier based on comprehensive criteria
    
    Uses user_config for tier bonuses and preferences
    
    Tier 1: Top tech giants, unicorns, leading Israeli companies
    - Examples: NVIDIA, Google, Microsoft, Intel, Wix, Monday.com
    - Criteria: 1000+ Israeli employees OR $1B+ valuation OR recognized leader
    
    Tier 2: Strong established companies, well-funded scale-ups
    - Examples: JFrog, Fiverr, Riskified, SentinelOne, Redis
    - Criteria: 200-1000 Israeli employees, Series C+, strong revenue
    
    Tier 3: Growth-stage startups, Series A-B companies
    - Criteria: 50-200 employees, solid funding, growing market
    
    Tier 4: Early-stage startups, small companies
    - Criteria: <50 employees, seed/early funding, high risk
    """
    
    # Tier 1 indicators
    tier_1_companies = [
        'nvidia', 'google', 'microsoft', 'intel', 'apple', 'amazon', 
        'meta', 'monday.com', 'wix', 'check point', 'mobileye'
    ]
    
    company_lower = company_data['company_name'].lower()
    
    if (company_data['employees_israel'] >= 1000 or
        company_data.get('valuation', 0) >= 1_000_000_000 or
        any(t1 in company_lower for t1 in tier_1_companies)):
        tier = 1
        tier_reasoning = "Large Israeli presence (1000+) or unicorn valuation or industry leader"
    
    # Tier 2 indicators
    elif (company_data['employees_israel'] >= 200 or
          company_data['funding_stage'] in ['Series C', 'Series D', 'Series E', 'IPO'] or
          company_data.get('profitable', False)):
        tier = 2
        tier_reasoning = "Significant presence (200+) or well-funded (Series C+) or profitable"
    
    # Tier 3 indicators
    elif (company_data['employees_israel'] >= 50 or
          company_data['funding_stage'] in ['Series A', 'Series B']):
        tier = 3
        tier_reasoning = "Growing presence (50+) or mid-stage funding (Series A/B)"
    
    # Tier 4: Default
    else:
        tier = 4
        tier_reasoning = "Early stage or small presence (<50 employees)"
    
    # Get tier bonus from user config
    tier_bonus = user_config['preferences']['company_tier_preference'].get(
        f'tier_{tier}_bonus', 
        0
    )
    
    # Tier score mapping
    tier_scores = {1: 10, 2: 7, 3: 4, 4: 0}
    tier_score = tier_scores[tier]
    
    return {
        'tier': tier,
        'tier_score': tier_score,
        'tier_bonus': tier_bonus,
        'tier_reasoning': tier_reasoning
    }
```

---

## Generate Company Profile with YAML

```python
def create_company_profile_with_yaml(all_research_data, user_config):
    """
    Combine all research into YAML + Markdown document
    
    Args:
        all_research_data: Dict with all research results
        user_config: User configuration for tier bonuses
    """
    
    from datetime import datetime
    from slug_utils import normalize_slug
    import yaml
    
    company_name = all_research_data['company_name']
    company_slug = normalize_slug(company_name)
    
    # Assess tier
    tier_data = assess_company_tier(all_research_data, user_config)
    
    # Create YAML frontmatter
    frontmatter = {
        'company_id': company_slug,
        'company_name': company_name,
        'tier': tier_data['tier'],
        'tier_score': tier_data['tier_score'],
        'tier_bonus': tier_data['tier_bonus'],
        
        # Size data
        'employees_global': all_research_data['employees_global'],
        'employees_israel': all_research_data['employees_israel'],
        
        # Ratings
        'glassdoor_rating': all_research_data.get('glassdoor_rating'),
        
        # Stage
        'funding_stage': all_research_data['funding_stage'],
        
        # Meta
        'research_date': datetime.now().strftime('%Y-%m-%d'),
        'updated': False,  # ⚠️ User must validate and set to True
        
        # Links
        'website': all_research_data['official_website'],
        'glassdoor_url': all_research_data.get('glassdoor_url'),
        'linkedin_url': all_research_data.get('linkedin_url'),
        
        # Quick facts
        'tech_stack': all_research_data.get('tech_stack', [])[:5],  # Top 5
        'industry': all_research_data.get('industry', 'Technology')
    }
    
    # Create markdown content
    content = f"""# {company_name}

## Overview
{all_research_data.get('mission', 'No mission statement available.')}

**Industry**: {all_research_data.get('industry', 'Technology')}  
**Founded**: {all_research_data.get('founded', 'N/A')}

## Scale & Presence

**Global Employees**: {all_research_data['employees_global']:,}  
**Israeli Employees**: {all_research_data['employees_israel']}  
**Funding Stage**: {all_research_data['funding_stage']}

## Tier Assessment

**Tier**: {tier_data['tier']}  
**Tier Score**: {tier_data['tier_score']} points (base)  
**Tier Bonus**: +{tier_data['tier_bonus']} points (from user preferences)

**Reasoning**: {tier_data['tier_reasoning']}

## Products & Services
"""
    
    if all_research_data.get('products'):
        for product in all_research_data['products']:
            content += f"- {product}\n"
    else:
        content += "See company website for details.\n"
    
    content += f"""
## Technology Stack

"""
    if all_research_data.get('tech_stack'):
        for tech in all_research_data['tech_stack'][:10]:  # Top 10
            content += f"- {tech}\n"
    else:
        content += "Not publicly disclosed.\n"
    
    content += f"""
## Israeli Operations

**Office Locations**: {', '.join(all_research_data.get('israel_offices', ['Tel Aviv (assumed)']))}  
**Team Size**: {all_research_data['employees_israel']} employees

## Culture & Work Environment
"""
    
    if all_research_data.get('glassdoor_rating'):
        content += f"""
**Glassdoor Rating**: {all_research_data['glassdoor_rating']}/5.0 ⭐  
**Work-Life Balance**: {all_research_data.get('work_life_balance', 'N/A')}/5.0  
**Culture & Values**: {all_research_data.get('culture_rating', 'N/A')}/5.0

### Top Pros
"""
        if all_research_data.get('pros'):
            for pro in all_research_data['pros']:
                content += f"- {pro}\n"
        
        content += "\n### Top Cons\n"
        if all_research_data.get('cons'):
            for con in all_research_data['cons']:
                content += f"- {con}\n"
    else:
        content += "\n*Glassdoor data not available*\n"
    
    content += f"""
## Recent News & Developments
"""
    
    if all_research_data.get('news_summary'):
        for news_item in all_research_data['news_summary']:
            content += f"- {news_item}\n"
    else:
        content += "No recent significant news.\n"
    
    content += f"""
## Research Notes

⚠️ **Validation Required**: Please review all data for accuracy.

**Key Points to Verify**:
- Israeli employee count
- Tier assessment
- Glassdoor ratings
- Recent developments

## Metadata

**Research Date**: {frontmatter['research_date']}  
**Research Method**: Automated via Bright Data MCP  
**Status**: Awaiting validation (`updated: false`)

---

*Company Profile v9.1*  
*Source: Bright Data search + official sources*
"""
    
    # Combine YAML + Markdown
    yaml_text = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    full_document = f"---\n{yaml_text}---\n\n{content}"
    
    return full_document, company_slug, frontmatter
```

---

## Save Company Profile

```python
def save_company_profile(company_document, company_slug):
    """
    Save company profile to database
    
    Args:
        company_document: Complete YAML + Markdown
        company_slug: Normalized company identifier
    """
    
    # Path from config
    company_path = f"{COMPANIES_DIR}/{company_slug}.md"
    
    try:
        # Save to filesystem
        with open(company_path, 'w', encoding='utf-8') as f:
            f.write(company_document)
        
        print(f"✅ Saved: companies/{company_slug}.md")
        return True
        
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False
```

---

## Research Complete Output

```python
def output_research_completion(company_data, company_slug):
    """
    Final output after research completion
    """
    
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ COMPANY RESEARCH COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Company: {company_data['company_name']}
🏢 Tier: {company_data['tier']} ({company_data['tier_score']} base points + {company_data['tier_bonus']} bonus)
👥 Israeli Employees: {company_data['employees_israel']}
⭐ Glassdoor: {company_data.get('glassdoor_rating', 'N/A')}/5.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 FILES SAVED

Company Profile: companies/{company_slug}.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ VALIDATION REQUIRED

Before analyzing jobs for this company:

1. Open file: companies/{company_slug}.md
2. Review all data for accuracy:
   - Employee counts
   - Tier assignment
   - Glassdoor ratings
   - Company description
3. Edit YAML frontmatter:
   Change: updated: false
   To: updated: true
4. Add any notes or corrections
5. Save the file

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 NEXT STEPS

✅ Company research: COMPLETE
⏸️ Job analysis: PAUSED

To analyze a job at {company_data['company_name']}:
1. Validate company profile (see above)
2. START NEW CONVERSATION
3. Provide job URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛑 STOPPING HERE - Research Phase Complete

Why start a new conversation?
- Research used ~15K tokens
- New conversation gives full budget for analysis
- Better performance and response quality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
```

---

## Error Handling

### Graceful Degradation

```python
def safe_research_operation(operation_func, operation_name, fallback_value=None):
    """
    Execute research step with error handling
    """
    
    try:
        result = operation_func()
        return result
        
    except Exception as e:
        print(f"⚠️ {operation_name} failed: {e}")
        
        if fallback_value is not None:
            print(f"Using fallback value: {fallback_value}")
            return fallback_value
        
        print("Continuing with partial data...")
        return None
```

### Recovery Suggestions

```python
def suggest_recovery_options(error_type, company_name):
    """
    Provide user with recovery options on failure
    """
    
    if error_type == "BrightDataUnavailable":
        return f"""
Alternative Options:
1. Enable Bright Data MCP and retry
2. Manually research {company_name}:
   - Visit company website
   - Check Glassdoor
   - Search LinkedIn
3. Use template: templates/example-company.md
4. Create basic profile with known information
"""
    
    elif error_type == "PartialDataFailure":
        return """
Partial Research Completed:
- Review saved data
- Add missing information manually
- Set updated: true when ready
- Proceed with job analysis
"""
    
    else:
        return "See docs/TROUBLESHOOTING.md for guidance"
```

---

## Complete Research Workflow

```python
def execute_company_research(company_name, user_config):
    """
    Main research orchestration
    
    Args:
        company_name: Company to research
        user_config: User configuration dict
    
    Returns:
        (success, company_slug, message)
    """
    
    print(f"""
🔬 COMPANY RESEARCH INITIATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Company: {company_name}
Estimated Time: 2-3 minutes
Token Usage: ~15K tokens

Steps:
1. Company overview search
2. Website deep dive
3. Recent news analysis
4. Glassdoor culture research
5. LinkedIn validation
6. Tier assessment
7. Profile generation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    # Step 1: Overview
    overview = safe_research_operation(
        lambda: search_company_overview(company_name),
        "Company Overview Search",
        fallback_value={'employees_israel': 0}
    )
    
    # Step 2: Website
    website_data = safe_research_operation(
        lambda: scrape_company_website(overview['official_website']),
        "Website Scraping",
        fallback_value={}
    )
    
    # Step 3: News
    news_data = safe_research_operation(
        lambda: search_recent_news(company_name),
        "News Search",
        fallback_value={}
    )
    
    # Step 4: Glassdoor
    glassdoor_data = safe_research_operation(
        lambda: research_glassdoor_data(company_name),
        "Glassdoor Research",
        fallback_value={'glassdoor_rating': None}
    )
    
    # Step 5: LinkedIn
    linkedin_data = safe_research_operation(
        lambda: validate_linkedin_presence(company_name),
        "LinkedIn Validation",
        fallback_value={}
    )
    
    # Combine all data
    all_research = {
        **overview,
        **website_data,
        **news_data,
        **glassdoor_data,
        **linkedin_data
    }
    
    # Step 6: Create profile
    company_document, company_slug, frontmatter = create_company_profile_with_yaml(
        all_research, 
        user_config
    )
    
    # Step 7: Save
    success = save_company_profile(company_document, company_slug)
    
    if success:
        # Output completion message
        output_research_completion(frontmatter, company_slug)
        return True, company_slug, "Research complete - validation required"
    else:
        return False, None, "Failed to save profile"
```

---

## Module Interface

### Input Requirements
```python
{
    'company_name': str,        # Company to research
    'user_config': dict,        # User configuration
    'USER_DATA_BASE': str,      # Base path for data
    'COMPANIES_DIR': str        # Path to companies directory
}
```

### Output Format
```python
{
    'success': bool,
    'company_slug': str,        # For file reference
    'requires_validation': True,
    'message': str
}
```

---

## Token Budget Impact

**Module Load**: ~4K tokens  
**Research Execution**: ~15K tokens  
**Total**: ~19K tokens (10% of budget)

**Optimization**: Module only loaded when company research needed

---

## Module Version

**Version**: v1.1.0  
**Last Updated**: October 28, 2025  
**Architecture**: User-config driven, Bright Data MCP  
**Status**: Production Ready ✅

---  
**Dependencies**: Bright Data MCP, user-config.yaml, paths.py
