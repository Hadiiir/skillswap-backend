#!/usr/bin/env python
"""
Setup script for SkillSwap local development
"""
import os
import sys
import django
import subprocess
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django with local settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_local')

def setup_local_development():
    """Set up local development environment"""
    print("🚀 Setting up SkillSwap Local Development")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("📦 Setting up local SQLite database...")
    
    try:
        # Initialize Django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.contrib.auth import get_user_model
        from skills.models import Category
        from points.models import PointsPackage
        
        User = get_user_model()
        
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("👤 Creating superuser...")
        if not User.objects.filter(email='admin@skillswap.com').exists():
            User.objects.create_superuser(
                email='admin@skillswap.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("✅ Superuser created: admin@skillswap.com / admin123")
        else:
            print("ℹ️  Superuser already exists")
        
        print("📂 Creating categories...")
        categories = [
            {'name': 'Programming', 'name_ar': 'البرمجة', 'description': 'Programming and software development', 'icon': 'fas fa-code'},
            {'name': 'Design', 'name_ar': 'التصميم', 'description': 'Graphic and web design', 'icon': 'fas fa-paint-brush'},
            {'name': 'Marketing', 'name_ar': 'التسويق', 'description': 'Digital marketing and advertising', 'icon': 'fas fa-bullhorn'},
            {'name': 'Writing', 'name_ar': 'الكتابة', 'description': 'Content writing and copywriting', 'icon': 'fas fa-pen'},
            {'name': 'Translation', 'name_ar': 'الترجمة', 'description': 'Language translation services', 'icon': 'fas fa-language'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                print(f"✅ Created category: {category.name}")
        
        print("💰 Creating points packages...")
        packages = [
            {'name': 'Starter Pack', 'name_ar': 'حزمة المبتدئين', 'points': 100, 'price': 10.00, 'currency': 'USD'},
            {'name': 'Pro Pack', 'name_ar': 'الحزمة الاحترافية', 'points': 500, 'price': 45.00, 'currency': 'USD', 'discount_percentage': 10, 'is_popular': True},
            {'name': 'Premium Pack', 'name_ar': 'الحزمة المميزة', 'points': 1000, 'price': 80.00, 'currency': 'USD', 'discount_percentage': 20},
        ]
        
        for pkg_data in packages:
            package, created = PointsPackage.objects.get_or_create(
                name=pkg_data['name'],
                defaults=pkg_data
            )
            if created:
                print(f"✅ Created package: {package.name}")
        
        print("🎯 Creating test users...")
        test_users = [
            {'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'testpass123'},
            {'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'password': 'testpass123'},
        ]
        
        for user_data in test_users:
            if not User.objects.filter(email=user_data['email']).exists():
                User.objects.create_user(**user_data)
                print(f"✅ Created user: {user_data['email']}")
        
        print("\n🎉 Local development setup completed!")
        print("=" * 50)
        print("🌐 You can now run: python manage.py runserver --settings=skillswap.settings_local")
        print("👤 Admin: admin@skillswap.com / admin123")
        print("🔗 Admin Panel: http://localhost:8000/admin/")
        print("📚 API Docs: http://localhost:8000/api/")
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_local_development()
