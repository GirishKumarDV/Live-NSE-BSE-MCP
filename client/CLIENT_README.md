# Python MCP Client for Indian Stock Exchange

A comprehensive Python MCP (Model Context Protocol) client that provides easy access to Indian Stock Exchange data through your MCP server.

## Features

- **Generic MCP Client**: Connect to any HTTP-based MCP server
- **Specialized ISE Client**: Pre-built methods for all Indian Stock Exchange tools
- **Async Support**: Built with asyncio for high performance
- **Type Safety**: Full type hints and data validation
- **Easy to Use**: Simple, intuitive API

## Installation

```bash
pip install -r client_requirements.txt
```

## Quick Start

### Basic Usage

```python
import asyncio
from simple_mcp_client import ISEMCPClient

async def main():
    # Create client
    client = ISEMCPClient()
    
    try:
        # Connect to server
        await client.connect()
        
        # Get trending stocks
        trending = await client.get_trending_stocks()
        print("Trending stocks:", trending)
        
        # Get stock data
        reliance_data = await client.get_stock_data("Reliance")
        print("Reliance data:", reliance_data)
        
    finally:
        await client.close()

asyncio.run(main())
```

### Generic MCP Client

```python
from simple_mcp_client import SimpleMCPClient

async def main():
    # Connect to any MCP server
    client = SimpleMCPClient("http://localhost:8000/jsonrpc")
    
    await client.connect()
    
    # List available tools
    tools = await client.list_tools()
    for tool in tools:
        print(f"Tool: {tool.name} - {tool.description}")
    
    # Call any tool
    result = await client.call_tool("get_trending_stocks")
    print("Result:", result)
    
    await client.close()

asyncio.run(main())
```

## ISE Client Methods

The `ISEMCPClient` provides convenient methods for all stock market tools:

### Market Data

```python
# Get trending stocks (gainers and losers)
trending = await client.get_trending_stocks()

# Get most active stocks
nse_active = await client.get_nse_most_active()
bse_active = await client.get_bse_most_active()

# Get 52-week high/low data
high_low = await client.get_52_week_high_low()

# Get price shockers
shockers = await client.get_price_shockers()
```

### Company Information

```python
# Get detailed stock data
stock_data = await client.get_stock_data("Reliance")

# Search by industry
banking_companies = await client.search_industry("Banking")

# Get analyst recommendations
recommendations = await client.get_analyst_recommendations("TCS")
```

### Historical Analysis

```python
# Get historical price data
history = await client.get_historical_data("TCS", period="1yr", filter_type="price")

# Get quarterly results
quarters = await client.get_historical_stats("TCS", stats_type="quarter_results")

# Available periods: 1m, 6m, 1yr, 3yr, 5yr, 10yr, max
# Available filters: default, price, pe, sm, evebitda, ptb, mcs
# Available stats: quarter_results, yoy_results, balancesheet, cashflow, ratios, shareholding_pattern_quarterly, shareholding_pattern_yearly
```

### Mutual Funds

```python
# Search mutual funds
equity_funds = await client.search_mutual_funds("equity")

# Get latest mutual fund data
latest_funds = await client.get_mutual_funds()
```

### Commodities

```python
# Get commodity futures data
commodities = await client.get_commodities()
```

## Complete Example

```python
import asyncio
import json
from simple_mcp_client import ISEMCPClient

async def market_dashboard():
    """Create a simple market dashboard"""
    client = ISEMCPClient()
    
    try:
        # Connect
        print("🔌 Connecting to ISE MCP Server...")
        await client.connect()
        
        # Server info
        info = client.get_server_info()
        print(f"📊 Connected to: {info.get('name')} v{info.get('version')}")
        
        # Market overview
        print("\n📈 Market Overview:")
        
        # Trending stocks
        trending = await client.get_trending_stocks()
        if trending:
            data = json.loads(trending)
            gainers = data["trending_stocks"]["top_gainers"][:3]
            losers = data["trending_stocks"]["top_losers"][:3]
            
            print("🔥 Top Gainers:")
            for stock in gainers:
                print(f"   • {stock['company_name']}: +{stock['percent_change']}%")
            
            print("📉 Top Losers:")
            for stock in losers:
                print(f"   • {stock['company_name']}: {stock['percent_change']}%")
        
        # Most active stocks
        print("\n📊 NSE Most Active:")
        nse_active = await client.get_nse_most_active()
        if nse_active:
            data = json.loads(nse_active)
            for i, stock in enumerate(data[:5], 1):
                print(f"   {i}. {stock['company']} - ₹{stock['price']} ({stock['percent_change']}%)")
        
        # Industry analysis
        print("\n🏦 Banking Sector:")
        banking = await client.search_industry("Banking")
        if banking:
            data = json.loads(banking)
            for i, company in enumerate(data[:3], 1):
                rating = company.get('activeStockTrends', {}).get('overallRating', 'N/A')
                print(f"   {i}. {company['commonName']} - {rating}")
        
        # Specific stock analysis
        print("\n📈 Reliance Analysis:")
        reliance = await client.get_stock_data("Reliance")
        if reliance:
            print("   ✅ Detailed data retrieved")
        
        # Historical analysis
        print("\n📚 TCS Historical Performance:")
        tcs_history = await client.get_historical_stats("TCS", "quarter_results")
        if tcs_history:
            data = json.loads(tcs_history)
            if "Sales" in data:
                recent_quarter = list(data["Sales"].keys())[-1]
                sales = data["Sales"][recent_quarter]
                print(f"   Latest Quarter ({recent_quarter}): ₹{sales} Cr Sales")
        
        print("\n✅ Market dashboard completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await client.close()

# Run the dashboard
asyncio.run(market_dashboard())
```

## Running Examples

The package includes comprehensive examples:

```bash
# Run interactive examples
python examples/basic_usage.py

# Choose from:
# 1. Basic Usage
# 2. Market Overview
# 3. Industry Analysis  
# 4. Mutual Funds
# 5. Historical Analysis
# 6. Generic Client
# 7. Run All Examples
```

## API Reference

### SimpleMCPClient

Generic MCP client for any HTTP-based MCP server.

```python
class SimpleMCPClient:
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None)
    async def connect(self) -> bool
    async def list_tools(self) -> List[Tool]
    async def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any
    def get_tool(self, name: str) -> Optional[Tool]
    def get_server_info(self) -> Dict[str, Any]
    async def close(self)
```

### ISEMCPClient

Specialized client for Indian Stock Exchange MCP server.

```python
class ISEMCPClient(SimpleMCPClient):
    def __init__(self, url: str = "http://localhost:8000/jsonrpc")
    
    # Market data methods
    async def get_trending_stocks(self) -> Dict[str, Any]
    async def get_nse_most_active(self) -> Dict[str, Any]
    async def get_bse_most_active(self) -> Dict[str, Any]
    async def get_52_week_high_low(self) -> Dict[str, Any]
    async def get_price_shockers(self) -> Dict[str, Any]
    
    # Company data methods
    async def get_stock_data(self, company_name: str) -> Dict[str, Any]
    async def search_industry(self, industry: str) -> Dict[str, Any]
    async def get_analyst_recommendations(self, stock_id: str) -> Dict[str, Any]
    
    # Historical data methods
    async def get_historical_data(self, stock_name: str, period: str = "1yr", filter_type: str = "price") -> Dict[str, Any]
    async def get_historical_stats(self, stock_name: str, stats_type: str = "quarter_results") -> Dict[str, Any]
    
    # Mutual funds methods
    async def search_mutual_funds(self, query: str) -> Dict[str, Any]
    async def get_mutual_funds(self) -> Dict[str, Any]
    
    # Commodities methods
    async def get_commodities(self) -> Dict[str, Any]
```

### Tool

Data class representing an MCP tool.

```python
@dataclass
class Tool:
    name: str
    description: str
    inputSchema: Dict[str, Any]
```

## Error Handling

```python
from simple_mcp_client import ISEMCPClient

async def safe_example():
    client = ISEMCPClient()
    
    try:
        # Connection errors
        if not await client.connect():
            print("Failed to connect to server")
            return
        
        # Tool call errors
        try:
            data = await client.get_stock_data("NonExistentCompany")
        except Exception as e:
            print(f"Tool call failed: {e}")
        
    except Exception as e:
        print(f"Client error: {e}")
    
    finally:
        # Always close the client
        await client.close()
```

## Requirements

- Python 3.8+
- httpx >= 0.25.0
- mcp >= 1.0.0
- typing-extensions >= 4.0.0

## Server Requirements

This client requires the Indian Stock Exchange MCP server to be running:

```bash
# Start the MCP server
python ise_mcp_server.py
```

The server should be accessible at `http://localhost:8000/jsonrpc` by default.

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Happy Trading! 📈🇮🇳**
