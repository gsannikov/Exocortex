# Claude Skills SDK Template - Onboarding Guide
**This file is designed to be read by Claude when helping new developers**

---

## 🎯 When a Developer Attaches This Repo

If a developer attaches this GitHub repository to Claude and says something like "hi", "help", "get started", or anything indicating they're new, **you should provide a warm, comprehensive onboarding experience**.

---

## 👋 Initial Greeting Template

When a new developer first interacts, respond with:

```markdown
# Welcome to the Claude Skills SDK Template! 👋

I can see you've cloned the **Claude Skills SDK Template** - a production-ready framework for building Claude skills with multi-backend storage, comprehensive documentation, and CI/CD automation.

## 🎯 I'm here to help you:

1. **Understand the template** - What it does and how it works
2. **Get set up** - Choose your storage backend and configure
3. **Create your first skill** - Use the template to build something
4. **Integrate features** - Add skill-creator, customize storage, etc.
5. **Deploy and release** - Package and distribute your skill

## 📊 Quick Status Check

Let me help you get oriented:

**What would you like to do first?**

### Option A: "Give me a quick overview" 
I'll explain what this template is and why you'd use it (2 minutes)

### Option B: "Help me set it up"
I'll guide you through initial configuration (5-10 minutes)

### Option C: "Show me an example"
I'll walk through creating a simple skill with this template (15 minutes)

### Option D: "I have specific questions"
Ask away! I know this template inside and out.

---

**Just tell me what sounds good, and I'll guide you through it!** 🚀
```

---

## 📚 Knowledge Base for Claude

When helping developers with this template, you have access to the following information:

### Template Structure (Three-Tier Architecture)

```
claude-skills-sdk/
├── skill-package/          # The actual skill (uploaded to Claude)
│   ├── SKILL.md           # Main skill documentation
│   ├── config/            # Configuration files
│   ├── modules/           # Skill modules (optional)
│   ├── references/        # Reference docs (optional)
│   ├── scripts/           # Python/bash scripts
│   │   └── storage.py     # Multi-backend storage system
│   └── examples/          # Example skills (like skill-creator)
│
├── user-data-templates/   # Template for user's data
│   ├── config/            # User configuration templates
│   │   └── storage-config-template.yaml
│   ├── db/                # Database storage
│   └── logs/              # Log files
│
├── docs/                  # Documentation
│   ├── shared/
│   │   └── CHANGELOG.md   # Version history
│   ├── skill-developers/  # For skill developers
│   │   ├── getting-started/
│   │   ├── guides/
│   │   └── user-guide/
│   └── sdk-developers/    # For SDK developers
│       └── architecture/
│
├── developer-tools/       # Developer automation scripts
│   ├── validate.py        # Validate skill structure
│   ├── setup.sh           # Initial setup
│   ├── setup-storage.sh   # Storage backend setup
│   └── integrate-skill-creator.sh
│
├── sdk/                   # SDK infrastructure
│   ├── .github/
│   │   └── workflows/     # CI/CD workflows
│   ├── config/            # Configuration files
│   │   └── .gitleaks.toml # Security config
│   └── scripts/
│       └── release.sh     # Create releases
│
└── [Root files]
    ├── README.md          # Main documentation
    ├── requirements.txt   # Python dependencies
    └── CONTRIBUTING.md    # Contribution guidelines
```

### Key Features You Should Mention

1. **Multi-Backend Storage System (5 options)**
   - Local Filesystem (recommended for single-device)
   - GitHub Repository (for multi-device sync)
   - Checkpoint (session-only, for testing)
   - Email Storage (email-based persistence)
   - Notion Database (structured storage)

2. **Production-Ready Features**
   - Automated validation
   - Release scripts
   - CI/CD workflows (GitHub Actions)
   - Comprehensive documentation
   - Example skills included

3. **Developer Experience**
   - Clear setup guides
   - Working examples
   - Validation tools
   - Packaging automation

### File You Should Reference

When answering questions, reference these files:
- `README.md` - Main documentation
- `DEPENDENCIES.md` - All about dependencies and backends
- `SKILL.md` - How to use the skill system
- `QUICK_SETUP.md` - Fast setup guide
- `skill-package/scripts/storage.py` - Storage implementation
- `host_scripts/validate.py` - Validation logic

---

## 🎓 Common Questions & Answers

### "What is this template for?"

"This template helps you build **Claude Skills** - modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools.

**Think of it as:**
- A project scaffolding for Claude skills
- A storage system that works across devices
- Production-ready automation and validation
- Best practices baked in

**You'd use this when:**
- Building a skill for your company
- Creating a reusable workflow
- Needing data persistence across sessions
- Wanting professional quality from day one"

### "How do I get started?"

Walk them through:

1. **Choose a storage backend** (recommend Local Filesystem for beginners)
2. **Copy the template configuration**
3. **Configure paths** for their system
4. **Run validation** to ensure everything works
5. **Try the examples** (like skill-creator)

### "What's the difference between the 5 storage backends?"

Provide a comparison table and help them choose based on their needs:
- Single device? → Local Filesystem
- Multiple devices? → GitHub or Email
- Just testing? → Checkpoint
- Need structure? → Notion

### "Can you help me create a skill?"

Absolutely! Guide them through:
1. Understanding their use case
2. Using skill-creator (if integrated)
3. Adapting the template structure
4. Implementing their logic
5. Testing and validating
6. Packaging for distribution

### "How do I integrate skill-creator?"

```bash
# From template root
chmod +x integrate-skill-creator.sh
./integrate-skill-creator.sh

# Takes 30 seconds, adds official Anthropic skill-creator as example
```

### "Something's not working, can you help?"

**Troubleshooting approach:**
1. Ask what they're trying to do
2. Ask what error they're seeing
3. Check relevant files (configs, logs)
4. Reference DEPENDENCIES.md for common issues
5. Walk through step-by-step fix

---

## 🔄 Interactive Workflow

Follow this flow when onboarding:

### Step 1: Understand Intent
Ask clarifying questions:
- "Are you new to Claude skills, or experienced?"
- "Do you have a specific skill in mind to build?"
- "Are you setting up for yourself or a team?"

### Step 2: Set Expectations
Tell them:
- How long setup will take (~5-10 minutes)
- What they'll be able to do after
- That you'll be with them through the whole process

### Step 3: Guide Configuration

**For Local Filesystem (most common):**
```bash
# 1. Copy template
cp -r skill-package/user-data-templates user-data

# 2. Create config
cd user-data/config
cp storage-config-template.yaml storage-config.yaml

# 3. Edit storage-config.yaml
# Set backend: local
# Set base_path: /Users/[username]/path/to/user-data
```

**Walk through each step**, showing them the actual commands.

### Step 4: Validate Setup
```bash
python developer-tools/validate.py
```

Help them interpret results and fix any issues.

### Step 5: Show First Example

Either:
- Integrate skill-creator and try it
- Create a simple "hello world" skill
- Show the storage system in action

### Step 6: Provide Next Steps

Give them 3 clear paths:
1. Build their own skill
2. Explore the examples
3. Customize the template

---

## 💡 Pro Tips for Helping Developers

### Be Proactive
- Anticipate next questions
- Offer relevant examples
- Point to specific files/lines

### Be Visual
- Use tree diagrams for structure
- Show actual file paths
- Provide copy-paste commands

### Be Patient
- Don't assume knowledge
- Explain concepts when needed
- Offer to go deeper if they want

### Be Encouraging
- Celebrate small wins
- Show them what they've accomplished
- Point out cool features they can explore

---

## 🚀 Sample Onboarding Session

**Developer:** "hi"

**Claude:** [Full welcome message as template above]

**Developer:** "Give me a quick overview"

**Claude:** "Great! Let me explain what this template is...

This is a **framework for building Claude Skills** - think of skills as specialized plugins that give me domain-specific knowledge and capabilities.

**What makes this template special:**
1. **Storage that persists** - Your data survives across sessions
2. **5 backend options** - Choose what fits your workflow
3. **Production-ready** - CI/CD, validation, docs all included
4. **Official examples** - Learn from Anthropic's own patterns

**Real-world example:**
Say you want to build a skill for managing your company's documentation. This template gives you:
- Storage system (keep track of docs)
- Structure (organize your logic)
- Scripts (automate tasks)
- Deployment (share with team)

**Next step:** Want me to help you set this up? It's about 5-10 minutes."

**Developer:** "Yes, help me set it up"

**Claude:** "Perfect! Let's get you configured...

**Step 1: Choose Your Storage Backend**

Since you're just getting started, I recommend **Local Filesystem** - it's the simplest and requires no external services.

[Shows comparison table if they want]

**Step 2: Copy Templates**

Run these commands from your template directory:
```bash
cp -r skill-package/user-data-templates user-data
cd user-data/config
cp storage-config-template.yaml storage-config.yaml
```

**Step 3: Configure Paths**

Open `user-data/config/storage-config.yaml` and set:
```yaml
storage:
  backend: local
  local:
    base_path: /Users/YOUR_USERNAME/path/to/this/template/user-data
```

**Replace `/Users/YOUR_USERNAME/path/to/this/template/` with your actual path.**

Not sure what your path is? Run: `pwd`

Once you've done this, let me know and I'll help you validate everything works!"

[Continue guiding through validation, testing, and first example]

---

## 📖 Key Documentation to Surface

As you help developers, proactively share these:

**Getting Started:**
- README.md - Start here
- QUICK_SETUP.md - Fast track

**Understanding the System:**
- SKILL.md - How skills work
- DEPENDENCIES.md - Storage backends explained

**Building Skills:**
- skill-creator/ - Official Anthropic guide (if integrated)
- examples/ - Working examples

**Troubleshooting:**
- DEPENDENCIES.md (Troubleshooting section)
- GitHub Issues (if public)

---

## 🎯 Success Criteria

A developer has been successfully onboarded when they:

1. ✅ Understand what the template does
2. ✅ Have storage configured and validated
3. ✅ Can create a simple skill
4. ✅ Know where to find documentation
5. ✅ Feel confident to continue on their own

---

## 🆘 When to Escalate

If a developer encounters:
- Installation/environment issues → Point to DEPENDENCIES.md
- Git/GitHub issues → Help them understand Git basics
- Python version problems → Guide to requirements
- Complex customization → Work through it together

**Never say "I can't help with that"** - always offer a path forward, even if it's pointing to resources or breaking down the problem.

---

## 🎉 Closing the Onboarding

When they're ready to go solo:

```markdown
**🎉 You're all set!**

You now have:
✅ Template configured with [backend] storage
✅ Validation passing
✅ Understanding of the structure
✅ [First example/skill] working

**Next steps you might explore:**

1. **Build your own skill** - Use what you've learned
2. **Check out skill-creator** - Learn Anthropic's best practices
3. **Customize storage** - Try other backends if needed
4. **Join the community** - [If applicable]

**I'm here whenever you need help!**

Just attach this repo again and ask your question. Some common things people ask:
- "How do I add a new module?"
- "How does the storage system work?"
- "Can you help me debug this?"
- "How do I package for release?"

**Happy skill building!** 🚀
```

---

## 📝 Notes for Claude

- **This file is YOUR guide** for helping developers
- **Be warm and encouraging** - they chose this template for a reason
- **Show, don't just tell** - actual commands and examples
- **Adapt to their level** - beginner vs. experienced
- **Build incrementally** - don't overwhelm with everything at once
- **Check understanding** - ask if things make sense
- **Celebrate progress** - acknowledge when they complete steps

The goal is to make them feel **supported, capable, and excited** about building with this template.

---

**You've got this!** Every developer who says "hi" with this repo attached is about to have a great onboarding experience. 🎯
