# Meeting Transcription Skill

## Overview
Process meeting recordings captured by the Meeting Recorder app. This skill extends the voice-memos transcription with meeting-specific analysis.

## Trigger Commands
- `process meeting recordings` - Process all pending meeting recordings
- `transcribe meeting [file]` - Transcribe a specific meeting file
- `summarize last meeting` - Summarize the most recent meeting

## Data Locations
```
Input:  ~/MyDrive/claude-skills-data/voice-memos/meetings/
Output: ~/MyDrive/claude-skills-data/voice-memos/meetings/transcripts/
Index:  ~/MyDrive/claude-skills-data/voice-memos/meetings/index.yaml
```

## Processing Pipeline

### Step 1: Discover Meeting Recordings
```yaml
scan_directory: ~/MyDrive/claude-skills-data/voice-memos/meetings/
file_patterns:
  - "*.m4a"
  - "*.mp3"
  - "*.wav"
exclude:
  - transcripts/
  - ".*"  # Hidden files
```

### Step 2: Handle Chunked Recordings
Meetings over 40 minutes are auto-chunked. Identify and group chunks:
```
Pattern: {timestamp}_{app}_chunk{N}.m4a
Example: 2024-01-15_14-30_zoom_chunk0.m4a
         2024-01-15_14-30_zoom_chunk1.m4a
         2024-01-15_14-30_zoom_chunk2.m4a

Group by base name (before _chunk) for unified processing.
```

### Step 3: Transcribe Audio
Use Claude's native audio processing with meeting-optimized settings:
```yaml
transcription_settings:
  speaker_labels: true
  max_speakers: 10          # Meetings often have many participants
  include_timestamps: true
  timestamp_frequency: paragraph
  language: auto
  confidence_threshold: 0.85
```

For chunked recordings:
1. Transcribe each chunk sequentially
2. Maintain speaker label consistency across chunks
3. Merge transcripts with proper timestamp offsets

### Step 4: Meeting-Specific Analysis
Extract meeting-specific insights:

```yaml
meeting_analysis:
  # Action Items with ownership
  action_items:
    extract: true
    include_owner: true      # "John will send the report"
    include_deadline: true   # "by Friday"
    priority_levels: true

  # Decisions Made
  decisions:
    extract: true
    include_context: true    # Why was this decided

  # Questions Raised
  questions:
    extract_unanswered: true
    extract_parking_lot: true

  # Attendee Summary
  attendees:
    identify_speakers: true
    speaking_time: true      # Rough percentage

  # Topic Segmentation
  topics:
    segment_by_topic: true
    generate_outline: true

  # Follow-ups
  follow_ups:
    extract: true
    link_to_owner: true
```

### Step 5: Generate Meeting Summary
Create structured meeting summary:

```markdown
# Meeting: {title or "Untitled Meeting"}

**Date**: {YYYY-MM-DD}
**Time**: {HH:MM} - {HH:MM}
**Duration**: {duration}
**Platform**: {Zoom/Meet/Teams}
**Recording**: {filename}

## Attendees
- Speaker 1 (primary speaker, ~40% of conversation)
- Speaker 2 (~35%)
- Speaker 3 (~25%)

## Executive Summary
{2-3 sentence high-level summary}

## Topics Discussed
1. **{Topic 1}** [00:00 - 15:30]
   - Key point A
   - Key point B

2. **{Topic 2}** [15:30 - 32:00]
   - Key point A
   - Decision: {decision made}

## Action Items
| Item | Owner | Deadline | Priority |
|------|-------|----------|----------|
| {task} | Speaker 1 | 2024-01-20 | HIGH |
| {task} | Speaker 2 | Next week | MEDIUM |

## Decisions Made
1. **{Decision}**: {context and rationale}
2. **{Decision}**: {context}

## Open Questions / Parking Lot
- [ ] {Question that wasn't resolved}
- [ ] {Item deferred to future discussion}

## Key Quotes
> "{Important verbatim quote}" - Speaker 1

## Full Transcript
[Link to full transcript or expand below]

<details>
<summary>Click to expand full transcript</summary>

{full transcript with timestamps and speaker labels}

</details>
```

### Step 6: Save and Index
```yaml
output_files:
  summary: "{date}_{time}_{app}-summary.md"
  transcript: "{date}_{time}_{app}-transcript.md"

index_entry:
  id: "{uuid}"
  date: "{date}"
  time: "{time}"
  duration: "{duration}"
  platform: "{app}"
  attendees_count: {N}
  action_items_count: {N}
  decisions_count: {N}
  topics: ["{topic1}", "{topic2}"]
  tags: ["meeting", "{app}", "{auto-tags}"]
  files:
    audio: "{audio_path}"
    summary: "{summary_path}"
    transcript: "{transcript_path}"
```

## Integration Options

### Calendar Integration
If calendar access is available:
- Match recording to calendar event
- Pull attendee names from invite
- Use meeting title from event

### Task Manager Integration
Export action items to:
- Apple Reminders
- Todoist
- Notion
- Linear

## Quality Guidelines

### Transcript Quality
- Mark uncertain words as `[uncertain: word]`
- Mark inaudible sections as `[inaudible, ~5 sec]`
- Preserve filler words in transcript but exclude from summary
- Note overlapping speech as `[crosstalk]`

### Speaker Identification
- Maintain consistent labels (Speaker 1, Speaker 2, etc.)
- Note voice characteristics for future meetings
- If names are mentioned, create mapping: "Speaker 1 appears to be 'John'"

### Time Accuracy
- Timestamps should be within ±5 seconds
- Use relative timestamps for chunks (continue from previous)

## Example Workflow

```
User: process meeting recordings

Claude:
1. Scanning ~/MyDrive/claude-skills-data/voice-memos/meetings/
2. Found 1 new recording:
   - 2024-01-15_14-30-00_zoom.m4a (45 min, 2 chunks)

3. Processing: 2024-01-15_14-30-00_zoom
   - Transcribing chunk 1/2... done
   - Transcribing chunk 2/2... done
   - Merging transcripts... done
   - Analyzing content...
   - Generating summary...

4. Results:
   Meeting: Project Kickoff
   Duration: 45 minutes
   Speakers: 4 identified
   Action Items: 7 extracted
   Decisions: 3 recorded

   Summary saved to: meetings/transcripts/2024-01-15_14-30_zoom-summary.md

   Key Action Items:
   • [HIGH] John to share project timeline by Friday
   • [MEDIUM] Sarah to schedule follow-up with design team
   • [LOW] All to review shared documents

   Would you like me to:
   - Open the full transcript?
   - Export action items to your task manager?
   - Add follow-up reminders to calendar?
```

## Error Handling

| Error | Action |
|-------|--------|
| Audio quality poor | Note in transcript, attempt enhancement |
| File too large | Auto-chunk and process sequentially |
| Permission denied | Prompt user to grant file access |
| Unsupported format | List supported formats, suggest conversion |
| Speaker confusion | Mark ambiguous sections, ask user to clarify |

## Performance Targets

| Metric | Target |
|--------|--------|
| Transcription speed | < 0.5x audio duration |
| Summary generation | < 30 seconds |
| Action item precision | > 90% |
| Speaker diarization accuracy | > 85% |
