# Output Pattern Module

## Overview

Generate reports, files, and exports from skill data.

## Output Types

| Type | Format | Use Case |
|------|--------|----------|
| Report | Markdown | Summaries, analysis |
| Export | CSV/Excel | Data for other tools |
| Document | DOCX/PDF | Formal documents |
| Artifact | HTML/React | Interactive displays |

## Report Generation

### Markdown Report

```markdown
# {Report Title}

Generated: {timestamp}
Period: {date_range}

## Summary
{Key metrics and highlights}

## Details
{Detailed breakdown}

## Recommendations
{Action items}
```

### Report Template System

```python
def generate_report(data: dict, template: str) -> str:
    """
    Generate report from data using template.
    """
    # Load template
    template_content = load_template(f"templates/{template}.md")
    
    # Fill placeholders
    report = template_content.format(**data)
    
    return report
```

## File Export

### CSV Export

```python
def export_to_csv(items: list, fields: list, output_path: str):
    """
    Export items to CSV file.
    """
    # Use computer tools to create file
    csv_content = generate_csv(items, fields)
    create_file(output_path, csv_content)
```

### Excel Export

```python
def export_to_excel(items: list, output_path: str):
    """
    Export to Excel with formatting.
    Use xlsx skill or openpyxl.
    """
    # Read xlsx skill: /mnt/skills/public/xlsx/SKILL.md
    # Generate workbook with proper formatting
```

## Artifact Generation

### Summary Artifact (React)

```jsx
// Interactive summary display
const SummaryDashboard = ({ data }) => (
  <div className="p-4">
    <h1 className="text-2xl font-bold">{data.title}</h1>
    <div className="grid grid-cols-3 gap-4 mt-4">
      <MetricCard label="Total" value={data.total} />
      <MetricCard label="Active" value={data.active} />
      <MetricCard label="Score" value={data.avgScore} />
    </div>
    <DataTable items={data.items} />
  </div>
);
```

### Chart Artifact

Use Recharts for data visualization:

```jsx
import { BarChart, Bar, XAxis, YAxis } from 'recharts';

const ScoreChart = ({ items }) => (
  <BarChart data={items}>
    <XAxis dataKey="name" />
    <YAxis />
    <Bar dataKey="score" fill="#3b82f6" />
  </BarChart>
);
```

## Output Locations

| Output Type | Location |
|-------------|----------|
| Reports | `~/exocortex-data/{skill}/reports/` |
| Exports | `/mnt/user-data/outputs/` (for download) |
| Artifacts | Rendered in chat |

## Formatting Standards

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data | Data | Data |
```

### Metrics Display

```
📊 Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Items:     42
Active:          38
Completed:        4
Average Score:   78.5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Best Practices

1. **Include timestamps** on all generated outputs
2. **Provide download links** for file exports
3. **Keep reports scannable** - use headers and bullets
4. **Offer multiple formats** when useful
5. **Cache generated reports** to avoid regeneration
