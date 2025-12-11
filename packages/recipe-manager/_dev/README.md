# Recipe Manager

Manage recipes, plan meals, and generate shopping lists. Extracts recipes from URLs (Instagram, YouTube, websites), images, and Apple Notes.

## Quick Start

1. Add URLs to **Recipe Inbox** Apple Note
2. Tell Claude: `"process recipe inbox"`
3. Or directly: `"add recipe from [URL]"`
4. View: `"show recipes"` or `"show ninja recipes"`

## Commands

| Command | Action |
|---------|--------|
| `process recipe inbox` | Import from Apple Notes |
| `add recipe from [URL]` | Extract from URL |
| `extract recipe from image` | Parse attached image |
| `show recipes` | List all |
| `show [type] recipes` | Filter by type |
| `mark [recipe] tried` | Update status |
| `rate [recipe] [1-5]` | Add rating |
| `sync to Notion` | Push to Notion |

## Features

- **Recipe Extraction**: Instagram, YouTube, Websites
- **Image Processing**: Parse recipe photos
- **Inbox Import**: Apple Notes integration
- **Multi-language**: Hebrew and English
- **Family Tracking**: Member preferences
- **Notion Sync**: Bi-directional with beautiful preview
- **Status Workflow**: To try → Perfected

## Supported Sources

- Instagram (Bright Data / Firecrawl)
- YouTube (Description analysis)
- Websites (Firecrawl)
- Images (Claude Vision)
- Apple Notes (Direct parse)

## CONFIGURATION

Recipes stored in: `~/exocortex-data/recipe-manager/` (YAML files)

### Settings
Configure in `config/settings.yaml`:
- Family members
- Device types (Oven, Ninja, etc.)
- Notion Database ID

## Workflow

1.  **Capture**: Save link/image to "Recipe Inbox"
2.  **Process**: Extract metadata and ingredients
3.  **Store**: YAML file created locally
4.  **Cook & Rate**: Update status and rating after cooking
5.  **Sync**: Sync to Notion mobile database (Optional)
