#!/usr/bin/env python
"""
Script to create sample data for testing
Run with: docker-compose exec web python create_sample_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_simple')
django.setup()

from django.contrib.auth import get_user_model
from skills.models import Category, Skill
from points.models import PointsPackage

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create categories
    categories_data = [
        {
            'name': 'Programming & Development',
            'name_ar': 'البرمجة والتطوير',
            'description': 'Web development, mobile apps, software engineering',
            'icon': 'fas fa-code'
        },
        {
            'name': 'Design & Creative',
            'name_ar': 'التصميم والإبداع',
            'description': 'Graphic design, UI/UX, branding',
            'icon': 'fas fa-palette'
        },
        {
            'name': 'Digital Marketing',
            'name_ar': 'التسويق الرقمي',
            'description': 'SEO, social media, content marketing',
            'icon': 'fas fa-bullhorn'
        }
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Created category: {category.name}")
    
    # Create points packages
    packages_data = [
        {
            'name': 'Starter Pack',
            'name_ar': 'حزمة البداية',
            'points': 50,
            'price': 50.00,
            'discount_percentage': 0
        },
        {
            'name': 'Popular Pack',
            'name_ar': 'الحزمة الشائعة',
            'points': 200,
            'price': 170.00,
            'discount_percentage': 15,
            'is_popular': True
        },
        {
            'name': 'Premium Pack',
            'name_ar': 'الحزمة المميزة',
            'points': 500,
            'price': 400.00,
            'discount_percentage': 20
        }
    ]
    
    for pkg_data in packages_data:
        package, created = PointsPackage.objects.get_or_create(
            name=pkg_data['name'],
            defaults=pkg_data
        )
        if created:
            print(f"✅ Created package: {package.name}")
    
    # Create sample users
    users_data = [
        {
            'email': 'ahmed@example.com',
            'first_name': 'Ahmed',
            'last_name': 'Hassan',
            'bio': 'Full-stack developer with 5+ years experience',
            'points_balance': 500
        },
        {
            'email': 'sara@example.com',
            'first_name': 'Sara',
            'last_name': 'Mohamed',
            'bio': 'UI/UX designer passionate about user experience',
            'points_balance': 300
        }
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✅ Created user: {user.full_name}")
    
    # Create sample skills
    try:
        programming_category = Category.objects.get(name='Programming & Development')
        design_category = Category.objects.get(name='Design & Creative')
        
        ahmed = User.objects.get(email='ahmed@example.com')
        sara = User.objects.get(email='sara@example.com')
        
        skills_data = [
            {
                'user': ahmed,
                'category': programming_category,
                'title': 'Django Web Development',
                'title_ar': 'تطوير مواقع Django',
                'description': 'I will create a professional Django web application for you',
                'points_required': 100,
                'estimated_duration': '1 week',
                'language': 'both',
                'difficulty': 'intermediate'
            },
            {
                'user': sara,
                'category': design_category,
                'title': 'Logo Design',
                'title_ar': 'تصميم شعار',
                'description': 'I will design a professional logo for your business',
                'points_required': 50,
                'estimated_duration': '3 days',
                'language': 'both',
                'difficulty': 'beginner'
            }
        ]
        
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                title=skill_data['title'],
                user=skill_data['user'],
                defaults=skill_data
            )
            if created:
                print(f"✅ Created skill: {skill.title}")
    
    except (Category.DoesNotExist, User.DoesNotExist) as e:
        print(f"⚠️ Warning: Could not create skills - {e}")
    
    print("🎉 Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()
