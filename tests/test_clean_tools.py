#!/usr/bin/env python3
"""
Test cleaned tool serialization
"""

import requests
import json

def test_clean_tools():
    """Test that tools are now properly serialized"""
    print("🔍 Testing Cleaned Tool Serialization")
    print("=" * 45)
    
    try:
        # Test tools/list with cleaned serialization
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
                tools = result["result"]["tools"]
                print(f"Found {len(tools)} tools")
                
                if len(tools) > 0:
                    first_tool = tools[0]
                    print(f"\n📋 First tool structure:")
                    print(json.dumps(first_tool, indent=2))
                    
                    # Check for clean fields
                    expected_fields = {"name", "description", "inputSchema"}
                    actual_fields = set(first_tool.keys())
                    
                    if actual_fields == expected_fields:
                        print(f"\nTool serialization is clean!")
                        print(f"   Fields: {sorted(actual_fields)}")
                    else:
                        extra_fields = actual_fields - expected_fields
                        missing_fields = expected_fields - actual_fields
                        if extra_fields:
                            print(f"\n⚠️  Extra fields: {extra_fields}")
                        if missing_fields:
                            print(f"\nMissing fields: {missing_fields}")
                else:
                    print("No tools found")
            else:
                print(f"Error in response: {result}")
        else:
            print(f"HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure server is running: python ise_mcp_server.py")

if __name__ == "__main__":
    test_clean_tools() 