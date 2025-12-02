---
title: Notion Sync Module
summary: Bi-directional synchronization between local YAML recipes and Notion database
last_updated: "2025-12-01"
---

# Notion Sync Module v1.0

## Purpose
Maintain consistency between local YAML recipe files and the Notion database for collaborative viewing and editing.

## When to Load This Module
- **Trigger**: User requests sync operations
- **Commands**: 
  - "Sync recipes to Notion"
  - "Import recipes from Notion"
  - "Pull latest from Notion"
  - "Push changes to Notion"

## Notion Database Details

```yaml
database_id: "2461eaaa56f680c4a8d7f1df05616964"
data_source_id: "2461eaaa-56f6-81cd-8003-000bfe08e51f"
database_url: "https://www.notion.so/2461eaaa56f680c4a8d7f1df05616964"
```

### Schema Mapping

| YAML Field | Notion Property | Type | Notes |
|------------|-----------------|------|-------|
| `name` | Name | title | Primary identifier |
| `rating` | Rating | number | 1-5 scale |
| `status` | Status | select | To try, Try next, Tried, Perfected |
| `type` | Type | select | Oven, Ninja, School Breakfast, etc. |
| `relevant` | Relevant | multi_select | Jonathan, Noga, Eitan |
| `source.url` | Source | url | Original recipe URL |
| `tags` | Tags | multi_select | Custom tags |

---

## Push to Notion (Local → Notion)

### Step 1: Load Local Recipes

```python
from pathlib import Path
import yaml

USER_DATA_BASE = "/Users/gursannikov/MyDrive/claude-skills-data/recipe-manager"
recipes_dir = Path(USER_DATA_BASE) / "recipes"

all_recipes = []
for status_dir in ['to-try', 'tried', 'perfected']:
    dir_path = recipes_dir / status_dir
    if dir_path.exists():
        for yaml_file in dir_path.glob('*.yaml'):
            with open(yaml_file) as f:
                recipe = yaml.safe_load(f)
                recipe['_local_path'] = str(yaml_file)
                all_recipes.append(recipe)
```

### Step 2: Check Existing Notion Pages

```python
# Search Notion for existing recipes
tool: "Notion:notion-search"
params:
  query: ""  # Get all
  data_source_url: "collection://2461eaaa-56f6-81cd-8003-000bfe08e51f"
```

### Step 3: Create/Update Logic

```
For each local recipe:
├── Has notion_page_id?
│   ├── Yes → Update existing page
│   └── No → Search by name
│       ├── Found → Update and save page_id locally
│       └── Not found → Create new page
```

### Create New Recipe in Notion

```python
tool: "Notion:notion-create-pages"
params:
  parent:
    data_source_id: "2461eaaa-56f6-81cd-8003-000bfe08e51f"
  pages:
    - properties:
        Name: "{recipe.name}"
        Rating: {recipe.rating or null}
        Status: "{recipe.status}"
        Type: "{recipe.type}"
        Relevant: "{','.join(recipe.relevant)}"
        Source: "{recipe.source.url}"
      content: |
        # Ingredients
        {formatted_ingredients}
        
        # Instructions
        {formatted_instructions}
        
        # Notes
        {formatted_notes}
```

### Update Existing Recipe

```python
tool: "Notion:notion-update-page"
params:
  data:
    page_id: "{recipe.notion_page_id}"
    command: "update_properties"
    properties:
      Rating: {recipe.rating}
      Status: "{recipe.status}"
      Type: "{recipe.type}"
      Relevant: "{','.join(recipe.relevant)}"
```

---

## Pull from Notion (Notion → Local)

### Step 1: Fetch All Notion Recipes

```python
tool: "Notion:notion-search"
params:
  query: ""
  data_source_url: "collection://2461eaaa-56f6-81cd-8003-000bfe08e51f"
```

### Step 2: Fetch Full Content for Each

```python
for page in notion_pages:
    tool: "Notion:notion-fetch"
    params:
      id: page.id
```

### Step 3: Convert and Save Locally

```python
from slug_utils import generate_slug

def notion_to_yaml(notion_page):
    name = notion_page.properties.Name
    slug = generate_slug(name)
    status_folder = status_to_folder(notion_page.properties.Status)
    
    recipe = {
        'id': slug,
        'name': name,
        'icon': extract_icon(notion_page),
        'type': notion_page.properties.Type,
        'status': notion_page.properties.Status,
        'rating': notion_page.properties.Rating,
        'relevant': notion_page.properties.Relevant.split(','),
        'source': {
            'url': notion_page.properties.Source,
            'type': 'text',
            'platform': 'Notion',
            'date_added': notion_page.created_time[:10]
        },
        'ingredients': parse_ingredients(notion_page.content),
        'instructions': parse_instructions(notion_page.content),
        'notes': parse_notes(notion_page.content),
        'notion_page_id': notion_page.id
    }
    
    return recipe, f"{status_folder}/{slug}.yaml"

def status_to_folder(status):
    mapping = {
        'To try': 'to-try',
        'Try next': 'to-try',  # Same folder
        'Tried': 'tried',
        'Perfected': 'perfected'
    }
    return mapping.get(status, 'to-try')
```

---

## Conflict Resolution

### Sync Priority: LOCAL WINS

If both local and Notion have changes:
1. Compare `updated_at` timestamps
2. If local is newer → Push to Notion
3. If Notion is newer → Prompt user for action

### Status Change Handling

When status changes (e.g., "To try" → "Perfected"):
1. Move YAML file to appropriate folder
2. Update Notion property
3. Update `updated_at` timestamp

```python
def move_recipe(recipe_path, new_status):
    old_path = Path(recipe_path)
    new_folder = status_to_folder(new_status)
    new_path = old_path.parent.parent / new_folder / old_path.name
    
    # Read, update, write to new location
    with open(old_path) as f:
        recipe = yaml.safe_load(f)
    
    recipe['status'] = new_status
    recipe['updated_at'] = datetime.now().isoformat()
    
    with open(new_path, 'w') as f:
        yaml.dump(recipe, f, allow_unicode=True)
    
    # Remove old file
    old_path.unlink()
    
    return new_path
```

---

## Sync Commands

### Full Sync (Recommended)
```
User: "Sync recipes to Notion"

Flow:
1. Load all local recipes
2. Fetch all Notion recipes
3. Compare by notion_page_id or name
4. Create/Update as needed
5. Report changes
```

### Push Only
```
User: "Push recipe changes to Notion"

Flow:
1. Load local recipes
2. Find those with notion_page_id
3. Update Notion pages
4. Report updates
```

### Pull Only
```
User: "Pull recipes from Notion"

Flow:
1. Fetch all Notion pages
2. Convert to YAML
3. Save locally (overwrite if exists)
4. Report additions/updates
```

---

## Success Output

```
📊 Sync Complete!

⬆️ Pushed to Notion: 3 recipes
  - arais-tortilla (created)
  - banana-bread (updated)
  - swedish-meatballs (created)

⬇️ Pulled from Notion: 1 recipe
  - new-discovery (created locally)

✅ Total: 16 recipes in sync

Notion Database: https://notion.so/2461eaaa56f680c4a8d7f1df05616964
```

---

**Version**: 1.0.0
**Last Updated**: 2025-12-01
