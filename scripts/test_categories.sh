#!/bin/bash

echo "🧪 Testing SkillSwap Categories and Filters"
echo "=========================================="

# Fix categories first
echo "🔧 Fixing categories..."
python scripts/fix_categories.py

echo ""
echo "🌐 Testing API endpoints..."

# Test categories endpoint
echo "📋 Testing categories endpoint:"
curl -s "http://localhost:8000/api/categories/" | python -m json.tool

echo ""
echo "🔍 Testing skills with category filter:"

# Test skills with category 1
echo "Category 1 (Programming):"
curl -s "http://localhost:8000/api/skills/?category=1" | python -m json.tool

echo ""
echo "Category 2 (Design):"
curl -s "http://localhost:8000/api/skills/?category=2" | python -m json.tool

echo ""
echo "Category 3 (Marketing):"
curl -s "http://localhost:8000/api/skills/?category=3" | python -m json.tool

echo ""
echo "✅ Test completed!"
