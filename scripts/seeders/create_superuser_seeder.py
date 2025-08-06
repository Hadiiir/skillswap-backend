#!/usr/bin/env python
"""
Superuser Seeder for SkillSwap
Creates admin superuser account with full permissions
"""
import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from base_seeder import BaseSeeder
from accounts.models import User

class CreateSuperuserSeeder(BaseSeeder):
    """Seeder for creating admin superuser"""
    
    def get_data(self):
        """Return superuser data"""
        return [
            {
                'email': 'admin@skillswap.com',
                'first_name': 'مدير',
                'last_name': 'النظام',
                'bio': 'مدير عام لمنصة تبادل المهارات - مسؤول عن إدارة النظام والمحتوى والمستخدمين',
                'phone': '+201000000000',
                'location': 'القاهرة، مصر',
                'password': 'admin123',
                'points_balance': 10000,
                'is_superuser': True,
                'is_staff': True,
                'is_active': True
            }
        ]
    
    def create_object(self, data):
        """Create superuser object"""
        user, created = self.get_or_create_safe(
            User,
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'bio': data['bio'],
                'phone': data['phone'],
                'location': data['location'],
                'points_balance': data['points_balance'],
                'is_superuser': data['is_superuser'],
                'is_staff': data['is_staff'],
                'is_active': data['is_active']
            },
            email=data['email']
        )
        
        if user:
            if created:
                user.set_password(data['password'])
                user.save()
                self.log_success(f"Created superuser: {data['email']}")
                self.log_info(f"Login credentials: {data['email']} / {data['password']}")
            else:
                # Update password for existing superuser
                user.set_password(data['password'])
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.log_success(f"Updated superuser: {data['email']}")
            
            return True
        
        return False

if __name__ == '__main__':
    seeder = CreateSuperuserSeeder()
    seeder.seed()
