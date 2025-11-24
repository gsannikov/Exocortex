# Voice Transcription Skill

**Version**: 1.0.0  
**Created**: 2025-11-03  
**Purpose**: Transcribe audio voice memos into clean, formatted text with timestamps and speaker identification

## Overview

This skill enables Claude to transcribe audio recordings into accurate, well-formatted text transcriptions. It handles multiple languages, identifies speakers, and includes timestamps for easy reference.

## When to Use This Skill

Use this skill when:
- User uploads an audio file (m4a, mp3, wav, aac, opus, flac)
- User asks to "transcribe my voice memo"
- User requests "convert audio to text"
- User mentions "voice recording" or "audio note"

## Capabilities

### Core Features
- **Accurate Transcription**: Convert speech to text with high accuracy
- **Multi-Language Support**: Auto-detect or specify language (English, Hebrew, Spanish, etc.)
- **Speaker Identification**: Distinguish between multiple speakers
- **Timestamp Integration**: Add timestamps at paragraph, sentence, or minute intervals
- **Quality Indicators**: Mark uncertain words for user review

### Output Formats
- Clean markdown with proper formatting
- Organized by speakers (if multiple)
- Timestamped sections for easy navigation
- Metadata header with file information

## Configuration

Load settings from: `~/MyDrive/VoiceMemos/config/settings.json`

Key configuration sections:
```json
{
  "transcription": {
    "include_timestamps": true,
    "timestamp_frequency": "paragraph",
    "language": "auto",
    "speaker_labels": true,
    "confidence_threshold": 0.85
  }
}
```

## Workflow

### Step 1: Receive Audio File
```
User uploads audio file or provides file path
↓
Validate file format and size
↓
Check configuration settings
```

### Step 2: Load Transcription Prompt
```
Read: ~/MyDrive/VoiceMemos/config/prompts/transcription.txt
↓
Apply user's configuration preferences
↓
Prepare transcription context
```

### Step 3: Transcribe Audio
```
Process audio content
↓
Detect language (if auto)
↓
Identify speakers (if enabled)
↓
Add timestamps (per configuration)
↓
Mark low-confidence words
```

### Step 4: Format Output
```
Create markdown document
↓
Add metadata header
↓
Structure by speakers/paragraphs
↓
Include timestamps
↓
Save to: ~/MyDrive/VoiceMemos/transcripts/YYYY-MM-DD/
```

### Step 5: Provide Results
```
Show preview to user
↓
Offer to run analysis skill next
↓
Provide file location
```

## Output Template

```markdown
# {Title or "Voice Memo"}

**Date**: {YYYY-MM-DD}
**Time**: {HH:MM}
**Duration**: {MM:SS}
**Language**: {detected language}
**Speakers**: {number detected}
**File**: {original filename}

## Transcript

[00:00:00] **Speaker 1**: {transcribed content with proper punctuation and formatting...}

[00:00:45] {content continues with natural paragraph breaks...}

[00:01:30] **Speaker 2**: {if multiple speakers detected, label them clearly...}

[00:02:15] {content continues...}

## Notes
- Words marked as [uncertain: word] indicate low confidence
- Timestamps indicate approximate position in audio
- Speaker labels are automatically assigned

---
*Transcription generated on {timestamp}*
*Located at: ~/MyDrive/VoiceMemos/transcripts/{date}/{filename}.md*
```

## Special Handling

### Multi-Language Detection
```
If user_config.language == "auto":
    Detect primary language
    Note if multiple languages present
    Use fallback language if confidence low
```

### Speaker Diarization
```
If user_config.speaker_labels == true:
    Identify distinct speakers
    Label as Speaker 1, Speaker 2, etc.
    Maintain consistency throughout
    Add speaker change indicators
```

### Timestamp Insertion
```
Based on user_config.timestamp_frequency:
    "paragraph": Add timestamp at each paragraph break
    "sentence": Add timestamp at each sentence
    "minute": Add timestamp every 60 seconds
```

### Quality Control
```
For words with confidence < threshold:
    Mark as [uncertain: word]
    Flag for user review
    
For unclear audio sections:
    Mark as [inaudible] or [unclear]
```

## Error Handling

### File Format Issues
```
If file format not supported:
    → List supported formats
    → Suggest conversion tools
    → Offer alternative approaches
```

### Audio Quality Problems
```
If audio quality is poor:
    → Inform user
    → Provide best-effort transcription
    → Suggest audio preprocessing
    → Mark many sections as [uncertain]
```

### Language Detection Failures
```
If cannot detect language:
    → Ask user to specify
    → Use fallback language
    → Proceed with caution
```

## Integration with Other Skills

### Trigger Analysis Skill
After successful transcription:
```
Offer to run voice-analysis skill:
"Transcription complete! Would you like me to analyze this 
and extract action items, key points, and summary?"

If yes → Load voice-analysis skill
If no → Provide file location and end
```

### File Organization
```
Save transcription to:
~/MyDrive/VoiceMemos/transcripts/YYYY-MM-DD/filename.md

Optionally:
- Copy to ~/MyDrive/VoiceMemos/by-topic/ (if topic detected)
- Sync to Apple Notes (if enabled in config)
- Upload to Google Drive (if enabled)
```

## Examples

### Example 1: Simple Voice Note
**Input**: Personal voice memo about project ideas

**Process**:
1. Detect language: English
2. One speaker detected
3. 2-minute duration
4. Paragraph-level timestamps

**Output**:
```markdown
# Project Ideas - Mobile App

**Date**: 2025-11-03
**Time**: 14:30
**Duration**: 02:15
**Language**: English
**Speakers**: 1

## Transcript

[00:00:00] I've been thinking about a mobile app that could help 
people track their daily water intake. The idea is to make it 
really simple - just tap a button every time you drink a glass 
of water. The app could send reminders and show progress toward 
your daily goal.

[00:00:45] The key features would be: simple one-tap logging, 
customizable goals based on body weight and activity level, 
gentle reminders throughout the day, and maybe some kind of 
achievement system to keep people motivated.

[00:01:30] I should research existing apps to see what's already 
out there and what gaps exist. Also need to think about the 
business model - freemium with premium features, or one-time 
purchase?

---
*Transcription generated on 2025-11-03 14:35*
```

### Example 2: Team Meeting (Multiple Speakers)
**Input**: 10-minute team meeting recording

**Process**:
1. Detect language: English
2. Three speakers identified
3. Minute-level timestamps
4. Include speaker changes

**Output Preview**:
```markdown
# Weekly Team Sync

**Date**: 2025-11-03
**Time**: 10:00
**Duration**: 10:45
**Language**: English
**Speakers**: 3

## Transcript

[00:00:00] **Speaker 1**: Good morning everyone. Let's start with 
project updates. Sarah, can you give us the status on the API 
integration?

[00:00:15] **Speaker 2**: Sure. The API integration is about 80% 
complete. We finished the authentication layer and most of the 
core endpoints. Still working on error handling and rate limiting.

[00:01:00] **Speaker 1**: Great progress. Any blockers?

[00:01:05] **Speaker 2**: We need the final API documentation from 
the partner team. They promised it by Wednesday.

[00:01:15] **Speaker 3**: I can follow up with them today to make 
sure we get it on time...
```

### Example 3: Hebrew Language Voice Memo
**Input**: Hebrew voice memo about family event

**Process**:
1. Auto-detect: Hebrew
2. One speaker
3. Paragraph timestamps

**Output Preview**:
```markdown
# תזכורת לאירוע משפחתי

**Date**: 2025-11-03
**Time**: 16:20
**Duration**: 01:30
**Language**: Hebrew
**Speakers**: 1

## Transcript

[00:00:00] צריך לזכור לקנות מתנה ליום ההולדת של אמא בשבוע הבא. 
היא אמרה שהיא רוצה ספר חדש או אולי כרטיס למופע תיאטרון...
```

## User Interaction Patterns

### Pattern 1: Direct Upload
```
User: "Transcribe this audio file"
[uploads file]

Claude: 
1. Load this skill
2. Process file
3. Show preview
4. Offer analysis
```

### Pattern 2: Batch Processing
```
User: "Transcribe all audio files in this folder"

Claude:
1. List files found
2. Confirm with user
3. Process each file
4. Save all transcriptions
5. Provide summary
```

### Pattern 3: Custom Settings
```
User: "Transcribe this but include timestamps every 30 seconds"

Claude:
1. Acknowledge custom request
2. Override default config for this session
3. Process with custom settings
4. Note the custom setting in output
```

## Performance Considerations

### Processing Time
- Typical: Real-time to 2x speed (10 min audio → 5-10 min processing)
- Complex audio (multiple speakers, poor quality): Up to 3x speed

### File Size Limits
- Maximum: 100MB per file (configurable)
- Recommended: Under 50MB for best performance

### Concurrent Processing
- Default: Process one at a time
- Can enable parallel processing in config for batch jobs

## Quality Assurance

### Confidence Scoring
- High confidence (>0.90): Clean transcription
- Medium confidence (0.75-0.90): Generally reliable
- Low confidence (<0.75): Mark as [uncertain]

### User Review Points
Always flag for review:
- Technical terms
- Proper names
- Numbers and dates
- Low-confidence sections

## Next Steps After Transcription

### Automatic
- Save file to organized location
- Update metadata index
- Log processing in history

### Suggested
1. Run voice-analysis skill for insights
2. Export to preferred format (docx, pdf)
3. Share via enabled integrations
4. Archive original audio

## Configuration Reference

### Essential Settings
```json
{
  "transcription": {
    "enabled": true,
    "language": "auto",
    "include_timestamps": true
  }
}
```

### Advanced Settings
```json
{
  "transcription": {
    "timestamp_frequency": "paragraph",
    "speaker_labels": true,
    "max_speakers": 5,
    "confidence_threshold": 0.85,
    "filter_filler_words": false,
    "custom_vocabulary": []
  }
}
```

## Troubleshooting

### Low Accuracy
**Symptoms**: Many [uncertain] markers, gibberish text
**Solutions**:
- Check audio quality
- Specify language manually
- Add custom vocabulary
- Reduce confidence threshold

### Missing Speakers
**Symptoms**: Multiple speakers not distinguished
**Solutions**:
- Enable speaker_labels in config
- Increase max_speakers
- Ensure audio has clear speaker separation

### Wrong Language Detected
**Symptoms**: Transcription in unexpected language
**Solutions**:
- Specify language in config
- Check audio content
- Use fallback_language setting

## File Locations

### Input
- Audio files: Any accessible location
- Config: `~/MyDrive/VoiceMemos/config/settings.json`
- Prompt: `~/MyDrive/VoiceMemos/config/prompts/transcription.txt`

### Output
- Transcriptions: `~/MyDrive/VoiceMemos/transcripts/YYYY-MM-DD/`
- Logs: `~/MyDrive/VoiceMemos/logs/` (if enabled)

## Success Metrics

- **Accuracy**: >90% word accuracy for clear audio
- **Speed**: Real-time to 2x playback speed
- **User Satisfaction**: Clear, usable transcriptions
- **Format Quality**: Properly structured markdown

---

**Skill Status**: Production Ready  
**Dependencies**: Audio processing capabilities, file system access  
**Related Skills**: voice-analysis (follow-up skill)  
**Support**: See CONFIG-GUIDE.md for detailed configuration help
