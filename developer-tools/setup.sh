#!/bin/bash
# Claude Skill Setup Script
# Initializes directory structure and configuration

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Claude Skill Setup${NC}\n"

# Get script directory (where this script is located)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${BLUE}Skill root: ${SKILL_ROOT}${NC}\n"

# Function to create directory if it doesn't exist
create_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo -e "${GREEN}✓${NC} Created: $1"
    else
        echo -e "${YELLOW}→${NC} Exists: $1"
    fi
}

# Function to copy template if target doesn't exist
copy_template() {
    local template=$1
    local target=$2
    
    if [ ! -f "$target" ]; then
        if [ -f "$template" ]; then
            cp "$template" "$target"
            echo -e "${GREEN}✓${NC} Created: $target"
        else
            echo -e "${YELLOW}⚠${NC}  Template not found: $template"
        fi
    else
        echo -e "${YELLOW}→${NC} Exists: $target"
    fi
}

echo -e "${BLUE}Step 1: Creating directory structure${NC}"
echo "----------------------------------------"

# Core directories
create_dir "$SKILL_ROOT/skill-package"
create_dir "$SKILL_ROOT/skill-package/config"
create_dir "$SKILL_ROOT/skill-package/modules"
create_dir "$SKILL_ROOT/skill-package/scripts"
create_dir "$SKILL_ROOT/skill-package/templates"
create_dir "$SKILL_ROOT/skill-package/references"

# User data directories
create_dir "$SKILL_ROOT/user-data"
create_dir "$SKILL_ROOT/user-data/config"
create_dir "$SKILL_ROOT/user-data/db"
create_dir "$SKILL_ROOT/user-data/logs"

# Documentation directories
create_dir "$SKILL_ROOT/docs"
create_dir "$SKILL_ROOT/docs/skill-developers"
create_dir "$SKILL_ROOT/docs/skill-developers/user-guide"
create_dir "$SKILL_ROOT/docs/skill-developers/guides"
create_dir "$SKILL_ROOT/docs/sdk-developers"
create_dir "$SKILL_ROOT/docs/sdk-developers/architecture"

# Automation directories
create_dir "$SKILL_ROOT/developer-tools"
create_dir "$SKILL_ROOT/sdk/.github"
create_dir "$SKILL_ROOT/sdk/.github/workflows"

echo ""
echo -e "${BLUE}Step 2: Creating configuration files${NC}"
echo "----------------------------------------"

# Copy user config template
copy_template \
    "$SKILL_ROOT/user-data/config/user-config-template.yaml" \
    "$SKILL_ROOT/user-data/config/user-config.yaml"

echo ""
echo -e "${BLUE}Step 3: Checking Python dependencies${NC}"
echo "----------------------------------------"

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"
    
    # Check for required packages
    if python3 -c "import yaml" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} PyYAML installed"
    else
        echo -e "${YELLOW}⚠${NC}  PyYAML not found. Install with: pip3 install pyyaml"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Python 3 not found. Some automation scripts may not work."
fi

echo ""
echo -e "${BLUE}Step 4: Git initialization (optional)${NC}"
echo "----------------------------------------"

if [ -d "$SKILL_ROOT/.git" ]; then
    echo -e "${YELLOW}→${NC} Git already initialized"
else
    read -p "Initialize Git repository? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$SKILL_ROOT"
        git init
        echo -e "${GREEN}✓${NC} Git initialized"
        
        # Create initial commit
        git add .gitignore README.md
        git commit -m "Initial commit: Claude Skill Template" 2>/dev/null || echo -e "${YELLOW}⚠${NC}  No files to commit"
    else
        echo -e "${YELLOW}→${NC} Skipped Git initialization"
    fi
fi

echo ""
echo -e "${BLUE}Step 5: Next steps${NC}"
echo "----------------------------------------"
echo ""
echo "Configuration:"
echo "  1. Edit skill-package/config/paths.py with your local path"
echo "  2. Edit user-data/config/user-config.yaml with your settings"
echo "  3. Upload skill-package/ to Claude Desktop"
echo ""
echo "Documentation:"
echo "  - README.md for overview"
echo "  - docs/skill-developers/user-guide/ for usage instructions"
echo "  - docs/skill-developers/guides/ for development guide"
echo ""
echo "Validation:"
echo "  Run: python3 developer-tools/validate.py"
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
