#!/usr/bin/env python
"""
Script to create a superuser for SkillSwap
"""
import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Create a superuser"""
    User = get_user_model()
    
    print("🔐 Creating SkillSwap Superuser")
    print("=" * 40)
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("⚠️  Superuser already exists!")
        existing_admin = User.objects.filter(is_superuser=True).first()
        print(f"   Email: {existing_admin.email}")
        print(f"   Name: {existing_admin.first_name} {existing_admin.last_name}")
        return
    
    # Create superuser
    try:
        admin_user = User.objects.create_superuser(
            email='admin@skillswap.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        print("✅ Superuser created successfully!")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: admin123")
        print(f"   Name: {admin_user.first_name} {admin_user.last_name}")
        print("\n🌐 Access admin panel at: http://localhost:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()
