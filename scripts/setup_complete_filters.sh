#!/bin/bash

echo "🚀 Comprehensive Setup for Skill Filters"
echo "==============================="

# 1. Create diverse skills
echo "📝 Creating diverse skills..."
docker-compose -f docker-compose.simple.yml exec web python manage.py shell < scripts/create_diverse_skills.py

echo ""
echo "⏳ Waiting a bit..."
sleep 5

# 2. Test the filters
echo "🧪 Testing the filters..."
bash scripts/test_category_filters.sh

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🌐 Now you can:"
echo "1. Go to: http://localhost:8000/api/skills/"
echo "2. Select any category from the dropdown list"
echo "3. You will see only the skills related to that category"
echo ""
echo "📊 Available categories:"
echo "- Programming & Development (ID: 1)"
echo "- Design & Creative (ID: 2)" 
echo "- Digital Marketing (ID: 3)" 
