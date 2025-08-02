#!/usr/bin/env python3
"""
Basic Usage Examples for Indian Stock Exchange MCP Client
"""

import asyncio
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.simple_mcp_client import ISEMCPClient, SimpleMCPClient

async def basic_example():
    """Basic usage example"""
    print("📈 Basic ISE MCP Client Usage")
    print("=" * 35)
    
    # Create client
    client = ISEMCPClient()
    
    try:
        # Connect
        await client.connect()
        
        # Get trending stocks
        print("\n🔥 Trending Stocks:")
        trending = await client.get_trending_stocks()
        if trending:
            data = json.loads(trending)
            gainers = data["trending_stocks"]["top_gainers"][:3]
            losers = data["trending_stocks"]["top_losers"][:3]
            
            print("   Top Gainers:")
            for stock in gainers:
                print(f"     • {stock['company_name']}: {stock['percent_change']}%")
            
            print("   Top Losers:")
            for stock in losers:
                print(f"     • {stock['company_name']}: {stock['percent_change']}%")
        
        # Get specific stock data
        print("\nStock Data for Reliance:")
        stock_data = await client.get_stock_data("Reliance")
        if stock_data:
            # Parse and display key info (simplified)
            print("     Stock data retrieved successfully")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

async def market_overview_example():
    """Market overview example"""
    print("🏛️ Market Overview Example")
    print("=" * 30)
    
    client = ISEMCPClient()
    
    try:
        await client.connect()
        
        # Get NSE most active
        print("\n📈 NSE Most Active Stocks:")
        nse_active = await client.get_nse_most_active()
        if nse_active:
            data = json.loads(nse_active)
            for i, stock in enumerate(data[:5], 1):
                print(f"   {i}. {stock['company']} - ₹{stock['price']} ({stock['percent_change']}%)")
        
        # Get BSE most active
        print("\n📈 BSE Most Active Stocks:")
        bse_active = await client.get_bse_most_active()
        if bse_active:
            data = json.loads(bse_active)
            for i, stock in enumerate(data[:5], 1):
                print(f"   {i}. {stock['company']} - ₹{stock['price']} ({stock['percent_change']}%)")
        
        # Get 52-week highs/lows
        print("\n🏔️ 52-Week High/Low Data:")
        high_low = await client.get_52_week_high_low()
        if high_low:
            print("     52-week data retrieved")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

async def industry_analysis_example():
    """Industry analysis example"""
    print("🏭 Industry Analysis Example")
    print("=" * 32)
    
    client = ISEMCPClient()
    
    try:
        await client.connect()
        
        # Search banking industry
        print("\n🏦 Banking Industry Companies:")
        banking = await client.search_industry("Banking")
        if banking:
            data = json.loads(banking)
            for i, company in enumerate(data[:5], 1):
                print(f"   {i}. {company['commonName']} - {company['mgSector']}")
        
        # Search IT industry
        print("\n💻 IT Industry Companies:")
        it = await client.search_industry("Software")
        if it:
            data = json.loads(it)
            for i, company in enumerate(data[:5], 1):
                print(f"   {i}. {company['commonName']} - {company['mgIndustry']}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

async def mutual_funds_example():
    """Mutual funds example"""
    print("💰 Mutual Funds Example")
    print("=" * 25)
    
    client = ISEMCPClient()
    
    try:
        await client.connect()
        
        # Search equity mutual funds
        print("\nEquity Mutual Funds:")
        equity_funds = await client.search_mutual_funds("equity")
        if equity_funds:
            data = json.loads(equity_funds)
            for i, fund in enumerate(data[:5], 1):
                print(f"   {i}. {fund['schemeName']}")
        
        # Get latest mutual fund data
        print("\n📈 Latest Mutual Fund Data:")
        latest_funds = await client.get_mutual_funds()
        if latest_funds:
            print("     Latest mutual fund data retrieved")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

async def historical_analysis_example():
    """Historical analysis example"""
    print("Historical Analysis Example")
    print("=" * 35)
    
    client = ISEMCPClient()
    
    try:
        await client.connect()
        
        # Get historical data for TCS
        print("\nTCS Historical Data (1 Year):")
        tcs_history = await client.get_historical_data("TCS", "1yr", "price")
        if tcs_history:
            print("     Historical price data retrieved")
        
        # Get quarterly results for TCS
        print("\n📈 TCS Quarterly Results:")
        tcs_quarters = await client.get_historical_stats("TCS", "quarter_results")
        if tcs_quarters:
            data = json.loads(tcs_quarters)
            if "Sales" in data:
                sales = data["Sales"]
                recent_quarters = list(sales.keys())[-4:]
                print("     Recent Quarterly Sales:")
                for quarter in recent_quarters:
                    print(f"       {quarter}: ₹{sales[quarter]} Cr")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

async def generic_client_example():
    """Example using the generic SimpleMCPClient"""
    print("🔧 Generic MCP Client Example")
    print("=" * 33)
    
    # Use generic client instead of specialized one
    client = SimpleMCPClient("http://localhost:8000/jsonrpc")
    
    try:
        await client.connect()
        
        # List all available tools
        tools = await client.list_tools()
        print(f"\n🛠️ Available Tools ({len(tools)}):")
        for i, tool in enumerate(tools, 1):
            print(f"   {i:2d}. {tool.name}")
            print(f"       {tool.description}")
        
        # Call a tool manually
        print(f"\n🔧 Manual Tool Call:")
        result = await client.call_tool("get_trending_stocks")
        if result:
            print("     Tool call successful")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await client.close()

async def main():
    """Run all examples"""
    examples = [
        ("Basic Usage", basic_example),
        ("Market Overview", market_overview_example), 
        ("Industry Analysis", industry_analysis_example),
        ("Mutual Funds", mutual_funds_example),
        ("Historical Analysis", historical_analysis_example),
        ("Generic Client", generic_client_example)
    ]
    
    print("🇮🇳 Indian Stock Exchange MCP Client Examples")
    print("=" * 50)
    print("Choose an example to run:")
    print()
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print(f"{len(examples) + 1}. Run All Examples")
    print()
    
    try:
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == str(len(examples) + 1):
            # Run all examples
            for name, func in examples:
                print(f"\n" + "="*60)
                print(f"Running: {name}")
                print("="*60)
                await func()
                print()
                await asyncio.sleep(1)  # Small delay between examples
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            # Run selected example
            name, func = examples[int(choice) - 1]
            print(f"\n" + "="*60)
            print(f"Running: {name}")
            print("="*60)
            await func()
        else:
            print("Invalid choice!")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 