# Voice Memos Automation - Quick Start Guide

**Goal**: Process your first voice memo in 5 minutes  
**Prerequisites**: Configuration files from Step 3

## Setup (One-Time - 2 minutes)

### Step 1: Create Directory Structure
```bash
mkdir -p ~/MyDrive/VoiceMemos/{config/prompts,transcripts,processed,raw}
```

### Step 2: Copy Configuration Files
```bash
cp ~/voice-memos-config/settings.json ~/MyDrive/VoiceMemos/config/
cp ~/voice-memos-config/prompts/* ~/MyDrive/VoiceMemos/config/prompts/
```

✅ **Setup Complete!**

---

## Your First Voice Memo

### Example: Team Meeting Update (2 minutes)

**You say to Claude:**
> "I have a voice memo from today's team meeting. Can you transcribe and analyze it?"  
> [Attach: team-meeting.m4a]

### What Happens:

**1. Transcription** (30 seconds)
```markdown
# Team Meeting - 2025-11-03

**Duration**: 02:15 | **Language**: English | **Speakers**: 1

[00:00:00] Quick update from standup. We discussed Q4 roadmap 
and agreed to prioritize feature X. Sarah will lead development, 
timeline is 6 weeks. Need budget approval from John by Friday.

[00:01:00] Mike mentioned QA can start parallel testing in week 3. 
I should schedule a kickoff meeting for next Monday.

---
*Saved to: ~/MyDrive/VoiceMemos/transcripts/2025-11-03/team-meeting.md*
```

**2. Claude Offers:**
> "Would you like me to analyze this and extract action items?"

**3. Analysis** (20 seconds)
```markdown
## Action Items

### HIGH Priority
- [ ] Get budget approval from John — Due: Friday, Nov 8
- [ ] Draft technical spec — Due: Wednesday, Nov 6

### MEDIUM Priority  
- [ ] Schedule kickoff meeting — Due: Monday, Nov 4

## Key Points
- Feature X prioritized for Q4
- Sarah leads (6-week timeline)
- QA starts week 3

**Categories**: meeting, work, planning  
**Tags**: #q4 #feature-x #team-meeting
```

✅ **Done in 3 minutes!**

---

## Common Workflows

### 1. Daily Journal
```
Upload → Transcribe → Skip action items → Get summary & sentiment
Result: Organized journal entry
```

### 2. Meeting Notes  
```
Upload → Transcribe with speakers → Extract decisions & action items
Option: Sync to Apple Notes & Calendar
```

### 3. Quick Task List
```
Upload 1-min recording → Auto-detects tasks → Prioritized checklist
```

---

## Customization

### More Timestamps
Edit `~/MyDrive/VoiceMemos/config/settings.json`:
```json
{"transcription": {"timestamp_frequency": "sentence"}}
```

### Detailed Summaries
```json
{"analysis": {"summary_length": "detailed"}}
```

### Custom Keywords
```json
{"analysis": {"action_item_keywords": ["todo", "task", "my-phrase"]}}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Inaccurate transcription | Specify language manually, add custom vocabulary |
| Missing action items | Add your phrases to config, use explicit keywords |
| Wrong categories | Customize category list in settings |

---

## Enable Integrations

### Apple Notes
```json
{"integrations": {"apple_notes": {"enabled": true}}}
```

### Calendar
```json
{"integrations": {"calendar": {"enabled": true, "auto_create_events": false}}}
```

---

**Time to First Result**: 3 minutes  
**Setup**: 2 minutes (one-time)

🎉 **You're ready to process voice memos!**
