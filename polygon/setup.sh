#!/bin/bash

# Setup script for Polygon MCP Server

echo "Setting up Polygon MCP Server..."

# Check if Python 3.13+ is available
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
echo "Found Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv-poly

# Activate virtual environment
echo "Activating virtual environment..."
source venv-poly/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv-poly/bin/activate"
echo "2. Set your Polygon API key: export POLYGON_API_KEY='your_key_here'"
echo "3. Run the server: python3 server.py"
echo ""
echo "Don't forget to add your Polygon.io API key to your environment variables!"
