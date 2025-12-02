---
title: Apple Notes Import Module
summary: Import recipes from Apple Notes inbox, process URLs or raw text, and archive processed notes
last_updated: "2025-12-01"
---

# Apple Notes Import Module v1.0

## Purpose
Enable quick recipe capture from mobile via Apple Notes, then process into structured YAML recipes.

## When to Load This Module
- **Trigger**: User wants to import recipes from Apple Notes
- **Commands**: 
  - "Process recipe inbox"
  - "Check recipe inbox"
  - "Import recipes from Apple Notes"
  - "Import recipe from note: [name]"

---

## Workflow Overview

```
📱 Mobile Capture          →  📝 Apple Notes        →  🍳 Recipe Manager
"Found cool recipe!"          "🍳 Recipe Inbox"        recipes/to-try/*.yaml
Copy URL to Notes             • URL 1                  Structured YAML
                              • URL 2
                              • Raw text recipe
```

---

## Apple Notes Inbox Convention

### Primary Inbox Note
- **Name**: `🍳 Recipe Inbox`
- **Folder**: Notes (default)
- **Format**: One item per line (URL or text block)

### Example Inbox Content
```
https://www.instagram.com/reel/ABC123/
https://youtube.com/watch?v=XYZ789
Shakshuka Recipe
- 4 eggs
- 2 tomatoes
- onion
- spices
Cook in pan 15 min
---
```

---

## Processing Steps

### Step 1: Read Inbox Note

```python
tool: "Read and Write Apple Notes:get_note_content"
params:
  note_name: "🍳 Recipe Inbox"
  folder: "Notes"  # Optional, search all if not found
```

### Step 2: Parse Content

```python
def parse_inbox(content):
    """Parse inbox note into individual recipe items."""
    items = []
    current_text = []
    
    for line in content.split('\n'):
        line = line.strip()
        
        # URL detection
        if line.startswith(('http://', 'https://')):
            # Save any accumulated text as previous item
            if current_text:
                items.append({
                    'type': 'text',
                    'content': '\n'.join(current_text)
                })
                current_text = []
            # Add URL item
            items.append({
                'type': 'url',
                'content': line,
                'platform': detect_platform(line)
            })
        
        # Separator detection
        elif line == '---':
            if current_text:
                items.append({
                    'type': 'text',
                    'content': '\n'.join(current_text)
                })
                current_text = []
        
        # Text accumulation
        elif line:
            current_text.append(line)
    
    # Don't forget trailing text
    if current_text:
        items.append({
            'type': 'text',
            'content': '\n'.join(current_text)
        })
    
    return items

def detect_platform(url):
    if 'instagram.com' in url:
        return 'Instagram'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'YouTube'
    elif 'tiktok.com' in url:
        return 'TikTok'
    else:
        return 'Website'
```

### Step 3: Process Each Item

```python
for item in items:
    if item['type'] == 'url':
        # Use recipe-extraction module for URLs
        # Load: recipe-extraction.md
        # Process URL per that module's pipeline
        pass
    
    elif item['type'] == 'text':
        # Parse raw text recipe
        recipe = parse_text_recipe(item['content'])
        save_recipe(recipe)
```

### Step 4: Parse Raw Text Recipe

```python
def parse_text_recipe(text):
    """Extract recipe from raw text."""
    lines = text.strip().split('\n')
    
    # First line is usually the name
    name = lines[0].strip()
    
    # Detect sections
    ingredients = []
    instructions = []
    current_section = 'unknown'
    
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Section detection
        lower = line.lower()
        if 'ingredient' in lower or 'מרכיבים' in lower:
            current_section = 'ingredients'
            continue
        elif 'instruction' in lower or 'step' in lower or 'הוראות' in lower:
            current_section = 'instructions'
            continue
        
        # Ingredient pattern (starts with -, •, or number + unit)
        if line.startswith(('-', '•', '*')) or re.match(r'^\d+\s*(g|kg|ml|cup|tbsp|tsp|יחידות|כוס)', line):
            current_section = 'ingredients'
            ingredients.append(line.lstrip('-•* '))
        
        # Numbered instruction pattern
        elif re.match(r'^\d+\.?\s', line):
            current_section = 'instructions'
            instructions.append(re.sub(r'^\d+\.?\s*', '', line))
        
        # Accumulate based on current section
        elif current_section == 'ingredients':
            ingredients.append(line)
        elif current_section == 'instructions':
            instructions.append(line)
        else:
            # Default: treat as ingredient if short, instruction if long
            if len(line) < 50:
                ingredients.append(line)
            else:
                instructions.append(line)
    
    return {
        'name': name,
        'ingredients': ingredients,
        'instructions': instructions,
        'source': {
            'type': 'text',
            'platform': 'Apple Notes',
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }
    }
```

### Step 5: Archive Processed Items

After successful processing, clear the inbox:

```python
tool: "Read and Write Apple Notes:update_note_content"
params:
  note_name: "🍳 Recipe Inbox"
  new_content: """
🍳 Recipe Inbox

Add recipe URLs or text here, one per line.
Use --- to separate multiple text recipes.

Last processed: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
```

---

## Alternative: Import from Named Note

For importing from a specific note instead of the inbox:

```
User: "Import recipe from note: Grandma's Cookies"

Flow:
1. Search for note by name
2. Parse entire content as single recipe
3. Save to YAML
4. Optionally delete/archive the note
```

```python
tool: "Read and Write Apple Notes:get_note_content"
params:
  note_name: "Grandma's Cookies"

# Then parse as single recipe
```

---

## Interactive Mode

When processing inbox, confirm each item:

```
📥 Processing Recipe Inbox...

Found 3 items:

1️⃣ Instagram Reel
   https://instagram.com/reel/ABC123
   → Extract? [Y/n]

2️⃣ YouTube Video  
   https://youtube.com/watch?v=XYZ789
   → Extract? [Y/n]

3️⃣ Raw Text Recipe
   "Shakshuka Recipe - 4 eggs, 2 tomatoes..."
   → Parse as recipe? [Y/n]
```

---

## Batch Mode

Process all without confirmation:

```
User: "Process recipe inbox - batch mode"

Flow:
1. Read inbox
2. Parse all items
3. Process each (skip failures)
4. Report results
5. Clear inbox
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Inbox note not found | Create it with template |
| URL extraction fails | Log and continue, don't clear from inbox |
| Text parse fails | Save raw text for manual review |
| Duplicate recipe | Append `-2` to slug |

---

## Success Output

```
📥 Recipe Inbox Processed!

✅ Successfully imported:
  1. arais-tortilla (from Instagram)
  2. shakshuka (from text)
  3. banana-bread (from YouTube)

⚠️ Skipped (extraction failed):
  - https://broken-link.com/recipe

📝 Inbox cleared and ready for new recipes.

Total: 3 recipes added to "To try"
```

---

## Mobile Quick Capture Tips

Tell users to:
1. Open Apple Notes on phone
2. Create/open "🍳 Recipe Inbox" note
3. Paste URL or type quick recipe
4. Later: "Process recipe inbox" on Claude

---

**Version**: 1.0.0
**Last Updated**: 2025-12-01
