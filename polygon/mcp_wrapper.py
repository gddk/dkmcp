#!/usr/bin/env python3
"""
MCP wrapper for Polygon HTTP server
Translates MCP protocol calls to HTTP requests to localhost:3000
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP Server instance
server = Server("polygon-mcp-wrapper")

# HTTP server configuration
HTTP_BASE_URL = "http://localhost:3000"

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="list_aggs",
            description="Fetch aggregate bars (OHLCV data) for a stock ticker via Polygon HTTP server",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL)"
                    },
                    "multiplier": {
                        "type": "integer",
                        "description": "Size of the timespan multiplier",
                        "default": 1
                    },
                    "timespan": {
                        "type": "string",
                        "description": "Size of the time window (minute, hour, day, week, month, quarter, year)",
                        "default": "day"
                    },
                    "from_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)",
                        "default": "2024-01-01"
                    },
                    "to_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)",
                        "default": "2024-12-31"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results to return",
                        "default": 100
                    }
                },
                "required": ["ticker"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls by making HTTP requests to the polygon server"""
    if name == "list_aggs":
        return await handle_list_aggs(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_list_aggs(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle list_aggs by calling the HTTP server"""
    try:
        # Build query parameters
        params = {
            "ticker": arguments["ticker"],
            "multiplier": arguments.get("multiplier", 1),
            "timespan": arguments.get("timespan", "day"),
            "from": arguments.get("from_date", "2024-01-01"),
            "to": arguments.get("to_date", "2024-12-31"),
            "max_results": arguments.get("max_results", 100)
        }
        
        # Make HTTP request to the polygon server
        logger.info(f"Making request to {HTTP_BASE_URL}/v1/list_aggs with params: {params}")
        
        response = requests.get(f"{HTTP_BASE_URL}/v1/list_aggs", params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]
        else:
            error_msg = f"HTTP Error {response.status_code}: {response.text}"
            logger.error(error_msg)
            return [TextContent(
                type="text",
                text=f"Error fetching data: {error_msg}"
            )]
            
    except requests.exceptions.ConnectionError:
        error_msg = "Could not connect to Polygon HTTP server at localhost:3000. Is it running?"
        logger.error(error_msg)
        return [TextContent(
            type="text",
            text=error_msg
        )]
    except Exception as e:
        error_msg = f"Error calling Polygon HTTP server: {str(e)}"
        logger.error(error_msg)
        return [TextContent(
            type="text",
            text=error_msg
        )]

async def main():
    """Main MCP server entry point"""
    logger.info("Starting Polygon MCP wrapper (stdio)")
    async with stdio_server() as streams:
        await server.run(*streams)

if __name__ == "__main__":
    asyncio.run(main())
