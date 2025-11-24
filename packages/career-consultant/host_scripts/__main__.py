#!/usr/bin/env python3
"""
Host Scripts CLI - Entry point for python -m host_scripts

Provides command-line utilities for repo maintenance and version management.
"""

import sys
import argparse
from pathlib import Path

# Add host_scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from update_version import update_version_references
from bump_version import main as bump_version_main
from validate import main as validate_main
from release import main as release_main


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Host scripts for Israeli Tech Career Consultant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m host_scripts update-version --quiet
  python -m host_scripts bump-version patch
  python -m host_scripts validate all
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # update-version command
    version_parser = subparsers.add_parser(
        'update-version',
        help='Synchronize version numbers across all files from version.yaml'
    )
    version_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output except errors'
    )
    
    # bump-version command
    bump_parser = subparsers.add_parser(
        'bump-version',
        help='Bump version in version.yaml'
    )
    bump_parser.add_argument(
        'action',
        choices=['patch', 'minor', 'major', 'show'],
        help='Version bump type or show current version'
    )
    
    # validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate documentation and package structure'
    )
    validate_parser.add_argument(
        'target',
        choices=['docs', 'package', 'all'],
        help='What to validate'
    )
    
    # release command
    release_parser = subparsers.add_parser(
        'release',
        help='Interactive release workflow guide'
    )
    release_parser.add_argument(
        '--patch',
        action='store_true',
        help='Create patch release (non-interactive)'
    )
    release_parser.add_argument(
        '--minor',
        action='store_true',
        help='Create minor release (non-interactive)'
    )
    release_parser.add_argument(
        '--major',
        action='store_true',
        help='Create major release (non-interactive)'
    )
    release_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would happen without making changes'
    )
    
    args = parser.parse_args()
    
    if args.command == 'update-version':
        try:
            update_version_references(quiet=args.quiet)
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'bump-version':
        # Call bump_version main with synthetic argv
        original_argv = sys.argv
        sys.argv = ['bump-version', args.action]
        try:
            bump_version_main()
            sys.exit(0)
        except SystemExit as e:
            sys.exit(e.code)
        finally:
            sys.argv = original_argv
    
    elif args.command == 'validate':
        # Call validate main with synthetic argv
        original_argv = sys.argv
        sys.argv = ['validate', args.target]
        try:
            validate_main()
            sys.exit(0)
        except SystemExit as e:
            sys.exit(e.code)
        finally:
            sys.argv = original_argv
    
    elif args.command == 'release':
        # Call release main with synthetic argv
        original_argv = sys.argv
        argv = ['release']
        if args.patch:
            argv.append('--patch')
        if args.minor:
            argv.append('--minor')
        if args.major:
            argv.append('--major')
        if args.dry_run:
            argv.append('--dry-run')
        sys.argv = argv
        try:
            release_main()
            sys.exit(0)
        except SystemExit as e:
            sys.exit(e.code)
        finally:
            sys.argv = original_argv
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
