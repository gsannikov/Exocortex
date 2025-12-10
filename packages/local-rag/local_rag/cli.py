"""Unified command-line entrypoint for Local RAG."""

import sys
from typing import List

from . import __version__, indexer, query, visualize
from .health import get_health
from .settings import get_settings


def _print_help():
    help_text = f"""
Local RAG CLI (v{__version__})

Commands:
  index      Index a folder of documents
  query      Search an existing index
  visualize  Inspect how text is chunked
  health     Show vector count and last index time

Examples:
  local-rag index ~/Docs --user-data-dir ~/rag-data
  local-rag query "neural nets" --user-data-dir ~/rag-data -k 5
  local-rag visualize README.md --strategy template
  local-rag health --user-data-dir ~/rag-data
"""
    print(help_text.strip())


def main(argv: List[str] | None = None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        _print_help()
        return 0

    command = args[0]
    passthrough = args[1:]

    if command in {"-v", "--version", "version"}:
        print(__version__)
        return 0

    if command == "index":
        sys.argv = [f"{sys.argv[0]} index"] + passthrough
        return indexer.main()

    if command == "query":
        sys.argv = [f"{sys.argv[0]} query"] + passthrough
        return query.main()

    if command == "visualize":
        sys.argv = [f"{sys.argv[0]} visualize"] + passthrough
        return visualize.main()

    if command == "health":
        # lightweight, no argparse; just print snapshot
        settings = get_settings()
        health = get_health(settings)
        print(health)
        return 0

    print(f"Unknown command: {command}", file=sys.stderr)
    _print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
