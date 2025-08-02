"""
Indian Stock Exchange MCP Server

A Model Context Protocol server for accessing live Indian stock market data
from BSE & NSE exchanges through a unified API interface.
"""

__version__ = "1.0.0"
__author__ = "ISE MCP Team"
__email__ = "contact@ise-mcp.com"
__description__ = "Indian Stock Exchange MCP Server - Access live market data from BSE & NSE"

from .config import Config

__all__ = ["Config", "__version__"] 