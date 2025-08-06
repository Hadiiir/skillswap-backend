#!/usr/bin/env python
"""
Add more marketing skills if needed
Run with: docker-compose exec web python manage.py shell < scripts/add_more_marketing_skills.py
"""

from skills.models import Category, Skill
from django.contrib.auth import get_user_model

User = get_user_model()

print("📢 Adding Additional Marketing Skills")
print("=" * 35)

# Get the marketing category
marketing_category = Category.objects.filter(name__icontains='Marketing').first()
if not marketing_category:
    print("❌ Marketing category not found!")
    exit()

print(f"📂 Category: {marketing_category.name} (ID: {marketing_category.id})")

# Check existing skills
existing_count = Skill.objects.filter(category=marketing_category, status='active').count()
print(f"📊 Existing Skills: {existing_count}")

if existing_count < 3:
    print("➕ Adding new marketing skills...")
    
    user = User.objects.first()
    if not user:
        print("❌ No users found!")
        exit()
    
    additional_skills = [
        {
            'title': 'Facebook Ads Management',
            'title_ar': 'إدارة إعلانات فيسبوك',
            'description': 'Create and manage profitable Facebook advertising campaigns',
            'description_ar': 'إنشاء وإدارة حملات إعلانية مربحة على فيسبوك',
            'language': 'both',
            'difficulty': 'intermediate',
            'points_required': 95,
            'tags': 'facebook, ads, social media, marketing'
        },
        {
            'title': 'Instagram Marketing',
            'title_ar': 'التسويق عبر إنستغرام',
            'description': 'Grow your Instagram following and engagement',
            'description_ar': 'زيادة متابعيك وتفاعلك على إنستغرام',
            'language': 'ar',
            'difficulty': 'beginner',
            'points_required': 65,
            'tags': 'instagram, social media, marketing, growth'
        },
        {
            'title': 'YouTube Channel Optimization',
            'title_ar': 'تحسين قناة يوتيوب',
            'description': 'Optimize your YouTube channel for maximum views',
            'description_ar': 'تحسين قناة يوتيوب للحصول على أقصى مشاهدات',
            'language': 'en',
            'difficulty': 'intermediate',
            'points_required': 85,
            'tags': 'youtube, video, marketing, seo'
        },
        {
            'title': 'Influencer Marketing Strategy',
            'title_ar': 'استراتيجية التسويق بالمؤثرين',
            'description': 'Build effective influencer marketing campaigns',
            'description_ar': 'بناء حملات تسويق فعالة بالمؤثرين',
            'language': 'both',
            'difficulty': 'advanced',
            'points_required': 140,
            'tags': 'influencer, marketing, strategy, social'
        },
        {
            'title': 'WhatsApp Business Marketing',
            'title_ar': 'التسويق عبر واتساب بزنس',
            'description': 'Use WhatsApp Business for customer engagement',
            'description_ar': 'استخدام واتساب بزنس للتفاعل مع العملاء',
            'language': 'ar',
            'difficulty': 'beginner',
            'points_required': 45,
            'tags': 'whatsapp, business, marketing, messaging'
        }
    ]
    
    created_count = 0
    for skill_data in additional_skills:
        skill_data['user'] = user
        skill_data['category'] = marketing_category
        skill_data['status'] = 'active'
        skill_data['estimated_duration'] = '1-2 weeks'
        
        skill, created = Skill.objects.get_or_create(
            title=skill_data['title'],
            defaults=skill_data
        )
        
        if created:
            created_count += 1
            print(f"  ✅ {skill.title} - {skill.points_required} points")
    
    print(f"\n🎉 {created_count} new marketing skills created!")

# Show all marketing skills
final_count = Skill.objects.filter(category=marketing_category, status='active').count()
print(f"\n📊 Total Marketing Skills: {final_count}")

marketing_skills = Skill.objects.filter(category=marketing_category, status='active')
print("\n📋 Marketing Skills List:")
for i, skill in enumerate(marketing_skills, 1):
    print(f"  {i}. {skill.title} - {skill.points_required} points - {skill.difficulty}")

print(f"\n🌐 Test the filter: http://localhost:8000/api/skills/?category={marketing_category.id}")
