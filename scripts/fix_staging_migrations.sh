#!/bin/bash

echo "🔧 Fixing Staging Database Migrations..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load staging environment variables
if [ -f .env.staging ]; then
    export $(grep -v '^#' .env.staging | grep -v '^$' | xargs)
    echo -e "${GREEN}✅ Loaded staging environment variables${NC}"
else
    echo -e "${RED}❌ .env.staging file not found${NC}"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    exit 1
fi

echo "🗄️ Resetting staging database..."

# Drop and recreate staging database
sudo -u postgres psql << EOF
-- Drop database if exists
DROP DATABASE IF EXISTS $STAGING_DB_NAME;

-- Drop user if exists
DROP USER IF EXISTS $STAGING_DB_USER;

-- Create user
CREATE USER $STAGING_DB_USER WITH PASSWORD '$STAGING_DB_PASSWORD';
ALTER USER $STAGING_DB_USER CREATEDB;

-- Create database
CREATE DATABASE $STAGING_DB_NAME OWNER $STAGING_DB_USER;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $STAGING_DB_NAME TO $STAGING_DB_USER;

-- Connect to database and grant schema privileges
\c $STAGING_DB_NAME
GRANT ALL ON SCHEMA public TO $STAGING_DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $STAGING_DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $STAGING_DB_USER;

\q
EOF

echo -e "${GREEN}✅ Database recreated successfully${NC}"

# Remove old migration files
echo "🧹 Cleaning old migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Create fresh migrations
echo "📝 Creating fresh migrations..."
python manage.py makemigrations accounts --settings=skillswap.settings
python manage.py makemigrations skills --settings=skillswap.settings
python manage.py makemigrations points --settings=skillswap.settings
python manage.py makemigrations chat --settings=skillswap.settings
python manage.py makemigrations payments --settings=skillswap.settings
python manage.py makemigrations reviews --settings=skillswap.settings
python manage.py makemigrations notifications --settings=skillswap.settings

# Apply migrations
echo "🔄 Applying migrations..."
python manage.py migrate --settings=skillswap.settings

echo -e "${GREEN}✅ Migrations applied successfully${NC}"

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell --settings=skillswap.settings << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='staging_admin').exists():
    admin_user = User.objects.create_superuser(
        username='staging_admin',
        email='admin@staging.com',
        password='staging123',
        first_name='Staging',
        last_name='Admin'
    )
    print("✅ Staging admin created: staging_admin/staging123")
else:
    print("✅ Staging admin already exists")
EOF

# Seed data
echo "🌱 Seeding staging data..."
python manage.py shell --settings=skillswap.settings << 'EOF'
from django.contrib.auth import get_user_model
from skills.models import Category, Skill
from points.models import PointPackage
import random

User = get_user_model()

# Create categories
categories_data = [
    {'name': 'البرمجة', 'description': 'مهارات البرمجة وتطوير البرمجيات'},
    {'name': 'التصميم', 'description': 'التصميم الجرافيكي وتصميم الواجهات'},
    {'name': 'التسويق', 'description': 'التسويق الرقمي ووسائل التواصل الاجتماعي'},
    {'name': 'اللغات', 'description': 'تعلم اللغات المختلفة'},
    {'name': 'الأعمال', 'description': 'إدارة الأعمال والمشاريع'},
]

print("📂 Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f"✅ Created category: {category.name}")

# Create skills
skills_data = [
    {'title': 'تطوير مواقع بـ Python Django', 'category': 'البرمجة', 'price': 150},
    {'title': 'تصميم تطبيقات React', 'category': 'البرمجة', 'price': 200},
    {'title': 'تصميم الشعارات والهوية البصرية', 'category': 'التصميم', 'price': 100},
    {'title': 'تصميم واجهات المستخدم UI/UX', 'category': 'التصميم', 'price': 180},
    {'title': 'التسويق عبر وسائل التواصل الاجتماعي', 'category': 'التسويق', 'price': 120},
    {'title': 'إعلانات جوجل وفيسبوك', 'category': 'التسويق', 'price': 160},
    {'title': 'تعليم اللغة الإنجليزية', 'category': 'اللغات', 'price': 80},
    {'title': 'تعليم اللغة الفرنسية', 'category': 'اللغات', 'price': 90},
    {'title': 'إدارة المشاريع', 'category': 'الأعمال', 'price': 140},
    {'title': 'استشارات الأعمال والتخطيط', 'category': 'الأعمال', 'price': 200},
]

print("🎯 Creating skills...")
admin_user = User.objects.filter(is_superuser=True).first()
for skill_data in skills_data:
    try:
        category = Category.objects.get(name=skill_data['category'])
        skill, created = Skill.objects.get_or_create(
            title=skill_data['title'],
            defaults={
                'description': f"وصف تفصيلي لمهارة {skill_data['title']}",
                'category': category,
                'price': skill_data['price'],
                'provider': admin_user
            }
        )
        if created:
            print(f"✅ Created skill: {skill.title}")
    except Exception as e:
        print(f"❌ Error creating skill {skill_data['title']}: {e}")

# Create point packages
packages_data = [
    {'name': 'حزمة المبتدئ', 'points': 100, 'price': 10.00},
    {'name': 'حزمة المتوسط', 'points': 500, 'price': 45.00},
    {'name': 'حزمة المتقدم', 'points': 1000, 'price': 80.00},
    {'name': 'حزمة الخبير', 'points': 2500, 'price': 180.00},
]

print("💰 Creating point packages...")
for pkg_data in packages_data:
    package, created = PointPackage.objects.get_or_create(
        name=pkg_data['name'],
        defaults={
            'points': pkg_data['points'],
            'price': pkg_data['price'],
            'description': f"حزمة {pkg_data['points']} نقطة بسعر ${pkg_data['price']}"
        }
    )
    if created:
        print(f"✅ Created package: {package.name}")

# Create test users
users_data = [
    {'username': 'user1', 'email': 'user1@staging.com', 'first_name': 'أحمد', 'last_name': 'محمد'},
    {'username': 'user2', 'email': 'user2@staging.com', 'first_name': 'فاطمة', 'last_name': 'علي'},
    {'username': 'user3', 'email': 'user3@staging.com', 'first_name': 'محمد', 'last_name': 'حسن'},
    {'username': 'user4', 'email': 'user4@staging.com', 'first_name': 'نور', 'last_name': 'أحمد'},
    {'username': 'user5', 'email': 'user5@staging.com', 'first_name': 'سارة', 'last_name': 'محمود'},
]

print("👥 Creating test users...")
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'is_active': True,
            'points_balance': random.randint(50, 500)
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Created user: {user.username} ({user.first_name} {user.last_name})")

print("🎉 Staging data seeding completed!")
print(f"📊 Total Categories: {Category.objects.count()}")
print(f"🎯 Total Skills: {Skill.objects.count()}")
print(f"💰 Total Point Packages: {PointPackage.objects.count()}")
print(f"👥 Total Users: {User.objects.count()}")
EOF

echo -e "${GREEN}🎉 Staging database setup complete!${NC}"
echo ""
echo "🌐 You can now access:"
echo "   Swagger UI: http://localhost:8001/swagger/"
echo "   Admin Panel: http://localhost:8001/admin/"
echo "   API Root: http://localhost:8001/api/"
echo ""
echo "👤 Admin: staging_admin / staging123"
echo "👥 Test Users: user1@staging.com to user5@staging.com / test123"
