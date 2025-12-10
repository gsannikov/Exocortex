---
name: recipe-manager
description: Imports recipes from web/Apple Notes, scales ingredients, and syncs to Notion.
---

# Recipe Manager Skill

AI-powered recipe collection manager for extracting, organizing, and tracking family recipes.

## 🌟 Key Capabilities

1. **Recipe Extraction**: Extract recipes from any URL (websites, Instagram reels, YouTube)
2. **Image Processing**: Parse recipe images and photos
3. **Apple Notes Import**: Import recipes saved in Apple Notes (URLs or raw text)
4. **Multi-language Support**: Hebrew and English recipes
5. **Family Tracking**: Track which family members like each recipe
6. **Status Management**: To try → Try next → Tried → Perfected workflow
7. **Notion Sync**: Bi-directional sync with Notion database
8. **Beautiful Preview**: Render recipe cards using shared-preview system

## ⚠️ CRITICAL: Storage Configuration

**Primary Storage: LOCAL FILESYSTEM**
All recipes are stored locally in YAML format for reliability and version control.

- **User Data Location**: Configured in `config/paths.py`
- **Path**: Configured in `shared/config/paths.py` (default: `~/Documents/claude-skills-data/recipe-manager`)
- **Recipe Files**: YAML files in `recipes/`
- **Configuration**: `config/settings.yaml`

**Directory Structure**:
```
~/Documents/claude-skills-data/recipe-manager/  # or as configured in shared/config/paths.py
├── config/
│   └── settings.yaml       # User preferences
├── recipes/
│   ├── to-try/            # Status-based organization
│   │   └── *.yaml
│   ├── tried/
│   │   └── *.yaml
│   └── perfected/
│       └── *.yaml
└── exports/
    └── recipes.xlsx        # Optional Excel export
```

**Secondary Storage: Notion** (optional sync)
- Notion Database ID: `2461eaaa56f680c4a8d7f1df05616964`
- Data Source ID: `2461eaaa-56f6-81cd-8003-000bfe08e51f`
- Sync is manual via explicit commands

## 📋 Recipe Data Structure

```yaml
# recipe-template.yaml
id: "arais-tortilla"                    # Auto-generated slug
name: "Arais Tortilla"                  # Recipe title
icon: "🌮"                              # Emoji icon

# Classification
type: "Ninja"                           # Oven | Ninja | School Breakfast | Stovetop | etc.
status: "To try"                        # To try | Try next | Tried | Perfected
rating: 5                               # 1-5 stars (null if not tried)

# Family preferences
relevant:                               # Who likes this recipe
  - "Jonathan"
  - "Noga"  
  - "Eitan"

# Source information
source:
  url: "https://instagram.com/reel/..."
  type: "video"                         # text | image | video
  platform: "Instagram"                 # Instagram | YouTube | Website | Manual | Apple Notes
  author: "שלומי סולומון"
  date_added: "2025-09-27"

# Recipe content
prep_time: "15 min"
cook_time: "20 min"
servings: 4
difficulty: "Easy"                      # Easy | Medium | Hard

ingredients:
  - "½ קילו בשר טחון (20% שומן מומלץ)"
  - "1 בצל קצוץ דק"
  - "..."

instructions:
  - "מערבבים את כל הירקות, התבלינים והבשר"
  - "מחממים נינג'ה גריל לחום גבוה"
  - "..."

# Optional sections
notes: []                               # Tweaks and experiments
tags:                                   # Custom tags
  - "meat"
  - "quick"
  - "family-favorite"

# Metadata
created_at: "2025-09-27T09:35:00Z"
updated_at: "2025-09-27T09:35:00Z"
notion_page_id: "27b1eaaa-56f6-8086-8c76-f27141babc62"  # For sync
```

## 🚀 Quick Start Commands

### Add Recipe from URL
```
"Add recipe from https://instagram.com/reel/..."
"Save recipe: [URL]"
"Extract recipe from this link: [URL]"
```

### Add Recipe from Image
```
"Extract recipe from this image" (with image attached)
"Parse recipe from photo"
```

### Apple Notes Import
```
"Process recipe inbox"           # Primary - processes 🍳 Recipe Inbox note
"Check recipe inbox"
"Import recipes from Apple Notes"
"Import recipe from note: [note name]"
```

### Manual Recipe Entry
```
"Add new recipe: Shakshuka"
"Create recipe for [dish name]"
```

### View Recipes
```
"Show my recipes"
"List recipes to try"
"Show perfected recipes"
"Find ninja recipes"
"Show recipe arais-tortilla"
```

### Preview Recipes
```
"Preview arais-tortilla"         # Beautiful card view
"Export arais-tortilla as HTML"  # Saveable file
```

### Update Recipe
```
"Rate arais-tortilla 5 stars"
"Mark shakshuka as Tried"
"Add note to arais-tortilla: less salt next time"
```

### Notion Sync
```
"Sync recipes to Notion"
"Import recipes from Notion"
"Pull latest from Notion"
```

## 🔄 Workflow

### Adding a New Recipe

1. **User provides URL/image/text**
2. **Extract & Parse**:
   - Scrape content using Firecrawl/Bright Data
   - Parse ingredients and instructions
   - Detect language (Hebrew/English)
   - Identify cooking method (Oven/Ninja/etc.)
3. **Create YAML file** in `recipes/`
4. **Optionally sync to Notion**

### Recipe Extraction Process

```
Input Source
    │
    ├── Instagram Reel/Post
    │   └── Use Bright Data or Firecrawl
    │       └── Extract caption + video description
    │
    ├── YouTube Video
    │   └── Fetch video description
    │       └── Parse ingredients/instructions
    │
    ├── Website
    │   └── Use Firecrawl scrape
    │       └── Parse structured recipe data
    │
    ├── Image
    │   └── Use Claude vision
    │       └── Extract text and structure
    │
    └── Apple Notes
        └── Read note content
            ├── URL found → Extract from source
            └── Raw text → Parse directly
```

## ⚙️ Configuration

### settings.yaml
```yaml
# User preferences
family_members:
  - id: "jonathan"
    name: "Jonathan"
  - id: "noga"
    name: "Noga"
  - id: "eitan"
    name: "Eitan"

# Cooking method categories
types:
  - "Oven"
  - "Ninja"
  - "School Breakfast"
  - "Stovetop"
  - "Grill"
  - "No Cook"
  - "Instant Pot"

# Status workflow
statuses:
  - "To try"
  - "Try next"
  - "Tried"
  - "Perfected"

# Notion sync settings
notion:
  enabled: true
  database_id: "2461eaaa56f680c4a8d7f1df05616964"
  data_source_id: "2461eaaa-56f6-81cd-8003-000bfe08e51f"
  auto_sync: false  # Manual sync by default

# Language preferences
default_language: "he"  # Hebrew
```

## 🛠️ MCP Tools Used

### Required
- **Filesystem MCP**: Local YAML storage
  - `filesystem:read_text_file`
  - `filesystem:write_file`
  - `filesystem:list_directory`

### For Web Extraction
- **Firecrawl MCP**: Web scraping
  - `firecrawl_scrape`
  - `firecrawl_search`
- **Bright Data MCP**: Instagram/LinkedIn
  - `Bright Data:scrape_as_markdown`

### For Notion Sync
- **Notion MCP**: Database operations
  - `Notion:notion-fetch`
  - `Notion:notion-create-pages`
  - `Notion:notion-update-page`
  - `Notion:notion-search`

### For Apple Notes Import
- **Apple Notes MCP**: Note access
  - `Read and Write Apple Notes:list_notes`
  - `Read and Write Apple Notes:get_note_content`
  - `Read and Write Apple Notes:update_note_content`

## 📚 Module Reference

| Module | Purpose | When Loaded |
|--------|---------|-------------|
| `recipe-extraction.md` | URL/image parsing | On add recipe |
| `notion-sync.md` | Notion bi-directional sync | On sync commands |
| `apple-notes-import.md` | Import from Apple Notes | On notes import commands |

## 🎨 Preview System

Uses **shared-preview** system for beautiful output:

- **Theme**: `cooking` (orange/red warm colors)
- **Mapping**: `templates/preview-mapping.yaml`
- **Commands**:
  - `"Preview [recipe]"` → React artifact
  - `"Show [recipe]"` → Markdown
  - `"Export [recipe] HTML"` → File

## 🔧 Helper Scripts

- `slug_utils.py` - Generate URL-safe recipe IDs with Hebrew transliteration
- `yaml_utils.py` - YAML parsing/generation

## ✅ Success Criteria

Recipe addition is successful when:
- ✅ Recipe extracted and parsed correctly
- ✅ YAML file created with all fields
- ✅ Recipe searchable by name/type/status
- ✅ Notion sync completes (if enabled)

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-01  
**Status**: Initial Release
