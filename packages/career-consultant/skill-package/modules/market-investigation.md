---
module_name: market-investigation
version: 1.0.0
description: Market analysis, company comparisons, salary benchmarking, and hiring trends
token_cost: ~5-8K tokens depending on complexity
dependencies: [database-operations-hybrid.md]
status: active
---

# Market Investigation Module

## Purpose

This module provides market intelligence capabilities to help users understand the Israeli tech job market, compare opportunities, benchmark salaries, and identify trends across their job backlog and analyzed opportunities.

## When to Load This Module

Load this module when user requests:
- "Compare [Company A] vs [Company B]"
- "What's the market rate for [role]?"
- "Show me all jobs at [company/tier]"
- "Analyze salary trends in my backlog"
- "What are the top-paying roles I've analyzed?"
- "Show trends in AI/ML hiring"

## Token Budget

- Company comparison (2 companies): ~3-4K tokens
- Salary benchmarking: ~2-3K tokens
- Trend analysis: ~4-6K tokens
- Full market report: ~8-10K tokens

## Core Workflows

### Workflow 1: Company Comparison

Compare 2-5 companies side-by-side across key dimensions.

**Command Examples:**
- "Compare NVIDIA vs Intel"
- "Compare Google Israel vs Microsoft Israel vs Apple Israel"

**Implementation:**

```python
def compare_companies(company_slugs: list[str], user_data_base: str):
    """
    Load and compare multiple companies side-by-side.
    
    Args:
        company_slugs: List of company IDs (e.g., ["nvidia", "intel", "google"])
        user_data_base: Path to user-data directory
    
    Returns:
        Comparison table and analysis
    """
    companies = []
    
    # Load company data
    for slug in company_slugs:
        try:
            content = filesystem:read_text_file(
                path=f"{user_data_base}/companies/{slug}.md"
            )
            company_data = parse_yaml_frontmatter(content)
            companies.append(company_data)
        except FileNotFoundError:
            print(f"⚠️  {slug} not found - needs research first")
            continue
    
    if len(companies) < 2:
        print("❌ Need at least 2 companies for comparison")
        return
    
    # Generate comparison
    generate_comparison_table(companies)
    generate_recommendation(companies)

def generate_comparison_table(companies: list):
    """Display side-by-side comparison table."""
    
    print(f"""
## Company Comparison

| Metric | {" | ".join([c['company_name'] for c in companies])} |
|--------|{"|".join(["--------" for _ in companies])}|
| **Tier** | {" | ".join([f"Tier {c['tier']}" for c in companies])} |
| **Employees (Israel)** | {" | ".join([str(c.get('employees_israel', 'N/A')) for c in companies])} |
| **Glassdoor Rating** | {" | ".join([f"{c.get('glassdoor_rating', 'N/A')}/5.0" for c in companies])} |
| **Market Cap/Valuation** | {" | ".join([c.get('market_cap', 'N/A') for c in companies])} |
| **Company Type** | {" | ".join([c.get('company_type', 'N/A') for c in companies])} |
| **Jobs Analyzed** | {" | ".join([str(c.get('num_jobs_analyzed', 0)) for c in companies])} |

### Detailed Comparison

""")
    
    # Compensation comparison
    print("#### 💰 Compensation")
    for company in companies:
        print(f"**{company['company_name']}:**")
        print(f"- Engineering Manager: {company.get('salary_em_range', 'Data pending')}")
        print(f"- Senior TPM: {company.get('salary_tpm_range', 'Data pending')}")
        print(f"- Premium: {company.get('market_premium', 'Market rate')}")
        print()
    
    # Culture comparison
    print("#### 🏢 Culture & Work Environment")
    for company in companies:
        print(f"**{company['company_name']}:**")
        print(f"- Pace: {company.get('work_pace', 'N/A')}")
        print(f"- Work-Life Balance: {company.get('wlb_rating', 'N/A')}/5.0")
        print(f"- Innovation Focus: {company.get('innovation_level', 'N/A')}")
        print()
    
    # Growth opportunities
    print("#### 📈 Growth & Impact")
    for company in companies:
        print(f"**{company['company_name']}:**")
        print(f"- Growth Trajectory: {company.get('growth_trajectory', 'N/A')}")
        print(f"- Israel Site Importance: {company.get('israel_importance', 'N/A')}")
        print(f"- Career Path: {company.get('career_opportunities', 'N/A')}")
        print()

def generate_recommendation(companies: list):
    """Provide recommendation based on comparison."""
    
   print("""
### 🎯 Recommendation

Based on this comparison:

**Best for Compensation:** [Company with highest tier/premium]
**Best for Work-Life Balance:** [Company with highest WLB rating]
**Best for Career Growth:** [Company with highest tier + growth]
**Best for Learning:** [Company with cutting-edge tech]

**Overall Assessment:**
- If prioritizing income → [Top comp company]
- If prioritizing WLB → [Top WLB company]
- If prioritizing impact → [Most strategic company]

💡 Consider your custom scoring weights to determine best fit.
    """)
```

**Example Output:**

```markdown
## Company Comparison: NVIDIA vs Intel vs Microsoft

| Metric | NVIDIA | Intel | Microsoft |
|--------|--------|-------|-----------|
| **Tier** | Tier 1 | Tier 1 | Tier 1 |
| **Employees (Israel)** | 4,500-5,000 | 11,700 | 2,500 |
| **Glassdoor Rating** | 4.3/5.0 | 3.7/5.0 | 4.2/5.0 |
| **Market Cap** | $4T | $100B | $3.1T |
| **Company Type** | AI Leaders | Semiconductor | Cloud/AI |
| **Jobs Analyzed** | 14 | 0 | 3 |

### Detailed Comparison

#### 💰 Compensation
**NVIDIA:**
- Engineering Manager: ₪900K-₪1.4M
- Senior TPM: ₪850K-₪1.3M
- Premium: +33% above competitors

**Intel:**
- Engineering Manager: ₪850K-₪1.2M
- Senior TPM: ₪800K-₪1.1M
- Premium: Market baseline

**Microsoft:**
- Engineering Manager: ₪900K-₪1.3M
- Senior TPM: ₪850K-₪1.2M
- Premium: +15-20% above market

#### 🏢 Culture & Work Environment
**NVIDIA:**
- Pace: Very fast-paced, high-intensity
- Work-Life Balance: 3.7/5.0
- Innovation Focus: Cutting-edge AI

**Intel:**
- Pace: Moderate, structured
- Work-Life Balance: 3.5/5.0
- Innovation Focus: Semiconductor innovation

**Microsoft:**
- Pace: Fast-paced, deadline-driven
- Work-Life Balance: 4.0/5.0
- Innovation Focus: Cloud + AI

### 🎯 Recommendation

Based on this comparison:

**Best for Compensation:** NVIDIA (+33% premium)
**Best for Work-Life Balance:** Microsoft (4.0/5.0)
**Best for Career Growth:** NVIDIA (fastest growing, core products)
**Best for Learning:** NVIDIA (AI infrastructure leadership)

**Overall Assessment:**
- If prioritizing income → **NVIDIA** (highest comp, RSUs)
- If prioritizing WLB → **Microsoft** (better balance)
- If prioritizing impact → **NVIDIA** (powering AI revolution)
```

---

### Workflow 2: Salary Benchmarking

Analyze salary ranges for specific roles across companies.

**Command Examples:**
- "What's the market rate for Engineering Manager?"
- "Show salary ranges for TPM roles"
- "Compare PM salaries across companies"

**Implementation:**

```python
def benchmark_salary(role_type: str, user_data_base: str):
    """
    Benchmark salary for a specific role across analyzed jobs.
    
    Args:
        role_type: Role to benchmark (e.g., "Engineering Manager", "TPM", "PM")
        user_data_base: Path to user-data
    
    Returns:
        Salary distribution and statistics
    """
    # Load all analyzed jobs
    analyzed_jobs = load_analyzed_jobs(user_data_base)
    
    # Filter by role type
    matching_jobs = [j for j in analyzed_jobs 
                     if role_type.lower() in j['role_title'].lower()]
    
    if not matching_jobs:
        print(f"❌ No {role_type} jobs analyzed yet")
        return
    
    # Extract salary data
    salaries = [j.get('income_estimate') for j in matching_jobs 
                if j.get('income_estimate')]
    
    # Calculate statistics
    avg_salary = sum(salaries) / len(salaries)
    min_salary = min(salaries)
    max_salary = max(salaries)
    median_salary = sorted(salaries)[len(salaries) // 2]
    
    # Group by company tier
    tier1_salaries = [j['income_estimate'] for j in matching_jobs 
                       if j.get('company_tier') == 1]
    tier2_salaries = [j['income_estimate'] for j in matching_jobs 
                      if j.get('company_tier') == 2]
    
    print(f"""
## {role_type} Salary Benchmark (Israeli Market)

### Overall Statistics
- **Sample Size:** {len(matching_jobs)} jobs analyzed
- **Average:** ₪{avg_salary:,.0f} annual
- **Median:** ₪{median_salary:,.0f} annual
- **Range:** ₪{min_salary:,.0f} - ₪{max_salary:,.0f}

### By Company Tier
**Tier 1 Companies** (FAANG, market leaders):
- Average: ₪{sum(tier1_salaries)/len(tier1_salaries) if tier1_salaries else 0:,.0f}
- Range: ₪{min(tier1_salaries) if tier1_salaries else 0:,.0f} - ₪{max(tier1_salaries) if tier1_salaries else 0:,.0f}

**Tier 2 Companies** (well-funded, established):
- Average: ₪{sum(tier2_salaries)/len(tier2_salaries) if tier2_salaries else 0:,.0f}
- Range: ₪{min(tier2_salaries) if tier2_salaries else 0:,.0f} - ₪{max(tier2_salaries) if tier2_salaries else 0:,.0f}

### Detailed Breakdown
""")
    
    # Show per-company breakdown
    by_company = {}
    for job in matching_jobs:
        company = job['company_name']
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(job['income_estimate'])
    
    for company, sals in sorted(by_company.items(), 
                                 key=lambda x: sum(x[1])/len(x[1]), 
                                 reverse=True):
        avg = sum(sals) / len(sals)
        print(f"**{company}:** ₪{avg:,.0f} ({len(sals)} jobs)")
    
    print(f"""

### 💡 Insights
- **Top Payer:** {max(by_company.items(), key=lambda x: sum(x[1])/len(x[1]))[0]}
- **Most Competitive:** Tier 1 companies offer {((sum(tier1_salaries)/len(tier1_salaries) / (sum(tier2_salaries)/len(tier2_salaries))) - 1) * 100:.0f}% premium
- **Your Profile:** Based on your requirements, target ₪{avg_salary * 1.1:,.0f}+ for strong fit

""")
```

**Example Output:**

```markdown
## Engineering Manager Salary Benchmark (Israeli Market)

### Overall Statistics
- **Sample Size:** 18 jobs analyzed
- **Average:** ₪1,150,000 annual
- **Median:** ₪1,100,000 annual
- **Range:** ₪850,000 - ₪1,500,000

### By Company Tier
**Tier 1 Companies** (FAANG, market leaders):
- Average: ₪1,250,000
- Range: ₪1,000,000 - ₪1,500,000

**Tier 2 Companies** (well-funded, established):
- Average: ₪950,000
- Range: ₪850,000 - ₪1,100,000

### Detailed Breakdown
**NVIDIA:** ₪1,350,000 (6 jobs)
**Microsoft:** ₪1,200,000 (4 jobs)
**Google:** ₪1,250,000 (3 jobs)
**AWS:** ₪1,150,000 (2 jobs)
**Akamai:** ₪900,000 (2 jobs)
**HARMAN:** ₪850,000 (1 job)

### 💡 Insights
- **Top Payer:** NVIDIA (₪1.35M average)
- **Most Competitive:** Tier 1 companies offer 32% premium over Tier 2
- **Your Profile:** Based on your requirements, target ₪1,260,000+ for strong fit
```

---

### Workflow 3: Trend Analysis

Analyze hiring trends, popular companies, role types in backlog.

**Command Examples:**
- "Show trends in my job search"
- "What companies am I targeting most?"
- "Analyze my backlog by role type"

**Implementation:**

```python
def analyze_trends(user_data_base: str):
    """
    Analyze trends across user's backlog and analyzed jobs.
    """
    # Load backlog
    backlog_content = filesystem:read_text_file(
        path=f"{user_data_base}/jobs/backlog.yaml"
    )
    backlog = yaml.safe_load(backlog_content)
    
    # Load analyzed jobs
    analyzed_jobs = load_analyzed_jobs(user_data_base)
    
    print(f"""
## Job Search Trends Analysis

### Backlog Overview
- **Total Jobs:** {backlog['stats']['total']}
- **Pending Analysis:** {backlog['stats']['pending']}
- **Analyzed:** {backlog['stats']['analyzed']}
- **Archived:** {len(backlog['jobs'].get('archived', []))}

""")
    
    # Company distribution
    companies = {}
    for job in backlog['jobs'].get('pending', []):
        company = job.get('company', 'Unknown')
        companies[company] = companies.get(company, 0) + 1
    
    print("### Top Companies in Backlog")
    for company, count in sorted(companies.items(), 
                                  key=lambda x: x[1], 
                                  reverse=True)[:10]:
        print(f"{count} jobs - {company}")
    
    # Role type distribution  
    roles = {}
    for job in backlog['jobs'].get('pending', []):
        role = job.get('role', 'Unknown')
        role_type = categorize_role(role)  # TPM, EM, PM, etc.
       roles[role_type] = roles.get(role_type, 0) + 1
    
    print("\n### Role Type Distribution")
    for role_type, count in sorted(roles.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True):
        print(f"{count} jobs - {role_type}")
    
    # Scoring distribution for analyzed jobs
    if analyzed_jobs:
        scores = [j['score_total'] for j in analyzed_jobs]
        first_priority = len([s for s in scores if s >= 54])
        second_priority = len([s for s in scores if 40 <= s < 54])
        third_priority = len([s for s in scores if s < 40])
        
        print(f"""

### Analyzed Jobs Distribution
- **First Priority** (≥54): {first_priority} jobs ({first_priority/len(analyzed_jobs)*100:.0f}%)
- **Second Priority** (40-53): {second_priority} jobs ({second_priority/len(analyzed_jobs)*100:.0f}%)
- **Third Priority** (<40): {third_priority} jobs ({third_priority/len(analyzed_jobs)*100:.0f}%)

**Average Score:** {sum(scores)/len(scores):.1f}/100
**Highest Score:** {max(scores)}/100
**Lowest Score:** {min(scores)}/100
        """)
    
    print("""

### 💡 Insights & Recommendations
[Generate personalized insights based on data]
""")
```

---

### Workflow 4: Job Aggregation & Filtering

Filter and group jobs by various criteria.

**Commands:**
- "Show all NVIDIA jobs"
- "Show all Tier 1 companies"
- "Show jobs scoring above 70"
- "Show all TPM roles"

```python
def filter_jobs(criteria: dict, user_data_base: str):
    """
    Filter jobs based on criteria.
    
    Args:
        criteria: {
            'company': 'NVIDIA',
            'role_type': 'TPM',
            'min_score': 70,
            'tier': 1
        }
    """
    analyzed_jobs = load_analyzed_jobs(user_data_base)
    
    filtered = analyzed_jobs
    
    # Apply filters
    if criteria.get('company'):
        filtered = [j for j in filtered 
                    if criteria['company'].lower() in j['company_name'].lower()]
    
    if criteria.get('role_type'):
        filtered = [j for j in filtered 
                    if criteria['role_type'].lower() in j['role_title'].lower()]
    
    if criteria.get('min_score'):
        filtered = [j for j in filtered 
                    if j['score_total'] >= criteria['min_score']]
    
    if criteria.get('tier'):
        filtered = [j for j in filtered 
                    if j.get('company_tier') == criteria['tier']]
    
    # Display results
    print(f"## Filtered Jobs ({len(filtered)} matches)\n")
    
    for job in sorted(filtered, key=lambda x: x['score_total'], reverse=True):
        print(f"**{job['score_total']}/100** - {job['company_name']} - {job['role_title']}")
        print(f"- Income: ₪{job.get('income_estimate', 0):,}")
        print(f"- Priority: {job['priority']}")
        print(f"- URL: {job['job_url']}")
        print()
```

---

## Helper Functions

```python
def load_analyzed_jobs(user_data_base: str) -> list:
    """Load all analyzed jobs from database."""
    jobs = []
    
    # List analyzed jobs directory
    analyzed_dir = f"{user_data_base}/jobs/analyzed"
    files = filesystem:list_directory(path=analyzed_dir)
    
    for file in files:
        if file.endswith('.md'):
            content = filesystem:read_text_file(path=f"{analyzed_dir}/{file}")
            job_data = parse_yaml_frontmatter(content)
            jobs.append(job_data)
    
    return jobs

def categorize_role(role_title: str) -> str:
    """Categorize role into standard types."""
    role_lower = role_title.lower()
    
    if 'tpm' in role_lower or 'technical program' in role_lower:
        return 'TPM'
    elif 'product manager' in role_lower or ' pm ' in role_lower:
        return 'Product Manager'
    elif 'engineering manager' in role_lower or 'em' in role_lower:
        return 'Engineering Manager'
    elif 'director' in role_lower:
        return 'Director'
    elif 'vp' in role_lower or 'vice president' in role_lower:
        return 'VP/Executive'
    elif 'architect' in role_lower:
        return 'Architect'
    else:
        return 'Other'
```

---

## Version History

- **v1.0.0** (2025-11-20): Initial release

---

**Module Status**: Active  
**Last Updated**: 2025-11-20  
**Dependencies**: database-operations-hybrid.md
