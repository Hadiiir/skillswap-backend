#!/bin/bash

echo "🔄 Restarting and Fixing Filters"
echo "==============================="

# 1. Restart Services
echo "🛑 Stopping services..."
docker-compose -f docker-compose.simple.yml down

echo "🚀 Restarting services..."
docker-compose -f docker-compose.simple.yml up -d

echo "⏳ Waiting for services to start..."
sleep 20

# 2. Fix Data
echo "🔧 Fixing data..."
docker-compose -f docker-compose.simple.yml exec web python manage.py shell < scripts/fix_browsable_api.py

# 3. Test Filters
echo "🧪 Testing filters..."
echo ""
echo "📋 All Skills:"
curl -s "http://localhost:8000/api/skills/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Total skills: {len(results)}')
except: pass
"

echo ""
echo "🎨 Category Filter (Programming):"
curl -s "http://localhost:8000/api/skills/?category=1" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Result count: {len(results)}')
except: pass
"

echo ""
echo "🌍 Language Filter (English):"
curl -s "http://localhost:8000/api/skills/?language=en" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Result count: {len(results)}')
except: pass
"

echo ""
echo "📚 Difficulty Filter (Advanced):"
curl -s "http://localhost:8000/api/skills/?difficulty=advanced" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Result count: {len(results)}')
except: pass
"

echo ""
echo "💰 Points Filter (More than 100):"
curl -s "http://localhost:8000/api/skills/?points_required__gte=100" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Result count: {len(results)}')
except: pass
"

echo ""
echo "🔍 Search (React):"
curl -s "http://localhost:8000/api/skills/?search=React" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Result count: {len(results)}')
except: pass
"

echo ""
echo "📊 Ordering (By Points Ascending):"
curl -s "http://localhost:8000/api/skills/?ordering=points_required" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data)
    print(f'Result count: {len(results)}')
    if results:
        points = [skill.get('points_required', 0) for skill in results[:3]]
        print(f'First 3 points: {points}')
except: pass
"

echo ""
echo "✅ Test finished!"
echo "🌐 Go to: http://localhost:8000/api/skills/ to test the browsable interface"
