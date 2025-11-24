# Voice Memos Automation - Configuration Guide

**Version**: 0.1.0  
**Last Updated**: 2025-11-03

## Overview

This guide explains how to configure Voice Memos Automation to match your workflow and preferences.

## Configuration Files

### 1. `settings.json` - Main Configuration
The primary configuration file controlling all aspects of voice memo processing.

**Location**: `~/MyDrive/VoiceMemos/config/settings.json`

### 2. Prompt Templates
Located in `prompts/` directory:
- `transcription.txt` - Controls how audio is transcribed
- `analysis.txt` - Controls how content is analyzed
- `meeting-notes.txt` - Template for meeting notes format
- `journal-entry.txt` - Template for journal entries

## Quick Start Configuration

### Minimal Setup (Phase 1 - MVP)
```json
{
  "transcription": {
    "enabled": true,
    "language": "auto"
  },
  "analysis": {
    "extract_action_items": true,
    "generate_summary": true
  },
  "organization": {
    "filing_structure": "date"
  }
}
```

### Recommended Setup (Phase 2)
Enable integrations and advanced features:
```json
{
  "integrations": {
    "apple_notes": {
      "enabled": true,
      "notebook": "Voice Memos"
    },
    "calendar": {
      "enabled": true,
      "auto_create_events": false
    }
  }
}
```

## Configuration Sections

### User Settings
```json
"user": {
  "name": "Your Name",
  "timezone": "Asia/Jerusalem",
  "language_preferences": ["en", "he"],
  "email": "your@email.com"
}
```

**Customize**:
- `name`: Your full name (used in output headers)
- `timezone`: Your timezone (IANA format)
- `language_preferences`: Languages you speak (prioritized order)

### Transcription Settings
```json
"transcription": {
  "include_timestamps": true,
  "timestamp_frequency": "paragraph",
  "language": "auto",
  "speaker_labels": true
}
```

**Key Options**:
- `timestamp_frequency`: "paragraph" | "sentence" | "minute"
- `language`: "auto" | "en" | "he" | specific language code
- `speaker_labels`: true/false - Identify different speakers

### Analysis Settings
```json
"analysis": {
  "extract_action_items": true,
  "generate_summary": true,
  "summary_length": "standard"
}
```

**Summary Levels**:
- `"brief"`: 3 sentences max (TL;DR)
- `"standard"`: 5-10 sentences (recommended)
- `"detailed"`: 15-20 sentences (comprehensive)

**Action Item Detection**:
Customize keywords that trigger action item extraction:
```json
"action_item_keywords": [
  "todo", "task", "need to", "must", "should",
  "follow up", "schedule", "call", "email"
]
```

**Priority Keywords**:
```json
"priority_keywords": {
  "high": ["urgent", "asap", "critical", "immediately"],
  "medium": ["soon", "this week"],
  "low": ["eventually", "someday", "maybe"]
}
```

### Organization Settings
```json
"organization": {
  "filing_structure": "date",
  "auto_tags": true,
  "max_tags": 10,
  "archive_after_days": 365
}
```

**Filing Options**:
- `"date"`: Organize by YYYY-MM-DD
- `"topic"`: Organize by detected topic
- `"project"`: Organize by project name
- `"custom"`: Use custom logic

**Naming Convention**:
```json
"naming_convention": "{date}_{time}_{title}"
```
Variables: `{date}`, `{time}`, `{title}`, `{category}`

### Integration Settings

#### Apple Notes
```json
"apple_notes": {
  "enabled": false,
  "notebook": "Voice Memos",
  "create_notes": true,
  "include_action_items": true,
  "sync_mode": "manual"
}
```

**Setup**:
1. Set `enabled: true`
2. Specify `notebook` name (will create if doesn't exist)
3. Choose `sync_mode`: "manual" | "automatic"

#### Calendar
```json
"calendar": {
  "enabled": false,
  "auto_create_events": false,
  "default_duration_minutes": 30,
  "require_confirmation": true
}
```

**Event Detection**:
System looks for phrases like:
- "meeting on Friday"
- "call at 3pm"
- "schedule for next week"

**Safety**: Set `require_confirmation: true` to approve before creating events

#### Notion
```json
"notion": {
  "enabled": false,
  "database_id": "your-database-id",
  "auto_sync": false
}
```

**Setup**:
1. Create a Notion database
2. Copy database ID from URL
3. Set `enabled: true`

### Output Settings
```json
"output": {
  "default_format": "markdown",
  "formats": ["markdown", "docx"],
  "templates": {
    "default": "basic-transcript",
    "meeting": "meeting-notes",
    "journal": "journal-entry"
  }
}
```

**Available Formats**:
- `markdown`: Clean, readable markdown
- `docx`: Microsoft Word document
- `txt`: Plain text
- `json`: Structured data

## Common Customizations

### For Meetings
```json
{
  "analysis": {
    "extract_action_items": true,
    "detect_decisions": true,
    "identify_entities": true
  },
  "integrations": {
    "apple_notes": {
      "enabled": true,
      "note_format": "meeting_notes"
    },
    "calendar": {
      "enabled": true,
      "auto_create_events": false
    }
  },
  "output": {
    "templates": {
      "default": "meeting-notes"
    }
  }
}
```

### For Personal Journaling
```json
{
  "analysis": {
    "sentiment_analysis": true,
    "extract_action_items": false,
    "generate_summary": true,
    "summary_length": "detailed"
  },
  "organization": {
    "filing_structure": "date",
    "auto_categorize": true,
    "categories": ["personal", "journal", "reflection"]
  },
  "output": {
    "templates": {
      "default": "journal-entry"
    }
  }
}
```

### For Task Capture
```json
{
  "analysis": {
    "extract_action_items": true,
    "priority_scoring": true,
    "extract_key_points": true
  },
  "integrations": {
    "apple_notes": {
      "enabled": true,
      "create_notes": true,
      "include_action_items": true
    }
  },
  "organization": {
    "priority_queue": true
  }
}
```

### Multi-Language Support
```json
{
  "user": {
    "language_preferences": ["en", "he"]
  },
  "transcription": {
    "language": "auto",
    "fallback_language": "en"
  }
}
```

## Privacy & Security

### Enable PII Detection
```json
"privacy": {
  "pii_detection": true,
  "pii_redaction": true,
  "sensitive_keywords": [
    "password", "credit card", "social security",
    "confidential", "secret"
  ]
}
```

### Audio Retention
```json
"audio": {
  "retention": {
    "keep_original_audio": true,
    "compress_old_files": true,
    "compression_age_days": 90
  }
}
```

## Performance Tuning

### For Faster Processing
```json
"performance": {
  "max_concurrent_processing": 3,
  "cache_transcriptions": true,
  "batch_processing": {
    "enabled": true,
    "parallel_processing": true
  }
}
```

### For Large Files
```json
"audio": {
  "max_file_size_mb": 200,
  "max_duration_minutes": 180,
  "preprocessing": {
    "noise_reduction": true,
    "trim_silence": true
  }
}
```

## Troubleshooting

### Problem: Transcription is inaccurate
**Solution**:
1. Check audio quality
2. Increase confidence threshold:
```json
"transcription": {
  "confidence_threshold": 0.90
}
```
3. Add custom vocabulary:
```json
"transcription": {
  "custom_vocabulary": ["specialized", "term", "names"]
}
```

### Problem: Missing action items
**Solution**:
Add your specific action phrases:
```json
"analysis": {
  "action_item_keywords": [
    "todo", "task", "I need to", "remember to"
  ]
}
```

### Problem: Wrong categories
**Solution**:
Customize category list:
```json
"analysis": {
  "categories": [
    "your-category-1",
    "your-category-2"
  ]
}
```

## Validation

Use the provided validation script to check your configuration:
```bash
python validate_config.py settings.json
```

## Backup

Always backup your configuration:
```bash
cp settings.json settings.backup.json
```

## Migration

When upgrading versions, check:
1. New configuration options
2. Deprecated settings
3. Breaking changes in CHANGELOG.md

## Support

- Documentation: `/docs/`
- Examples: `/examples/`
- Issues: File in project tracker

---

**Next Steps**:
1. Copy default settings to your config directory
2. Customize for your use case
3. Test with a sample voice memo
4. Iterate and refine

**Version History**:
- 0.1.0 (2025-11-03): Initial configuration system
