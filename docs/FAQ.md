# Frequently Asked Questions (FAQ)

Common questions about using and developing Claude Skills.

---

## Table of Contents

- [General](#general)
- [Installation & Setup](#installation--setup)
- [Using Skills](#using-skills)
- [Developing Skills](#developing-skills)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## General

### What is the Claude Skills Ecosystem?

A monorepo containing 6 production-ready skills that turn Claude into a persistent productivity engine. Skills include job search assistance, reading list management, idea capture, voice memo transcription, document search, and social media post generation.

### How is this different from just using Claude?

Claude alone has no persistent memory—context resets every conversation. These skills:
- Store data in local YAML databases
- Enable semantic search across your information
- Provide specialized workflows (job scoring, STAR stories, RAG, etc.)
- Integrate with Apple Notes for mobile capture

### Is my data secure?

Yes. All data is stored locally in `~/MyDrive/claude-skills-data/` on your machine. Nothing is sent to external services except:
- Website scraping (through Firecrawl or direct HTTP)
- Claude API calls (standard Claude.ai usage)

### Do I need coding skills to use this?

**As a user**: No. Just run the installer and use natural language commands.

**As a developer**: Basic familiarity with Python, YAML, and Markdown helps but isn't required.

---

## Installation & Setup

### How do I install?

One command:
```bash
curl -fsSL https://raw.githubusercontent.com/gsannikov/claude-skills/main/install.sh | bash
```

This sets up the monorepo, installs dependencies, and configures Claude Desktop.

### What are the prerequisites?

- **Claude Desktop** app
- **Python 3.8+** (for local scripts)
- **Git** (for cloning)
- **macOS/Linux** (Windows support experimental)

### Where is everything installed?

- **Code**: `~/MyDrive/claude-skills/`
- **User Data**: `~/MyDrive/claude-skills-data/`
- **Claude Config**: `~/Library/Application Support/Claude/`

### Can I move the installation directory?

Yes, but you'll need to update:
1. Claude Desktop config (`claude_desktop_config.json`)
2. Skill path references in SKILL.md files
3. User data path (can be anywhere, configured per skill)

### How do I update to the latest version?

```bash
cd ~/MyDrive/claude-skills
git pull origin main
```

Then restart Claude Desktop.

---

## Using Skills

### How do I capture items from my phone?

All skills support **Apple Notes** inbox capture:

1. Create note: "Job Links Inbox" (job-analyzer)
2. Paste URLs or text
3. In Claude: `process inbox`

Skills automatically sync and process items.

### What if I don't use Apple Notes?

You can use direct commands:
- job-analyzer: `add to backlog: https://...`
- reading-list: `add article: https://...`
- ideas-capture: `expand: My idea text`

### How do I see what's in my database?

Each skill stores data in:
```
~/MyDrive/claude-skills-data/{skill-name}/db/
```

Files are human-readable YAML. You can open them in any text editor.

### Can I edit the YAML files manually?

Yes, but be careful:
- Maintain proper YAML syntax
- Don't change structure (keys, types)
- Back up before editing
- Use the skill commands when possible

### How do I back up my data?

```bash
# Quick backup
cp -r ~/MyDrive/claude-skills-data ~/Backups/claude-skills-data-$(date +%Y%m%d)

# Or use git (if data directory is a git repo)
cd ~/MyDrive/claude-skills-data
git add .
git commit -m "Backup $(date)"
```

### What if I hit the context window limit?

Skills use **progressive loading**:
- Only load necessary data
- Summarize old data
- On-demand module loading

If you still hit limits:
- Archive old items
- Split large databases
- Process in batches

---

## Developing Skills

### How do I create a new skill?

1. **Use the generator**:
   ```bash
   python shared/scripts/skill_generator.py --name my-skill --patterns inbox,database
   ```

2. **Or manually**: Copy existing skill structure

3. **Required files**:
   - `SKILL.md` - Main specification
   - `README.md` - Documentation
   - `CHANGELOG.md` - Version history
   - `version.yaml` - Metadata

### What patterns should I follow?

See existing skills for examples:

**Inbox Pattern** (reading-list, job-analyzer):
- Apple Notes integration
- Batch processing
- Item deduplication

**Database Pattern** (all skills):
- YAML storage
- Structured data
- Append-only logs

**Scoring Pattern** (job-analyzer, ideas-capture):
- Multi-dimensional scoring
- Weighted components
- Tier classification

**RAG Pattern** (local-rag):
- Document chunking
- Vector embeddings
- Semantic search

### How do I handle large data?

**Token Budget Management**:
1. **Progressive loading**: Load summaries first, details on demand
2. **On-demand modules**: Separate heavy logic into modules
3. **Chunking**: Process batches, not all at once
4. **Archiving**: Move old data out of active context

### Can skills talk to each other?

Currently: No direct skill-to-skill communication.

**Workarounds**:
- Shared user data directory
- Cross-reference by ID
- Manual data export/import

**Future**: Planned for v2.0 (cross-skill intelligence)

### How do I test my skill?

1. **Manual testing**: Upload to Claude, run commands
2. **YAML validation**: Check syntax
3. **Python linting**: If using scripts
4. **Integration test**: Full workflow end-to-end

---

## Troubleshooting

### "Firecrawl API error"

**Cause**: Rate limit or API key issue

**Fix**:
- Wait a minute, try again
- Check Firecrawl credits
- Use fallback: `web_fetch` instead

### "Apple Notes fetch timeout"

**Cause**: Too many items in inbox (\u003e100)

**Fix**:
- Process in smaller batches
- Clear old items from inbox
- Use direct commands instead

### "YAML parsing error"

**Cause**: Malformed YAML file

**Fix**:
1. Check error message for line number
2. Validate YAML: `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`
3. Restore from backup if needed

### "Module not found"

**Cause**: Missing Python dependencies

**Fix**:
```bash
# For job-analyzer
pip install pandas openpyxl

# For local-rag
pip install chromadb sentence-transformers

# Core
pip install pyyaml
```

### "Context window exceeded"

**Cause**: Too much data loaded

**Fix**:
- Archive old items
- Use on-demand modules
- Process fewer items at once
- Check SKILL.md for token estimates

### Command not recognized

**Cause**: Typo or skill not loaded

**Fix**:
1. Check command spelling in README
2. Verify skill is uploaded to Claude
3. Restart Claude Desktop
4. Check version compatibility

---

## Best Practices

### Data Management

**DO**:
- ✅ Back up data regularly
- ✅ Archive old items
- ✅ Keep YAML files under 10,000 lines
- ✅ Use meaningful IDs

**DON'T**:
- ❌ Edit YAML while skill is running
- ❌ Store sensitive credentials in YAML
- ❌ Commit user data to git

### Performance

**DO**:
- ✅ Process items in batches
- ✅ Use on-demand modules
- ✅ Archive inactive data
- ✅ Clear Apple Notes inbox regularly

**DON'T**:
- ❌ Load entire database every command
- ❌ Scrape 100+ URLs at once
- ❌ Keep massive transcripts in memory

### Security

**DO**:
- ✅ Store user data outside repo
- ✅ Use `.gitignore` for sensitive files
- ✅ Review scraped content before storing
- ✅ Keep dependencies updated

**DON'T**:
- ❌ Commit API keys or tokens
- ❌ Share user database files
- ❌ Store passwords in YAML

### Development

**DO**:
- ✅ Follow existing skill patterns
- ✅ Document all commands
- ✅ Include examples in README
- ✅ Update CHANGELOG.md

**DON'T**:
- ❌ Break existing skill structure
- ❌ Add large dependencies unnecessarily
- ❌ Skip version bumping
- ❌ Forget to update documentation

---

## AlignTrue (Cross-Platform AI)

### What is AlignTrue?

AlignTrue keeps AI instructions in sync across multiple platforms (Claude, OpenAI Codex, Cursor, Google Antigravity). You write rules once in `.aligntrue/rules/` and it generates the correct format for each platform.

### Do I need to install AlignTrue?

Only if you're contributing to the repo. Users don't need it—the generated files (`CLAUDE.md`, `AGENTS.md`) are already committed.

### Which file should I edit?

**Always edit** `.aligntrue/rules/CLAUDE.md` (the source file).
**Never edit** `CLAUDE.md`, `AGENTS.md`, or `.cursorrules` directly—they're auto-generated.

---

## Still Have Questions?

- **Issues**: https://github.com/gsannikov/claude-skills/issues
- **Discussions**: https://github.com/gsannikov/claude-skills/discussions
- **Email**: [See GitHub profile]

Use the **Question** issue template for new questions!
