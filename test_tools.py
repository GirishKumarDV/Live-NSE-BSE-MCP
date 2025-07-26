#!/usr/bin/env python3
import requests
import json

try:
    # Test JSON-RPC tools/list
    response = requests.post(
        "http://localhost:8000/jsonrpc",
        json={
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 1
        },
        timeout=5
    )
    
    if response.status_code == 200:
        result = response.json()
        if "result" in result:
            tools = result["result"].get("tools", [])
            print(f"✅ Found {len(tools)} tools:")
            for i, tool in enumerate(tools, 1):
                print(f"  {i}. {tool['name']}")
        else:
            print(f"❌ Error: {result}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")
    print("Make sure the server is running with: python ise_mcp_server.py") 