#!/bin/bash

echo "🧪 Testing SkillSwap Basic APIs..."

# Test API endpoints
echo "Testing API endpoints..."

echo "1. Testing root endpoint:"
curl -s http://localhost:8000/ | python -m json.tool

echo -e "\n2. Testing skills endpoint:"
curl -s http://localhost:8000/api/skills/ | python -m json.tool

echo -e "\n3. Testing categories:"
curl -s http://localhost:8000/api/skills/categories/ | python -m json.tool

echo -e "\n4. Testing points packages:"
curl -s http://localhost:8000/api/points/packages/ | python -m json.tool

echo -e "\n✅ Basic API tests completed!"
