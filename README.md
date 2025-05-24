# DK MCP Servers Collection

A collection of Model Context Protocol (MCP) servers for various data sources and APIs, designed to extend Claude Desktop with specialized functionality.

## About This Repository

This repository contains custom MCP servers that integrate with Claude Desktop to provide access to external APIs and data sources. Each server is designed to be modular, well-documented, and easy to deploy.

## Available MCP Servers

### 🏛️ Polygon.io Stock Market Data Server
**Directory:** `polygon/`

A FastAPI HTTP server with MCP wrapper for fetching real-time and historical stock market data from Polygon.io.

**Features:**
- Fetch aggregate bars (OHLCV data) for any stock ticker
- Support for multiple timeframes (minute, hour, day, week, month, etc.)
- Configurable date ranges and result limits
- FastAPI HTTP server for direct testing with curl
- MCP wrapper for seamless Claude Desktop integration
- Interactive API documentation

**Quick Start:**
```bash
cd polygon
./setup.sh
source venv-poly/bin/activate
export POLYGON_API_KEY="your_polygon_api_key"
python3 server.py  # HTTP server on localhost:3000
```

**Claude Desktop Integration:**
Add to your `claude_desktop_config.json`:
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

## Repository Structure

```
dkmcp/
├── README.md                 # This file
├── polygon/                  # Polygon.io stock data server
│   ├── server.py            # FastAPI HTTP server
│   ├── mcp_wrapper.py       # MCP protocol wrapper
│   ├── requirements.txt     # Python dependencies
│   ├── setup.sh            # Quick setup script
│   ├── test_server.py      # Test utilities
│   └── README.md           # Detailed documentation
└── [future servers...]      # Additional MCP servers
```

## Development Philosophy

Each MCP server in this collection follows these principles:

1. **Dual Interface Design**: HTTP server for direct testing + MCP wrapper for Claude integration
2. **Developer Friendly**: Easy to debug with breakpoints, comprehensive logging, auto-reload
3. **Well Documented**: Clear setup instructions, API documentation, examples
4. **Production Ready**: Proper error handling, validation, environment configuration
5. **Modular**: Each server is self-contained with its own dependencies

## Requirements

- Python >=3.13.3
- Claude Desktop application
- API keys for respective services (Polygon.io, etc.)

## Contributing

When adding new MCP servers:

1. Create a new directory for each server
2. Include both HTTP server and MCP wrapper components
3. Provide comprehensive README.md documentation
4. Include setup scripts and test utilities
5. Follow the established patterns for configuration and error handling

## Getting Started

1. **Clone this repository:**
   ```bash
   git clone https://github.com/gddk/dkmcp.git
   cd dkmcp
   ```

2. **Choose a server to set up** (e.g., polygon)

3. **Follow the server-specific setup instructions** in its README.md

4. **Update your Claude Desktop configuration** to include the new MCP server

5. **Restart Claude Desktop** to load the new functionality

## Troubleshooting

- Ensure all required API keys are set as environment variables
- Check that virtual environments are properly activated
- Verify Claude Desktop configuration syntax
- Review server logs for detailed error messages
- Test HTTP endpoints directly with curl before debugging MCP integration

## License

This project is open source. Individual servers may use APIs that require authentication and have their own terms of service.

---

**Author:** Dave K  
**Repository:** https://github.com/gddk/dkmcp  
**Purpose:** Extending Claude Desktop with specialized data access capabilities
