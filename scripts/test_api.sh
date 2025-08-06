#!/bin/bash

echo "🧪 Full Test for SkillSwap API"
echo "=================================="

BASE_URL="http://localhost:8000/api"

echo ""
echo "📋 1. Test Categories List:"
curl -s "$BASE_URL/skills/categories/" | python -m json.tool

echo ""
echo "📦 2. Test Points Packages:"
curl -s "$BASE_URL/points/packages/" | python -m json.tool

echo ""
echo "👤 3. Test Registration:"
curl -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }' | python -m json.tool

echo ""
echo "🔐 4. Test Login:"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ahmed@example.com",
    "password": "testpass123"
  }')

echo "$LOGIN_RESPONSE" | python -m json.tool

# Extract access token
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['tokens']['access'])" 2>/dev/null)

if [ ! -z "$ACCESS_TOKEN" ]; then
    echo ""
    echo "👤 5. Test Profile:"
    curl -s "$BASE_URL/auth/profile/" \
      -H "Authorization: Bearer $ACCESS_TOKEN" | python -m json.tool

    echo ""
    echo "📝 6. Test Creating a New Skill:"
    curl -X POST "$BASE_URL/skills/" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -d '{
        "category": 1,
        "title": "React Development",
        "title_ar": "تطوير React",
        "description": "I will create a modern React application",
        "description_ar": "سأقوم بإنشاء تطبيق React حديث",
        "points_required": 150,
        "estimated_duration": "2 weeks",
        "language": "both",
        "difficulty": "advanced",
        "tags": "react, javascript, frontend"
      }' | python -m json.tool
fi

echo ""
echo "🎯 7. Test Skill Search:"
curl -s "$BASE_URL/skills/?search=django" | python -m json.tool

echo ""
echo "🔍 8. Test Filter by Category:"
curl -s "$BASE_URL/skills/?category=1" | python -m json.tool

echo ""
echo "✅ Full testing completed!"
