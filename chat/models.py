from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    order = models.OneToOneField('points.Order', on_delete=models.CASCADE, related_name='order_chat_room')
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Chat Room')
        verbose_name_plural = _('Chat Rooms')

    def __str__(self):
        return f"Chat for Order #{self.order.id}"

class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', _('Text')),
        ('image', _('Image')),
        ('file', _('File')),
        ('system', _('System')),
    ]

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(_('message type'), max_length=80, choices=MESSAGE_TYPES, default='text')
    content = models.TextField(_('content'), blank=True)
    file = models.FileField(_('file'), upload_to='chat/files/', blank=True, null=True)
    is_read = models.BooleanField(_('is read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.full_name}: {self.content[:50]}"
