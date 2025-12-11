# The "Second Brain" Architecture: A Deep Dive into 6 Custom AI Skills

![Skills Architecture Hero](../images/skills-architecture-hero.png)

*Part 2 of the "AI-Augmented Homosapiens" series. [Read Part 1 here](LINK_TO_PART_1).*

---

In the [first article](LINK_TO_PINNED_POST), I outlined the high-level architecture of my local-first AI system. Today, we're opening the hood.

I don't use generic AI tools. I use **6 specialized skills**—modular, versioned code containers that run locally and connect my LLM to my digital life.

Here is the technical breakdown of each production skill and the patterns that power them.

---

## 🏗️ The Core Pattern: What is a "Skill"?

Before diving in, let's define the architecture. A "Skill" in my monorepo isn't just a prompt. It's a structured package:

```python
# The Anatomy of a Skill
class Skill:
    def __init__(self):
        self.system_prompt = load_prompt("system.md") # The "Brain"
        self.tools = load_tools("tools.py")           # The "Hands"
        self.memory = load_memory("context.md")       # The "Memory"
        self.config = load_config("config.yaml")      # The "Settings"
```

All skills share a common **MCP (Model Context Protocol)** layer for file access, web scraping, and Apple Notes integration.

---

## 🟢 Production Skills (Live & Daily Use)

### 1. Job Analyzer 💼
**Purpose**: Systematically analyze job postings and optimize applications. (Now split into `job-analyzer` and `interview-prep`).

**The Problem**: Applying to jobs is a black box. You forget what you applied to, and tailoring CVs is slow.
**The Solution**: A skill that maintains a structured database of my career profile and matches it against scraped job descriptions.

**Architecture**:
```mermaid
graph LR
    Job[LinkedIn Job] -->|Scrape| Text
    Text -->|Analyze| Scorer
    Profile[CV Variants] --> Scorer
    Scorer -->|Score| Result
    Result -->|Strategy| Output
```
*   **Input**: LinkedIn URL (via Bright Data MCP)
*   **Data**: `profile.yaml` (3 CV variants: EM, TPM, AI Engineer)
*   **Logic**: Scoring algorithm (0-100) based on Keywords, Seniority, and Tech Stack.
*   **Output**: Match Score + Tailored Cover Letter Strategy.

**Code Snippet (Scoring Logic)**:
```python
def score_job(job_desc, user_profile):
    # Vector similarity for semantic match
    semantic_score = rag.similarity(job_desc, user_profile.experience)
    
    # Hard constraints check
    hard_skills_score = check_constraints(job_desc, ["Python", "LLM", "System Design"])
    
    return (semantic_score * 0.7) + (hard_skills_score * 0.3)
```

### 2. Local RAG (Memory) 🧠
**Purpose**: Hybrid semantic + keyword search over my entire personal knowledge base.

**The Stack**:
*   **Vector DB**: ChromaDB (default) or Qdrant (scalable)
*   **Keyword Search**: BM25 with inverted index
*   **Embeddings**: `all-MiniLM-L6-v2` (384-dim, runs on CPU)
*   **Reranking**: Cross-encoder (optional, for precision)
*   **Storage**: Hybrid storage with ChromaDB SQLite and BM25 index in `~/MyDrive/claude-skills-data/local-rag/`
    *   `vectordb/` - ChromaDB collections and SQLite database
    *   `state/` - Ingestion state tracking and BM25 index

**Workflow**:
```mermaid
graph TD
    File[Document] -->|Watcher| Change{Changed?}
    Change -- Yes --> Chunk[Smart Chunker]
    Chunk --> Embed[Embedding + BM25 Index]
    Embed --> Vector[Vector Store]
    Vector -->|Hybrid Query| Fusion[Result Fusion]
    Fusion -->|Optional| Rerank[Cross-Encoder]
    Rerank -->|Results| Claude
```

**Chunking Strategies** (configurable):
*   **Fixed**: Character-based with overlap
*   **Sentence**: Respects sentence boundaries
*   **Semantic**: Groups by embedding similarity
*   **Template**: Document-aware (markdown headers, code functions)

**Search Methods**:
*   **Vector-only**: Pure semantic similarity
*   **BM25-only**: Keyword matching with IDF weighting
*   **Hybrid** (default): RRF fusion of both for best recall

**Performance**: <150ms for hybrid search over 10k documents.

### 3. Reading List Manager 📚
**Purpose**: Triage the firehose of information.

**The "Inbox" Pattern**:
1.  **Capture**: I paste URLs into a specific Apple Note ("Reading Inbox").
2.  **Process**: The skill reads the note via Apple Notes MCP.
3.  **Scrape**: Uses Firecrawl to get full text.
4.  **Synthesize**: Summarizes (150 words) + Categorizes + Prioritizes.
5.  **Archive**: Moves processed links to `archive.md`.

**Result**: I only read what matters. The rest is indexed for later search.

### 4. Voice Memos Intelligence 🎙️
**Purpose**: Capture fleeting thoughts and turn them into action.

**The Challenge**: Voice memos usually die in the app.
**The Fix**:
*   **Input**: Audio files (m4a) from iCloud Drive.
*   **Process**: Whisper (local) or API for transcription.
*   **Intelligence**: Claude analyzes the text.
    *   *Hebrew/English mixed support*
    *   *Action Item Extraction*
    *   *Topic Categorization*

### 5. Ideas Capture 💡
**Purpose**: Structured thinking partner.

**Workflow**:
*   I dump a raw idea (chat or voice).
*   Skill asks clarifying questions (Socratic method).
*   Skill formats it into a structured **One-Pager**:
    *   Problem Statement
    *   Proposed Solution
    *   Risks
    *   Next Steps
*   Saves to `ideas/` directory as Markdown.

### 6. Social Media Post Generator 📱
**Purpose**: Generate platform-optimized posts using algorithm insights and best practices.

**The Challenge**: Each platform has different character limits, hashtag strategies, and algorithm priorities.
**The Fix**: A skill that encodes platform-specific best practices (updated for 2025) and generates tailored content.

**Supported Platforms**:

| Platform | Char Limit | Hashtags | Best For |
|----------|------------|----------|----------|
| Threads | 500 (10K extended) | None | Conversational, questions |
| X (Twitter) | 280 (25K Blue) | 1-2 max | Concise announcements |
| LinkedIn | 3,000 | 3-5 max | Professional deep-dives |

**Algorithm Priorities (2025)**:
*   **Threads**: Engagement (40%) > Recency (30%) > Relevance (20%) > Profile (10%)
*   **X**: Engagement rate > Recency > Media > Authenticity
*   **LinkedIn**: Dwell time > Engagement > Relevance > Connections

**Output Format**:
Each generated post includes:
*   **Platform**: Target platform
*   **Character Count**: Current/limit
*   **Engagement Hooks**: Questions, CTAs used
*   **Media Suggestion**: Recommended visuals
*   **Best Posting Time**: Optimal time for US audience
*   **Engagement Score**: 1-10 rating

**Example Output**:
```
Platform: Threads
Style: Short & Punchy
Character Count: 274/500

Teach Claude Code to automate like a Pro.

Navigator v3.3.1:
✅ One-command updates
✅ Figma MCP integration
✅ Storybook + Chromatic automation
✅ 18 skills total

"Update Navigator" → Done in 2 min

Install: /plugin marketplace add alekspetrov/navigator

What workflow would you automate next?

---
Metadata:
- Engagement Hook: Opening statement + closing question
- Visual Suggestion: Terminal screenshot
- Best Time: Tuesday 10 AM ET
- Engagement Score: 8.5/10
```

---

## 🟡 Bonus: Meeting Recorder

The Voice Memos skill includes a **Meeting Recorder** component—a production-grade macOS menu bar app built in Swift that captures audio from meeting applications (Zoom, Google Meet, Teams).

**Features**:
- **ScreenCaptureKit**: Uses Apple's modern API (no BlackHole needed)
- **Swift 6 Concurrency**: Full Sendable compliance for thread-safe audio capture
- **Auto-Detection**: Detects when meeting apps start
- **Smart Compression**: 64kbps AAC optimized for speech (~30MB/hour)
- **Auto-Chunking**: Long meetings split into processable chunks
- **Menu Bar UI**: Unobtrusive recording controls with status indicators

**Architecture**:
```swift
// AudioCapture.swift - Thread-safe audio routing
@MainActor
final class AudioCapture: NSObject, Sendable {
    func captureAudio(from app: SCRunningApplication) async throws
}
```

**Use Case**: "What did we agree on in the standup?" → Process meeting recordings → Query transcripts via RAG.

---

## 🛠️ How It All Fits Together

This isn't a collection of scripts. It's a **System**.

*   **Shared Library**: All skills use `shared/utils` for logging, config, and MCP clients.
*   **Unified Context**: The RAG skill is available to *all* other skills. The Career Consultant can ask RAG "What projects did I do with Python?" to tailor a CV.
*   **Single Interface**: I interact with everything through one Claude Desktop window.

## 🛡️ Strategic Advantages: Why This Architecture Wins

Beyond the cool factor, there are three hard strategic reasons I built it this way:

### 1. Radical Data Sovereignty
My life isn't locked in a proprietary database.
*   **Format**: Everything is plain text (YAML, Python, Markdown).
*   **Access**: I can edit my "memory" with a text editor.
*   **Exit Strategy**: If I want to leave, I just `zip` the folder. No "Export Data" requests, no API limits, no dependency on Notion/Google/Microsoft ecosystems.

### 2. Decoupled Architecture (The "Anti-Fragile" Design)
The AI landscape changes every week. This system is designed to survive the churn.
*   **LLM Agnostic**: While I use Claude today, the skills are written in generic Python. They can be repointed to OpenAI, Gemini, or a local Llama model with minimal changes.
*   **Tool Agnostic**: I use Apple Notes for convenience, but swapping it for Google Keep or a text file is just changing one MCP connector. The core logic stays the same.
*   **Future Proof**: Skills can be converted into local Docker containers wrapped with MCP, making them accessible from *any* client, not just Claude Desktop.

### 3. Enterprise-Ready by Default (The Bonus)
Because this is an **edge design** (local code, local data), it solves the biggest blocker for enterprise AI adoption: **Data Privacy**.
*   This entire system can run behind a corporate firewall.
*   Connect it to an internal enterprise LLM, and you have a full agentic workforce without a single byte of data leaving the building.

---

## 🔄 Platform Independence: AlignTrue Integration

One of the biggest challenges with AI skills is platform lock-in. What if you want to switch from Claude to OpenAI? What if your team uses different AI assistants? What if a new, better model launches tomorrow?

### The Multi-Platform Challenge

Different AI platforms expect instructions in different formats:
- **Claude Desktop**: `CLAUDE.md` in project root
- **OpenAI Codex**: `AGENTS.md` 
- **Cursor IDE**: `.cursor/rules/*.mdc` multi-file format
- **Google Antigravity**: Platform-agnostic markdown
- **Windsurf, Cody, Continue**: Each with custom configuration

Building skills that work everywhere requires maintaining multiple versions of the same instructions—a maintenance nightmare that kills productivity.

###AlignTrue: The Solution

I integrated [AlignTrue](https://github.com/aligntrue/aligntrue) to solve this problem elegantly:

```yaml
# .aligntrue/config.yaml
mode: solo
sources:
  - type: local
    path: .aligntrue/rules
exporters:
  - claude          # Claude Desktop (CLAUDE.md)
  - openai-codex    # OpenAI Codex CLI (AGENTS.md)
  - cursor          # Cursor IDE (.cursor/rules/*.mdc)
```

**The Workflow:**
1. Maintain **ONE** source file: `.aligntrue/rules/CLAUDE.md`
2. Run `aligntrue sync`
3. Platform-specific files auto-generate from the single source of truth

**The Architecture:**

```mermaid
graph TD
    Source[/.aligntrue/rules/CLAUDE.md/]
    
    Source -->|sync| Claude[CLAUDE.md<br/>Claude Desktop]
    Source -->|sync| OpenAI[AGENTS.md<br/>OpenAI Codex]
    Source -->|sync| Cursor[.cursor/rules/*.mdc<br/>Cursor IDE]
    Source -->|sync| Anti[Platform-agnostic<br/>Google Antigravity]
    
    Dev1[Developer 1<br/>Uses Claude] --> Claude
    Dev2[Developer 2<br/>Uses GPT-4] --> OpenAI
    Dev3[Developer 3<br/>Uses Cursor] --> Cursor
    Dev4[Developer 4<br/>Uses Antigravity] --> Anti
    
    style Source fill:#fef3c7,stroke:#92400e,stroke-width:3px
    style Claude fill:#e3f2fd,stroke:#1565c0
    style OpenAI fill:#f3e5f5,stroke:#7b1fa2
    style Cursor fill:#e8f5e9,stroke:#2e7d32
    style Anti fill:#ffebee,stroke:#c62828
```

### Benefits for SDK Developers

**For Open Source Contributors:**
- Clone the repo and use **your** preferred AI assistant
- No manual format conversion needed
- Guaranteed consistency across platforms
- Lower barrier to entry—use familiar tools

**For Teams:**
- Team members can use different AI platforms
- Instructions stay synchronized automatically
- No "works on my machine" issues
- Easy onboarding regardless of AI preference

**For You:**
- Switch AI platforms without migration pain
- Future-proof against new AI assistants
- No vendor lock-in
- True platform independence

### Real-World Impact

Since integrating AlignTrue, the claude-skills repository has had contributors using:
- **Claude Desktop** (original target)
- **OpenAI Codex** via CLI
- **Cursor IDE** for integrated development
- **Google Antigravity** (the platform we're using right now!)

All working on the same codebase, with the same capabilities, **without manual instruction translation**. This is the future of AI-augmented development: platform-agnostic, vendor-independent, and truly open.

This architectural decision makes claude-skills not just open-source in code, but **open-source in platform accessibility**. You're never locked in. You always have choice.

---

## 🚀 Next Up: The Monorepo

Managing 6+ skills can be a nightmare. In the next article, I'll show you the **Monorepo Architecture** that keeps this maintainable: CI/CD, shared dependencies, and standardized testing.

**Follow to catch Part 3 next week.**

---

*Questions about a specific skill? Ask in the comments and I'll share the prompt structure.* 👇

#AI #Engineering #LocalFirst #Python #LLM
 
