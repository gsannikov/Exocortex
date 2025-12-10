"""
MCP Server for Setup & Maintenance Manager.
"""
import logging
import platform
from pathlib import Path
from typing import Any, Sequence

import mcp.types as types
from mcp.server import Server
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    TextContent,
)

from .config_manager import add_mcp_server, get_config_path
from .discovery import get_skill_details, list_installed_skills
from .maintenance import (
    backup_skill_data,
    clean_logs,
    reset_skill_data,
    update_all_dependencies,
)
from .setup import check_system_requirements, install_package_dependencies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("setup-manager")

# Helper to get default data dir (can be overridden by args if needed, but good default)
def get_default_data_dir() -> Path:
    """Get default data directory using centralized path config."""
    try:
        # Try to import from shared config
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent.parent
        sys.path.insert(0, str(project_root))
        from shared.config.paths import get_user_data_base
        return get_user_data_base()
    except ImportError:
        # Fallback if shared config not available
        if platform.system() == "Windows":
            return Path.home() / "Documents" / "claude-skills-data"
        return Path.home() / "Documents" / "claude-skills-data"

server = Server("setup-manager")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="check_environment",
            description="Check if required system tools (python, uv, npm, git) are installed.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="install_dependencies",
            description="Install dependencies for a specific package or the current project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "package_path": {
                        "type": "string",
                        "description": "Path to the package directory. If omitted, checks system requirements.",
                    }
                },
            },
        ),
        types.Tool(
            name="list_skills",
            description="List all available skills in the packages directory.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="get_skill_guide",
            description="Get detailed usage information for a specific skill.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_id": {
                        "type": "string",
                        "description": "The directory name of the skill (e.g., 'local-rag').",
                    }
                },
                "required": ["skill_id"],
            },
        ),
        types.Tool(
            name="perform_maintenance",
            description="Perform maintenance tasks like log cleanup and dependency updates.",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["clean_logs", "update_deps"],
                        "description": "The maintenance action to perform.",
                    },
                    "target_path": {
                        "type": "string",
                        "description": "Target directory for the action (e.g., log directory or packages root).",
                    }
                },
                "required": ["action"],
            },
        ),
        types.Tool(
            name="get_mcp_config_path",
            description="Get the path to the Claude Desktop configuration file.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="install_mcp_server",
            description="Add or update an MCP server in the Claude Desktop configuration.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the MCP server (key in config).",
                    },
                    "command": {
                        "type": "string",
                        "description": "Executable command to run the server.",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Arguments for the command.",
                    },
                    "env": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                        "description": "Environment variables for the server.",
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Set to true to apply changes. If false (default), returns a diff for review.",
                    }
                },
                "required": ["name", "command", "args"],
            },
        ),
        types.Tool(
            name="backup_skill_data",
            description="Create a zip backup of a skill's data directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_id": {
                        "type": "string",
                        "description": "The ID of the skill to backup.",
                    },
                    "data_dir": {
                        "type": "string",
                        "description": "Root data directory (optional, defaults to standard location).",
                    }
                },
                "required": ["skill_id"],
            },
        ),
        types.Tool(
            name="reset_skill_data",
            description="Reset (wipe and recreate) a skill's data directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_id": {
                        "type": "string",
                        "description": "The ID of the skill to reset.",
                    },
                    "data_dir": {
                        "type": "string",
                        "description": "Root data directory (optional, defaults to standard location).",
                    },
                    "backup": {
                        "type": "boolean",
                        "description": "Create a backup before resetting (default: true).",
                    }
                },
                "required": ["skill_id"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    if name == "check_environment":
        status = check_system_requirements()
        output = "System Requirements Check:\n"
        for tool, installed in status.items():
            icon = "✅" if installed else "❌"
            output += f"{icon} {tool}: {'Installed' if installed else 'Missing'}\n"
        return [types.TextContent(type="text", text=output)]

    elif name == "install_dependencies":
        package_path = arguments.get("package_path")
        if package_path:
            success, msg = install_package_dependencies(Path(package_path))
            return [types.TextContent(type="text", text=f"Result: {msg}")]
        else:
            return [types.TextContent(type="text", text="Please provide a package_path.")]

    elif name == "list_skills":
        skills = list_installed_skills()
        output = "Installed Skills:\n\n"
        for skill in skills:
            output += f"### {skill['name']} (`{skill['id']}`)\n"
            output += f"{skill['description']}\n\n"
        return [types.TextContent(type="text", text=output)]

    elif name == "get_skill_guide":
        skill_id = arguments.get("skill_id")
        details = get_skill_details(skill_id)
        if details:
            output = f"# Guide for {skill_id}\n\n"
            if details['skill_def']:
                output += "## Skill Definition\n" + details['skill_def'] + "\n\n"
            if details['readme']:
                output += "## README\n" + details['readme']
            return [types.TextContent(type="text", text=output)]
        else:
            return [types.TextContent(type="text", text=f"Skill '{skill_id}' not found.")]

    elif name == "perform_maintenance":
        action = arguments.get("action")
        target_path = arguments.get("target_path")
        
        if action == "clean_logs":
            if not target_path:
                return [types.TextContent(type="text", text="Error: target_path required for clean_logs")]
            removed, freed = clean_logs(Path(target_path))
            return [types.TextContent(type="text", text=f"Logs cleaned. Removed {removed} files, freed {freed} bytes.")]
            
        elif action == "update_deps":
            if not target_path:
                # Default to packages dir relative to this file
                target_path = Path(__file__).parent.parent.parent
            else:
                target_path = Path(target_path)
                
            results = update_all_dependencies(target_path)
            return [types.TextContent(type="text", text="Dependency Updates:\n" + "\n".join(results))]
            
        return [types.TextContent(type="text", text=f"Unknown action: {action}")]

    elif name == "get_mcp_config_path":
        path = get_config_path()
        return [types.TextContent(type="text", text=str(path))]

    elif name == "install_mcp_server":
        server_name = arguments.get("name")
        command = arguments.get("command")
        args = arguments.get("args")
        env = arguments.get("env")
        confirm = arguments.get("confirm", False)
        
        success, msg = add_mcp_server(
            name=server_name,
            command=command,
            args=args,
            env=env,
            preview_only=not confirm
        )
        
        return [types.TextContent(type="text", text=msg)]

    elif name == "backup_skill_data":
        skill_id = arguments.get("skill_id")
        data_dir_str = arguments.get("data_dir")
        data_dir = Path(data_dir_str) if data_dir_str else get_default_data_dir()
        
        success, msg = backup_skill_data(skill_id, data_dir)
        return [types.TextContent(type="text", text=msg)]

    elif name == "reset_skill_data":
        skill_id = arguments.get("skill_id")
        data_dir_str = arguments.get("data_dir")
        backup = arguments.get("backup", True)
        data_dir = Path(data_dir_str) if data_dir_str else get_default_data_dir()
        
        success, msg = reset_skill_data(skill_id, data_dir, backup=backup)
        return [types.TextContent(type="text", text=msg)]

    raise ValueError(f"Unknown tool: {name}")

def main():
    # Run the server using stdin/stdout
    import asyncio

    from mcp.server.stdio import stdio_server

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    asyncio.run(run())

if __name__ == "__main__":
    main()
