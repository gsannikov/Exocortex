# GitHub Release Automation - Quick Start Guide

## 🚀 Generic Automated Release Script

This script uses GitHub CLI (`gh`) to automate the entire GitHub release process. It's now **generic and reusable** for any repository!

---

## ✅ Prerequisites

1. **GitHub CLI installed**
   ```bash
   # Check if installed
   gh --version
   
   # If not installed:
   # macOS: brew install gh
   ```

2. **GitHub CLI authenticated**
   ```bash
   # Check authentication
   gh auth status
   
   # If not authenticated:
   gh auth login
   ```

3. **Git repository initialized**
   - At least one commit
   - Optional: git tags for releases

---

## 📝 Usage

### **Basic Syntax:**
```bash
./github-release-auto.sh <work_dir> <repo_name> [repo_owner] [release_tag]
```

### **Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `work_dir` | ✅ Yes | Path to your git repository | `/Users/you/myproject` |
| `repo_name` | ✅ Yes | GitHub repository name | `my-awesome-project` |
| `repo_owner` | ⚪ Optional | GitHub username/org (auto-detected if omitted) | `yourusername` |
| `release_tag` | ⚪ Optional | Release tag (uses latest git tag if omitted) | `v1.0.0` |

---

## 🎯 Examples

### **Example 1: Minimal (Auto-detect everything possible)**
```bash
bash /Users/username/MyDrive/github-release-auto.sh \
  /Users/username/MyDrive/job-analyzer.skill/claude-skills-sdk/claude-skill-template \
  claude-skill-template
```
**What happens:**
- ✅ Owner: Auto-detected from `gh` CLI
- ✅ Release tag: Uses latest git tag
- ✅ Description: Extracted from README.md

---

### **Example 2: Specify owner**
```bash
bash /Users/username/MyDrive/github-release-auto.sh \
  /Users/username/MyDrive/myproject \
  my-awesome-repo \
  gsannikov
```
**What happens:**
- ✅ Owner: `gsannikov` (specified)
- ✅ Release tag: Uses latest git tag
- ✅ Creates repo: `gsannikov/my-awesome-repo`

---

### **Example 3: Specify custom release tag**
```bash
bash /Users/username/MyDrive/github-release-auto.sh \
  /Users/username/MyDrive/myproject \
  my-awesome-repo \
  gsannikov \
  v2.0.0
```
**What happens:**
- ✅ Owner: `gsannikov`
- ✅ Release tag: `v2.0.0` (specified)
- ✅ Creates release with tag `v2.0.0`

---

### **Example 4: For your Claude Skills SDK Template**
```bash
# Make script executable (first time only)
chmod +x /Users/username/MyDrive/github-release-auto.sh

# Run the script
bash /Users/username/MyDrive/github-release-auto.sh \
  /Users/username/MyDrive/job-analyzer.skill/claude-skills-sdk/claude-skill-template \
  claude-skill-template \
  gsannikov \
  v1.0.0
```

---

## 🎯 What the Script Does

### **Automatic Actions:**

1. ✅ **Validates** work directory and git repository
2. ✅ **Auto-detects** GitHub username (if not provided)
3. ✅ **Extracts** repository description from README.md
4. ✅ **Finds** release assets in `releases/` directory
5. ✅ **Creates** GitHub repository (if doesn't exist)
6. ✅ **Pushes** code and tags to GitHub
7. ✅ **Creates** release with assets
8. ✅ **Enables** Issues and Discussions

### **Smart Features:**

- 🔍 **Auto-detects release tag** from git tags
- 📦 **Auto-finds release assets** in `releases/` folder
- 📝 **Extracts changelog** for release notes (if CHANGELOG.md exists)
- ⚠️ **Prompts for confirmation** before overwriting
- 🎨 **Color-coded output** for easy reading
- ❌ **Exits on errors** to prevent partial deployments

---

## 📁 Release Assets

The script automatically includes files from the `releases/` directory:

**Supported file types:**
- `*.zip` - ZIP archives
- `*.tar.gz` - Tarball archives  
- `*CHECKSUM*` - Checksum files
- `*.txt` - Text files (like checksums)

**Example structure:**
```
your-project/
├── releases/
│   ├── project-v1.0.0.zip
│   ├── CHECKSUMS-1.0.0.txt
│   └── documentation.pdf
└── ...
```

All files matching these patterns will be automatically attached to the release!

---

## 🔍 Sample Output

```bash
======================================================================
GitHub Automated Release - my-awesome-repo
======================================================================

ℹ️  Navigating to: /Users/you/myproject
✅ In correct directory: /Users/you/myproject
✅ GitHub CLI found
✅ GitHub CLI authenticated as: yourusername

======================================================================
Step 1: Verifying Repository
======================================================================
✅ Git repository verified
ℹ️  Repository description: An awesome project for doing awesome things
ℹ️  Using latest git tag: v1.0.0
✅ Found 2 release asset(s) in releases/
ℹ️    - releases/project-v1.0.0.zip
ℹ️    - releases/CHECKSUMS.txt

======================================================================
Step 3: Creating GitHub Repository
======================================================================
ℹ️  Creating repository: yourusername/my-awesome-repo
✅ Repository created: https://github.com/yourusername/my-awesome-repo

======================================================================
Step 6: Creating GitHub Release
======================================================================
ℹ️  Creating release: v1.0.0
✅ Release created successfully!

======================================================================
🎉 GitHub Setup Complete!
======================================================================

✅ Repository: https://github.com/yourusername/my-awesome-repo
✅ Code pushed to GitHub
✅ Release published: https://github.com/yourusername/my-awesome-repo/releases/tag/v1.0.0
✅ Assets uploaded: 2 file(s)
✅ Issues and Discussions enabled

All done! 🚀
```

---

## ⚠️ Important Notes

1. **First Time Setup**
   ```bash
   # Make executable
   chmod +x /Users/gursannikov/MyDrive/github-release-auto.sh
   ```

2. **Path Flexibility**
   - Script works from any location
   - Automatically navigates to your project directory
   - No need to `cd` before running

3. **Interactive Prompts**
   - Asks before overwriting existing repos/releases
   - Can skip release creation if no tags exist
   - Safe to run multiple times

4. **Error Handling**
   - Exits immediately on any error
   - Clear error messages
   - Won't create partial deployments

---

## 🐛 Troubleshooting

### **"GitHub CLI not found"**
```bash
brew install gh  # macOS
```

### **"Not authenticated"**
```bash
gh auth login
# Follow the prompts
```

### **"Not in a git repository"**
```bash
cd your-project
git init
git add .
git commit -m "Initial commit"
```

### **"No git tags found"**
```bash
# The script will still work but skip release creation
# To create a release, add a tag:
git tag -a v1.0.0 -m "First release"
```

### **"Could not determine GitHub username"**
```bash
# Either authenticate with gh CLI:
gh auth login

# Or provide username explicitly:
./github-release-auto.sh /path/to/project my-repo YOUR_USERNAME
```

---

## 📚 Help Command

```bash
# Show full usage instructions
bash /Users/gursannikov/MyDrive/github-release-auto.sh

# Or with any invalid arguments
bash /Users/gursannikov/MyDrive/github-release-auto.sh --help
```

---

## 🎯 Common Use Cases

### **Use Case 1: Quick Release**
```bash
# Just provide path and name, let script auto-detect everything else
./github-release-auto.sh ~/myproject my-project-name
```

### **Use Case 2: Multiple Projects**
```bash
# Release several projects with one script
./github-release-auto.sh ~/project1 proj1
./github-release-auto.sh ~/project2 proj2  
./github-release-auto.sh ~/project3 proj3
```

### **Use Case 3: Organization Repository**
```bash
# Create repo under organization
./github-release-auto.sh ~/project my-org-project my-organization
```

---

## ✨ Tips & Best Practices

1. **Use git tags** for versioning
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   ```

2. **Put release files** in `releases/` directory
   - They'll be automatically attached to releases

3. **Write a CHANGELOG.md**
   - Script extracts release notes automatically

4. **Test in private repo first**
   - Change `--public` to `--private` in script for testing

5. **Reuse the script**
   - One script works for all your projects!

---

**Script Location:**
`/Users/gursannikov/MyDrive/github-release-auto.sh`

**Estimated Time:** 2-3 minutes per release

---

Ready to release? Just run it! 🚀
