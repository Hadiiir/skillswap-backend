#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')
django.setup()

from skills.models import Category, Skill
from accounts.models import User

def fix_categories():
    """Fix categories and create test data"""
    print("🔧 Fixing categories and creating test data...")
    
    # Create categories if they don't exist
    categories_data = [
        {'name': 'Programming', 'name_ar': 'البرمجة', 'description': 'Software development and programming skills', 'icon': 'fas fa-code'},
        {'name': 'Design', 'name_ar': 'التصميم', 'description': 'Graphic design, UI/UX, and creative skills', 'icon': 'fas fa-paint-brush'},
        {'name': 'Marketing', 'name_ar': 'التسويق', 'description': 'Digital marketing and promotion skills', 'icon': 'fas fa-bullhorn'},
        {'name': 'Writing', 'name_ar': 'الكتابة', 'description': 'Content writing and copywriting skills', 'icon': 'fas fa-pen'},
        {'name': 'Business', 'name_ar': 'الأعمال', 'description': 'Business development and consulting', 'icon': 'fas fa-briefcase'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"📋 Category exists: {category.name}")
    
    # Create a test user if needed
    test_user, created = User.objects.get_or_create(
        email='test@skillswap.com',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print("✅ Created test user")
    
    # Create test skills for each category
    programming_cat = Category.objects.get(name='Programming')
    design_cat = Category.objects.get(name='Design')
    marketing_cat = Category.objects.get(name='Marketing')
    
    test_skills = [
        {
            'title': 'Python Development',
            'description': 'Learn Python programming from basics to advanced',
            'category': programming_cat,
            'points_required': 100,
            'difficulty': 'intermediate',
            'language': 'en'
        },
        {
            'title': 'Logo Design',
            'description': 'Create professional logos for businesses',
            'category': design_cat,
            'points_required': 150,
            'difficulty': 'beginner',
            'language': 'en'
        },
        {
            'title': 'Social Media Marketing',
            'description': 'Grow your social media presence',
            'category': marketing_cat,
            'points_required': 120,
            'difficulty': 'intermediate',
            'language': 'en'
        }
    ]
    
    for skill_data in test_skills:
        skill, created = Skill.objects.get_or_create(
            title=skill_data['title'],
            user=test_user,
            defaults=skill_data
        )
        if created:
            print(f"✅ Created skill: {skill.title}")
        else:
            print(f"📋 Skill exists: {skill.title}")
    
    print("\n📊 Current data:")
    print(f"Categories: {Category.objects.count()}")
    print(f"Skills: {Skill.objects.count()}")
    print(f"Users: {User.objects.count()}")
    
    print("\n🔍 Testing category filters:")
    for category in Category.objects.all():
        skills_count = Skill.objects.filter(category=category).count()
        print(f"Category {category.id} ({category.name}): {skills_count} skills")

if __name__ == '__main__':
    fix_categories()
