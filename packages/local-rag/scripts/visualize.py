#!/usr/bin/env python3
"""
Chunk visualization CLI for Local RAG.

Provides tools to visualize how documents are chunked:
- Show chunk boundaries with markers
- Display chunk statistics
- Preview chunks in different formats
- Compare chunking strategies
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from chunking import (
    Chunk,
    ChunkingStrategy,
    get_chunker,
    FixedChunker,
    SentenceChunker,
    SemanticChunker,
    TemplateChunker
)


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DIM = '\033[2m'


# Color cycle for chunk boundaries
CHUNK_COLORS = [Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.CYAN, Colors.RED]


def colorize(text: str, color: str) -> str:
    """Wrap text in ANSI color codes."""
    return f"{color}{text}{Colors.END}"


def visualize_chunks(
    text: str,
    chunks: List[Chunk],
    show_markers: bool = True,
    show_preview: bool = True,
    max_preview_length: int = 200
) -> str:
    """
    Create a visualization of chunk boundaries.

    Args:
        text: Original text
        chunks: List of Chunk objects
        show_markers: Whether to show chunk boundary markers
        show_preview: Whether to show chunk content preview
        max_preview_length: Maximum length of preview text

    Returns:
        Formatted string visualization
    """
    output = []

    # Header
    output.append(colorize("=" * 60, Colors.HEADER))
    output.append(colorize(f" CHUNK VISUALIZATION ({len(chunks)} chunks)", Colors.BOLD))
    output.append(colorize("=" * 60, Colors.HEADER))
    output.append("")

    for i, chunk in enumerate(chunks):
        color = CHUNK_COLORS[i % len(CHUNK_COLORS)]

        # Chunk header
        output.append(colorize(f"┌─ Chunk {i + 1}/{len(chunks)} ", color) +
                     colorize(f"[{chunk.start}:{chunk.end}]", Colors.DIM))

        # Metadata
        if chunk.metadata:
            meta_str = ", ".join(f"{k}={v}" for k, v in chunk.metadata.items())
            output.append(colorize(f"│  {meta_str}", Colors.DIM))

        # Length info
        output.append(colorize(f"│  Length: {len(chunk.text)} chars", Colors.DIM))

        # Content preview
        if show_preview:
            preview = chunk.text[:max_preview_length]
            if len(chunk.text) > max_preview_length:
                preview += "..."

            # Format preview with line breaks
            preview_lines = preview.split('\n')
            for j, line in enumerate(preview_lines[:5]):  # Max 5 lines
                prefix = "│  " if j == 0 else "│  "
                output.append(colorize(prefix, color) + line[:80])

            if len(preview_lines) > 5:
                output.append(colorize(f"│  ... ({len(preview_lines) - 5} more lines)", Colors.DIM))

        # Chunk footer
        output.append(colorize("└" + "─" * 40, color))
        output.append("")

    return "\n".join(output)


def visualize_boundaries(text: str, chunks: List[Chunk]) -> str:
    """
    Create inline visualization of chunk boundaries.

    Shows the original text with markers where chunks begin and end.
    """
    # Sort chunks by start position
    sorted_chunks = sorted(chunks, key=lambda c: c.start)

    # Build marked text
    result = []
    last_end = 0

    for i, chunk in enumerate(sorted_chunks):
        color = CHUNK_COLORS[i % len(CHUNK_COLORS)]

        # Add text before this chunk (if gap)
        if chunk.start > last_end:
            gap = text[last_end:chunk.start]
            if gap.strip():
                result.append(colorize(f"[GAP:{len(gap)}]", Colors.RED))

        # Add chunk marker and content
        result.append(colorize(f"«{i + 1}»", color))
        result.append(text[chunk.start:chunk.end])

        last_end = chunk.end

    # Add remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining.strip():
            result.append(colorize(f"[REMAINING:{len(remaining)}]", Colors.RED))

    return "".join(result)


def print_stats(chunks: List[Chunk], text: str):
    """Print statistics about chunks."""
    if not chunks:
        print("No chunks to analyze.")
        return

    lengths = [len(c.text) for c in chunks]
    total_chars = sum(lengths)

    print(colorize("\n" + "=" * 40, Colors.HEADER))
    print(colorize(" CHUNK STATISTICS", Colors.BOLD))
    print(colorize("=" * 40, Colors.HEADER))

    print(f"\nOriginal text length: {len(text):,} chars")
    print(f"Number of chunks:     {len(chunks)}")
    print(f"Total chunk chars:    {total_chars:,}")

    # Calculate overlap
    overlap_chars = total_chars - len(text)
    overlap_pct = (overlap_chars / len(text) * 100) if text else 0
    print(f"Overlap chars:        {overlap_chars:,} ({overlap_pct:.1f}%)")

    print(f"\nChunk size distribution:")
    print(f"  Min:     {min(lengths):,} chars")
    print(f"  Max:     {max(lengths):,} chars")
    print(f"  Mean:    {sum(lengths) / len(lengths):,.0f} chars")
    print(f"  Median:  {sorted(lengths)[len(lengths) // 2]:,} chars")

    # Strategy breakdown
    strategies = {}
    for chunk in chunks:
        strategy = chunk.metadata.get('strategy', 'unknown')
        strategies[strategy] = strategies.get(strategy, 0) + 1

    if len(strategies) > 1:
        print(f"\nStrategies used:")
        for strategy, count in sorted(strategies.items()):
            print(f"  {strategy}: {count}")


def compare_strategies(
    text: str,
    chunk_size: int = 3000,
    chunk_overlap: int = 400,
    file_path: Optional[str] = None
):
    """Compare different chunking strategies on the same text."""
    print(colorize("\n" + "=" * 60, Colors.HEADER))
    print(colorize(" CHUNKING STRATEGY COMPARISON", Colors.BOLD))
    print(colorize("=" * 60, Colors.HEADER))
    print(f"\nText length: {len(text):,} chars")
    print(f"Chunk size: {chunk_size}, Overlap: {chunk_overlap}")
    print()

    strategies = [
        (ChunkingStrategy.FIXED, {}),
        (ChunkingStrategy.SENTENCE, {}),
        (ChunkingStrategy.TEMPLATE, {'file_path': file_path}),
    ]

    results = []

    for strategy, kwargs in strategies:
        chunker = get_chunker(strategy, chunk_size, chunk_overlap)
        chunks = list(chunker.chunk(text, **kwargs))

        lengths = [len(c.text) for c in chunks] if chunks else [0]
        total = sum(lengths)

        results.append({
            'strategy': strategy.value,
            'num_chunks': len(chunks),
            'total_chars': total,
            'min_size': min(lengths),
            'max_size': max(lengths),
            'avg_size': sum(lengths) / len(lengths) if lengths else 0,
            'overlap_pct': ((total - len(text)) / len(text) * 100) if text else 0
        })

    # Print comparison table
    print(f"{'Strategy':<12} {'Chunks':>8} {'Total':>10} {'Min':>8} {'Max':>8} {'Avg':>8} {'Overlap':>10}")
    print("-" * 70)

    for r in results:
        print(f"{r['strategy']:<12} {r['num_chunks']:>8} {r['total_chars']:>10,} "
              f"{r['min_size']:>8,} {r['max_size']:>8,} {r['avg_size']:>8,.0f} {r['overlap_pct']:>9.1f}%")


def visualize_file(
    file_path: str,
    strategy: str = "template",
    chunk_size: int = 3000,
    chunk_overlap: int = 400,
    output_format: str = "visual",
    compare: bool = False
):
    """
    Visualize chunks for a file.

    Args:
        file_path: Path to file to analyze
        strategy: Chunking strategy to use
        chunk_size: Maximum chunk size
        chunk_overlap: Overlap between chunks
        output_format: Output format (visual, json, stats, boundaries)
        compare: Compare all strategies
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Read file
    try:
        text = path.read_text(errors='ignore')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print("File is empty.")
        return

    if compare:
        compare_strategies(text, chunk_size, chunk_overlap, file_path)
        return

    # Get chunker and chunk
    try:
        strat = ChunkingStrategy(strategy)
    except ValueError:
        print(f"Unknown strategy: {strategy}. Available: {[s.value for s in ChunkingStrategy]}")
        sys.exit(1)

    chunker = get_chunker(strat, chunk_size, chunk_overlap)
    chunks = list(chunker.chunk(text, file_path=file_path))

    # Output based on format
    if output_format == "json":
        output = {
            "file": file_path,
            "strategy": strategy,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "num_chunks": len(chunks),
            "chunks": [
                {
                    "index": i,
                    "start": c.start,
                    "end": c.end,
                    "length": len(c.text),
                    "text": c.text[:500] + "..." if len(c.text) > 500 else c.text,
                    "metadata": c.metadata
                }
                for i, c in enumerate(chunks)
            ]
        }
        print(json.dumps(output, indent=2))

    elif output_format == "stats":
        print_stats(chunks, text)

    elif output_format == "boundaries":
        print(visualize_boundaries(text, chunks))

    else:  # visual (default)
        print(f"\nFile: {file_path}")
        print(f"Strategy: {strategy}")
        print(visualize_chunks(text, chunks))
        print_stats(chunks, text)


def main():
    parser = argparse.ArgumentParser(
        description="Visualize how documents are chunked",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.md                     # Visualize with default settings
  %(prog)s document.md -s sentence         # Use sentence-based chunking
  %(prog)s document.md --compare           # Compare all strategies
  %(prog)s document.md -f json             # Output as JSON
  %(prog)s document.md -f stats            # Show statistics only
  %(prog)s document.md --size 1000         # Use smaller chunks
        """
    )

    parser.add_argument("file", help="File to analyze")
    parser.add_argument(
        "-s", "--strategy",
        choices=[s.value for s in ChunkingStrategy],
        default="template",
        help="Chunking strategy (default: template)"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=3000,
        help="Chunk size in characters (default: 3000)"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=400,
        help="Chunk overlap in characters (default: 400)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["visual", "json", "stats", "boundaries"],
        default="visual",
        help="Output format (default: visual)"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare all chunking strategies"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    args = parser.parse_args()

    # Disable colors if requested or not a TTY
    if args.no_color or not sys.stdout.isatty():
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')

    visualize_file(
        file_path=args.file,
        strategy=args.strategy,
        chunk_size=args.size,
        chunk_overlap=args.overlap,
        output_format=args.format,
        compare=args.compare
    )


if __name__ == "__main__":
    main()
