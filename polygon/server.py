#!/usr/bin/env python3
"""
Polygon.io HTTP API Server
A FastAPI HTTP server for fetching stock market data from Polygon.io
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from polygon import RESTClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app instance
app = FastAPI(
    title="Polygon.io API Server",
    description="HTTP API server for fetching stock market data from Polygon.io",
    version="1.0.0"
)

# Global client instance
polygon_client: Optional[RESTClient] = None


class AggregateData(BaseModel):
    """Model for aggregate data response"""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: int
    vwap: Optional[float] = None
    transactions: Optional[int] = None


class ListAggsResponse(BaseModel):
    """Model for list_aggs API response"""
    ticker: str
    timespan: str
    from_date: str
    to_date: str
    count: int
    aggregates: List[AggregateData]
    note: Optional[str] = None


def initialize_polygon_client():
    """Initialize the Polygon.io client with API key from environment"""
    global polygon_client
    
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        raise ValueError("POLYGON_API_KEY environment variable is required")
    
    polygon_client = RESTClient(api_key=api_key)
    logger.info("Polygon.io client initialized")


@app.on_event("startup")
async def startup_event():
    """Initialize the polygon client on startup"""
    try:
        initialize_polygon_client()
        logger.info("Server startup complete")
    except Exception as e:
        logger.error(f"Failed to initialize: {str(e)}")
        raise


@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "service": "Polygon.io API Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "list_aggs": "/v1/list_aggs",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "polygon_client_initialized": polygon_client is not None
    }


@app.get("/v1/list_aggs", response_model=ListAggsResponse)
async def list_aggs(
    ticker: str = Query(..., description="Stock ticker symbol (e.g., AAPL)"),
    multiplier: int = Query(1, description="Size of the timespan multiplier"),
    timespan: str = Query("minute", description="Size of the time window (minute, hour, day, week, month, quarter, year)"),
    from_date: str = Query("2023-01-01", alias="from", description="Start date (YYYY-MM-DD)"),
    to_date: str = Query("2023-06-13", alias="to", description="End date (YYYY-MM-DD)"),
    limit: int = Query(50000, description="Maximum number of results"),
    max_results: int = Query(100, description="Maximum results to return in response (for display purposes)")
):
    """
    Fetch aggregate bars (OHLCV data) for a stock ticker
    
    This endpoint fetches minute-by-minute (or other timespan) stock data including:
    - Open, High, Low, Close prices
    - Volume
    - VWAP (Volume Weighted Average Price) when available
    - Transaction count when available
    """
    if not polygon_client:
        raise HTTPException(
            status_code=503, 
            detail="Polygon client not initialized. Please ensure POLYGON_API_KEY is set."
        )
    
    try:
        logger.info(f"Fetching aggregates for {ticker} from {from_date} to {to_date}")
        
        # Fetch aggregates using the polygon client
        aggs = []
        for a in polygon_client.list_aggs(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_=from_date,
            to=to_date,
            limit=limit
        ):
            # Convert the aggregate object to our model
            agg_data = AggregateData(
                timestamp=a.timestamp,
                open=a.open,
                high=a.high,
                low=a.low,
                close=a.close,
                volume=a.volume,
                vwap=getattr(a, 'vwap', None),
                transactions=getattr(a, 'transactions', None)
            )
            aggs.append(agg_data)
        
        # Limit results for response (but log total count)
        display_aggs = aggs[:max_results]
        note = None
        if len(aggs) > max_results:
            note = f"Showing first {max_results} of {len(aggs)} total aggregates"
        
        logger.info(f"Successfully fetched {len(aggs)} aggregates for {ticker}")
        
        return ListAggsResponse(
            ticker=ticker,
            timespan=f"{multiplier} {timespan}",
            from_date=from_date,
            to_date=to_date,
            count=len(aggs),
            aggregates=display_aggs,
            note=note
        )
        
    except Exception as e:
        logger.error(f"Error fetching aggregates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching aggregates: {str(e)}")


if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.getenv("POLY_MCP_HOST", "localhost")
    port = int(os.getenv("POLY_MCP_PORT", "3000"))
    
    logger.info(f"Starting Polygon HTTP API Server on {host}:{port}")
    
    # Run the server
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        log_level="info",
        reload=True  # Enable auto-reload for development
    )
