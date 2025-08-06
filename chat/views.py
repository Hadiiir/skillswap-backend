from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomListView(APIView):
    """
    Chat Rooms List API
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get user's chat rooms",
        responses={200: ChatRoomSerializer(many=True)},
        tags=['Chat']
    )
    def get(self, request):
        rooms = ChatRoom.objects.filter(
            participants=request.user
        ).order_by('-updated_at')
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data)

class ChatRoomDetailView(APIView):
    """
    Chat Room Detail API
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return ChatRoom.objects.get(pk=pk, participants=user)
        except ChatRoom.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Get chat room detail",
        responses={200: ChatRoomSerializer},
        tags=['Chat']
    )
    def get(self, request, pk):
        room = self.get_object(pk, request.user)
        if not room:
            return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)

class MessageListView(APIView):
    """
    Messages List API
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get messages in a chat room",
        responses={200: MessageSerializer(many=True)},
        tags=['Chat']
    )
    def get(self, request, pk):
        try:
            # Verify user has access to this chat room
            ChatRoom.objects.get(pk=pk, participants=request.user)
            
            messages = Message.objects.filter(
                chat_room_id=pk
            ).order_by('created_at')
            
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)

class SendMessageView(APIView):
    """
    Send Message API
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Send a message in a chat room",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Message content')
            },
            required=['content']
        ),
        responses={201: MessageSerializer},
        tags=['Chat']
    )
    def post(self, request, pk):
        try:
            chat_room = ChatRoom.objects.get(pk=pk, participants=request.user)
            content = request.data.get('content', '')
            
            if not content.strip():
                return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            message = Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content
            )
            
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)
