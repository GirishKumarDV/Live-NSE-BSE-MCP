#!/usr/bin/env python3
"""
Setup script for Indian Stock Exchange MCP Server
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="ise-mcp-server",
    version="1.0.0",
    author="Girish Kumar D V",
    author_email="girishdivate@gkdv.dev",
    description="Indian Stock Exchange MCP Server - Access live market data from BSE & NSE through Model Context Protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "testing": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.25.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ise-mcp-server=ise_mcp.server:cli_main",
            "ise-mcp-stdio=ise_mcp.stdio_server:main",
        ],
    },
    keywords="indian stock exchange mcp model context protocol bse nse financial market data api",
    project_urls={
        "Bug Reports": "https://github.com/GirishKumarDV/Live-NSE-BSE-MCP/issues",
        "Source": "https://github.com/GirishKumarDV/Live-NSE-BSE-MCP.git",
        "Documentation": "https://github.com/GirishKumarDV/Live-NSE-BSE-MCP#readme",
        "API Documentation": "https://indianapi.in/",
    },
    include_package_data=True,
    zip_safe=False,
) 