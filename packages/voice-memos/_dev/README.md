# 🎙️ Voice Memos Automation

Process, transcribe, and analyze voice memos and audio notes.

## Quick Start

1. Record in **Voice Memos** app
2. Add filename to **🎙️ Voice Memos Inbox** note
3. Tell Claude: `"process voice memos"`
4. Or upload directly: `"transcribe and analyze this"`

## Commands

| Command | Action |
|---------|--------|
| `process voice memos` | Process inbox |
| `transcribe [file]` | Transcribe uploaded file |
| `analyze memo` | Analyze last transcript |
| `show pending memos` | List unprocessed |
| `show transcripts` | List all transcripts |
| `search memos: [query]` | Find by keyword |

## Features

- **Multi-Language**: Auto-detect EN, HE, and more
- **Speaker Labels**: Identify up to 10 speakers
- **Action Items**: Extract with priorities (HIGH/MEDIUM/LOW)
- **Smart Summaries**: Brief, standard, or detailed
- **Auto-Categorization**: Meeting, journal, brainstorm, interview, etc.

## Supported Formats

m4a, mp3, wav, aac, opus, flac

## Storage

User data: `~/exocortex-data/voice-memos/`

## Version

See `version.yaml`

---

Part of [Exocortex](../../README.md)
