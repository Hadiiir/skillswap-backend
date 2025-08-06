#!/bin/bash

echo "🎯 Detailed Test for Category Filters"
echo "================================="

BASE_URL="http://localhost:8000/api/skills"

echo ""
echo "📂 1. Display All Available Categories:"
curl -s "$BASE_URL/categories/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    categories = data if isinstance(data, list) else data.get('results', [])
    print(f'Total categories: {len(categories)}')
    for cat in categories:
        print(f'  - ID: {cat[\"id\"]} | {cat[\"name\"]}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "📋 2. All Skills (No Filter):"
curl -s "$BASE_URL/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Total skills: {len(results)}')
    
    # Group by category
    categories = {}
    for skill in results:
        cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
        if cat_name not in categories:
            categories[cat_name] = 0
        categories[cat_name] += 1
    
    print('Skill distribution by category:')
    for cat, count in categories.items():
        print(f'  - {cat}: {count} skills')
        
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "💻 3. Filter: Programming & Development:"
curl -s "$BASE_URL/?category=1" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Programming skills count: {len(results)}')
    
    if len(results) > 0:
        print('Skills:')
        for skill in results:
            cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
            print(f'  - {skill.get(\"title\", \"Untitled\")} | {skill.get(\"points_required\", 0)} pts | {skill.get(\"difficulty\", \"Unknown\")}')
    else:
        print('❌ No skills found in this category!')
        
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🎨 4. Filter: Design & Creative:"
curl -s "$BASE_URL/?category=2" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Design skills count: {len(results)}')
    
    if len(results) > 0:
        print('Skills:')
        for skill in results:
            cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
            print(f'  - {skill.get(\"title\", \"Untitled\")} | {skill.get(\"points_required\", 0)} pts | {skill.get(\"difficulty\", \"Unknown\")}')
    else:
        print('❌ No skills found in this category!')
        
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "📢 5. Filter: Digital Marketing:"
curl -s "$BASE_URL/?category=3" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'Marketing skills count: {len(results)}')
    
    if len(results) > 0:
        print('Skills:')
        for skill in results:
            cat_name = skill.get('category', {}).get('name', 'Uncategorized') if skill.get('category') else 'Uncategorized'
            print(f'  - {skill.get(\"title\", \"Untitled\")} | {skill.get(\"points_required\", 0)} pts | {skill.get(\"difficulty\", \"Unknown\")}')
    else:
        print('❌ No skills found in this category!')
        
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🔍 6. Multiple Filters Test:"
echo "   - Programming + Advanced:"
curl -s "$BASE_URL/?category=1&difficulty=advanced" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'     Result count: {len(results)}')
except: pass
"

echo "   - Design + Beginner:"
curl -s "$BASE_URL/?category=2&difficulty=beginner" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'     Result count: {len(results)}')
except: pass
"

echo "   - Marketing + less than 100 points:"
curl -s "$BASE_URL/?category=3&points_required__lt=100" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'     Result count: {len(results)}')
except: pass
"

echo ""
echo "✅ Filters test completed!"
echo "🌐 Visit: http://localhost:8000/api/skills/ to try the interactive interface"
