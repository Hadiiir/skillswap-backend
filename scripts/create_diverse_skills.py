#!/usr/bin/env python
"""
Create diverse skills for each category to test filters
Run with: docker-compose exec web python manage.py shell < scripts/create_diverse_skills.py
"""

from skills.models import Category, Skill
from django.contrib.auth import get_user_model

User = get_user_model()

print("🎯 Creating diverse skills to test filters")
print("=" * 40)

# Get the first user or create one
user = User.objects.first()
if not user:
    print("📝 Creating a test user...")
    user = User.objects.create_user(
        email='skillcreator@example.com',
        first_name='Skill',
        last_name='Creator',
        password='testpass123'
    )
    print(f"✅ User created: {user.full_name}")

# Get categories
categories = {
    'programming': Category.objects.filter(name__icontains='Programming').first(),
    'design': Category.objects.filter(name__icontains='Design').first(),
    'marketing': Category.objects.filter(name__icontains='Marketing').first(),
}

print(f"\n📂 Available categories:")
for key, category in categories.items():
    if category:
        print(f"- {category.name} (ID: {category.id})")

# Diverse skills for each category
skills_data = {
    'programming': [
        {
            'title': 'React.js Development',
            'title_ar': 'تطوير React.js',
            'description': 'Build modern React applications with hooks and context',
            'description_ar': 'بناء تطبيقات React حديثة باستخدام Hooks و Context',
            'language': 'en',
            'difficulty': 'advanced',
            'points_required': 200,
            'tags': 'react, javascript, frontend, hooks'
        },
        {
            'title': 'Python Django Backend',
            'title_ar': 'تطوير Backend بـ Django',
            'description': 'Create robust backend APIs with Django REST Framework',
            'description_ar': 'إنشاء APIs قوية باستخدام Django REST Framework',
            'language': 'both',
            'difficulty': 'intermediate',
            'points_required': 150,
            'tags': 'python, django, backend, api'
        },
        {
            'title': 'JavaScript Basics',
            'title_ar': 'أساسيات JavaScript',
            'description': 'Learn JavaScript fundamentals from scratch',
            'description_ar': 'تعلم أساسيات JavaScript من الصفر',
            'language': 'ar',
            'difficulty': 'beginner',
            'points_required': 80,
            'tags': 'javascript, basics, programming'
        },
        {
            'title': 'Node.js API Development',
            'title_ar': 'تطوير APIs بـ Node.js',
            'description': 'Build scalable APIs with Node.js and Express',
            'description_ar': 'بناء APIs قابلة للتوسع باستخدام Node.js و Express',
            'language': 'en',
            'difficulty': 'intermediate',
            'points_required': 120,
            'tags': 'nodejs, express, api, backend'
        },
        {
            'title': 'Mobile App Development',
            'title_ar': 'تطوير تطبيقات الجوال',
            'description': 'Create mobile apps with React Native',
            'description_ar': 'إنشاء تطبيقات الجوال باستخدام React Native',
            'language': 'both',
            'difficulty': 'advanced',
            'points_required': 250,
            'tags': 'react-native, mobile, ios, android'
        }
    ],
    'design': [
        {
            'title': 'Logo Design',
            'title_ar': 'تصميم الشعارات',
            'description': 'Professional logo design for your brand',
            'description_ar': 'تصميم شعارات احترافية لعلامتك التجارية',
            'language': 'both',
            'difficulty': 'beginner',
            'points_required': 50,
            'tags': 'logo, branding, design, illustrator'
        },
        {
            'title': 'UI/UX Design',
            'title_ar': 'تصميم واجهات المستخدم',
            'description': 'Create beautiful and functional user interfaces',
            'description_ar': 'إنشاء واجهات مستخدم جميلة وعملية',
            'language': 'en',
            'difficulty': 'advanced',
            'points_required': 180,
            'tags': 'ui, ux, design, figma, adobe'
        },
        {
            'title': 'Graphic Design',
            'title_ar': 'التصميم الجرافيكي',
            'description': 'Professional graphic design services',
            'description_ar': 'خدمات التصميم الجرافيكي الاحترافية',
            'language': 'ar',
            'difficulty': 'intermediate',
            'points_required': 100,
            'tags': 'graphic, design, photoshop, illustrator'
        },
        {
            'title': 'Web Design',
            'title_ar': 'تصميم المواقع',
            'description': 'Modern responsive web design',
            'description_ar': 'تصميم مواقع حديثة ومتجاوبة',
            'language': 'both',
            'difficulty': 'intermediate',
            'points_required': 130,
            'tags': 'web, design, responsive, css, html'
        },
        {
            'title': 'Brand Identity Design',
            'title_ar': 'تصميم الهوية التجارية',
            'description': 'Complete brand identity packages',
            'description_ar': 'حزم هوية تجارية كاملة',
            'language': 'en',
            'difficulty': 'advanced',
            'points_required': 220,
            'tags': 'branding, identity, logo, design'
        }
    ],
    'marketing': [
        {
            'title': 'SEO Optimization',
            'title_ar': 'تحسين محركات البحث',
            'description': 'Improve your website ranking on Google',
            'description_ar': 'تحسين ترتيب موقعك في جوجل',
            'language': 'ar',
            'difficulty': 'intermediate',
            'points_required': 110,
            'tags': 'seo, google, ranking, optimization'
        },
        {
            'title': 'Social Media Marketing',
            'title_ar': 'التسويق عبر وسائل التواصل',
            'description': 'Grow your social media presence',
            'description_ar': 'تنمية حضورك على وسائل التواصل الاجتماعي',
            'language': 'both',
            'difficulty': 'beginner',
            'points_required': 70,
            'tags': 'social media, marketing, facebook, instagram'
        },
        {
            'title': 'Google Ads Management',
            'title_ar': 'إدارة إعلانات جوجل',
            'description': 'Professional Google Ads campaign management',
            'description_ar': 'إدارة احترافية لحملات إعلانات جوجل',
            'language': 'en',
            'difficulty': 'advanced',
            'points_required': 160,
            'tags': 'google ads, ppc, advertising, marketing'
        },
        {
            'title': 'Content Marketing',
            'title_ar': 'تسويق المحتوى',
            'description': 'Create engaging content that converts',
            'description_ar': 'إنشاء محتوى جذاب يحقق التحويلات',
            'language': 'both',
            'difficulty': 'intermediate',
            'points_required': 90,
            'tags': 'content, marketing, copywriting, strategy'
        },
        {
            'title': 'Email Marketing',
            'title_ar': 'التسويق عبر البريد الإلكتروني',
            'description': 'Build effective email marketing campaigns',
            'description_ar': 'بناء حملات تسويق فعالة عبر البريد الإلكتروني',
            'language': 'ar',
            'difficulty': 'beginner',
            'points_required': 60,
            'tags': 'email, marketing, campaigns, automation'
        }
    ]
}

# Create skills
total_created = 0
for category_key, skills_list in skills_data.items():
    category = categories[category_key]
    if not category:
        print(f"⚠️ Category {category_key} not found")
        continue
    
    print(f"\n📝 Creating skills for category: {category.name}")
    
    for skill_data in skills_list:
        skill_data['user'] = user
        skill_data['category'] = category
        skill_data['status'] = 'active'
        skill_data['estimated_duration'] = '1-2 weeks'
        
        skill, created = Skill.objects.get_or_create(
            title=skill_data['title'],
            defaults=skill_data
        )
        
        if created:
            total_created += 1
            print(f"  ✅ {skill.title} - {skill.points_required} points - {skill.difficulty}")
        else:
            print(f"  ⚪ {skill.title} - already exists")

print(f"\n🎉 {total_created} new skills created!")

# Final stats
print(f"\n📊 Final Statistics:")
for category_key, category in categories.items():
    if category:
        count = Skill.objects.filter(category=category, status='active').count()
        print(f"- {category.name}: {count} skills")

print(f"\n🌐 Go to: http://localhost:8000/api/skills/ to test filters")
