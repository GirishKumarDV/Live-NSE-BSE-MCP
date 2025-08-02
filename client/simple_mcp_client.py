#!/usr/bin/env python3
"""
Simple Python MCP Client for HTTP Servers

A focused MCP client for connecting to HTTP-based MCP servers
like the Indian Stock Exchange server.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple-mcp-client")

@dataclass
class Tool:
    """MCP Tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]

class SimpleMCPClient:
    """Simple MCP client for HTTP JSON-RPC servers"""
    
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.headers = headers or {}
        self.client = httpx.AsyncClient(timeout=30.0)
        self._request_id = 0
        self.tools: List[Tool] = []
        self.server_info: Dict[str, Any] = {}
        self.connected = False
    
    def _next_id(self) -> int:
        """Get next request ID"""
        self._request_id += 1
        return self._request_id
    
    async def _send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send JSON-RPC request"""
        request_data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self._next_id()
        }
        
        logger.debug(f"→ {method}")
        
        try:
            response = await self.client.post(
                self.url,
                json=request_data,
                headers={
                    "Content-Type": "application/json",
                    **self.headers
                }
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")
            
            return result.get("result", {})
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise Exception(f"Request failed: {str(e)}")
    
    async def connect(self) -> bool:
        """Connect and initialize MCP session"""
        try:
            # Initialize
            init_params = {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "simple-mcp-client",
                    "version": "1.0.0"
                }
            }
            
            result = await self._send_request("initialize", init_params)
            self.server_info = result.get("serverInfo", {})
            
            # Load tools
            tools_result = await self._send_request("tools/list")
            tools_data = tools_result.get("tools", [])
            
            self.tools = []
            for tool_data in tools_data:
                tool = Tool(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    inputSchema=tool_data["inputSchema"]
                )
                self.tools.append(tool)
            
            self.connected = True
            logger.info(f"Connected to {self.server_info.get('name', 'Unknown')} - {len(self.tools)} tools")
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def list_tools(self) -> List[Tool]:
        """Get available tools"""
        if not self.connected:
            raise Exception("Not connected. Call connect() first.")
        return self.tools
    
    async def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Call a tool"""
        if not self.connected:
            raise Exception("Not connected. Call connect() first.")
        
        params = {
            "name": name,
            "arguments": arguments or {}
        }
        
        logger.info(f"🔧 Calling tool: {name}")
        result = await self._send_request("tools/call", params)
        return result.get("content", [])
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name"""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return self.server_info
    
    async def close(self):
        """Close connection"""
        await self.client.aclose()
        self.connected = False

# Indian Stock Exchange specific client
class ISEMCPClient(SimpleMCPClient):
    """Specialized client for Indian Stock Exchange MCP server"""
    
    def __init__(self, url: str = "http://localhost:8000/jsonrpc"):
        super().__init__(url)
    
    async def get_stock_data(self, company_name: str) -> Dict[str, Any]:
        """Get detailed stock data for a company"""
        result = await self.call_tool("get_stock_data", {"name": company_name})
        return result[0]["text"] if result else {}
    
    async def search_industry(self, industry: str) -> Dict[str, Any]:
        """Search companies in an industry"""
        result = await self.call_tool("search_industry", {"query": industry})
        return result[0]["text"] if result else {}
    
    async def get_trending_stocks(self) -> Dict[str, Any]:
        """Get trending stocks (gainers and losers)"""
        result = await self.call_tool("get_trending_stocks")
        return result[0]["text"] if result else {}
    
    async def get_nse_most_active(self) -> Dict[str, Any]:
        """Get most active NSE stocks"""
        result = await self.call_tool("get_nse_most_active")
        return result[0]["text"] if result else {}
    
    async def get_bse_most_active(self) -> Dict[str, Any]:
        """Get most active BSE stocks"""
        result = await self.call_tool("get_bse_most_active")
        return result[0]["text"] if result else {}
    
    async def get_52_week_high_low(self) -> Dict[str, Any]:
        """Get 52-week high/low stocks"""
        result = await self.call_tool("get_52_week_high_low")
        return result[0]["text"] if result else {}
    
    async def search_mutual_funds(self, query: str) -> Dict[str, Any]:
        """Search mutual funds"""
        result = await self.call_tool("search_mutual_funds", {"query": query})
        return result[0]["text"] if result else {}
    
    async def get_mutual_funds(self) -> Dict[str, Any]:
        """Get latest mutual fund data"""
        result = await self.call_tool("get_mutual_funds")
        return result[0]["text"] if result else {}
    
    async def get_price_shockers(self) -> Dict[str, Any]:
        """Get stocks with significant price changes"""
        result = await self.call_tool("get_price_shockers")
        return result[0]["text"] if result else {}
    
    async def get_commodities(self) -> Dict[str, Any]:
        """Get commodity futures data"""
        result = await self.call_tool("get_commodities")
        return result[0]["text"] if result else {}
    
    async def get_analyst_recommendations(self, stock_id: str) -> Dict[str, Any]:
        """Get analyst recommendations for a stock"""
        result = await self.call_tool("get_analyst_recommendations", {"stock_id": stock_id})
        return result[0]["text"] if result else {}
    
    async def get_historical_data(self, stock_name: str, period: str = "1yr", filter_type: str = "price") -> Dict[str, Any]:
        """Get historical stock data"""
        result = await self.call_tool("get_historical_data", {
            "stock_name": stock_name,
            "period": period,
            "filter": filter_type
        })
        return result[0]["text"] if result else {}
    
    async def get_historical_stats(self, stock_name: str, stats_type: str = "quarter_results") -> Dict[str, Any]:
        """Get historical statistics for a stock"""
        result = await self.call_tool("get_historical_stats", {
            "stock_name": stock_name,
            "stats": stats_type
        })
        return result[0]["text"] if result else {}

async def demo():
    """Demo the ISE MCP client"""
    print("🇮🇳 Indian Stock Exchange MCP Client Demo")
    print("=" * 45)
    
    # Create client
    client = ISEMCPClient()
    
    try:
        # Connect
        if not await client.connect():
            print("Failed to connect")
            return
        
        # Show server info
        info = client.get_server_info()
        print(f"Server: {info.get('name')} v{info.get('version')}")
        
        # List tools
        tools = await client.list_tools()
        print(f"🔧 Tools: {len(tools)} available")
        
        # Demo calls
        print("\n📈 Market Data:")
        
        # Trending stocks
        print("   • Getting trending stocks...")
        trending = await client.get_trending_stocks()
        if trending:
            print("     Success")
        
        # Stock data
        print("   • Getting Reliance stock data...")
        stock_data = await client.get_stock_data("Reliance")
        if stock_data:
            print("     Success")
        
        # NSE active stocks
        print("   • Getting NSE most active...")
        nse_active = await client.get_nse_most_active()
        if nse_active:
            print("     Success")
        
        print("\n✨ Demo completed!")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(demo()) 