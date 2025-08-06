from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order_created', _('Order Created')),
        ('order_accepted', _('Order Accepted')),
        ('order_completed', _('Order Completed')),
        ('order_cancelled', _('Order Cancelled')),
        ('message_received', _('Message Received')),
        ('review_received', _('Review Received')),
        ('points_purchased', _('Points Purchased')),
        ('points_earned', _('Points Earned')),
        ('system', _('System Notification')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(_('notification type'), max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(_('title'), max_length=200)
    message = models.TextField(_('message'))
    is_read = models.BooleanField(_('is read'), default=False)
    
    # Related objects
    order = models.ForeignKey('points.Order', on_delete=models.CASCADE, null=True, blank=True)
    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"
