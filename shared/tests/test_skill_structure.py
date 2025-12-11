"""
Test suite for validating Claude Skills structure and SKILL.md compliance.

This module validates that all skills in the packages/ directory follow
the Claude Skills conventions documented in CONTRIBUTING.md.

Rules validated based on CONTRIBUTING.md:

Required Files (per CONTRIBUTING.md):
- SKILL.md - Main specification loaded by Claude
- README.md - Human-readable documentation
- CHANGELOG.md - Version history
- version.yaml - Version metadata

SKILL.md Structure:
1. Frontmatter (YAML): name, description
2. Header: # Skill Name
3. Overview/Capabilities section
4. Commands/Tools section
5. Workflows (recommended)
6. Configuration (recommended)
7. Data Storage (recommended)

version.yaml Format:
- version: semver (MAJOR.MINOR.PATCH)
- updated: date
- skill: skill-name
- codename: Descriptive Name
- status: stable|beta|alpha|deprecated

Naming Conventions:
- skills: kebab-case (e.g., career-consultant)
- files: kebab-case.yaml or kebab-case.md
"""

import re
from pathlib import Path
from typing import Optional

import pytest
import yaml


# =============================================================================
# SKILL.md Validation Rules (from CONTRIBUTING.md)
# =============================================================================

# Required frontmatter fields per CONTRIBUTING.md
REQUIRED_FRONTMATTER_FIELDS = ["name", "description"]

# Required files per CONTRIBUTING.md:
# "SKILL.md - Main specification loaded by Claude"
# "README.md - Human-readable documentation"
# "CHANGELOG.md - Version history"
# "version.yaml - Version metadata"
REQUIRED_FILES = ["SKILL.md", "README.md", "CHANGELOG.md", "version.yaml"]

# Optional but recommended
RECOMMENDED_FILES = ["AI_GUIDE.md"]

# Required version.yaml fields per CONTRIBUTING.md
REQUIRED_VERSION_YAML_FIELDS = ["version", "updated", "skill"]
RECOMMENDED_VERSION_YAML_FIELDS = ["codename", "status"]
VALID_STATUS_VALUES = ["stable", "beta", "alpha", "deprecated"]


# =============================================================================
# Helper Functions
# =============================================================================

def parse_yaml_frontmatter(content: str) -> tuple[Optional[dict], str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, remaining_content).
        frontmatter_dict is None if no frontmatter found.
    """
    if not content.startswith("---"):
        return None, content

    # Find closing ---
    match = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.DOTALL)
    if not match:
        return None, content

    try:
        frontmatter = yaml.safe_load(match.group(1))
        return frontmatter, match.group(2)
    except yaml.YAMLError:
        return None, content


def extract_headers(content: str) -> list[tuple[int, str]]:
    """
    Extract all markdown headers from content.

    Returns:
        List of (level, header_text) tuples.
    """
    headers = []
    for line in content.split("\n"):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append((level, text))
    return headers


def has_section(headers: list[tuple[int, str]], section_keywords: tuple[str, ...]) -> bool:
    """
    Check if any header contains one of the section keywords.

    Args:
        headers: List of (level, text) tuples from extract_headers
        section_keywords: Tuple of keywords to match (any match is success)
    """
    for _, text in headers:
        text_lower = text.lower()
        for keyword in section_keywords:
            if keyword in text_lower:
                return True
    return False


# =============================================================================
# Test Discovery - Parameterized Tests
# =============================================================================

def get_all_skill_dirs() -> list[Path]:
    """Discover all skill directories for test parameterization."""
    repo_root = Path(__file__).parent.parent.parent
    packages_dir = repo_root / "packages"

    if not packages_dir.exists():
        return []

    return [
        d for d in packages_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")
    ]


SKILL_DIRS = get_all_skill_dirs()
SKILL_IDS = [d.name for d in SKILL_DIRS]


# =============================================================================
# Tests: Required File Structure (per CONTRIBUTING.md)
# =============================================================================

class TestSkillRequiredFiles:
    """Test that skill packages have required files per CONTRIBUTING.md."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_skill_md_exists(self, skill_dir: Path):
        """SKILL.md MUST exist - Main specification loaded by Claude."""
        skill_md = skill_dir / "SKILL.md"
        assert skill_md.exists(), (
            f"Missing required SKILL.md in {skill_dir.name}. "
            f"Per CONTRIBUTING.md: 'SKILL.md - Main specification loaded by Claude'"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_readme_exists(self, skill_dir: Path):
        """README.md MUST exist - Human-readable documentation."""
        readme = skill_dir / "README.md"
        dev_readme = skill_dir / "_dev" / "README.md"
        
        assert readme.exists() or dev_readme.exists(), (
            f"Missing required README.md in {skill_dir.name}. "
            f"Per CONTRIBUTING.md: 'README.md - Human-readable documentation' "
            f"(checked root and _dev/)"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_changelog_exists(self, skill_dir: Path):
        """CHANGELOG.md MUST exist - Version history."""
        changelog = skill_dir / "CHANGELOG.md"
        dev_changelog = skill_dir / "_dev" / "CHANGELOG.md"
        
        assert changelog.exists() or dev_changelog.exists(), (
            f"Missing required CHANGELOG.md in {skill_dir.name}. "
            f"Per CONTRIBUTING.md: 'CHANGELOG.md - Version history' "
            f"(checked root and _dev/)"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_exists(self, skill_dir: Path):
        """version.yaml MUST exist - Version metadata."""
        version_file = skill_dir / "version.yaml"
        dev_version_file = skill_dir / "_dev" / "version.yaml"
        
        assert version_file.exists() or dev_version_file.exists(), (
            f"Missing required version.yaml in {skill_dir.name}. "
            f"Per CONTRIBUTING.md: 'version.yaml - Version metadata' "
            f"(checked root and _dev/)"
        )


# =============================================================================
# Tests: SKILL.md Frontmatter (per CONTRIBUTING.md)
# =============================================================================

class TestSkillMdFrontmatter:
    """Test SKILL.md YAML frontmatter compliance per CONTRIBUTING.md."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_has_yaml_frontmatter(self, skill_dir: Path):
        """SKILL.md MUST have YAML frontmatter."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        frontmatter, _ = parse_yaml_frontmatter(content)

        assert frontmatter is not None, (
            f"SKILL.md in {skill_dir.name} must start with YAML frontmatter. "
            f"Per CONTRIBUTING.md format:\n"
            f"---\n"
            f"name: skill-name\n"
            f"description: One-line description\n"
            f"---"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_has_name_field(self, skill_dir: Path):
        """SKILL.md frontmatter MUST have 'name' field."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        frontmatter, _ = parse_yaml_frontmatter(content)

        if frontmatter is None:
            pytest.skip("No frontmatter found")

        assert "name" in frontmatter, (
            f"SKILL.md in {skill_dir.name} must have 'name' field in frontmatter"
        )
        assert frontmatter["name"], (
            f"SKILL.md 'name' field in {skill_dir.name} must not be empty"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_has_description_field(self, skill_dir: Path):
        """SKILL.md frontmatter MUST have 'description' field."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        frontmatter, _ = parse_yaml_frontmatter(content)

        if frontmatter is None:
            pytest.skip("No frontmatter found")

        assert "description" in frontmatter, (
            f"SKILL.md in {skill_dir.name} must have 'description' field in frontmatter"
        )
        assert frontmatter["description"], (
            f"SKILL.md 'description' field in {skill_dir.name} must not be empty"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_description_is_meaningful(self, skill_dir: Path):
        """SKILL.md description SHOULD be at least 20 characters."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        frontmatter, _ = parse_yaml_frontmatter(content)

        if frontmatter is None or "description" not in frontmatter:
            pytest.skip("No description field found")

        description = frontmatter["description"]
        min_length = 20

        assert len(description) >= min_length, (
            f"SKILL.md description in {skill_dir.name} should be at least "
            f"{min_length} characters (got {len(description)}). "
            f"Provide a meaningful one-line description of what the skill does."
        )


# =============================================================================
# Tests: SKILL.md Required Sections (per CONTRIBUTING.md)
# =============================================================================

class TestSkillMdSections:
    """Test SKILL.md has required content sections per CONTRIBUTING.md."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_has_h1_title(self, skill_dir: Path):
        """SKILL.md MUST have an H1 title (# Skill Name)."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        _, body = parse_yaml_frontmatter(content)
        headers = extract_headers(body)

        h1_headers = [h for level, h in headers if level == 1]

        assert len(h1_headers) >= 1, (
            f"SKILL.md in {skill_dir.name} must have an H1 title header. "
            f"Per CONTRIBUTING.md: 'Header: # Skill Name'"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_has_capabilities_section(self, skill_dir: Path):
        """SKILL.md MUST have capabilities/overview section."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        _, body = parse_yaml_frontmatter(content)
        headers = extract_headers(body)

        # Per CONTRIBUTING.md: "Overview: What the skill does, key capabilities"
        capability_keywords = (
            "capabilities", "key capabilities", "overview",
            "what this does", "features"
        )

        assert has_section(headers, capability_keywords), (
            f"SKILL.md in {skill_dir.name} must have a capabilities/overview section. "
            f"Per CONTRIBUTING.md: 'Overview: What the skill does, key capabilities'. "
            f"Add a section with one of these headers: {capability_keywords}"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_has_commands_section(self, skill_dir: Path):
        """SKILL.md MUST have commands section."""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md not found")

        content = skill_md.read_text()
        _, body = parse_yaml_frontmatter(content)
        headers = extract_headers(body)

        # Per CONTRIBUTING.md: "Commands: All user-facing commands with examples"
        command_keywords = ("commands", "tools", "usage", "when to invoke")

        assert has_section(headers, command_keywords), (
            f"SKILL.md in {skill_dir.name} must have a commands section. "
            f"Per CONTRIBUTING.md: 'Commands: All user-facing commands with examples'. "
            f"Add a section with one of these headers: {command_keywords}"
        )


# =============================================================================
# Tests: version.yaml Structure (per CONTRIBUTING.md)
# =============================================================================

class TestVersionYaml:
    """Test version.yaml compliance per CONTRIBUTING.md format."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_is_valid(self, skill_dir: Path):
        """version.yaml MUST be valid YAML."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
            assert data is not None, "version.yaml is empty"
        except yaml.YAMLError as e:
            pytest.fail(f"version.yaml in {skill_dir.name} has invalid YAML: {e}")

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_has_version(self, skill_dir: Path):
        """version.yaml MUST have 'version' field."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            pytest.skip("Invalid YAML")

        assert "version" in data, (
            f"version.yaml in {skill_dir.name} must have 'version' field. "
            f"Per CONTRIBUTING.md format: version: 1.0.0"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_has_updated(self, skill_dir: Path):
        """version.yaml MUST have 'updated' field."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            pytest.skip("Invalid YAML")

        assert "updated" in data, (
            f"version.yaml in {skill_dir.name} must have 'updated' field. "
            f"Per CONTRIBUTING.md format: updated: 2025-11-25"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_has_skill(self, skill_dir: Path):
        """version.yaml MUST have 'skill' field."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            pytest.skip("Invalid YAML")

        assert "skill" in data, (
            f"version.yaml in {skill_dir.name} must have 'skill' field. "
            f"Per CONTRIBUTING.md format: skill: {skill_dir.name}"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_follows_semver(self, skill_dir: Path):
        """version.yaml version MUST follow semver format."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            pytest.skip("Invalid YAML")

        if "version" not in data:
            pytest.skip("No version field")

        version = str(data["version"])
        # Semver pattern: MAJOR.MINOR.PATCH with optional pre-release/build
        semver_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$"

        assert re.match(semver_pattern, version), (
            f"version.yaml in {skill_dir.name} has version '{version}' "
            f"which doesn't follow semver format (MAJOR.MINOR.PATCH). "
            f"Per CONTRIBUTING.md: Use patch/minor/major bumping"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_status_is_valid(self, skill_dir: Path):
        """version.yaml 'status' field (if present) MUST be valid value."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            pytest.skip("Invalid YAML")

        if "status" not in data:
            pytest.skip("No status field (optional)")

        status = data["status"]
        assert status in VALID_STATUS_VALUES, (
            f"version.yaml in {skill_dir.name} has invalid status '{status}'. "
            f"Per CONTRIBUTING.md, valid values are: {VALID_STATUS_VALUES}"
        )


# =============================================================================
# Tests: Naming Conventions (per CONTRIBUTING.md)
# =============================================================================

class TestNamingConventions:
    """Test naming conventions per CONTRIBUTING.md."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_skill_directory_is_kebab_case(self, skill_dir: Path):
        """Skill directory names MUST be kebab-case."""
        name = skill_dir.name
        # Per CONTRIBUTING.md: "skills: kebab-case (e.g., career-consultant)"
        kebab_pattern = r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$"

        assert re.match(kebab_pattern, name), (
            f"Skill directory '{name}' must be kebab-case. "
            f"Per CONTRIBUTING.md: 'skills: kebab-case (e.g., career-consultant)'"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_version_yaml_skill_matches_directory(self, skill_dir: Path):
        """version.yaml 'skill' field SHOULD match directory name."""
        version_file = skill_dir / "version.yaml"
        if not version_file.exists():
            version_file = skill_dir / "_dev" / "version.yaml"
            
        if not version_file.exists():
            pytest.skip("version.yaml not found")

        content = version_file.read_text()
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            pytest.skip("Invalid YAML")

        if "skill" not in data:
            pytest.skip("No skill field")

        skill_name = data["skill"]
        assert skill_name == skill_dir.name, (
            f"version.yaml 'skill' field ({skill_name}) should match "
            f"directory name ({skill_dir.name})"
        )


# =============================================================================
# Tests: README Compliance
# =============================================================================

class TestReadmeCompliance:
    """Test README.md follows documentation standards."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_readme_has_title(self, skill_dir: Path):
        """README.md SHOULD have an H1 title."""
        readme = skill_dir / "README.md"
        if not readme.exists():
            readme = skill_dir / "_dev" / "README.md"
            
        if not readme.exists():
            pytest.skip("README.md not found")

        content = readme.read_text()
        headers = extract_headers(content)
        h1_headers = [h for level, h in headers if level == 1]

        assert len(h1_headers) >= 1, (
            f"README.md in {skill_dir.name} should have an H1 title"
        )

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_readme_not_empty(self, skill_dir: Path):
        """README.md SHOULD have meaningful content."""
        readme = skill_dir / "README.md"
        if not readme.exists():
            readme = skill_dir / "_dev" / "README.md"
            
        if not readme.exists():
            pytest.skip("README.md not found")

        content = readme.read_text().strip()
        min_length = 100  # At least a few paragraphs

        assert len(content) >= min_length, (
            f"README.md in {skill_dir.name} should have meaningful content "
            f"(at least {min_length} characters, got {len(content)})"
        )


# =============================================================================
# Tests: CHANGELOG Compliance
# =============================================================================

class TestChangelogCompliance:
    """Test CHANGELOG.md follows version history standards."""

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=SKILL_IDS)
    def test_changelog_has_version_entries(self, skill_dir: Path):
        """CHANGELOG.md SHOULD have version entries."""
        changelog = skill_dir / "CHANGELOG.md"
        if not changelog.exists():
            changelog = skill_dir / "_dev" / "CHANGELOG.md"
            
        if not changelog.exists():
            pytest.skip("CHANGELOG.md not found")

        content = changelog.read_text()

        # Look for version patterns like [1.0.0], ## 1.0.0, or v1.0.0
        version_pattern = r"(\[?\d+\.\d+\.\d+\]?|v\d+\.\d+\.\d+)"
        versions = re.findall(version_pattern, content)

        assert len(versions) >= 1, (
            f"CHANGELOG.md in {skill_dir.name} should have at least one version entry. "
            f"Per CONTRIBUTING.md format:\n"
            f"## [1.0.0] - 2025-11-25\n"
            f"### Added\n"
            f"- New feature X"
        )


# =============================================================================
# Summary Tests
# =============================================================================

class TestSkillSummary:
    """Summary tests for overall skill ecosystem health."""

    def test_at_least_one_skill_exists(self):
        """Repository MUST have at least one skill."""
        assert len(SKILL_DIRS) > 0, "No skills found in packages/ directory"

    def test_all_skills_have_skill_md(self):
        """All skills MUST have SKILL.md."""
        missing = [
            d.name for d in SKILL_DIRS
            if not (d / "SKILL.md").exists()
        ]
        assert not missing, (
            f"Missing SKILL.md in: {', '.join(missing)}"
        )

    def test_skill_count_summary(self):
        """Report total number of skills (informational)."""
        count = len(SKILL_DIRS)
        print(f"\n  Found {count} skills in packages/")
        # Count compliant skills
        compliant = sum(
            1 for d in SKILL_DIRS
            if all((d / f).exists() or (d / "_dev" / f).exists() for f in REQUIRED_FILES)
        )
        print(f"  {compliant}/{count} have all required files")
