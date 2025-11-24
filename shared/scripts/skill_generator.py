#!/usr/bin/env python3
"""
Claude Skills - Skill Generator

Creates a new skill with proper structure based on learned patterns.

Usage:
    python skill_generator.py --name "expense-tracker" --patterns inbox,database
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PACKAGES_DIR = REPO_ROOT / 'packages'
TEMPLATES_DIR = Path(__file__).parent.parent / 'templates'

# Emoji mapping for skill types
EMOJI_MAP = {
    'tracker': '📊',
    'capture': '💡',
    'automation': '⚙️',
    'list': '📚',
    'memos': '🎙️',
    'notes': '📝',
    'calendar': '📅',
    'finance': '💰',
    'health': '❤️',
    'default': '🔧',
}


def get_emoji(name: str) -> str:
    """Get appropriate emoji based on skill name."""
    for key, emoji in EMOJI_MAP.items():
        if key in name.lower():
            return emoji
    return EMOJI_MAP['default']


def create_skill_structure(name: str, patterns: list, description: str = ''):
    """Create the full skill directory structure."""
    skill_dir = PACKAGES_DIR / name
    
    if skill_dir.exists():
        print(f"❌ Skill '{name}' already exists at {skill_dir}")
        return False
    
    # Create directories
    (skill_dir / 'skill-package').mkdir(parents=True)
    (skill_dir / 'skill-package' / 'modules').mkdir()
    
    emoji = get_emoji(name)
    display_name = name.replace('-', ' ').title()
    
    # Generate SKILL.md
    skill_md = generate_skill_md(name, emoji, display_name, patterns, description)
    (skill_dir / 'skill-package' / 'SKILL.md').write_text(skill_md)
    
    # Generate version.yaml
    version_yaml = f"""version: 1.0.0
updated: {datetime.now().strftime('%Y-%m-%d')}
skill: {name}
codename: "Initial Release"
"""
    (skill_dir / 'skill-package' / 'version.yaml').write_text(version_yaml)
    
    # Generate README.md
    readme = f"""# {emoji} {display_name}

{description or f'A Claude skill for {display_name.lower()}.'}

## Quick Start

```
process {name.replace('-', ' ')}
```

## Patterns

- {'Apple Notes Inbox' if 'inbox' in patterns else 'Direct input'}
- {'YAML Database' if 'database' in patterns else 'File-based storage'}
{'- Scoring System' if 'scoring' in patterns else ''}

## Version

See `skill-package/version.yaml` for version info.
"""
    (skill_dir / 'README.md').write_text(readme)
    
    # Generate CHANGELOG.md
    changelog = f"""# Changelog

## [1.0.0] - {datetime.now().strftime('%Y-%m-%d')}

- Initial release
- {', '.join(patterns)} patterns implemented
"""
    (skill_dir / 'CHANGELOG.md').write_text(changelog)
    
    print(f"✅ Created skill: {skill_dir}")
    print(f"   - skill-package/SKILL.md")
    print(f"   - skill-package/version.yaml")
    print(f"   - README.md")
    print(f"   - CHANGELOG.md")
    
    # Create user-data directory
    user_data_dir = Path.home() / 'MyDrive' / 'claude-skills-data' / name
    if not user_data_dir.exists():
        user_data_dir.mkdir(parents=True)
        print(f"✅ Created user-data: {user_data_dir}")
    
    # Suggest Apple Note creation
    if 'inbox' in patterns:
        print(f"\n📝 Create Apple Note: '{emoji} {display_name} Inbox'")
    
    return True


def generate_skill_md(name: str, emoji: str, display_name: str, patterns: list, description: str) -> str:
    """Generate SKILL.md content based on patterns."""
    
    # Base template
    content = f"""---
name: {name}
description: {description or f'{display_name} skill with {", ".join(patterns)} patterns.'}
---

# {emoji} {display_name}

{description or f'A Claude skill for {display_name.lower()}.'}

## 🌟 Key Capabilities
"""
    
    # Add capabilities based on patterns
    cap_num = 1
    if 'inbox' in patterns:
        content += f"{cap_num}. **Apple Notes Inbox**: Add items to \"{emoji} {display_name} Inbox\" note\n"
        cap_num += 1
    if 'database' in patterns:
        content += f"{cap_num}. **YAML Database**: Persistent storage with stats tracking\n"
        cap_num += 1
    if 'scoring' in patterns:
        content += f"{cap_num}. **Scoring System**: Multi-dimensional scoring with tiers\n"
        cap_num += 1
    
    # Storage configuration
    content += f"""
## ⚙️ Storage Configuration

**User Data Location**: `~/MyDrive/claude-skills-data/{name}/`

```
{name}/
├── {name}.yaml           # Main database
├── config.yaml           # Local config overrides
└── output/               # Generated outputs
```

## 🚀 Commands

| Command | Action |
|---------|--------|
| `process {name.replace('-', ' ')}` | Process items from inbox |
| `show {name.replace('-', ' ')}` | Display current items |
| `search: [query]` | Find by keyword |
"""
    
    # Add inbox workflow if applicable
    if 'inbox' in patterns:
        content += f"""
## 📋 Workflow: Apple Notes Inbox

### Step 1: Read Inbox

```python
def process_inbox():
    note_content = get_note_content("{emoji} {display_name} Inbox")
    # Parse pending section
    # Process items
    # Update processed section
```

### Step 2: Process Items

For each item in inbox:
1. Validate/parse input
2. {'Score and classify' if 'scoring' in patterns else 'Process content'}
3. Save to database
4. Update Apple Note

### Step 3: Update Apple Note

Move processed items to Processed section with timestamp.
"""
    
    # Footer
    content += f"""
---

**Version**: 1.0.0
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
**Patterns**: {', '.join(patterns)}
"""
    
    return content


def main():
    parser = argparse.ArgumentParser(description='Generate new Claude Skill')
    parser.add_argument('--name', required=True, help='Skill name (kebab-case)')
    parser.add_argument('--patterns', default='inbox,database',
                       help='Patterns to include (comma-separated: inbox,database,scoring)')
    parser.add_argument('--description', default='', help='Skill description')
    
    args = parser.parse_args()
    
    patterns = [p.strip() for p in args.patterns.split(',')]
    
    create_skill_structure(args.name, patterns, args.description)


if __name__ == '__main__':
    main()
