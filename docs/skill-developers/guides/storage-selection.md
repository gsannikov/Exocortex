# Storage Backend Selection Guide
**Choose the right storage for your Claude skill**

---

## 🎯 Quick Decision Tree

```
Do you need data to persist between sessions?
├─ NO → Use Checkpoint System (Option 3)
│
└─ YES → Do you use multiple devices?
    ├─ NO → Use Local Filesystem (Option 1)
    │
    └─ YES → Do you want version history?
        ├─ YES → Use GitHub Repo (Option 2)
        │
        └─ NO → Need nice UI for viewing data?
            ├─ YES → Use Notion (Option 5)
            │
            └─ NO → Use Email System (Option 4)
```

---

## 📊 Comparison Matrix

| Feature | Local FS | GitHub | Checkpoint | Email | Notion |
|---------|----------|--------|------------|-------|--------|
| **Setup Time** | 5 min | 3 min | 0 min | 2 min | 5 min |
| **Persistence** | ✅ | ✅ | ⚠️ Manual | ✅ | ✅ |
| **Multi-Device** | ❌ | ✅ | ⚠️ Manual | ✅ | ✅ |
| **Offline** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Version History** | ❌ | ✅ | ❌ | ⚠️ Limited | ⚠️ Limited |
| **Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Privacy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Collaboration** | ❌ | ✅ | ⚠️ Manual | ❌ | ✅ |
| **Easy Backup** | ⚠️ Manual | ✅ Auto | ✅ Files | ✅ Auto | ✅ Auto |
| **View/Edit UI** | Text Editor | GitHub Web | Text Editor | Email Client | Notion UI |
| **Cost** | Free | Free | Free | Free | Free tier |
| **Dependencies** | MCP FS | GitHub + PyGithub | None | Email access | Notion API |

---

## 1️⃣ Local Filesystem

### Best For
- ✅ Single device use
- ✅ Maximum privacy (data never leaves machine)
- ✅ Offline work
- ✅ Fastest performance
- ✅ Large datasets (GBs)
- ✅ Direct file editing

### Not Good For
- ❌ Multi-device sync
- ❌ Automatic backup
- ❌ Collaboration
- ❌ Remote access

### When to Choose
**Use if:**
- Primary/only development machine
- Privacy is critical
- Working offline frequently
- Need maximum speed
- Large files (>100MB)

**Example Use Cases:**
- Personal productivity tools
- Local data analysis
- Offline-first applications
- Privacy-focused tools

### Setup Effort
⭐⭐⭐ (3/5) - Requires MCP configuration

### Configuration
```yaml
# user-data/config/storage-config.yaml
storage:
  backend: "local"
  local:
    base_path: "/absolute/path/to/user-data"
```

---

## 2️⃣ GitHub Repository

### Best For
- ✅ Multi-device sync
- ✅ Version control (full history)
- ✅ Collaboration (share repo)
- ✅ Automatic backup
- ✅ Code/structured data (YAML, markdown)
- ✅ Can revert mistakes

### Not Good For
- ❌ Large binary files (>100MB)
- ❌ Very frequent updates (1000s/hour)
- ❌ Offline work
- ❌ Non-technical users

### When to Choose
**Use if:**
- Work from multiple machines
- Want to see change history
- Collaborating with team
- Already use GitHub
- Want automatic backup

**Example Use Cases:**
- Team workflows
- Configuration management
- Multi-device personal use
- Open-source skill development

### Setup Effort
⭐⭐ (2/5) - Create repo + token

### Configuration
```yaml
# user-data/config/storage-config.yaml
storage:
  backend: "github"
  github:
    repo: "username/repo-name"
    token: "ghp_xxxxxxxxxxxx"
    branch: "main"
```

---

## 3️⃣ Checkpoint System

### Best For
- ✅ Zero setup
- ✅ Demo/testing
- ✅ Occasional use
- ✅ Learning/exploration
- ✅ Full portability (you control files)

### Not Good For
- ❌ Regular production use
- ❌ Automatic persistence
- ❌ Frequent updates
- ❌ Forgetting to export

### When to Choose
**Use if:**
- Just trying out the skill
- Don't want any setup
- Occasional use (weekly/monthly)
- Want maximum control of data
- Teaching/demos

**Example Use Cases:**
- Initial skill testing
- Workshop/training
- Proof-of-concept
- Temporary projects

### Setup Effort
⭐ (1/5) - No setup needed

### Configuration
```yaml
# user-data/config/storage-config.yaml
storage:
  backend: "checkpoint"
  checkpoint:
    auto_export_after: 10  # Export after N operations
```

### Usage Pattern
```
Session Start:
You: "Import last checkpoint" (upload file)
Claude: [Restores state]

During Session:
[Work normally]

Session End:
You: "Export checkpoint"
Claude: [Creates artifact with all data]
You: Download and save
```

---

## 4️⃣ Email Storage

### Best For
- ✅ Multi-device (works anywhere with email)
- ✅ Built-in backup (email archive)
- ✅ No special services needed
- ✅ Maximum portability
- ✅ Searchable (email search)

### Not Good For
- ❌ Large files
- ❌ Frequent updates (email limits)
- ❌ Real-time sync
- ❌ Privacy (email content visible to provider)

### When to Choose
**Use if:**
- Want to access from ANY device
- Already heavily use email
- Don't want vendor lock-in
- Want automatic backup via email
- Small, infrequent updates

**Example Use Cases:**
- Mobile access (via email app)
- Long-term archival
- Cross-platform (any device with email)
- Emergency backup option

### Setup Effort
⭐⭐ (2/5) - Configure email access

### Configuration
```yaml
# user-data/config/storage-config.yaml
storage:
  backend: "email"
  email:
    imap_server: "imap.gmail.com"
    smtp_server: "smtp.gmail.com"
    email: "your-email@gmail.com"
    password: "app-password"  # Use app password, not real password
    folder: "Claude/SkillData"  # Email folder
```

### Email Rules Setup
**Gmail:**
```
1. Create label: "Claude/SkillData"
2. Create filter:
   - From: your-email@gmail.com
   - Subject: [Claude Skill Data]
   - Apply label: Claude/SkillData
   - Skip inbox (archive)
```

**Outlook:**
```
1. Create folder: "Claude/SkillData"
2. Create rule:
   - From: your-email@outlook.com
   - Subject contains: [Claude Skill Data]
   - Move to: Claude/SkillData
```

---

## 5️⃣ Notion Database

### Best For
- ✅ Nice UI for viewing data
- ✅ Mobile access (Notion app)
- ✅ Cross-device sync
- ✅ Structured/searchable data
- ✅ Can create dashboards
- ✅ Already use Notion heavily

### Not Good For
- ❌ Raw YAML/markdown (converts to blocks)
- ❌ Large files
- ❌ Complex nested structures
- ❌ Frequent small updates (API limits)

### When to Choose
**Use if:**
- Already use Notion for everything
- Want to view data in nice UI
- Need mobile access
- Want to create dashboards/reports
- Non-technical users viewing data

**Example Use Cases:**
- Personal knowledge management
- Team dashboards
- CRM-like applications
- Content management

### Setup Effort
⭐⭐⭐⭐ (4/5) - Setup integration + database

### Configuration
```yaml
# user-data/config/storage-config.yaml
storage:
  backend: "notion"
  notion:
    token: "secret_xxxxxxxx"
    database_id: "xxxxxxxxxx"
```

---

## 🎯 Recommendations by Skill Type

### Personal Productivity Skills
**Recommended:** Local Filesystem or GitHub
- Fast access
- Privacy
- Can use git for backup

### Team/Collaboration Skills
**Recommended:** GitHub or Notion
- Multi-user access
- Sync across team
- Version control

### Mobile-Accessible Skills
**Recommended:** Email or Notion
- Access from phone
- Simple sync

### Demo/Learning Skills
**Recommended:** Checkpoint
- Zero setup
- Easy to try

### Data Analysis Skills
**Recommended:** Local Filesystem
- Large files
- Fast access
- Direct file manipulation

---

## 🔄 Migration Paths

### Local → GitHub
```bash
cd user-data
git init
git add .
git commit -m "Initial"
git remote add origin <url>
git push
# Update config to github backend
```

### GitHub → Local
```bash
git clone <repo-url> user-data
# Update config to local backend
```

### Checkpoint → Any
```
1. Import checkpoint
2. Change backend in config
3. Data automatically migrates
```

### Any → Checkpoint
```
1. "Export checkpoint"
2. Change backend to checkpoint
3. Import when needed
```

---

## ⚙️ Configuration

### Choosing Backend at Setup

**Option 1: Interactive (Recommended)**
```python
# First run - skill asks user
print("Choose storage backend:")
print("1. Local Filesystem (fast, private)")
print("2. GitHub (multi-device, versioned)")
print("3. Checkpoint (zero setup)")
print("4. Email (universal access)")
print("5. Notion (nice UI)")

choice = input("Enter number: ")
```

**Option 2: Config File**
```yaml
# Edit user-data/config/storage-config.yaml before first use
storage:
  backend: "local"  # or github, checkpoint, email, notion
```

**Option 3: Environment Variable**
```bash
export SKILL_STORAGE_BACKEND=github
```

---

## 🧪 Testing Each Backend

```bash
# Test local
./test-storage.sh local

# Test github
./test-storage.sh github

# Test checkpoint
./test-storage.sh checkpoint

# Test email
./test-storage.sh email

# Test notion
./test-storage.sh notion
```

---

## 📝 Documentation Requirements

For each skill, document:

```markdown
## Storage Backend

This skill supports multiple storage backends:

**Recommended:** Local Filesystem or GitHub

**Supported:**
- Local Filesystem (fast, private)
- GitHub Repository (multi-device, versioned)
- Checkpoint System (zero setup)
- Email Storage (universal access)
- Notion Database (nice UI)

**Setup:** See [storage-setup.md](docs/storage-setup.md)
```

---

## 🎯 Default Recommendation

**For Template:**
- Default: Local Filesystem
- Reason: Most common use case, best performance
- Fallback: Checkpoint (if MCP not configured)

**For Production Skills:**
- Let developer choose based on use case
- Document recommended option
- Support switching backends

---

## 📊 Backend Selection Checklist

**Choose Local Filesystem if:**
- [ ] Single device primary use
- [ ] Need maximum speed
- [ ] Privacy critical
- [ ] Offline work needed
- [ ] Large files (>100MB)

**Choose GitHub if:**
- [ ] Multi-device sync needed
- [ ] Want version history
- [ ] Team collaboration
- [ ] Automatic backup important
- [ ] Already use GitHub

**Choose Checkpoint if:**
- [ ] Just testing
- [ ] Occasional use
- [ ] Zero setup requirement
- [ ] Demo/workshop

**Choose Email if:**
- [ ] Need universal access
- [ ] Any device, anywhere
- [ ] Small, infrequent updates
- [ ] Want email archive backup

**Choose Notion if:**
- [ ] Heavy Notion user
- [ ] Need nice UI
- [ ] Mobile access important
- [ ] Dashboard/reports needed

---

**Still unsure? Start with Checkpoint (zero setup), migrate later when needs are clear.**
