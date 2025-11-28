#!/usr/bin/env python3
"""
MCP Server for Local RAG.
Exposes tools for indexing and querying local documents.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Sequence

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    CallToolRequest,
    CallToolResult,
)

# Import from local package
from .utils import setup_logging
from .settings import get_settings
from .indexer import DocumentIndexer, load_state
from .query import DocumentSearcher
from .storage import create_repository
from .vectorstore import get_vector_store

# Setup logging
setup_logging(verbose=True)
logger = logging.getLogger("mcp-server")

# Initialize Server
server = Server("local-rag")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="local_rag_index",
            description="Index a directory of documents for RAG search. Supports PDF, DOCX, MD, TXT, code files, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to the directory or file to index"
                    },
                    "user_data_dir": {
                        "type": "string",
                        "description": "Directory to store the index and state (default: ~/.local-rag-data)"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force re-indexing of all files even if unchanged",
                        "default": False
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="local_rag_query",
            description="Search the indexed documents using hybrid search (vector + keyword).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "user_data_dir": {
                        "type": "string",
                        "description": "Directory where the index is stored (default: ~/.local-rag-data)"
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    },
                    "method": {
                        "type": "string",
                        "enum": ["hybrid", "vector", "bm25"],
                        "description": "Search method (default: hybrid)",
                        "default": "hybrid"
                    },
                    "rerank": {
                        "type": "boolean",
                        "description": "Enable cross-encoder reranking for better precision (slower)",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="local_rag_stats",
            description="Get statistics about the current index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_data_dir": {
                        "type": "string",
                        "description": "Directory where the index is stored (default: ~/.local-rag-data)"
                    }
                }
            }
        ),
        Tool(
            name="local_rag_health",
            description="Lightweight health info: vector count and last index mtime.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_data_dir": {
                        "type": "string",
                        "description": "Directory where the index is stored (default: ~/.local-rag-data)"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(
    name: str, arguments: Any
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    
    user_data_dir = arguments.get("user_data_dir")
    settings = get_settings(user_data_dir=user_data_dir)
    settings.apply_runtime_env()
    Path(settings.user_data_dir).mkdir(parents=True, exist_ok=True)

    try:
        if name == "local_rag_index":
            path = arguments.get("path")
            force = arguments.get("force", False)
            
            if not path:
                raise ValueError("Path is required")

            indexer = DocumentIndexer(
                settings=settings
            )
            
            source_path = Path(path)
            if not source_path.exists():
                return [TextContent(type="text", text=f"Error: Path {path} does not exist")]

            if source_path.is_file():
                count, dropped = indexer.index_file(source_path)
                return [TextContent(type="text", text=f"Indexed file: {path} ({count} chunks, dropped {dropped})")]
            else:
                stats = indexer.index_directory(source_path, force=force)
                return [TextContent(type="text", text=json.dumps(stats, indent=2))]

        elif name == "local_rag_query":
            query = arguments.get("query")
            k = arguments.get("k", 5)
            method = arguments.get("method", settings.search_method)
            rerank = arguments.get("rerank", settings.use_reranker)

            searcher = DocumentSearcher(
                settings=settings,
                search_method=method,
                use_reranker=rerank
            )

            results = searcher.search(query, k=k)
            
            # Format results for display
            formatted_results = []
            for r in results:
                formatted_results.append(
                    f"**{r['filename']}** (Score: {r['score']})\n"
                    f"Path: `{r['path']}`\n"
                    f"Preview:\n> {r['preview'].replace(chr(10), chr(10) + '> ')}\n"
                )
            
            response_text = f"Found {len(results)} results for '{query}':\n\n" + "\n---\n".join(formatted_results)
            return [TextContent(type="text", text=response_text)]

        elif name == "local_rag_stats":
            searcher = DocumentSearcher(user_data_dir=user_data_dir)
            stats = searcher.get_stats()
            return [TextContent(type="text", text=json.dumps(stats, indent=2))]
        elif name == "local_rag_health":
            repo = create_repository(settings, factory=get_vector_store)
            count = repo.count()
            state = load_state(settings.paths["state_path"])
            last_index = None
            if state:
                try:
                    last_index = max(entry.get("mtime", 0) for entry in state.values())
                except Exception:
                    last_index = None
            health = {
                "vector_count": count,
                "last_index_mtime": last_index,
                "user_data_dir": str(settings.user_data_dir),
                "collection": settings.collection_name,
            }
            return [TextContent(type="text", text=json.dumps(health, indent=2))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.exception("Error executing tool")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    # Run the server using stdin/stdout streams
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
