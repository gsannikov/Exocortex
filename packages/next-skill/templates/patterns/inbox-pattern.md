# Inbox Pattern Module

## Overview

Process items from Apple Notes inbox for structured data extraction.

## Inbox Location

Apple Notes folder: `{Skill} Inbox`

## Processing Workflow

### Step 1: Read Inbox
```
Use Read and Write Apple Notes:list_notes
Filter: folder = "{Skill} Inbox"
```

### Step 2: Parse Items
Each note contains one or more items to process.

**Expected Format**:
```
{item identifier}
{additional details}
---
{next item}
```

### Step 3: Extract Data
Parse each item into structured format:
```yaml
id: generated-uuid
raw_text: "original note content"
extracted:
  field1: value
  field2: value
created: timestamp
source: inbox
```

### Step 4: Store
Add to main data storage (see database pattern).

### Step 5: Clear Processed
After successful processing:
- Archive note content to `_dev/inbox-archive/`
- Clear or delete original note

## Error Handling

| Error | Action |
|-------|--------|
| Parse failure | Log to `_dev/parse-errors.log`, skip item |
| Empty inbox | Return "No items to process" |
| Note access error | Retry once, then report |

## Integration Points

- **Input**: Apple Notes
- **Output**: Structured YAML data
- **Triggers**: Manual command or scheduled
