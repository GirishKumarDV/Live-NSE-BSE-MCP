"""
Python MCP Client for Indian Stock Exchange

A comprehensive MCP client package for connecting to MCP servers,
with specialized support for the Indian Stock Exchange server.
"""

from .simple_mcp_client import SimpleMCPClient, ISEMCPClient, Tool

__version__ = "1.0.0"
__author__ = "ISE MCP Client"
__description__ = "Python MCP Client for Indian Stock Exchange"

__all__ = [
    "SimpleMCPClient",
    "ISEMCPClient", 
    "Tool"
] 