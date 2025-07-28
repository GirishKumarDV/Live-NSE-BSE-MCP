# Indian Stock Exchange MCP Server

This server provides access to live market data from Indian Stock Exchanges (BSE & NSE) through the Model Context Protocol (MCP), powered by [IndianAPI](https://indianapi.in/).

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- **API Key from IndianAPI**: Sign up at [https://indianapi.in/](https://indianapi.in/) and obtain an API key for the Stock Market API

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd ise_mcp
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Get your API key**:
   - Visit [https://indianapi.in/](https://indianapi.in/)
   - Sign up for a free account
   - Navigate to the Stock Market API section
   - Subscribe to get your API key

4. **Configure environment variables**:

   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your IndianAPI key
   # ISE_API_KEY=your_indianapi_key_here
   ```

5. **Start the server**:

   ```bash
   python ise_mcp_server.py
   ```

The server will start on `http://localhost:8000` by default.

## 🔧 Configuration

The server uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

```bash
# Required: API Key from IndianAPI (https://indianapi.in/)
ISE_API_KEY=your_indianapi_key_here

# Optional: API Base URL (default: https://stock.indianapi.in/)
ISE_API_BASE_URL=https://stock.indianapi.in/

# Optional: Server configuration
ISE_HTTP_HOST=0.0.0.0
ISE_HTTP_PORT=8000
ISE_REQUEST_TIMEOUT=30
ISE_LOG_LEVEL=INFO
```

**Important**: The `ISE_API_KEY` is required and the server will not start without it. Make sure to add your `.env` file to `.gitignore` to prevent committing sensitive information.

## 🌐 Client Connections

### Using with Cursor/VSCode

- **URL**: `http://localhost:8000/jsonrpc`
- **Type**: HTTP JSON-RPC

### Using with Dify

- **URL**: `http://localhost:8000/jsonrpc`
- **Type**: MCP over HTTP

## 📊 Available Tools

The server provides the following tools for accessing Indian stock market data:

### Market Data Tools

- `get_stock_data` - Get detailed financial data for a specific company
- `get_trending_stocks` - Get trending stocks with top gainers and losers
- `get_52_week_high_low` - Get stocks with highest and lowest prices in the last 52 weeks
- `get_nse_most_active` - Get most active stocks on NSE by trading volume
- `get_bse_most_active` - Get most active stocks on BSE by trading volume
- `get_price_shockers` - Get stocks with significant price changes

### Research Tools

- `search_industry` - Search for companies within a specific industry
- `get_analyst_recommendations` - Get analyst target prices and recommendations
- `get_stock_forecasts` - Get detailed forecast information for a stock
- `get_historical_data` - Get historical stock data with various filters
- `get_historical_stats` - Get historical statistics for a stock

### Investment Tools

- `search_mutual_funds` - Search for mutual funds
- `get_mutual_funds` - Get latest mutual fund data with NAV and returns
- `get_commodities` - Get real-time commodity futures data

## 🔗 API Endpoints

### Health Check

```bash
GET http://localhost:8000/health
```

### Server Information

```bash
GET http://localhost:8000/info
```

### MCP JSON-RPC

```bash
POST http://localhost:8000/jsonrpc
```

## 📝 Example Usage

### Get Stock Data

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_stock_data",
    "arguments": {
      "name": "Reliance"
    }
  },
  "id": 1
}
```

### Get Trending Stocks

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_trending_stocks",
    "arguments": {}
  },
  "id": 2
}
```

## 🛠️ Development

### Running Tests

```bash
python test_tools.py
python test_connection.py
```

### Debug Mode

Set the log level to DEBUG in your `.env` file:

```bash
ISE_LOG_LEVEL=DEBUG
```

## 🔒 Security

- **Environment Variables**: All sensitive configuration is stored in environment variables
- **API Key Protection**: The API key is never logged or exposed in responses
- **CORS**: Proper CORS headers are set for cross-origin requests
- **Input Validation**: All tool inputs are validated against JSON schemas

## 🐛 Troubleshooting

### Common Issues

1. **Server won't start**: Check that your `ISE_API_KEY` from [IndianAPI](https://indianapi.in/) is set in the `.env` file
2. **API errors**: Verify your IndianAPI key is valid and has sufficient quota
3. **Connection issues**: Ensure the server is running on the correct host/port
4. **CORS errors**: The server includes CORS headers, but check your client configuration

### Error Handling

The server provides detailed error messages in JSON-RPC format:

- `-32600`: Invalid Request
- `-32601`: Method not found  
- `-32602`: Invalid params
- `-32603`: Internal error

## 📚 Related Projects

- **MCP Client**: [client/](./client/) - Python client for testing
- **Examples**: [examples/](./examples/) - Usage examples
- **Gemini Advisor**: [gemini_financial_advisor.py](./gemini_financial_advisor.py) - AI-powered financial analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **IndianAPI Marketplace**: <https://indianapi.in/>
- **Indian Stock API**: <https://stock.indianapi.in/>
- **Model Context Protocol**: <https://modelcontextprotocol.io/>
- **MCP Specification**: <https://spec.modelcontextprotocol.io/>

---

Made with ❤️ for the Indian Stock Market community
