#!/bin/bash

echo "🔍 SkillSwap API Filters Test"
echo "============================="

BASE_URL="http://localhost:8000/api"

echo ""
echo "📋 1. All Skills:"
curl -s "$BASE_URL/skills/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total skills: {len(results)}')
    if len(results) > 0:
        print('First 3 skills:')
        for skill in results[:3]:
            cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
            print(f'  - {skill.get(\"title\", \"Untitled\")} | Category: {cat_name} | Language: {skill.get(\"language\", \"Unknown\")} | Difficulty: {skill.get(\"difficulty\", \"Unknown\")}')
    else:
        print('❌ No skills found!')
except Exception as e:
    print(f'Error: {e}')
    print('Raw response:')
    print(sys.stdin.read())
"

echo ""
echo "📂 2. Available Categories:"
curl -s "$BASE_URL/skills/categories/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    categories = data if isinstance(data, list) else data.get('results', [])
    print(f'Total categories: {len(categories)}')
    for cat in categories:
        print(f'  - ID: {cat.get(\"id\")} | {cat.get(\"name\", \"Unnamed\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🎨 3. Filter by Category 1:"
curl -s "$BASE_URL/skills/?category=1" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Results for Category 1: {len(results)}')
    for skill in results:
        cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
        print(f'  - {skill.get(\"title\", \"Untitled\")} | Category: {cat_name}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🎨 4. Filter by Category 2:"
curl -s "$BASE_URL/skills/?category=2" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Results for Category 2: {len(results)}')
    for skill in results:
        cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
        print(f'  - {skill.get(\"title\", \"Untitled\")} | Category: {cat_name}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🌍 5. Filter by Language (both):"
curl -s "$BASE_URL/skills/?language=both" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Results for language 'both': {len(results)}')
    for skill in results:
        print(f'  - {skill.get(\"title\", \"Untitled\")} | Language: {skill.get(\"language\", \"Unknown\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "📚 6. Filter by Difficulty (beginner):"
curl -s "$BASE_URL/skills/?difficulty=beginner" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Results for difficulty 'beginner': {len(results)}')
    for skill in results:
        print(f'  - {skill.get(\"title\", \"Untitled\")} | Difficulty: {skill.get(\"difficulty\", \"Unknown\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🔍 7. Search for django:"
curl -s "$BASE_URL/skills/?search=django" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Search results for django: {len(results)}')
    for skill in results:
        print(f'  - {skill.get(\"title\", \"Untitled\")}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "✅ Test completed!"
