#!/bin/bash
# Auto-setup script for local filesystem storage
# Run once, works forever

set -e

echo "🚀 Claude Skill Storage Setup"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Claude"
    OS="Linux"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Detected: $OS"
echo ""

# Get current directory
SKILL_DIR="$(pwd)"
USER_DATA_DIR="$SKILL_DIR/user-data"

echo "📁 Skill directory: $SKILL_DIR"
echo "💾 User data will be at: $USER_DATA_DIR"
echo ""

# Create user-data from templates
if [ ! -d "$USER_DATA_DIR" ]; then
    echo "Creating user-data directory..."
    cp -r user-data-templates "$USER_DATA_DIR"
    echo "✅ Created user-data/"
else
    echo "✅ user-data/ already exists"
fi

# Update paths.py
PATHS_FILE="$SKILL_DIR/skill-package/config/paths.py"
if [ -f "$PATHS_FILE" ]; then
    echo "Updating paths.py..."
    cat > "$PATHS_FILE" << EOF
"""File system paths configuration"""
import os

# User data directory (absolute path)
USER_DATA_BASE = "$USER_DATA_DIR"

# Subdirectories
CONFIG_DIR = os.path.join(USER_DATA_BASE, "config")
DB_DIR = os.path.join(USER_DATA_BASE, "db")
LOGS_DIR = os.path.join(USER_DATA_BASE, "logs")
EOF
    echo "✅ Updated paths.py"
fi

# Check if Claude config exists
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "⚠️  Claude config not found at: $CONFIG_FILE"
    echo "Creating it now..."
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "$USER_DATA_DIR"
      ]
    }
  }
}
EOF
    echo "✅ Created Claude config"
else
    # Check if filesystem MCP already configured
    if grep -q "filesystem" "$CONFIG_FILE"; then
        echo ""
        echo "⚠️  Filesystem MCP already configured"
        echo "Current config: $CONFIG_FILE"
        echo ""
        echo "To use this skill's user-data, update the path to:"
        echo "  $USER_DATA_DIR"
    else
        echo ""
        echo "Adding filesystem MCP to config..."
        # Backup original
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
        
        # Add filesystem MCP (assumes valid JSON)
        python3 << PYTHON
import json

config_file = "$CONFIG_FILE"
with open(config_file, 'r') as f:
    config = json.load(f)

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['filesystem'] = {
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "$USER_DATA_DIR"
    ]
}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Added filesystem MCP to config")
PYTHON
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Restart Claude Desktop (Cmd+Q or close completely)"
echo "2. Upload skill-package/ to Claude"
echo "3. Start using the skill!"
echo ""
echo "Your data will be stored at:"
echo "  $USER_DATA_DIR"
echo ""
