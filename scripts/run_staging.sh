#!/bin/bash

echo "🚀 Starting Staging Environment..."

# Load staging environment
export $(cat .env.staging | xargs)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Setup staging database if needed
if ! PGPASSWORD=staging_password_123 psql -h localhost -p 5432 -U skillswap_staging -d skillswap_staging -c "SELECT 1;" &>/dev/null; then
    echo "Setting up staging database..."
    chmod +x scripts/setup_staging_db.sh
    ./scripts/setup_staging_db.sh
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create staging data
echo "Creating staging data..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from skills.models import Category, Skill
from points.models import PointsPackage
from accounts.models import UserProfile
import random

User = get_user_model()

# Create superuser
if not User.objects.filter(username='staging_admin').exists():
    admin = User.objects.create_superuser('staging_admin', 'staging@skillswap.com', 'staging123')
    print('✅ Staging superuser created: staging_admin/staging123')

# Create test users
test_users = []
for i in range(5):
    email = f'user{i+1}@staging.com'
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(
            username=f'user{i+1}',
            email=email,
            password='test123',
            first_name=f'User{i+1}',
            last_name='Test'
        )
        test_users.append(user)
        print(f'✅ Test user created: {email}/test123')

# Create categories
categories_data = [
    {'name': 'Programming', 'name_ar': 'البرمجة', 'description': 'Programming and software development'},
    {'name': 'Design', 'name_ar': 'التصميم', 'description': 'Graphic and web design'},
    {'name': 'Marketing', 'name_ar': 'التسويق', 'description': 'Digital marketing and advertising'},
    {'name': 'Languages', 'name_ar': 'اللغات', 'description': 'Language learning and teaching'},
    {'name': 'Business', 'name_ar': 'الأعمال', 'description': 'Business and entrepreneurship'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f'✅ Category created: {category.name}')

# Create skills
skills_data = [
    {'title': 'Python Programming', 'title_ar': 'برمجة Python', 'category': 'Programming', 'points': 100},
    {'title': 'React Development', 'title_ar': 'تطوير React', 'category': 'Programming', 'points': 150},
    {'title': 'Logo Design', 'title_ar': 'تصميم الشعارات', 'category': 'Design', 'points': 80},
    {'title': 'Social Media Marketing', 'title_ar': 'التسويق عبر وسائل التواصل', 'category': 'Marketing', 'points': 120},
    {'title': 'English Tutoring', 'title_ar': 'تدريس الإنجليزية', 'category': 'Languages', 'points': 90},
    {'title': 'Business Planning', 'title_ar': 'التخطيط التجاري', 'category': 'Business', 'points': 200},
    {'title': 'Web Design', 'title_ar': 'تصميم المواقع', 'category': 'Design', 'points': 180},
    {'title': 'Django Development', 'title_ar': 'تطوير Django', 'category': 'Programming', 'points': 160},
    {'title': 'Content Writing', 'title_ar': 'كتابة المحتوى', 'category': 'Marketing', 'points': 70},
    {'title': 'Arabic Teaching', 'title_ar': 'تدريس العربية', 'category': 'Languages', 'points': 85},
]

for skill_data in skills_data:
    category = Category.objects.get(name=skill_data['category'])
    if not Skill.objects.filter(title=skill_data['title']).exists():
        # Get random user as skill provider
        provider = random.choice(User.objects.all())
        skill = Skill.objects.create(
            category=category,
            provider=provider,
            title=skill_data['title'],
            title_ar=skill_data['title_ar'],
            description=f'Learn {skill_data[\"title\"]} with expert guidance',
            description_ar=f'تعلم {skill_data[\"title_ar\"]} مع إرشاد الخبراء',
            points_required=skill_data['points'],
            estimated_duration='1-2 weeks',
            language='both',
            difficulty='intermediate',
            tags=skill_data['title'].lower().replace(' ', ','),
            is_active=True
        )
        print(f'✅ Skill created: {skill.title}')

# Create points packages
packages_data = [
    {'name': 'Starter Pack', 'points': 100, 'price': 10.00},
    {'name': 'Popular Pack', 'points': 500, 'price': 45.00},
    {'name': 'Premium Pack', 'points': 1000, 'price': 80.00},
    {'name': 'Ultimate Pack', 'points': 2500, 'price': 180.00},
]

for pkg_data in packages_data:
    package, created = PointsPackage.objects.get_or_create(
        name=pkg_data['name'],
        defaults=pkg_data
    )
    if created:
        print(f'✅ Points package created: {package.name}')

print('🎉 Staging data created successfully!')
print(f'📊 Total Users: {User.objects.count()}')
print(f'📊 Total Categories: {Category.objects.count()}')
print(f'📊 Total Skills: {Skill.objects.count()}')
print(f'📊 Total Packages: {PointsPackage.objects.count()}')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Staging environment ready!"
echo "🌐 Admin: http://localhost:8001/admin (staging_admin/staging123)"
echo "📚 API: http://localhost:8001/api"
echo "📖 Swagger: http://localhost:8001/swagger"
echo "🗄️ Database: skillswap_staging on port 5434"
echo "🔴 Redis: database 1"

# Start server on port 8001
python manage.py runserver 0.0.0.0:8001
