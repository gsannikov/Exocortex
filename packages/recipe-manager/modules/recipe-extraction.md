---
title: Recipe Extraction Module
summary: Extract and parse recipes from URLs (websites, Instagram, YouTube), images, and raw text
last_updated: "2025-12-01"
---

# Recipe Extraction Module v1.0

## Purpose
Extract structured recipe data from various sources and create properly formatted YAML files.

## When to Load This Module
- **Trigger**: User provides URL, image, or text to create a new recipe
- **Commands**: "Add recipe from...", "Save recipe:", "Extract recipe..."
- **Prerequisites**: Filesystem MCP available, USER_DATA_BASE configured

---

## Extraction Pipeline

### 1. Source Detection

```
Detect source type from input:
├── Instagram URL → Use Bright Data scraper
├── YouTube URL → Use Firecrawl or manual parsing
├── Regular URL → Use Firecrawl scrape
├── Image → Use Claude vision directly
└── Raw text → Parse directly
```

### 2. Source-Specific Extraction

#### Instagram (Reels/Posts)
```python
# Priority: Bright Data (more reliable for Instagram)
tool: "Bright Data:scrape_as_markdown"
params:
  url: <instagram_url>

# Fallback: Firecrawl
tool: "firecrawl_scrape"
params:
  url: <instagram_url>
  formats: ["markdown"]
```

**Instagram parsing targets:**
- Caption text (usually contains full recipe)
- Author name (@username)
- Video description if available

#### YouTube Videos
```python
tool: "firecrawl_scrape"
params:
  url: <youtube_url>
  formats: ["markdown"]
```

**YouTube parsing targets:**
- Video description (often has full recipe)
- Pinned comment (sometimes has ingredients)
- Channel name as author

#### Website URLs
```python
tool: "firecrawl_scrape"
params:
  url: <url>
  formats: ["markdown"]
  onlyMainContent: true
```

**Website parsing targets:**
- Recipe schema (JSON-LD) if present
- Ingredient lists (look for `<li>` patterns)
- Instruction steps (numbered lists)
- Prep/cook time, servings

#### Images
Use Claude vision capabilities directly - no external tool needed.

**Image parsing:**
- OCR all visible text
- Identify ingredients section
- Identify instructions section
- Extract any metadata (author, source)

---

## 3. Recipe Normalization

### Field Mapping

| Source Field | YAML Field | Notes |
|--------------|------------|-------|
| Title/Name | `name` | Capitalize properly |
| - | `id` | Generate slug from name |
| - | `icon` | Auto-assign emoji |
| Source URL | `source.url` | Original URL |
| Platform | `source.platform` | Instagram/YouTube/Website |
| Author | `source.author` | Creator name |
| Today | `source.date_added` | YYYY-MM-DD format |
| Ingredients list | `ingredients` | Array of strings |
| Steps/Instructions | `instructions` | Array of strings |
| Prep time | `prep_time` | Normalize to "X min" |
| Cook time | `cook_time` | Normalize to "X min" |
| Servings | `servings` | Integer |

### Auto-Detection Rules

**Cooking Type Detection:**
```
Contains "ninja" or "air fryer" → type: "Ninja"
Contains "oven" or "bake" → type: "Oven"
Contains "stovetop" or "pan" or "skillet" → type: "Stovetop"
Contains "grill" → type: "Grill"
Contains "no cook" or "raw" → type: "No Cook"
Contains "instant pot" or "pressure" → type: "Instant Pot"
Contains "breakfast" or "בוקר" → type: "School Breakfast"
Default → type: "" (empty, user will set)
```

**Icon Assignment:**
```
Meat dishes → 🍖
Chicken → 🍗
Fish → 🐟
Vegetarian → 🥗
Breakfast → 🍳
Dessert/Sweets → 🍰
Pasta → 🍝
Pizza/Flatbread → 🍕
Soup → 🍲
Salad → 🥗
Sandwich/Wrap → 🌮
Default → 🍽️
```

---

## 4. Slug Generation (Hebrew Support)

```python
# Hebrew transliteration map
HEBREW_MAP = {
    'א': '', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h',
    'ו': 'v', 'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'y',
    'כ': 'k', 'ך': 'k', 'ל': 'l', 'מ': 'm', 'ם': 'm',
    'נ': 'n', 'ן': 'n', 'ס': 's', 'ע': '', 'פ': 'p',
    'ף': 'f', 'צ': 'ts', 'ץ': 'ts', 'ק': 'k', 'ר': 'r',
    'ש': 'sh', 'ת': 't', '״': '', '׳': ''
}

def generate_slug(name):
    # Transliterate Hebrew
    result = transliterate(name, HEBREW_MAP)
    # Lowercase, replace spaces with dashes
    result = result.lower().replace(' ', '-')
    # Remove special chars
    result = re.sub(r'[^a-z0-9-]', '', result)
    # Clean up multiple dashes
    result = re.sub(r'-+', '-', result).strip('-')
    return result

# Example: "עוף עם תפו״א מדורה" → "of-im-tpva-mdvrh"
```

---

## 5. File Creation

### Output Path
```
{USER_DATA_BASE}/recipe-manager/recipes/to-try/{slug}.yaml
```

### YAML Template
```yaml
id: "{slug}"
name: "{extracted_name}"
icon: "{auto_icon}"

type: "{detected_type}"
status: "To try"
rating: null

relevant: []

source:
  url: "{source_url}"
  type: "{text|image|video}"
  platform: "{platform}"
  author: "{author}"
  date_added: "{today}"

prep_time: "{extracted_prep_time}"
cook_time: "{extracted_cook_time}"
servings: {extracted_servings}
difficulty: "{Easy|Medium|Hard}"

ingredients:
{formatted_ingredients}

instructions:
{formatted_instructions}

notes: []
tags: []

created_at: "{iso_timestamp}"
updated_at: "{iso_timestamp}"
notion_page_id: null
```

---

## 6. Validation Checklist

Before saving, verify:
- [ ] `id` is unique (check existing files)
- [ ] `name` is not empty
- [ ] `ingredients` has at least 1 item
- [ ] `instructions` has at least 1 step
- [ ] `source.url` is valid (if from URL)
- [ ] Hebrew text preserved correctly

---

## Error Handling

| Error | Recovery |
|-------|----------|
| URL unreachable | Inform user, suggest manual entry |
| Empty recipe content | Ask user to paste text directly |
| Duplicate slug | Append `-2`, `-3`, etc. |
| Parse failure | Save partial data, flag for review |

---

## Success Output

```
✅ Recipe Added Successfully!

📋 {name}
🔖 ID: {slug}
📍 Status: To try
🍳 Type: {type}

📄 Saved to: recipes/to-try/{slug}.yaml

Would you like to:
- Preview the recipe card?
- Sync to Notion?
- Add another recipe?
```

---

**Version**: 1.0.0
**Last Updated**: 2025-12-01
