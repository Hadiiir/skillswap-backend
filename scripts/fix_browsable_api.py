#!/usr/bin/env python
"""
Fix browsable API filters
Run with: docker-compose exec web python manage.py shell < scripts/fix_browsable_api.py
"""

from skills.models import Skill, Category
from django.contrib.auth import get_user_model

User = get_user_model()

print("🔧 إصلاح واجهة Django REST Framework")
print("=" * 40)

# 1. التأكد من وجود بيانات كافية للاختبار
print("\n📊 فحص البيانات الحالية:")
print(f"- الفئات: {Category.objects.count()}")
print(f"- المهارات النشطة: {Skill.objects.filter(status='active').count()}")

# 2. إنشاء مهارات متنوعة للاختبار
categories = Category.objects.all()
users = User.objects.all()

if users.exists() and categories.exists():
    user = users.first()
    
    # مهارات متنوعة لاختبار الفلاتر
    test_skills = [
        {
            'title': 'React Development',
            'title_ar': 'تطوير React',
            'description': 'Build modern React applications',
            'language': 'en',
            'difficulty': 'advanced',
            'points_required': 200,
            'category': categories.filter(name__icontains='Programming').first(),
        },
        {
            'title': 'Logo Design',
            'title_ar': 'تصميم الشعارات',
            'description': 'Professional logo design services',
            'language': 'both',
            'difficulty': 'beginner',
            'points_required': 50,
            'category': categories.filter(name__icontains='Design').first(),
        },
        {
            'title': 'SEO Optimization',
            'title_ar': 'تحسين محركات البحث',
            'description': 'Improve your website SEO ranking',
            'language': 'ar',
            'difficulty': 'intermediate',
            'points_required': 120,
            'category': categories.filter(name__icontains='Marketing').first(),
        },
        {
            'title': 'Python Programming',
            'title_ar': 'برمجة Python',
            'description': 'Learn Python from basics to advanced',
            'language': 'both',
            'difficulty': 'intermediate',
            'points_required': 150,
            'category': categories.filter(name__icontains='Programming').first(),
        },
        {
            'title': 'UI/UX Design',
            'title_ar': 'تصميم واجهات المستخدم',
            'description': 'Create beautiful user interfaces',
            'language': 'en',
            'difficulty': 'advanced',
            'points_required': 180,
            'category': categories.filter(name__icontains='Design').first(),
        }
    ]
    
    created_count = 0
    for skill_data in test_skills:
        if skill_data['category']:
            skill_data['user'] = user
            skill_data['status'] = 'active'
            skill_data['tags'] = f"{skill_data['language']}, {skill_data['difficulty']}"
            
            skill, created = Skill.objects.get_or_create(
                title=skill_data['title'],
                defaults=skill_data
            )
            if created:
                created_count += 1
                print(f"✅ تم إنشاء: {skill.title}")
    
    print(f"\n📈 تم إنشاء {created_count} مهارة جديدة")

# 3. عرض إحصائيات الفلاتر
print(f"\n📊 إحصائيات الفلاتر:")
print(f"- إجمالي المهارات النشطة: {Skill.objects.filter(status='active').count()}")

# ��سب الفئة
for category in categories:
    count = Skill.objects.filter(category=category, status='active').count()
    print(f"- {category.name}: {count} مهارة")

# حسب اللغة
for lang_code, lang_name in Skill.LANGUAGE_CHOICES:
    count = Skill.objects.filter(language=lang_code, status='active').count()
    print(f"- {lang_name}: {count} مهارة")

# حسب الصعوبة
for diff_code, diff_name in Skill.DIFFICULTY_CHOICES:
    count = Skill.objects.filter(difficulty=diff_code, status='active').count()
    print(f"- {diff_name}: {count} مهارة")

print(f"\n🎉 تم إصلاح البيانات!")
print(f"🌐 اذهب إلى: http://localhost:8000/api/skills/ لاختبار الفلاتر")
