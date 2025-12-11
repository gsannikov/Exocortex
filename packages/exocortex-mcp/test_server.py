#!/usr/bin/env python3
"""Quick test for exocortex MCP server."""

import asyncio
import json
from exocortex_mcp.server import (
    list_skills, 
    get_skill, 
    load_module,
    skill_action,
    ListSkillsInput,
    GetSkillInput,
    LoadModuleInput,
    SkillActionInput,
    ResponseFormat
)

async def test_list_skills():
    """Test listing skills."""
    print("=" * 50)
    print("TEST: list_skills")
    print("=" * 50)
    
    result = await list_skills(ListSkillsInput(format=ResponseFormat.JSON))
    data = json.loads(result)
    print(f"Found {data['count']} skills:")
    for s in data['skills']:
        print(f"  - {s['name']}: {s['triggers'][:3]}")
    print()

async def test_get_skill():
    """Test getting skill overview."""
    print("=" * 50)
    print("TEST: get_skill (job-analyzer)")
    print("=" * 50)
    
    result = await get_skill(GetSkillInput(
        skill_name="job-analyzer",
        include_modules=True
    ))
    # Show first 500 chars
    print(result[:500] + "...\n")

async def test_load_module():
    """Test loading a module."""
    print("=" * 50)
    print("TEST: load_module (scoring-formulas)")
    print("=" * 50)
    
    result = await load_module(LoadModuleInput(
        skill_name="job-analyzer",
        module_name="scoring-formulas"
    ))
    # Show first 400 chars
    print(result[:400] + "...\n")

async def test_skill_action():
    """Test skill action with suggestions."""
    print("=" * 50)
    print("TEST: skill_action (analyze)")
    print("=" * 50)
    
    result = await skill_action(SkillActionInput(
        skill_name="job-analyzer",
        action="analyze job",
        params={"url": "https://example.com/job"}
    ))
    print(result)
    print()

async def main():
    """Run all tests."""
    await test_list_skills()
    await test_get_skill()
    await test_load_module()
    await test_skill_action()
    print("✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
