# Recipe Manager Skill

Imports recipes from web/Apple Notes, scales ingredients, and syncs to Notion.

## 🌟 Capabilities

1.  **Recipe Extraction**: Extract recipes from any URL (websites, Instagram reels, YouTube)
2.  **Image Processing**: Parse recipe images and photos
3.  **Apple Notes Import**: Import recipes saved in Apple Notes (URLs or raw text)
4.  **Multi-language Support**: Hebrew and English recipes
5.  **Family Tracking**: Track which family members like each recipe
6.  **Status Management**: To try → Try next → Tried → Perfected workflow
7.  **Notion Sync**: Bi-directional sync with Notion database
8.  **Beautiful Preview**: Render recipe cards using shared-preview system

## 🚀 Quick Start

### Add Recipe
- **From URL**: `"Add recipe from [URL]"`
- **From Image**: `"Extract recipe from this image"` (attach image)
- **From Apple Notes**: `"Process recipe inbox"` or `"Import recipes from Apple Notes"`
- **Manual**: `"Add new recipe: Shakshuka"`

### View & Organize
- **List**: `"Show my recipes"` or `"List recipes to try"`
- **Search**: `"Find ninja recipes"` or `"Show recipe arais-tortilla"`
- **Preview**: `"Preview arais-tortilla"` (Beautiful card view)
- **Update**: `"Rate arais-tortilla 5 stars"` or `"Mark shakshuka as Tried"`

### Sync
- **Notion**: `"Sync recipes to Notion"` or `"Pull latest from Notion"`

## ⚙️ Configuration

Recipes are stored as YAML files in your `exocortex-data` directory (default: `~/exocortex-data/recipe-manager`).

### `config/settings.yaml`
You can configure family members, cooking types, and Notion settings in the `config/settings.yaml` file within your data directory.

```yaml
family_members:
  - id: "user"
    name: "User"

types:
  - "Oven"
  - "Stovetop"
  - "Grill"
  - "No Cook"

notion:
  enabled: true
  database_id: "your-database-id"
```

## 🔄 Workflow

1.  **Capture**: Save a link to your "Recipe Inbox" Apple Note or just paste it to Claude.
2.  **Process**: Claude extracts ingredients, instructions, and metadata.
3.  **Store**: A YAML file is created locally.
4.  **Cook & Rate**: After cooking, tell Claude your rating and notes.
5.  **Sync**: Optionally sync to Notion for mobile access.
