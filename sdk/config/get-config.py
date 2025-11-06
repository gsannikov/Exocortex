#!/usr/bin/env python3
"""
Configuration Value Extractor for GitHub Actions and Scripts

This script extracts values from template-config.yaml for use in workflows and scripts.

Usage:
    # Get single value
    python sdk/config/get-config.py version.template

    # Get multiple values as JSON
    python sdk/config/get-config.py --json version repository.name testing.comprehensive_test_count

    # Get all storage backends as comma-separated list
    python sdk/config/get-config.py --list storage_backends.available

    # Output as GitHub Actions environment variables
    python sdk/config/get-config.py --github-env version.template repository.owner python.tested_version
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Any, List


def load_config() -> dict:
    """Load configuration from template-config.yaml"""
    config_path = Path(__file__).parent / "template-config.yaml"

    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        sys.exit(1)


def get_value(config: dict, key: str) -> Any:
    """Get value from config using dot notation"""
    keys = key.split('.')
    value = config

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None

    return value


def format_value(value: Any, as_list: bool = False) -> str:
    """Format value for output"""
    if value is None:
        return ""

    if isinstance(value, list):
        if as_list:
            return ",".join(str(v) for v in value)
        return json.dumps(value)

    if isinstance(value, dict):
        return json.dumps(value)

    return str(value)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    config = load_config()

    # Parse arguments
    mode = "single"  # single, json, list, github-env
    keys = []

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == "--json":
            mode = "json"
        elif arg == "--list":
            mode = "list"
        elif arg == "--github-env":
            mode = "github-env"
        elif arg.startswith("--"):
            print(f"Unknown option: {arg}", file=sys.stderr)
            sys.exit(1)
        else:
            keys.append(arg)

        i += 1

    if not keys:
        print("Error: No keys specified", file=sys.stderr)
        sys.exit(1)

    # Process based on mode
    if mode == "single":
        # Single value output
        if len(keys) > 1:
            print("Error: Multiple keys specified without --json or --github-env", file=sys.stderr)
            sys.exit(1)

        value = get_value(config, keys[0])
        print(format_value(value))

    elif mode == "json":
        # JSON output of multiple values
        result = {}
        for key in keys:
            value = get_value(config, key)
            # Use last part of key as dict key
            short_key = key.split('.')[-1]
            result[short_key] = value

        print(json.dumps(result, indent=2))

    elif mode == "list":
        # Comma-separated list output
        if len(keys) > 1:
            print("Error: --list mode only supports single key", file=sys.stderr)
            sys.exit(1)

        value = get_value(config, keys[0])
        print(format_value(value, as_list=True))

    elif mode == "github-env":
        # GitHub Actions environment variable format
        for key in keys:
            value = get_value(config, key)
            # Convert key to env var name (e.g., version.template -> VERSION_TEMPLATE)
            env_var = key.upper().replace('.', '_')
            print(f"{env_var}={format_value(value)}")


if __name__ == "__main__":
    main()
