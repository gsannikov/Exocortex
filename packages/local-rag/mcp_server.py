#!/usr/bin/env python3
"""
MCP Server for Local RAG.

Exposes local-rag functionality via the Model Context Protocol.
All stdout output MUST be valid JSON-RPC messages.
Debug/info messages go to stderr only.
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import Iterator, Tuple, Dict, Any, List, Optional

# MCP protocol constants
JSONRPC_VERSION = "2.0"

# State management
STATE_DIR = Path(__file__).parent / "state"
STATE_PATH = STATE_DIR / "mcp_state.json"


# =============================================================================
# Helper functions (used by tests)
# =============================================================================

def chunk_text(text: str, size: int = 500, overlap: int = 50) -> Iterator[Tuple[int, int, str]]:
    """
    Chunk text into overlapping segments.
    
    Yields:
        Tuples of (start_index, end_index, chunk_content)
    """
    if not text:
        return
    
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        yield (start, end, text[start:end])
        
        if end >= len(text):
            break
        
        start = end - overlap
        if start < 0:
            start = 0


def fhash(filepath: Path) -> str:
    """Compute SHA1 hash of a file's content."""
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()


def load_state() -> Dict[str, Any]:
    """Load MCP server state from disk."""
    if not STATE_PATH.exists():
        return {}
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_state(state: Dict[str, Any]) -> None:
    """Save MCP server state to disk."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)


# =============================================================================
# MCP Protocol Implementation
# =============================================================================

def log(msg: str) -> None:
    """Log to stderr (not stdout, which is reserved for JSON-RPC)."""
    print(f"[local-rag-mcp] {msg}", file=sys.stderr)


def send_response(id: Any, result: Any) -> None:
    """Send a JSON-RPC response."""
    response = {
        "jsonrpc": JSONRPC_VERSION,
        "id": id,
        "result": result
    }
    print(json.dumps(response), flush=True)


def send_error(id: Any, code: int, message: str, data: Any = None) -> None:
    """Send a JSON-RPC error response."""
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    
    response = {
        "jsonrpc": JSONRPC_VERSION,
        "id": id,
        "error": error
    }
    print(json.dumps(response), flush=True)


def handle_initialize(id: Any, params: dict) -> None:
    """Handle initialize request."""
    log("Handling initialize request")
    
    result = {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "local-rag",
            "version": "2.0.0"
        }
    }
    send_response(id, result)


def handle_initialized(id: Any, params: dict) -> None:
    """Handle initialized notification."""
    log("Server initialized")
    # This is a notification, no response needed if id is None
    if id is not None:
        send_response(id, {})


def handle_tools_list(id: Any, params: dict) -> None:
    """Handle tools/list request."""
    log("Listing tools")
    
    tools = [
        {
            "name": "local_rag_index",
            "description": "Index a folder of documents for semantic search. Creates vector embeddings for all supported document types (PDF, DOCX, TXT, MD, etc.).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "Path to the folder containing documents to index"
                    },
                    "user_data_dir": {
                        "type": "string",
                        "description": "Path to store the index data (default: ~/local-rag-data)"
                    }
                },
                "required": ["folder_path"]
            }
        },
        {
            "name": "local_rag_query",
            "description": "Search the indexed documents using semantic search. Returns the most relevant document chunks.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "user_data_dir": {
                        "type": "string",
                        "description": "Path to the index data (default: ~/local-rag-data)"
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "local_rag_stats",
            "description": "Get statistics about the indexed documents.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_data_dir": {
                        "type": "string",
                        "description": "Path to the index data (default: ~/local-rag-data)"
                    }
                }
            }
        }
    ]
    
    send_response(id, {"tools": tools})


def handle_tools_call(id: Any, params: dict) -> None:
    """Handle tools/call request."""
    tool_name = params.get("name", "")
    arguments = params.get("arguments", {})
    
    log(f"Calling tool: {tool_name}")
    
    try:
        if tool_name == "local_rag_index":
            result = call_index(arguments)
        elif tool_name == "local_rag_query":
            result = call_query(arguments)
        elif tool_name == "local_rag_stats":
            result = call_stats(arguments)
        else:
            send_error(id, -32601, f"Unknown tool: {tool_name}")
            return
        
        send_response(id, {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
                }
            ]
        })
        
    except Exception as e:
        log(f"Tool error: {e}")
        send_response(id, {
            "content": [
                {
                    "type": "text",
                    "text": f"Error: {str(e)}"
                }
            ],
            "isError": True
        })


def call_index(arguments: dict) -> dict:
    """Execute the index command."""
    from local_rag.indexer import DocumentIndexer
    
    folder_path = arguments.get("folder_path")
    if not folder_path:
        raise ValueError("folder_path is required")
    
    user_data_dir = arguments.get("user_data_dir", str(Path.home() / "local-rag-data"))
    
    indexer = DocumentIndexer(user_data_dir=user_data_dir)
    stats = indexer.index_directory(Path(folder_path))
    
    return {
        "status": "success",
        "indexed_folder": folder_path,
        "user_data_dir": user_data_dir,
        "stats": stats
    }


def call_query(arguments: dict) -> dict:
    """Execute the query command."""
    from local_rag.query import DocumentSearcher
    
    query = arguments.get("query")
    if not query:
        raise ValueError("query is required")
    
    user_data_dir = arguments.get("user_data_dir", str(Path.home() / "local-rag-data"))
    k = arguments.get("k", 5)
    
    searcher = DocumentSearcher(user_data_dir=user_data_dir)
    results = searcher.search(query=query, k=k)
    
    return {
        "query": query,
        "results": results
    }


def call_stats(arguments: dict) -> dict:
    """Get index statistics."""
    from local_rag.query import DocumentSearcher
    
    user_data_dir = arguments.get("user_data_dir", str(Path.home() / "local-rag-data"))
    
    try:
        searcher = DocumentSearcher(user_data_dir=user_data_dir)
        stats = searcher.get_stats()
        return stats
    except FileNotFoundError:
        return {
            "status": "no_index",
            "message": f"No index found at {user_data_dir}. Run local_rag_index first."
        }


def handle_request(request: dict) -> None:
    """Route a JSON-RPC request to the appropriate handler."""
    method = request.get("method", "")
    id = request.get("id")
    params = request.get("params", {})
    
    log(f"Received method: {method}")
    
    handlers = {
        "initialize": handle_initialize,
        "initialized": handle_initialized,
        "notifications/initialized": handle_initialized,
        "tools/list": handle_tools_list,
        "tools/call": handle_tools_call,
    }
    
    handler = handlers.get(method)
    if handler:
        handler(id, params)
    elif method.startswith("notifications/"):
        # Notifications don't require responses
        pass
    else:
        if id is not None:
            send_error(id, -32601, f"Method not found: {method}")


def main():
    """Main MCP server loop."""
    log("Starting Local RAG MCP server...")
    
    # Read JSON-RPC messages from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            request = json.loads(line)
            handle_request(request)
        except json.JSONDecodeError as e:
            log(f"JSON parse error: {e}")
            # Send error for invalid JSON
            send_error(None, -32700, f"Parse error: {e}")
        except Exception as e:
            log(f"Unexpected error: {e}")
            send_error(None, -32603, f"Internal error: {e}")


if __name__ == "__main__":
    main()
