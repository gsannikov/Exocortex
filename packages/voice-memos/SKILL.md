---
name: voice-memos
description: Process voice memos with AI transcription and analysis. Multi-language support (EN, HE), speaker identification, action item extraction with priorities, smart summaries, and auto-categorization (meeting, journal, brainstorm, interview). Triggers - "process voice memos", "transcribe", "analyze memo", "show transcripts", "voice inbox", "extract action items", "meeting notes", "transcribe audio".
---

# Voice Memos Automation

## Overview

Process, transcribe, and analyze voice memos and audio notes.

## Storage

Path: `~/exocortex-data/voice-memos/`

```
voice-memos/
├── index.yaml        # Master index
├── transcripts/      # Raw transcriptions
├── analyzed/         # Full analysis
└── config.yaml       # Preferences
```

## Commands

| Command | Action |
|---------|--------|
| `process voice memos` | Process inbox |
| `transcribe [file]` | Transcribe uploaded file |
| `analyze memo` | Analyze last transcript |
| `show pending memos` | List unprocessed |
| `show transcripts` | List all transcripts |
| `search memos: [query]` | Find by keyword |

## Categories

| Category | Use For |
|----------|---------|
| meeting | Standups, 1:1s, team meetings |
| journal | Personal thoughts |
| brainstorm | Ideas, planning |
| interview | Job/user interviews |
| call | Phone/video calls |
| reminder | Quick reminders |

## Analysis Output

For each memo, extracts:
- **Summary**: 50-300 words
- **Action Items**: With owner, deadline, priority (HIGH/MEDIUM/LOW)
- **Key Points**: Up to 7 takeaways
- **Entities**: People, dates, locations, organizations
- **Tags**: Auto-generated keywords

## Workflow

1. Read "Voice Memos Inbox" from Apple Notes
2. Identify audio files (m4a, mp3, wav, etc.)
3. Transcribe with speaker identification
4. AI analyze: summary, actions, entities
5. Save to `transcripts/` and `analyzed/`
6. Update `index.yaml`

For detailed implementation, see `references/workflow.md`.

## Quick Start

1. Record in Voice Memos app
2. Add filename to "Voice Memos Inbox" note
3. Say: `"process voice memos"`
4. Or upload directly: `"transcribe and analyze this"`
