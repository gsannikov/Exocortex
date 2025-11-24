---
name: israeli-tech-career-consultant
description: Automated Israeli tech job analysis system. Analyzes job opportunities with 6-component customizable scoring (Match, Income, Growth, LowPrep, Stress, Location). Uses local filesystem storage, automated company research, and multi-CV matching. Outputs markdown analyses and Excel tracking. Best for tech professionals in Israel's tech market. Storage location configured in skill-package/config/paths.py
---

# Israeli Tech Career Consultant

AI-powered assistant for analyzing tech job opportunities in the Israeli market with personalized scoring and intelligent matching.

## 🌟 Key Capabilities
1. **Deep Job Analysis**: 6-point scoring system (Match, Income, Growth, LowPrep, Stress, Location)
2. **Smart Backlog Management**: "Capture First, Analyze Later" with Inbox and Batch processing
3. **Company Research**: Automated intelligence gathering via Bright Data / Firecrawl
4. **Dynamic Reporting**: Generate interactive HTML databases and Excel reports
5. **Multi-CV Matching**: Automatically selects the best CV variant for each role
6. **Token Optimization**: Smart context management and budget tracking

## ⚠️ CRITICAL: Storage Configuration

**DO NOT USE NOTION**  
This skill uses **LOCAL FILESYSTEM ONLY**. All user data is stored in:
- **User Data Location**: Configured in `skill-package/config/paths.py`
- **Default Path**: `/Users/<username>/Documents/career-consultant/user-data/`
- **Database Files**: YAML files in `user-data/companies/` and `user-data/jobs/`
- **Configuration**: `user-data/profile/settings.yaml`

**Never use**:
- ❌ Notion API tools (github.com/makenotion/notion-mcp-server)
- ❌ Google Drive MCP
- ❌ Any external storage APIs

**Always use**:
- ✅ MCP Filesystem tools for USER DATA:
  - Read user files: `filesystem:read_text_file`
  - Write user files: `filesystem:write_file`  
  - List directories: `filesystem:list_directory`
  - Create directories: `filesystem:create_directory`
  - Edit files: `filesystem:edit_file`
  - Search files: `filesystem:search_files`
- ✅ Paths from `paths.py` configuration
- ✅ Local YAML files for data storage

**MCP Server Reference**:
- Package: `@modelcontextprotocol/server-filesystem`
- GitHub: github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- Setup Guide: See `docs/guides/user-guide/mcp-servers.md`

**File Path Rules**:

1. **Skill Modules** (company-research.md, skills-matching.md, etc.):
   - **Location**: Uploaded with skill to `/mnt/skills/user/israeli-tech-career-consultant/`
   - **Access Method**: Use `file_read("modules/module-name.md")` with relative paths
   - **Key Point**: These are embedded resources, NOT filesystem files
   - **Examples**:
     ```python
     research_module = file_read("modules/company-research.md")
     matching_module = file_read("modules/skills-matching.md")
     ```

2. **User Data** (CVs, companies, roles, config):
   - **Location**: User's filesystem (e.g., `~/Documents/career-consultant`)
   - **Access Method**: Use `filesystem:read_text_file` with absolute paths from `paths.py`
   - **Key Point**: These are accessed via MCP Filesystem server
   - **Examples**:
     ```python
     config = filesystem:read_text_file(
         path=f"{USER_DATA_BASE}/profile/settings.yaml"
     )
     cv = filesystem:read_text_file(
         path=f"{USER_DATA_BASE}/config/cv-variants/cv-em.md"
     )
     ```

3. **CRITICAL RULE**: 
   - ❌ NEVER use `filesystem:read_text_file` for skill modules
   - ❌ NEVER use `file_read` for user data
   - ❌ NEVER search filesystem for skill files
   
   If you cannot access skill modules via `file_read`, the skill was not properly uploaded.

## ⚠️ Token Budget Requirements

**Critical**: This skill requires significant token budget due to:
- Module loading (2-4K tokens per module)
- CV processing (8-12K total for multiple CVs)
- Company research (15-20K if new company)

**Best Practice**:
- Start fresh conversation for each job analysis
- Monitor token usage after each major step
- Research phase: Stop after company creation, validate, then restart for analysis
- Analysis phase: Complete in single session if company cached

**Typical Token Usage**:
- Research new company: 15-20K tokens → **STOP**, validate, restart
- Analyze with cached company: 25-35K tokens → Complete in one session

## ⚠️ CRITICAL: Token Budget Protection

**FORBIDDEN OPERATIONS:**
- ❌ NEVER use `directory_tree` on allowed directory roots
- ❌ NEVER use `directory_tree` without confirming small scope (<100 files)
- ❌ NEVER perform recursive operations on large directories
- ❌ NEVER search entire filesystem for skill files

**REQUIRED DISCOVERY PATTERN:**

When you need to understand directory structure:

1. **Use `list_allowed_directories`** to find MCP roots
   ```python
   roots = filesystem:list_allowed_directories()
   # Returns: ["/Users/username/MyDrive/career-consultant.skill"]
   ```

2. **Ask user for specific location** if multiple roots:
   ```python
   print("""
   I see multiple allowed directories:
   {roots}
   
   Which directory contains your career-consultant data?
   """)
   ```

3. **Navigate incrementally** using `list_directory` (non-recursive):
   ```python
   # Safe: lists immediate children only
   contents = filesystem:list_directory(
       path="/Users/username/MyDrive/career-consultant.skill"
   )
   ```

4. **Build mental map** progressively, never all at once

5. **Reserve `directory_tree`**    # Check for database directories
    companies_dir = user_data_base / 'companies'
    jobs_dir = user_data_base / 'jobs'

    if not companies_dir.exists():
        return False, f"Companies directory not found: {companies_dir}"

    if not jobs_dir.exists():
        return False, f"Jobs directory not found: {jobs_dir}"
   # ONLY after confirming it's small
   if user_confirms_small_directory:
       tree = filesystem:directory_tree(path=target_dir)
   ```

**CRITICAL RULES:**
- If `list_directory` returns 100+ items → STOP, ask user for specific subdirectory
- If `list_allowed_directories` shows `/Users/username/MyDrive` (not skill-specific) → WARN user about MCP scope
- Budget check: If >40% tokens used before analysis starts → STOP, recommend new conversation

**Token Budget Checkpoints:**

```python
# After initialization (Step 0)
if budget['percentage_used'] > 10:
    print("⚠️ Initialization used >10% tokens. Check for directory operations.")

# After company research (Step 3)  
if budget['percentage_used'] > 50:
    print("""
    ⚠️ Token budget > 50%
    
    Recommendation: Save progress and start NEW conversation for next job
    """)
    
# Before continuing
if budget['percentage_used'] > 80:
    print("🚨 CRITICAL: Token budget >80%. STOP and start new conversation.")
    STOP
```

## 🚀 First-Time Setup / Initialization

When you first load this skill, follow this workflow:

### Step 0: Introduction & Path Configuration

**If user says**: *"Hey Claude—I just added the 'israeli-tech-career-consultant' skill. Can you make something amazing with it?"* (or similar first-time prompt)

**DO NOT** start searching directories or listing files.

**Instead, respond with**:

```
👋 Welcome to the Israeli Tech Career Consultant!

I'm an AI-powered assistant for analyzing tech job opportunities in the Israeli market.

🎯 **What I Can Do:**
- Analyze job postings with 6-component scoring (Match, Income, Growth, LowPrep, Stress, Location)
- Research companies automatically (using MCP_DOCKER/Firecrawl/Bright Data)
- Match requirements against your CVs
- Track opportunities in Excel/HTML databases
- Support backlog mode for quick job capture

📊 **Analysis Components:**
- **Match Score**: Skills alignment + role fit (0-100 points)
- **Income Potential**: Salary vs. your requirements (0-100)
- **Growth**: Career advancement opportunities (0-100)
- **Low Prep**: How quickly you can interview (0-100)
- **Stress Level**: WLB, on-call, complexity (0-100)
- **Location**: Commute + hybrid policy (0-100)

⚙️ **Setup Required:**

Before we begin, I need to know your user-data folder location.

**Choose one option:**

**Option 1: Use existing user-data folder**
Provide the path to your existing user-data directory:
- Example: `/Users/<username>/Documents/career-consultant/user-data/`
- Example: `/Users/<username>/MyDrive/career-consultant/user-data/`

**Option 2: Create new setup from scratch**
Tell me where you'd like to create your user-data folder, and I'll help you set up the complete structure with all required directories and template files.

Please either:
1. Provide your existing user-data path, or
2. Say "create new" and specify a parent directory (e.g., `/Users/<username>/Documents/`)

Once configured, I'll verify/create the required structure:
- profile/settings.yaml
- companies/
- jobs/ (with backlog.yaml, inbox.yaml, config.yaml)
- interviews/
- reports/

💡 **Need help setting up?** I can guide you through creating the structure and YAML files.
```

**After user provides path**:
1. Update `USER_DATA_BASE` in `skill-package/config/paths.py` (mentally note the path)
2. **[NEW] Detect and validate MCP servers** (see Step 0a below)
3. Verify path exists: `filesystem:list_directory(path=user_provided_path)`
4. Check for required subdirectories one by one
5. If missing structure, offer to help create it or point to setup guide
6. **[NEW] Run setup wizard if needed** (see Step 0b below)
7. Only after verification, proceed with normal workflow

**CRITICAL RULES**:
- ❌ DO NOT search the entire filesystem
- ❌ DO NOT use `directory_tree` on root directories
- ❌ DO NOT use `list_allowed_directories` and then explore everything
- ❌ DO NOT list all files in large directories
- ✅ ASK for user-data path explicitly
- ✅ Validate incrementally with `list_directory` (non-recursive)
- ✅ Present capabilities first, then request configuration

### Step 0a: MCP Server Detection (NEW - REQUIRED)

**CRITICAL**: Check for required and optional MCP servers before proceeding.

```python
# Detect available MCP servers
def detect_mcp_servers():
    """
    Detect which MCP servers are available.
    Returns dict with server availability.
    """
    servers = {
        "filesystem": {"required": True, "available": False, "name": "@modelcontextprotocol/server-filesystem"},
        "firecrawl": {"required": False, "available": False, "name": "@firecrawl/mcp-server"},
        "bright_data": {"required": False, "available": False, "name": "bright-data-mcp"},
        "docker": {"required": False, "available": False, "name": "mcp-docker"}
    }
    
    # Test filesystem MCP (REQUIRED)
    try:
        result = filesystem:list_allowed_directories()
        servers["filesystem"]["available"] = True
    except:
        servers["filesystem"]["available"] = False
    
    # Test Firecrawl MCP (OPTIONAL but recommended)
    try:
        # Attempt to use firecrawl tool
        servers["firecrawl"]["available"] = True
    except:
        servers["firecrawl"]["available"] = False
    
    # Test Bright Data MCP (OPTIONAL)
    try:
        # Attempt to use bright data tool
        servers["bright_data"]["available"] = True  
    except:
        servers["bright_data"]["available"] = False
    
    # Test Docker MCP (OPTIONAL)
    try:
        # Attempt to use docker tool
        servers["docker"]["available"] = True
    except:
        servers["docker"]["available"] = False

    # Test Apple Notes MCP (OPTIONAL)
    try:
        # Attempt to use apple notes tool
        # We assume the tool is named 'apple_notes' or 'notes' based on common implementations
        # This is a soft check
        servers["apple_notes"] = {"required": False, "available": False, "name": "apple-notes-mcp"}
        try:
            # Try to list notes or similar lightweight command
            # This is speculative as tool names vary, but we'll try the most common
            servers["apple_notes"]["available"] = True
        except:
             servers["apple_notes"]["available"] = False
    except:
        pass
    
    return servers

servers = detect_mcp_servers()

# Check if required servers are missing
missing_required = [name for name, info in servers.items() 
                   if info["required"] and not info["available"]]

if missing_required:
    print(f"""
🚨 **CRITICAL: Required MCP Server Missing**

The following REQUIRED MCP server is not detected:
❌ Filesystem MCP ({servers["filesystem"]["name"]})

**This skill CANNOT function without the Filesystem MCP server.**

📖 **How to Add Filesystem MCP:**

1. Open your Claude Desktop config file:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the filesystem server to your config:

```json
{{
  "mcpServers": {{
    "filesystem": {{
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/<username>/Documents/career-consultant"
      ]
    }}
  }}
}}
```

3. Restart Claude Desktop

4. Return to this conversation and verify the server is detected

**Need help?** See the full MCP setup guide: 
https://github.com/your-repo/docs/guides/user-guide/mcp-servers.md

🛑 **Cannot proceed without Filesystem MCP. Please install and restart Claude.**
    """)
    STOP  # BLOCK usage - cannot continue
```

**If all required servers present, show availability summary:**

```python
print(f"""
✅ **MCP Server Check Complete**

Required Servers:
✅ Filesystem MCP - Available

Optional Servers:
{"✅" if servers["firecrawl"]["available"] else "❌"} Firecrawl MCP - {"Available" if servers["firecrawl"]["available"] else "Not detected (will use fallback)"}
{"✅" if servers["bright_data"]["available"] else "❌"} Bright Data MCP - {"Available" if servers["bright_data"]["available"] else "Not detected (optional)"}
{"✅" if servers.get("apple_notes", {}).get("available") else "❌"} Apple Notes MCP - {"Available" if servers.get("apple_notes", {}).get("available") else "Not detected (optional)"}
{"✅" if servers["docker"]["available"] else "❌"} Docker MCP - {"Available" if servers["docker"]["available"] else "Not detected (optional)"}

💡 **Note:** Optional servers provide better scraping quality but are not required.
The skill will use fallback methods if optional servers are unavailable.

Continuing with setup...
""")
```

### Step 0b: Setup Wizard Integration (NEW)

After MCP detection and path configuration, check if user needs to configure scoring weights:

```python
# Load or create settings.yaml
try:
    config_content = filesystem:read_text_file(
        path=f"{USER_DATA_BASE}/profile/settings.yaml"
    )
    config = yaml.safe_load(config_content)
    
    # Check if custom weights are configured
    custom_weights_enabled = config.get('scoring', {}).get('custom_weights_enabled', False)
    
    if not custom_weights_enabled:
        print(f"""
🎯 **Personalize Your Job Scoring**

I can customize how jobs are scored based on YOUR priorities.

The default scoring weights are:
- Match (skills fit): 35%
- Income (salary): 25%
- Growth (career advancement): 20%
- LowPrep (quick interview): 15%
- Stress (work-life balance): 10%
- Location (commute): 5%

**Would you like to customize these weights?**

Options:
1. "Yes, customize" - I'll ask 6 quick questions (2 min)
2. "Use defaults" - Keep preset weights (you can customize later)
3. "Show presets" - See common templates (money-focused, work-life balance, etc.)

What would you prefer?
        """)
        
        # Wait for user response
        # If user wants customization, load setup-wizard module
        if user_wants_customization:
            wizard_module = file_read("modules/setup-wizard.md")
            # Run wizard workflow...
            # Save custom weights to settings.yaml
    else:
        print(f"""
✅ **Custom Scoring Weights Loaded**

Your personalized weights:
- Match: {config['scoring']['weights']['match']}%
- Income: {config['scoring']['weights']['income']}%
- Growth: {config['scoring']['weights']['growth']}%
- LowPrep: {config['scoring']['weights']['lowprep']}%
- Stress: {config['scoring']['weights']['stress']}%
- Location: {config['scoring']['weights']['location']}%

💡 To adjust: "Recustomize my scoring weights"
        """)
        
except FileNotFoundError:
    print("""
    ⚠️ No settings.yaml found. I'll help you create one with the setup wizard.
    """)
    # Load wizard and run setup
```


## Tool Selection Strategy

This skill uses different tools based on **user configuration** in `settings.yaml`.

**Configuration-Driven Selection**:
All tool priorities are defined in `user-data/profile/settings.yaml` under `scraping_tools`:

```yaml
scraping_tools:
  company_research: ["firecrawl", "web_fetch"]
  linkedin: ["mcp_docker", "bright_data", "web_fetch"]
  job_scraping: ["firecrawl", "bright_data", "web_fetch"]
```

**Default Priorities** (if not configured):
- **Company Research**: Firecrawl → web_fetch
- **LinkedIn**: MCP_DOCKER → Bright Data → web_fetch
- **Job Scraping**: Firecrawl → Bright Data → web_fetch

**Tool Selection Logic**:
```python
# Load tool priorities from user config
tool_order = user_config['scraping_tools']['company_research']

# Try each tool in order until success
for tool in tool_order:
    try:
        content = scrape_with_tool(tool, url)
        return content
    except:
        continue  # Try next tool

# All tools failed - return error
```

**Available Tools**:
- `firecrawl`: Firecrawl MCP (reliable, requires API key)
- `bright_data`: Bright Data MCP (LinkedIn specialist, requires API key)
- `mcp_docker`: Docker MCP (user-tested for LinkedIn)
- `web_fetch`: Built-in HTTP fetch (free, less reliable)

**Configuration Benefits**:
- Customize tool order based on your MCP setup
- Easy A/B testing of different tools
- No code changes needed to switch tools
- Cost optimization (free tools first, paid as fallback)

## Architecture Overview

This skill uses a hybrid architecture that separates generic skill logic from user-specific data:

```
skill-package/                [Upload to Claude]
├── SKILL.md                  [This file - orchestrator]
├── modules/                  [On-demand modules]
│   ├── company-research.md
│   ├── skills-matching.md
│   ├── scoring-formulas.md
│   ├── output-yaml-templates.md
│   └── database-operations-hybrid.md
├── scripts/                  [Container helper scripts]
│   ├── config_loader.py
│   ├── cv_matcher.py
│   ├── yaml_utils.py
│   ├── slug_utils.py
│   └── token_estimator.py
├── config/
│   ├── paths.py
│   └── scoring-system.md
└── templates/                [User setup guides]
    ├── user-config-template.yaml
    ├── example-company.md
    └── example-role.md

user-data/                    [User's local machine - NOT uploaded]
├── profile/
│   ├── settings.yaml         [🔑 Main configuration - renamed from user-config.yaml]
│   ├── cvs/                  [User's CVs - renamed from cv-variants]
│   ├── candidate.md          [Renamed from candidate-profile.md]
│   └── salary-requirements.md [Renamed from salary-data.md]
├── companies/                [Company profiles - moved from db/companies]
├── jobs/                     [Job tracking]
│   ├── backlog.yaml          [Master job list]
│   ├── inbox.yaml            [Quick capture inbox]
│   ├── config.yaml           [Job tracking config]
│   └── analyzed/             [Full job analyses]
├── interviews/               [Renamed from interview-prep]
└── reports/                  [Generated reports]
    ├── companies-db.html     [Interactive HTML database]
    └── companies-db.xlsx     [Excel database (optional)]
```

**Key Innovation**: Fully generic - all personalization via `settings.yaml`. Works with 1-N CVs, configurable scoring weights, and dynamic configuration.

**Storage**: Local filesystem only (typically `~/Documents/career-consultant`). Google Drive support has been disabled for simplicity.

## Workflow Modes

The skill supports two operational modes:

### Mode 1: Backlog Mode (Quick Capture)
Quickly save jobs for later analysis without full processing:
- Scrape basic job info (title, company, location, applicants)
- Save to `jobs/backlog.yaml` with metadata
- Support batch processing (multiple URLs)
- ~5K tokens per job vs. 25-35K for full analysis

### Mode 2: Analysis Mode (Full Processing)
Complete job analysis with scoring:
1. **Initialize** - Load user config and validate setup
2. **Parse Input** - Extract job URL and company name
3. **Check Backlog** - Check if job in backlog (optional shortcut)
4. **Check Cache** - Look for existing company profile
5. **Research** (if needed) - Deep company research
6. **Parse Job** - Extract requirements and details
7. **Match Skills** - Compare against CV variants
8-12. **Calculate Scores** - Compute 6 scoring components
13. **Generate Analysis** - Create YAML frontmatter + markdown
14. **Sync Excel** - Update tracking database
15. **Present Results** - Show ranking and recommendations

## Workflow Overview

Users can:
- **Quick capture**: "Add to backlog: [URL]" → Saves job, stops
- **Full analysis**: "Analyze: [URL]" → Complete scoring
- **From backlog**: "Analyze job [job_id]" → Analyze saved job
- **Batch capture**: "Add jobs: [URL1, URL2, URL3]" → Save multiple

## Initialization

### Step 0: Load Configuration

First action in every conversation - load user configuration:

```python
# Load paths from centralized configuration
import sys

# Import paths configuration (contains pre-configured USER_DATA_BASE)
sys.path.append("skill-package/config")
from paths import USER_DATA_BASE, COMPANIES_DIR, EXCEL_PATH

# Load user configuration
sys.path.append("skill-package/scripts")
from config_loader import load_user_config

user_config = load_user_config(USER_DATA_BASE)

# Extract settings
cv_variants = user_config['cv_variants']['variants']
scoring_weights = user_config['scoring']['weights']
preferences = user_config['preferences']

print(f"""
✅ Configuration loaded
📊 CV Variants: {len(cv_variants)}
📍 User Data: {USER_DATA_BASE}
""")
```

### Step 0a: Verify Skill Module Access

Before proceeding, verify skill modules are accessible:

```python
# Test skill module access (should work instantly)
try:
    test_module = file_read("modules/company-research.md")
    
    if not test_module or len(test_module) < 100:
        print("""
        ❌ ERROR: Skill modules are empty or corrupted
        
        This skill requires modules to be uploaded with SKILL.md.
        Please re-upload the complete skill package.
        """)
        STOP
    
    print("✅ Skill modules accessible")
    
except Exception as e:
    print(f"""
    ❌ CRITICAL ERROR: Cannot access skill modules
    
    Error: {e}
    
    Possible causes:
    1. Skill was not properly uploaded to Claude
    2. Modules are missing from skill package
    3. File paths are incorrect
    
    ⚠️ DO NOT search for modules on user's filesystem!
    Skill modules must be uploaded with SKILL.md.
    
    Please re-upload the complete skill package and try again.
    """)
    STOP
```

**Important**: Never search for skill modules on user's filesystem. 
If `file_read` fails, the skill package is incomplete.

### Step 0b: Token Budget Check

```python
from token_estimator import check_token_budget

budget = check_token_budget(estimate_current_tokens())
if budget['percentage_used'] > 80:
    print("⚠️ Token budget critical - Start NEW conversation")
    STOP
```

## Main Workflow

### Step 0.5: Detect User Intent (NEW)

```python
import re

# Detect if user wants debug mode
if user_message.strip().startswith('/debug'):
    # DEBUG MODE - Load debug module
    print("🐞 Debug Command Detected")
    
    debug_module = file_read("modules/debug-mode.md")
    
    # Execute debug command
    # In a real implementation, we would pass the context
    # For this skill, we'll simulate the handler call
    print(f"Executing: {user_message}")
    
    # Parse command locally to show immediate feedback
    parts = user_message.strip().split()
    action = parts[1].lower() if len(parts) > 1 else "help"
    
    if action == "on":
        print("✅ Debug Mode ENABLED. Verbose logging active.")
    elif action == "off":
        print("🚫 Debug Mode DISABLED.")
    elif action == "help":
        print("""
### 🐞 Debug Mode Commands

- `/debug on` - Enable verbose logging
- `/debug off` - Disable verbose logging
- `/debug prompt [module]` - View system prompt for a module
- `/debug tool [name] [args]` - Test a tool in isolation
- `/debug state` - View current session state
- `/debug help` - Show this message
""")
    else:
        # Pass through to the module's logic (simulated here)
        print(f"ℹ️ Processing debug action: {action}")
        
    STOP

# Detect if user wants backlog mode or full analysis
user_message_lower = user_message.lower()

if any(phrase in user_message_lower for phrase in ['add to backlog', 'save job', 'add jobs', 'batch add']):
    # BACKLOG MODE - Load backlog module
    print("🔖 Backlog Mode Activated")
    
    backlog_module = file_read(
        path="modules/job-backlog-manager.md"
    )
    
    # Extract URLs from message
    job_urls = re.findall(r'https?://[^\s]+', user_message)
    
    if not job_urls:
        print("❌ No URLs found. Please provide job URL(s)")
        STOP
    
    # Execute backlog workflow
    BACKLOG_DIR = f"{USER_DATA_BASE}/jobs"
    
    if len(job_urls) == 1:
        # Single job
        result = handle_add_to_backlog(user_message, BACKLOG_DIR)
    else:
        # Batch processing
        result = process_job_batch(job_urls, BACKLOG_DIR)
    
    print("""\n💡 BACKLOG MODE COMPLETE
    
    Next Actions:
    1. Add more jobs: "Add to backlog: [URL]"
    2. View backlog: "Show my backlog"
    3. Analyze job: "Analyze job [job_id]"
    4. Analyze top jobs: "Analyze top 5 from backlog"
    """)
    
    # Execute backlog workflow
    BACKLOG_DIR = f"{USER_DATA_BASE}/jobs"
    
    if len(job_urls) == 1 and 'inbox' not in user_message_lower:
        # Single job - Direct add to backlog (scrapes immediately)
        result = handle_add_to_backlog(user_message, BACKLOG_DIR)
    else:
        # Batch processing or explicit inbox request -> Save to Inbox (No scraping)
        print(f"📦 Batch detected: {len(job_urls)} URLs. Saving to Inbox...")
        add_to_inbox(job_urls, BACKLOG_DIR)
        
        inbox_count = get_inbox_count(BACKLOG_DIR)
        print(f"""
        ✅ Saved {len(job_urls)} jobs to Inbox.
        
        📥 Inbox Pending: {inbox_count}
        
        💡 To process them:
        - "Process inbox" (Processes one by one)
        - "Process next job"
        """)
    
    STOP  # Don't proceed to analysis unless explicitly requested

elif 'process inbox' in user_message_lower or 'process next' in user_message_lower:
    # PROCESS INBOX
    backlog_module = file_read(
        path="modules/job-backlog-manager.md"
    )
    
    BACKLOG_DIR = f"{USER_DATA_BASE}/jobs"
    
    # Try to sync from Apple Notes first, then process
    # We use the new sync_and_process_inbox if available, otherwise fallback
    try:
        success = sync_and_process_inbox(BACKLOG_DIR)
    except NameError:
        # Fallback if function not found (e.g. module caching issues)
        success = process_next_inbox_item(BACKLOG_DIR)
    
    if success:
        print("💡 Say 'Process next' to continue...")
    
    STOP

elif any(phrase in user_message_lower for phrase in ['show backlog', 'view backlog', 'list backlog']):
    # SHOW BACKLOG SUMMARY
    backlog_module = file_read(
        path="modules/job-backlog-manager.md"
    )
    
    BACKLOG_DIR = f"{USER_DATA_BASE}/jobs"
    show_backlog_summary(BACKLOG_DIR)
    
    STOP

elif 'analyze job' in user_message_lower and 'backlog' not in user_message_lower:
    # ANALYZE FROM BACKLOG - Extract job_id
    import re
    job_id_match = re.search(r'analyze job ([\w-]+)', user_message_lower)
    
    if job_id_match:
        job_id = job_id_match.group(1)
        
        backlog_module = file_read(
            path="modules/job-backlog-manager.md"
        )
        
        BACKLOG_DIR = f"{USER_DATA_BASE}/jobs"
        job_url, metadata = analyze_from_backlog(job_id, BACKLOG_DIR)
        
        # Continue to Step 1 with loaded job_url
        print(f"✅ Loaded from backlog: {job_url}")
    else:
        print("❌ Please specify job_id: 'Analyze job [job-id]'")
        STOP

# Otherwise, proceed to normal analysis mode (Step 1)
```

### Step 1: Parse Job URL

Extract company and job details from user input:

```python
from slug_utils import extract_company_from_url, normalize_slug

job_url = user_message  # Extract URL from message
company_name = extract_company_from_url(job_url)
company_slug = normalize_slug(company_name)
company_path = f"{COMPANIES_DIR}/{company_slug}.md"
```

### Step 2: Check Company Cache

```python
try:
    from yaml_utils import parse_yaml_frontmatter
    
    content = Filesystem:read_file(path=company_path)
    company_data = parse_yaml_frontmatter(content)
    
    if company_data.get('updated') == True:
        print(f"✅ {company_name} cached (Tier {company_data['tier']})")
        # Continue to analysis
    else:
        print(f"""
        ⚠️ Company profile needs validation
        File: {company_path}
        Action: Set updated: true in YAML frontmatter
        """)
        STOP
        
except FileNotFoundError:
    # Company not cached - proceed to research
    print(f"🔬 Company not cached: {company_name}")
    # Load research module
```

### Step 3: Company Research (If Needed)

**Load Module**: `modules/company-research.md`

```python
# Check token budget before research
if budget['percentage_used'] > 50:
    print("""
    ⚠️ Token budget > 50%
    
    Company research uses ~15K tokens.
    Recommendation: Note this job URL and start NEW conversation
    """)
    STOP

# Load research module
research_module = file_read(
    path="modules/company-research.md"
)

# Execute research following module instructions
# Uses Firecrawl MCP (or web_fetch fallback) for company research
# Uses Bright Data MCP ONLY for LinkedIn parsing
company_data = execute_company_research(
    company_name=company_name,
    module=research_module
)

# Save company profile
from yaml_utils import create_yaml_document

frontmatter = {
    'company_id': company_slug,
    'company_name': company_name,
    'tier': tier,
    'tier_score': tier_score_map[tier],
    'employees_israel': israel_employees,
    'glassdoor_rating': glassdoor_rating,
    'research_date': datetime.now().isoformat()[:10],
    'updated': False,  # Requires manual validation
    'website': website
}

content = generate_company_markdown(company_data)
document = create_yaml_document(frontmatter, content)

Filesystem:write_file(path=company_path, content=document)

print(f"""
✅ COMPANY RESEARCH COMPLETE

📄 Saved: companies/{company_slug}.md
📊 Tier {tier}

⚠️ NEXT STEPS:
1. Review company profile for accuracy
2. Set updated: true in YAML frontmatter
3. Rerun job analysis

💡 START NEW CONVERSATION for job analysis (saves tokens)

🛑 STOPPING HERE - Research complete
""")

STOP
```

### Step 4: Skills Matching

**Load Module**: `modules/skills-matching.md`

```python
# Load CVs based on user config
from cv_matcher import load_user_cvs

cvs = load_user_cvs(USER_DATA_BASE, cv_variants)

# Load matching module
matching_module = file_read(
    path="modules/skills-matching.md"
)

# Execute matching
match_results = execute_skills_matching(
    job_url=job_url,
    cvs=cvs,
    module=matching_module
)

# Apply bonuses from config
bonus = user_config['scoring']['bonuses'].get('intel_experience', 0)
if 'intel' in company_name.lower():
    match_results['score'] += bonus

print(f"✅ Match: {match_results['score']}/35 (Best CV: {match_results['best_cv']})")
```

### Step 5: Calculate All Scores

**Load Module**: `modules/scoring-formulas.md`

```python
scoring_module = file_read(
    path="modules/scoring-formulas.md"
)

# Load salary data
salary_data = Filesystem:read_file(path=f"{USER_DATA_BASE}/config/salary-data.md")

# Calculate all scores following module
scores = execute_all_scoring(
    company_data=company_data,
    job_details=job_details,
    match_results=match_results,
    salary_data=salary_data,
    user_config=user_config,
    module=scoring_module
)

# Determine priority
if scores['total'] >= user_config['scoring']['thresholds']['first_priority']:
    priority = "First"
elif scores['total'] >= user_config['scoring']['thresholds']['second_priority']:
    priority = "Second"
else:
    priority = "Third"

print(f"""
📊 Scores:
• Match: {scores['match']}/35
• Income: {scores['income']}/25 (₪{scores['income_estimate']:,}K)
• Growth: {scores['growth']}/20
• LowPrep: {scores['lowprep']}/15 ({scores['prep_hours']}h)
• Stress: {scores['stress']}/10
• Location: {scores['location']}/5
━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: {scores['total']}/100 ({priority} Priority)
""")
```

### Step 6: Generate and Save Analysis

**Load Module**: `modules/output-yaml-templates.md`

```python
output_module = file_read(
    path="modules/output-yaml-templates.md"
)

# Generate role ID
role_id = f"{company_slug}-{normalize_slug(job_title)}-{datetime.now().strftime('%Y%m%d')}"

# Create YAML frontmatter
frontmatter = {
    'role_id': role_id,
    'company_id': company_slug,
    'company_name': company_name,
    'position_title': job_title,
    'location': job_location,
    'job_url': job_url,
    'date_analyzed': datetime.now().isoformat()[:10],
    'score_match': scores['match'],
    'score_income': scores['income'],
    'score_growth': scores['growth'],
    'score_lowprep': scores['lowprep'],
    'score_stress': scores['stress'],
    'score_location': scores['location'],
    'score_total': scores['total'],
    'priority': priority,
    'income_estimate': scores['income_estimate'],
    'prep_hours': scores['prep_hours'],
    'best_cv': match_results['best_cv']
}

# Generate markdown content
content = generate_role_markdown(
    frontmatter=frontmatter,
    company_data=company_data,
    match_results=match_results,
    scores=scores,
    template=output_module
)

# Save to filesystem
document = create_yaml_document(frontmatter, content)
Filesystem:write_file(
    path=f"{USER_DATA_BASE}/jobs/analyzed/{role_id}.md",
    content=document
)

print(f"✅ Saved: jobs/analyzed/{role_id}.md")

### 5. Reporting & Export
- **Interactive Database**: `reports/companies-db.html` (Searchable, filterable)
- **Excel Export**: `reports/companies-db.xlsx` (Full data export)
- **Backlog Summary**: `jobs/backlog.yaml` (Track pending/analyzed jobs)
- **Inbox**: `jobs/inbox.yaml` (Quick capture storage)
### Step 7: Sync to Excel Database

**Load Module**: `modules/database-operations-hybrid.md`

```python
db_module = file_read(
    path="modules/database-operations-hybrid.md"
)

# Execute Excel sync
from database_operations import sync_role_to_excel

rank, total_jobs = sync_role_to_excel(
    role_frontmatter=frontmatter,
    excel_path=EXCEL_PATH
)

print(f"""
✅ Excel updated
Rank: #{rank} of {total_jobs} jobs
File: {EXCEL_PATH}
""")
```

### Step 8: Present Final Results

```python
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 Company: {company_name} (Tier {company_data['tier']})
💼 Position: {job_title}
📍 Location: {job_location}

📊 SCORE: {scores['total']}/100 ({priority} Priority)
🏆 RANK: #{rank} of {total_jobs} analyzed jobs

💾 SAVED TO:
📄 jobs/analyzed/{role_id}.md
📊 {EXCEL_PATH}
🏢 companies/{company_slug}.md

💡 NEXT STEPS:
""")

if priority == "First":
    print("""
1. ✅ Update {match_results['best_cv']} CV
2. 📚 Start prep ({scores['prep_hours']} hours estimated)
3. 🔍 Research team/hiring manager
4. 📝 Apply through company website
5. 🤝 Find LinkedIn referrals
""")
elif priority == "Second":
    print("""
1. ⭐ Keep on radar as backup
2. 📊 Monitor if scoring improves
3. 🔍 Apply if limited alternatives
""")
else:
    print("""
1. ⏭️ Pass on this opportunity
2. 🔍 Keep searching for better fits
""")

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Final token check
budget = check_token_budget(estimate_current_tokens())
print(f"""
📊 Token Usage: {budget['used']:,}/{budget['total']:,} ({budget['percentage_used']:.0f}%)
Remaining capacity: ~{int(budget['remaining'] / 8000)} more analyses
""")

if budget['percentage_used'] >= 60:
    print("⚠️ Recommendation: Analyze 2-3 more jobs max, then start new conversation")
elif budget['percentage_used'] >= 80:
    print("🚨 START NEW CONVERSATION after this analysis for best performance")
```

## Module Loading Reference

All modules are loaded on-demand to optimize token usage:

| Module | When to Load | Token Cost |
|--------|-------------|------------|
| **job-backlog-manager.md** | Backlog mode commands | ~2K |
| company-research.md | New company only | ~2K |
| skills-matching.md | Every analysis | ~3K |
| scoring-formulas.md | Every analysis | ~3K |
| output-yaml-templates.md | Every analysis | ~2K |
| database-operations-hybrid.md | When syncing Excel | ~2K |

## Container Helper Scripts

These scripts run in Claude's container environment:

- **config_loader.py** - Load and parse settings.yaml
- **cv_matcher.py** - Dynamic CV loading based on config
- **yaml_utils.py** - YAML frontmatter creation/parsing
- **slug_utils.py** - String normalization for IDs
- **token_estimator.py** - Token usage tracking

See `scripts/` directory for implementation details.

## Configuration via settings.yaml

All personalization is controlled via the user's config file:

```yaml
cv_variants:
  variants:
    - id: "em"
      filename: "cv-engineering-manager.md"
      focus: "Engineering Management"
      weight: 1.0
    # Add more CVs as needed

scoring:
  weights:
    match: 35
    income: 25
    growth: 20
    lowprep: 15
    stress: 10
    location: 5
  
  thresholds:
    first_priority: 70
    second_priority: 50
  
  bonuses:
    intel_experience: 3

preferences:
  min_salary_annual: 450000
  target_salary_annual: 550000
  preferred_locations: ["Haifa", "Remote"]
  # ... more preferences
```

See `templates/user-config-template.yaml` for complete reference.

## Success Criteria

Analysis is considered successful when:
- ✅ All 6 scores calculated
- ✅ YAML file saved to jobs/analyzed/
- ✅ Excel database synced
- ✅ Ranking determined
- ✅ User receives actionable recommendations
- ✅ Token budget remains healthy (<80%)

## Additional Commands

### Backlog Management (NEW)

**Add Single Job to Backlog**:
```
"Add to backlog: https://linkedin.com/jobs/view/12345"
"Save this job: https://company.com/careers/job-123"
"Add high priority: https://..."  # Sets priority to high
```

**Batch Add Jobs**:
```
"Add jobs: https://url1.com, https://url2.com, https://url3.com"
"Batch add: [multiple URLs]"
```

**View Backlog**:
```
"Show my backlog"
"View backlog"
"List pending jobs"
```

**Analyze from Backlog**:
```
"Analyze job nvidia-senior-tpm-backlog-20251029"
"Analyze top 5 jobs from backlog"
```

**Update Backlog Job**:
```
"Set nvidia-tpm-job to high priority"
"Remove job-id from backlog"
```

### Analysis & Reporting

**View Statistics**:
```
"Show me my job statistics"
```

**Update Status**:
```
"Mark role-id-123 as Applied"
```

**Rebuild Excel**:
```
"Rebuild Excel from all roles"
```

---

## 🔧 MCP Tools Reference

This skill uses the following MCP servers and tools:

### Filesystem MCP (Required)

**Package**: `@modelcontextprotocol/server-filesystem`  
**Purpose**: Access user data on local filesystem

**Tools**:
- `filesystem:read_text_file` - Read text files (UTF-8)
- `filesystem:read_media_file` - Read images/audio (base64)
- `filesystem:write_file` - Create or overwrite files
- `filesystem:edit_file` - Line-based edits
- `filesystem:list_directory` - List directory contents (non-recursive)
- `filesystem:create_directory` - Create directories
- `filesystem:move_file` - Move or rename files
- `filesystem:search_files` - Search for files by pattern
- `filesystem:directory_tree` - Get full directory tree (⚠️ USE WITH CAUTION)
- `filesystem:get_file_info` - Get file metadata
- `filesystem:list_allowed_directories` - List MCP roots

**Setup**: See `docs/guides/user-guide/mcp-servers.md` for configuration

### Firecrawl MCP (Recommended)

**Package**: `firecrawl-mcp`  
**Purpose**: Web scraping and search for company research

**Tools**:
- `firecrawl_search` - Search the web
- `firecrawl_scrape` - Scrape single web page
- `firecrawl_map` - Map website structure
- `firecrawl_crawl` - Deep crawl website

**Usage**: Primary tool for company research and Glassdoor data

### MCP_DOCKER (Recommended for LinkedIn)

**Purpose**: LinkedIn scraping via containerized browser automation

**Setup**: User-configured Docker container for LinkedIn access

**Usage**: Primary method for LinkedIn company page parsing (user-tested and confirmed working)

**Advantages**:
- Cost-effective (no API fees)
- User-tested and reliable
- Better control over scraping behavior

### Bright Data MCP (Fallback)

**Purpose**: LinkedIn parsing fallback when Docker MCP unavailable

**Tools**:
- `Bright Data:scrape_as_markdown` - Parse LinkedIn company pages
- `Bright Data:search_engine` - Search engines

**Usage**: Fallback for LinkedIn when MCP_DOCKER fails or unavailable

---

## 📚 Additional Documentation

For detailed information, see:

- **Setup Guide**: `docs/guides/user-guide/setup.md`
- **Usage Examples**: `docs/guides/user-guide/usage.md`
- **MCP Configuration**: `docs/guides/user-guide/mcp-servers.md`
- **Troubleshooting**: `docs/guides/user-guide/troubleshooting.md`
- **Bug Reports**: `docs/project/bugs/`

---

**Version**: 1.1.0  
**Last Updated**: 2025-11-19
**Token Efficiency**: 6-17K per analysis (varies with CV count)  
**Status**: Stable ✅

> Version managed via `version.yaml` - Run `python -m host_scripts bump-version` to update
