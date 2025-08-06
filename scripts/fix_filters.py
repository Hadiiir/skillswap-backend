#!/usr/bin/env python
"""
Script to fix common filter issues
Run with: docker-compose exec web python scripts/fix_filters.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_simple')
django.setup()

from skills.models import Category, Skill

def fix_filters():
    print("🔧 إصلاح مشاكل الفلاتر")
    print("=" * 25)
    
    # 1. التأكد من وجود فئات نشطة
    active_categories = Category.objects.filter(is_active=True)
    print(f"\n📋 الفئات النشطة: {active_categories.count()}")
    
    if active_categories.count() == 0:
        print("⚠�� لا توجد فئات نشطة! إنشاء فئات تجريبية...")
        Category.objects.all().update(is_active=True)
        print("✅ تم تفعيل جميع الفئات")
    
    # 2. التأكد من وجود مهارات نشطة
    active_skills = Skill.objects.filter(status='active')
    print(f"📝 المهارات النشطة: {active_skills.count()}")
    
    if active_skills.count() == 0:
        print("⚠️ لا توجد مهارات نشطة! تفعيل المهارات...")
        Skill.objects.all().update(status='active')
        print("✅ تم تفعيل جميع المهارات")
    
    # 3. إصلاح القيم الفارغة
    print("\n🔧 إصلاح القيم الفارغة:")
    
    # إصلاح اللغة
    skills_no_lang = Skill.objects.filter(language__isnull=True)
    if skills_no_lang.exists():
        skills_no_lang.update(language='en')
        print(f"✅ تم إصلاح {skills_no_lang.count()} مهارة بدون لغة")
    
    # إصلاح الصعوبة
    skills_no_diff = Skill.objects.filter(difficulty__isnull=True)
    if skills_no_diff.exists():
        skills_no_diff.update(difficulty='beginner')
        print(f"✅ تم إصلاح {skills_no_diff.count()} مهارة بدون صعوبة")
    
    # إصلاح النقاط
    skills_no_points = Skill.objects.filter(points_required__isnull=True)
    if skills_no_points.exists():
        skills_no_points.update(points_required=50)
        print(f"✅ تم إصلاح {skills_no_points.count()} مهارة بدون نقاط")
    
    # 4. إنشاء مهارات تجريبية إضافية للاختبار
    print("\n➕ إنشاء مهارات تجريبية للاختبار:")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # البحث عن مستخدم موجود
        user = User.objects.first()
        if not user:
            print("⚠️ لا يوجد مستخدمين! إنشاء مستخدم تجريبي...")
            user = User.objects.create_user(
                email='testuser@example.com',
                first_name='Test',
                last_name='User',
                password='testpass123'
            )
        
        # إنشاء مهارات متنوعة
        categories = Category.objects.all()[:3]
        languages = ['en', 'ar', 'both']
        difficulties = ['beginner', 'intermediate', 'advanced']
        
        test_skills = [
            {
                'title': 'Web Design Basics',
                'title_ar': 'أساسيات تصميم المواقع',
                'description': 'Learn web design fundamentals',
                'language': 'both',
                'difficulty': 'beginner',
                'points_required': 30
            },
            {
                'title': 'Advanced Python Programming',
                'title_ar': 'برمجة Python المتقدمة',
                'description': 'Master advanced Python concepts',
                'language': 'en',
                'difficulty': 'advanced',
                'points_required': 200
            },
            {
                'title': 'Digital Marketing Strategy',
                'title_ar': 'استراتيجية التسويق الرقمي',
                'description': 'Create effective marketing campaigns',
                'language': 'ar',
                'difficulty': 'intermediate',
                'points_required': 120
            }
        ]
        
        for i, skill_data in enumerate(test_skills):
            if i < len(categories):
                skill_data['user'] = user
                skill_data['category'] = categories[i]
                skill_data['status'] = 'active'
                
                skill, created = Skill.objects.get_or_create(
                    title=skill_data['title'],
                    defaults=skill_data
                )
                if created:
                    print(f"✅ تم إنشاء: {skill.title}")
    
    except Exception as e:
        print(f"⚠️ خطأ في إنشاء المهارات التجريبية: {e}")
    
    print("\n🎉 تم الانتهاء من الإصلاح!")
    print("\n📊 الإحصائيات النهائية:")
    print(f"- الفئات النشطة: {Category.objects.filter(is_active=True).count()}")
    print(f"- المهارات النشطة: {Skill.objects.filter(status='active').count()}")
    
    # عرض توزيع الفلاتر
    print(f"- اللغة الإنجليزية: {Skill.objects.filter(language='en', status='active').count()}")
    print(f"- اللغة العربية: {Skill.objects.filter(language='ar', status='active').count()}")
    print(f"- اللغتان معاً: {Skill.objects.filter(language='both', status='active').count()}")
    print(f"- مبتدئ: {Skill.objects.filter(difficulty='beginner', status='active').count()}")
    print(f"- متوسط: {Skill.objects.filter(difficulty='intermediate', status='active').count()}")
    print(f"- متقدم: {Skill.objects.filter(difficulty='advanced', status='active').count()}")

if __name__ == '__main__':
    fix_filters()
