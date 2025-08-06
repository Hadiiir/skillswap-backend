#!/usr/bin/env python
"""
Notifications Seeder for SkillSwap
Seeds notifications matching the Notification model exactly
"""
import os
import sys
import django
from pathlib import Path
import random
from datetime import timedelta

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from base_seeder import BaseSeeder
from notifications.models import Notification
from points.models import Order
from accounts.models import User
from skills.models import Skill
from django.utils import timezone

class NotificationsSeeder(BaseSeeder):
    """Seeder for notifications matching the Notification model exactly"""
    
    def get_dependencies(self):
        """Notifications depend on Orders, Users, and Skills"""
        return ['points.Order', 'accounts.User', 'skills.Skill']
    
    def get_data(self):
        """Generate notifications data based on existing orders and activities"""
        notifications_data = []
        
        # Get recent orders for generating notifications
        orders = Order.objects.all().order_by('-created_at')[:30]
        users = list(User.objects.filter(is_active=True, is_superuser=False))
        skills = list(Skill.objects.filter(status='active'))
        
        # Generate order-related notifications
        for order in orders:
            # Order created notification for seller
            notifications_data.append({
                'user': order.seller,
                'notification_type': 'order_created',
                'title': 'طلب جديد على مهارتك',
                'message': f'تم إنشاء طلب جديد على مهارة "{order.skill.title}" من قبل {order.buyer.get_full_name()}',
                'order': order,
                'skill': order.skill,
                'is_read': random.choice([True, False]),
                'created_at': order.created_at
            })
            
            # Order accepted notification for buyer
            if order.accepted_at:
                notifications_data.append({
                    'user': order.buyer,
                    'notification_type': 'order_accepted',
                    'title': 'تم قبول طلبك',
                    'message': f'تم قبول طلبك لمهارة "{order.skill.title}" من قبل {order.seller.get_full_name()}',
                    'order': order,
                    'skill': order.skill,
                    'is_read': random.choice([True, False]),
                    'created_at': order.accepted_at
                })
            
            # Order completed notifications
            if order.status == 'completed':
                # Notification for buyer
                notifications_data.append({
                    'user': order.buyer,
                    'notification_type': 'order_completed',
                    'title': 'تم إكمال طلبك',
                    'message': f'تم إكمال طلبك لمهارة "{order.skill.title}" بنجاح. يمكنك الآن تقييم التجربة.',
                    'order': order,
                    'skill': order.skill,
                    'is_read': random.choice([True, False]),
                    'created_at': order.completed_at or order.created_at + timedelta(days=7)
                })
                
                # Notification for seller
                notifications_data.append({
                    'user': order.seller,
                    'notification_type': 'order_completed',
                    'title': 'تم إكمال الطلب',
                    'message': f'تم إكمال طلب "{order.skill.title}" بنجاح. تم إضافة النقاط إلى رصيدك.',
                    'order': order,
                    'skill': order.skill,
                    'is_read': random.choice([True, False]),
                    'created_at': order.completed_at or order.created_at + timedelta(days=7)
                })
            
            # Order cancelled notifications
            if order.status == 'cancelled':
                # Notification for buyer
                notifications_data.append({
                    'user': order.buyer,
                    'notification_type': 'order_cancelled',
                    'title': 'تم إلغاء طلبك',
                    'message': f'تم إلغاء طلبك لمهارة "{order.skill.title}". تم إرجاع النقاط إلى رصيدك.',
                    'order': order,
                    'skill': order.skill,
                    'is_read': random.choice([True, False]),
                    'created_at': order.cancelled_at or order.created_at + timedelta(days=1)
                })
                
                # Notification for seller
                notifications_data.append({
                    'user': order.seller,
                    'notification_type': 'order_cancelled',
                    'title': 'تم إلغاء طلب',
                    'message': f'تم إلغاء طلب "{order.skill.title}" من قبل {order.buyer.get_full_name()}.',
                    'order': order,
                    'skill': order.skill,
                    'is_read': random.choice([True, False]),
                    'created_at': order.cancelled_at or order.created_at + timedelta(days=1)
                })
        
        # Generate review notifications
        from reviews.models import Review
        reviews = Review.objects.all().order_by('-created_at')[:20]
        
        for review in reviews:
            notifications_data.append({
                'user': review.reviewee,
                'notification_type': 'review_received',
                'title': 'تقييم جديد',
                'message': f'حصلت على تقييم {review.rating} نجوم من {review.reviewer.get_full_name()} على مهارة "{review.skill.title}"',
                'order': review.order,
                'skill': review.skill,
                'is_read': random.choice([True, False]),
                'created_at': review.created_at
            })
        
        # Generate points-related notifications
        for user in random.sample(users, min(10, len(users))):
            # Points earned notification
            notifications_data.append({
                'user': user,
                'notification_type': 'points_earned',
                'title': 'تم إضافة نقاط إلى رصيدك',
                'message': f'تم إضافة {random.randint(50, 200)} نقطة إلى رصيدك بعد إكمال طلب بنجاح',
                'is_read': random.choice([True, False]),
                'created_at': timezone.now() - timedelta(days=random.randint(1, 30))
            })
            
            # Points purchased notification
            if random.choice([True, False]):
                notifications_data.append({
                    'user': user,
                    'notification_type': 'points_purchased',
                    'title': 'تم شراء نقاط بنجاح',
                    'message': f'تم شراء {random.randint(100, 500)} نقطة بنجاح وإضافتها إلى رصيدك',
                    'is_read': random.choice([True, False]),
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 15))
                })
        
        # Generate system notifications
        system_notifications = [
            {
                'title': 'مرحباً بك في منصة تبادل المهارات',
                'message': 'نرحب بك في منصتنا! استكشف المهارات المتاحة وابدأ رحلة التعلم والتعليم معنا.',
                'notification_type': 'system'
            },
            {
                'title': 'تحديث جديد على المنصة',
                'message': 'تم إضافة ميزات جديدة لتحسين تجربتك. اكتشف الآن!',
                'notification_type': 'system'
            },
            {
                'title': 'نصائح لتحسين ملفك الشخصي',
                'message': 'أضف صورة شخصية ووصف مفصل لمهاراتك لجذب المزيد من العملاء.',
                'notification_type': 'system'
            }
        ]
        
        for user in random.sample(users, min(15, len(users))):
            system_notif = self.get_random_choice(system_notifications)
            notifications_data.append({
                'user': user,
                'notification_type': system_notif['notification_type'],
                'title': system_notif['title'],
                'message': system_notif['message'],
                'is_read': random.choice([True, False]),
                'created_at': timezone.now() - timedelta(days=random.randint(1, 60))
            })
        
        return notifications_data
    
    def create_object(self, data):
        """Create notification object matching the Notification model exactly"""
        notification, created = self.get_or_create_safe(
            Notification,
            defaults={
                'notification_type': data['notification_type'],
                'title': data['title'],
                'message': data['message'],
                'is_read': data['is_read'],
                'order': data.get('order'),
                'skill': data.get('skill'),
                'created_at': data['created_at']
            },
            user=data['user'],
            title=data['title'],
            created_at=data['created_at']
        )
        
        if notification:
            action = "Created" if created else "Updated"
            read_status = "read" if data['is_read'] else "unread"
            self.log_success(f"{action} notification: {data['notification_type']} - {read_status}")
            return True
        
        return False

if __name__ == '__main__':
    seeder = NotificationsSeeder()
    seeder.seed()
