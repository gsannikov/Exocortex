# Usage Guide

Learn how to use 2ndBrain_RAG to search and retrieve information from your documents using Claude.

---

## Quick Start

Once installed and configured, 2ndBrain_RAG automatically:
1. Watches your documents folder
2. Indexes new and modified files
3. Makes them searchable via Claude

You interact with it entirely through Claude Desktop/Code.

---

## Available Tools

2ndBrain_RAG provides 5 MCP tools that Claude can use:

### 1. `rag.search`

**Purpose**: Semantic search over your documents

**When Claude uses it**: When you ask questions about your documents

**Example prompts**:
```
"Search my documents for information about RAG systems"
"Find notes about the meeting with client X"
"What do my documents say about Python optimization?"
```

**What it returns**: Top relevant passages with:
- Document path
- Text excerpt
- Relevance score
- Byte offset (for retrieval)

---

### 2. `rag.get`

**Purpose**: Retrieve specific document sections

**When Claude uses it**: After searching, to read full context

**Example workflow**:
```
You: "Find my notes about the API design"
Claude: [Uses rag.search, finds relevant section]
Claude: [Uses rag.get to read full context]
Claude: "According to your notes in docs/api-design.md..."
```

**What it returns**: Full text window around the match

---

### 3. `rag.stats`

**Purpose**: Get index statistics

**When Claude uses it**: When you ask about index status

**Example prompts**:
```
"How many documents are indexed?"
"What's the status of my RAG index?"
"Show me index statistics"
```

**What it returns**:
- Total documents indexed
- Total chunks
- Last indexing time
- Storage size

---

### 4. `rag.reindex`

**Purpose**: Manually trigger reindexing

**When Claude uses it**: When you ask to reindex

**Example prompts**:
```
"Reindex all my documents"
"Reindex the file /path/to/file.pdf"
"Update the index"
```

**What it does**:
- Full reindex (all documents)
- Partial reindex (specific files)
- Useful after major changes

---

### 5. `rag.invalidate`

**Purpose**: Remove documents from index

**When Claude uses it**: When you want to remove files

**Example prompts**:
```
"Remove file.pdf from the index"
"Stop indexing /path/to/old-project/"
```

**What it does**: Deletes document chunks from index

---

## Common Workflows

### Workflow 1: Initial Setup

**Scenario**: You just installed 2ndBrain_RAG

```
1. You: "Can you check my RAG index status?"
   Claude: [Uses rag.stats]
   Claude: "Your index is empty. Would you like me to index your documents?"

2. You: "Yes, please reindex everything"
   Claude: [Uses rag.reindex]
   Claude: "Indexing 342 documents... This may take a few minutes."

3. [Wait for indexing to complete]

4. You: "What's the status now?"
   Claude: [Uses rag.stats]
   Claude: "Index now contains 342 documents with 5,234 chunks."
```

**Time**: ~30 seconds per 100 documents

---

### Workflow 2: Finding Information

**Scenario**: Looking for specific information

```
You: "What do my notes say about improving search relevance?"

Claude: [Uses rag.search with query="improving search relevance"]
Claude: [Finds relevant passages in notes/rag-improvements.md]
Claude: [Uses rag.get to read full context]

Claude: "According to your notes in notes/rag-improvements.md,
        you explored three approaches to improving search relevance:
        1. Hybrid search (BM25 + semantic)
        2. Query expansion
        3. Reranking with cross-encoder

        You noted that hybrid search gave the best results..."
```

**Result**: Claude synthesizes answer with citations

---

### Workflow 3: Cross-Document Questions

**Scenario**: Questions spanning multiple documents

```
You: "Across all my project docs, what are the common challenges mentioned?"

Claude: [Uses rag.search with "challenges" or "problems"]
Claude: [Finds matches in multiple documents]
Claude: [Uses rag.get on top matches to read context]

Claude: "Looking across your project documents, I found these recurring challenges:

        From project-alpha/notes.md:
        - Performance issues with large datasets

        From project-beta/retrospective.md:
        - Integration complexity with legacy systems

        From project-gamma/design.md:
        - Balancing features vs. simplicity

        [Full analysis...]"
```

**Power**: Finds patterns you might have missed

---

### Workflow 4: Automatic Reindexing

**Scenario**: You edit a document

```
1. [You save changes to project-notes.md]

2. [File watcher detects change]

3. [Automatic reindexing happens in background]

4. [No action needed from you]

5. You: "What does project-notes.md say about X?"
   Claude: [Searches using updated index]
   Claude: [Returns results with your latest changes]
```

**Time**: Usually <5 seconds for updated file

**Note**: You can continue working during reindexing

---

## Tips for Effective Search

### 1. Use Natural Language

**Good**:
```
"What are the best practices for error handling in my notes?"
"Find discussions about user authentication"
```

**Also works**:
```
"error handling best practices"
"user authentication"
```

**Why**: Semantic search understands both

---

### 2. Be Specific for Better Results

**Vague**:
```
"Tell me about the project"
```

**Better**:
```
"What were the main decisions in the API design for project Alpha?"
```

**Why**: More specific queries return more relevant results

---

### 3. Ask Follow-Up Questions

```
You: "Find notes about database optimization"
Claude: [Returns results from notes/db-perf.md]

You: "Can you show me more context around the indexing strategy?"
Claude: [Uses rag.get with larger window]

You: "Are there other documents that mention indexing?"
Claude: [Expands search]
```

**Power**: Claude maintains context across the conversation

---

### 4. Request Different Perspectives

```
You: "Search for mentions of 'technical debt'"
Claude: [Finds 12 references]

You: "Summarize the common themes"
Claude: [Analyzes and synthesizes]

You: "Which documents are most concerned about it?"
Claude: [Ranks by frequency/emphasis]
```

---

### 5. Combine with Claude's Knowledge

```
You: "My notes mention using Redis for caching. What are best practices?"

Claude: [Uses rag.search to find your notes]
Claude: [Combines with built-in knowledge]
Claude: "According to your notes in arch/caching.md, you're planning
        to use Redis for session storage. Here are best practices
        that complement your approach:

        From your notes:
        - [Your specific context]

        General best practices:
        - [Claude's knowledge]
        ..."
```

**Result**: Personalized advice based on your context

---

## Understanding Search Results

### Result Format

When Claude searches, results include:

1. **Path**: Document location
2. **Excerpt**: Relevant text snippet
3. **Score**: Relevance (0-1, higher is better)
4. **Offset**: Position in document (for retrieval)

### Relevance Scores

- **0.8-1.0**: Highly relevant, exact or near match
- **0.6-0.8**: Relevant, topically related
- **0.4-0.6**: Somewhat relevant, tangentially related
- **<0.4**: Less relevant (usually filtered out)

### No Results?

If search returns nothing:

1. **Check index**: "What's my RAG index status?"
2. **Try different phrasing**: Semantic search is flexible
3. **Reindex**: "Please reindex my documents"
4. **Verify file is indexed**: Check file extension is in `ALLOWED_EXTS`

---

## Working with Different Document Types

### PDFs

**Text-based PDFs**: Indexed automatically
**Scanned PDFs**: OCR automatically applied
**Encrypted PDFs**: Cannot be indexed

**Tip**: For better OCR, use high-quality scans

---

### Office Documents

**Supported**: DOCX, PPTX, XLSX
**Indexed**: Text, headings, table contents
**Not indexed**: Embedded images (unless OCR is applied)

---

### Markdown and Text

**Supported**: .md, .txt
**Indexed**: All text content
**Preserves**: Heading structure (useful for context)

---

### Code Files

**Not currently supported** by default

**Workaround**: Add file extensions to `ALLOWED_EXTS`:
```bash
ALLOWED_EXTS=.pdf,.txt,.md,.py,.js,.go
```

**Note**: Code search is text-based, no syntax awareness

---

## Advanced Usage

### Custom Search Parameters

You can ask Claude to adjust search behavior:

```
"Search with more results: find 20 documents about AI"
→ Claude uses k=20 instead of default

"Search only in the /projects/ folder"
→ Claude filters results by path
```

---

### Temporal Queries

```
"What documents did I work on this week?"
→ Uses file modification times

"Show me my notes from last month"
→ Filters by date
```

**Note**: Depends on file modification timestamps

---

### Combining Multiple Queries

```
"Search for 'machine learning' AND 'deployment'"
→ Claude searches, filters results

"Find documents about Python OR JavaScript"
→ Claude runs multiple searches, combines
```

---

## Monitoring and Maintenance

### Check Index Health

```
You: "How's my RAG index doing?"

Claude: [Uses rag.stats]
Claude: "Your index contains:
        - 423 documents
        - 8,234 chunks
        - Last updated: 2 minutes ago
        - Size: 234MB
        Everything looks healthy!"
```

---

### Reindex Specific Files

```
You: "I updated my design doc. Can you reindex it?"

Claude: [Uses rag.reindex with specific path]
Claude: "Reindexed /path/to/design.md.
        Found 45 chunks, updated index."
```

---

### Clean Up Old Documents

```
You: "Remove old-project/ from the index"

Claude: [Uses rag.invalidate on directory]
Claude: "Removed 23 documents from old-project/.
        Index now contains 400 documents."
```

---

## Troubleshooting

### "No results found"

**Possible causes**:
1. Document not indexed
2. File type not supported
3. Content doesn't match query

**Try**:
```
"Check RAG index status"
"Reindex my documents"
"Try different search terms"
```

---

### "File not found" errors

**Possible causes**:
1. File moved or deleted
2. Path changed
3. Permission issues

**Fix**:
```
"Reindex everything" → Removes stale references
```

---

### Slow search results

**Possible causes**:
1. Large corpus (>50k documents)
2. Complex query
3. System resource constraints

**Solutions**:
- Increase `CHUNK_SIZE` (fewer chunks)
- Use more specific queries
- Close other applications

---

### Incorrect or outdated results

**Cause**: File changed but not reindexed

**Fix**:
```
"Reindex /path/to/file"
```

**Note**: File watcher should auto-reindex, but may be delayed

---

## Privacy and Security

### What's Stored Locally

- **Document chunks**: Text content, chunked
- **Embeddings**: Vector representations (not readable)
- **Metadata**: Paths, timestamps, offsets
- **State**: Hashes for change detection

### What's NOT Stored

- ❌ Cloud services (everything local)
- ❌ Telemetry or usage data
- ❌ API keys (except for Claude)
- ❌ User credentials

### Where Files Are Stored

```
2ndBrain_RAG/
├── .chromadb/          # Vector database
├── state/              # File state tracking
└── [Your ROOT_DIR is NOT copied, only indexed]
```

**Important**: Original documents stay in your `ROOT_DIR`, only index is stored in `2ndBrain_RAG/`.

---

## Best Practices

### 1. Organize Your Documents

```
documents/
├── projects/
│   ├── alpha/
│   └── beta/
├── notes/
├── research/
└── archive/
```

**Why**: Easier to search by folder, better organization

---

### 2. Use Descriptive Filenames

**Good**: `2024-project-alpha-design-decisions.md`
**Bad**: `doc1.md`

**Why**: Filenames appear in search results, help with context

---

### 3. Regular Maintenance

**Monthly**:
```
"Show me RAG index stats"
"Are there any old documents to clean up?"
```

**As needed**:
```
"Reindex everything" → After major reorganization
```

---

### 4. Tune Configuration

If search quality isn't great:

```bash
# Edit .env

# For longer context:
CHUNK_SIZE=5000

# For more precise matches:
CHUNK_SIZE=1500

# For better embeddings (slower):
EMBED_MODEL=sentence-transformers/all-mpnet-base-v2
```

**Then**: Reindex all documents

---

## What's Next?

- **Advanced tips**: See [Advanced Usage Guide](advanced-usage.md)
- **OCR setup**: See [OCR Configuration Guide](ocr-setup.md)
- **Troubleshooting**: See [Troubleshooting Guide](troubleshooting.md)
- **Feature requests**: Open issue on GitHub

---

## FAQ

**Q: How often does it reindex?**
A: Automatically on file changes, or manually via `rag.reindex`.

**Q: Can I search while indexing?**
A: Yes, search uses existing index. New/updated files appear after indexing completes.

**Q: How do I exclude certain files?**
A: Remove their extensions from `ALLOWED_EXTS` or move them outside `ROOT_DIR`.

**Q: Can I have multiple document folders?**
A: Not currently. Set `ROOT_DIR` to a parent folder containing all subfolders.

**Q: Does it work offline?**
A: Yes (after initial model download). Claude requires internet, but RAG is local.

**Q: How private is this?**
A: Fully private. Documents never leave your machine. Only Claude's responses go to Anthropic.

---

**Happy searching!**

For more help, see:
- [Troubleshooting Guide](troubleshooting.md)
- [GitHub Issues](https://github.com/yourusername/2ndBrain_RAG/issues)
- [Community Discussions](https://github.com/yourusername/2ndBrain_RAG/discussions)

---

**Last Updated**: 2025-11-13
**Applies to**: v0.2.0+
