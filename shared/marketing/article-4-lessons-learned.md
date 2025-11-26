# The Hard Truth: 5 Lessons from Building a Local AI System

![Lessons Learned Hero](images/lessons-learned-hero.png)

*Part 4 of the "AI-Augmented Homosapiens" series. [Read Part 3 here](LINK_TO_PART_3).*

---

In the last three articles, I showed you the shiny architecture. The Monorepo. The RAG system. The diagrams.

But engineering is about trade-offs, and I made **a lot of mistakes** getting here.

If you're building your own AI skills, here is the "blooper reel"—and what I learned from it.

---

## 🛑 Mistake 1: Over-Engineering with "Frameworks"

**The Fail**: When I started, I used a heavy orchestration framework (LangChain). I thought I needed "Chains" and "Agents" and "Memory Classes".
**The Reality**: It was a nightmare to debug. I spent more time fighting the abstraction than writing prompts.
**The Fix**: I deleted it all. My current "framework" is 3 Python files:
1.  `mcp_client.py` (Connect to tools)
2.  `logger.py` (See what's happening)
3.  `Claude` (The LLM does the reasoning)

**Lesson**: **Prompts > Code.** Let the LLM handle the logic. Keep the Python dumb.

---

## 🛑 Mistake 2: The "Context Window" Trap

**The Fail**: For my "Reading List" skill, I initially fed the *entire* HTML of every article into Claude.
**The Reality**:
1.  It cost a fortune.
2.  It hit the 200k limit after 3 articles.
3.  Claude got "distracted" by navigation menus and ads.
**The Fix**: I added a **Scraper & Cleaner** step (using Firecrawl) that strips everything except the main text *before* it hits the LLM.

**Lesson**: **Garbage In, Expensive Garbage Out.** Sanitize your inputs.

---

## 🛑 Mistake 3: Ignoring Latency

**The Fail**: My "Voice Memos" skill used to do everything in one shot: Transcribe -> Summarize -> Extract Actions -> Email me.
**The Reality**: It took 45 seconds. I'd stare at the spinner and think it crashed.
**The Fix**: **Async Pipelines**.
1.  Transcribe (User sees "Done!")
2.  Background: Summarize & Extract.
3.  Background: Update Notion.

**Lesson**: **UI Latency matters.** If it takes >3 seconds, background it.

---

## ✅ What Worked: The "Inbox" Pattern

The single best decision I made was **decoupling capture from processing**.

*   **Don't** try to categorize the link *while* you're saving it.
*   **Do** dump it in a messy "Inbox" note.
*   **Do** let the AI clean it up later.

This removed the friction of using the system. If I had to fill out a form to save a link, I wouldn't do it.

---

## ✅ What Worked: "Small Models" for Triage

I don't use Claude 3.5 Sonnet for everything.
*   **Embedding**: `all-MiniLM-L6-v2` (Runs locally on CPU).
*   **Simple Classification**: `Llama-3-8b` (Local via Ollama).
*   **Complex Reasoning**: `Claude 3.5 Sonnet`.

**Lesson**: **Tier your intelligence.** Don't use a PhD to organize your socks.

---

## ✅ What Worked: Dependency Tracking

Documentation always drifts. You update code, forget the README. You improve the README, but the user guide goes stale.

**The Fix**: A dependency graph (`dependencies.yaml`) that tracks which files depend on which.

```yaml
# When SKILL.md changes, README must be updated
- path: packages/career-consultant/README.md
  depends_on:
    - packages/career-consultant/SKILL.md
```

**The Workflow**:
1.  CI checks if source files changed without updating dependents.
2.  PRs show warnings.
3.  Releases are blocked if docs are stale.

**Lesson**: **Automate the boring stuff.** If you have to remember to update something, you'll forget.

---

## 🧠 The Philosophy Shift

The biggest lesson wasn't technical. It was mental.

I stopped trying to build "Automation" (replacing me) and started building "Augmentation" (helping me).
*   **Automation**: "Write this blog post for me." (Result: Generic trash)
*   **Augmentation**: "Here is my outline and my tone. Draft the sections." (Result: 10x speed, my voice)

---

## 🔮 Next Week: The Philosophy

We've covered the code, the architecture, and the mistakes.
Next week, in the final article, we'll talk about **Why**. Why local-first? Why now? And where is this "Homosapiens 2.0" thing actually going?

**See you for the finale.** 👇

#Engineering #Failures #LessonsLearned #AI #LocalFirst
