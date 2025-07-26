# 🇮🇳 Indian Stock Exchange MCP Server

A comprehensive **Model Context Protocol (MCP) server** that provides real-time access to Indian Stock Exchange data from **BSE & NSE**. Built with Python and the official MCP SDK, this server offers 14 powerful tools for market analysis, stock research, and financial data retrieval.

## 🌟 Features

- **14 Stock Market Tools** - Complete market data access
- **Real-time Data** - Live BSE & NSE market information
- **HTTP JSON-RPC Server** - Compatible with Claude Desktop, Cursor, and VSCode
- **Comprehensive Coverage** - Stocks, mutual funds, commodities, historical data
- **Industry Analysis** - Search companies by sector/industry
- **Historical Analytics** - Quarterly results, balance sheets, cash flow
- **Analyst Insights** - Recommendations and forecasts
- **Type-Safe** - Full TypeScript/Python type definitions

## 📊 Available Tools

### Market Data (5 tools)

1. **`get_trending_stocks`** - Top gainers and losers
2. **`get_nse_most_active`** - Most active NSE stocks by volume
3. **`get_bse_most_active`** - Most active BSE stocks by volume
4. **`get_52_week_high_low`** - 52-week high/low performers
5. **`get_price_shockers`** - Stocks with significant price changes

### Company Information (3 tools)

6. **`get_stock_data`** - Detailed company financial data
7. **`search_industry`** - Find companies by industry/sector
8. **`get_analyst_recommendations`** - Analyst ratings and target prices

### Historical Analysis (2 tools)

9. **`get_historical_data`** - Historical price and ratio data
10. **`get_historical_stats`** - Quarterly results, balance sheets, ratios

### Mutual Funds (2 tools)

11. **`search_mutual_funds`** - Search mutual fund schemes
12. **`get_mutual_funds`** - Latest mutual fund NAV and returns

### Commodities & Advanced (2 tools)

13. **`get_commodities`** - Real-time commodity futures data
14. **`get_stock_forecasts`** - Advanced forecasting data

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Active internet connection for market data

### Installation

1. **Clone/Download the project:**

   ```bash
   git clone <repository-url>
   cd ise_mcp
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional):**

   ```bash
   python setup.py  # Creates .env file with default settings
   ```

4. **Start the server:**

   ```bash
   python ise_mcp_server.py
   ```

   You should see:

   ```
   INFO:ise-mcp-server:🚀 Indian Stock Exchange MCP Server starting...
   INFO:ise-mcp-server:📊 Server: indian-stock-exchange v1.0.0
   INFO:ise-mcp-server:🔧 Tools: 14 tools loaded
   INFO:ise-mcp-server:🌐 HTTP Server running on http://0.0.0.0:8000
   INFO:ise-mcp-server:📡 JSON-RPC endpoint: http://0.0.0.0:8000/jsonrpc
   INFO:ise-mcp-server:❤️ Health check: http://0.0.0.0:8000/health
   ```

## 🔧 Client Setup

### 1. Claude Desktop Setup

**Step 1:** Install Claude Desktop from [claude.ai](https://claude.ai/download)

**Step 2:** Open Claude Desktop settings (Ctrl/Cmd + ,)

**Step 3:** Add MCP server configuration:

```json
{
  "mcpServers": {
    "indian-stock-exchange": {
      "command": "python",
      "args": ["D:/Pro/Migration/ise_mcp/ise_mcp_server.py"],
      "env": {
        "PYTHONPATH": "D:/Pro/Migration/ise_mcp"
      }
    }
  }
}
```

**Step 4:** Restart Claude Desktop

**Step 5:** Verify connection - you should see "14 tools enabled" in the status bar

### 2. Cursor Setup

**Step 1:** Install Cursor from [cursor.sh](https://cursor.sh)

**Step 2:** Start your MCP server:

```bash
python ise_mcp_server.py
```

**Step 3:** Open Cursor Settings (Ctrl/Cmd + ,)

**Step 4:** Go to "Extensions" → Search for "MCP" → Install MCP extension

**Step 5:** Add server configuration:

```json
{
  "mcp.servers": {
    "indian-stock-exchange": {
      "transport": "http",
      "url": "http://localhost:8000/jsonrpc",
      "name": "Indian Stock Exchange"
    }
  }
}
```

**Step 6:** Restart Cursor

**Step 7:** Check status bar for "14 tools enabled"

### 3. VSCode Setup

**Step 1:** Install VSCode from [code.visualstudio.com](https://code.visualstudio.com)

**Step 2:** Install the MCP extension:

- Open Extensions (Ctrl/Cmd + Shift + X)
- Search for "Model Context Protocol"
- Install the official MCP extension

**Step 3:** Start your MCP server:

```bash
python ise_mcp_server.py
```

**Step 4:** Configure in settings.json:

```json
{
  "mcp.servers": [
    {
      "name": "indian-stock-exchange",
      "transport": "http",
      "url": "http://localhost:8000/jsonrpc",
      "description": "Indian Stock Exchange Data"
    }
  ]
}
```

**Step 5:** Reload VSCode (Ctrl/Cmd + Shift + P → "Developer: Reload Window")

**Step 6:** Open Command Palette → "MCP: Connect to Server"

## 📈 Demo Execution

### Demo 1: Market Overview

**In Claude Desktop/Cursor/VSCode, ask:**

```
Show me the current market trends and most active stocks
```

**Expected Response:**

```
I'll get you the current market trends and most active stocks from both NSE and BSE.

🔥 Trending Stocks:
Top Gainers:
• Adani Enterprises: +8.45%
• Tata Motors: +6.23%
• HDFC Bank: +4.17%

Top Losers:
• Paytm: -5.67%
• Zomato: -4.32%
• BYJU'S: -3.89%

📊 NSE Most Active:
1. Reliance Industries - ₹2,456.70 (+2.34%)
2. TCS - ₹3,789.15 (+1.67%)
3. Infosys - ₹1,543.20 (+0.98%)
4. HDFC Bank - ₹1,678.45 (+4.17%)
5. ITC - ₹412.30 (-0.56%)

📈 BSE Most Active:
1. Sensex Heavyweights showing strong volume
2. Banking sector leading trading activity
```

### Demo 2: Company Analysis

**Ask:**

```
Analyze Reliance Industries stock with historical data and analyst recommendations
```

**Expected Response:**

```
📊 Reliance Industries Analysis:

💼 Company Overview:
• Current Price: ₹2,456.70 (+2.34%)
• Market Cap: ₹16,58,432 Crores
• Sector: Oil & Gas / Petrochemicals
• Industry: Integrated Oil & Gas

📈 Historical Performance:
• 52-Week High: ₹2,856.15
• 52-Week Low: ₹2,120.30
• Year-to-Date: +12.45%

🎯 Analyst Recommendations:
• Overall Rating: BUY
• Target Price: ₹2,750.00
• Upside Potential: +11.94%
• Analysts Coverage: 25 analysts

📚 Recent Quarterly Results:
Q3 FY24: Revenue ₹2,35,122 Cr (+8.2% YoY)
Profit: ₹18,951 Cr (+15.3% YoY)
```

### Demo 3: Industry Research

**Ask:**

```
Find the top banking companies and their current performance
```

**Expected Response:**

```
🏦 Banking Sector Analysis:

Top Banking Companies:
1. HDFC Bank - ₹1,678.45 (+4.17%)
   • Rating: BUY
   • P/E Ratio: 18.7
   • ROE: 17.2%

2. ICICI Bank - ₹1,034.20 (+2.89%)
   • Rating: BUY  
   • P/E Ratio: 15.4
   • ROE: 16.8%

3. State Bank of India - ₹567.80 (+1.45%)
   • Rating: HOLD
   • P/E Ratio: 12.3
   • ROE: 14.5%

4. Axis Bank - ₹987.65 (+0.98%)
   • Rating: BUY
   • P/E Ratio: 13.7
   • ROE: 15.2%

📊 Sector Performance:
• Banking Index: +2.34% (Day)
• YTD Performance: +18.67%
• Outlook: Positive due to economic growth
```

### Demo 4: Mutual Fund Research

**Ask:**

```
Show me the best performing equity mutual funds
```

**Expected Response:**

```
💰 Top Performing Equity Mutual Funds:

🏆 Large Cap Funds:
1. HDFC Top 100 Fund
   • NAV: ₹789.34
   • 1Y Return: +18.45%
   • 3Y Return: +12.67% (CAGR)

2. ICICI Prudential Bluechip Fund
   • NAV: ₹567.89
   • 1Y Return: +16.78%
   • 3Y Return: +11.23% (CAGR)

🚀 Mid Cap Funds:
1. DSP Midcap Fund
   • NAV: ₹156.78
   • 1Y Return: +24.56%
   • 3Y Return: +15.89% (CAGR)

📈 Small Cap Funds:
1. SBI Small Cap Fund
   • NAV: ₹234.12
   • 1Y Return: +28.34%
   • 3Y Return: +18.45% (CAGR)
```

## 🔍 Testing the Server

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:** `{"status": "healthy", "server": "indian-stock-exchange", "version": "1.0.0"}`

### List Tools

```bash
curl -X POST http://localhost:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
  }'
```

### Call a Tool

```bash
curl -X POST http://localhost:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_trending_stocks",
      "arguments": {}
    },
    "id": 2
  }'
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# API Configuration
BASE_URL=https://stock.indianapi.in/
API_KEY=your_api_key_here

# Server Configuration  
HTTP_HOST=0.0.0.0
HTTP_PORT=8000
SERVER_NAME=indian-stock-exchange
LOG_LEVEL=INFO

# Timeouts
REQUEST_TIMEOUT=30
```

### Server Ports

- **Main Server:** <http://localhost:8000>
- **JSON-RPC Endpoint:** <http://localhost:8000/jsonrpc>
- **Health Check:** <http://localhost:8000/health>
- **Server Info:** <http://localhost:8000/info>

## 🛠️ Tool Reference

### Market Data Tools

#### `get_trending_stocks`

```javascript
// No parameters required
{
  "name": "get_trending_stocks",
  "arguments": {}
}
```

#### `get_nse_most_active` / `get_bse_most_active`

```javascript
// No parameters required
{
  "name": "get_nse_most_active", 
  "arguments": {}
}
```

#### `get_52_week_high_low`

```javascript
// No parameters required
{
  "name": "get_52_week_high_low",
  "arguments": {}
}
```

### Company Tools

#### `get_stock_data`

```javascript
{
  "name": "get_stock_data",
  "arguments": {
    "name": "Reliance"  // Company name or symbol
  }
}
```

#### `search_industry`

```javascript
{
  "name": "search_industry",
  "arguments": {
    "query": "Banking"  // Industry search term
  }
}
```

#### `get_analyst_recommendations`

```javascript
{
  "name": "get_analyst_recommendations",
  "arguments": {
    "stock_id": "TCS"  // Stock symbol
  }
}
```

### Historical Data Tools

#### `get_historical_data`

```javascript
{
  "name": "get_historical_data",
  "arguments": {
    "stock_name": "TCS",
    "period": "1yr",        // 1m, 6m, 1yr, 3yr, 5yr, 10yr, max
    "filter": "price"       // default, price, pe, sm, evebitda, ptb, mcs
  }
}
```

#### `get_historical_stats`

```javascript
{
  "name": "get_historical_stats",
  "arguments": {
    "stock_name": "TCS",
    "stats": "quarter_results"  // quarter_results, yoy_results, balancesheet, etc.
  }
}
```

## 🐛 Troubleshooting

### Common Issues

#### "0 tools enabled" in Cursor/VSCode

**Solution:** Ensure server is running and accessible:

```bash
# Check if server is running
curl http://localhost:8000/health

# Restart server if needed
python ise_mcp_server.py
```

#### "fetch failed" error

**Solutions:**

1. **Check server status:**

   ```bash
   python ise_mcp_server.py
   ```

2. **Verify port availability:**

   ```bash
   netstat -an | grep 8000
   ```

3. **Test with curl:**

   ```bash
   curl -X POST http://localhost:8000/jsonrpc \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
   ```

#### Connection timeout

**Solutions:**

1. **Increase timeout in config.py:**

   ```python
   REQUEST_TIMEOUT = 60  # Increase from 30
   ```

2. **Check firewall settings**

3. **Verify network connectivity**

#### API rate limits

**Solution:** The server includes automatic rate limiting and retry logic. If you hit limits:

1. Wait a few seconds between requests
2. Check your API key quota
3. Consider caching frequently accessed data

### Server Logs

Monitor server logs for debugging:

```bash
python ise_mcp_server.py --log-level DEBUG
```

### Performance Tips

1. **Keep server running** - Don't restart between requests
2. **Use appropriate timeouts** - Adjust based on your network
3. **Monitor API usage** - Some endpoints have rate limits
4. **Cache results** - For frequently accessed data

## 📝 API Documentation

For complete API documentation of the underlying stock data service, refer to the Indian Stock API documentation at `https://stock.indianapi.in/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Indian Stock API** for providing comprehensive market data
- **MCP SDK** for the excellent protocol implementation
- **Python asyncio** for high-performance async operations

---

## 🚀 Ready to Use

Your Indian Stock Exchange MCP Server is now ready to provide real-time market data to Claude Desktop, Cursor, VSCode, and any other MCP-compatible client!

### Quick Test

```bash
# Start server
python ise_mcp_server.py

# In your MCP client, ask:
"Show me trending stocks and NSE most active stocks"
```

**Happy Trading! 📈🇮🇳**
