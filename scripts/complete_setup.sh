#!/bin/bash

echo "🚀 Complete SkillSwap Setup"
echo "=========================="

# Make script executable
chmod +x scripts/fix_migrations.sh

# Fix migrations first
echo "🔧 Step 1: Fixing migrations..."
./scripts/fix_migrations.sh

if [ $? -ne 0 ]; then
    echo "❌ Migration fix failed!"
    exit 1
fi

# Create superuser
echo "👤 Step 2: Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@skillswap.com').exists():
    User.objects.create_superuser(
        email='admin@skillswap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created: admin@skillswap.com / admin123')
else:
    print('ℹ️  Superuser already exists')
"

# Run seeders
echo "🌱 Step 3: Running seeders..."
./scripts/run_seeders.sh all

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "🔗 Next Steps:"
echo "   1. Start server: python manage.py runserver"
echo "   2. Admin panel: http://localhost:8000/admin/"
echo "   3. API docs: http://localhost:8000/swagger/"
echo "   4. Login: admin@skillswap.com / admin123"
echo ""
