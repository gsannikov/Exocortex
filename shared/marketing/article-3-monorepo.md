# Scaling AI: The Monorepo Architecture for Custom Skills

![Monorepo Architecture Hero](images/monorepo-hero.png)

*Part 3 of the "AI-Augmented Homosapiens" series. [Read Part 2 here](LINK_TO_PART_2).*

---

In [Part 2](LINK_TO_PART_2), I broke down the 8 custom skills that run my digital life. But here's the catch: **building one skill is easy. Managing 8 is a nightmare.**

If you copy-paste your `setup.py` and `prompts` folder 8 times, you've created a maintenance trap.

Today, I'm sharing the **Monorepo Architecture** I use to scale from 1 skill to 100 without losing my mind.

---

## 🏗️ The Problem: The "Skill Sprawl"

When I started, I had 3 separate repos.
*   **Repo 1 (Career)**: Used `openai` library.
*   **Repo 2 (RAG)**: Used `langchain`.
*   **Repo 3 (Voice)**: Used raw `requests`.

**The Result**:
*   Inconsistent logging.
*   3 different ways to handle API keys.
*   Updating the system prompt meant editing 3 files.
*   Zero code reuse.

I realized: **I'm not building scripts. I'm building an Operating System.**

---

## 📐 The Solution: A Unified Monorepo

I consolidated everything into a single repository with a strict structure.

### 1. The Directory Structure

```text
claude-skills/
├── packages/                  # The "Apps"
│   ├── career-consultant/     # Skill 1
│   ├── local-rag/             # Skill 2
│   ├── reading-list/          # Skill 3
│   └── ...
├── shared/                    # The "OS"
│   ├── python/
│   │   ├── mcp_client.py      # Unified MCP connector
│   │   ├── logger.py          # Standardized logging
│   │   └── config_loader.py   # YAML config parser
│   └── prompts/
│       └── core_identity.md   # "You are an AI assistant..."
├── .github/                   # CI/CD
│   └── workflows/
│       └── validate-skills.yml
└── pyproject.toml             # Workspace dependencies
```

**Why this wins**:
*   **One Config**: All skills share the same `user-config.yaml` structure.
*   **One Identity**: The `core_identity.md` ensures all skills "feel" like the same assistant.
*   **Shared Core**: If I improve the MCP client, *all* skills get better instantly.

---

## 🧩 Shared Utilities (The "DRY" Principle)

The magic happens in the `shared/` folder.

**Example: The Unified MCP Client**
Instead of every skill writing its own HTTP requests to talk to the filesystem or Apple Notes, they import a shared client.

```python
# shared/python/mcp_client.py
class MCPClient:
    def read_file(self, path):
        # Standardized error handling
        try:
            return self.client.call_tool("filesystem", "read_file", path=path)
        except MCPError as e:
            logger.error(f"Failed to read {path}: {e}")
            raise
```

**Usage in a Skill**:
```python
from shared.mcp_client import MCPClient

def run(self):
    content = MCPClient().read_file("notes.md")
    # No boilerplate. Just logic.
```

---

## 🔄 CI/CD: Automated Validation

You don't want to break your "Career Consultant" while fixing your "Voice Memos".

I use **GitHub Actions** to validate every pull request.

**The Workflow (`validate-skills.yml`)**:
1.  **Detect Changes**: Which packages changed?
2.  **Lint**: Run `ruff` and `mypy` on changed packages.
3.  **Test**: Run `pytest` for specific skills.
4.  **Verify Config**: Ensure `SKILL.md` and `config.yaml` exist and are valid.

```yaml
# .github/workflows/validate-skills.yml
name: Validate Skills
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          for package in packages/*; do
            if [ -f "$package/tests" ]; then
              pytest "$package"
            fi
          done
```

---

## 📦 Version Management

Each skill has a `version.yaml`.

```yaml
# packages/career-consultant/version.yaml
version: 1.2.0
last_updated: 2025-11-24
changes:
  - Added support for PDF resumes
```

When the system loads, it checks these versions. If a skill is outdated or has a breaking change, the main runner flags it.

---

## 🛡️ The "Skill Interface" Standard

To make skills plug-and-play, every skill MUST implement a standard interface in its `SKILL.md` (the prompt file):

1.  **Identity**: Who are you? (Inherits from shared)
2.  **Capabilities**: What tools do you have?
3.  **Input Schema**: What do you expect? (URL, Text, File)
4.  **Output Schema**: What will you return? (JSON, Markdown)

This means my main "Router" agent doesn't need to know *how* a skill works. It just knows:
*"If user asks for job analysis -> Send to Career Consultant."*

---

## 🚀 The Result

*   **Onboarding a new skill**: Takes 10 minutes. Copy template -> Write logic -> Add to registry.
*   **Refactoring**: I switched from `requests` to `httpx` in one file (`shared/mcp_client.py`), and 8 skills were updated instantly.
*   **Stability**: CI catches broken imports before I merge.

**This is how you move from "tinkering" to "engineering".**

---

## 🔮 Next Week: Lessons Learned

We've covered the **What** (Pinned Post), the **How** (Skills Deep Dive), and the **Structure** (Monorepo).

Next week, I'll share the **Pain**: The failures, the hallucinations, and the hard lessons learned from 6 months of building this.

**Follow to avoid my mistakes.** 👇

#SoftwareArchitecture #Monorepo #DevOps #Python #AI
