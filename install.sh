#!/bin/bash
#
# Claude Skills One-Line Installer
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/gsannikov/claude-skills/main/install.sh | bash
#
# Or download and run:
#   chmod +x install.sh && ./install.sh
#

set -e

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

REPO_URL="https://github.com/gsannikov/claude-skills.git"
INSTALL_DIR="${CLAUDE_SKILLS_DIR:-$HOME/MyDrive/claude-skills}"
BRANCH="${CLAUDE_SKILLS_BRANCH:-main}"

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Disable colors if not terminal
if [ ! -t 1 ]; then
    RED='' GREEN='' YELLOW='' BLUE='' CYAN='' BOLD='' DIM='' NC=''
fi

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

print_header() {
    echo ""
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}  $1${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${BOLD}${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    print_header "Claude Skills Installer"

    echo -e "This script will:"
    echo -e "  1. Check prerequisites (git, python3)"
    echo -e "  2. Clone the Claude Skills repository"
    echo -e "  3. Run the setup wizard"
    echo ""

    # ─────────────────────────────────────────────────────────────────────────
    # Check prerequisites
    # ─────────────────────────────────────────────────────────────────────────

    print_step "Checking prerequisites..."

    # Check git
    if check_command git; then
        print_success "git is installed"
    else
        print_error "git is not installed"
        echo ""
        echo "Please install git first:"
        case "$(uname -s)" in
            Darwin)
                echo "  brew install git"
                echo "  or: xcode-select --install"
                ;;
            Linux)
                echo "  sudo apt install git"
                echo "  or: sudo yum install git"
                ;;
            *)
                echo "  Please install git for your platform"
                ;;
        esac
        exit 1
    fi

    # Check Python 3
    PYTHON_CMD=""
    if check_command python3; then
        PYTHON_CMD="python3"
        print_success "python3 is installed"
    elif check_command python; then
        # Check if it's Python 3
        if python --version 2>&1 | grep -q "Python 3"; then
            PYTHON_CMD="python"
            print_success "python is installed (Python 3)"
        else
            print_error "Python 3 is required, but only Python 2 was found"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        echo ""
        echo "Please install Python 3 first:"
        case "$(uname -s)" in
            Darwin)
                echo "  brew install python3"
                ;;
            Linux)
                echo "  sudo apt install python3"
                echo "  or: sudo yum install python3"
                ;;
            *)
                echo "  Please install Python 3 for your platform"
                ;;
        esac
        exit 1
    fi

    # ─────────────────────────────────────────────────────────────────────────
    # Confirm installation directory
    # ─────────────────────────────────────────────────────────────────────────

    print_step "Installation directory"

    echo -e "Skills will be installed to: ${CYAN}${INSTALL_DIR}${NC}"
    echo ""

    # Check if directory exists
    if [ -d "$INSTALL_DIR" ]; then
        if [ -d "$INSTALL_DIR/.git" ]; then
            print_warning "Directory exists and is a git repository"
            echo ""
            read -p "Update existing installation? [Y/n] " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Nn]$ ]]; then
                print_info "Installation cancelled"
                exit 0
            fi

            # Pull latest changes
            print_step "Updating existing installation..."
            cd "$INSTALL_DIR"
            git fetch origin "$BRANCH"
            git checkout "$BRANCH"
            git pull origin "$BRANCH"
            print_success "Updated to latest version"
        else
            print_error "Directory exists but is not a Claude Skills repository"
            echo "Please remove it or set CLAUDE_SKILLS_DIR to a different location:"
            echo "  CLAUDE_SKILLS_DIR=~/other/path ./install.sh"
            exit 1
        fi
    else
        # Clone repository
        print_step "Cloning repository..."

        # Create parent directory if needed
        mkdir -p "$(dirname "$INSTALL_DIR")"

        git clone --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
        print_success "Repository cloned"

        cd "$INSTALL_DIR"
    fi

    # ─────────────────────────────────────────────────────────────────────────
    # Run setup script
    # ─────────────────────────────────────────────────────────────────────────

    print_step "Running setup wizard..."
    echo ""

    if [ -f "setup.py" ]; then
        $PYTHON_CMD setup.py
    else
        print_error "setup.py not found in repository"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# Error handling
# ═══════════════════════════════════════════════════════════════════════════════

trap 'print_error "Installation failed!"; exit 1' ERR

# ═══════════════════════════════════════════════════════════════════════════════
# Run
# ═══════════════════════════════════════════════════════════════════════════════

main "$@"
