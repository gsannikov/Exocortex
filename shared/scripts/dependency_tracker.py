#!/usr/bin/env python3
"""
Dependency Tracker for Claude Skills Monorepo

This script manages the dependency graph between files, detecting which files
are out of date and need to be rebuilt when their dependencies change.

Usage:
    python dependency_tracker.py status              # Show dependency status
    python dependency_tracker.py check <file>        # Check specific file
    python dependency_tracker.py graph               # Display dependency graph
    python dependency_tracker.py rebuild-order       # Show files needing update
    python dependency_tracker.py affected <file>     # Show what depends on a file
"""

import argparse
import hashlib
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

import yaml


def get_repo_root() -> Path:
    """Get the repository root directory."""
    script_path = Path(__file__).resolve()
    # Navigate up from shared/scripts/ to repo root
    return script_path.parent.parent.parent


def load_dependencies(repo_root: Path) -> dict:
    """Load the dependencies.yaml manifest."""
    deps_file = repo_root / "dependencies.yaml"
    if not deps_file.exists():
        print(f"Error: {deps_file} not found")
        sys.exit(1)

    with open(deps_file, "r") as f:
        return yaml.safe_load(f)


def get_file_hash(filepath: Path) -> str:
    """Calculate SHA256 hash of file content."""
    if not filepath.exists():
        return ""

    # For directories, hash the directory listing
    if filepath.is_dir():
        files = sorted(filepath.rglob("*"))
        content = "\n".join(str(f.relative_to(filepath)) for f in files if f.is_file())
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def get_git_last_modified(filepath: Path, repo_root: Path) -> Optional[str]:
    """Get the last git commit date for a file."""
    try:
        rel_path = filepath.relative_to(repo_root)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", "--", str(rel_path)],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_git_last_commit(filepath: Path, repo_root: Path) -> Optional[str]:
    """Get the last git commit hash for a file."""
    try:
        rel_path = filepath.relative_to(repo_root)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%h", "--", str(rel_path)],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


class DependencyGraph:
    """Manages the dependency graph and tracks file states."""

    def __init__(self, repo_root: Path, config: dict):
        self.repo_root = repo_root
        self.config = config
        self.nodes = {node["path"]: node for node in config.get("nodes", [])}
        self.settings = config.get("settings", {})

        # Build reverse dependency map (what depends on what)
        self.dependents = defaultdict(list)
        for node in config.get("nodes", []):
            for dep in node.get("depends_on", []):
                self.dependents[dep].append(node["path"])

    def get_node(self, path: str) -> Optional[dict]:
        """Get node info for a path."""
        return self.nodes.get(path)

    def get_dependents(self, path: str) -> list:
        """Get all files that depend on the given path."""
        return self.dependents.get(path, [])

    def get_all_affected(self, path: str, visited: set = None) -> set:
        """Recursively get all files affected by changes to path."""
        if visited is None:
            visited = set()

        if path in visited:
            return visited

        visited.add(path)

        for dependent in self.get_dependents(path):
            self.get_all_affected(dependent, visited)

        return visited

    def get_file_state(self, path: str) -> dict:
        """Get current state of a file."""
        filepath = self.repo_root / path

        # Handle glob patterns (e.g., packages/career-consultant/modules/)
        if path.endswith("/"):
            filepath = self.repo_root / path.rstrip("/")

        exists = filepath.exists()

        return {
            "path": path,
            "exists": exists,
            "hash": get_file_hash(filepath) if exists else None,
            "git_commit": get_git_last_commit(filepath, self.repo_root) if exists else None,
            "git_date": get_git_last_modified(filepath, self.repo_root) if exists else None,
        }

    def check_needs_update(self, path: str) -> tuple[bool, list]:
        """
        Check if a file needs to be updated based on its dependencies.
        Returns (needs_update, list of changed dependencies).
        """
        node = self.get_node(path)
        if not node:
            return False, []

        deps = node.get("depends_on", [])
        if not deps:
            return False, []  # Source files don't need updates

        file_state = self.get_file_state(path)
        if not file_state["exists"]:
            return True, ["file does not exist"]

        file_commit = file_state["git_commit"]
        changed_deps = []

        for dep in deps:
            dep_state = self.get_file_state(dep)
            if not dep_state["exists"]:
                continue

            dep_commit = dep_state["git_commit"]

            # Compare git commits to see if dependency is newer
            if dep_commit and file_commit:
                # Check if dep was modified after the file
                try:
                    result = subprocess.run(
                        ["git", "log", "--oneline", f"{file_commit}..{dep_commit}", "--", dep],
                        cwd=self.repo_root,
                        capture_output=True,
                        text=True
                    )
                    if result.stdout.strip():
                        changed_deps.append(dep)
                except Exception:
                    pass

        return len(changed_deps) > 0, changed_deps

    def get_rebuild_order(self) -> list:
        """
        Get topologically sorted list of files that need updating.
        Returns files in order they should be rebuilt (dependencies first).
        """
        needs_update = []

        for path in self.nodes:
            needs, reasons = self.check_needs_update(path)
            if needs:
                needs_update.append((path, reasons))

        # Sort by dependency depth (sources first, then derived)
        def get_depth(path):
            node = self.get_node(path)
            if not node:
                return 0
            deps = node.get("depends_on", [])
            if not deps:
                return 0
            tracked_deps = [d for d in deps if d in self.nodes]
            if not tracked_deps:
                return 1  # Has deps but none are tracked nodes
            return 1 + max(get_depth(d) for d in tracked_deps)

        needs_update.sort(key=lambda x: get_depth(x[0]))
        return needs_update

    def print_status(self):
        """Print overall dependency status."""
        print("=" * 60)
        print("DEPENDENCY STATUS")
        print("=" * 60)

        # Group by type
        by_type = defaultdict(list)
        for path, node in self.nodes.items():
            by_type[node.get("type", "unknown")].append(path)

        for file_type in ["source", "derived", "documentation", "marketing"]:
            if file_type not in by_type:
                continue

            print(f"\n{file_type.upper()} FILES:")
            print("-" * 40)

            for path in sorted(by_type[file_type]):
                state = self.get_file_state(path)
                needs, reasons = self.check_needs_update(path)

                status = ""
                if not state["exists"]:
                    status = "[MISSING]"
                elif needs:
                    status = f"[NEEDS UPDATE: {', '.join(reasons)}]"
                else:
                    status = "[OK]"

                commit = state.get("git_commit", "?")[:7] if state.get("git_commit") else "?"
                print(f"  {path}")
                print(f"    Status: {status}")
                if state["exists"]:
                    print(f"    Last commit: {commit}")

        # Summary
        total = len(self.nodes)
        needs_update = len([p for p in self.nodes if self.check_needs_update(p)[0]])

        print("\n" + "=" * 60)
        print(f"SUMMARY: {needs_update}/{total} files need attention")
        print("=" * 60)

    def print_graph(self):
        """Print the dependency graph in ASCII format."""
        print("=" * 60)
        print("DEPENDENCY GRAPH")
        print("=" * 60)

        # Find root nodes (no dependencies)
        roots = [p for p, n in self.nodes.items() if not n.get("depends_on")]

        def print_tree(path, prefix="", is_last=True):
            node = self.get_node(path)
            node_type = node.get("type", "?")[0].upper() if node else "?"

            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}[{node_type}] {path}")

            deps = self.get_dependents(path)
            new_prefix = prefix + ("    " if is_last else "│   ")

            for i, dep in enumerate(sorted(deps)):
                print_tree(dep, new_prefix, i == len(deps) - 1)

        for i, root in enumerate(sorted(roots)):
            if i > 0:
                print()
            print_tree(root, "", True)

    def print_affected(self, path: str):
        """Print all files affected by changes to path."""
        print(f"Files affected by changes to: {path}")
        print("-" * 40)

        affected = self.get_all_affected(path)
        affected.discard(path)  # Remove the source file itself

        if not affected:
            print("  No dependent files found")
            return

        for dep in sorted(affected):
            node = self.get_node(dep)
            node_type = node.get("type", "unknown") if node else "unknown"
            print(f"  [{node_type}] {dep}")

    def print_rebuild_order(self):
        """Print files that need rebuilding in order."""
        print("=" * 60)
        print("REBUILD ORDER")
        print("=" * 60)

        rebuild_list = self.get_rebuild_order()

        if not rebuild_list:
            print("\nAll files are up to date!")
            return

        print(f"\n{len(rebuild_list)} file(s) need updating:\n")

        for i, (path, reasons) in enumerate(rebuild_list, 1):
            node = self.get_node(path)
            print(f"{i}. {path}")
            print(f"   Type: {node.get('type', 'unknown')}")
            print(f"   Reason: {', '.join(reasons)}")

            if node.get("rebuild_instructions"):
                instructions = node["rebuild_instructions"].strip().split("\n")[0]
                print(f"   Instructions: {instructions}...")
            print()

    def generate_claude_prompt(self) -> str:
        """Generate a prompt for Claude to rebuild outdated files."""
        rebuild_list = self.get_rebuild_order()

        if not rebuild_list:
            return "All files are up to date. No rebuilding needed."

        prompt = "# Dependency Rebuild Required\n\n"
        prompt += f"The following {len(rebuild_list)} file(s) need to be updated:\n\n"

        for i, (path, reasons) in enumerate(rebuild_list, 1):
            node = self.get_node(path)
            prompt += f"## {i}. `{path}`\n\n"
            prompt += f"**Reason**: Dependencies changed: {', '.join(reasons)}\n\n"

            if node.get("rebuild_instructions"):
                prompt += f"**Instructions**:\n{node['rebuild_instructions']}\n\n"

            prompt += "---\n\n"

        prompt += "Please update each file according to its instructions, "
        prompt += "working through the list in order (dependencies first).\n"

        return prompt


def main():
    parser = argparse.ArgumentParser(description="Dependency tracker for Claude Skills")
    parser.add_argument(
        "command",
        choices=["status", "check", "graph", "rebuild-order", "affected", "prompt"],
        help="Command to run"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="File path (for check and affected commands)"
    )

    args = parser.parse_args()

    repo_root = get_repo_root()
    config = load_dependencies(repo_root)
    graph = DependencyGraph(repo_root, config)

    if args.command == "status":
        graph.print_status()

    elif args.command == "check":
        if not args.file:
            print("Error: file path required for check command")
            sys.exit(1)
        needs, reasons = graph.check_needs_update(args.file)
        if needs:
            print(f"NEEDS UPDATE: {args.file}")
            print(f"Reasons: {', '.join(reasons)}")
        else:
            print(f"UP TO DATE: {args.file}")

    elif args.command == "graph":
        graph.print_graph()

    elif args.command == "rebuild-order":
        graph.print_rebuild_order()

    elif args.command == "affected":
        if not args.file:
            print("Error: file path required for affected command")
            sys.exit(1)
        graph.print_affected(args.file)

    elif args.command == "prompt":
        print(graph.generate_claude_prompt())


if __name__ == "__main__":
    main()
