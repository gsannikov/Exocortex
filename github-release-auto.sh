#!/bin/bash
# Generic GitHub Release Script using GitHub CLI
# Usage: ./github-release-auto.sh <work_dir> <repo_name> [repo_owner] [release_tag]

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}${BOLD}======================================================================${NC}"
    echo -e "${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}${BOLD}======================================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

show_usage() {
    cat << EOF
${BOLD}GitHub Automated Release Script${NC}

${BOLD}Usage:${NC}
    $0 <work_dir> <repo_name> [repo_owner] [release_tag]

${BOLD}Arguments:${NC}
    work_dir      Path to the git repository (required)
    repo_name     GitHub repository name (required)
    repo_owner    GitHub username/org (optional, default: current user)
    release_tag   Release tag to create (optional, default: from git tags)

${BOLD}Examples:${NC}
    # Basic usage (will prompt for owner)
    $0 /Users/you/project my-awesome-repo

    # With owner specified
    $0 /Users/you/project my-awesome-repo yourusername

    # With custom release tag
    $0 /Users/you/project my-awesome-repo yourusername v2.0.0

${BOLD}Requirements:${NC}
    - GitHub CLI (gh) installed and authenticated
    - Git repository initialized with at least one commit
    - Release assets in 'releases/' directory (optional)

${BOLD}What it does:${NC}
    1. Verifies repository and GitHub authentication
    2. Creates GitHub repository (if doesn't exist)
    3. Pushes code and tags to GitHub
    4. Creates a release with assets from releases/ directory
    5. Adds repository topics (if configured)
    6. Enables Issues and Discussions

EOF
    exit 1
}

# Parse arguments
WORK_DIR="$1"
REPO_NAME="$2"
REPO_OWNER="${3:-}"
RELEASE_TAG="${4:-}"

# Check required arguments
if [ -z "$WORK_DIR" ] || [ -z "$REPO_NAME" ]; then
    print_error "Missing required arguments"
    echo ""
    show_usage
fi

# Validate work directory exists
if [ ! -d "$WORK_DIR" ]; then
    print_error "Work directory does not exist: $WORK_DIR"
    exit 1
fi

# If repo_owner not provided, get from gh CLI
if [ -z "$REPO_OWNER" ]; then
    if command -v gh &> /dev/null && gh auth status &> /dev/null; then
        REPO_OWNER=$(gh api user -q .login 2>/dev/null || echo "")
        if [ -z "$REPO_OWNER" ]; then
            print_error "Could not determine GitHub username. Please provide repo_owner argument."
            exit 1
        fi
        print_info "Using GitHub user: $REPO_OWNER"
    else
        print_error "GitHub CLI not authenticated. Please provide repo_owner argument or run: gh auth login"
        exit 1
    fi
fi

print_header "GitHub Automated Release - ${REPO_NAME}"

# Change to work directory
print_info "Navigating to: $WORK_DIR"
cd "$WORK_DIR" || {
    print_error "Failed to navigate to $WORK_DIR"
    exit 1
}
print_success "In correct directory: $(pwd)"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

print_success "GitHub CLI found"

# Check if authenticated
if ! gh auth status &> /dev/null; then
    print_error "Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

print_success "GitHub CLI authenticated as: $REPO_OWNER"

# Step 1: Verify git repository
print_header "Step 1: Verifying Repository"

if [ ! -d ".git" ]; then
    print_error "Not in a git repository: $WORK_DIR"
    exit 1
fi

print_success "Git repository verified"

# Get repository description from README if exists
REPO_DESCRIPTION=""
if [ -f "README.md" ]; then
    # Try to extract first paragraph or heading as description
    REPO_DESCRIPTION=$(head -20 README.md | grep -v "^#" | grep -v "^$" | head -1 | cut -c1-100)
fi

if [ -z "$REPO_DESCRIPTION" ]; then
    REPO_DESCRIPTION="Repository: ${REPO_NAME}"
fi

print_info "Repository description: $REPO_DESCRIPTION"

# Determine release tag if not provided
if [ -z "$RELEASE_TAG" ]; then
    # Get latest git tag
    RELEASE_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
    
    if [ -z "$RELEASE_TAG" ]; then
        print_warning "No git tags found. Skipping release creation."
        CREATE_RELEASE=false
    else
        print_info "Using latest git tag: $RELEASE_TAG"
        CREATE_RELEASE=true
    fi
else
    print_info "Using specified release tag: $RELEASE_TAG"
    CREATE_RELEASE=true
fi

# Check for release assets
RELEASE_ASSETS=()
if [ -d "releases" ]; then
    while IFS= read -r -d '' file; do
        RELEASE_ASSETS+=("$file")
    done < <(find releases -type f \( -name "*.zip" -o -name "*.tar.gz" -o -name "*CHECKSUM*" -o -name "*.txt" \) -print0 2>/dev/null)
    
    if [ ${#RELEASE_ASSETS[@]} -gt 0 ]; then
        print_success "Found ${#RELEASE_ASSETS[@]} release asset(s) in releases/"
        for asset in "${RELEASE_ASSETS[@]}"; do
            print_info "  - $asset"
        done
    fi
fi

# Step 2: Check if remote already exists
print_header "Step 2: Checking Remote"

if git remote get-url origin &> /dev/null; then
    print_warning "Remote 'origin' already exists"
    EXISTING_URL=$(git remote get-url origin)
    echo "Existing URL: $EXISTING_URL"
    read -p "Remove and re-add? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
        print_success "Removed existing remote"
    else
        print_info "Keeping existing remote"
    fi
fi

# Step 3: Create GitHub repository
print_header "Step 3: Creating GitHub Repository"

print_info "Creating repository: ${REPO_OWNER}/${REPO_NAME}"

# Check if repository already exists
if gh repo view "${REPO_OWNER}/${REPO_NAME}" &> /dev/null; then
    print_warning "Repository ${REPO_OWNER}/${REPO_NAME} already exists"
    read -p "Continue with existing repository? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted by user"
        exit 0
    fi
    REPO_EXISTS=true
else
    # Create the repository
    gh repo create "${REPO_OWNER}/${REPO_NAME}" \
        --public \
        --description "$REPO_DESCRIPTION" \
        --source=. \
        --push

    print_success "Repository created: https://github.com/${REPO_OWNER}/${REPO_NAME}"
    REPO_EXISTS=false
fi

# Step 4: Push code if repo already existed
if [ "$REPO_EXISTS" = true ]; then
    print_header "Step 4: Pushing Code"
    
    # Ensure remote is set
    if ! git remote get-url origin &> /dev/null; then
        git remote add origin "https://github.com/${REPO_OWNER}/${REPO_NAME}.git"
    fi
    
    # Push main/master branch
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    git push -u origin "$CURRENT_BRANCH"
    print_success "Code pushed to GitHub"
else
    print_info "Code already pushed during repository creation"
fi

# Step 5: Push tags
print_header "Step 5: Pushing Tags"

if [ "$CREATE_RELEASE" = true ]; then
    if git ls-remote --tags origin | grep -q "$RELEASE_TAG"; then
        print_warning "Tag $RELEASE_TAG already exists on remote"
    else
        git push origin --tags
        print_success "Tags pushed to GitHub"
    fi
else
    print_info "No tags to push"
fi

# Step 6: Create GitHub release
if [ "$CREATE_RELEASE" = true ]; then
    print_header "Step 6: Creating GitHub Release"
    
    print_info "Creating release: $RELEASE_TAG"
    
    # Check if release already exists
    if gh release view "$RELEASE_TAG" --repo "${REPO_OWNER}/${REPO_NAME}" &> /dev/null; then
        print_warning "Release $RELEASE_TAG already exists"
        read -p "Delete and recreate? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            gh release delete "$RELEASE_TAG" --repo "${REPO_OWNER}/${REPO_NAME}" --yes
            print_success "Deleted existing release"
        else
            print_info "Keeping existing release, skipping release creation"
            CREATE_RELEASE=false
        fi
    fi
    
    if [ "$CREATE_RELEASE" = true ]; then
        # Prepare release notes
        RELEASE_NOTES="Release ${RELEASE_TAG}

Automated release created from git tag.

For detailed information, see the repository README and CHANGELOG."
        
        # Check if CHANGELOG exists and extract notes for this version
        if [ -f "CHANGELOG.md" ]; then
            CHANGELOG_SECTION=$(awk "/## \[?${RELEASE_TAG#v}\]?/,/## \[?[0-9]/" CHANGELOG.md | sed '1d;$d' 2>/dev/null || echo "")
            if [ ! -z "$CHANGELOG_SECTION" ]; then
                RELEASE_NOTES="$CHANGELOG_SECTION"
            fi
        fi
        
        # Create the release with or without assets
        if [ ${#RELEASE_ASSETS[@]} -gt 0 ]; then
            gh release create "$RELEASE_TAG" \
                --repo "${REPO_OWNER}/${REPO_NAME}" \
                --title "$RELEASE_TAG" \
                --notes "$RELEASE_NOTES" \
                "${RELEASE_ASSETS[@]}"
        else
            gh release create "$RELEASE_TAG" \
                --repo "${REPO_OWNER}/${REPO_NAME}" \
                --title "$RELEASE_TAG" \
                --notes "$RELEASE_NOTES"
        fi
        
        print_success "Release created successfully!"
    fi
else
    print_info "Skipping release creation (no tags found)"
fi

# Step 7: Enable features
print_header "Step 7: Enabling Repository Features"

gh repo edit "${REPO_OWNER}/${REPO_NAME}" \
    --enable-issues \
    --enable-discussions 2>/dev/null || print_warning "Could not enable all features"

print_success "Repository features configured"

# Final summary
print_header "🎉 GitHub Setup Complete!"

echo ""
echo "✅ Repository: https://github.com/${REPO_OWNER}/${REPO_NAME}"
echo "✅ Code pushed to GitHub"
if [ "$CREATE_RELEASE" = true ]; then
    echo "✅ Release published: https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/tag/${RELEASE_TAG}"
    if [ ${#RELEASE_ASSETS[@]} -gt 0 ]; then
        echo "✅ Assets uploaded: ${#RELEASE_ASSETS[@]} file(s)"
    fi
fi
echo "✅ Issues and Discussions enabled"
echo ""
echo "${BOLD}Next Steps:${NC}"
echo "1. Visit: https://github.com/${REPO_OWNER}/${REPO_NAME}"
echo "2. Review the repository"
echo "3. Add repository topics for discoverability"
echo "4. Share with your community!"
echo ""

print_success "All done! 🚀"
echo ""
