---
name: voice-memos
description: Process voice memos via Apple Notes inbox. Transcribe, extract action items, generate summaries, and organize automatically. Commands - "process voice memos", "transcribe [file]", "analyze memo", "show transcripts".
---

# 🎙️ Voice Memos Automation

Capture → Transcribe → Analyze → Organize

## 🌟 Key Capabilities
1. **Apple Notes Inbox**: Add memo references to "🎙️ Voice Memos Inbox" note
2. **Multi-Language Transcription**: Auto-detect or specify (EN, HE, etc.)
3. **Speaker Identification**: Label up to 10 speakers
4. **Action Item Extraction**: With priorities (HIGH/MEDIUM/LOW)
5. **Smart Summaries**: Brief, standard, or detailed
6. **Auto-Organization**: Categorize, tag, and sync

## ⚙️ Storage Configuration

**User Data Location**: `~/MyDrive/claude-skills-data/voice-memos/`

```
voice-memos/
├── config.yaml           # Local config overrides
├── transcripts/          # Raw transcriptions
│   └── {date}-{slug}.md
├── analyzed/             # Full analysis
│   └── {date}-{slug}.md
└── index.yaml            # Master index
```

## 🚀 Commands

| Command | Action |
|---------|--------|
| `process voice memos` | Process all from Apple Notes inbox |
| `transcribe [file]` | Transcribe single uploaded file |
| `analyze memo` | Analyze last transcription |
| `show pending memos` | List unprocessed memos |
| `show transcripts` | List all transcripts |
| `search memos: [query]` | Find by keyword |

## 📋 Workflow: Process Voice Memos

### Step 1: Read Apple Notes Inbox

```python
def process_voice_inbox():
    """
    Read 🎙️ Voice Memos Inbox note, identify memos to process.
    """
    note_content = get_note_content("🎙️ Voice Memos Inbox")
    
    # Parse - split by processed marker
    if "✅ PROCESSED" in note_content:
        pending_section = note_content.split("✅ PROCESSED")[0]
    else:
        pending_section = note_content
    
    # Extract memo references
    # Format: filename.m4a [optional notes]
    memos = []
    for line in pending_section.split('\n'):
        line = line.strip()
        if not line or line.startswith('━') or line.startswith('📥'):
            continue
        if any(ext in line.lower() for ext in ['.m4a', '.mp3', '.wav', '.aac', '.opus', '.flac']):
            memos.append(parse_memo_reference(line))
    
    return memos
```

### Step 2: Transcribe Audio

```python
def transcribe_memo(audio_file, config):
    """
    Transcribe voice memo with configurable settings.
    
    Supported formats: m4a, mp3, wav, aac, opus, flac
    """
    settings = config.get('transcription', {})
    
    params = {
        'language': settings.get('language', 'auto'),
        'speaker_labels': settings.get('speaker_labels', True),
        'max_speakers': settings.get('max_speakers', 5),
        'timestamps': settings.get('include_timestamps', True),
        'timestamp_granularity': settings.get('timestamp_granularity', 'paragraph')
    }
    
    # Use Claude's native audio transcription
    transcript = transcribe_audio(
        audio_file,
        language=params['language'],
        identify_speakers=params['speaker_labels']
    )
    
    return {
        'raw': transcript,
        'formatted': format_transcript(transcript, params),
        'metadata': {
            'duration': get_audio_duration(audio_file),
            'detected_language': transcript.language,
            'speaker_count': len(transcript.speakers),
            'word_count': len(transcript.text.split())
        }
    }
```

### Step 3: Analyze Content

```python
def analyze_transcript(transcript, config):
    """
    Extract insights from transcript.
    """
    settings = config.get('analysis', {})
    analysis = {}
    
    # Action Items
    if settings.get('extract_action_items', True):
        analysis['action_items'] = extract_action_items(
            transcript,
            include_owners=True,
            include_deadlines=True,
            priority_levels=['HIGH', 'MEDIUM', 'LOW']
        )
    
    # Summary
    if settings.get('generate_summary', True):
        length = settings.get('summary_length', 'standard')
        analysis['summary'] = generate_summary(transcript, length=length)
    
    # Key Points
    analysis['key_points'] = extract_key_points(transcript, max_items=7)
    
    # Entities
    analysis['entities'] = {
        'people': extract_people(transcript),
        'dates': extract_dates(transcript),
        'locations': extract_locations(transcript),
        'organizations': extract_orgs(transcript)
    }
    
    # Categorization
    analysis['category'] = categorize_memo(transcript)
    analysis['tags'] = generate_tags(transcript, max_tags=10)
    
    return analysis
```

### Step 4: Save Results

```python
def save_memo_results(filename, transcript, analysis, user_data_base):
    """
    Save transcript and analysis to filesystem.
    """
    from datetime import datetime
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(filename.replace('.m4a', '').replace('.mp3', ''))
    
    # Save transcript
    transcript_path = f"{user_data_base}/transcripts/{date_str}-{slug}.md"
    transcript_content = f"""# 🎙️ Transcript: {filename}

**Date**: {date_str}
**Duration**: {transcript['metadata']['duration']}
**Language**: {transcript['metadata']['detected_language']}
**Speakers**: {transcript['metadata']['speaker_count']}

---

{transcript['formatted']}
"""
    
    # Save analysis
    analysis_path = f"{user_data_base}/analyzed/{date_str}-{slug}.md"
    # ... format and save analysis
    
    return {'transcript_path': transcript_path, 'analysis_path': analysis_path}
```

## 📊 Output Templates

### Memo Analysis

```markdown
# 🎙️ team-standup-2024-11-24.m4a

**Date**: 2024-11-24
**Category**: meeting
**Tags**: standup, engineering, sprint-planning

## 📝 Summary
Daily standup covering sprint progress. Team discussed blockers 
on the authentication feature.

## 🎯 Key Points
- Sprint velocity on track
- Auth feature blocked by API changes
- New designer starting Monday

## ✅ Action Items
- 🔴 **Fix auth API integration** (@Dan) - Due: Nov 25
- 🟡 **Prepare onboarding for new designer** (@Sarah)
- 🟢 **Update sprint board** (@Gur)

## 👥 People Mentioned
Dan, Sarah, Mike

## 📅 Dates Mentioned
Monday, Nov 25
```

## 🏷️ Categories

| Category | Description |
|----------|-------------|
| meeting | Team meetings, standups, 1:1s |
| journal | Personal thoughts, reflections |
| task-list | Quick task capture |
| brainstorm | Ideas, planning sessions |
| interview | Job interviews, user research |
| lecture | Learning content, courses |
| call | Phone/video calls |
| reminder | Quick reminders |
| other | Uncategorized |

## ⚡ Quick Start

1. **Record** voice memo in Voice Memos app
2. **Add to inbox**: Open "🎙️ Voice Memos Inbox" note, add filename
3. **Process**: Tell Claude `"process voice memos"`
4. **Or direct**: Upload file and say `"transcribe and analyze this"`

## 💡 Tips

- **Batch process**: Add multiple memos, process once weekly
- **Quick capture**: Just drag files into the Apple Note
- **Speaker hints**: Add "Speakers: Gur, Dan" for better labeling
- **Hebrew+English**: Works seamlessly with mixed language

---

**Version**: 1.0.0
**Last Updated**: 2024-11-24
**Patterns**: inbox, transcription, analysis
