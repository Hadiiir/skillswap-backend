#!/usr/bin/env python
"""
Seed script to populate the database with initial data
Run with: python manage.py shell < scripts/seed_data.py
"""

from django.contrib.auth import get_user_model
from skills.models import Category, Skill
from points.models import PointsPackage

User = get_user_model()

# Create categories
categories_data = [
    {
        'name': 'Programming & Development',
        'name_ar': 'البرمجة والتطوير',
        'description': 'Web development, mobile apps, software engineering',
        'description_ar': 'تطوير المواقع، تطبيقات الجوال، هندسة البرمجيات',
        'icon': 'fas fa-code'
    },
    {
        'name': 'Design & Creative',
        'name_ar': 'التصميم والإبداع',
        'description': 'Graphic design, UI/UX, branding, illustration',
        'description_ar': 'التصميم الجرافيكي، تصميم واجهات المستخدم، العلامات التجارية',
        'icon': 'fas fa-palette'
    },
    {
        'name': 'Digital Marketing',
        'name_ar': 'التسويق الرقمي',
        'description': 'SEO, social media, content marketing, advertising',
        'description_ar': 'تحسين محركات البحث، وسائل التواصل الاجتماعي، تسويق المحتوى',
        'icon': 'fas fa-bullhorn'
    },
    {
        'name': 'Writing & Translation',
        'name_ar': 'الكتابة والترجمة',
        'description': 'Content writing, copywriting, translation services',
        'description_ar': 'كتابة المحتوى، الكتابة الإعلانية، خدمات الترجمة',
        'icon': 'fas fa-pen'
    },
    {
        'name': 'Business & Consulting',
        'name_ar': 'الأعمال والاستشارات',
        'description': 'Business strategy, consulting, project management',
        'description_ar': 'استراتيجية الأعمال، الاستشارات، إدارة المشاريع',
        'icon': 'fas fa-briefcase'
    },
    {
        'name': 'Education & Training',
        'name_ar': 'التعليم والتدريب',
        'description': 'Online tutoring, course creation, skill training',
        'description_ar': 'التدريس عبر الإنترنت، إنشاء الدورات، تدريب المهارات',
        'icon': 'fas fa-graduation-cap'
    }
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"Created category: {category.name}")

# Create points packages
packages_data = [
    {
        'name': 'Starter Pack',
        'name_ar': 'حزمة البداية',
        'points': 50,
        'price': 50.00,
        'discount_percentage': 0,
        'is_popular': False
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
        'discount_percentage': 20,
        'is_popular': False
    },
    {
        'name': 'Enterprise Pack',
        'name_ar': 'حزمة المؤسسات',
        'points': 1000,
        'price': 750.00,
        'discount_percentage': 25,
        'is_popular': False
    }
]

print("Creating points packages...")
for pkg_data in packages_data:
    package, created = PointsPackage.objects.get_or_create(
        name=pkg_data['name'],
        defaults=pkg_data
    )
    if created:
        print(f"Created package: {package.name} - {package.points} points")

# Create demo users
demo_users_data = [
    {
        'email': 'ahmed.developer@example.com',
        'first_name': 'Ahmed',
        'last_name': 'Hassan',
        'bio': 'Full-stack developer with 5+ years experience in Django and React',
        'location': 'Cairo, Egypt',
        'points_balance': 500
    },
    {
        'email': 'sara.designer@example.com',
        'first_name': 'Sara',
        'last_name': 'Mohamed',
        'bio': 'UI/UX designer passionate about creating beautiful user experiences',
        'location': 'Alexandria, Egypt',
        'points_balance': 300
    },
    {
        'email': 'omar.marketer@example.com',
        'first_name': 'Omar',
        'last_name': 'Ali',
        'bio': 'Digital marketing specialist with expertise in SEO and social media',
        'location': 'Giza, Egypt',
        'points_balance': 250
    }
]

print("Creating demo users...")
for user_data in demo_users_data:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            **user_data,
            'username': user_data['email'],
            'is_active': True
        }
    )
    if created:
        user.set_password('demo123456')
        user.save()
        print(f"Created user: {user.full_name}")

print("Database seeded successfully!")
