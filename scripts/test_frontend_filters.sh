#!/bin/bash

echo "🌐 Testing Filters with Frontend"
echo "==============================="

# Create HTML test file
echo "📝 Creating test page..."

# Start simple server to test HTML
echo "🚀 Starting test server on port 3000..."
echo "Open your browser at: http://localhost:3000/test_frontend.html"

# Check for Python
if command -v python3 &> /dev/null; then
    echo "Using Python 3..."
    cd "$(dirname "$0")/.." && python3 -m http.server 3000
elif command -v python &> /dev/null; then
    echo "Using Python 2..."
    cd "$(dirname "$0")/.." && python -m SimpleHTTPServer 3000
else
    echo "❌ Python is not installed. Please open test_frontend.html directly in your browser"
fi
