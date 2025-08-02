# Indian Stock Exchange MCP Server

This server provides access to live market data from Indian Stock Exchanges (BSE & NSE) through the Model Context Protocol (MCP), powered by [IndianAPI](https://indianapi.in/).

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- **API Key from IndianAPI**: Sign up at [https://indianapi.in/](https://indianapi.in/) and obtain an API key for the Stock Market API

### Installation

> **Note**: This package is not yet published to PyPI. Please use source installation for now.

#### Option 1: Quick Install from Source (Recommended)

```bash
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP
pip install -e .
```

#### Option 2: Development Installation

```bash
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP
pip install -r requirements.txt
pip install -e .
```

#### Option 3: Manual Execution (No Installation)

If you prefer not to install the package:

```bash
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP
pip install -r requirements.txt
# Run directly with: python -m ise_mcp.server
```

**Important**: Since the package isn't on PyPI yet, use module execution (`python -m ise_mcp.server`) or install from source for the console scripts to work.

### Configuration

1. **Get your API key**:
   - Visit [https://indianapi.in/](https://indianapi.in/)
   - Sign up for a free account
   - Navigate to the Stock Market API section
   - Subscribe to get your API key

2. **Configure environment variables**:

   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env and add your IndianAPI key
   # ISE_API_KEY=your_indianapi_key_here
   ```

### Usage

#### HTTP Server Mode (for web clients like Cursor, VSCode, Dify)

After installation, you can run the server in several ways:

**Method 1: Module Execution (Recommended)**

```bash
# From the project root directory
python -m ise_mcp.server
```

**Method 2: Using Batch Script (Windows)**

```bash
# Use the provided batch script (note the .\ prefix for PowerShell)
.\ise-mcp-server.bat

# Or with environment variables
$env:ISE_HTTP_PORT=9000; .\ise-mcp-server.bat
```

**Method 3: Development Mode**

```bash
# If not installed, run as module from parent directory
cd ..
python -m ise_mcp.server
```

**Note**: Console scripts from PyPI (`ise-mcp-server`) are not available yet. Use module execution or the batch script instead.

The server will start on `http://localhost:8000` by default.

#### Stdio Mode (for direct MCP clients like Claude Desktop)

**Method 1: Module Execution (Recommended)**

```bash
# From the project root directory
python -m ise_mcp.stdio_server
```

**Method 2: Using Batch Script (Windows)**

```bash
# Use the existing batch script (note the .\ prefix for PowerShell)
.\ise-mcp-stdio.bat
```

**Note**: Console scripts from PyPI (`ise-mcp-stdio`) are not available yet. Use module execution or the batch script instead.

**Important**: Do NOT run the server files directly (e.g., `python server.py`) as this will cause import errors. Always use the console scripts or module execution.

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

## 🌐 Client Integrations

### Claude Desktop Integration

Claude Desktop uses the stdio transport for direct MCP communication.

#### Step 1: Install the Server

Since the package isn't on PyPI yet, install from source:

```bash
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP
pip install -e .
```

#### Step 2: Configure Claude Desktop

**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

Choose one of the following configuration methods based on your setup:

**Option 1: Using Virtual Environment Python (Most Reliable)**

If you have a virtual environment with dependencies installed:

```json
{
  "mcpServers": {
    "ise-mcp": {
      "command": "C:\\path\\to\\your\\project\\venv\\Scripts\\python.exe",
      "args": ["-m", "ise_mcp.stdio_server"],
      "cwd": "C:\\path\\to\\your\\project",
      "env": {
        "ISE_API_KEY": "your_indianapi_key_here"
      }
    }
  }
}
```

**Option 2: Using PYTHONPATH (Recommended Fallback)**

```json
{
  "mcpServers": {
    "ise-mcp": {
      "command": "python",
      "args": ["-m", "ise_mcp.stdio_server"],
      "cwd": "C:\\path\\to\\your\\project",
      "env": {
        "ISE_API_KEY": "your_indianapi_key_here",
        "PYTHONPATH": "C:\\path\\to\\your\\project"
      }
    }
  }
}
```

**Option 3: Using Batch Script (Windows)**

```json
{
  "mcpServers": {
    "ise-mcp": {
      "command": "C:\\path\\to\\your\\project\\ise-mcp-stdio.bat",
      "cwd": "C:\\path\\to\\your\\project",
      "env": {
        "ISE_API_KEY": "your_indianapi_key_here"
      }
    }
  }
}
```

**Option 4: Direct File Execution**

```json
{
  "mcpServers": {
    "ise-mcp": {
      "command": "python",
      "args": ["ise_mcp/stdio_server.py"],
      "cwd": "C:\\path\\to\\your\\project",
      "env": {
        "ISE_API_KEY": "your_indianapi_key_here",
        "PYTHONPATH": "C:\\path\\to\\your\\project"
      }
    }
  }
}
```

**Option 5: Using PowerShell (if execution policies allow)**

```json
{
  "mcpServers": {
    "ise-mcp": {
      "command": "powershell",
      "args": ["-Command", "cd 'C:\\path\\to\\your\\project'; python -m ise_mcp.stdio_server"],
      "env": {
        "ISE_API_KEY": "your_indianapi_key_here"
      }
    }
  }
}
```

**Option 6: After Global Installation**

If you've installed the package globally with `pip install -e .`:

```json
{
  "mcpServers": {
    "ise-mcp": {
      "command": "python",
      "args": ["-m", "ise_mcp.stdio_server"],
      "env": {
        "ISE_API_KEY": "your_indianapi_key_here"
      }
    }
  }
}
```

**macOS/Linux Equivalents:**

For macOS/Linux, replace Windows paths with Unix-style paths:

- `C:\\path\\to\\your\\project` becomes `/path/to/your/project`
- `venv\\Scripts\\python.exe` becomes `venv/bin/python`
- Use forward slashes `/` instead of backslashes `\\`

**Notes:**

- Replace `C:\\path\\to\\your\\project` with your actual project path
- Replace `your_indianapi_key_here` with your actual API key from [IndianAPI](https://indianapi.in/)
- Try options in order - **Option 1** (virtual environment) is most reliable
- If one doesn't work, try the next option

#### Step 3: Restart Claude Desktop

After saving the configuration, restart Claude Desktop. You should see the ISE MCP tools available in your chat.

#### Testing Claude Integration

Once configured, you can ask Claude:

- "Show me trending stocks in the Indian market"
- "Get me data for Reliance Industries"
- "What are the top gainers today?"

### VSCode Integration

VSCode can use the HTTP transport to connect to the MCP server.

#### Step 1: Install MCP Extension

Install an MCP-compatible extension in VSCode or use the built-in MCP support if available.

#### Step 2: Start the HTTP Server

Clone and setup the server first:

```bash
# Clone the repository
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP

# Install dependencies  
pip install -r requirements.txt

# Start the server
python -m ise_mcp.server
```

#### Step 3: Configure VSCode

Add to your VSCode settings.json:

```json
{
  "mcp.servers": {
    "ise-mcp": {
      "url": "http://localhost:8000/jsonrpc",
      "type": "http"
    }
  }
}
```

#### Step 4: Set Environment Variables

Ensure your `ISE_API_KEY` is set:

```bash
# In your terminal before starting VSCode
export ISE_API_KEY=your_indianapi_key_here
code .
```

### Cursor Integration

Cursor supports MCP through HTTP transport.

#### Step 1: Start the HTTP Server

Clone and setup the server first:

```bash
# Clone the repository
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP

# Install dependencies  
pip install -r requirements.txt

# Start the server
python -m ise_mcp.server
```

#### Step 2: Configure Cursor

In Cursor, go to Settings → Extensions → MCP and add:

- **Server URL**: `http://localhost:8000/jsonrpc`
- **Server Type**: HTTP JSON-RPC

#### Step 3: Environment Setup

Make sure your API key is configured in your `.env` file:

```bash
ISE_API_KEY=your_indianapi_key_here
```

#### Testing Cursor Integration

You can now ask Cursor's AI:

- "Use the ISE MCP to get stock data for TCS"
- "Show me the most active stocks on NSE"

### Other MCP Clients

#### HTTP Transport (Web Clients)

For any HTTP-based MCP client:

- **URL**: `http://localhost:8000/jsonrpc`
- **Type**: HTTP JSON-RPC 2.0
- **Content-Type**: `application/json`

#### Stdio Transport (Command Line)

For stdio-based MCP clients:

```bash
# Clone and setup first
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP
pip install -r requirements.txt

# Direct stdio connection
python -m ise_mcp.stdio_server

# Or with environment variables
ISE_API_KEY=your_key python -m ise_mcp.stdio_server
```

### Dify Integration

Dify can connect using HTTP transport:

- **URL**: `http://localhost:8000/jsonrpc`
- **Type**: MCP over HTTP
- **Headers**: `Content-Type: application/json`

## Available Tools

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

## 🛠️ Development & Testing

### Running Tests

The project includes several test files for different aspects of functionality:

#### 1. Tool Testing

```bash
# Test individual MCP tools functionality
python tests/test_tools.py
```

#### 2. Connection Testing

```bash
# Test basic HTTP connections and API responses
python tests/test_connection.py
```

#### 3. Clean Tools Testing

```bash
# Test tool validation and clean responses
python tests/test_clean_tools.py
```

#### 4. VSCode Integration Testing

```bash
# Test VSCode MCP integration
python tests/test_vscode_connection.py
```

#### 5. Run All Tests

```bash
# If you have pytest installed (recommended)
pytest tests/

# Or run all test files manually
python tests/test_tools.py && python tests/test_connection.py && python tests/test_clean_tools.py && python tests/test_vscode_connection.py
```

### Testing with Different Clients

#### Testing with curl

```bash
# Start the HTTP server
python -m ise_mcp.server

# Test health endpoint
curl http://localhost:8000/health

# Test server info
curl http://localhost:8000/info

# Test MCP tool call
curl -X POST http://localhost:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_trending_stocks",
      "arguments": {}
    },
    "id": 1
  }'
```

#### Testing with Python Client

```bash
# Use the included Python client
cd client
python simple_mcp_client.py

# Or run the basic usage example
cd examples
python basic_usage.py
```

### Debug Mode

Set the log level to DEBUG in your `.env` file:

```bash
ISE_LOG_LEVEL=DEBUG
```

### Development Workflow

1. **Setup Development Environment**:

   ```bash
   git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
   cd Live-NSE-BSE-MCP
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Create Configuration**:

   ```bash
   cp env.example .env
   # Edit .env and add your API key
   ```

3. **Run Tests**:

   ```bash
   python tests/test_tools.py
   ```

4. **Start Development Server**:

   ```bash
   python -m ise_mcp.server
   ```

## 🔒 Security

- **Environment Variables**: All sensitive configuration is stored in environment variables
- **API Key Protection**: The API key is never logged or exposed in responses
- **CORS**: Proper CORS headers are set for cross-origin requests
- **Input Validation**: All tool inputs are validated against JSON schemas

## 📦 Publishing to PyPI

> **Current Status**: This package is not yet published to PyPI. Users must install from source.

Users should install from source using the methods described in the [Installation](#installation) section.

### Development Installation

```bash
# Clone and install in development mode
git clone https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git
cd Live-NSE-BSE-MCP
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black .

# Type check
mypy ise_mcp/
```

## 🐛 Troubleshooting

### Common Issues

1. **Relative Import Error** (`attempted relative import with no known parent package`):
   - **Problem**: Running `python server.py` or `python stdio_server.py` directly
   - **Solution**: Use module execution (`python -m ise_mcp.server`, `python -m ise_mcp.stdio_server`) or install from source with `pip install -e .`

2. **Server won't start**:
   - Check that your `ISE_API_KEY` from [IndianAPI](https://indianapi.in/) is set in the `.env` file
   - Verify the API key is valid and not expired

3. **API errors**:
   - Verify your IndianAPI key is valid and has sufficient quota
   - Check if you've subscribed to the Stock Market API on IndianAPI

4. **Connection issues**:
   - Ensure the server is running on the correct host/port
   - Check if port 8000 is available
   - Verify firewall settings

5. **CORS errors**:
   - The server includes CORS headers, but check your client configuration
   - Ensure you're making requests to the correct endpoint

6. **Module not found**:
   - Ensure you've installed the package with `pip install -e .` from the project directory
   - Check if virtual environment is activated
   - Note: PyPI installation (`pip install ise-mcp-server`) is not available yet

7. **Import errors**:
   - Check Python version compatibility (requires Python 3.8+)
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

### Installation Issues

#### Error: `No module named 'ise_mcp'`

```bash
# Solution 1: Install the package
pip install -e .

# Solution 2: Run from correct directory
cd /path/to/Live-NSE-BSE-MCP
python -m ise_mcp.server
```

#### Error: `ModuleNotFoundError: No module named 'mcp'`

```bash
# Install MCP dependency
pip install mcp>=1.0.0

# Or install all requirements
pip install -r requirements.txt
```

### Client Integration Issues

#### Claude Desktop Not Detecting Server

1. Check configuration file location:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Verify JSON syntax is valid
3. Restart Claude Desktop completely
4. Check console logs for error messages

#### VSCode/Cursor Connection Issues

1. Ensure HTTP server is running: `python -m ise_mcp.server`
2. Test server health: `curl http://localhost:8000/health`
3. Check if MCP extension is properly installed
4. Verify environment variables are set

### Error Handling

The server provides detailed error messages in JSON-RPC format:

- `-32600`: Invalid Request
- `-32601`: Method not found  
- `-32602`: Invalid params
- `-32603`: Internal error

### Transport-Specific Issues

#### HTTP Transport

- Check if port 8000 is available: `netstat -an | grep 8000`
- Verify firewall settings
- Test with `curl http://localhost:8000/health`
- Check server logs for error messages

#### Stdio Transport

- Ensure no other output to stdout
- Check that environment variables are set
- Verify MCP client configuration
- Test stdio connection: `echo '{"jsonrpc":"2.0","method":"ping","id":1}' | python -m ise_mcp.stdio_server`

### Development Issues

#### Tests Failing

```bash
# Check if server is running
curl http://localhost:8000/health

# Verify API key is set
echo $ISE_API_KEY

# Run individual tests
python tests/test_connection.py
python tests/test_tools.py
```

#### Debugging Server Issues

1. Enable debug logging in `.env`:

   ```bash
   ISE_LOG_LEVEL=DEBUG
   ```

2. Check server logs for detailed error information
3. Test API endpoints manually with curl
4. Verify IndianAPI service status

## 📚 Related Projects

- **MCP Client**: [client/](./client/) - Python client for testing
- **Examples**: [examples/](./examples/) - Usage examples

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
