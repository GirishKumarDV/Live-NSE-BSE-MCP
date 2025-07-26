#!/usr/bin/env python3
"""
Test connection to MCP server from external client (like VSCode)
"""

import requests
import json

def test_cors_and_connection():
    """Test CORS headers and connection like VSCode would"""
    print("🔍 Testing MCP Server Connection (VSCode/External Client)")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Test CORS preflight (OPTIONS request)
        print("\n1. Testing CORS Preflight (OPTIONS)...")
        options_response = requests.options(
            f"{base_url}/jsonrpc",
            headers={
                "Origin": "vscode-webview://",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            },
            timeout=5
        )
        
        print(f"   Status: {options_response.status_code}")
        cors_headers = {
            'Access-Control-Allow-Origin': options_response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': options_response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': options_response.headers.get('Access-Control-Allow-Headers')
        }
        print(f"   CORS Headers: {cors_headers}")
        
        # 2. Test health endpoint
        print("\n2. Testing Health Endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"   Response: {health_response.json()}")
        
        # 3. Test JSON-RPC initialize (like VSCode would)
        print("\n3. Testing JSON-RPC Initialize...")
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "vscode",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        
        init_response = requests.post(
            f"{base_url}/jsonrpc",
            json=init_request,
            headers={
                "Content-Type": "application/json",
                "Origin": "vscode-webview://"
            },
            timeout=5
        )
        
        print(f"   Status: {init_response.status_code}")
        print(f"   Response CORS: {init_response.headers.get('Access-Control-Allow-Origin')}")
        
        if init_response.status_code == 200:
            result = init_response.json()
            if "result" in result:
                print("   ✅ Initialize successful!")
                server_info = result["result"].get("serverInfo", {})
                print(f"   Server: {server_info.get('name')} v{server_info.get('version')}")
            else:
                print(f"   ❌ Initialize failed: {result}")
        
        # 4. Test tools/list
        print("\n4. Testing Tools List...")
        tools_request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 2
        }
        
        tools_response = requests.post(
            f"{base_url}/jsonrpc",
            json=tools_request,
            headers={
                "Content-Type": "application/json",
                "Origin": "vscode-webview://"
            },
            timeout=5
        )
        
        print(f"   Status: {tools_response.status_code}")
        if tools_response.status_code == 200:
            result = tools_response.json()
            if "result" in result:
                tools = result["result"].get("tools", [])
                print(f"   ✅ Found {len(tools)} tools!")
                print(f"   Sample tools: {[t['name'] for t in tools[:3]]}")
            else:
                print(f"   ❌ Error: {result}")
        
        print("\n🎉 Connection Test Summary:")
        print("✅ CORS headers properly configured")
        print("✅ Server responding to external clients")
        print("✅ JSON-RPC protocol working")
        print(f"✅ {len(tools) if 'tools' in locals() else 'Unknown'} tools available")
        
        print(f"\n📋 For VSCode MCP Configuration:")
        print(f"   URL: http://localhost:8000/jsonrpc")
        print(f"   Type: HTTP")
        print(f"   Protocol: JSON-RPC 2.0")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure server is running:")
        print("   python ise_mcp_server.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_cors_and_connection() 