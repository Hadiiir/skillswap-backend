#!/bin/bash

echo "⚡ Quick test for all filters"
echo "============================"

BASE_URL="http://localhost:8000/api/skills"

echo ""
echo "📊 Quick summary:"

echo "💻 Programming:"
curl -s "$BASE_URL/?category=1" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo "🎨 Design:"
curl -s "$BASE_URL/?category=2" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo "📢 Marketing:"
curl -s "$BASE_URL/?category=3" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo ""
echo "🌍 Language filters test:"
echo "Arabic:"
curl -s "$BASE_URL/?language=ar" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo "English:"
curl -s "$BASE_URL/?language=en" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo "Both:"
curl -s "$BASE_URL/?language=both" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo ""
echo "📚 Difficulty filters test:"
echo "Beginner:"
curl -s "$BASE_URL/?difficulty=beginner" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo "Intermediate:"
curl -s "$BASE_URL/?difficulty=intermediate" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo "Advanced:"
curl -s "$BASE_URL/?difficulty=advanced" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  {len(results)} skills')
except: print('  Error')
"

echo ""
echo "✅ Quick test completed!"