# Troubleshooting Guide

**Purpose**: Solutions to common issues and error messages

---

## Voice Memos Issues

### Transcription Problems

#### Issue: "Transcription failed - unsupported format"

**Symptoms:**
- Error message when uploading audio
- File rejected

**Causes:**
- File format not supported
- File corrupted
- File too large

**Solutions:**
```
1. Check file format:
   Supported: m4a, mp3, wav, aac, opus, flac
   
2. Convert if needed:
   Use: CloudConvert, FFmpeg, or macOS/iOS export
   
3. Check file size:
   Max: 100MB (default, configurable)
   Solution: Compress audio or split file
   
4. Verify file integrity:
   Try playing file first to ensure it's not corrupted
```

---

#### Issue: Inaccurate transcription / Wrong words

**Symptoms:**
- Many incorrect words
- Gibberish in transcript
- Names spelled wrong

**Causes:**
- Poor audio quality
- Background noise
- Accent/dialect not recognized
- Technical terms unknown
- Wrong language detected

**Solutions:**
```
1. Audio Quality:
   ✓ Re-record in quiet environment
   ✓ Use better microphone
   ✓ Speak clearly, not too fast
   
2. Language Specification:
   Edit settings.json:
   {"transcription": {"language": "en"}}  // Instead of "auto"
   
3. Custom Vocabulary:
   Add specialized terms:
   {"transcription": {
     "custom_vocabulary": [
       "Kubernetes", "OAuth", "Sannikov", "Tel Aviv"
     ]
   }}
   
4. Confidence Threshold:
   Lower for difficult audio:
   {"transcription": {"confidence_threshold": 0.75}}  // Default: 0.85
```

**Example Fix:**
```json
{
  "transcription": {
    "language": "en",
    "confidence_threshold": 0.80,
    "custom_vocabulary": [
      "Firecrawl", "NotebookLM", "Anthropic", 
      "Hadera", "Israeli", "Calcalist"
    ]
  }
}
```

---

#### Issue: Speaker labels missing or wrong

**Symptoms:**
- All text attributed to "Speaker 1"
- Speakers not distinguished
- Wrong speaker labels

**Causes:**
- speaker_labels disabled
- Similar voices
- Overlapping speech
- max_speakers too low

**Solutions:**
```
1. Enable speaker labeling:
   {"transcription": {"speaker_labels": true}}
   
2. Increase max speakers:
   {"transcription": {"max_speakers": 10}}  // Default: 5
   
3. Recording tips:
   - Have speakers introduce themselves
   - Minimize cross-talk
   - Use separate mics if possible
   
4. Manual correction:
   - Review transcript
   - Correct speaker labels
   - Add to feedback
```

---

### Analysis Problems

#### Issue: No action items extracted

**Symptoms:**
- Empty action items section
- Obvious tasks not identified

**Causes:**
- Keywords not matched
- Vague language used
- Action items not explicit

**Solutions:**
```
1. Add your phrases to config:
   {"analysis": {
     "action_item_keywords": [
       "todo", "task", "need to", "remember",
       "I'll", "we should", "let's"  // Add your patterns
     ]
   }}
   
2. Be explicit when recording:
   Say: "Action item: Call John by Friday"
   Not: "Should probably reach out to John"
   
3. Review and flag:
   Tell Claude: "This is an action item: [quote text]"
```

---

#### Issue: Wrong priority assigned

**Symptoms:**
- Urgent items marked LOW
- Non-urgent marked HIGH

**Causes:**
- Priority keywords not recognized
- Deadline ambiguous

**Solutions:**
```
1. Customize priority keywords:
   {"analysis": {
     "priority_keywords": {
       "high": ["urgent", "asap", "critical", "today", "immediately"],
       "medium": ["this week", "soon", "important"],
       "low": ["eventually", "someday", "when possible"]
     }
   }}
   
2. Be explicit with deadlines:
   Say: "This needs to be done by Friday" (specific)
   Not: "This should happen soon" (vague)
   
3. Manual override:
   Tell Claude: "Change item 3 to HIGH priority"
```

---

#### Issue: Wrong category assigned

**Symptoms:**
- Meeting tagged as "journal"
- Work tagged as "personal"

**Causes:**
- Auto-categorization rules don't fit
- Content ambiguous

**Solutions:**
```
1. Customize categories:
   {"analysis": {
     "categories": [
       "team-meeting", "1on1", "standup",  // More specific
       "work-task", "personal-task",
       "idea", "reflection"
     ]
   }}
   
2. Provide context:
   Start recording: "This is a team meeting about..."
   
3. Manual correction:
   "This should be categorized as 'work', not 'personal'"
```

---

## Reading List Issues

### Scraping Problems

#### Issue: "Failed to capture article"

**Symptoms:**
- Error message
- No content extracted
- "Content length too short"

**Causes:**
- Firecrawl blocked/failed
- Paywall encountered
- JavaScript-heavy site
- Invalid URL

**Solutions:**
```
1. Check URL validity:
   - Include https://
   - Remove tracking parameters
   - Verify URL loads in browser
   
2. Enable Bright Data fallback:
   {"capture": {
     "default_scraper": "firecrawl",
     "fallback_scraper": "bright_data"  // Handles complex sites
   }}
   
3. For paywalled content:
   Option A: Subscribe to source
   Option B: Enable Bright Data
   Option C: Copy/paste content manually
   
4. Retry:
   "Try capturing this URL again using Bright Data"
```

---

#### Issue: Gibberish / Broken content

**Symptoms:**
- Extracted text is garbled
- Random characters
- Missing paragraphs

**Causes:**
- Encoding issues
- Site structure unusual
- Content dynamically loaded

**Solutions:**
```
1. Try fallback scraper:
   "Use Bright Data for this URL"
   
2. Check source:
   View page in browser - does it load properly?
   
3. Manual extraction:
   Copy/paste article content:
   "Here's the article text: [paste]"
   
4. Report issue:
   Note the domain for future configuration
```

---

#### Issue: Missing key information

**Symptoms:**
- No author extracted
- No publish date
- Incomplete metadata

**Causes:**
- Metadata not standard format
- Source doesn't provide info
- Extraction rules didn't match

**Solutions:**
```
1. Not critical - content is most important
   
2. Manual addition:
   "Add metadata: Author: John Smith, Published: Nov 1, 2025"
   
3. Configure trusted sources:
   Add to sources.json with expected metadata format
```

---

### Analysis Problems

#### Issue: Poor summary quality

**Symptoms:**
- Summary misses key points
- Too generic
- Doesn't capture nuance

**Causes:**
- Article too long/complex
- Summary level too brief
- Content very technical

**Solutions:**
```
1. Request detailed summary:
   "Provide a detailed summary instead of brief"
   
2. Adjust config:
   {"analysis": {
     "summary_levels": ["brief", "standard", "detailed"],
     "summary_configs": {
       "detailed": {"enabled": true}
     }
   }}
   
3. For complex content:
   "Export to NotebookLM for detailed analysis"
```

---

#### Issue: Wrong topics assigned

**Symptoms:**
- AI article tagged as "business"
- Tech article missed "israeli-tech"

**Causes:**
- Topic taxonomy doesn't match
- Classification confidence low

**Solutions:**
```
1. Customize taxonomy:
   Edit sources.json:
   {"topic_taxonomy": {
     "ai-ml": ["artificial intelligence", "machine learning", "LLM", "GPT"],
     "israeli-tech": ["israel", "tel aviv", "israeli startup", "jerusalem"]
   }}
   
2. Adjust confidence threshold:
   {"organization": {
     "classification_confidence_threshold": 0.6  // Lower = more inclusive
   }}
   
3. Manual correction:
   "This article should be tagged 'ai-ml' not 'business'"
```

---

#### Issue: Low priority score for relevant article

**Symptoms:**
- Important article marked LOW
- Relevance score seems wrong

**Causes:**
- User interests not configured
- Older article (recency penalty)
- Source not in preferred list

**Solutions:**
```
1. Update user interests:
   Edit settings.json:
   {"user": {
     "interests": ["ai", "israeli-tech", "management", "career"]
   }}
   
2. Adjust scoring weights:
   {"organization": {
     "priority_scoring": {
       "factors": {
         "relevance": 0.5,      // Increase importance
         "recency": 0.1,        // Decrease recency weight
         "source_authority": 0.2
       }
     }
   }}
   
3. Manual override:
   "Mark this as HIGH priority"
```

---

### Research Report Problems

#### Issue: Insufficient sources for report

**Symptoms:**
- "Need at least 5 articles"
- Report too shallow

**Causes:**
- Not enough articles in collection
- Articles too diverse (no themes)

**Solutions:**
```
1. Capture more articles:
   Minimum: 5 articles
   Recommended: 10-15 for solid report
   Ideal: 20+ for comprehensive analysis
   
2. Ensure coherent collection:
   Articles should be related by theme
   Mix of perspectives valuable
   Include foundational + recent sources
   
3. Combine collections:
   "Create report from 'AI' and 'Transformation' collections"
```

---

#### Issue: Citations formatting wrong

**Symptoms:**
- Inconsistent citation format
- Missing information

**Causes:**
- Citation style not specified
- Source metadata incomplete

**Solutions:**
```
1. Specify style explicitly:
   {"research": {"default_citation_style": "APA"}}
   
2. In request:
   "Generate report using IEEE citation style"
   
3. Fix individual citations:
   "Correct citation 5 to include DOI"
   
4. For missing info:
   Provide: "Add to citation: DOI 10.xxxx/xxxxx"
```

---

## Integration Issues

### Apple Notes

#### Issue: Notes not syncing

**Symptoms:**
- No notes created
- "Sync failed" message

**Causes:**
- Integration not enabled
- Notebook doesn't exist
- Permissions issue

**Solutions:**
```
1. Enable integration:
   {"integrations": {
     "apple_notes": {
       "enabled": true,
       "notebook": "Voice Memos"
     }
   }}
   
2. Create notebook:
   Open Apple Notes → New Folder → "Voice Memos"
   
3. Check permissions:
   System Settings → Privacy → Automation → Allow Claude
   
4. Manual fallback:
   Copy content and paste into Apple Notes
```

---

### Calendar

#### Issue: Events not creating

**Symptoms:**
- No calendar events
- Dates not recognized

**Causes:**
- Integration disabled
- Dates ambiguous
- Requires confirmation

**Solutions:**
```
1. Enable integration:
   {"integrations": {
     "calendar": {
       "enabled": true,
       "auto_create_events": false  // Requires confirmation
     }
   }}
   
2. Be explicit with dates:
   Say: "Friday, November 8th at 2pm"
   Not: "next week sometime"
   
3. Confirm when prompted:
   Claude: "Create event on Nov 8?"
   You: "Yes"
```

---

### Notion

#### Issue: Database sync failing

**Symptoms:**
- No Notion updates
- "Database not found"

**Causes:**
- Database ID incorrect
- Permissions not granted
- Integration not connected

**Solutions:**
```
1. Verify database ID:
   Copy from Notion URL after "/database/"
   Paste in config: "database_id": "abc123..."
   
2. Grant permissions:
   Notion → Settings → Integrations → Allow access
   
3. Test connection:
   "Test Notion sync with a sample article"
```

---

## Configuration Issues

#### Issue: Changes not taking effect

**Symptoms:**
- Modified config, no change in behavior
- Old settings still applied

**Causes:**
- Wrong file edited
- JSON syntax error
- Config not reloaded

**Solutions:**
```
1. Verify file location:
   Voice: ~/MyDrive/VoiceMemos/config/settings.json
   Reading: ~/MyDrive/ReadingList/config/settings.json
   
2. Check JSON validity:
   Use JSON validator (jsonlint.com)
   Common errors:
   - Missing comma
   - Extra comma at end
   - Unmatched brackets
   
3. Reload config:
   Start new Claude conversation
   Or: "Reload configuration files"
```

---

#### Issue: Can't find configuration file

**Symptoms:**
- "Configuration not found"
- Default settings used

**Causes:**
- Files not copied to correct location
- Directory structure wrong

**Solutions:**
```
1. Verify structure:
   ~/MyDrive/VoiceMemos/
   ├── config/
   │   ├── settings.json
   │   └── prompts/
   └── ...
   
2. Copy files:
   cp ~/voice-memos-config/settings.json ~/MyDrive/VoiceMemos/config/
   
3. Create if missing:
   Use default from ~/voice-memos-config/
```

---

## Performance Issues

#### Issue: Processing is slow

**Symptoms:**
- Takes >5 minutes for simple task
- "Processing..." indefinitely

**Causes:**
- Large files
- Complex processing
- API rate limits
- Network issues

**Solutions:**
```
1. For large files:
   - Split into smaller chunks
   - Reduce quality/compress audio
   - Process in batches
   
2. Check network:
   - Verify internet connection
   - API status (Firecrawl, Bright Data)
   
3. Retry:
   "Try processing again"
   
4. Simplify:
   - Disable advanced features temporarily
   - Use brief summaries instead of detailed
```

---

## Getting Help

### When to Ask Claude

```
Good questions:
- "Why wasn't this recognized as an action item?"
- "How do I adjust priority scoring?"
- "Show me the current configuration for transcription"
- "What's the best way to handle multi-language content?"

Claude can:
- Explain configurations
- Troubleshoot specific issues
- Suggest optimizations
- Clarify workflows
```

### Resources

```
Configuration Guides:
- ~/voice-memos-config/CONFIG-GUIDE.md
- ~/reading-list-config/CONFIG-GUIDE.md

Skill Documentation:
- ~/skills/voice-transcription/SKILL.md
- ~/skills/voice-analysis/SKILL.md
- ~/skills/reading-list-capture/SKILL.md
- ~/skills/reading-list-research/SKILL.md

Workflows:
- ~/workflows/voice-memos-quickstart.md
- ~/workflows/reading-list-quickstart.md
- ~/workflows/advanced-use-cases.md
```

### Reporting Issues

```
When reporting an issue to Claude:

1. Describe what you tried:
   "I uploaded [file type] and asked for [action]"
   
2. What happened:
   "Got error message: [exact text]"
   
3. What you expected:
   "Expected [desired outcome]"
   
4. Configuration:
   "My settings have [relevant settings]"
   
5. Files involved:
   Share error logs if available
```

---

## Quick Fixes Checklist

### Before asking for help:

Voice Memos:
- [ ] File format is supported (m4a, mp3, wav, aac, opus, flac)
- [ ] File size under limit (100MB default)
- [ ] Configuration file exists and valid JSON
- [ ] Language setting appropriate
- [ ] Audio quality is clear

Reading List:
- [ ] URL is valid and loads in browser
- [ ] Firecrawl API key configured
- [ ] Configuration file exists and valid JSON
- [ ] User interests configured
- [ ] Source not blocked/paywalled

Both:
- [ ] Files in correct location
- [ ] JSON syntax valid (no errors)
- [ ] Latest configuration loaded
- [ ] Specific about issue when asking

---

**Still stuck?**

Ask Claude with:
1. Specific issue description
2. What you've tried
3. Relevant configuration
4. Error messages (exact text)

**Claude is here to help!** 🤝
