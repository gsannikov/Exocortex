# GitHub Storage Backend - Design Proposal

## Why GitHub?

**Perfect fit for Claude skills:**
- ✅ Native markdown/YAML support
- ✅ Version control (see all changes)
- ✅ Cross-device sync automatic
- ✅ Free private repos
- ✅ Can view/edit on web
- ✅ Git diffs show exactly what changed
- ✅ Backup built-in
- ✅ Can share/collaborate
- ✅ Industry standard

**Better than local filesystem:**
- ✅ Multi-device (use skill on any machine)
- ✅ Automatic backup
- ✅ History of all changes
- ✅ Can revert mistakes

**Better than Google Drive:**
- ✅ Perfect for code/structured data
- ✅ No format conversion
- ✅ Better for text files
- ✅ Version control

---

## Setup (One-Time, 3 minutes)

### Step 1: Create Private Repo
```bash
# On GitHub.com
1. Click "New Repository"
2. Name: "my-skill-data" (or anything)
3. ✅ Private
4. Create
```

### Step 2: Create Access Token
```bash
# GitHub Settings > Developer Settings > Personal Access Tokens
1. Generate new token (classic)
2. Name: "Claude Skill Access"
3. Scopes: ✅ repo (full control)
4. Generate token
5. Copy token (save somewhere safe)
```

### Step 3: Configure Skill
```yaml
# user-data/config/storage.yaml
storage:
  type: "github"
  repo: "username/my-skill-data"
  token: "ghp_xxxxxxxxxxxxx"
  branch: "main"
```

**Done!** Works forever now.

---

## Implementation

```python
"""GitHub Storage Backend"""

from github import Github
from datetime import datetime
import yaml
import base64

class GitHubStorage:
    def __init__(self, repo_name: str, token: str, branch: str = "main"):
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)
        self.branch = branch
    
    def save(self, path: str, content: str, message: str = None):
        """Save file to GitHub repo"""
        if message is None:
            message = f"Update {path} - {datetime.now()}"
        
        try:
            # Try to get existing file
            file = self.repo.get_contents(path, ref=self.branch)
            # Update existing
            self.repo.update_file(
                path=path,
                message=message,
                content=content,
                sha=file.sha,
                branch=self.branch
            )
        except:
            # Create new file
            self.repo.create_file(
                path=path,
                message=message,
                content=content,
                branch=self.branch
            )
        
        return True
    
    def load(self, path: str):
        """Load file from GitHub repo"""
        try:
            file = self.repo.get_contents(path, ref=self.branch)
            return file.decoded_content.decode('utf-8')
        except:
            return None
    
    def list_files(self, directory: str = ""):
        """List files in directory"""
        try:
            contents = self.repo.get_contents(directory, ref=self.branch)
            files = []
            for content in contents:
                if content.type == "file":
                    files.append(content.path)
                elif content.type == "dir":
                    # Recursive
                    files.extend(self.list_files(content.path))
            return files
        except:
            return []
    
    def get_history(self, path: str, limit: int = 10):
        """Get commit history for file"""
        commits = self.repo.get_commits(path=path, sha=self.branch)
        history = []
        for commit in commits[:limit]:
            history.append({
                'date': commit.commit.author.date,
                'message': commit.commit.message,
                'author': commit.commit.author.name,
                'sha': commit.sha
            })
        return history
    
    def revert_to(self, path: str, commit_sha: str):
        """Revert file to specific commit"""
        commit = self.repo.get_commit(commit_sha)
        file = self.repo.get_contents(path, ref=commit_sha)
        
        current_file = self.repo.get_contents(path, ref=self.branch)
        self.repo.update_file(
            path=path,
            message=f"Revert {path} to {commit_sha[:7]}",
            content=file.decoded_content.decode('utf-8'),
            sha=current_file.sha,
            branch=self.branch
        )
    
    def diff_versions(self, path: str, sha1: str, sha2: str):
        """Show diff between two versions"""
        comparison = self.repo.compare(sha1, sha2)
        for file in comparison.files:
            if file.filename == path:
                return file.patch
        return None


# Usage in skill
storage = GitHubStorage(
    repo_name="gursannikov/my-skill-data",
    token=config['github_token']
)

# Save
storage.save("config/settings.yaml", yaml_content)

# Load
settings = storage.load("config/settings.yaml")

# History
history = storage.get_history("config/settings.yaml")
print(f"Last 10 changes to settings:")
for h in history:
    print(f"  {h['date']} - {h['message']}")

# Revert if needed
storage.revert_to("config/settings.yaml", "abc123...")
```

---

## User Experience

### Normal Use
```
You: "Update my config"
Claude: [Updates config.yaml in GitHub repo]
        "✅ Config updated (commit: abc123)"

You: "Show config history"
Claude: "Last 10 changes:
         1. 2025-11-03 14:30 - Updated email
         2. 2025-11-02 10:15 - Added new feature
         3. 2025-11-01 16:45 - Initial setup"

You: "Revert to version 2"
Claude: "✅ Reverted config to 2025-11-02 version"
```

### Multi-Device
```
Device A:
You: "Set preference to X"
Claude: [Commits to GitHub]

Device B (later):
You: "What's my preference?"
Claude: [Reads from GitHub]
        "Your preference is X"
        (automatically synced!)
```

---

## Security

**Token Safety:**
```yaml
# NEVER commit token to skill-package
# Store in user-data/config/storage.yaml (gitignored)

storage:
  github_token: "ghp_xxxx"  # ← This file is gitignored
```

**Repo Visibility:**
```
✅ Private repo (only you can access)
✅ Token has minimal permissions (just this repo)
✅ Can revoke token anytime
```

---

## Advantages Over Local Filesystem

| Feature | Local FS | GitHub |
|---------|----------|--------|
| **Setup** | MCP config + restart | PAT + config |
| **Multi-device** | ❌ No | ✅ Yes |
| **Backup** | Manual | Automatic |
| **History** | ❌ No | ✅ Full git history |
| **Revert** | ❌ No | ✅ Easy |
| **Collaborate** | Hard | Easy (share repo) |
| **View online** | ❌ No | ✅ GitHub web |
| **Mobile access** | ❌ No | ✅ GitHub app |
| **Offline** | ✅ Yes | ❌ No |
| **Speed** | Fast | Medium |

---

## Migration Path

**From Local to GitHub:**
```bash
# 1. Create GitHub repo
# 2. Push existing user-data
cd user-data
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/user/my-skill-data
git push -u origin main

# 3. Configure skill to use GitHub
# 4. Done!
```

**From GitHub to Local:**
```bash
# 1. Clone repo
git clone https://github.com/user/my-skill-data user-data

# 2. Configure skill to use local
# 3. Done!
```

---

## Cost

**Free tier:**
- ✅ Unlimited private repos
- ✅ Unlimited commits
- ✅ 1GB storage
- ✅ 500MB file size limit

**More than enough for skill data (typically <10MB)**

---

## Comparison

| Storage | Setup | Persist | Multi-Device | History | Cost |
|---------|-------|---------|--------------|---------|------|
| Local FS | 5 min | ✅ | ❌ | ❌ | Free |
| GitHub | 3 min | ✅ | ✅ | ✅ | Free |
| G Drive | 2 min | ✅ | ✅ | ⚠️  | Free |
| Session | 0 min | ❌ | N/A | ❌ | Free |

---

## Recommendation

**Use GitHub if:**
- ✅ Want multi-device sync
- ✅ Want version history
- ✅ Want to collaborate
- ✅ Want backup
- ✅ Already use GitHub

**Use Local FS if:**
- ✅ Want maximum privacy
- ✅ Want offline capability
- ✅ Single device only
- ✅ Want fastest speed

**Use Both (Hybrid):**
```python
# Primary: GitHub (for sync)
# Fallback: Local (for offline)

try:
    storage = GitHubStorage(...)
except:
    storage = LocalStorage(...)
```

---

## Next Steps

1. Implement GitHubStorage class
2. Add to storage.py as alternative backend
3. Update setup docs
4. Test multi-device workflow
5. Add to release

**Implementation time:** ~2-3 hours
