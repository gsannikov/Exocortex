---
title: Database Operations Module (Hybrid Architecture)
summary: Synchronize YAML, HTML, and Excel data sources across the hybrid content store.
last_updated: "2025-10-29"
---

# Database Operations Module v9.2 (Hybrid Architecture)

## Purpose
Manage YAML ↔ HTML/Excel synchronization and database operations for the hybrid storage architecture.

## Core Principle

**Source of Truth**: YAML frontmatter in markdown files  
**Convenience Views**: 
- **HTML** (Primary): Interactive browser-based database (works everywhere)
- **Excel** (Legacy): Spreadsheet for desktop users  
**Philosophy**: Write to YAML, read from anywhere

---

## When to Load This Module

- **Step 2**: Check company cache status
- **Step 11**: Save role analysis with YAML
- **Step 12**: Sync role to HTML (and optionally Excel)
- **Maintenance**: Batch resync, validation, statistics

> **📚 Extended Documentation**: For advanced queries, batch operations, and comprehensive error 
> handling patterns, see [references/database-operations-examples.md](../references/database-operations-examples.md)

---

## Database Architecture

```
user-data/
├── db/
│   ├── companies/           # Company profiles (YAML + MD)
│   │   ├── nvidia.md
│   │   ├── google.md
│   │   └── ...
│   ├── jobs/analyzed/      # Role analyses (YAML + MD)
│   │   ├── nvidia-eng-mgr-20251028.md
│   │   ├── google-tpm-20251027.md
│   │   └── ...
│   ├── db.html            # Interactive HTML database (PRIMARY)
│   └── db.xlsx            # Excel database (LEGACY, optional)
```

---

## Configuration and Paths

### Load from User Config

```python
def initialize_database_paths(user_config, USER_DATA_BASE):
    """
    Initialize all database paths from user configuration
    
    Args:
        user_config: Loaded user-config.yaml
        USER_DATA_BASE: Base path to user data
    
    Returns:
        dict with all database paths
    """
    
    paths = user_config['paths']
    
    db_paths = {
        'COMPANIES_DIR': f"{USER_DATA_BASE}/{paths['companies_db']}",
        'ROLES_DIR': f"{USER_DATA_BASE}/{paths['roles_db']}",
        'EXCEL_PATH': f"{USER_DATA_BASE}/{paths['excel_db']}"
    }
    
    # Validate paths exist
    from pathlib import Path
    
    for name, path in db_paths.items():
        path_obj = Path(path)
        if name != 'EXCEL_PATH':  # Excel might not exist yet
            if not path_obj.exists():
                raise FileNotFoundError(f"{name} does not exist: {path}")
    
    return db_paths
```

---

## YAML Operations

### Parse YAML Frontmatter

```python
def parse_yaml_frontmatter(markdown_content: str) -> tuple[dict, str]:
    """
    Extract YAML frontmatter and markdown body
    
    Format:
    ---
    key: value
    another_key: value
    ---
    
    # Markdown content...
    
    Args:
        markdown_content: Complete markdown file content
    
    Returns:
        (frontmatter_dict, markdown_body)
    """
    
    import yaml
    
    # Check for frontmatter
    if not markdown_content.startswith('---'):
        return {}, markdown_content
    
    # Split by --- delimiters
    parts = markdown_content.split('---', 2)
    
    if len(parts) < 3:
        # Malformed frontmatter
        return {}, markdown_content
    
    try:
        yaml_text = parts[1].strip()
        frontmatter = yaml.safe_load(yaml_text) or {}
        markdown_body = parts[2].strip()
        
        return frontmatter, markdown_body
    
    except yaml.YAMLError as e:
        print(f"⚠️ YAML parsing error: {e}")
        return {}, markdown_content
```

### Create YAML Document

```python
def create_yaml_document(frontmatter: dict, markdown_body: str) -> str:
    """
    Combine YAML frontmatter with markdown body
    
    Args:
        frontmatter: Dictionary of YAML fields
        markdown_body: Markdown content
    
    Returns:
        Complete document string
    """
    
    import yaml
    
    # Serialize YAML with proper formatting
    yaml_text = yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False  # Preserve insertion order
    )
    
    # Combine with markdown
    full_document = f"---\n{yaml_text}---\n\n{markdown_body}"
    
    return full_document
```

---

## Company Operations

### Check Company Cache

```python
def check_company_cache(company_slug: str, db_paths: dict) -> tuple[bool, bool, dict]:
    """
    Check if company exists and is validated
    
    Args:
        company_slug: Normalized company identifier
        db_paths: Database paths dict
    
    Returns:
        (exists, is_validated, company_data)
        
        Examples:
        - (False, False, None): Company not in database
        - (True, False, None): Exists but updated=false
        - (True, True, data): Exists and validated with data
    """
    
    company_path = f"{db_paths['COMPANIES_DIR']}/{company_slug}.md"
    
    try:
        # Read markdown file
        with open(company_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse YAML
        frontmatter, _ = parse_yaml_frontmatter(content)
        
        if not frontmatter:
            print(f"⚠️ Company file exists but has no YAML: {company_slug}")
            return True, False, None
        
        # Check validation status
        is_validated = frontmatter.get('updated', False) == True
        
        if is_validated:
            return True, True, frontmatter
        else:
            return True, False, frontmatter
    
    except FileNotFoundError:
        return False, False, None
    
    except Exception as e:
        print(f"⚠️ Error reading company file: {e}")
        return False, False, None
```

### Get Company Data

```python
def load_company_data(company_slug: str, db_paths: dict) -> dict:
    """
    Load validated company data
    
    Raises FileNotFoundError if company not found or not validated
    
    Args:
        company_slug: Company identifier
        db_paths: Database paths
    
    Returns:
        Company frontmatter dict
    """
    
    exists, validated, data = check_company_cache(company_slug, db_paths)
    
    if not exists:
        raise FileNotFoundError(f"Company not found: {company_slug}")
    
    if not validated:
        raise ValueError(f"Company not validated: {company_slug} (updated=false)")
    
    return data
```

---

## Role Operations

### Save Role Analysis

```python
def save_role_analysis(role_frontmatter: dict, markdown_body: str, db_paths: dict) -> tuple[bool, str]:
    """
    Save role analysis with YAML frontmatter
    
    Args:
        role_frontmatter: Role YAML data
        markdown_body: Analysis markdown
        db_paths: Database paths
    
    Returns:
        (success, role_path)
    """
    
    role_id = role_frontmatter['role_id']
    role_path = f"{db_paths['ROLES_DIR']}/{role_id}.md"
    
    try:
        # Create complete document
        full_document = create_yaml_document(role_frontmatter, markdown_body)
        
        # Save to file
        with open(role_path, 'w', encoding='utf-8') as f:
            f.write(full_document)
        
        print(f"✅ Saved: db/jobs/analyzed/{role_id}.md")
        return True, role_path
    
    except Exception as e:
        print(f"❌ Failed to save role: {e}")
        return False, None
```

### Load Role Data

```python
def load_role_data(role_id: str, db_paths: dict) -> tuple[dict, str]:
    """
    Load role analysis from file
    
    Args:
        role_id: Role identifier
        db_paths: Database paths
    
    Returns:
        (frontmatter, markdown_body)
    """
    
    role_path = f"{db_paths['ROLES_DIR']}/{role_id}.md"
    
    try:
        with open(role_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, body = parse_yaml_frontmatter(content)
        
        if not frontmatter:
            raise ValueError(f"No YAML frontmatter in role: {role_id}")
        
        return frontmatter, body
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Role not found: {role_id}")
```

### Update Role Status

```python
def update_role_status(role_id: str, new_status: str, db_paths: dict) -> bool:
    """
    Update role status in YAML
    
    Valid statuses: New, Applied, Interview, Rejected, Offer, Accepted
    
    Args:
        role_id: Role identifier
        new_status: New status value
        db_paths: Database paths
    
    Returns:
        Success boolean
    """
    
    from datetime import datetime
    
    valid_statuses = ['New', 'Applied', 'Interview', 'Rejected', 'Offer', 'Accepted']
    
    if new_status not in valid_statuses:
        print(f"⚠️ Invalid status: {new_status}")
        print(f"Valid: {', '.join(valid_statuses)}")
        return False
    
    try:
        # Load current data
        frontmatter, body = load_role_data(role_id, db_paths)
        
        # Update status
        old_status = frontmatter.get('status', 'New')
        frontmatter['status'] = new_status
        frontmatter['status_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        # Save back
        role_path = f"{db_paths['ROLES_DIR']}/{role_id}.md"
        updated_doc = create_yaml_document(frontmatter, body)
        
        with open(role_path, 'w', encoding='utf-8') as f:
            f.write(updated_doc)
        
        print(f"✅ Status updated: {old_status} → {new_status}")
        return True
    
    except Exception as e:
        print(f"❌ Status update failed: {e}")
        return False
```

---

## Excel Synchronization

### Sync Single Role to Excel

```python
def sync_role_to_excel(role_frontmatter: dict, db_paths: dict) -> tuple[int, int]:
    """
    Add or update role in Excel database
    
    Args:
        role_frontmatter: Role YAML data
        db_paths: Database paths
    
    Returns:
        (rank, total_jobs) - Role's rank and total job count
    """
    
    import pandas as pd
    from pathlib import Path
    
    excel_path = db_paths['EXCEL_PATH']
    role_id = role_frontmatter['role_id']
    
    try:
        # Check if Excel exists
        if Path(excel_path).exists():
            # Load existing
            df = pd.read_excel(excel_path, sheet_name='Jobs')
        else:
            # Create new DataFrame
            df = pd.DataFrame()
            print("📊 Creating new Excel database")
        
        # Convert frontmatter to Excel row
        excel_row = frontmatter_to_excel_row(role_frontmatter)
        
        # Check if role exists
        if 'role_id' in df.columns and role_id in df['role_id'].values:
            # Update existing row
            idx = df[df['role_id'] == role_id].index[0]
            for col, val in excel_row.items():
                df.at[idx, col] = val
            print(f"📝 Updated existing role: {role_id}")
        else:
            # Add new row
            new_row = pd.DataFrame([excel_row])
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"➕ Added new role: {role_id}")
        
        # Sort by total score (descending)
        df = df.sort_values('score_total', ascending=False, ignore_index=True)
        
        # Calculate ranks
        df['rank'] = range(1, len(df) + 1)
        
        # Get this role's rank
        role_row = df[df['role_id'] == role_id]
        if len(role_row) > 0:
            rank = int(role_row['rank'].iloc[0])
            total_jobs = len(df)
        else:
            rank = None
            total_jobs = len(df)
        
        # Save Excel
        df.to_excel(excel_path, index=False, sheet_name='Jobs', engine='openpyxl')
        
        print(f"✅ Excel synced: {excel_path}")
        
        return rank, total_jobs
    
    except Exception as e:
        print(f"❌ Excel sync failed: {e}")
        print("Role saved as YAML - Excel can be rebuilt later")
        return None, None


def frontmatter_to_excel_row(frontmatter: dict) -> dict:
    """
    Convert YAML frontmatter to Excel row format
    
    Args:
        frontmatter: Role YAML data
    
    Returns:
        Dict with Excel column names and values
    """
    
    return {
        # IDs
        'role_id': frontmatter['role_id'],
        'company_id': frontmatter['company_id'],
        
        # Basic info
        'date_analyzed': frontmatter['date_analyzed'],
        'company_name': frontmatter['company_name'],
        'position_title': frontmatter['position_title'],
        'location': frontmatter['location'],
        'job_url': frontmatter['job_url'],
        
        # Scores
        'score_match': float(frontmatter['score_match']),
        'score_income': float(frontmatter['score_income']),
        'score_growth': float(frontmatter['score_growth']),
        'score_lowprep': float(frontmatter['score_lowprep']),
        'score_stress': float(frontmatter['score_stress']),
        'score_location': float(frontmatter['score_location']),
        'score_total': float(frontmatter['score_total']),
        
        # Classification
        'priority': frontmatter['priority'],
        'status': frontmatter.get('status', 'New'),
        
        # Details
        'income_estimate': int(frontmatter['income_estimate']),
        'prep_hours': int(frontmatter['prep_hours']),
        'best_cv': frontmatter['best_cv'],
        
        # File path
        'analysis_path': f"jobs/analyzed/{frontmatter['role_id']}.md"
    }
```

### Rebuild Excel from YAML

```python
def rebuild_excel_from_yaml(db_paths: dict) -> int:
    """
    Rebuild entire Excel database from all YAML role files
    
    Use when:
    - Excel is corrupted or lost
    - Need to rebuild from markdown source
    - After manual YAML edits
    
    Args:
        db_paths: Database paths
    
    Returns:
        Number of roles synced
    """
    
    import pandas as pd
    from pathlib import Path
    
    print("🔄 Rebuilding Excel from YAML files...")
    
    roles_dir = Path(db_paths['ROLES_DIR'])
    
    # Get all role files
    role_files = list(roles_dir.glob('*.md'))
    
    if not role_files:
        print("⚠️ No role files found")
        return 0
    
    print(f"📄 Found {len(role_files)} role files")
    
    # Collect all role data
    all_roles = []
    skipped = []
    
    for role_file in role_files:
        try:
            with open(role_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, _ = parse_yaml_frontmatter(content)
            
            if frontmatter and 'role_id' in frontmatter:
                excel_row = frontmatter_to_excel_row(frontmatter)
                all_roles.append(excel_row)
            else:
                skipped.append(role_file.name)
        
        except Exception as e:
            print(f"⚠️ Skipping {role_file.name}: {e}")
            skipped.append(role_file.name)
            continue
    
    if not all_roles:
        print("❌ No valid roles found")
        return 0
    
    # Create DataFrame
    df = pd.DataFrame(all_roles)
    
    # Sort and rank
    df = df.sort_values('score_total', ascending=False, ignore_index=True)
    df['rank'] = range(1, len(df) + 1)
    
    # Save to Excel
    excel_path = db_paths['EXCEL_PATH']
    df.to_excel(excel_path, index=False, sheet_name='Jobs', engine='openpyxl')
    
    print(f"""
✅ Excel rebuilt successfully

Processed: {len(all_roles)} roles
Skipped: {len(skipped)} files
Output: {excel_path}
""")
    
    if skipped:
        print(f"Skipped files: {', '.join(skipped)}")
    
    return len(all_roles)
```

---

## Database Queries

### Get Job Statistics

```python
def get_job_statistics(db_paths: dict) -> dict:
    """
    Calculate summary statistics from Excel
    
    Args:
        db_paths: Database paths
    
    Returns:
        Statistics dictionary
    """
    
    import pandas as pd
    from pathlib import Path
    
    excel_path = db_paths['EXCEL_PATH']
    
    if not Path(excel_path).exists():
        return {
            'error': 'Excel database not found',
            'suggestion': 'Run rebuild_excel_from_yaml()'
        }
    
    try:
        df = pd.read_excel(excel_path, sheet_name='Jobs')
        
        if len(df) == 0:
            return {'total_jobs': 0}
        
        stats = {
            'total_jobs': len(df),
            'avg_score': round(df['score_total'].mean(), 1),
            'highest_score': round(df['score_total'].max(), 1),
            'lowest_score': round(df['score_total'].min(), 1),
            'median_score': round(df['score_total'].median(), 1),
            
            # By priority
            'first_priority': len(df[df['priority'] == 'First']),
            'second_priority': len(df[df['priority'] == 'Second']),
            
            # By status
            'by_status': df['status'].value_counts().to_dict() if 'status' in df.columns else {},
            
            # Top companies
            'top_companies': df['company_name'].value_counts().head(5).to_dict()
        }
        
        return stats
    
    except Exception as e:
        return {'error': str(e)}
```

### Find Roles by Company

```python
def get_company_roles(company_id: str, db_paths: dict) -> list[dict]:
    """
    Get all roles analyzed for a specific company
    
    Args:
        company_id: Company slug
        db_paths: Database paths
    
    Returns:
        List of role frontmatter dicts, sorted by score
    """
    
    from pathlib import Path
    
    roles_dir = Path(db_paths['ROLES_DIR'])
    role_files = list(roles_dir.glob('*.md'))
    
    company_roles = []
    
    for role_file in role_files:
        try:
            with open(role_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, _ = parse_yaml_frontmatter(content)
            
            if frontmatter.get('company_id') == company_id:
                company_roles.append(frontmatter)
        
        except:
            continue
    
    # Sort by total score (descending)
    company_roles.sort(key=lambda x: x.get('score_total', 0), reverse=True)
    
    return company_roles
```

### Search Roles

```python
def search_roles(query: str, db_paths: dict, filters: dict = None) -> list[dict]:
    """
    Search roles by criteria
    
    Args:
        query: Search string (matches title, company)
        db_paths: Database paths
        filters: Optional filters dict
            {
                'min_score': 60,
                'priority': 'First',
                'status': 'New'
            }
    
    Returns:
        Matching roles, sorted by score
    """
    
    from pathlib import Path
    
    roles_dir = Path(db_paths['ROLES_DIR'])
    role_files = list(roles_dir.glob('*.md'))
    
    query_lower = query.lower()
    matching_roles = []
    
    for role_file in role_files:
        try:
            with open(role_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, body = parse_yaml_frontmatter(content)
            
            if not frontmatter:
                continue
            
            # Text search
            title = frontmatter.get('position_title', '').lower()
            company = frontmatter.get('company_name', '').lower()
            
            if query_lower not in title and query_lower not in company:
                continue
            
            # Apply filters
            if filters:
                if 'min_score' in filters:
                    if frontmatter.get('score_total', 0) < filters['min_score']:
                        continue
                
                if 'priority' in filters:
                    if frontmatter.get('priority') != filters['priority']:
                        continue
                
                if 'status' in filters:
                    if frontmatter.get('status') != filters['status']:
                        continue
            
            matching_roles.append(frontmatter)
        
        except:
            continue
    
    # Sort by score
    matching_roles.sort(key=lambda x: x.get('score_total', 0), reverse=True)
    
    return matching_roles
```

---

## Validation

### Validate YAML Structure

```python
def validate_yaml_structure(frontmatter: dict, doc_type: str = 'role') -> tuple[bool, list]:
    """
    Validate YAML frontmatter has required fields
    
    Args:
        frontmatter: YAML dict
        doc_type: 'role' or 'company'
    
    Returns:
        (is_valid, missing_fields)
    """
    
    if doc_type == 'role':
        required_fields = [
            'role_id', 'company_id', 'company_name', 'position_title',
            'job_url', 'date_analyzed',
            'score_match', 'score_income', 'score_growth', 
            'score_lowprep', 'score_stress', 'score_location', 
            'score_total', 'priority',
            'income_estimate', 'prep_hours', 'best_cv'
        ]
    
    elif doc_type == 'company':
        required_fields = [
            'company_id', 'company_name', 'tier', 'tier_score',
            'employees_israel', 'funding_stage',
            'research_date', 'updated', 'website'
        ]
    
    else:
        return False, ['Unknown document type']
    
    missing = [field for field in required_fields if field not in frontmatter]
    
    is_valid = len(missing) == 0
    
    return is_valid, missing
```

### Validate Database Integrity

```python
def validate_database_integrity(db_paths: dict) -> dict:
    """
    Check database health and consistency
    
    For detailed validation implementation, see references/database-operations-examples.md
    """
    
    from pathlib import Path
    
    report = {'timestamp': datetime.now().isoformat(), 'companies': {}, 'roles': {}, 'excel': {}}
    
    # Basic counts
    companies_dir = Path(db_paths['COMPANIES_DIR'])
    roles_dir = Path(db_paths['ROLES_DIR'])
    
    report['companies']['total'] = len(list(companies_dir.glob('*.md')))
    report['roles']['total'] = len(list(roles_dir.glob('*.md')))
    report['excel']['exists'] = Path(db_paths['EXCEL_PATH']).exists()
    
    return report
```

---

## Error Handling

### Safe Operations Wrapper

```python
def safe_db_operation(operation_func, operation_name: str):
    """
    Execute database operation with error handling
    
    For extended error handling patterns, see references/database-operations-examples.md
    """
    
    try:
        result = operation_func()
        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e), 'operation': operation_name}
```

---

## Module Interface

### Input Requirements

```python
{
    'user_config': dict,        # From user-config.yaml
    'USER_DATA_BASE': str,      # Base path
    'operation': str,           # Operation to perform
    'data': dict                # Operation-specific data
}
```

### Output Format

```python
{
    'success': bool,
    'result': any,              # Operation result
    'message': str,
    'error': str or None
}
```

---

## Usage Examples

### Example 1: Check Company Before Analysis

```python
exists, validated, company_data = check_company_cache('nvidia', db_paths)

if exists and validated:
    print(f"✅ {company_data['company_name']} (Tier {company_data['tier']})")
    # Proceed with analysis
elif exists:
    print("⚠️ Please validate company profile first")
    print("Set updated: true in YAML")
else:
    print("Company not in database - starting research...")
```

### Example 2: Save Role and Sync

```python
# After analysis complete
success, role_path = save_role_analysis(
    role_frontmatter=frontmatter,
    markdown_body=analysis_markdown,
    db_paths=db_paths
)

if success:
    # Sync to Excel
    rank, total = sync_role_to_excel(frontmatter, db_paths)
    print(f"✅ Ranked #{rank} of {total} jobs")
```

### Example 3: Rebuild After Manual Edits

```python
# If you edited YAML files manually
count = rebuild_excel_from_yaml(db_paths)
print(f"✅ Rebuilt Excel with {count} roles")
```

---

---

## HTML Synchronization

### Generate HTML Database

```python
def generate_html_database(db_paths: dict) -> tuple[bool, str]:
    """
    Generate complete interactive HTML database from all YAML roles
    
    This is the PRIMARY output format - works everywhere (filesystem, Drive, browser)
    
    Args:
        db_paths: Database paths dict
    
    Returns:
        (success, html_path)
    """
    
    from pathlib import Path
    import sys
    
    # Import the html_generator script
    scripts_dir = Path(__file__).parent.parent / 'scripts'
    sys.path.insert(0, str(scripts_dir))
    
    try:
        from html_generator import load_all_roles, calculate_statistics, generate_html_database
        
        # Load all roles
        roles_dir = Path(db_paths['ROLES_DIR'])
        roles = load_all_roles(roles_dir)
        
        if not roles:
            print("⚠️ No roles found to generate HTML")
            return False, None
        
        # Calculate statistics
        stats = calculate_statistics(roles)
        
        # Generate HTML content
        html_content = generate_html_database(roles, stats)
        
        # Save to file
        html_path = Path(db_paths['DB_DIR']) / 'db.html'
        html_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated HTML database: {html_path}")
        print(f"📋 {len(roles)} jobs | {len(html_content) / 1024:.1f} KB")
        print(f"🌐 Open in browser: file://{html_path}")
        
        return True, str(html_path)
    
    except Exception as e:
        print(f"❌ HTML generation failed: {e}")
        return False, None
```

### Sync After Each Role (Automatic)

```python
def sync_role_to_html(role_frontmatter: dict, db_paths: dict) -> tuple[bool, str]:
    """
    Regenerate HTML database after adding/updating a role
    
    This automatically rebuilds the entire HTML from YAML source.
    Fast operation (~100ms for 50 jobs)
    
    Args:
        role_frontmatter: The role that was just saved
        db_paths: Database paths
    
    Returns:
        (success, html_path)
    """
    
    print("🔄 Syncing to HTML database...")
    
    success, html_path = generate_html_database(db_paths)
    
    if success:
        # Get role's rank
        roles_dir = Path(db_paths['ROLES_DIR'])
        all_roles = load_all_roles(roles_dir)
        all_roles_sorted = sorted(all_roles, key=lambda x: x.get('score_total', 0), reverse=True)
        
        role_id = role_frontmatter['role_id']
        rank = next((i+1 for i, r in enumerate(all_roles_sorted) if r.get('role_id') == role_id), None)
        
        if rank:
            print(f"✅ Ranked #{rank} of {len(all_roles)} jobs")
        
        return True, html_path
    
    return False, None
```

### HTML vs Excel Decision

```python
def sync_database_views(db_paths: dict, generate_excel: bool = False) -> dict:
    """
    Sync database to convenience views
    
    Args:
        db_paths: Database paths
        generate_excel: If True, also generate Excel (default: False)
    
    Returns:
        Results dict with paths and success status
    """
    
    results = {
        'html': {'generated': False, 'path': None},
        'excel': {'generated': False, 'path': None}
    }
    
    # Always generate HTML (primary)
    html_success, html_path = generate_html_database(db_paths)
    results['html']['generated'] = html_success
    results['html']['path'] = html_path
    
    # Optionally generate Excel (legacy)
    if generate_excel:
        try:
            excel_count = rebuild_excel_from_yaml(db_paths)
            results['excel']['generated'] = excel_count > 0
            results['excel']['path'] = db_paths.get('EXCEL_PATH')
        except Exception as e:
            print(f"⚠️ Excel generation skipped: {e}")
    
    return results
```

---

## Unified Workflow

### After Analyzing a Job

```python
# Step 11: Save to YAML (source of truth)
success, role_path = save_role_analysis(
    role_frontmatter=frontmatter,
    markdown_body=analysis_markdown,
    db_paths=db_paths
)

if success:
    # Step 12: Sync to HTML (always)
    html_success, html_path = sync_role_to_html(frontmatter, db_paths)
    
    if html_success:
        print(f"✨ View your database: {html_path}")
        print("👉 Double-click to open in browser")
        
        # Optional: Also sync to Excel if user wants
        # (Only needed for users who still use Excel)
        if user_config.get('generate_excel', False):
            rank, total = sync_role_to_excel(frontmatter, db_paths)
            print(f"📋 Also generated Excel: #{rank} of {total}")
```

### Rebuild All Views

```python
# After manual YAML edits or database cleanup
results = sync_database_views(
    db_paths=db_paths,
    generate_excel=True  # Set to True if user still uses Excel
)

if results['html']['generated']:
    print(f"✅ HTML: {results['html']['path']}")

if results['excel']['generated']:
    print(f"✅ Excel: {results['excel']['path']}")
```

---

## Module Version

**Version**: v1.1.0  
**Architecture**: Hybrid YAML + HTML (+ Excel optional)  
**Primary Output**: Interactive HTML  
**Dependencies**: pyyaml (required), pandas/openpyxl (optional for Excel)  
**Status**: Production Ready ✅

---

**Last Updated**: October 2025  
**Token Budget**: ~7K tokens (loaded as needed)
