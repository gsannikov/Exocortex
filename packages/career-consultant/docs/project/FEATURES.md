# Israeli Tech Career Consultant - Features Overview

Simplified overview of core system capabilities.

## Core Features

### 1. Job Analysis & Scoring
6-component scoring system (Match, Income, Growth, LowPrep, Stress, Location) evaluates opportunities against your profile. Scores 0-100 determine priority: First (≥54), Second (≥40), Third (<40).

### 2. Company Research
Automated research using MCP tools (Docker, Firecrawl, Bright Data). Caches company data locally to speed up future job analyses. Extracts: tier, employee count, tech stack, culture, market position.

### 3. Skills Matching
Multi-CV comparison against job requirements. Identifies skill gaps, calculates match percentage, suggests best CV variant for each role.

### 4. Job Backlog System
Quick-save jobs (5K tokens) for later analysis. Batch processing, priority tagging, metadata extraction. Analyze when ready with cached company data.

### 5. Database & Reporting
Generated outputs:
- **HTML Database**: Interactive, filterable job tracker
- **Excel Export**: Spreadsheet for offline analysis
- **Markdown Files**: Source of truth (YAML frontmatter + content)

### 6. Configurable Tool Selection
User-defined scraping tool priorities via `settings.yaml`. Supports MCP_DOCKER, Firecrawl, Bright Data, web_fetch with automatic fallback.

## Implementation Status

✅ **Production Ready**:
- Job analysis workflow
- Company research & caching
- Skills matching (multi-CV)
- Backlog manager
- HTML/Excel database
- Configurable tools

🚧 **Future Enhancements**:
- Interview preparation templates
- Resume generation per job
- Application tracking
- Career discovery chat
