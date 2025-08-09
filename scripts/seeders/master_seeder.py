#!/usr/bin/env python
"""
Master Seeder for SkillSwap - Runs all seeders in correct order
Comprehensive seeding system that matches all models exactly
"""
import os
import sys
import django
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_staging')

import django

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
import django
django.setup()

from create_superuser_seeder import CreateSuperuserSeeder
from categories_seeder import CategoriesSeeder
from users_seeder import UsersSeeder
from points_seeder import PointsSeeder
from skills_seeder import SkillsSeeder
from orders_seeder import OrdersSeeder
from reviews_seeder import ReviewsSeeder
from notifications_seeder import NotificationsSeeder
from payments_seeder import PaymentsSeeder
from chatroom_seeder import ChatRoomSeeder


class MasterSeeder:
    """Master seeder that runs all seeders in the correct dependency order"""
    
    def __init__(self):
        self.seeders = [
            ('Superuser', CreateSuperuserSeeder, 'إنشاء حساب المدير الرئيسي'),
            ('Categories', CategoriesSeeder, 'إنشاء فئات المهارات'),
            ('Users', UsersSeeder, 'إنشاء المستخدمين وملفاتهم الشخصية'),
            ('Points Packages', PointsSeeder, 'إنشاء حزم النقاط'),
            ('Skills', SkillsSeeder, 'إنشاء المهارات والأسئلة الشائعة'),
            ('Orders', OrdersSeeder, 'إنشاء الطلبات النموذجية'),
            ('Reviews', ReviewsSeeder, 'إنشاء التقييمات والمراجعات'),
            ('Payments', PaymentsSeeder, 'إنشاء سجلات المدفوعات'),
            ('Notifications', NotificationsSeeder, 'إنشاء الإشعارات'),
            ('ChatRoom', ChatRoomSeeder, 'إنشاء غرف المحادثة')
        ]
        
        self.total_created = 0
        self.total_updated = 0
        self.total_skipped = 0
        self.total_errors = 0
        self.total_warnings = 0
        self.start_time = None
        self.end_time = None
    
    def print_header(self):
        """Print seeding header"""
        print("🌱 SkillSwap Database Seeding System")
        print("=" * 60)
        print("📋 This will seed your database with comprehensive sample data")
        print("🔄 All models will be populated with realistic Arabic/English content")
        print("⚡ Seeding order optimized for model dependencies")
        print("=" * 60)
    
    def print_seeder_info(self, name, description, index, total):
        """Print seeder information"""
        print(f"\n📦 [{index}/{total}] {name} Seeder")
        print(f"📝 {description}")
        print("-" * 50)
    
    def run_all(self):
        """Run all seeders in dependency order"""
        self.start_time = datetime.now()
        self.print_header()
        
        total_seeders = len(self.seeders)
        
        for index, (seeder_name, seeder_class, description) in enumerate(self.seeders, 1):
            self.print_seeder_info(seeder_name, description, index, total_seeders)
            
            try:
                seeder = seeder_class()
                seeder.seed()
                
                # Accumulate statistics
                self.total_created += seeder.created_count
                self.total_updated += seeder.updated_count
                self.total_skipped += getattr(seeder, 'skipped_count', 0)
                self.total_errors += len(seeder.errors)
                self.total_warnings += len(getattr(seeder, 'warnings', []))
                
            except Exception as e:
                print(f"❌ Fatal error running {seeder_name} seeder: {str(e)}")
                self.total_errors += 1
                continue
        
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print comprehensive final summary"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("🎉 SkillSwap Database Seeding Completed!")
        print("=" * 60)
        
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"📊 Final Statistics:")
        print(f"   ✅ Created: {self.total_created}")
        print(f"   🔄 Updated: {self.total_updated}")
        print(f"   ⏭️  Skipped: {self.total_skipped}")
        print(f"   ⚠️  Warnings: {self.total_warnings}")
        print(f"   ❌ Errors: {self.total_errors}")
        
        if self.total_errors == 0:
            print("\n🎊 All seeders completed successfully!")
            print("✨ Your database is now populated with comprehensive sample data")
        else:
            print(f"\n⚠️  Completed with {self.total_errors} errors. Check logs above.")
        
        print("\n🚀 Your SkillSwap platform is now ready!")
        print("=" * 60)
        
        print("🔗 Next Steps:")
        print("   1. Start your Django server:")
        print("      python manage.py runserver")
        print("   2. Visit the admin panel:")
        print("      http://localhost:8000/admin/")
        print("   3. Login with admin credentials:")
        print("      Email: admin@skillswap.com")
        print("      Password: admin123")
        
        print("\n👥 Sample User Accounts:")
        sample_users = [
            "ahmed.developer@skillswap.com",
            "sara.designer@skillswap.com", 
            "omar.marketer@skillswap.com",
            "fatima.writer@skillswap.com"
        ]
        
        for user in sample_users:
            print(f"   📧 {user} / skillswap123")
        
        print("\n📱 Available Features:")
        print("   🎯 12 skill categories with Arabic/English content")
        print("   👨‍💼 8 sample users with detailed profiles and skills")
        print("   📦 6 points packages with different pricing tiers")
        print("   🎓 8 comprehensive skills with FAQs and descriptions")
        print("   📋 50 sample orders in various statuses")
        print("   ⭐ Realistic reviews and ratings")
        print("   💳 30 payment records with different methods")
        print("   🔔 Comprehensive notification system")
        
        print("\n🌐 API Endpoints Available:")
        print("   📊 Swagger UI: http://localhost:8000/swagger/")
        print("   📖 ReDoc: http://localhost:8000/redoc/")
        print("   🔌 API Root: http://localhost:8000/api/")
        
        print("=" * 60)
        print("🙏 Thank you for using SkillSwap Database Seeder!")
        print("💡 For support, check the documentation or contact the team.")
        print("=" * 60)

if __name__ == '__main__':
    master_seeder = MasterSeeder()
    master_seeder.run_all()
