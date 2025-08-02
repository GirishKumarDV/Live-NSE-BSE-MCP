#!/usr/bin/env python3
"""
Check tool serialization to debug Cursor issue
"""

import json
import asyncio
from mcp.types import Tool

# Replicate the tool creation from the server
def create_test_tool():
    return Tool(
        name="get_stock_data",
        description="Get detailed financial data for a specific company by name",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Company name, shortened name, or search term"
                }
            },
            "required": ["name"]
        }
    )

def test_serialization():
    print("🔍 Testing Tool Serialization")
    print("=" * 40)
    
    tool = create_test_tool()
    
    print("1. Tool object attributes:")
    print(f"   - name: {tool.name}")
    print(f"   - description: {tool.description}")
    print(f"   - inputSchema: {tool.inputSchema}")
    
    print("\n2. model_dump() output:")
    dumped = tool.model_dump()
    print(json.dumps(dumped, indent=2))
    
    print(f"\n3. Keys in dumped tool: {list(dumped.keys())}")
    
    print("\n4. Expected MCP tool format should only have:")
    print("   - name")
    print("   - description") 
    print("   - inputSchema")
    
    # Check for extra fields
    expected_fields = {"name", "description", "inputSchema"}
    actual_fields = set(dumped.keys())
    extra_fields = actual_fields - expected_fields
    
    if extra_fields:
        print(f"\nExtra fields found: {extra_fields}")
        print("   These might be confusing Cursor!")
    else:
        print("\nTool serialization looks correct")

if __name__ == "__main__":
    test_serialization() 