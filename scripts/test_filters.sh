#!/bin/bash

echo "🔍 SkillSwap API Filters Test"
echo "============================="

BASE_URL="http://localhost:8000/api"

echo ""
echo "📋 1. Test All Skills (No Filter):"
curl -s "$BASE_URL/skills/" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'Total Skills: {len(data.get(\"results\", data))}')
    for skill in data.get('results', data)[:3]:
        print(f'- {skill.get(\"title\", \"N/A\")} | Category: {skill.get(\"category\", {}).get(\"name\", \"N/A\")} | Language: {skill.get(\"language\", \"N/A\")}')
except:
    print('Error parsing data')
"

echo ""
echo "🎨 2. Test Filter by Category (Design & Creative):"
curl -s "$BASE_URL/skills/?category=2" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")} | Category: {skill.get(\"category\", {}).get(\"name\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "💻 3. Test Filter by Category (Programming):"
curl -s "$BASE_URL/skills/?category=1" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")} | Category: {skill.get(\"category\", {}).get(\"name\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🌍 4. Test Filter by Language (Arabic):"
curl -s "$BASE_URL/skills/?language=ar" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")} | Language: {skill.get(\"language\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "📚 5. Test Filter by Difficulty (Beginner):"
curl -s "$BASE_URL/skills/?difficulty=beginner" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")} | Difficulty: {skill.get(\"difficulty\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "💰 6. Test Filter by Points (Less than 100):"
curl -s "$BASE_URL/skills/?points_required__lt=100" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")} | Points: {skill.get(\"points_required\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🔍 7. Test Search:"
curl -s "$BASE_URL/skills/?search=django" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "📊 8. Test Multiple Filters:"
curl -s "$BASE_URL/skills/?category=1&difficulty=intermediate&language=both" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total Results: {len(results)}')
    for skill in results:
        print(f'- {skill.get(\"title\", \"N/A\")} | Category: {skill.get(\"category\", {}).get(\"name\", \"N/A\")} | Difficulty: {skill.get(\"difficulty\", \"N/A\")} | Language: {skill.get(\"language\", \"N/A\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "✅ Filters Test Completed!"
