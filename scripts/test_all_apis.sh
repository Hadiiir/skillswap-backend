#!/bin/bash

echo "🚀 SkillSwap API Testing Suite"
echo "=============================="

# Check if server is running
if ! curl -s http://localhost:8000 > /dev/null; then
    echo "❌ Server is not running. Please start it first:"
    echo "   bash scripts/run_local.sh"
    exit 1
fi

echo "✅ Server is running. Starting API tests..."

# Run the Python API test script
python scripts/test_all_apis.py

echo ""
echo "🔍 Manual API Tests with curl:"
echo "=============================="

# Test basic endpoints
echo ""
echo "1. Testing Skills API:"
curl -s -X GET "http://localhost:8000/api/skills/" | python -m json.tool

echo ""
echo "2. Testing Categories API:"
curl -s -X GET "http://localhost:8000/api/skills/categories/" | python -m json.tool

echo ""
echo "3. Testing Points Packages API:"
curl -s -X GET "http://localhost:8000/api/points/packages/" | python -m json.tool

echo ""
echo "✅ API Testing Complete!"
