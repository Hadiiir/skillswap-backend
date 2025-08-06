#!/usr/bin/env python
"""
Points Seeder for SkillSwap
Seeds points packages matching the PointsPackage model
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
from points.models import PointsPackage

class PointsSeeder(BaseSeeder):
    """Seeder for points packages matching the PointsPackage model exactly"""
    
    def __init__(self):
        super().__init__()
        self.created_count = 0
        self.updated_count = 0
    
    def get_data(self):
        """Return points packages data matching PointsPackage model fields"""
        return [
            {
                'name': 'حزمة المبتدئ',
                'name_ar': 'حزمة المبتدئ',
                'points': 100,
                'price': 15.00,
                'currency': 'USD',
                'discount_percentage': 0,
                'is_popular': False,
                'is_active': True
            },
            {
                'name': 'حزمة الأساسية',
                'name_ar': 'حزمة الأساسية',
                'points': 250,
                'price': 35.00,
                'currency': 'USD',
                'discount_percentage': 5,
                'is_popular': False,
                'is_active': True
            },
            {
                'name': 'حزمة المحترف',
                'name_ar': 'حزمة المحترف',
                'points': 500,
                'price': 65.00,
                'currency': 'USD',
                'discount_percentage': 10,
                'is_popular': True,
                'is_active': True
            },
            {
                'name': 'حزمة الخبير',
                'name_ar': 'حزمة الخبير',
                'points': 1000,
                'price': 120.00,
                'currency': 'USD',
                'discount_percentage': 15,
                'is_popular': False,
                'is_active': True
            },
            {
                'name': 'حزمة المؤسسات',
                'name_ar': 'حزمة المؤسسات',
                'points': 2500,
                'price': 280.00,
                'currency': 'USD',
                'discount_percentage': 20,
                'is_popular': False,
                'is_active': True
            },
            {
                'name': 'حزمة الشركات الكبرى',
                'name_ar': 'حزمة الشركات الكبرى',
                'points': 5000,
                'price': 500.00,
                'currency': 'USD',
                'discount_percentage': 25,
                'is_popular': False,
                'is_active': True
            }
        ]
    
    def seed(self):
        """Seed points packages"""
        self.log_info("Starting points packages seeding...")
        
        for package_data in self.get_data():
            if self.create_object(package_data):
                self.created_count += 1
        
        self.log_success("Points packages seeding completed!")
        self.print_summary()
    
    def create_object(self, data):
        """Create points package object matching the PointsPackage model"""
        package, created = self.get_or_create_safe(
            PointsPackage,
            defaults={
                'name_ar': data['name_ar'],
                'points': data['points'],
                'price': data['price'],
                'currency': data['currency'],
                'discount_percentage': data['discount_percentage'],
                'is_popular': data['is_popular'],
                'is_active': data['is_active']
            },
            name=data['name']
        )
        
        if package:
            action = "Created" if created else "Updated"
            # Fix decimal calculation
            discount_decimal = data['discount_percentage'] / 100.0
            discounted_price = float(data['price']) * (1 - discount_decimal)
            self.log_success(f"{action} package: {data['name']} - {data['points']} points for ${discounted_price:.2f}")
            return True
        
        return False
    
    def print_summary(self):
        """Print seeding summary"""
        self.log_info("=" * 50)
        self.log_info(f"📊 Points Packages Seeder Summary")
        self.log_info("=" * 50)
        self.log_info(f"⏱️  Duration: {self.get_duration():.2f} seconds")
        self.log_success(f"✅ Created: {self.created_count}")
        self.log_info(f"🔄 Updated: {self.updated_count}")
        self.log_info(f"⏭️  Skipped: 0")
        self.log_info(f"⚠️  Warnings: 0")
        self.log_info(f"❌ Errors: 0")
        self.log_success("🎉 Points packages seeding completed successfully!")
        self.log_info("=" * 50)

if __name__ == '__main__':
    seeder = PointsSeeder()
    seeder.seed()
