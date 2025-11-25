#!/bin/bash
# Meeting Recorder - Setup Script
# Builds and installs the Meeting Recorder menu bar app

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/MeetingRecorder"
BUILD_DIR="$APP_DIR/.build/release"
INSTALL_DIR="$HOME/Applications"
APP_NAME="MeetingRecorder"
DATA_DIR="$HOME/MyDrive/claude-skills-data/voice-memos/meetings"

echo "=================================="
echo "Meeting Recorder Setup"
echo "=================================="
echo ""

# Check for macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "Error: This app only runs on macOS"
    exit 1
fi

# Check macOS version (need 12.3+ for ScreenCaptureKit)
macos_version=$(sw_vers -productVersion)
major_version=$(echo "$macos_version" | cut -d. -f1)
minor_version=$(echo "$macos_version" | cut -d. -f2)

if [[ "$major_version" -lt 12 ]] || ([[ "$major_version" -eq 12 ]] && [[ "$minor_version" -lt 3 ]]); then
    echo "Error: macOS 12.3 or later required for ScreenCaptureKit"
    echo "Current version: $macos_version"
    exit 1
fi

echo "✓ macOS version: $macos_version"

# Check for Xcode command line tools
if ! xcode-select -p &> /dev/null; then
    echo "Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "Please run this script again after installation completes."
    exit 1
fi

echo "✓ Xcode Command Line Tools installed"

# Create data directory
if [[ ! -d "$DATA_DIR" ]]; then
    echo "Creating data directory: $DATA_DIR"
    mkdir -p "$DATA_DIR"
    mkdir -p "$DATA_DIR/transcripts"
fi

echo "✓ Data directory ready"

# Build the app
echo ""
echo "Building Meeting Recorder..."
cd "$APP_DIR"

# Clean previous build
rm -rf .build

# Build release version
swift build -c release

if [[ ! -f "$BUILD_DIR/$APP_NAME" ]]; then
    echo "Error: Build failed"
    exit 1
fi

echo "✓ Build successful"

# Create Applications directory if needed
if [[ ! -d "$INSTALL_DIR" ]]; then
    mkdir -p "$INSTALL_DIR"
fi

# Create app bundle
APP_BUNDLE="$INSTALL_DIR/$APP_NAME.app"
CONTENTS_DIR="$APP_BUNDLE/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo ""
echo "Creating app bundle..."

rm -rf "$APP_BUNDLE"
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Copy binary
cp "$BUILD_DIR/$APP_NAME" "$MACOS_DIR/"

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Meeting Recorder</string>
    <key>CFBundleDisplayName</key>
    <string>Meeting Recorder</string>
    <key>CFBundleIdentifier</key>
    <string>com.claude-skills.meeting-recorder</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleExecutable</key>
    <string>MeetingRecorder</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.3</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSMicrophoneUsageDescription</key>
    <string>Meeting Recorder needs microphone access to capture your voice in meetings.</string>
    <key>NSScreenCaptureUsageDescription</key>
    <string>Meeting Recorder needs screen recording permission to capture meeting audio from apps like Zoom and Google Meet.</string>
    <key>NSAppleEventsUsageDescription</key>
    <string>Meeting Recorder needs automation access to detect when meeting apps are running.</string>
</dict>
</plist>
PLIST

echo "✓ App bundle created"

# Sign the app (ad-hoc for local use)
echo ""
echo "Signing app bundle..."
codesign --force --deep --sign - "$APP_BUNDLE" 2>/dev/null || true
echo "✓ App signed (ad-hoc)"

# Create launch agent for auto-start (optional)
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENT_DIR/com.claude-skills.meeting-recorder.plist"

echo ""
read -p "Would you like Meeting Recorder to start automatically at login? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "$LAUNCH_AGENT_DIR"
    cat > "$LAUNCH_AGENT_FILE" << LAUNCHAGENT
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude-skills.meeting-recorder</string>
    <key>ProgramArguments</key>
    <array>
        <string>$MACOS_DIR/$APP_NAME</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
LAUNCHAGENT
    echo "✓ Launch agent created (will start at login)"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "App installed to: $APP_BUNDLE"
echo "Recordings saved to: $DATA_DIR"
echo ""
echo "IMPORTANT - Grant Permissions:"
echo "1. Open System Preferences → Privacy & Security"
echo "2. Enable 'Screen Recording' for Meeting Recorder"
echo "3. Enable 'Accessibility' for Meeting Recorder (optional, for app detection)"
echo ""
echo "To start the app now, run:"
echo "  open '$APP_BUNDLE'"
echo ""
echo "Or search for 'Meeting Recorder' in Spotlight."
echo ""
