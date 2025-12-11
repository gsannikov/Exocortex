#!/usr/bin/env python3
"""
Exocortex MCP Server

Exposes Claude skills through MCP protocol for use with any LLM platform.
Implements lazy loading for token optimization and self-update capabilities.
"""

import json
import logging
import re
import shutil
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

# Configuration
SKILLS_DIR = Path(__file__).parent.parent.parent  # packages/
BACKUP_DIR = Path.home() / "exocortex-data" / "mcp-backups"
DATA_DIR = Path.home() / "exocortex-data"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("exocortex-mcp")

# Initialize MCP Server
mcp = FastMCP("exocortex_mcp")


# =============================================================================
# Pydantic Models
# =============================================================================

class ResponseFormat(str, Enum):
    """Output format for responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class ListSkillsInput(BaseModel):
    """Input for listing available skills."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    format: ResponseFormat = Field(
        default=ResponseFormat.JSON,
        description="Output format: 'json' for compact, 'markdown' for readable"
    )


class GetSkillInput(BaseModel):
    """Input for getting skill overview."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    skill_name: str = Field(
        ..., 
        description="Name of the skill (e.g., 'job-analyzer', 'recipe-manager')",
        min_length=1,
        max_length=50
    )
    include_modules: bool = Field(
        default=False,
        description="Include module list in response"
    )


class LoadModuleInput(BaseModel):
    """Input for loading a specific module."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    skill_name: str = Field(..., description="Parent skill name", min_length=1)
    module_name: str = Field(..., description="Module filename without .md extension", min_length=1)


class LoadReferenceInput(BaseModel):
    """Input for loading reference documentation."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    skill_name: str = Field(..., description="Parent skill name", min_length=1)
    reference_name: str = Field(..., description="Reference filename without .md extension", min_length=1)


class UpdateModuleInput(BaseModel):
    """Input for updating a module (self-update capability)."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    skill_name: str = Field(..., description="Parent skill name", min_length=1)
    module_name: str = Field(..., description="Module to update", min_length=1)
    content: str = Field(..., description="New module content in markdown", min_length=10)
    reason: str = Field(..., description="Reason for the update", min_length=5, max_length=200)


class SkillActionInput(BaseModel):
    """Input for executing a skill action."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    skill_name: str = Field(..., description="Skill to use", min_length=1)
    action: str = Field(..., description="Action/command to execute", min_length=1)
    params: dict = Field(default_factory=dict, description="Action parameters")


# =============================================================================
# Helper Functions  
# =============================================================================

def parse_skill_header(skill_path: Path) -> dict:
    """Parse SKILL.md frontmatter for minimal metadata."""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None
    
    content = skill_file.read_text()
    
    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            name = ""
            description = ""
            triggers = []
            
            for line in frontmatter.split("\n"):
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("description:"):
                    desc_text = line.split(":", 1)[1].strip()
                    description = desc_text
                    # Extract triggers from description
                    if "Triggers" in desc_text:
                        trigger_part = desc_text.split("Triggers")[-1]
                        triggers = re.findall(r'"([^"]+)"', trigger_part)
            
            # Estimate tokens (rough: ~4 chars per token)
            token_estimate = len(content) // 4
            
            return {
                "name": name or skill_path.name,
                "description": description[:200] + "..." if len(description) > 200 else description,
                "triggers": triggers[:5],  # Top 5 triggers
                "token_estimate": token_estimate,
                "has_modules": (skill_path / "modules").exists(),
                "has_scripts": (skill_path / "scripts").exists(),
                "has_references": (skill_path / "references").exists(),
            }
    
    return None


def list_modules(skill_path: Path) -> list[str]:
    """List available modules for a skill."""
    modules_dir = skill_path / "modules"
    if not modules_dir.exists():
        return []
    return [f.stem for f in modules_dir.glob("*.md")]


def list_references(skill_path: Path) -> list[str]:
    """List available references for a skill."""
    refs_dir = skill_path / "references"
    if not refs_dir.exists():
        return []
    return [f.stem for f in refs_dir.glob("*.md")]


def backup_file(file_path: Path) -> Path:
    """Create timestamped backup of a file."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"{file_path.stem}_{timestamp}{file_path.suffix}"
    shutil.copy(file_path, backup_path)
    return backup_path


# =============================================================================
# MCP Tools
# =============================================================================

@mcp.tool(
    name="exocortex_list_skills",
    annotations={
        "title": "List Available Skills",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_skills(params: ListSkillsInput) -> str:
    """List all available exocortex skills with minimal metadata.
    
    Returns skill names, trigger phrases, and token estimates.
    Use this first to discover which skill to use for a task.
    
    Args:
        params: ListSkillsInput with format preference
        
    Returns:
        str: JSON or markdown list of available skills
    """
    skills = []
    
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            # Skip the MCP package itself
            if skill_dir.name == "exocortex-mcp":
                continue
            
            skill_info = parse_skill_header(skill_dir)
            if skill_info:
                skills.append(skill_info)
    
    if params.format == ResponseFormat.JSON:
        return json.dumps({"skills": skills, "count": len(skills)}, indent=2)
    
    # Markdown format
    lines = ["# Available Exocortex Skills\n"]
    for s in skills:
        lines.append(f"## {s['name']}")
        lines.append(f"**Triggers**: {', '.join(s['triggers']) if s['triggers'] else 'N/A'}")
        lines.append(f"**Tokens**: ~{s['token_estimate']}")
        lines.append(f"_{s['description']}_\n")
    
    return "\n".join(lines)


@mcp.tool(
    name="exocortex_get_skill",
    annotations={
        "title": "Get Skill Overview",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_skill(params: GetSkillInput) -> str:
    """Load a skill's SKILL.md overview and command reference.
    
    Returns the full skill documentation without loading modules.
    Use this to understand commands before executing actions.
    
    Args:
        params: GetSkillInput with skill_name and optional include_modules
        
    Returns:
        str: Skill documentation in markdown
    """
    skill_path = SKILLS_DIR / params.skill_name
    skill_file = skill_path / "SKILL.md"
    
    if not skill_file.exists():
        available = [d.name for d in SKILLS_DIR.iterdir() 
                     if d.is_dir() and (d / "SKILL.md").exists()]
        return f"Error: Skill '{params.skill_name}' not found.\nAvailable: {', '.join(available)}"
    
    content = skill_file.read_text()
    
    if params.include_modules:
        modules = list_modules(skill_path)
        references = list_references(skill_path)
        
        content += "\n\n---\n## Available Modules\n"
        if modules:
            content += "Load these for detailed workflows:\n"
            for m in modules:
                content += f"- `{m}`\n"
        else:
            content += "_No modules available_\n"
        
        content += "\n## Available References\n"
        if references:
            for r in references:
                content += f"- `{r}`\n"
        else:
            content += "_No references available_\n"
    
    return content


@mcp.tool(
    name="exocortex_load_module",
    annotations={
        "title": "Load Skill Module",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def load_module(params: LoadModuleInput) -> str:
    """Load a specific module's detailed documentation.
    
    Modules contain specialized workflows, formulas, and procedures.
    Only load modules when you need their specific functionality.
    
    Args:
        params: LoadModuleInput with skill_name and module_name
        
    Returns:
        str: Module content in markdown
    """
    module_path = SKILLS_DIR / params.skill_name / "modules" / f"{params.module_name}.md"
    
    if not module_path.exists():
        available = list_modules(SKILLS_DIR / params.skill_name)
        return f"Error: Module '{params.module_name}' not found.\nAvailable: {', '.join(available) or 'none'}"
    
    content = module_path.read_text()
    return f"# Module: {params.module_name}\n\n{content}"


@mcp.tool(
    name="exocortex_load_reference",
    annotations={
        "title": "Load Reference Documentation",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def load_reference(params: LoadReferenceInput) -> str:
    """Load reference documentation for a skill.
    
    References contain setup guides, examples, and background info.
    
    Args:
        params: LoadReferenceInput with skill_name and reference_name
        
    Returns:
        str: Reference content in markdown
    """
    ref_path = SKILLS_DIR / params.skill_name / "references" / f"{params.reference_name}.md"
    
    if not ref_path.exists():
        available = list_references(SKILLS_DIR / params.skill_name)
        return f"Error: Reference '{params.reference_name}' not found.\nAvailable: {', '.join(available) or 'none'}"
    
    return ref_path.read_text()


@mcp.tool(
    name="exocortex_update_module",
    annotations={
        "title": "Update Skill Module (Self-Update)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def update_module(params: UpdateModuleInput) -> str:
    """Update a module's content with automatic backup.
    
    Enables self-improvement: update modules based on conversation learnings.
    Creates backup before modification. SKILL.md is protected (read-only).
    
    Args:
        params: UpdateModuleInput with skill_name, module_name, content, reason
        
    Returns:
        str: JSON result with status and backup path
    """
    skill_path = SKILLS_DIR / params.skill_name
    module_path = skill_path / "modules" / f"{params.module_name}.md"
    
    # Validate skill exists
    if not skill_path.exists():
        return json.dumps({"status": "error", "message": f"Skill '{params.skill_name}' not found"})
    
    # Create modules dir if needed
    modules_dir = skill_path / "modules"
    modules_dir.mkdir(exist_ok=True)
    
    # Backup existing file
    backup_path = None
    if module_path.exists():
        backup_path = backup_file(module_path)
    
    # Write new content with update metadata
    header = f"""---
updated: {datetime.now().isoformat()}
reason: {params.reason}
---

"""
    module_path.write_text(header + params.content)
    
    # Log the update
    log_path = DATA_DIR / "mcp-updates.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {params.skill_name}/{params.module_name} | {params.reason}\n")
    
    return json.dumps({
        "status": "success",
        "skill": params.skill_name,
        "module": params.module_name,
        "backup": str(backup_path) if backup_path else None,
        "message": f"Module updated. Backup: {backup_path}"
    }, indent=2)


@mcp.tool(
    name="exocortex_skill_action",
    annotations={
        "title": "Execute Skill Action",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def skill_action(params: SkillActionInput) -> str:
    """Execute a skill action/command.
    
    Interprets action and returns guidance or executes if script available.
    Use after loading the skill overview to understand commands.
    
    Args:
        params: SkillActionInput with skill_name, action, and params dict
        
    Returns:
        str: Action result with suggested next modules
    """
    skill_path = SKILLS_DIR / params.skill_name
    
    if not skill_path.exists():
        return json.dumps({"status": "error", "message": f"Skill '{params.skill_name}' not found"})
    
    # Check for executable script
    scripts_dir = skill_path / "scripts"
    action_script = scripts_dir / f"{params.action.replace(' ', '_')}.py"
    
    result = {
        "skill": params.skill_name,
        "action": params.action,
        "params": params.params,
        "script_available": action_script.exists(),
        "suggested_modules": [],
        "guidance": ""
    }
    
    # Suggest relevant modules based on action keywords
    modules = list_modules(skill_path)
    action_lower = params.action.lower()
    
    module_keywords = {
        "scoring": ["score", "analyze", "rate", "evaluate"],
        "company-research": ["company", "research", "investigate"],
        "skills-matching": ["match", "skills", "cv", "resume"],
        "linkedin-tracking": ["linkedin", "track", "application"],
        "recruiter-contacts": ["contact", "recruiter", "network"],
        "follow-up-reminders": ["reminder", "follow", "followup"],
        "job-backlog-manager": ["backlog", "queue", "pending"],
        "database-operations": ["save", "export", "database", "excel"],
    }
    
    for module, keywords in module_keywords.items():
        if module in modules and any(kw in action_lower for kw in keywords):
            result["suggested_modules"].append(module)
    
    # Provide guidance based on action
    if "analyze" in action_lower or "score" in action_lower:
        result["guidance"] = "Load scoring-formulas and skills-matching modules. Provide URL in params['url']. Workflow: 1) Parse job posting, 2) Research company, 3) Match skills, 4) Calculate scores."
    elif "track" in action_lower or "linkedin" in action_lower:
        result["guidance"] = "Load linkedin-tracking module. Use params['url'] for LinkedIn job URL."
    elif "contact" in action_lower or "recruiter" in action_lower:
        result["guidance"] = "Load recruiter-contacts module for contact management."
    elif "reminder" in action_lower or "follow" in action_lower:
        result["guidance"] = "Load follow-up-reminders module for reminder operations."
    elif "backlog" in action_lower:
        result["guidance"] = "Load job-backlog-manager module for queue operations."
    elif not result["guidance"]:
        result["guidance"] = f"Load skill overview first to see available commands for '{params.action}'."
    
    if not result["suggested_modules"]:
        result["suggested_modules"] = modules[:3]  # First 3 as fallback
    
    return json.dumps(result, indent=2)


@mcp.tool(
    name="exocortex_get_config",
    annotations={
        "title": "Get Skill Configuration",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_config(skill_name: str) -> str:
    """Get configuration file for a skill if available.
    
    Args:
        skill_name: Name of the skill
        
    Returns:
        str: Configuration content or error message
    """
    config_paths = [
        SKILLS_DIR / skill_name / "config" / "config.yaml",
        SKILLS_DIR / skill_name / "config.yaml",
        DATA_DIR / skill_name.replace("-", "/") / "config.yaml",
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            return f"# Config: {config_path}\n\n```yaml\n{config_path.read_text()}\n```"
    
    return f"No configuration found for '{skill_name}'"


# =============================================================================
# Entry Point
# =============================================================================

def main():
    """Entry point for CLI."""
    mcp.run()


if __name__ == "__main__":
    main()
