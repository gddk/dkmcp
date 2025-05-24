# Polygon.io HTTP API Server with MCP Integration

A FastAPI HTTP server with MCP wrapper for fetching real-time and historical stock market data from Polygon.io that you can run locally and test with curl, plus seamless integration with Claude Desktop.

This server provides a wrapper interface for the [Polygon.io REST API](https://polygon.io/docs/rest/) using the official [Polygon.io Python client](https://github.com/polygon-io/client-python), making stock market data easily accessible through both HTTP endpoints and Claude Desktop's MCP protocol.

## Requirements

- Python >=3.13.3 (developed on Python 3.13.3)
- Polygon.io API key

## Architecture

This server uses a **dual-interface design**:

1. **HTTP Server** (`server.py`) - FastAPI server on localhost:3000 for direct testing with curl
2. **MCP Wrapper** (`mcp_wrapper.py`) - Model Context Protocol wrapper that bridges to the HTTP server for Claude Desktop integration

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv-poly
   source venv-poly/bin/activate  # On macOS/Linux
   # or
   venv-poly\Scripts\activate     # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   export POLYGON_API_KEY="your_polygon_api_key_here"
   
   # Optional: Configure host/port (defaults to localhost:3000)
   export POLY_MCP_HOST="localhost"
   export POLY_MCP_PORT="3000"
   ```

## Getting a Polygon.io API Key

1. Sign up at [polygon.io](https://polygon.io/)
2. Go to your dashboard and copy your API key
3. Set it as an environment variable: `export POLYGON_API_KEY="your_key_here"`

## Usage

### Running the HTTP Server

```bash
python3 server.py
```

The server will start on `http://localhost:3000` by default. You'll see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Polygon.io client initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:3000 (Press CTRL+C to quit)
```

### Available Endpoints

- **GET /**: Root endpoint with service info
- **GET /health**: Health check endpoint
- **GET /v1/list_aggs**: Fetch aggregate bars (OHLCV data) for a stock ticker

### API Parameters for /v1/list_aggs

- `ticker` (required): Stock ticker symbol (e.g., "GDDY")
- `multiplier` (optional): Size of the timespan multiplier (default: 1)
- `timespan` (optional): Size of the time window (default: "minute")
- `from` (optional): Start date in YYYY-MM-DD format (default: "2023-01-01")
- `to` (optional): End date in YYYY-MM-DD format (default: "2023-06-13")
- `limit` (optional): Maximum number of results to fetch (default: 50000)
- `max_results` (optional): Maximum results to return in response (default: 100)

### Example Usage with curl

```bash
# Basic request for GDDY data
curl "http://localhost:3000/v1/list_aggs?ticker=GDDY"

# Custom date range and daily timespan for GoDaddy
curl "http://localhost:3000/v1/list_aggs?ticker=GDDY&from=2025-05-21&to=2025-05-23&timespan=day"

# Hourly data for GoDaddy over recent period
curl "http://localhost:3000/v1/list_aggs?ticker=GDDY&from=2025-05-21&to=2025-05-23&timespan=hour"

# Health check
curl "http://localhost:3000/health"

# Service info
curl "http://localhost:3000/"
```

### Interactive API Documentation

Once the server is running, you can view interactive API documentation at:
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

### Example Response

The `list_aggs` endpoint returns JSON like this:
```json
{
  "ticker": "GDDY",
  "timespan": "1 day",
  "from_date": "2025-05-21",
  "to_date": "2025-05-23",
  "count": 3,
  "aggregates": [
    {
      "timestamp": 1747800000000,
      "open": 186.74,
      "high": 187.41,
      "low": 182.26,
      "close": 183.49,
      "volume": 1539700,
      "vwap": 183.6263,
      "transactions": 33018
    }
  ]
}
```

## Claude Desktop Integration

### Setup

1. **Ensure both servers are running:**
   ```bash
   # Terminal 1: HTTP Server
   cd /Users/dave/mcp/polygon
   source venv-poly/bin/activate
   export POLYGON_API_KEY="your_key"
   python3 server.py
   ```

2. **Add to your `claude_desktop_config.json`:**
   ```json
   {
     "mcpServers": {
       "polygon": {
         "command": "/Users/dave/mcp/polygon/venv-poly/bin/python",
         "args": ["/Users/dave/mcp/polygon/mcp_wrapper.py"],
         "cwd": "/Users/dave/mcp/polygon"
       }
     }
   }
   ```

3. **Restart Claude Desktop** to load the MCP server

### Using with Claude Desktop

Once configured, you can ask Claude to fetch stock data like:

- "Get me daily data for GoDaddy (GDDY) from May 21 to May 23, 2025"
- "Show me hourly price data for GDDY over the past few days"
- "Fetch the latest trading data for GoDaddy stock"

Claude will use the `list_aggs` tool to fetch real-time data from Polygon.io via your local server.

## Development

This server implements basic aggregate data fetching functionality. Future enhancements may include:

- Additional Polygon.io API endpoints (tickers, trades, quotes, etc.)
- Real-time data streaming
- More advanced filtering and analysis tools
- Authentication and rate limiting
- Caching for improved performance

### Development Mode

The HTTP server runs with auto-reload enabled by default, so changes to the code will automatically restart the server.

### Debugging in VS Code

To debug with breakpoints in VS Code:
1. Set breakpoints in `server.py` or `mcp_wrapper.py`
2. Create a launch configuration in `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Polygon Server",
            "type": "python",
            "request": "launch",
            "program": "server.py",
            "console": "integratedTerminal",
            "env": {
                "POLYGON_API_KEY": "your_api_key_here"
            }
        }
    ]
}
```
3. Press F5 to start debugging

### Testing

Use the included test script to verify everything works:
```bash
python3 test_server.py
```

## File Structure

```
polygon/
├── server.py              # FastAPI HTTP server
├── mcp_wrapper.py         # MCP wrapper for Claude Desktop
├── requirements.txt       # Python dependencies
├── setup.sh              # Quick setup script
├── test_server.py        # Test utilities
├── README.md             # This file
└── .gitignore           # Git ignore patterns
```

## Troubleshooting

- Ensure your Polygon.io API key is valid and has the necessary permissions
- Check that all dependencies are installed in your virtual environment
- Verify that you're using Python >=3.13.3
- If you get port conflicts, change the port: `export POLY_MCP_PORT=3001`
- Check the server logs for detailed error messages
- For Claude Desktop issues, check MCP logs in `~/Library/Logs/Claude/mcp-server-polygon.log`

## Architecture Benefits

The dual-interface design provides:

1. **Direct HTTP Testing** - Test with curl, Postman, or any HTTP client
2. **Claude Desktop Integration** - Seamless access through MCP protocol
3. **Development Flexibility** - Debug HTTP server independently
4. **Production Ready** - Proper error handling, logging, and documentation
5. **Extensible** - Easy to add new Polygon.io endpoints

This pattern can be replicated for other API integrations requiring both direct access and Claude Desktop integration.
