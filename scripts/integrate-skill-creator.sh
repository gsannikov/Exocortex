#!/bin/bash
# integrate-skill-creator.sh
# Downloads and integrates official skill-creator into SDK template

set -e

SKILL_CREATOR_DIR="skill-package/examples/skill-creator"
BASE_URL="https://raw.githubusercontent.com/anthropics/skills/main/skill-creator"

echo "🚀 Integrating skill-creator from Anthropic's official skills repo"
echo ""

# Create directories
echo "📁 Creating directory structure..."
mkdir -p "$SKILL_CREATOR_DIR/scripts"
mkdir -p "$SKILL_CREATOR_DIR/references"

# Download main files
echo "📥 Downloading SKILL.md..."
curl -sL "$BASE_URL/SKILL.md" -o "$SKILL_CREATOR_DIR/SKILL.md"

echo "📥 Downloading LICENSE.txt..."
curl -sL "$BASE_URL/LICENSE.txt" -o "$SKILL_CREATOR_DIR/LICENSE.txt"

# Download scripts
echo "📥 Downloading scripts..."
curl -sL "$BASE_URL/scripts/init_skill.py" -o "$SKILL_CREATOR_DIR/scripts/init_skill.py"
curl -sL "$BASE_URL/scripts/package_skill.py" -o "$SKILL_CREATOR_DIR/scripts/package_skill.py"
curl -sL "$BASE_URL/scripts/validate_skill.py" -o "$SKILL_CREATOR_DIR/scripts/validate_skill.py"

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x "$SKILL_CREATOR_DIR/scripts/"*.py

# Create README
echo "📝 Creating integration README..."
cat > "$SKILL_CREATOR_DIR/README.md" << 'EOF'
# skill-creator (Official Anthropic Skill)

**Source:** https://github.com/anthropics/skills/tree/main/skill-creator  
**License:** Apache 2.0 (see LICENSE.txt)  
**Integrated:** 2025-11-04

This is the official Anthropic skill-creator, included as a reference example in the Claude Skills SDK Template.

---

## 🎯 What It Does

skill-creator is a meta-skill that guides you through creating effective Claude skills. It provides:

- **Step-by-step Process** - Clear workflow from concept to package
- **Best Practices** - Anthropic's recommended patterns
- **Validation Tools** - Automated quality checks
- **Packaging Scripts** - Distribution-ready output
- **Progressive Disclosure** - Efficient context management

---

## 📚 How to Use

### As Reference Documentation

Read `SKILL.md` to learn Anthropic's official best practices for skill creation:

```bash
# View the skill documentation
cat SKILL.md

# Or read it with Claude
file_read("examples/skill-creator/SKILL.md")
```

### Using the Scripts

**Initialize a new skill:**
```bash
python scripts/init_skill.py my-new-skill --path ../my-skills/
```

This creates:
```
my-new-skill/
├── SKILL.md           # Template with TODO placeholders
├── scripts/           # Example executable scripts
├── references/        # Example reference docs
└── assets/            # Example assets
```

**Package a skill:**
```bash
python scripts/package_skill.py path/to/my-skill
```

This will:
1. Validate the skill structure
2. Check YAML frontmatter
3. Verify naming conventions
4. Create distributable ZIP file

**Validate a skill:**
```bash
python scripts/validate_skill.py path/to/my-skill
```

---

## 🔄 Adaptation for SDK Template

This skill is provided as-is from Anthropic's repository. Here's how it relates to the SDK template:

### Similarities ✅
- Progressive disclosure design
- Modular resource organization
- Validation before packaging
- Script-based automation

### Differences ⚠️

| Official skill-creator | SDK Template |
|----------------------|--------------|
| Simple structure | Three-tier (skill-package, user-data, docs) |
| No storage backend | Multi-backend (Local, GitHub, Email, Notion, Checkpoint) |
| scripts/, references/, assets/ | + config/, templates/, modules/ |
| Basic validation | + CI/CD workflows |

### Using with SDK Template

When creating skills for the SDK template, you can:

1. **Use init_skill.py** to create basic structure
2. **Add SDK features** like:
   - `config/` directory for settings
   - Storage backend configuration
   - User data handling
   - Module references

3. **Adapt scripts** if needed for storage backends

---

## 📖 Key Concepts from skill-creator

### Progressive Disclosure (Three Levels)

1. **Metadata** (~100 words) - Always loaded
   ```yaml
   name: my-skill
   description: What this skill does and when to use it
   ```

2. **SKILL.md** (<5k words) - Loaded when triggered
   - Core instructions
   - Workflow guidance
   - Resource references

3. **Bundled Resources** (Unlimited) - Loaded as needed
   - Scripts (executable code)
   - References (documentation)
   - Assets (output templates)

### Resource Types

**scripts/** - Executable code for deterministic tasks
- Python, Bash, etc.
- Reduces token usage
- Can execute without loading

**references/** - Documentation for Claude to reference
- API specs, schemas, policies
- Loaded into context as needed
- Keeps SKILL.md lean

**assets/** - Files used in output
- Templates, images, fonts
- Not loaded into context
- Copied/modified in output

---

## 🎓 Learning Path

1. **Read SKILL.md** - Understand the framework
2. **Study the scripts** - See how validation works
3. **Create test skill** - Practice with init_skill.py
4. **Adapt to template** - Add SDK-specific features
5. **Package and deploy** - Use SDK's release scripts

---

## 🔗 Integration with SDK Template

The SDK template extends skill-creator's concepts:

**skill-creator provides:**
- Skill creation methodology
- Basic structure and validation
- Packaging tools

**SDK Template adds:**
- Multi-backend storage system
- Production CI/CD workflows
- Comprehensive documentation pipeline
- Development and testing tools
- Release automation

**Together they provide:**
A complete end-to-end skill development environment!

---

## 🐛 Troubleshooting

### Scripts don't run
```bash
# Make sure they're executable
chmod +x scripts/*.py

# Check Python version (requires 3.6+)
python --version
```

### Validation fails
- Check YAML frontmatter format
- Verify required fields (name, description)
- Ensure skill name matches directory name
- Review error messages for specifics

### Package output unexpected
- Scripts work with official skill format
- May need adaptation for SDK template features
- Use SDK's release.sh for full template packaging

---

## 📚 Additional Resources

**Official Documentation:**
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [skill-creator Source](https://github.com/anthropics/skills/tree/main/skill-creator)
- [Anthropic Docs](https://docs.anthropic.com)

**SDK Template Docs:**
- [Setup Guide](../../docs/guides/user-guide/setup.md)
- [SKILL.md](../SKILL.md)
- [DEPENDENCIES.md](../../DEPENDENCIES.md)

---

## ⚖️ License

This skill is licensed under **Apache License 2.0** by Anthropic.

See `LICENSE.txt` for full terms.

**Note:** The SDK template itself is MIT licensed, but this specific component retains its Apache 2.0 license.

---

## 🙏 Attribution

**Created by:** Anthropic  
**Source:** https://github.com/anthropics/skills  
**Integrated into:** Claude Skills SDK Template  
**Integration Date:** 2025-11-04

---

*For questions about skill-creator itself, refer to Anthropic's repository.*  
*For questions about SDK template integration, see main template documentation.*
EOF

echo "✅ skill-creator integrated successfully!"
echo ""
echo "📂 Location: $SKILL_CREATOR_DIR"
echo ""
echo "📚 Files created:"
echo "  ✅ SKILL.md (official documentation)"
echo "  ✅ LICENSE.txt (Apache 2.0)"
echo "  ✅ README.md (integration guide)"
echo "  ✅ scripts/init_skill.py"
echo "  ✅ scripts/package_skill.py"
echo "  ✅ scripts/validate_skill.py"
echo ""
echo "🎯 Next steps:"
echo "  1. Review: $SKILL_CREATOR_DIR/README.md"
echo "  2. Read: $SKILL_CREATOR_DIR/SKILL.md"
echo "  3. Try: python $SKILL_CREATOR_DIR/scripts/init_skill.py test-skill"
echo ""
echo "🚀 Integration complete!"
