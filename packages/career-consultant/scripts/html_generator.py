"""
HTML Database Generator for Israeli Tech Career Consultant

Generates a self-contained, interactive HTML database from YAML role files.
Features: sorting, filtering, searching, pagination, export, responsive design.

Usage:
    python html_generator.py

Dependencies:
    - pyyaml (for reading YAML frontmatter)
    - Standard library only otherwise

Author: Gur Sannikov
Version: 9.1.0
"""

import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


def parse_yaml_frontmatter(markdown_content: str) -> Tuple[Dict, str]:
    """
    Extract YAML frontmatter and markdown body from a markdown file.
    
    Args:
        markdown_content: Complete markdown file content
    
    Returns:
        Tuple of (frontmatter_dict, markdown_body)
    """
    if not markdown_content.startswith('---'):
        return {}, markdown_content
    
    parts = markdown_content.split('---', 2)
    
    if len(parts) < 3:
        return {}, markdown_content
    
    try:
        yaml_text = parts[1].strip()
        frontmatter = yaml.safe_load(yaml_text) or {}
        markdown_body = parts[2].strip()
        return frontmatter, markdown_body
    except yaml.YAMLError as e:
        print(f"⚠️ YAML parsing error: {e}")
        return {}, markdown_content


def load_all_roles(roles_dir: Path) -> List[Dict]:
    """
    Load all role files from the roles directory.
    
    Args:
        roles_dir: Path to roles directory
    
    Returns:
        List of role frontmatter dictionaries
    """
    roles = []
    role_files = list(roles_dir.glob('*.md'))
    
    print(f"📄 Found {len(role_files)} role files")
    
    for role_file in role_files:
        try:
            with open(role_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, _ = parse_yaml_frontmatter(content)
            
            if frontmatter and 'role_id' in frontmatter:
                roles.append(frontmatter)
            else:
                print(f"⚠️ Skipping {role_file.name}: No valid frontmatter")
        
        except Exception as e:
            print(f"⚠️ Error reading {role_file.name}: {e}")
            continue
    
    return roles


def calculate_statistics(roles: List[Dict]) -> Dict:
    """
    Calculate summary statistics from roles data.
    
    Args:
        roles: List of role dictionaries
    
    Returns:
        Dictionary with statistics
    """
    if not roles:
        return {
            'total_jobs': 0,
            'avg_score': 0,
            'highest_score': 0,
            'median_score': 0,
            'first_priority': 0,
            'second_priority': 0,
            'third_priority': 0,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    
    scores = [r.get('score_total', 0) for r in roles]
    scores_sorted = sorted(scores)
    
    stats = {
        'total_jobs': len(roles),
        'avg_score': round(sum(scores) / len(scores), 1),
        'highest_score': round(max(scores), 1),
        'lowest_score': round(min(scores), 1),
        'median_score': round(scores_sorted[len(scores_sorted) // 2], 1),
        'first_priority': len([r for r in roles if r.get('priority') == 'First']),
        'second_priority': len([r for r in roles if r.get('priority') == 'Second']),
        'third_priority': len([r for r in roles if r.get('priority') == 'Third']),
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    return stats


def generate_html_database(roles: List[Dict], stats: Dict) -> str:
    """
    Generate complete HTML database with interactive DataTables.
    
    Args:
        roles: List of role dictionaries
        stats: Statistics dictionary
    
    Returns:
        Complete HTML string
    """
    
    # Sort roles by total score (descending)
    roles_sorted = sorted(roles, key=lambda x: x.get('score_total', 0), reverse=True)
    
    # Generate table rows
    table_rows = ""
    for idx, role in enumerate(roles_sorted, 1):
        priority_class = f"priority-{role.get('priority', 'Third').lower()}"
        score_total = role.get('score_total', 0)
        
        # Generate score bar HTML
        score_bar_html = f'''
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: bold; min-width: 35px;">{score_total}</span>
                <div class="score-bar">
                    <div class="score-fill" style="width: {score_total}%"></div>
                </div>
            </div>
        '''
        
        # Status badge
        status = role.get('status', 'New')
        status_class = f"status-{status.lower()}"
        
        table_rows += f'''
            <tr>
                <td style="text-align: center;">{idx}</td>
                <td><strong>{role.get('company_name', 'Unknown')}</strong></td>
                <td>{role.get('position_title', 'Unknown')}</td>
                <td>{score_bar_html}</td>
                <td style="text-align: center;">{role.get('score_match', 0)}</td>
                <td style="text-align: center;">{role.get('score_income', 0)}</td>
                <td style="text-align: center;">{role.get('score_growth', 0)}</td>
                <td style="text-align: center;">{role.get('score_lowprep', 0)}</td>
                <td style="text-align: center;">{role.get('score_stress', 0)}</td>
                <td style="text-align: center;">{role.get('score_location', 0)}</td>
                <td class="{priority_class}" style="text-align: center; font-weight: bold;">{role.get('priority', 'Third')}</td>
                <td><span class="status-badge {status_class}">{status}</span></td>
                <td style="text-align: center;">{role.get('best_cv', 'N/A')}</td>
                <td style="text-align: center;">{role.get('date_analyzed', 'N/A')}</td>
                <td style="text-align: center; white-space: nowrap;">
                    <a href="{role.get('job_url', '#')}" target="_blank" class="action-link">🔗 Job</a>
                    <br>
                    <a href="../jobs/analyzed/{role.get('role_id', '')}.md" class="action-link">📄 Analysis</a>
                </td>
            </tr>
        '''
    
    # Complete HTML document
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Israeli Tech Career Consultant - Job Database</title>
    
    <!-- DataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/responsive/2.5.0/css/responsive.dataTables.min.css">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.95em;
            font-weight: 500;
        }}
        
        .table-container {{
            padding: 30px;
        }}
        
        table.dataTable {{
            width: 100% !important;
            border-collapse: collapse;
            font-size: 0.9em;
        }}
        
        table.dataTable thead th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 8px;
            font-weight: 600;
            border: none;
            white-space: nowrap;
        }}
        
        table.dataTable tbody td {{
            padding: 12px 8px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        table.dataTable tbody tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .score-bar {{
            flex: 1;
            height: 24px;
            background: #e9ecef;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }}
        
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ef4444 0%, #f59e0b 40%, #84cc16 70%, #22c55e 100%);
            transition: width 0.3s ease;
            border-radius: 12px;
        }}
        
        .priority-first {{
            color: #22c55e;
            font-weight: bold;
        }}
        
        .priority-second {{
            color: #3b82f6;
            font-weight: 600;
        }}
        
        .priority-third {{
            color: #94a3b8;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .status-new {{
            background: #dbeafe;
            color: #1e40af;
        }}
        
        .status-applied {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .status-interview {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-rejected {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .status-offer {{
            background: #ddd6fe;
            color: #5b21b6;
        }}
        
        .status-accepted {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .action-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        .action-link:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}
        
        .dataTables_wrapper .dataTables_filter input {{
            border: 2px solid #e9ecef;
            border-radius: 6px;
            padding: 8px 12px;
            margin-left: 8px;
            font-size: 0.95em;
        }}
        
        .dataTables_wrapper .dataTables_filter input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .dataTables_wrapper .dataTables_length select {{
            border: 2px solid #e9ecef;
            border-radius: 6px;
            padding: 6px 10px;
            margin: 0 8px;
        }}
        
        div.dt-buttons {{
            margin-bottom: 15px;
        }}
        
        .dt-button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            margin-right: 8px !important;
            font-weight: 500 !important;
            transition: transform 0.2s, box-shadow 0.2s !important;
        }}
        
        .dt-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .stats-container {{
                grid-template-columns: repeat(2, 1fr);
                padding: 20px;
                gap: 15px;
            }}
            
            .stat-value {{
                font-size: 2em;
            }}
            
            .table-container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Israeli Tech Career Consultant</h1>
            <p>Job Analysis Database - Generated {stats['generated_date']}</p>
        </div>
        
        <!-- Statistics -->
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">{stats['total_jobs']}</div>
                <div class="stat-label">Total Jobs Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['avg_score']}</div>
                <div class="stat-label">Average Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['highest_score']}</div>
                <div class="stat-label">Highest Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['median_score']}</div>
                <div class="stat-label">Median Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['first_priority']}</div>
                <div class="stat-label">First Priority</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['second_priority']}</div>
                <div class="stat-label">Second Priority</div>
            </div>
        </div>
        
        <!-- Data Table -->
        <div class="table-container">
            <table id="jobsTable" class="display responsive nowrap" style="width:100%">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Company</th>
                        <th>Position</th>
                        <th>Total Score</th>
                        <th>Match</th>
                        <th>Income</th>
                        <th>Growth</th>
                        <th>LowPrep</th>
                        <th>Stress</th>
                        <th>Location</th>
                        <th>Priority</th>
                        <th>Status</th>
                        <th>Best CV</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Israeli Tech Career Consultant</strong> v9.1.0 | MIT License | Generated from YAML source files</p>
            <p>Sort, filter, and export your job analysis data. This is a read-only view - edit YAML files to update data.</p>
        </div>
    </div>
    
    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
    <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.print.min.js"></script>
    <script src="https://cdn.datatables.net/responsive/2.5.0/js/dataTables.responsive.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
    
    <script>
        $(document).ready(function() {{
            $('#jobsTable').DataTable({{
                order: [[3, 'desc']], // Sort by total score descending
                pageLength: 25,
                responsive: true,
                dom: 'Bfrtip',
                buttons: [
                    {{
                        extend: 'copy',
                        text: '📋 Copy'
                    }},
                    {{
                        extend: 'excel',
                        text: '📊 Excel'
                    }},
                    {{
                        extend: 'csv',
                        text: '📄 CSV'
                    }},
                    {{
                        extend: 'pdf',
                        text: '📑 PDF',
                        orientation: 'landscape',
                        pageSize: 'A3'
                    }},
                    {{
                        extend: 'print',
                        text: '🖨️ Print'
                    }}
                ],
                columnDefs: [
                    {{ orderable: false, targets: 14 }}, // Actions column not sortable
                    {{ className: 'dt-center', targets: [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] }}
                ],
                language: {{
                    search: "🔍 Search:",
                    lengthMenu: "Show _MENU_ jobs per page",
                    info: "Showing _START_ to _END_ of _TOTAL_ jobs",
                    infoEmpty: "No jobs to display",
                    infoFiltered: "(filtered from _MAX_ total jobs)",
                    paginate: {{
                        first: "First",
                        last: "Last",
                        next: "Next →",
                        previous: "← Previous"
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>'''
    
    return html


def main():
    """Main execution function."""
    
    print("🚀 HTML Database Generator")
    print("=" * 50)
    
    # Get paths from user config
    # For standalone script, use default paths
    user_data_base = Path.home() / "MyDrive" / "career-consultant.skill" / "user-data"
    roles_dir = user_data_base / "jobs" / "analyzed"
    output_path = user_data_base / "reports" / "companies-db.html"
    
    # Check if roles directory exists
    if not roles_dir.exists():
        print(f"❌ Roles directory not found: {roles_dir}")
        print("Please update the paths in the script or run from correct location.")
        return
    
    # Load all roles
    print(f"\n📂 Loading roles from: {roles_dir}")
    roles = load_all_roles(roles_dir)
    
    if not roles:
        print("❌ No valid role files found!")
        return
    
    print(f"✅ Loaded {len(roles)} roles")
    
    # Calculate statistics
    print("\n📊 Calculating statistics...")
    stats = calculate_statistics(roles)
    
    print(f"   Total Jobs: {stats['total_jobs']}")
    print(f"   Average Score: {stats['avg_score']}")
    print(f"   Highest Score: {stats['highest_score']}")
    print(f"   First Priority: {stats['first_priority']}")
    
    # Generate HTML
    print("\n🔨 Generating HTML database...")
    html_content = generate_html_database(roles, stats)
    
    # Save to file
    print(f"\n💾 Saving to: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Success! Generated: {output_path}")
    print(f"📊 File size: {len(html_content) / 1024:.1f} KB")
    print("\n🌐 To view:")
    print(f"   Double-click the file to open in your browser")
    print(f"   Or open: file://{output_path}")
    print("\n✨ Features available:")
    print("   • Sort by clicking column headers")
    print("   • Search using the search box")
    print("   • Export to Excel, CSV, PDF")
    print("   • Print-friendly format")
    print("   • Responsive design (works on mobile)")


if __name__ == "__main__":
    main()
