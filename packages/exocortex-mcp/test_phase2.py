#!/usr/bin/env python3
"""Test Phase 2 self-update tools for exocortex MCP server."""

import asyncio
import json
from exocortex_mcp.server import (
    # Phase 1 tools
    list_skills, 
    get_skill, 
    load_module,
    skill_action,
    update_module,
    ListSkillsInput,
    GetSkillInput,
    LoadModuleInput,
    SkillActionInput,
    UpdateModuleInput,
    ResponseFormat,
    # Phase 2 tools
    list_backups,
    rollback_module,
    diff_module,
    learn_pattern,
    propose_update,
    apply_patch,
    list_patterns,
    mark_pattern_applied,
    ListBackupsInput,
    DiffModuleInput,
    LearnPatternInput,
    ProposeUpdateInput,
    ApplyPatchInput,
)

async def test_phase2_workflow():
    """Test full Phase 2 self-update workflow."""
    print("=" * 60)
    print("PHASE 2: Self-Update Loop Test")
    print("=" * 60)
    
    # 1. Learn a pattern
    print("\n1. Learning a pattern...")
    result = await learn_pattern(LearnPatternInput(
        skill_name="job-analyzer",
        pattern_type="improvement",
        description="Remote work scoring should weight higher for senior roles",
        suggested_change="In scoring-formulas, increase remote bonus from 5 to 8 for senior positions",
        module_name="scoring-formulas"
    ))
    data = json.loads(result)
    print(f"   Pattern captured: {data['pattern_id']}")
    
    # 2. List patterns
    print("\n2. Listing patterns...")
    result = await list_patterns(skill_name="job-analyzer")
    data = json.loads(result)
    print(f"   Found {data['count']} patterns for job-analyzer")
    
    # 3. Propose updates
    print("\n3. Proposing updates...")
    result = await propose_update(ProposeUpdateInput(
        skill_name="job-analyzer",
        module_name="scoring-formulas"
    ))
    data = json.loads(result)
    print(f"   {data['count']} proposals generated")
    if data['proposals']:
        print(f"   First proposal: {data['proposals'][0]['description'][:60]}...")
    
    # 4. List backups
    print("\n4. Listing backups...")
    result = await list_backups(ListBackupsInput(limit=5))
    data = json.loads(result)
    print(f"   Found {data['count']} backups")
    
    # 5. Test diff (if backups exist)
    if data['count'] > 0:
        print("\n5. Testing diff...")
        # Try to find a scoring-formulas backup
        for b in data['backups']:
            if 'scoring' in b['filename']:
                result = await diff_module(DiffModuleInput(
                    skill_name="job-analyzer",
                    module_name="scoring-formulas",
                    backup_filename=b['filename']
                ))
                print(f"   Diff result: {result[:100]}...")
                break
        else:
            print("   No scoring-formulas backup found for diff test")
    else:
        print("\n5. Skipping diff test (no backups)")
    
    print("\n" + "=" * 60)
    print("✅ Phase 2 tests completed!")
    print("=" * 60)


async def main():
    """Run Phase 2 tests."""
    await test_phase2_workflow()


if __name__ == "__main__":
    asyncio.run(main())
