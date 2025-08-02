#!/usr/bin/env python3
"""
Test VSCode-style connection to debug fetch failed issue
"""

import asyncio
import aiohttp
import json

async def test_vscode_style_connection():
    """Test connection exactly like VSCode would"""
    print("🔍 Testing VSCode-Style Connection")
    print("=" * 45)
    
    url = "http://localhost:8000/jsonrpc"
    
    # Create session with VSCode-like settings
    timeout = aiohttp.ClientTimeout(total=10, connect=5)
    connector = aiohttp.TCPConnector(
        keepalive_timeout=30,
        enable_cleanup_closed=True,
        limit=10,
        limit_per_host=5
    )
    
    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers={
            "User-Agent": "vscode/1.85.0"
        }
    ) as session:
        
        try:
            # Test 1: Basic connectivity
            print("\n1. Testing basic connectivity...")
            async with session.get("http://localhost:8000/health") as response:
                print(f"   Health Status: {response.status}")
                text = await response.text()
                print(f"   Health Response: {text[:100]}...")
            
            # Test 2: OPTIONS preflight (like browsers do)
            print("\n2. Testing CORS preflight...")
            async with session.options(
                url,
                headers={
                    "Origin": "vscode-webview://",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type"
                }
            ) as response:
                print(f"   OPTIONS Status: {response.status}")
                print(f"   CORS Headers: {dict(response.headers)}")
            
            # Test 3: Initialize request (exactly like VSCode)
            print("\n3. Testing initialize request...")
            init_payload = {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "vscode",
                        "version": "1.85.0"
                    }
                },
                "id": 1
            }
            
            async with session.post(
                url,
                json=init_payload,
                headers={
                    "Content-Type": "application/json",
                    "Origin": "vscode-webview://",
                }
            ) as response:
                print(f"   Initialize Status: {response.status}")
                print(f"   Response Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"   Initialize Success!")
                    print(f"   Server: {result.get('result', {}).get('serverInfo', {})}")
                else:
                    text = await response.text()
                    print(f"   Initialize Failed: {text}")
            
            # Test 4: Tools list
            print("\n4. Testing tools/list...")
            tools_payload = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 2
            }
            
            async with session.post(
                url,
                json=tools_payload,
                headers={
                    "Content-Type": "application/json",
                    "Origin": "vscode-webview://",
                }
            ) as response:
                print(f"   Tools Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    tools = result.get('result', {}).get('tools', [])
                    print(f"   Found {len(tools)} tools!")
                    if tools:
                        print(f"   First tool: {tools[0].get('name')}")
                else:
                    text = await response.text()
                    print(f"   Tools Failed: {text}")
            
            print(f"\n🎉 VSCode-style connection test completed!")
            
        except aiohttp.ClientConnectorError as e:
            print(f"Connection Error: {e}")
            print("   This matches the 'fetch failed' error VSCode is seeing")
        except asyncio.TimeoutError:
            print(f"Timeout Error")
            print("   Server might be too slow to respond")
        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_vscode_style_connection()) 