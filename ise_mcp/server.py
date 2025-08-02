#!/usr/bin/env python3
"""
Indian Stock Exchange MCP Server

This server provides access to live market data from Indian Stock Exchanges (BSE & NSE)
through the Model Context Protocol (MCP).
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx
from aiohttp import web
from aiohttp.web import Application, Request, Response, middleware
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

from .config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ise-mcp-server")

app = Server("indian-stock-exchange")

class ISEClient:
    """Client for Indian Stock Exchange API"""
    
    def __init__(self, base_url: str = Config.BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            timeout=Config.REQUEST_TIMEOUT,
            headers=Config.get_headers()
        )
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to the API with x-api-key header"""
        try:
            url = f"{self.base_url}{endpoint}"
            if params:
                url += f"?{urlencode(params)}"

            # Prepare headers with x-api-key
            headers = Config.get_headers().copy()
            if Config.API_KEY:
                headers["x-api-key"] = Config.API_KEY

            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Global client instance
ise_client = ISEClient()

@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools for Indian Stock Exchange data"""
    return [
        Tool(
            name="get_stock_data",
            description="Get detailed financial data for a specific company by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Company name, shortened name, or search term"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="search_industry",
            description="Search for companies within a specific industry",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Industry search term"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_mutual_funds",
            description="Search for mutual funds",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Mutual fund search term"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_trending_stocks",
            description="Get trending stocks with top gainers and losers",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_52_week_high_low",
            description="Get stocks with highest and lowest prices in the last 52 weeks",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_nse_most_active",
            description="Get most active stocks on NSE by trading volume",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_bse_most_active",
            description="Get most active stocks on BSE by trading volume",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_mutual_funds",
            description="Get latest mutual fund data with NAV and returns",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_price_shockers",
            description="Get stocks with significant price changes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_commodities",
            description="Get real-time commodity futures data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_analyst_recommendations",
            description="Get analyst target prices and recommendations for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "stock_id": {
                        "type": "string",
                        "description": "Stock identifier"
                    }
                },
                "required": ["stock_id"]
            }
        ),
        Tool(
            name="get_stock_forecasts",
            description="Get detailed forecast information for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "stock_id": {
                        "type": "string",
                        "description": "Stock identifier"
                    },
                    "measure_code": {
                        "type": "string",
                        "enum": ["EPS", "CPS", "CPX", "DPS", "EBI", "EBT", "GPS", "GRM", "NAV", "NDT", "NET", "PRE", "ROA", "ROE", "SAL"],
                        "description": "Measure code for forecast"
                    },
                    "period_type": {
                        "type": "string",
                        "enum": ["Annual", "Interim"],
                        "description": "Period type"
                    },
                    "data_type": {
                        "type": "string",
                        "enum": ["Actuals", "Estimates"],
                        "description": "Data type"
                    },
                    "age": {
                        "type": "string",
                        "enum": ["OneWeekAgo", "ThirtyDaysAgo", "SixtyDaysAgo", "NinetyDaysAgo", "Current"],
                        "description": "Data age"
                    }
                },
                "required": ["stock_id", "measure_code", "period_type", "data_type", "age"]
            }
        ),
        Tool(
            name="get_historical_data",
            description="Get historical stock data with various filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "stock_name": {
                        "type": "string",
                        "description": "Stock symbol or name"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["1m", "6m", "1yr", "3yr", "5yr", "10yr", "max"],
                        "description": "Time period",
                        "default": "5yr"
                    },
                    "filter": {
                        "type": "string",
                        "enum": ["default", "price", "pe", "sm", "evebitda", "ptb", "mcs"],
                        "description": "Data filter",
                        "default": "default"
                    }
                },
                "required": ["stock_name"]
            }
        ),
        Tool(
            name="get_historical_stats",
            description="Get historical statistics for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "stock_name": {
                        "type": "string",
                        "description": "Stock symbol or name"
                    },
                    "stats": {
                        "type": "string",
                        "enum": ["quarter_results", "yoy_results", "balancesheet", "cashflow", "ratios", "shareholding_pattern_quarterly", "shareholding_pattern_yearly"],
                        "description": "Type of historical statistics"
                    }
                },
                "required": ["stock_name", "stats"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool calls for Indian Stock Exchange data"""
    try:
        if name == "get_stock_data":
            data = await ise_client._make_request("/stock", {"name": arguments["name"]})
            return [types.TextContent(
                type="text",
                text=f"Stock Data for {arguments['name']}:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "search_industry":
            data = await ise_client._make_request("/industry_search", {"query": arguments["query"]})
            return [types.TextContent(
                type="text",
                text=f"Industry Search Results for '{arguments['query']}':\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "search_mutual_funds":
            data = await ise_client._make_request("/mutual_fund_search", {"query": arguments["query"]})
            return [types.TextContent(
                type="text",
                text=f"Mutual Fund Search Results for '{arguments['query']}':\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_trending_stocks":
            data = await ise_client._make_request("/trending")
            return [types.TextContent(
                type="text",
                text=f"Trending Stocks:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_52_week_high_low":
            data = await ise_client._make_request("/fetch_52_week_high_low_data")
            return [types.TextContent(
                type="text",
                text=f"52 Week High/Low Data:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_nse_most_active":
            data = await ise_client._make_request("/NSE_most_active")
            return [types.TextContent(
                type="text",
                text=f"NSE Most Active Stocks:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_bse_most_active":
            data = await ise_client._make_request("/BSE_most_active")
            return [types.TextContent(
                type="text",
                text=f"BSE Most Active Stocks:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_mutual_funds":
            data = await ise_client._make_request("/mutual_funds")
            return [types.TextContent(
                type="text",
                text=f"Mutual Funds Data:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_price_shockers":
            data = await ise_client._make_request("/price_shockers")
            return [types.TextContent(
                type="text",
                text=f"Price Shockers:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_commodities":
            data = await ise_client._make_request("/commodities")
            return [types.TextContent(
                type="text",
                text=f"Commodity Futures Data:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_analyst_recommendations":
            data = await ise_client._make_request("/stock_target_price", {"stock_id": arguments["stock_id"]})
            return [types.TextContent(
                type="text",
                text=f"Analyst Recommendations for {arguments['stock_id']}:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_stock_forecasts":
            params = {
                "stock_id": arguments["stock_id"],
                "measure_code": arguments["measure_code"],
                "period_type": arguments["period_type"],
                "data_type": arguments["data_type"],
                "age": arguments["age"]
            }
            data = await ise_client._make_request("/stock_forecasts", params)
            return [types.TextContent(
                type="text",
                text=f"Stock Forecasts for {arguments['stock_id']}:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_historical_data":
            params = {"stock_name": arguments["stock_name"]}
            if "period" in arguments:
                params["period"] = arguments["period"]
            if "filter" in arguments:
                params["filter"] = arguments["filter"]
            
            data = await ise_client._make_request("/historical_data", params)
            return [types.TextContent(
                type="text",
                text=f"Historical Data for {arguments['stock_name']}:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        elif name == "get_historical_stats":
            params = {
                "stock_name": arguments["stock_name"],
                "stats": arguments["stats"]
            }
            data = await ise_client._make_request("/historical_stats", params)
            return [types.TextContent(
                type="text",
                text=f"Historical Stats ({arguments['stats']}) for {arguments['stock_name']}:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]

class JSONRPCHandler:
    """Handle JSON-RPC requests for MCP over HTTP"""
    
    def __init__(self, mcp_server: Server):
        self.mcp_server = mcp_server
    
    async def handle_jsonrpc(self, request: Request) -> Response:
        """Handle JSON-RPC request with improved error handling for Dify compatibility"""
        try:
            # Log request details for debugging
            logger.info(f"📥 Request from: {request.remote} - {request.method} {request.path}")
            logger.info(f"📥 User-Agent: {request.headers.get('User-Agent', 'unknown')}")
            
            # Parse JSON-RPC request
            data = await request.json()
            logger.info(f"📥 JSON-RPC request: {data}")
            
            # Validate required JSON-RPC fields with better error handling
            jsonrpc_version = data.get("jsonrpc")
            if jsonrpc_version != "2.0":
                logger.warning(f"Invalid JSON-RPC version: {jsonrpc_version}")
                return self._create_error_response(
                    {"code": -32600, "message": "Invalid Request - JSON-RPC version must be 2.0"},
                    request_id=data.get("id")
                )
            
            method = data.get("method")
            params = data.get("params", {})
            request_id = data.get("id")
            
            # Handle missing method field (common issue with Dify)
            if method is None:
                # Check if this looks like a malformed notification/initialized
                if "initialized" in str(data):
                    logger.info("Detected malformed initialized notification, treating as valid")
                    return self._create_success_response({}, request_id)
                
                logger.error(f"Missing method field in request: {data}")
                return self._create_error_response(
                    {"code": -32600, "message": "Invalid Request - method field is required"},
                    request_id=request_id
                )
            
            # Handle requests vs notifications
            # A notification is a JSON-RPC message without an "id" field at all
            is_notification = "id" not in data
            
            if is_notification:
                logger.info(f"📥 JSON-RPC notification: {method}")
            else:
                logger.info(f"📥 JSON-RPC request: {method} (id: {request_id})")
            
            result = None
            error = None
            
            try:
                if method == "tools/list":
                    tools = await handle_list_tools()
                    # Clean up tool serialization - only include required MCP fields
                    clean_tools = []
                    for tool in tools:
                        clean_tool = {
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": tool.inputSchema
                        }
                        clean_tools.append(clean_tool)
                    result = {"tools": clean_tools}
                
                elif method == "tools/call":
                    tool_name = params.get("name")
                    tool_arguments = params.get("arguments", {})
                    
                    if not tool_name:
                        error = {"code": -32602, "message": "Missing tool name"}
                    else:
                        tool_result = await handle_call_tool(tool_name, tool_arguments)
                        # Clean up content serialization 
                        clean_content = []
                        for content in tool_result:
                            clean_content_item = {
                                "type": content.type,
                                "text": content.text
                            }
                            clean_content.append(clean_content_item)
                        result = {"content": clean_content}
                
                elif method == "initialize":
                    # Enhanced initialization handling for Dify compatibility
                    client_info = params.get("clientInfo", {})
                    client_name = client_info.get("name", "unknown")
                    client_version = client_info.get("version", "unknown")
                    
                    logger.info(f"Initializing connection from {client_name} v{client_version}")
                    
                    result = {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": Config.SERVER_NAME,
                            "version": "1.0.0"
                        }
                    }
                
                elif method == "notifications/initialized":
                    # Handle initialization complete notification
                    logger.info("Client initialization completed")
                    # For notifications, we don't send a response (per JSON-RPC spec)
                    return Response(
                        text="",
                        status=202,  # Accepted
                        headers=self._get_cors_headers()
                    )
                
                elif method == "ping":
                    result = {}
                
                else:
                    error = {"code": -32601, "message": f"Method not found: {method}"}
            
            except Exception as e:
                logger.error(f"Error handling method {method}: {str(e)}", exc_info=True)
                error = {"code": -32603, "message": f"Internal error: {str(e)}"}
            
            # For notifications, don't send a response unless there's an error
            if is_notification and not error:
                return Response(
                    text="",
                    status=202,  # Accepted
                    headers=self._get_cors_headers()
                )
            
            # Create JSON-RPC response
            if error:
                return self._create_error_response(error, request_id)
            else:
                return self._create_success_response(result, request_id)
        
        except json.JSONDecodeError as e:
            logger.error(f"📤 JSON Parse Error: {str(e)}")
            return self._create_error_response(
                {"code": -32700, "message": "Parse error"},
                request_id=None,
                status=400
            )
        
        except Exception as e:
            logger.error(f"📤 Unexpected error in JSON-RPC handler: {str(e)}", exc_info=True)
            request_id = data.get("id") if 'data' in locals() else None
            return self._create_error_response(
                {"code": -32603, "message": f"Internal error: {str(e)}"},
                request_id=request_id,
                status=500
            )

    def _get_cors_headers(self) -> dict:
        """Get CORS headers for responses"""
        return {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, x-requested-with",
            "Access-Control-Max-Age": "86400",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Connection": "keep-alive"
        }
    
    def _create_success_response(self, result: Any, request_id: Any) -> Response:
        """Create a successful JSON-RPC response"""
        response_data = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        
        logger.info(f"📤 JSON-RPC Success Response (id: {request_id})")
        response_text = json.dumps(response_data, ensure_ascii=False, separators=(',', ':'))
        
        return Response(
            text=response_text,
            content_type="application/json",
            charset="utf-8",
            headers=self._get_cors_headers()
        )
    
    def _create_error_response(self, error: dict, request_id: Any, status: int = 200) -> Response:
        """Create an error JSON-RPC response"""
        response_data = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error
        }
        
        logger.error(f"📤 JSON-RPC Error Response: {error}")
        response_text = json.dumps(response_data, ensure_ascii=False, separators=(',', ':'))
        
        return Response(
            text=response_text,
            content_type="application/json",
            charset="utf-8",
            status=status,
            headers=self._get_cors_headers()
        )

    async def handle_options(self, request: Request) -> Response:
        """Handle CORS preflight requests"""
        return Response(
            text="",
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, x-requested-with",
                "Access-Control-Max-Age": "86400",
                "Content-Length": "0"
            }
        )

    async def handle_health(self, request: Request) -> Response:
        """Health check endpoint"""
        return Response(
            text=json.dumps({
                "status": "healthy",
                "server": Config.SERVER_NAME,
                "version": "1.0.0"
            }),
            content_type="application/json"
        )

    async def handle_info(self, request: Request) -> Response:
        """Server info endpoint"""
        tools = await handle_list_tools()
        return Response(
            text=json.dumps({
                "server": Config.SERVER_NAME,
                "version": "1.0.0",
                "description": "Indian Stock Exchange MCP Server",
                "capabilities": {
                    "tools": len(tools)
                },
                "tools": [{"name": tool.name, "description": tool.description} for tool in tools]
            }, indent=2, ensure_ascii=False),
            content_type="application/json"
        )

@middleware
async def cors_middleware(request: Request, handler):
    """CORS middleware for all requests"""
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return web.Response(
            text="",
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, x-requested-with",
                "Access-Control-Max-Age": "86400",
                "Content-Length": "0"
            }
        )
    
    # Process the request
    try:
        response = await handler(request)
        # Add CORS headers to response
        response.headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, x-requested-with",
        })
        return response
    except Exception as e:
        logger.error(f"Request handler error: {e}")
        # Return error with CORS headers
        return web.Response(
            text=json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, x-requested-with",
            }
        )

async def create_app() -> Application:
    """Create aiohttp application"""
    app_http = Application(middlewares=[cors_middleware])
    
    # Create JSON-RPC handler
    rpc_handler = JSONRPCHandler(app)
    
    # Add routes
    app_http.router.add_post("/jsonrpc", rpc_handler.handle_jsonrpc)
    app_http.router.add_options("/jsonrpc", rpc_handler.handle_options)
    app_http.router.add_get("/health", rpc_handler.handle_health)
    app_http.router.add_get("/info", rpc_handler.handle_info)
    app_http.router.add_get("/", rpc_handler.handle_info)  # Root endpoint shows info
    
    return app_http

async def main():
    """Main entry point for the HTTP server"""
    logger.info(f"Starting Indian Stock Exchange MCP HTTP Server...")
    
    # Validate configuration
    try:
        Config.validate_config()
        logger.info(f"Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    logger.info(f"Server will listen on {Config.HTTP_HOST}:{Config.HTTP_PORT}")
    
    # Create aiohttp application
    app_http = await create_app()
    
    # Create and start the HTTP server
    runner = web.AppRunner(app_http)
    await runner.setup()
    
    site = web.TCPSite(runner, Config.HTTP_HOST, Config.HTTP_PORT)
    await site.start()
    
    logger.info(f"Server started successfully!")
    logger.info(f"JSON-RPC endpoint: http://{Config.HTTP_HOST}:{Config.HTTP_PORT}/jsonrpc")
    logger.info(f"Server info: http://{Config.HTTP_HOST}:{Config.HTTP_PORT}/info")
    logger.info(f" Health check: http://{Config.HTTP_HOST}:{Config.HTTP_PORT}/health")
    logger.info(f"API Base URL: {Config.BASE_URL}")
    
    # Connection help for different clients
    logger.info(f"🔗 Client Connection URLs:")
    logger.info(f"   • VSCode: http://localhost:{Config.HTTP_PORT}/jsonrpc")
    logger.info(f"   • Cursor: http://localhost:{Config.HTTP_PORT}/jsonrpc") 
    logger.info(f"   • External: http://{Config.HTTP_HOST}:{Config.HTTP_PORT}/jsonrpc")
    
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        await runner.cleanup()
        await ise_client.close()

def cli_main():
    """Synchronous entry point for console script"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped.")
    except Exception as e:
        logger.error(f"Server error: {e}")


if __name__ == "__main__":
    cli_main() 