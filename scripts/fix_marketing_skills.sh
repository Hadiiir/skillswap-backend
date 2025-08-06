#!/bin/bash

echo "🔧 Fixing Digital Marketing Skills"
echo "================================="

# Fix TTY issue
echo "📝 Creating marketing skills..."

# Use docker exec instead of shell input
docker-compose -f docker-compose.simple.yml exec -T web python manage.py shell << 'EOF'
from skills.models import Category, Skill
from django.contrib.auth import get_user_model

User = get_user_model()

print("📢 Adding marketing skills")
print("=" * 25)

# Get marketing category
marketing_category = Category.objects.filter(name__icontains='Marketing').first()
if not marketing_category:
    print("❌ Marketing category not found!")
    # Create category if not exists
    marketing_category = Category.objects.create(
        name='Digital Marketing',
        name_ar='التسويق الرقمي',
        description='Digital marketing and advertising services',
        description_ar='خدمات التسويق الرقمي والإعلان',
        icon='fas fa-bullhorn',
        is_active=True
    )
    print(f"✅ Created category: {marketing_category.name}")

print(f"📂 Category: {marketing_category.name} (ID: {marketing_category.id})")

# Get user
user = User.objects.first()
if not user:
    print("❌ No users found!")
    user = User.objects.create_user(
        email='marketer@example.com',
        first_name='Marketing',
        last_name='Expert',
        password='testpass123'
    )
    print(f"✅ Created user: {user.full_name}")

# Digital marketing skills
marketing_skills = [
    {
        'title': 'SEO Optimization',
        'title_ar': 'تحسين محركات البحث',
        'description': 'Improve your website ranking on Google and search engines',
        'description_ar': 'تحسين ترتيب موقعك في جوجل ومحركات البحث',
        'language': 'both',
        'difficulty': 'intermediate',
        'points_required': 110,
        'tags': 'seo, google, ranking, optimization, search'
    },
    {
        'title': 'Social Media Marketing',
        'title_ar': 'التسويق عبر وسائل التواصل',
        'description': 'Grow your social media presence and engagement',
        'description_ar': 'تنمية حضورك وتفاعلك على وسائل التواصل الاجتماعي',
        'language': 'ar',
        'difficulty': 'beginner',
        'points_required': 70,
        'tags': 'social media, facebook, instagram, twitter, marketing'
    },
    {
        'title': 'Google Ads Management',
        'title_ar': 'إدارة إعلانات جوجل',
        'description': 'Professional Google Ads campaign setup and management',
        'description_ar': 'إعداد وإدارة حملات إعلانات جوجل بشكل احترافي',
        'language': 'en',
        'difficulty': 'advanced',
        'points_required': 160,
        'tags': 'google ads, ppc, advertising, campaigns, marketing'
    },
    {
        'title': 'Content Marketing Strategy',
        'title_ar': 'استراتيجية تسويق المحتوى',
        'description': 'Create engaging content that converts visitors to customers',
        'description_ar': 'إنشاء محتوى جذاب يحول الزوار إلى عملاء',
        'language': 'both',
        'difficulty': 'intermediate',
        'points_required': 90,
        'tags': 'content, marketing, strategy, copywriting, blogging'
    },
    {
        'title': 'Email Marketing Campaigns',
        'title_ar': 'حملات التسويق عبر البريد الإلكتروني',
        'description': 'Build effective email marketing campaigns that drive sales',
        'description_ar': 'بناء حملات تسويق فعالة عبر البريد الإلكتروني تحقق المبيعات',
        'language': 'ar',
        'difficulty': 'beginner',
        'points_required': 60,
        'tags': 'email, marketing, campaigns, automation, newsletters'
    },
    {
        'title': 'Facebook Ads Management',
        'title_ar': 'إدارة إعلانات فيسبوك',
        'description': 'Create and optimize profitable Facebook advertising campaigns',
        'description_ar': 'إنشاء وتحسين حملات إعلانية مربحة على فيسبوك',
        'language': 'both',
        'difficulty': 'intermediate',
        'points_required': 95,
        'tags': 'facebook, ads, social media, advertising, campaigns'
    },
    {
        'title': 'Instagram Marketing',
        'title_ar': 'التسويق عبر إنستغرام',
        'description': 'Grow your Instagram following and increase engagement',
        'description_ar': 'زيادة متابعيك وتفاعلك على إنستغرام',
        'language': 'ar',
        'difficulty': 'beginner',
        'points_required': 55,
        'tags': 'instagram, social media, marketing, growth, engagement'
    },
    {
        'title': 'YouTube Channel Optimization',
        'title_ar': 'تحسين قناة يوتيوب',
        'description': 'Optimize your YouTube channel for maximum views and subscribers',
        'description_ar': 'تحسين قناة يوتيوب للحصول على أقصى مشاهدات ومشتركين',
        'language': 'en',
        'difficulty': 'intermediate',
        'points_required': 85,
        'tags': 'youtube, video, marketing, seo, optimization'
    }
]

created_count = 0
for skill_data in marketing_skills:
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
        print(f"✅ {skill.title} - {skill.points_required} points - {skill.difficulty}")

print(f"\n🎉 Created {created_count} marketing skills!")

# Show final stats
final_count = Skill.objects.filter(category=marketing_category, status='active').count()
print(f"📊 Total marketing skills: {final_count}")

print(f"\n🌐 Test the filter: http://localhost:8000/api/skills/?category={marketing_category.id}")
EOF

echo ""
echo "🧪 Testing filter after adding:"
curl -s "http://localhost:8000/api/skills/?category=3" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'✅ Number of marketing skills now: {len(results)}')
    
    if len(results) > 0:
        print('\n📋 First 3 skills:')
        for i, skill in enumerate(results[:3], 1):
            print(f'  {i}. {skill.get(\"title\", \"N/A\")} - {skill.get(\"points_required\", 0)} points')
    else:
        print('❌ Still empty! I will try to fix the issue...')
        
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🎯 Testing multiple filters:"

echo "Marketing + Beginner:"
curl -s "http://localhost:8000/api/skills/?category=3&difficulty=beginner" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  Number of results: {len(results)}')
    if results:
        for skill in results:
            print(f'    - {skill.get(\"title\", \"N/A\")}')
except: print('  Error')
"

echo ""
echo "Marketing + Less than 100 points:"
curl -s "http://localhost:8000/api/skills/?category=3&points_required__lt=100" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'  Number of results: {len(results)}')
    if results:
        for skill in results:
            print(f'    - {skill.get(\"title\", \"N/A\")} ({skill.get(\"points_required\", 0)} points)')
except: print('  Error')
"

echo ""
echo "🎉 Digital Marketing Skills Fixed!"
echo "🌐 Go to: http://localhost:8000/api/skills/?category=3"
