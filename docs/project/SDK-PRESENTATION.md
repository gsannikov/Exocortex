# Claude Skills SDK Template
## Building Production-Ready Claude Skills

**Presentation Guide**  
Version 1.0.0 | 2025-11-03

---

## 📋 Table of Contents

1. The Problem
2. The Solution
3. Architecture Overview
4. Workflow Guide
5. Testing & Validation
6. Real-World Example
7. Getting Started
8. Q&A

---

# SECTION 1: THE PROBLEM

---

## Slide 1.1: The Challenge

### Why Claude Skills Fail

**Common Issues:**
- 🔴 **Token Exhaustion** - Skills run out of context mid-conversation
- 🔴 **Context Loss** - Information lost between conversations
- 🔴 **Mixed Concerns** - User data tangled with skill logic
- 🔴 **Poor Documentation** - Unclear how to use or extend
- 🔴 **No Version Control** - Can't track changes or rollback

**Impact:**
- Frustrated users
- Unreliable behavior
- Difficult to maintain
- Hard to scale

---

## Slide 1.2: Real Example - Token Crisis

### What Happens Without Token Management

```
Conversation Flow (BAD):
┌─────────────────────────────────────┐
│ User: "Analyze this job"            │
│ Tokens: 5,000 used                  │
├─────────────────────────────────────┤
│ Claude loads ALL modules (50K)      │
│ Tokens: 55,000 used ⚠️              │
├─────────────────────────────────────┤
│ User: "Add more details"            │
│ Tokens: 65,000 used 🔴              │
├─────────────────────────────────────┤
│ Context length exceeded!            │
│ Conversation crashes 💥             │
└─────────────────────────────────────┘
```

**Result:** Incomplete analysis, lost work, frustrated user

---

## Slide 1.3: The Root Causes

### Why This Keeps Happening

1. **No Budget Awareness**
   - Skills don't track token usage
   - Load everything at once
   - No progressive disclosure

2. **Monolithic Design**
   - All logic in one file
   - Can't selectively load features
   - Everything loads or nothing loads

3. **No State Management**
   - Each conversation starts fresh
   - Repeat expensive operations
   - Can't resume work

4. **Development Chaos**
   - No structure or standards
   - Ad-hoc file organization
   - Impossible to collaborate

---

# SECTION 2: THE SOLUTION

---

## Slide 2.1: Introducing Claude Skills SDK

### Production-Ready Framework

**What It Provides:**
- ✅ Token budget protection
- ✅ Modular architecture
- ✅ State management
- ✅ MCP integration
- ✅ Professional tooling
- ✅ Comprehensive documentation

**Based On:**
Israeli Tech Career Consultant v9.3.0
- 30+ features
- Battle-tested in production
- Hundreds of analyses completed
- Token-optimized (5-35K per session)

---

## Slide 2.2: Key Innovations

### What Makes This Different

1. **Three-Tier Architecture**
   - Skill logic (portable)
   - User data (local)
   - Documentation (comprehensive)

2. **Token Budget System**
   - Track usage in real-time
   - Load modules on-demand
   - Archive when threshold reached

3. **Session State Management**
   - DEV_SESSION_STATE.md tracks progress
   - Resume across conversations
   - Never lose context

4. **Automation-First**
   - Validation scripts catch errors
   - Release automation
   - Setup wizards

---

## Slide 2.3: Design Philosophy

### Core Principles

```
┌──────────────────────────────────────────────┐
│ 1. Separation of Concerns                   │
│    Skill logic ≠ User data                   │
│                                              │
│ 2. Token Efficiency First                   │
│    Load only what's needed, when needed     │
│                                              │
│ 3. Documentation-Driven                     │
│    Write spec before code                    │
│                                              │
│ 4. Automation Prevents Errors               │
│    Scripts > manual processes               │
│                                              │
│ 5. Version Control Builds Trust             │
│    Every change tracked and documented      │
└──────────────────────────────────────────────┘
```

---

# SECTION 3: ARCHITECTURE OVERVIEW

---

## Slide 3.1: Directory Structure

### The Three-Tier System

```
claude-skill-template/
│
├── skill-package/          📦 TIER 1: Skill Logic
│   ├── SKILL.md           # Main skill definition
│   ├── config/            # Static configuration
│   ├── modules/           # Core features
│   ├── scripts/           # Python utilities
│   └── templates/         # Output formats
│
├── user-data/             💾 TIER 2: User Storage
│   ├── config/           # User settings
│   ├── db/               # Dynamic data
│   └── logs/             # Operation logs
│
├── docs/                  📚 TIER 3: Documentation
│   ├── guides/           # How-to guides
│   └── project/          # Specs & planning
│
├── host_scripts/         🔧 Automation
└── .github/              🚀 CI/CD
```

---

## Slide 3.2: Tier 1 - Skill Package

### What Gets Uploaded to Claude

```
skill-package/
├── SKILL.md                    # 🎯 Entry point
│   └── Instructions for Claude
│   └── Available modules list
│   └── Token budget rules
│
├── config/
│   └── paths.py                # 📍 Storage paths
│
├── modules/
│   ├── feature-a.md           # 🔧 Feature modules
│   ├── feature-b.md
│   └── feature-c.md
│
├── scripts/
│   ├── config_loader.py       # ⚙️ Utilities
│   └── yaml_utils.py
│
└── templates/
    └── output-formats.md      # 📄 Output templates
```

**Key Points:**
- Read-only for Claude
- Version controlled
- Portable across users
- Token-optimized

---

## Slide 3.3: Tier 2 - User Data

### Local Storage (Not in Claude)

```
user-data/
├── config/
│   └── user-config.yaml       # 👤 Personal settings
│       ├── name
│       ├── preferences
│       └── API keys
│
├── db/
│   ├── entities.yaml          # 💾 Domain data
│   ├── history.yaml
│   └── cache.yaml
│
└── logs/
    ├── operations.log         # 📊 Audit trail
    └── errors.log
```

**Key Points:**
- Read-write via MCP Filesystem
- User-specific data
- Never version controlled
- Gitignored for safety

---

## Slide 3.4: Tier 3 - Documentation

### Knowledge Base

```
docs/
├── guides/
│   ├── user-guide/           # 👥 For users
│   │   ├── setup.md
│   │   ├── usage.md
│   │   └── troubleshooting.md
│   │
│   └── developer-guide/      # 👨‍💻 For developers
│       ├── architecture.md
│       ├── module-guide.md
│       └── testing.md
│
└── project/
    ├── features/             # 📋 Feature specs
    └── session-reports/      # 📊 Session tracking
```

**Key Points:**
- Comprehensive and maintained
- Specs before code
- Examples included
- Version controlled

---

## Slide 3.5: Data Flow Diagram

### How It All Works Together

```
┌─────────────────────────────────────────────────────┐
│                   CLAUDE                            │
│                                                     │
│  ┌──────────────────────────────────────┐          │
│  │  SKILL.md                            │          │
│  │  • Reads configuration               │          │
│  │  • Loads modules on-demand           │          │
│  │  • Tracks token usage                │          │
│  └──────────────────────────────────────┘          │
│            ↓                    ↓                   │
│    ┌─────────────┐      ┌──────────────┐          │
│    │  Module A   │      │   Module B   │          │
│    │  (5K tokens)│      │   (8K tokens)│          │
│    └─────────────┘      └──────────────┘          │
└─────────────────────────────────────────────────────┘
                     ↓
            ┌────────────────┐
            │  MCP Filesystem│
            └────────────────┘
                     ↓
        ┌─────────────────────────────┐
        │     YOUR MAC                │
        │  /user-data/                │
        │  ├── config/                │
        │  ├── db/                    │
        │  └── logs/                  │
        └─────────────────────────────┘
```

---

## Slide 3.6: Token Budget System

### Progressive Disclosure Pattern

```
Session Start:
├── Load SKILL.md (2K tokens)           ✅ Always
├── Load paths.py (1K tokens)           ✅ Always
└── Wait for user request...            ⏸️ Pause

User Request: "Use Feature A"
├── Load module-a.md (5K tokens)        ✅ On-demand
├── Execute feature                     ⚙️ Work
└── Archive if threshold hit            🗃️ Conditional

Token Budget:
├── Threshold: 50% of max (95K/190K)   ⚠️ Warning
├── Archive: Save state & restart      🔄 Reset
└── Resume: Continue from checkpoint    ▶️ Continue
```

**Result:** Never exhaust context!

---

# SECTION 4: WORKFLOW GUIDE

---

## Slide 4.1: Getting Started

### Step 1: Installation

```bash
# 1. Clone or download template
git clone https://github.com/you/claude-skill-template.git my-skill
cd my-skill

# 2. Run setup wizard
./host_scripts/setup.sh

# Output:
# ✅ Created directories
# ✅ Initialized config
# ✅ Set up git hooks
# ✅ Ready to customize!
```

**Time:** 2 minutes  
**Complexity:** Beginner-friendly

---

## Slide 4.2: Configuration

### Step 2: Set Your Paths

**Edit:** `skill-package/config/paths.py`

```python
# Before (template):
USER_DATA_BASE = "/path/to/user-data"

# After (your system):
USER_DATA_BASE = "/Users/john/my-skill/user-data"
```

**Then configure MCP in Claude Desktop:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/john/my-skill/user-data"
      ]
    }
  }
}
```

---

## Slide 4.3: Creating Your First Module

### Step 3: Build a Feature

**1. Write Specification:**
```bash
cp docs/project/features/TEMPLATE.md \
   docs/project/features/my-feature.md

# Document:
# - What it does
# - How it works
# - Success criteria
```

**2. Create Module:**
```bash
cp skill-package/modules/module-template.md \
   skill-package/modules/my-feature.md

# Implement:
# - Feature logic
# - Error handling
# - Output formatting
```

**3. Update SKILL.md:**
```markdown
## Available Modules
- **my-feature**: Does amazing things
```

---

## Slide 4.4: Testing Your Module

### Step 4: Validation

```bash
# Run validation script
python host_scripts/validate.py

# Checks performed:
✅ Directory structure correct
✅ Required files present
✅ YAML syntax valid
✅ Python syntax valid
✅ SKILL.md format correct
✅ No sensitive data exposed
✅ Version consistency

# Output:
🎉 All checks passed!
```

**If errors found:**
- Clear error messages
- Line numbers provided
- Suggestions for fixes

---

## Slide 4.5: Manual Testing

### Step 5: Test with Claude

**1. Upload skill-package/:**
- In Claude Desktop
- Upload entire folder
- Or individual files

**2. Test the feature:**
```
You: "Use my-feature to..."

Claude: 
[Loads my-feature module]
[Executes logic]
[Returns formatted output]
```

**3. Verify:**
- ✅ Feature works as expected
- ✅ Token usage reasonable
- ✅ Output properly formatted
- ✅ Data saved correctly

---

## Slide 4.6: Release Process

### Step 6: Create Release

```bash
# Create release
./host_scripts/release.sh 1.0.0

# What happens:
# 1. ✅ Validates everything
# 2. ✅ Creates git tag
# 3. ✅ Packages skill
# 4. ✅ Generates checksums
# 5. ✅ Updates changelog
# 6. ✅ Pushes to GitHub

# Output:
# releases/my-skill-v1.0.0.zip
# releases/CHECKSUMS.txt
```

**Result:** Professional, versioned release!

---

## Slide 4.7: Complete Workflow

### The Full Cycle

```
┌─────────────────────────────────────────┐
│ 1. PLAN                                 │
│    Write feature specification          │
│    ↓                                    │
│ 2. BUILD                                │
│    Create module                        │
│    ↓                                    │
│ 3. TEST                                 │
│    Validate & manual test               │
│    ↓                                    │
│ 4. DOCUMENT                             │
│    Update guides & README               │
│    ↓                                    │
│ 5. RELEASE                              │
│    Version & publish                    │
│    ↓                                    │
│ 6. ITERATE                              │
│    Gather feedback, improve             │
│    ↓                                    │
│    (repeat from step 1)                 │
└─────────────────────────────────────────┘
```

---

# SECTION 5: TESTING & VALIDATION

---

## Slide 5.1: Validation System

### 7 Automated Checks

```
1. ✅ Directory Structure
   - All required dirs present
   - No unexpected files
   
2. ✅ Required Files
   - SKILL.md exists
   - Config files present
   
3. ✅ YAML Syntax
   - Valid YAML format
   - No parsing errors
   
4. ✅ Python Syntax
   - Valid Python code
   - No syntax errors
```

---

## Slide 5.2: Validation System (cont.)

### Checks 5-7

```
5. ✅ SKILL.md Format
   - Proper structure
   - All sections present
   
6. ✅ Sensitive Data
   - No API keys
   - No passwords
   - No personal info
   
7. ✅ Version Consistency
   - Version matches across files
   - Changelog updated
```

**Run:** `python host_scripts/validate.py`

---

## Slide 5.3: Testing Strategies

### Multi-Layer Approach

**1. Unit Testing (Module Level)**
```python
# Test individual functions
def test_calculate_score():
    result = calculate_score(data)
    assert result == expected
```

**2. Integration Testing (Skill Level)**
```
Test full workflows:
- User uploads file
- Skill processes
- Output generated
- Data saved
```

**3. Token Budget Testing**
```
Monitor throughout:
- Track tokens per module
- Verify progressive loading
- Test archiving behavior
```

---

## Slide 5.4: Manual Testing Checklist

### Before Every Release

```
□ Basic Functionality
  □ Skill loads in Claude
  □ All modules accessible
  □ Commands work as expected
  
□ Token Management
  □ Budget tracking accurate
  □ Modules load on-demand
  □ Archiving works correctly
  
□ Data Persistence
  □ Config reads/writes
  □ Database operations
  □ Logs generated
  
□ Error Handling
  □ Graceful failures
  □ Clear error messages
  □ Recovery possible
  
□ Documentation
  □ README accurate
  □ Examples work
  □ Guides up-to-date
```

---

## Slide 5.5: Debugging Tools

### When Things Go Wrong

**1. Check Logs:**
```bash
tail -f user-data/logs/operations.log
```

**2. Validate Structure:**
```bash
python host_scripts/validate.py
```

**3. Check Token Usage:**
```
Add to SKILL.md:
"Show token usage after each operation"
```

**4. Test in Isolation:**
```
Upload single module
Test specific feature
Verify in clean conversation
```

---

# SECTION 6: REAL-WORLD EXAMPLE

---

## Slide 6.1: Case Study

### Israeli Tech Career Consultant

**Stats:**
- 📦 Version 9.3.0 (mature product)
- 🎯 30+ implemented features
- 📊 Hundreds of analyses completed
- 🔧 Token optimized (5-35K per analysis)
- ⭐ Production-ready quality

**Complexity:**
- Job analysis with 6-component scoring
- Multiple CV variants
- LinkedIn integration
- Excel export with formulas
- Interview preparation tools

---

## Slide 6.2: Token Management in Action

### Real Token Usage

```
Typical Job Analysis Session:
├── Initial load: 15K tokens         (SKILL.md + core)
├── Job analysis: +12K tokens        (analysis module)
├── LinkedIn scrape: +8K tokens      (research module)
├── CV matching: +10K tokens         (matching module)
├── Excel export: +5K tokens         (export module)
└── Total: 50K tokens               ✅ Under threshold

Complex Analysis:
├── Initial: 15K
├── Deep analysis: +20K
├── Hit 50% threshold
├── Archive state → new conversation
├── Resume with saved context
└── Complete without token exhaustion ✅
```

---

## Slide 6.3: Lessons Learned

### What Worked

**✅ Modular Design:**
- Easy to add features
- Each module self-contained
- Clear dependencies

**✅ Token Budgets:**
- Never exceeded limits
- Progressive loading effective
- Archive/resume pattern robust

**✅ Documentation:**
- Reduced support burden
- Users self-serve
- Developers onboard quickly

**✅ Automation:**
- Validation caught 100+ errors
- Releases consistent
- Time saved: ~10 hours/month

---

## Slide 6.4: What We'd Change

### Areas for Improvement

**🔶 Testing:**
- Need automated integration tests
- More edge case coverage
- Performance benchmarking

**🔶 User Experience:**
- Simpler setup process
- Better error messages
- Interactive tutorials

**🔶 Developer Tools:**
- VS Code extension
- Debug mode
- Live token monitoring

**Note:** These improvements are coming in SDK v2.0!

---

# SECTION 7: GETTING STARTED

---

## Slide 7.1: Prerequisites

### What You Need

**Required:**
- ✅ macOS 14+ (or Linux)
- ✅ Claude Desktop with MCP support
- ✅ Python 3.8+
- ✅ Git
- ✅ Text editor (VS Code recommended)

**Optional:**
- ⚪ GitHub account (for releases)
- ⚪ Firecrawl API (for web scraping)
- ⚪ Bright Data API (for advanced scraping)

**Time Investment:**
- Quick start: 30 minutes
- First module: 2-4 hours
- Production-ready skill: 1-2 weeks

---

## Slide 7.2: Learning Resources

### Where to Learn More

**Documentation:**
- 📖 README.md - Overview & quick start
- 📖 Architecture Guide - Deep dive
- 📖 Module Guide - How to build features
- 📖 Testing Guide - Quality assurance

**Examples:**
- 🔍 module-template.md - Template to copy
- 🔍 Israeli Career Consultant - Real implementation
- 🔍 Sample configs - Configuration examples

**Community:**
- 💬 GitHub Discussions - Ask questions
- 🐛 GitHub Issues - Report bugs
- ⭐ Star the repo - Show support

---

## Slide 7.3: Quick Wins

### Start Here for Fast Results

**Beginner (Day 1):**
1. Clone template
2. Run setup script
3. Configure paths
4. Test basic upload
5. **Win:** Working skill!

**Intermediate (Week 1):**
1. Create first module
2. Add custom config
3. Test with real data
4. Document usage
5. **Win:** Custom feature!

**Advanced (Month 1):**
1. Build multi-module feature
2. Optimize token usage
3. Create release
4. Share with community
5. **Win:** Published skill!

---

## Slide 7.4: Common Pitfalls

### Avoid These Mistakes

**❌ Token Overload:**
- Loading all modules at once
- **Fix:** Use progressive loading

**❌ Mixed Concerns:**
- User data in skill-package
- **Fix:** Use three-tier architecture

**❌ No Documentation:**
- Skip writing specs
- **Fix:** Doc-first development

**❌ Manual Processes:**
- Hand-edit version numbers
- **Fix:** Use automation scripts

**❌ No Testing:**
- Ship without validation
- **Fix:** Run validate.py always

---

## Slide 7.5: Success Checklist

### You're Ready When...

```
✅ Setup
   □ Template cloned
   □ Paths configured
   □ MCP connected
   
✅ Development
   □ First module created
   □ Validation passing
   □ Manual tests successful
   
✅ Documentation
   □ Feature spec written
   □ User guide updated
   □ Examples provided
   
✅ Release
   □ Version tagged
   □ Package created
   □ Changelog updated
   
✅ Distribution
   □ GitHub repository
   □ Release published
   □ Community notified
```

---

## Slide 7.6: Next Steps

### After This Presentation

**Immediate (Today):**
1. Clone the template
2. Star the repository
3. Read the README
4. Join discussions

**This Week:**
1. Complete quick start
2. Create first module
3. Run validation
4. Test with Claude

**This Month:**
1. Build complete skill
2. Write documentation
3. Create release
4. Share your work

**Join the community and build amazing skills!**

---

# SECTION 8: Q&A

---

## Slide 8.1: Frequently Asked Questions

### Common Questions

**Q: Do I need to know Python?**
A: Basic Python helpful for scripts, but not required for creating skills. Modules are markdown.

**Q: Can I use this for commercial projects?**
A: Yes! MIT license allows commercial use.

**Q: How do I handle secrets?**
A: Store in user-data/config (gitignored). Never in skill-package.

**Q: What if I exceed token limits?**
A: SDK's archive/resume pattern handles this automatically.

---

## Slide 8.2: Advanced Questions

### For Power Users

**Q: Can I customize the architecture?**
A: Yes, but maintain three-tier separation for portability.

**Q: How do I add new MCP servers?**
A: Document in docs/guides/user-guide/mcp-servers.md

**Q: Can I integrate with APIs?**
A: Yes, use scripts/ directory for API clients.

**Q: How do I optimize token usage further?**
A: See Architecture Guide for advanced patterns.

---

## Slide 8.3: Contributing

### Join the Project

**Ways to Help:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve docs
- 🔧 Submit PRs
- ⭐ Star & share

**Guidelines:**
- Read CONTRIBUTING.md
- Follow code style
- Include tests
- Update docs
- Be kind & respectful

---

## Slide 8.4: Resources

### Links & References

**Repository:**
https://github.com/gsannikov/claude-skill-template

**Documentation:**
https://github.com/gsannikov/claude-skill-template/tree/main/docs

**Discussions:**
https://github.com/gsannikov/claude-skill-template/discussions

**Issues:**
https://github.com/gsannikov/claude-skill-template/issues

**Example Skill:**
https://github.com/gsannikov/israeli-tech-career-consultant

---

## Slide 8.5: Thank You!

### Let's Build Amazing Skills Together

**Remember:**
- Start small, iterate fast
- Documentation is your friend
- Token management is critical
- Community support available
- Have fun building!

**Questions?**

📧 gursannikov@users.noreply.github.com  
🐙 github.com/gsannikov  
💬 Open a Discussion

**Thank you for your time!**

---

## Slide 8.6: Call to Action

### Your Turn!

**Today:**
- Clone the template
- Star the repository

**This Week:**
- Build your first module
- Share your progress

**This Month:**
- Release your skill
- Help others succeed

**Let's revolutionize Claude skill development!**

🚀 Get started: github.com/gsannikov/claude-skill-template

---

# END OF PRESENTATION

---

## Appendix: Conversion Notes

### Creating Slides

**For PowerPoint/Keynote:**
1. Use each ## heading as a new slide
2. Convert code blocks to fixed-width font
3. Add your branding/theme
4. Include diagrams as images

**For Google Slides:**
1. Import markdown using add-on
2. Adjust formatting
3. Add speaker notes
4. Share with team

**For reveal.js:**
1. Use `---` as slide separators
2. Host on GitHub Pages
3. Interactive presentations!

---

**Presentation Duration:** 45-60 minutes  
**Target Audience:** Claude skill developers  
**Level:** Beginner to Intermediate  
**Format:** Educational / Tutorial

---

*Created: 2025-11-03*  
*Version: 1.0.0*  
*Author: Gur Sannikov*
