# Database Pattern Module

## Overview

YAML-based structured data storage with index management.

## Storage Structure

```
~/exocortex-data/{skill}/
├── index.yaml           # Main index with metadata
├── items/               # Individual item files (optional)
│   ├── item-001.yaml
│   └── item-002.yaml
└── archive/             # Archived/completed items
```

## Index Format

```yaml
# index.yaml
metadata:
  skill: {skill-name}
  version: 1
  updated: 2025-12-11T10:00:00Z
  count: 42

items:
  - id: item-001
    title: "Item title"
    status: active
    created: 2025-12-01
    updated: 2025-12-10
    # ... item-specific fields
    
  - id: item-002
    # ...
```

## Operations

### Create Item
```python
def create_item(data: dict) -> str:
    item = {
        'id': generate_id(),
        'created': datetime.now().isoformat(),
        'updated': datetime.now().isoformat(),
        **data
    }
    index['items'].append(item)
    save_index()
    return item['id']
```

### Read Item
```python
def get_item(item_id: str) -> dict:
    return next((i for i in index['items'] if i['id'] == item_id), None)
```

### Update Item
```python
def update_item(item_id: str, updates: dict) -> bool:
    item = get_item(item_id)
    if item:
        item.update(updates)
        item['updated'] = datetime.now().isoformat()
        save_index()
        return True
    return False
```

### Delete/Archive Item
```python
def archive_item(item_id: str) -> bool:
    item = get_item(item_id)
    if item:
        item['status'] = 'archived'
        item['archived_at'] = datetime.now().isoformat()
        # Optionally move to archive file
        save_index()
        return True
    return False
```

### Query Items
```python
def query_items(filters: dict) -> list:
    results = index['items']
    for key, value in filters.items():
        results = [i for i in results if i.get(key) == value]
    return results
```

## Best Practices

1. **Always update metadata.updated** on any change
2. **Use ISO format** for all timestamps
3. **Generate UUIDs** for item IDs
4. **Keep index.yaml < 1MB** - archive old items if larger
5. **Backup before bulk operations**
