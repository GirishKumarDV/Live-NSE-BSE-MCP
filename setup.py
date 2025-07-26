#!/usr/bin/env python3
"""
Setup script for Indian Stock Exchange MCP Server
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create environment configuration file"""
    env_content = """# Indian Stock Exchange MCP Server Configuration
# Update with your actual values

# API Configuration
ISE_API_BASE_URL=https://stock.indianapi.in/
ISE_API_KEY=sk-live-C6rewTUHqgJDuFeYOutcieJhvVwAQDxfUiXqvoXv

# Server Configuration
ISE_REQUEST_TIMEOUT=30
ISE_LOG_LEVEL=INFO

# Example configurations for different environments:

# Development
# ISE_LOG_LEVEL=DEBUG
# ISE_REQUEST_TIMEOUT=60

# Production
# ISE_LOG_LEVEL=WARNING
# ISE_REQUEST_TIMEOUT=30
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("📝 Please update .env with your actual API URL and credentials")
    else:
        print("⚠️  .env file already exists")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required dependencies"""
    try:
        import subprocess
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("💡 Try running: pip install -r requirements.txt")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print("\n📋 Next Steps:")
    print("1. Update .env file with your actual API URL")
    print("2. Set your API key if required")
    print("3. Run the demo: python demo.py")
    print("4. Start the server: python ise_mcp_server.py")
    print("\n📚 Documentation:")
    print("- Read README.md for detailed instructions")
    print("- Check demo.py for usage examples")
    print("\n💡 Configuration:")
    print("- API URL: Update ISE_API_BASE_URL in .env")
    print("- API Key: Update ISE_API_KEY in .env (if needed)")
    print("- Timeout: Adjust ISE_REQUEST_TIMEOUT if needed")

def main():
    """Main setup function"""
    print("🇮🇳 Indian Stock Exchange MCP Server Setup")
    print("=" * 50)
    print()
    
    # Check Python version
    check_python_version()
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 