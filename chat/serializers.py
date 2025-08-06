from rest_framework import serializers
from .models import ChatRoom, Message
from accounts.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'message_type', 'content', 'file',
            'is_read', 'created_at'
        ]

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserProfileSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'participants', 'order', 'is_active',
            'last_message', 'created_at', 'updated_at'
        ]

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
