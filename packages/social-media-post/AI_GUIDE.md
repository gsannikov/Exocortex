# AI Guide: Social Media Post Generator

Quick reference for Claude when using this skill.

## When to Invoke

Auto-invoke when user mentions:
- "Create/Write/Generate a [platform] post"
- "Social media post for [topic]"
- "Threads/X/Twitter/LinkedIn announcement"
- "Option 5 style" (short & punchy format)

## Key Decisions

1. **Platform Selection**: Default to multi-platform unless user specifies
2. **Post Length**: Start with medium (300-500 chars) unless requested otherwise
3. **Tone**: Match technical-casual for developer content, professional for business
4. **Hashtags**: None for Threads, 1-2 for X, 3-5 for LinkedIn

## Quick Reference

### Character Limits
- Threads: 500 (standard) / 10,000 (with attachment)
- X: 280 (standard) / 25,000 (Blue)
- LinkedIn: 3,000 (shows "see more" after 140)

### Algorithm Priorities (2025)

**Threads**: Engagement (40%) > Recency (30%) > Relevance (20%) > Profile (10%)
**X**: Engagement rate > Recency > Media > Authenticity
**LinkedIn**: Dwell time > Engagement > Relevance > Connections

## Output Format

Always include:
1. Platform name
2. Post content
3. Character count / limit
4. Engagement hooks used
5. Suggested media
6. Best posting time
