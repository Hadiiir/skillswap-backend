import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

class NotificationService:
    """خدمة الإشعارات المتقدمة"""
    
    @staticmethod
    def create_notification(user, notification_type, title, message, **kwargs):
        """إنشاء إشعار جديد"""
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            **kwargs
        )
        
        NotificationService.send_realtime_notification(user, notification)
        
        if user.email_notifications:
            NotificationService.send_email_notification(user, notification)
        
        if user.push_notifications:
            NotificationService.send_push_notification(user, notification)
        
        return notification
    
    @staticmethod
    def send_realtime_notification(user, notification):
        """إرسال إشعار فوري عبر WebSocket"""
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{user.id}',
                {
                    'type': 'notification_message',
                    'notification': {
                        'id': notification.id,
                        'type': notification.notification_type,
                        'title': notification.title,
                        'message': notification.message,
                        'created_at': notification.created_at.isoformat(),
                        'is_read': notification.is_read
                    }
                }
            )
        except Exception as e:
            print(f"Error sending realtime notification: {e}")
    
    @staticmethod
    def send_email_notification(user, notification):
        """إرسال إشعار عبر البريد الإلكتروني"""
        try:
            html_content = render_to_string('emails/notification.html', {
                'user': user,
                'notification': notification,
                'site_url': settings.FRONTEND_URL
            })
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = notification.title
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = user.email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(msg)
                
        except Exception as e:
            print(f"Error sending email notification: {e}")
    
    @staticmethod
    def send_push_notification(user, notification):
        """إرسال push notification"""
        try:
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {settings.ONESIGNAL_API_KEY}'
            }
            
            payload = {
                'app_id': settings.ONESIGNAL_APP_ID,
                'include_external_user_ids': [str(user.id)],
                'headings': {'en': notification.title},
                'contents': {'en': notification.message},
                'data': {
                    'notification_id': notification.id,
                    'type': notification.notification_type
                }
            }
            
            response = requests.post(
                'https://onesignal.com/api/v1/notifications',
                json=payload,
                headers=headers
            )
            
            return response.json()
            
        except Exception as e:
            print(f"Error sending push notification: {e}")
    
    @staticmethod
    def send_order_notifications(order, status_change):
        """إرسال إشعارات خاصة بالطلبات"""
        notifications_map = {
            'created': {
                'buyer': ('تم إنشاء طلبك', f'تم إنشاء طلبك لمهارة "{order.skill.title}" بنجاح'),
                'seller': ('طلب جديد', f'لديك طلب جديد لمهارة "{order.skill.title}"')
            },
            'accepted': {
                'buyer': ('تم قبول طلبك', f'تم قبول طلبك لمهارة "{order.skill.title}"'),
                'seller': ('تم قبول الطلب', f'تم قبول طلب مهارة "{order.skill.title}"')
            },
            'completed': {
                'buyer': ('تم إكمال طلبك', f'تم إكمال طلبك لمهارة "{order.skill.title}"'),
                'seller': ('تم إكمال الطلب', f'تم إكمال طلب مهارة "{order.skill.title}"')
            },
            'cancelled': {
                'buyer': ('تم إلغاء طلبك', f'تم إلغاء طلبك لمهارة "{order.skill.title}"'),
                'seller': ('تم إلغاء الطلب', f'تم إلغاء طلب مهارة "{order.skill.title}"')
            }
        }
        
        if status_change in notifications_map:

            buyer_title, buyer_message = notifications_map[status_change]['buyer']
            NotificationService.create_notification(
                user=order.buyer,
                notification_type=f'order_{status_change}',
                title=buyer_title,
                message=buyer_message,
                order=order,
                skill=order.skill
            )
            
            seller_title, seller_message = notifications_map[status_change]['seller']
            NotificationService.create_notification(
                user=order.seller,
                notification_type=f'order_{status_change}',
                title=seller_title,
                message=seller_message,
                order=order,
                skill=order.skill
            )
