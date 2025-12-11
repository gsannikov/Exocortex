"""
Exocortex MCP Server

Expose Exocortex Claude skills through MCP protocol.
"""

from .server import mcp

__version__ = "0.1.0"
__all__ = ["mcp"]
