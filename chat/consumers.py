import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from notifications.models import Notification

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        # التحقق من صلاحية الوصول للغرفة
        has_access = await self.check_room_access()
        if not has_access:
            await self.close()
            return

        # الانضمام لمجموعة الغرفة
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # إرسال الرسائل السابقة
        await self.send_previous_messages()

        # إشعار بالاتصال
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'status': 'online',
                'user_name': self.user.full_name
            }
        )

    async def disconnect(self, close_code):
        # إشعار بقطع الاتصال
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'status': 'offline',
                'user_name': self.user.full_name
            }
        )

        # مغادرة المجموعة
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'message')

            if message_type == 'message':
                await self.handle_message(text_data_json)
            elif message_type == 'typing':
                await self.handle_typing(text_data_json)
            elif message_type == 'read_receipt':
                await self.handle_read_receipt(text_data_json)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))

    async def handle_message(self, data):
        message_content = data.get('message', '').strip()
        if not message_content:
            return

        # حفظ الرسالة في قاعدة البيانات
        message = await self.save_message(message_content)
        if not message:
            return

        # إرسال الرسالة لجميع أعضاء الغرفة
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': message.id,
                'message': message_content,
                'user_id': self.user.id,
                'user_name': self.user.full_name,
                'user_avatar': self.user.avatar.url if self.user.avatar else None,
                'timestamp': message.created_at.isoformat(),
                'message_type': 'text'
            }
        )

        # إرسال إشعار للطرف الآخر
        await self.send_notification(message)

    async def handle_typing(self, data):
        is_typing = data.get('is_typing', False)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': self.user.id,
                'user_name': self.user.full_name,
                'is_typing': is_typing
            }
        )

    async def handle_read_receipt(self, data):
        message_id = data.get('message_id')
        if message_id:
            await self.mark_message_as_read(message_id)

    async def chat_message(self, event):
        # إرسال الرسالة للعميل
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': event['message_id'],
            'message': event['message'],
            'user_id': event['user_id'],
            'user_name': event['user_name'],
            'user_avatar': event['user_avatar'],
            'timestamp': event['timestamp'],
            'message_type': event['message_type']
        }))

    async def typing_indicator(self, event):
        # لا نرسل مؤشر الكتابة للمرسل نفسه
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user_id': event['user_id'],
                'user_name': event['user_name'],
                'is_typing': event['is_typing']
            }))

    async def user_status(self, event):
        # لا نرسل حالة المستخدم لنفسه
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'user_status',
                'user_id': event['user_id'],
                'user_name': event['user_name'],
                'status': event['status']
            }))

    @database_sync_to_async
    def check_room_access(self):
        """التحقق من صلاحية الوصول للغرفة"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            return chat_room.participants.filter(id=self.user.id).exists()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        """حفظ الرسالة في قاعدة البيانات"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            message = Message.objects.create(
                chat_room=chat_room,
                sender=self.user,
                content=content,
                message_type='text'
            )
            # تحديث وقت آخر نشاط في الغرفة
            chat_room.save()
            return message
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def send_previous_messages(self):
        """إرسال الرسائل السابقة عند الاتصال"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            messages = chat_room.messages.select_related('sender').order_by('-created_at')[:50]
            
            for message in reversed(messages):
                asyncio.create_task(self.send(text_data=json.dumps({
                    'type': 'message',
                    'message_id': message.id,
                    'message': message.content,
                    'user_id': message.sender.id,
                    'user_name': message.sender.full_name,
                    'user_avatar': message.sender.avatar.url if message.sender.avatar else None,
                    'timestamp': message.created_at.isoformat(),
                    'message_type': message.message_type,
                    'is_read': message.is_read
                })))
        except ChatRoom.DoesNotExist:
            pass

    @database_sync_to_async
    def send_notification(self, message):
        """إرسال إشعار للطرف الآخر"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            other_participants = chat_room.participants.exclude(id=self.user.id)
            
            for participant in other_participants:
                Notification.objects.create(
                    user=participant,
                    notification_type='message_received',
                    title=f'رسالة جديدة من {self.user.full_name}',
                    message=message.content[:100] + ('...' if len(message.content) > 100 else ''),
                    order=chat_room.order if hasattr(chat_room, 'order') else None
                )
        except ChatRoom.DoesNotExist:
            pass

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        """تحديد الرسالة كمقروءة"""
        try:
            message = Message.objects.get(id=message_id)
            if message.sender != self.user:
                message.is_read = True
                message.save()
        except Message.DoesNotExist:
            pass
