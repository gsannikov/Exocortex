#!/usr/bin/env python3
"""Test Phase 3 features: caching, metrics, smart matching, health."""

import asyncio
import json
import sys
sys.path.insert(0, str(__file__).rsplit('/', 1)[0])

from exocortex_mcp.server import (
    find_skill, health_check, get_metrics, cache_control,
    cross_skill_reference, list_skills, FindSkillInput,
    CacheControlInput, ListSkillsInput, ResponseFormat
)


async def test_smart_matching():
    """Test find_skill with natural language queries."""
    print("\n=== Smart Trigger Matching ===")
    
    queries = [
        "I need to analyze a job posting",
        "prepare for interview",
        "capture an idea",
        "create a social media post",
        "manage my reading list"
    ]
    
    for query in queries:
        result = await find_skill(FindSkillInput(query=query, top_k=2))
        data = json.loads(result)
        print(f"\nQuery: '{query}'")
        if data.get("matches"):
            for m in data["matches"]:
                print(f"  → {m['skill']} (score: {m['score']})")
        else:
            print("  → No matches")
    
    return True


async def test_health():
    """Test health check."""
    print("\n=== Health Check ===")
    result = await health_check()
    data = json.loads(result)
    print(f"Status: {data['status']}")
    print(f"Skills: {data['skills_available']}")
    print(f"Backups: {data['backups_available']}")
    print(f"Version: {data['version']}")
    return data["status"] == "healthy"


async def test_metrics():
    """Test metrics tracking."""
    print("\n=== Metrics ===")
    
    # Make some tool calls to generate metrics
    await list_skills(ListSkillsInput(format=ResponseFormat.JSON))
    await list_skills(ListSkillsInput(format=ResponseFormat.JSON))
    
    result = await get_metrics()
    data = json.loads(result)
    
    print(f"Total calls: {data['summary']['total_tool_calls']}")
    print(f"Most used: {data['summary']['most_used_tool']}")
    print(f"Sessions: {data['summary']['total_sessions']}")
    
    return True


async def test_caching():
    """Test caching system."""
    print("\n=== Caching ===")
    
    # Get cache stats
    result = await cache_control(CacheControlInput(action="stats"))
    data = json.loads(result)
    print(f"Cache entries: {data['cache']['entries']}")
    
    # Make cached call
    await list_skills(ListSkillsInput(format=ResponseFormat.JSON))
    
    # Check again
    result = await cache_control(CacheControlInput(action="stats"))
    data = json.loads(result)
    print(f"After call: {data['cache']['entries']} entries")
    print(f"Cache keys: {data['cache']['keys']}")
    
    # Invalidate
    result = await cache_control(CacheControlInput(action="invalidate"))
    data = json.loads(result)
    print(f"Invalidated: {data['status']}")
    
    return True


async def test_cross_skill():
    """Test cross-skill references."""
    print("\n=== Cross-Skill References ===")
    
    pairs = [
        ("job-analyzer", "interview-prep"),
        ("ideas-capture", "social-media-post"),
        ("recipe-manager", "job-analyzer")  # No relation
    ]
    
    for src, tgt in pairs:
        result = await cross_skill_reference(src, tgt)
        data = json.loads(result)
        rel = data.get("handoff", data.get("relationship", "none"))
        print(f"{src} → {tgt}: {rel[:50]}...")
    
    return True


async def main():
    print("=" * 60)
    print("PHASE 3 TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Smart Matching", test_smart_matching),
        ("Health Check", test_health),
        ("Metrics", test_metrics),
        ("Caching", test_caching),
        ("Cross-Skill", test_cross_skill),
    ]
    
    results = []
    for name, test_fn in tests:
        try:
            passed = await test_fn()
            results.append((name, "✅" if passed else "❌"))
        except Exception as e:
            results.append((name, f"❌ {e}"))
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    for name, status in results:
        print(f"{name}: {status}")


if __name__ == "__main__":
    asyncio.run(main())
