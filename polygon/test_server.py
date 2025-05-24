#!/usr/bin/env python3
"""
Simple test script for the Polygon HTTP API server
"""

import requests
import json
import sys

BASE_URL = "http://localhost:3000"

def test_endpoint(endpoint, description):
    """Test a single endpoint"""
    print(f"\n🧪 Testing {description}")
    print(f"GET {BASE_URL}{endpoint}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(json.dumps(data, indent=2)[:500] + "..." if len(json.dumps(data, indent=2)) > 500 else json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Is the server running on localhost:3000?")
    except requests.exceptions.Timeout:
        print("❌ Timeout - Server took too long to respond")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print("🚀 Polygon HTTP API Server Test")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoint("/", "Root endpoint")
    test_endpoint("/health", "Health check")
    
    # Test the main API endpoint
    test_endpoint("/v1/list_aggs?ticker=AAPL&max_results=3", "List aggregates (limited results)")
    
    print("\n" + "=" * 50)
    print("✨ Test complete!")
    print("\nTo run manual tests:")
    print('curl "http://localhost:3000/health"')
    print('curl "http://localhost:3000/v1/list_aggs?ticker=AAPL&max_results=5"')
    print("\nTo view interactive docs:")
    print("http://localhost:3000/docs")

if __name__ == "__main__":
    main()
