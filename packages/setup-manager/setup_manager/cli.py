"""
Interactive CLI for Setup & Maintenance Manager.
Replaces the root setup.py script.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add package root to path to allow imports if run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from setup_manager.config_manager import add_mcp_server, get_config_path
from setup_manager.maintenance import backup_skill_data, reset_skill_data
from setup_manager.setup import check_system_requirements, install_package_dependencies
from setup_manager.utils import (
    Colors,
    print_error,
    print_header,
    print_info,
    print_section,
    print_success,
    print_warning,
    prompt_yes_no,
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

PACKAGE_ROOT = Path(__file__).parent.parent
DATA_DIR = PACKAGE_ROOT / "data"
MARKETPLACE_FILE = DATA_DIR / "marketplace.json"

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def load_marketplace_data() -> Dict[str, Any]:
    """Load skill definitions from marketplace.json."""
    if not MARKETPLACE_FILE.exists():
        return {"plugins": []}
    try:
        with open(MARKETPLACE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print_error(f"Failed to load marketplace data: {e}")
        return {"plugins": []}

# ═══════════════════════════════════════════════════════════════════════════════
# CORE LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def check_prerequisites() -> bool:
    """Check system requirements."""
    print_section("Checking Prerequisites")
    reqs = check_system_requirements()
    all_ok = True
    for tool, installed in reqs.items():
        if installed:
            print_success(f"{tool} is installed")
        else:
            print_warning(f"{tool} is missing")
            all_ok = False
    return all_ok

def setup_data_directories(skills_data_path: Path, skills: List[Dict]):
    """Create data directories for skills."""
    print_section("Creating Data Directories")
    
    # Ensure main data dir exists
    skills_data_path.mkdir(parents=True, exist_ok=True)
    print_success(f"Main data directory: {skills_data_path}")

    # Create subdirectories based on skill needs
    # TODO: Move this config to marketplace.json metadata
    dir_map = {
        "career-consultant": ["profile", "companies", "jobs", "jobs/analyzed", "reports"],
        "reading-list": ["summaries"],
        "ideas-capture": ["expanded"],
        "voice-memos": ["transcripts", "analyzed"],
        "local-rag": ["chromadb", "state", "logs"],
    }

    for skill in skills:
        skill_id = skill.get("name")
        if skill_id in dir_map:
            skill_path = skills_data_path / skill_id
            skill_path.mkdir(parents=True, exist_ok=True)
            for subdir in dir_map[skill_id]:
                (skill_path / subdir).mkdir(parents=True, exist_ok=True)
            print_success(f"Created directories for {skill_id}")

def install_mcp_servers(skills: List[Dict], project_root: Path):
    """Configure MCP servers for skills."""
    print_section("Configuring MCP Servers")
    
    for skill in skills:
        skill_id = skill.get("name")
        mcp_config = skill.get("mcp")
        
        if mcp_config:
            # Resolve absolute paths in args
            # We assume paths starting with "packages/" are relative to project root
            args = []
            for arg in mcp_config.get("args", []):
                if arg.startswith("packages/"):
                    args.append(str(project_root / arg))
                else:
                    args.append(arg)
            
            # Special handling for local-rag python path if needed
            cmd = mcp_config.get("command")
            env = mcp_config.get("env", {}).copy()
            
            if skill_id == "local-rag" and cmd == "python3":
                # Use venv python if available
                venv_python = project_root / ".venv" / "bin" / "python"
                if venv_python.exists():
                    cmd = str(venv_python)
                else:
                    cmd = sys.executable
                
                # Add project root to PYTHONPATH
                env["PYTHONPATH"] = str(project_root / "packages" / "local-rag")
            
            success, msg = add_mcp_server(
                name=skill_id,
                command=cmd,
                args=args,
                env=env,
                preview_only=False
            )
            
            if success:
                print_success(f"Configured MCP server for {skill_id}")
            else:
                print_error(f"Failed to configure {skill_id}: {msg}")

def manage_data(skills_data_path: Path, skills: List[Dict]):
    """Interactive data management menu."""
    print_header("Manage Skill Data")
    
    print("Available Skills:")
    for i, skill in enumerate(skills, 1):
        print(f"  {i}. {skill['name']}")
        
    print("\nActions:")
    print("  b. Backup Data")
    print("  r. Reset Data (Wipe & Recreate)")
    print("  q. Back to Main Menu")
    
    choice = input("\nSelect action (b/r/q): ").strip().lower()
    
    if choice == 'q':
        return
        
    if choice in ('b', 'r'):
        try:
            skill_idx = int(input("Select skill number: ").strip()) - 1
            if 0 <= skill_idx < len(skills):
                skill = skills[skill_idx]
                skill_id = skill['name']
                
                if choice == 'b':
                    print_info(f"Backing up {skill_id}...")
                    success, msg = backup_skill_data(skill_id, skills_data_path)
                    if success:
                        print_success(msg)
                    else:
                        print_error(msg)
                        
                elif choice == 'r':
                    print_warning(f"This will DELETE all data for {skill_id}!")
                    if prompt_yes_no("Are you sure?", default=False):
                        print_info(f"Resetting {skill_id}...")
                        success, msg = reset_skill_data(skill_id, skills_data_path, backup=True)
                        if success:
                            print_success(msg)
                        else:
                            print_error(msg)
            else:
                print_error("Invalid skill number")
        except ValueError:
            print_error("Invalid input")

def run_setup(args):
    """Main setup flow."""
    print_header("Claude Skills Setup")
    
    # Determine paths using centralized config
    project_root = Path(__file__).parent.parent.parent.parent
    try:
        sys.path.insert(0, str(project_root))
        from shared.config.paths import get_user_data_base
        skills_data_path = get_user_data_base()
    except ImportError:
        # Fallback if shared config not available
        skills_data_path = Path.home() / "Documents" / "claude-skills-data"
    
    print_info(f"Project Root: {project_root}")
    print_info(f"Data Directory: {skills_data_path}")

    # Load skills
    marketplace = load_marketplace_data()
    skills = marketplace.get("plugins", [])
    print_info(f"Found {len(skills)} skills in marketplace definition")
    
    while True:
        print_header("Main Menu")
        print("1. Full Setup (Prerequisites, Data Dirs, Deps, MCP)")
        print("2. Manage Data (Backup / Reset)")
        print("3. Check System Status")
        print("q. Quit")
        
        choice = input("\nSelect option: ").strip().lower()
        
        if choice == 'q':
            break
            
        elif choice == '1':
            # 1. Check Prerequisites
            if not check_prerequisites():
                if not prompt_yes_no("Some prerequisites are missing. Continue?", default=False):
                    continue

            # 2. Setup Data Directories
            setup_data_directories(skills_data_path, skills)

            # 3. Install Dependencies
            print_section("Installing Dependencies")
            install_package_dependencies(project_root / "packages" / "setup-manager")
            
            for skill in skills:
                skill_path = project_root / skill.get("source", "").lstrip("./")
                if skill_path.exists():
                    print_info(f"Installing dependencies for {skill['name']}...")
                    success, msg = install_package_dependencies(skill_path)
                    if success:
                        print_success(f"{skill['name']}: Installed")
                    else:
                        print_warning(f"{skill['name']}: {msg}")

            # 4. Configure MCP
            if prompt_yes_no("Configure MCP servers in Claude Desktop?", default=True):
                install_mcp_servers(skills, project_root)
                
            print_success("Setup complete!")
            
        elif choice == '2':
            manage_data(skills_data_path, skills)
            
        elif choice == '3':
            run_check(args)
            
    return True

def run_check(args):
    """Status check."""
    print_header("System Status Check")
    check_prerequisites()
    
    config_path = get_config_path()
    if config_path.exists():
        print_success(f"Claude Config found at: {config_path}")
    else:
        print_warning("Claude Config not found")
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Claude Skills Setup & Manager")
    parser.add_argument("--check", action="store_true", help="Check system status")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
        
    if args.check:
        run_check(args)
    else:
        run_setup(args)

if __name__ == "__main__":
    main()
