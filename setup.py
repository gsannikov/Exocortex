#!/usr/bin/env python3
"""
Claude Skills Setup Script

Automated first-time setup for Claude Skills ecosystem.
Downloads, configures, and integrates skills with Claude Desktop.

Usage:
    python setup.py              # Interactive setup
    python setup.py --check      # Check installation status only
    python setup.py --uninstall  # Remove skills and configs
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SKILLS = {
    "career-consultant": {
        "name": "Career Consultant",
        "emoji": "📋",
        "inbox": "Job Links Inbox",
        "commands": [
            "process inbox",
            "Add to backlog: [url]",
            "Analyze: [url]",
            "Show my backlog",
            "Mark [job-id] as Applied",
        ],
        "requires_mcp": False,
    },
    "reading-list": {
        "name": "Reading List",
        "emoji": "📚",
        "inbox": "Reading List Inbox",
        "commands": [
            "process reading list",
            "show unread",
            "show reading list",
            "search: [query]",
            "mark read: [title]",
        ],
        "requires_mcp": False,
    },
    "ideas-capture": {
        "name": "Ideas Capture",
        "emoji": "💡",
        "inbox": "Ideas Inbox",
        "commands": [
            "process ideas",
            "show ideas",
            "expand: [idea]",
            "evaluate: [idea]",
            "link ideas: [A] + [B]",
        ],
        "requires_mcp": False,
    },
    "voice-memos": {
        "name": "Voice Memos",
        "emoji": "🎙️",
        "inbox": "Voice Memos Inbox",
        "commands": [
            "process voice memos",
            "transcribe [file]",
            "show transcripts",
            "show pending memos",
            "search memos: [query]",
        ],
        "requires_mcp": False,
    },
    "local-rag": {
        "name": "Local RAG",
        "emoji": "🔍",
        "inbox": None,
        "commands": [
            "update rag from [path]",
            "query rag [question]",
            "search documents [query]",
        ],
        "requires_mcp": True,
        "mcp_config": {
            "command": "python",
            "args": ["-u", "mcp_server.py"],
            "env": {"PYTHONUNBUFFERED": "1"},
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS AND FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════


class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @classmethod
    def disable(cls):
        """Disable colors for non-terminal output."""
        cls.HEADER = ""
        cls.BLUE = ""
        cls.CYAN = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.RED = ""
        cls.BOLD = ""
        cls.DIM = ""
        cls.RESET = ""


# Disable colors if not a terminal
if not sys.stdout.isatty():
    Colors.disable()


def print_header(text: str):
    """Print a styled header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}\n")


def print_section(text: str):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {text}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLATFORM DETECTION
# ═══════════════════════════════════════════════════════════════════════════════


def get_platform_info() -> dict:
    """Detect OS and relevant paths."""
    system = platform.system().lower()
    home = Path.home()

    info = {
        "system": system,
        "home": home,
        "claude_desktop_path": None,
        "claude_config_path": None,
        "skills_data_path": home / "MyDrive" / "claude-skills-data",
        "skills_code_path": Path(__file__).parent.resolve(),
    }

    if system == "darwin":  # macOS
        info["claude_desktop_path"] = Path("/Applications/Claude.app")
        info["claude_config_path"] = home / ".config" / "Claude" / "claude_desktop_config.json"
        # Alternative location for Claude commands
        info["claude_commands_path"] = home / ".claude" / "commands"
    elif system == "linux":
        # Check common Linux installation paths
        possible_paths = [
            Path("/usr/bin/claude"),
            Path("/usr/local/bin/claude"),
            home / ".local" / "bin" / "claude",
            Path("/opt/Claude"),
        ]
        for path in possible_paths:
            if path.exists():
                info["claude_desktop_path"] = path
                break
        info["claude_config_path"] = home / ".config" / "Claude" / "claude_desktop_config.json"
        info["claude_commands_path"] = home / ".claude" / "commands"
    elif system == "windows":
        appdata = os.environ.get("APPDATA", "")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            info["claude_desktop_path"] = Path(localappdata) / "Programs" / "Claude" / "Claude.exe"
        if appdata:
            info["claude_config_path"] = Path(appdata) / "Claude" / "claude_desktop_config.json"
            info["claude_commands_path"] = Path(appdata) / "Claude" / "commands"
        # Windows uses different data path
        info["skills_data_path"] = home / "Documents" / "claude-skills-data"

    return info


def check_claude_desktop(info: dict) -> bool:
    """Check if Claude Desktop is installed."""
    path = info.get("claude_desktop_path")
    if path and path.exists():
        return True

    # Try running claude command
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════


def load_claude_config(config_path: Path) -> dict:
    """Load existing Claude Desktop config or create empty structure."""
    if config_path and config_path.exists():
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print_warning(f"Invalid JSON in {config_path}, will create backup")
            backup_path = config_path.with_suffix(".json.backup")
            shutil.copy(config_path, backup_path)
            print_info(f"Backup created: {backup_path}")

    return {"mcpServers": {}}


def save_claude_config(config_path: Path, config: dict) -> bool:
    """Save Claude Desktop config."""
    try:
        # Ensure parent directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print_error(f"Failed to save config: {e}")
        return False


def update_mcp_config(config: dict, skills_path: Path) -> dict:
    """Add/update MCP server configurations for skills that need them."""
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    for skill_id, skill_info in SKILLS.items():
        if skill_info.get("requires_mcp"):
            mcp_config = skill_info["mcp_config"].copy()

            # Update the path to mcp_server.py to be absolute
            skill_path = skills_path / "packages" / skill_id
            mcp_server_path = skill_path / "mcp_server.py"

            if mcp_server_path.exists():
                mcp_config["args"] = ["-u", str(mcp_server_path)]
                # Also set cwd for the MCP server
                mcp_config["cwd"] = str(skill_path)
                config["mcpServers"][skill_id] = mcp_config
                print_success(f"Added MCP config for {skill_info['name']}")
            else:
                print_warning(f"MCP server not found for {skill_info['name']}: {mcp_server_path}")

    return config


# ═══════════════════════════════════════════════════════════════════════════════
# SKILL INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════


def create_data_directories(data_path: Path) -> bool:
    """Create user data directories for all skills."""
    print_section("Creating Data Directories")

    directories = {
        "career-consultant": ["profile", "companies", "jobs", "jobs/analyzed", "reports"],
        "reading-list": ["summaries"],
        "ideas-capture": ["expanded"],
        "voice-memos": ["transcripts", "analyzed"],
        "local-rag": ["chromadb", "state"],
    }

    try:
        for skill_id, subdirs in directories.items():
            skill_data_path = data_path / skill_id
            skill_data_path.mkdir(parents=True, exist_ok=True)

            for subdir in subdirs:
                (skill_data_path / subdir).mkdir(parents=True, exist_ok=True)

            print_success(f"Created directories for {skill_id}")

        return True
    except Exception as e:
        print_error(f"Failed to create directories: {e}")
        return False


def install_slash_commands(commands_path: Path, skills_path: Path) -> bool:
    """Install skill slash commands for Claude CLI."""
    print_section("Installing Slash Commands")

    try:
        commands_path.mkdir(parents=True, exist_ok=True)

        # Create slash commands that load skill SKILL.md files
        for skill_id, skill_info in SKILLS.items():
            skill_md_path = skills_path / "packages" / skill_id / "SKILL.md"
            if skill_md_path.exists():
                command_file = commands_path / f"{skill_id}.md"

                # Create a command that instructs Claude to load the skill
                command_content = f"""Load and execute the {skill_info['name']} skill.

Read the skill specification from: {skill_md_path}

Then follow the instructions in that file to help the user.
"""
                with open(command_file, "w") as f:
                    f.write(command_content)

                print_success(f"Created /{skill_id} command")

        return True
    except Exception as e:
        print_error(f"Failed to install slash commands: {e}")
        return False


def check_python_dependencies(skills_path: Path) -> dict:
    """Check if required Python dependencies are installed."""
    print_section("Checking Python Dependencies")

    results = {}

    # Check for local-rag dependencies
    local_rag_path = skills_path / "packages" / "local-rag"
    requirements_file = local_rag_path / "requirements.txt"

    if requirements_file.exists():
        print_info("Local RAG requires additional Python packages")
        with open(requirements_file, "r") as f:
            deps = [line.strip().split(">=")[0].split("==")[0] for line in f if line.strip() and not line.startswith("#")]

        missing = []
        for dep in deps:
            try:
                __import__(dep.replace("-", "_"))
            except ImportError:
                missing.append(dep)

        results["local-rag"] = {"required": deps, "missing": missing}

        if missing:
            print_warning(f"Missing packages for Local RAG: {', '.join(missing)}")
            print_info(f"Install with: pip install -r {requirements_file}")
        else:
            print_success("All Local RAG dependencies installed")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# USER INTERACTION
# ═══════════════════════════════════════════════════════════════════════════════


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """Prompt user for yes/no answer."""
    default_str = "Y/n" if default else "y/N"
    answer = input(f"{question} [{default_str}]: ").strip().lower()

    if not answer:
        return default
    return answer in ("y", "yes")


def display_commands():
    """Display all available commands from all skills."""
    print_section("Available Commands")

    for skill_id, skill_info in SKILLS.items():
        emoji = skill_info["emoji"]
        name = skill_info["name"]
        inbox = skill_info.get("inbox")

        print(f"\n{Colors.BOLD}{emoji} {name}{Colors.RESET}")
        if inbox:
            print(f"   {Colors.DIM}Apple Note: {inbox}{Colors.RESET}")

        print(f"   {Colors.DIM}Commands:{Colors.RESET}")
        for cmd in skill_info["commands"]:
            print(f"     • {cmd}")


def display_apple_notes_setup():
    """Display Apple Notes inbox setup instructions."""
    print_section("Apple Notes Setup")

    print(f"""
For skills that use Apple Notes, create inbox notes with this structure:

{Colors.DIM}┌─────────────────────────────────────────────┐
│ [Emoji] [Skill Name] Inbox                  │
│                                             │
│ ADD BELOW                                   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│                                             │
│ [Your items here]                           │
│                                             │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│ PROCESSED                                   │
│                                             │
│ [Stats will appear here]                    │
└─────────────────────────────────────────────┘{Colors.RESET}

Required Notes:
""")

    for skill_id, skill_info in SKILLS.items():
        inbox = skill_info.get("inbox")
        if inbox:
            emoji = skill_info["emoji"]
            print(f"  • {emoji} {inbox}")


def display_status(info: dict):
    """Display current installation status."""
    print_section("Installation Status")

    # Claude Desktop
    if check_claude_desktop(info):
        print_success("Claude Desktop: Installed")
    else:
        print_warning("Claude Desktop: Not found")

    # Config file
    config_path = info.get("claude_config_path")
    if config_path and config_path.exists():
        print_success(f"Config file: {config_path}")
        config = load_claude_config(config_path)
        mcp_servers = config.get("mcpServers", {})
        if mcp_servers:
            print_info(f"  MCP Servers configured: {', '.join(mcp_servers.keys())}")
    else:
        print_warning(f"Config file: Not found ({config_path})")

    # Data directory
    data_path = info.get("skills_data_path")
    if data_path and data_path.exists():
        print_success(f"Data directory: {data_path}")
        existing = [d.name for d in data_path.iterdir() if d.is_dir()]
        if existing:
            print_info(f"  Skills with data: {', '.join(existing)}")
    else:
        print_warning(f"Data directory: Not found ({data_path})")

    # Skills code
    skills_path = info.get("skills_code_path")
    packages_path = skills_path / "packages"
    if packages_path.exists():
        print_success(f"Skills code: {skills_path}")
        skills = [d.name for d in packages_path.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        if skills:
            print_info(f"  Available skills: {', '.join(skills)}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN SETUP FLOW
# ═══════════════════════════════════════════════════════════════════════════════


def run_setup():
    """Run the complete setup process."""
    print_header("Claude Skills Setup")

    # Detect platform and paths
    info = get_platform_info()
    print_info(f"Platform: {info['system']}")
    print_info(f"Skills location: {info['skills_code_path']}")

    # Step 1: Check Claude Desktop
    print_section("Step 1: Checking Claude Desktop")

    claude_installed = check_claude_desktop(info)
    if claude_installed:
        print_success("Claude Desktop is installed")
    else:
        print_warning("Claude Desktop not detected")
        print_info("You can still set up skills, but some features may not work")
        print_info("Download Claude Desktop from: https://claude.ai/download")

        if not prompt_yes_no("Continue anyway?", default=True):
            print_info("Setup cancelled")
            return False

    # Display what will be done
    print_section("Step 2: Review Installation Plan")

    print(f"""
The setup will perform the following actions:

  1. Create data directories at:
     {Colors.CYAN}{info['skills_data_path']}{Colors.RESET}

  2. Update Claude Desktop config at:
     {Colors.CYAN}{info.get('claude_config_path', 'N/A')}{Colors.RESET}
     - Add MCP server for Local RAG skill

  3. Check Python dependencies for Local RAG
""")

    display_commands()

    # Ask permission
    print_section("Step 3: Confirm Installation")

    if not prompt_yes_no("Proceed with installation?", default=True):
        print_info("Setup cancelled")
        return False

    # Step 4: Create data directories
    print_section("Step 4: Setting Up Data Directories")

    if not create_data_directories(info["skills_data_path"]):
        print_error("Failed to create data directories")
        return False

    # Step 5: Update Claude config
    print_section("Step 5: Updating Claude Configuration")

    config_path = info.get("claude_config_path")
    if config_path:
        config = load_claude_config(config_path)
        config = update_mcp_config(config, info["skills_code_path"])

        if save_claude_config(config_path, config):
            print_success(f"Updated config: {config_path}")
        else:
            print_warning("Could not update Claude config (will need manual setup)")
    else:
        print_warning("Claude config path not found")

    # Step 6: Install slash commands (optional)
    print_section("Step 6: Optional - Slash Commands")

    commands_path = info.get("claude_commands_path")
    if commands_path:
        if prompt_yes_no("Install slash commands for Claude CLI?", default=True):
            install_slash_commands(commands_path, info["skills_code_path"])

    # Step 7: Check dependencies
    check_python_dependencies(info["skills_code_path"])

    # Done!
    print_header("Setup Complete!")

    print(f"""
{Colors.GREEN}Claude Skills has been set up successfully!{Colors.RESET}

{Colors.BOLD}Next Steps:{Colors.RESET}

  1. Restart Claude Desktop to load new MCP servers

  2. Create Apple Notes inboxes (see below)

  3. Start using skills with commands like:
     • "process inbox" (Career Consultant)
     • "process reading list" (Reading List)
     • "process ideas" (Ideas Capture)
     • "update rag from ~/Documents" (Local RAG)
""")

    display_apple_notes_setup()

    print(f"""
{Colors.BOLD}Documentation:{Colors.RESET}
  • User Guide: {info['skills_code_path']}/USER_GUIDE.md
  • Developer Guide: {info['skills_code_path']}/DEVELOPER_GUIDE.md

{Colors.DIM}Happy productivity!{Colors.RESET}
""")

    return True


def run_check():
    """Check installation status only."""
    print_header("Claude Skills Status Check")

    info = get_platform_info()
    display_status(info)
    display_commands()

    return True


def run_uninstall():
    """Uninstall skills and configurations."""
    print_header("Claude Skills Uninstall")

    info = get_platform_info()

    print_warning("This will remove:")
    print(f"  • MCP server configurations from Claude Desktop config")
    print(f"  • Slash commands from {info.get('claude_commands_path', 'N/A')}")
    print()
    print_info("Your data will NOT be deleted:")
    print(f"  • {info['skills_data_path']}")

    if not prompt_yes_no("Proceed with uninstall?", default=False):
        print_info("Uninstall cancelled")
        return False

    # Remove MCP configs
    config_path = info.get("claude_config_path")
    if config_path and config_path.exists():
        config = load_claude_config(config_path)
        for skill_id in SKILLS:
            if skill_id in config.get("mcpServers", {}):
                del config["mcpServers"][skill_id]
                print_success(f"Removed MCP config for {skill_id}")

        save_claude_config(config_path, config)

    # Remove slash commands
    commands_path = info.get("claude_commands_path")
    if commands_path and commands_path.exists():
        for skill_id in SKILLS:
            cmd_file = commands_path / f"{skill_id}.md"
            if cmd_file.exists():
                cmd_file.unlink()
                print_success(f"Removed /{skill_id} command")

    print_header("Uninstall Complete")
    print_info(f"Your data is preserved at: {info['skills_data_path']}")
    print_info("Delete it manually if you want to remove all data")

    return True


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Claude Skills Setup - Automated installation and configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup.py              # Interactive setup
  python setup.py --check      # Check installation status
  python setup.py --uninstall  # Remove skills and configs

For more information, see USER_GUIDE.md
""",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check installation status only",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove skills and configurations",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    try:
        if args.check:
            success = run_check()
        elif args.uninstall:
            success = run_uninstall()
        else:
            success = run_setup()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if os.environ.get("DEBUG"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
