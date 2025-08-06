from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Chat Rooms
    path('rooms/', views.ChatRoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', views.ChatRoomDetailView.as_view(), name='room-detail'),
    
    # Messages
    path('rooms/<int:pk>/messages/', views.MessageListView.as_view(), name='messages'),
    path('rooms/<int:pk>/send/', views.SendMessageView.as_view(), name='send-message'),
]
