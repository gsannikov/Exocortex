#!/bin/bash
# Claude Skill Release Script
# Creates release package with skill-package + user-data templates

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

VERSION=$1

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 1.0.0"
    exit 1
fi

if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Invalid version format${NC}"
    echo "Version must be in format: MAJOR.MINOR.PATCH (e.g., 1.0.0)"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${BLUE}🚀 Claude Skill Release v${VERSION}${NC}\n"

# Check git repository
if [ ! -d "$SKILL_ROOT/.git" ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠  Warning: You have uncommitted changes${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 1
    fi
fi

echo -e "${BLUE}Step 1: Updating version files${NC}"
echo "----------------------------------------"

# Update version.yaml
if [ -f "$SKILL_ROOT/version.yaml" ]; then
    echo "version: \"$VERSION\"" > "$SKILL_ROOT/version.yaml.tmp"
    echo "release_date: \"$(date +%Y-%m-%d)\"" >> "$SKILL_ROOT/version.yaml.tmp"
    echo "status: \"stable\"" >> "$SKILL_ROOT/version.yaml.tmp"
    mv "$SKILL_ROOT/version.yaml.tmp" "$SKILL_ROOT/version.yaml"
    echo -e "${GREEN}✓${NC} Updated version.yaml"
fi

# Update SKILL.md version
if [ -f "$SKILL_ROOT/skill-package/SKILL.md" ]; then
    sed -i.bak "s/version: .*/version: $VERSION/" "$SKILL_ROOT/skill-package/SKILL.md" 2>/dev/null || \
    sed -i '' "s/version: .*/version: $VERSION/" "$SKILL_ROOT/skill-package/SKILL.md" 2>/dev/null
    rm -f "$SKILL_ROOT/skill-package/SKILL.md.bak"
    echo -e "${GREEN}✓${NC} Updated SKILL.md"
fi

echo ""
echo -e "${BLUE}Step 2: Creating release package${NC}"
echo "----------------------------------------"

mkdir -p "$SKILL_ROOT/releases"

RELEASE_NAME="skill-package-v${VERSION}"
RELEASE_DIR="$SKILL_ROOT/releases/$RELEASE_NAME"
RELEASE_ZIP="$SKILL_ROOT/releases/$RELEASE_NAME.zip"

rm -rf "$RELEASE_DIR"
rm -f "$RELEASE_ZIP"
mkdir -p "$RELEASE_DIR"

echo -e "${YELLOW}→${NC} Packaging skill-package (for Claude upload)"
cp -r "$SKILL_ROOT/skill-package/"* "$RELEASE_DIR/"

echo -e "${YELLOW}→${NC} Including user-data templates (for initialization)"
if [ -d "$SKILL_ROOT/user-data-templates" ]; then
    cp -r "$SKILL_ROOT/user-data-templates" "$RELEASE_DIR/"
    echo -e "${GREEN}✓${NC} Copied user-data-templates"
else
    echo -e "${RED}✗${NC} Warning: user-data-templates not found"
fi

# Add setup instructions
cat > "$RELEASE_DIR/SETUP.md" << 'EOF'
# Quick Setup

## 1. Choose Storage Backend

Edit `user-data-templates/config/storage-config-template.yaml` to choose your storage:

- **local** - Local filesystem (recommended)
- **github** - GitHub repository (multi-device)
- **checkpoint** - Session-only (zero setup)
- **email** - Email-based storage
- **notion** - Notion database

## 2. Copy Templates

```bash
cp -r user-data-templates user-data
cd user-data/config
cp storage-config-template.yaml storage-config.yaml
# Edit storage-config.yaml with your settings
```

## 3. Upload to Claude

Upload the entire `skill-package/` directory to Claude Desktop.

## 4. Configure MCP (if using local or github)

See the full setup guide in docs/ for detailed instructions.

---

For complete documentation, see: docs/guides/user-guide/setup.md
EOF

echo -e "${GREEN}✓${NC} Created release directory"

# Create ZIP archive
cd "$SKILL_ROOT/releases"
zip -r "$RELEASE_NAME.zip" "$RELEASE_NAME" > /dev/null
rm -rf "$RELEASE_NAME"

echo -e "${GREEN}✓${NC} Created: releases/$RELEASE_NAME.zip"

# Generate checksum
shasum -a 256 "$RELEASE_NAME.zip" > "CHECKSUMS-${VERSION}.txt"
echo -e "${GREEN}✓${NC} Generated: releases/CHECKSUMS-${VERSION}.txt"

echo ""
echo -e "${BLUE}Step 3: Git operations${NC}"
echo "----------------------------------------"

cd "$SKILL_ROOT"
git add .
echo -e "${GREEN}✓${NC} Staged changes"

git commit -m "Release v${VERSION}" 2>/dev/null || echo -e "${YELLOW}→${NC} No changes to commit"

if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠  Tag v${VERSION} already exists${NC}"
else
    git tag -a "v${VERSION}" -m "Release version ${VERSION}"
    echo -e "${GREEN}✓${NC} Created tag v${VERSION}"
fi

echo ""
echo -e "${BLUE}Step 4: Release Summary${NC}"
echo "----------------------------------------"
echo ""
echo "✅ Release v${VERSION} created!"
echo ""
echo -e "${GREEN}Package Contents:${NC}"
echo "  📦 skill-package/        - Core skill (upload to Claude)"
echo "  📁 user-data-templates/  - Storage configuration templates"
echo "  📄 SETUP.md             - Quick setup guide"
echo ""
echo -e "${BLUE}Release Files:${NC}"
echo "  • releases/$RELEASE_NAME.zip"
echo "  • releases/CHECKSUMS-${VERSION}.txt"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Test: unzip and verify contents"
echo "  2. Push: git push origin main --tags"
echo "  3. Create GitHub release with ZIP"
echo "  4. Update CHANGELOG.md"
echo ""
echo -e "${GREEN}✅ Done!${NC}"
