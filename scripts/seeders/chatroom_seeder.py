# chatroom_seeder.py
from chat.models import ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoomSeeder:
    def __init__(self):
        self.created_count = 0
        self.updated_count = 0
        self.errors = []

    def seed(self):
        try:
            user1 = User.objects.get(email='ahmed.developer@skillswap.com')
            user2 = User.objects.get(email='sara.designer@skillswap.com')
            room, created = ChatRoom.objects.get_or_create(name="Dev-Design")
            room.participants.set([user1, user2])
            room.save()

            if created:
                self.created_count += 1
            else:
                self.updated_count += 1

        except Exception as e:
            self.errors.append(str(e))
