#!/usr/bin/env python3
"""
Recipe Card Generator
Generates beautiful HTML recipe cards from YAML files.

Usage:
    python generate_card.py <recipe_id>
    python generate_card.py tomato-rice-soup
    python generate_card.py --all  # Generate all recipes
"""

import yaml
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Configuration
BASE_DIR = Path("/Users/gursannikov/MyDrive/claude-skills-data/recipe-manager")
RECIPES_DIR = BASE_DIR / "recipes"
EXPORTS_DIR = BASE_DIR / "exports"

# Color themes based on recipe type/tags
THEMES = {
    "default": {
        "gradient": "from-emerald-500 to-lime-500",
        "bg": "from-emerald-50 via-white to-lime-50",
        "accent": "emerald",
        "emoji": "🍳"
    },
    "soup": {
        "gradient": "from-amber-500 via-orange-500 to-red-500",
        "bg": "from-amber-50 via-white to-red-50",
        "accent": "amber",
        "emoji": "🍲"
    },
    "tomato": {
        "gradient": "from-red-500 to-orange-500",
        "bg": "from-red-50 via-white to-orange-50",
        "accent": "red",
        "emoji": "🍅"
    },
    "breakfast": {
        "gradient": "from-yellow-400 to-orange-500",
        "bg": "from-yellow-50 via-white to-orange-50",
        "accent": "yellow",
        "emoji": "🍳"
    },
    "meat": {
        "gradient": "from-rose-600 to-red-700",
        "bg": "from-rose-50 via-white to-red-50",
        "accent": "rose",
        "emoji": "🥩"
    },
    "vegetarian": {
        "gradient": "from-green-500 to-emerald-600",
        "bg": "from-green-50 via-white to-emerald-50",
        "accent": "green",
        "emoji": "🥗"
    },
    "ninja": {
        "gradient": "from-slate-700 to-zinc-800",
        "bg": "from-slate-50 via-white to-zinc-50",
        "accent": "slate",
        "emoji": "🔥"
    },
    "chicken": {
        "gradient": "from-amber-400 to-yellow-500",
        "bg": "from-amber-50 via-white to-yellow-50",
        "accent": "amber",
        "emoji": "🐔"
    },
    "oven": {
        "gradient": "from-orange-500 to-red-600",
        "bg": "from-orange-50 via-white to-red-50",
        "accent": "orange",
        "emoji": "🫕"
    }
}


def get_theme(recipe: dict) -> dict:
    """Determine theme based on recipe tags/type."""
    tags = recipe.get("tags", [])
    recipe_type = recipe.get("type", "").lower()
    
    # Check type first
    if "ninja" in recipe_type.lower():
        return THEMES["ninja"]
    if "oven" in recipe_type.lower():
        return THEMES["oven"]
    
    # Then check tags
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower in THEMES:
            return THEMES[tag_lower]
    
    return THEMES["default"]


def generate_ingredient_html(ingredients: list, accent: str) -> str:
    """Generate HTML for ingredients list."""
    items = []
    for idx, item in enumerate(ingredients, 1):
        items.append(f'''
                    <div class="flex items-center gap-3 p-2 bg-gray-50 rounded-xl hover:bg-{accent}-50 transition-colors">
                        <span class="w-7 h-7 bg-gradient-to-br from-{accent}-500 to-{accent}-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">{idx}</span>
                        <span class="text-gray-700 text-sm">{item}</span>
                    </div>''')
    return "\n".join(items)


def generate_instructions_html(instructions: list, gradient: str) -> str:
    """Generate HTML for instructions list."""
    items = []
    for idx, step in enumerate(instructions, 1):
        items.append(f'''
                    <div class="flex gap-3">
                        <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-br {gradient} text-white rounded-full flex items-center justify-center font-bold text-sm shadow-lg">{idx}</div>
                        <div class="flex-1 bg-gray-50 p-3 rounded-xl"><p class="text-gray-700 text-sm">{step}</p></div>
                    </div>''')
    return "\n".join(items)


def generate_notes_html(notes: list) -> str:
    """Generate HTML for notes list."""
    items = []
    for note in notes:
        items.append(f'''
                    <div class="flex items-start gap-2 p-3 bg-yellow-50 rounded-xl border border-yellow-100">
                        <span class="text-lg">💡</span>
                        <p class="text-gray-700 text-sm">{note}</p>
                    </div>''')
    return "\n".join(items)


def generate_tags_html(tags: list) -> str:
    """Generate HTML for tags."""
    items = []
    for tag in tags:
        items.append(f'<span class="bg-white px-3 py-1 rounded-full text-xs font-medium text-gray-600 shadow-sm border border-gray-100">#{tag}</span>')
    return "\n            ".join(items)


def generate_html(recipe: dict) -> str:
    """Generate complete HTML for a recipe card."""
    theme = get_theme(recipe)
    
    # Extract recipe data with defaults
    name = recipe.get("name", "Unknown Recipe")
    name_en = recipe.get("name_en", "")
    icon = recipe.get("icon", theme["emoji"])
    recipe_type = recipe.get("type", "")
    status = recipe.get("status", "To try")
    servings = recipe.get("servings", "")
    prep_time = recipe.get("prep_time", "")
    cook_time = recipe.get("cook_time", "")
    ingredients = recipe.get("ingredients", [])
    instructions = recipe.get("instructions", [])
    notes = recipe.get("notes", [])
    tags = recipe.get("tags", [])
    source = recipe.get("source", {})
    credit = source.get("credit", "")
    date_added = source.get("date_added", "")
    
    # Build meta cards
    meta_cards = []
    if servings:
        meta_cards.append(f'''
                    <div class="flex items-center gap-2 bg-{theme["accent"]}-50 px-3 py-2 rounded-xl">
                        <span class="text-xl">👥</span>
                        <div>
                            <p class="text-xs text-gray-500">Servings</p>
                            <p class="font-semibold text-{theme["accent"]}-700 text-sm">{servings}</p>
                        </div>
                    </div>''')
    if prep_time:
        meta_cards.append(f'''
                    <div class="flex items-center gap-2 bg-blue-50 px-3 py-2 rounded-xl">
                        <span class="text-xl">⏱️</span>
                        <div>
                            <p class="text-xs text-gray-500">Prep</p>
                            <p class="font-semibold text-blue-700 text-sm">{prep_time}</p>
                        </div>
                    </div>''')
    if cook_time:
        meta_cards.append(f'''
                    <div class="flex items-center gap-2 bg-orange-50 px-3 py-2 rounded-xl">
                        <span class="text-xl">🔥</span>
                        <div>
                            <p class="text-xs text-gray-500">Cook</p>
                            <p class="font-semibold text-orange-700 text-sm">{cook_time}</p>
                        </div>
                    </div>''')
    meta_cards.append(f'''
                    <div class="flex items-center gap-2 bg-purple-50 px-3 py-2 rounded-xl">
                        <span class="text-xl">📋</span>
                        <div>
                            <p class="text-xs text-gray-500">Status</p>
                            <p class="font-semibold text-purple-700 text-sm">{status}</p>
                        </div>
                    </div>''')
    
    html = f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | {name_en}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700&display=swap');
        body {{ font-family: 'Heebo', sans-serif; }}
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br {theme["bg"]} p-4">
    <div class="max-w-2xl mx-auto">
        <div class="bg-white rounded-3xl shadow-xl overflow-hidden mb-4">
            <!-- Header -->
            <div class="bg-gradient-to-r {theme["gradient"]} p-6 text-white relative overflow-hidden">
                <div class="absolute top-0 right-0 text-8xl opacity-20 transform translate-x-6 -translate-y-2">{icon}</div>
                <div class="relative z-10">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-4xl">{icon}</span>
                        <span class="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">{recipe_type}</span>
                    </div>
                    <h1 class="text-3xl font-bold mb-1">{name}</h1>
                    <p class="text-white/80">{name_en}</p>
                </div>
            </div>

            <!-- Meta -->
            <div class="p-4 border-b border-gray-100">
                <div class="flex flex-wrap gap-3 justify-center">
                    {"".join(meta_cards)}
                </div>
            </div>

            <!-- Tabs -->
            <div class="flex border-b border-gray-100">
                <button onclick="showTab('ingredients')" id="tab-ingredients" class="flex-1 py-3 text-center font-medium text-sm text-{theme["accent"]}-600 border-b-2 border-{theme["accent"]}-500 bg-{theme["accent"]}-50/50">🥗 מצרכים</button>
                <button onclick="showTab('instructions')" id="tab-instructions" class="flex-1 py-3 text-center font-medium text-sm text-gray-400 hover:text-gray-600">👨‍🍳 הכנה</button>
                <button onclick="showTab('notes')" id="tab-notes" class="flex-1 py-3 text-center font-medium text-sm text-gray-400 hover:text-gray-600">📝 טיפים</button>
            </div>

            <!-- Content -->
            <div class="p-4 max-h-96 overflow-y-auto">
                <div id="content-ingredients" class="space-y-2">
                    {generate_ingredient_html(ingredients, theme["accent"])}
                </div>
                <div id="content-instructions" class="space-y-3 hidden">
                    {generate_instructions_html(instructions, theme["gradient"])}
                </div>
                <div id="content-notes" class="space-y-2 hidden">
                    {generate_notes_html(notes) if notes else '<p class="text-gray-400 text-center">אין הערות</p>'}
                </div>
            </div>
        </div>

        <!-- Tags -->
        <div class="flex flex-wrap gap-2 justify-center mb-4">
            {generate_tags_html(tags)}
        </div>

        <!-- Credit -->
        <div class="text-center text-xs text-gray-400">
            <p>Credit: {credit} • Added: {date_added}</p>
        </div>
    </div>

    <script>
        function showTab(tab) {{
            document.getElementById('content-ingredients').classList.add('hidden');
            document.getElementById('content-instructions').classList.add('hidden');
            document.getElementById('content-notes').classList.add('hidden');
            
            document.querySelectorAll('[id^="tab-"]').forEach(el => {{
                el.className = 'flex-1 py-3 text-center font-medium text-sm text-gray-400 hover:text-gray-600';
            }});
            
            document.getElementById('content-' + tab).classList.remove('hidden');
            document.getElementById('tab-' + tab).className = 'flex-1 py-3 text-center font-medium text-sm text-{theme["accent"]}-600 border-b-2 border-{theme["accent"]}-500 bg-{theme["accent"]}-50/50';
        }}
    </script>
</body>
</html>'''
    
    return html


def find_recipe(recipe_id: str) -> Optional[Path]:
    """Find a recipe YAML file by ID."""
    for status_dir in ["to-try", "tried", "perfected"]:
        path = RECIPES_DIR / status_dir / f"{recipe_id}.yaml"
        if path.exists():
            return path
    return None


def generate_card(recipe_id: str, open_browser: bool = True) -> Optional[Path]:
    """Generate HTML card for a recipe."""
    # Find recipe file
    recipe_path = find_recipe(recipe_id)
    if not recipe_path:
        print(f"❌ Recipe not found: {recipe_id}")
        return None
    
    # Load recipe
    with open(recipe_path, 'r', encoding='utf-8') as f:
        recipe = yaml.safe_load(f)
    
    # Generate HTML
    html = generate_html(recipe)
    
    # Ensure exports dir exists
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save HTML
    output_path = EXPORTS_DIR / f"{recipe_id}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated: {output_path}")
    
    # Open in browser
    if open_browser:
        subprocess.run(["open", str(output_path)])
    
    return output_path


def generate_all(open_browser: bool = False):
    """Generate cards for all recipes."""
    count = 0
    errors = []
    for status_dir in ["to-try", "tried", "perfected"]:
        dir_path = RECIPES_DIR / status_dir
        if not dir_path.exists():
            continue
        for yaml_file in dir_path.glob("*.yaml"):
            recipe_id = yaml_file.stem
            try:
                generate_card(recipe_id, open_browser=False)
                count += 1
            except Exception as e:
                errors.append(f"{recipe_id}: {e}")
                print(f"⚠️  Skipped {recipe_id}: {e}")
    
    print(f"\n✅ Generated {count} recipe cards in {EXPORTS_DIR}")
    if errors:
        print(f"⚠️  {len(errors)} errors occurred")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_card.py <recipe_id>")
        print("       python generate_card.py --all")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "--all":
        generate_all()
    else:
        generate_card(arg)
