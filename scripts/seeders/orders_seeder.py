#!/usr/bin/env python
"""
Orders Seeder for SkillSwap
Seeds sample orders matching the Order model exactly
"""
import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from base_seeder import BaseSeeder
from points.models import Order
from skills.models import Skill
from accounts.models import User
from django.utils import timezone

class OrdersSeeder(BaseSeeder):
    """Seeder for orders matching the Order model exactly"""
    
    def get_dependencies(self):
        """Orders depend on Skills and Users"""
        return ['skills.Skill', 'accounts.User']
    
    def get_data(self):
        """Generate sample orders data"""
        # Get all skills and users
        skills = list(Skill.objects.filter(status='active'))
        users = list(User.objects.filter(is_active=True, is_superuser=False))
        
        if not skills or len(users) < 2:
            self.log_error("Not enough skills or users to create orders")
            return []
        
        orders_data = []
        
        # Generate 50 sample orders
        for i in range(50):
            skill = self.get_random_choice(skills)
            # Buyer cannot be the skill owner
            available_buyers = [u for u in users if u != skill.user]
            
            if not available_buyers:
                continue
            
            buyer = self.get_random_choice(available_buyers)
            seller = skill.user
            
            # Random status with realistic distribution
            status_choices = [
                ('completed', 0.4),  # 40% completed
                ('in_progress', 0.3),  # 30% in progress
                ('accepted', 0.15),  # 15% accepted
                ('pending', 0.1),  # 10% pending
                ('cancelled', 0.05)  # 5% cancelled
            ]
            
            status = self.weighted_random_choice(status_choices)
            
            # Calculate points and fees
            points_amount = skill.points_required
            platform_fee = int(points_amount * 0.08)  # 8% platform fee
            total_points = points_amount + platform_fee
            
            # Generate realistic timestamps based on status
            created_at = timezone.now() - timedelta(days=random.randint(1, 90))
            
            order_data = {
                'buyer': buyer,
                'seller': seller,
                'skill': skill,
                'points_amount': points_amount,
                'platform_fee': platform_fee,
                'total_points': total_points,
                'status': status,
                'requirements': self.generate_requirements(skill),
                'delivery_notes': self.generate_delivery_notes(status),
                'created_at': created_at
            }
            
            # Add status-specific timestamps
            if status in ['accepted', 'in_progress', 'completed', 'cancelled']:
                order_data['accepted_at'] = created_at + timedelta(hours=random.randint(1, 48))
            
            if status in ['in_progress', 'completed']:
                order_data['started_at'] = order_data['accepted_at'] + timedelta(hours=random.randint(1, 24))
            
            if status == 'completed':
                order_data['completed_at'] = order_data['started_at'] + timedelta(days=random.randint(1, 14))
                order_data['actual_delivery'] = order_data['completed_at']
            
            if status == 'cancelled':
                order_data['cancelled_at'] = created_at + timedelta(hours=random.randint(1, 72))
            
            # Set expected delivery
            if status != 'cancelled':
                order_data['expected_delivery'] = created_at + timedelta(days=random.randint(3, 21))
            
            orders_data.append(order_data)
        
        return orders_data
    
    def weighted_random_choice(self, choices):
        """Choose randomly based on weights"""
        total = sum(weight for choice, weight in choices)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in choices:
            if upto + weight >= r:
                return choice
            upto += weight
        return choices[-1][0]  # fallback
    
    def generate_requirements(self, skill):
        """Generate realistic requirements based on skill"""
        requirements_templates = [
            f"أحتاج مساعدة في {skill.title} مع التركيز على الجوانب العملية والتطبيقية",
            f"أريد تعلم {skill.title} من البداية مع أمثلة واقعية",
            f"أحتاج تدريب متقدم في {skill.title} لتطوير مهاراتي المهنية",
            f"أريد مشروع عملي في {skill.title} يمكنني إضافته لمعرض أعمالي",
            f"أحتاج استشارة متخصصة في {skill.title} لحل مشكلة محددة في عملي"
        ]
        
        return self.get_random_choice(requirements_templates)
    
    def generate_delivery_notes(self, status):
        """Generate delivery notes based on order status"""
        if status == 'completed':
            notes = [
                "تم إنجاز العمل بجودة عالية وفي الوقت المحدد. العميل راضٍ جداً عن النتائج",
                "تم تسليم المشروع مع جميع الملفات المطلوبة والتوثيق الكامل",
                "العمل مكتمل بنجاح مع تقديم شرح مفصل وإرشادات للاستخدام",
                "تم الانتهاء من جميع المتطلبات مع إضافات قيمة لم تكن متوقعة"
            ]
        elif status == 'in_progress':
            notes = [
                "العمل يسير بشكل ممتاز، تم إنجاز 70% من المتطلبات",
                "في المرحلة الأخيرة من التنفيذ، متوقع الانتهاء خلال يومين",
                "تم الانتهاء من الجزء الأساسي، جاري العمل على التفاصيل النهائية"
            ]
        elif status == 'accepted':
            notes = [
                "تم قبول الطلب وسيبدأ العمل خلال 24 ساعة",
                "تم مراجعة المتطلبات والموافقة عليها، سنبدأ فوراً"
            ]
        elif status == 'cancelled':
            notes = [
                "تم إلغاء الطلب بناءً على طلب العميل",
                "تم الإلغاء بسبب عدم توافق في المتطلبات",
                "ألغي الطلب لظروف خارجة عن الإرادة"
            ]
        else:  # pending
            notes = ["", "في انتظار مراجعة المتطلبات"]
        
        return self.get_random_choice(notes) if notes[0] else ""
    
    def create_object(self, data):
        """Create order object matching the Order model exactly"""
        order, created = self.get_or_create_safe(
            Order,
            defaults={
                'seller': data['seller'],
                'skill': data['skill'],
                'points_amount': data['points_amount'],
                'platform_fee': data['platform_fee'],
                'total_points': data['total_points'],
                'status': data['status'],
                'requirements': data['requirements'],
                'delivery_notes': data['delivery_notes'],
                'created_at': data['created_at'],
                'accepted_at': data.get('accepted_at'),
                'started_at': data.get('started_at'),
                'completed_at': data.get('completed_at'),
                'cancelled_at': data.get('cancelled_at'),
                'expected_delivery': data.get('expected_delivery'),
                'actual_delivery': data.get('actual_delivery')
            },
            buyer=data['buyer'],
            skill=data['skill'],
            created_at=data['created_at']
        )
        
        if order:
            action = "Created" if created else "Updated"
            self.log_success(f"{action} order: {data['skill'].title} - {data['status']} - {data['points_amount']} points")
            return True
        
        return False

if __name__ == '__main__':
    seeder = OrdersSeeder()
    seeder.seed()
