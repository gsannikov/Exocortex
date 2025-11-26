# Meeting Recorder

A lightweight macOS menu bar app that captures audio from meeting applications (Zoom, Google Meet, Microsoft Teams, etc.) and integrates with the voice-memos skill for transcription and analysis.

## Features

- **Auto-Detection**: Automatically detects when meeting apps start
- **One-Click Recording**: Start/stop recording from menu bar
- **Notification Prompts**: "Record this meeting?" when meetings detected
- **ScreenCaptureKit**: Uses Apple's modern API - no BlackHole needed
- **Smart Compression**: 64kbps AAC optimized for speech (~30MB/hour)
- **Auto-Chunking**: Long meetings split into processable chunks
- **Claude Integration**: Seamless handoff to voice-memos skill

## Requirements

- macOS 12.3 or later (for ScreenCaptureKit)
- Xcode Command Line Tools
- Screen Recording permission

## Quick Install

```bash
cd ~/MyDrive/claude-skills/packages/voice-memos/meeting-recorder
./setup.sh
```

## Manual Build

```bash
cd MeetingRecorder

# Standard build
swift build -c release
./.build/release/MeetingRecorder

# If building from Google Drive (to avoid sync conflicts)
swift build -c release --scratch-path /tmp/MeetingRecorder-build
```

> **Note**: If you see "disk I/O error" during build, use the `--scratch-path` option to place build artifacts outside the synced folder.

## Permissions Required

After first launch, grant these permissions in **System Preferences → Privacy & Security**:

| Permission | Why Needed |
|------------|------------|
| **Screen Recording** | Capture audio from meeting apps via ScreenCaptureKit |
| **Accessibility** | Detect running applications (optional but recommended) |
| **Notifications** | Show "Record meeting?" prompts |

## Usage

### Automatic Mode
1. Start the app (runs in menu bar)
2. Join a meeting in Zoom/Meet/Teams
3. Notification appears: "Record this meeting?"
4. Click "Record" to start
5. Recording stops when meeting ends (or click "Stop")

### Manual Mode
1. Click menu bar icon
2. Select "Start Recording"
3. Recording captures all system audio
4. Click "Stop Recording" when done

### Processing Recordings
```
# In Claude Desktop or CLI
process meeting recordings
```

Or add to Apple Notes inbox manually.

## File Locations

```
Recordings:   ~/MyDrive/claude-skills-data/voice-memos/meetings/
Transcripts:  ~/MyDrive/claude-skills-data/voice-memos/meetings/transcripts/
Config:       ~/MyDrive/claude-skills-data/voice-memos/meeting-recorder-config.yaml
```

## Supported Meeting Apps

| App | Detection | Notes |
|-----|-----------|-------|
| Zoom | ✅ Native | Detects meeting windows |
| Google Meet | ✅ Browser | Via Chrome/Safari window title |
| Microsoft Teams | ✅ Native | Desktop app |
| Slack Huddles | ✅ Native | Desktop app |
| Discord | ✅ Native | Voice channels |
| Webex | ✅ Native | Desktop app |
| FaceTime | ✅ Native | Built-in |

## Audio Settings

Default settings optimized for speech transcription:

| Setting | Value | Reason |
|---------|-------|--------|
| Format | M4A (AAC) | Good compression, wide support |
| Bitrate | 64 kbps | Sufficient for speech |
| Sample Rate | 16 kHz | Optimal for speech recognition |
| Channels | Mono | Meetings don't need stereo |
| Chunk Size | 40 min | Stays under Claude's 25MB limit |

## Auto-Chunking

For meetings longer than 40 minutes:
- Recording automatically splits into chunks
- Files named: `2024-01-15_14-30_zoom_chunk0.m4a`, `_chunk1.m4a`, etc.
- Voice-memos skill merges transcripts automatically
- Speaker labels maintained across chunks

## Troubleshooting

### "No audio captured"
1. Check Screen Recording permission is granted
2. Ensure meeting app has audio playing
3. Try manual recording mode

### "App not detected"
1. Grant Accessibility permission
2. Check if meeting app is in supported list
3. Use manual recording as fallback

### "Permission denied" error
```bash
# Reset permissions and try again
tccutil reset ScreenCapture com.claude-skills.meeting-recorder
```

### Build fails
```bash
# Ensure Xcode CLI tools installed
xcode-select --install

# For XCTest errors, point to full Xcode
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

# Clean and rebuild
cd MeetingRecorder
rm -rf .build
swift build -c release

# For Google Drive: use external scratch path
swift build -c release --scratch-path /tmp/MeetingRecorder-build
```

## Configuration

Edit `~/MyDrive/claude-skills-data/voice-memos/meeting-recorder-config.yaml`:

```yaml
# Audio settings
audio:
  format: m4a
  bitrate: 64000
  sample_rate: 16000
  channels: 1

# Chunking
chunking:
  enabled: true
  duration_minutes: 40

# Behavior
behavior:
  auto_detect_meetings: true
  notifications_enabled: true
  auto_record: false  # Set true to skip confirmation

# Meeting apps to detect
meeting_apps:
  - Zoom
  - Google Meet
  - Microsoft Teams
  - Slack
  - Discord
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Meeting Recorder                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                   │
│  │ AppDelegate  │───▶│ Menu Bar UI  │                   │
│  └──────┬───────┘    └──────────────┘                   │
│         │                                                │
│  ┌──────▼───────┐    ┌──────────────┐                   │
│  │ Meeting      │───▶│ Notification │                   │
│  │ Detector     │    │ "Record?"    │                   │
│  └──────────────┘    └──────────────┘                   │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                   │
│  │ Audio        │───▶│ .m4a files   │                   │
│  │ Capture      │    │ (chunked)    │                   │
│  │ (SCKit)      │    └──────┬───────┘                   │
│  └──────────────┘           │                           │
│                             ▼                           │
│                    ┌──────────────┐                     │
│                    │ voice-memos  │                     │
│                    │ skill        │                     │
│                    └──────────────┘                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Integration with Claude

The app creates recordings that the voice-memos skill can process:

```
# Automatic discovery
Claude: "process meeting recordings"

# Or via Apple Notes
Add to "🎙️ Voice Memos Inbox":
  meetings/2024-01-15_14-30_zoom.m4a
```

## Privacy

- **100% Local**: Audio never leaves your Mac during recording
- **No Cloud**: ScreenCaptureKit runs entirely on-device
- **You Control**: Only transcribed when you process with Claude
- **Delete Anytime**: Recordings stored locally in your data folder

## Version History

### 1.0.1 (2025-11)
- Fixed Swift 6 Sendable concurrency warnings
- Added `@unchecked Sendable` to AudioCapture class
- Improved build documentation for Google Drive users

### 1.0.0 (2024-01)
- Initial release
- ScreenCaptureKit audio capture
- Meeting app detection
- Auto-chunking for long meetings
- Integration with voice-memos skill
