# 👋 Welcome to Claude Skills SDK Template!

## 🚀 First Time Here?

**The easiest way to get started:**

1. **Open Claude** (claude.ai)
2. **Attach this entire GitHub repository** to your conversation
3. **Say:** "hi" or "help me get started"
4. **Follow Claude's guided onboarding** (~10-15 minutes)

Claude will read [CLAUDE_ONBOARDING_GUIDE.md](CLAUDE_ONBOARDING_GUIDE.md) and walk you through everything interactively!

---

## 📚 What You'll Learn

During onboarding, Claude helps you:

✅ **Understand** what this template does  
✅ **Choose** the right storage backend for you  
✅ **Configure** everything step-by-step  
✅ **Create** your first skill  
✅ **Use** the automation tools  

---

## 🎯 What This Template Is

A **production-ready framework** for building Claude Skills with:

- **5 storage backends** (Local, GitHub, Checkpoint, Email, Notion)
- **Complete architecture** (skill-package, user-data, docs)
- **Automation tools** (validate, release, setup)
- **Best practices** from Anthropic

Perfect for building:
- Company-specific skills
- Workflow automation
- Data-persistent applications
- Team collaboration tools

---

## 📖 Manual Setup (If You Prefer)

Prefer written instructions? See [QUICK_SETUP.md](QUICK_SETUP.md)

Or jump straight to the full docs: [README.md](../README.md)

---

## 🆘 Need Help?

**Immediate help:**
- Attach this repo to Claude and ask!

**Documentation:**
- [QUICK_SETUP.md](QUICK_SETUP.md) - Fast track
- [README.md](../README.md) - Complete guide
- [DEPENDENCIES.md](DEPENDENCIES.md) - Storage details
- [Full Documentation](../) - Deep dives

---

## ⚡ Quick Commands

```bash
# Set up storage backend
cp -r user-data-templates user-data
cd user-data/config
cp storage-config-template.yaml storage-config.yaml
# Edit storage-config.yaml with your settings

# Validate everything works
python host_scripts/validate.py

# Integrate official skill-creator (optional)
chmod +x integrate-skill-creator.sh
./integrate-skill-creator.sh

# Create a release
./host_scripts/release.sh 1.1.0
```

---

## 🎉 You're Going to Love This!

This template makes building Claude skills easy, professional, and fun.

**Ready?** Open Claude, attach this repo, and say "hi"! 🚀

---

*Claude Skills SDK Template v1.1.0 | MIT License*
