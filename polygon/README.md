# Polygon.io HTTP API Server

A FastAPI HTTP server for fetching stock market data from Polygon.io that you can run locally and test with curl.

## Requirements

- Python >=3.13.3 (developed on Python 3.13.3)
- Polygon.io API key

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

- `ticker` (required): Stock ticker symbol (e.g., "AAPL")
- `multiplier` (optional): Size of the timespan multiplier (default: 1)
- `timespan` (optional): Size of the time window (default: "minute")
- `from` (optional): Start date in YYYY-MM-DD format (default: "2023-01-01")
- `to` (optional): End date in YYYY-MM-DD format (default: "2023-06-13")
- `limit` (optional): Maximum number of results to fetch (default: 50000)
- `max_results` (optional): Maximum results to return in response (default: 100)

### Example Usage with curl

```bash
# Basic request for AAPL data
curl "http://localhost:3000/v1/list_aggs?ticker=AAPL"

# Custom date range and timespan
curl "http://localhost:3000/v1/list_aggs?ticker=AAPL&from=2024-01-01&to=2024-01-31&timespan=hour"

# Daily data for Tesla
curl "http://localhost:3000/v1/list_aggs?ticker=TSLA&timespan=day&from=2024-01-01&to=2024-12-31"

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
  "ticker": "AAPL",
  "timespan": "1 minute",
  "from_date": "2023-01-01",
  "to_date": "2023-06-13",
  "count": 50000,
  "aggregates": [
    {
      "timestamp": 1672531800000,
      "open": 130.28,
      "high": 130.90,
      "low": 130.15,
      "close": 130.73,
      "volume": 30000,
      "vwap": 130.52,
      "transactions": 250
    }
  ],
  "note": "Showing first 100 of 50000 total aggregates"
}
```

## Development

This server is currently in development and implements basic aggregate data fetching functionality. Future enhancements may include:

- Additional Polygon.io API endpoints (tickers, trades, quotes, etc.)
- Real-time data streaming
- More advanced filtering and analysis tools
- Authentication and rate limiting
- Caching for improved performance

### Development Mode

The server runs with auto-reload enabled by default, so changes to the code will automatically restart the server.

### Debugging in VS Code

To debug with breakpoints in VS Code:
1. Set breakpoints in `server.py`
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

## Troubleshooting

- Ensure your Polygon.io API key is valid and has the necessary permissions
- Check that all dependencies are installed in your virtual environment
- Verify that you're using Python >=3.13.3
- If you get port conflicts, change the port: `export POLY_MCP_PORT=3001`
- Check the server logs for detailed error messages
