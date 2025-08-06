#!/usr/bin/env python
"""
Script to debug filter issues
Run with: docker-compose exec web python scripts/debug_filters.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_simple')
django.setup()

from skills.models import Category, Skill
from django.db.models import Q

def debug_filters():
    print("🔍 Diagnosing Filter Issues")
    print("=" * 30)
    
    # 1. Check categories
    print("\n📋 Available Categories:")
    categories = Category.objects.all()
    for cat in categories:
        skill_count = Skill.objects.filter(category=cat, status='active').count()
        print(f"- ID: {cat.id} | {cat.name} | Skills Count: {skill_count}")
    
    # 2. Check skills
    print(f"\n📝 Total Active Skills: {Skill.objects.filter(status='active').count()}")
    
    # 3. Check languages
    print("\n🌍 Language Distribution:")
    languages = Skill.objects.filter(status='active').values_list('language', flat=True).distinct()
    for lang in languages:
        count = Skill.objects.filter(status='active', language=lang).count()
        print(f"- {lang}: {count} skill(s)")
    
    # 4. Check difficulty levels
    print("\n📚 Difficulty Level Distribution:")
    difficulties = Skill.objects.filter(status='active').values_list('difficulty', flat=True).distinct()
    for diff in difficulties:
        count = Skill.objects.filter(status='active', difficulty=diff).count()
        print(f"- {diff}: {count} skill(s)")
    
    # 5. Check points
    print("\n💰 Points Distribution:")
    skills = Skill.objects.filter(status='active').values_list('points_required', flat=True)
    if skills:
        print(f"- Minimum: {min(skills)}")
        print(f"- Maximum: {max(skills)}")
        print(f"- Average: {sum(skills) / len(skills):.1f}")
    
    # 6. Test filters
    print("\n🧪 Testing Filters:")
    
    # Category filter
    cat1_skills = Skill.objects.filter(category_id=1, status='active')
    print(f"- Category 1: {cat1_skills.count()} skill(s)")
    
    # Language filter
    ar_skills = Skill.objects.filter(language='ar', status='active')
    both_skills = Skill.objects.filter(language='both', status='active')
    print(f"- Arabic: {ar_skills.count()} skill(s)")
    print(f"- Both languages: {both_skills.count()} skill(s)")
    
    # Difficulty filter
    beginner_skills = Skill.objects.filter(difficulty='beginner', status='active')
    print(f"- Beginner: {beginner_skills.count()} skill(s)")
    
    # 7. Display sample skills
    print("\n📋 Sample Skills:")
    sample_skills = Skill.objects.filter(status='active')[:5]
    for skill in sample_skills:
        print(f"- {skill.title}")
        print(f"  Category: {skill.category.name} (ID: {skill.category.id})")
        print(f"  Language: {skill.language}")
        print(f"  Difficulty: {skill.difficulty}")
        print(f"  Points: {skill.points_required}")
        print()

if __name__ == '__main__':
    debug_filters()
