#!/usr/bin/env python3
"""
Direct MCP server for Polygon.io - no HTTP wrapper
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List

from polygon import RESTClient
from mcp.server.stdio import stdio_server
from mcp import types
from mcp.server import Server

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("polygon-direct")

# Global client instance
polygon_client = None

def initialize_polygon_client():
    """Initialize the Polygon.io client"""
    global polygon_client
    
    # For testing, let's use a dummy client that returns mock data
    # api_key = os.getenv("POLYGON_API_KEY")
    # if not api_key:
    #     raise ValueError("POLYGON_API_KEY environment variable is required")
    # polygon_client = RESTClient(api_key=api_key)
    
    # For now, just set a flag that we're "initialized"
    polygon_client = "initialized"
    logger.info("Polygon client initialized (mock mode)")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    logger.info("list_tools called")
    
    return [
        types.Tool(
            name="list_aggs",
            description="Fetch aggregate bars (OHLCV data) for a stock ticker",
            inputSchema={
                "type": "object", 
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "from_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "to_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                    "timespan": {"type": "string", "description": "Time window", "default": "day"}
                },
                "required": ["ticker"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    logger.info(f"call_tool called: {name} with {arguments}")
    
    if name == "list_aggs":
        # Now make real HTTP request to our polygon server
        params = {
            "ticker": arguments.get("ticker", "AAPL"),
            "from": arguments.get("from_date", "2024-01-01"),
            "to": arguments.get("to_date", "2024-12-31"),
            "timespan": arguments.get("timespan", "day"),
            "multiplier": 1,
            "max_results": 100
        }
        
        try:
            import requests
            logger.info(f"Making HTTP request with params: {params}")
            response = requests.get("http://localhost:3000/v1/list_aggs", params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                result = json.dumps(data, indent=2)
                logger.info(f"HTTP request successful, returning real data")
                return [types.TextContent(type="text", text=result)]
            else:
                error_msg = f"HTTP Error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
                
        except Exception as e:
            error_msg = f"Error calling HTTP server: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main server entry point"""
    try:
        logger.info("Starting direct polygon MCP server")
        initialize_polygon_client()
        
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Direct MCP server initialized")
            # Use proper initialization options instead of empty dict
            from mcp.server import InitializationOptions
            init_options = InitializationOptions(
                server_name="polygon-direct",
                server_version="1.0.0",
                capabilities={}
            )
            await server.run(read_stream, write_stream, init_options)
            
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
