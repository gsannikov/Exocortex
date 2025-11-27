"""Unified command-line entrypoint for Local RAG."""

import sys
from typing import List

from . import __version__
from . import indexer, query, visualize


def _print_help():
    help_text = f"""
Local RAG CLI (v{__version__})

Commands:
  index      Index a folder of documents
  query      Search an existing index
  visualize  Inspect how text is chunked

Examples:
  local-rag index ~/Docs --user-data-dir ~/rag-data
  local-rag query "neural nets" --user-data-dir ~/rag-data -k 5
  local-rag visualize README.md --strategy template
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

    print(f"Unknown command: {command}", file=sys.stderr)
    _print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
